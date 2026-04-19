"""
GreenThumb AI — FastAPI Backend
Handles: image upload → EfficientNet → RAG → LLM → structured diagnosis
"""

import os
import sys
import subprocess
import time
import requests
import io
import json
import logging
from pathlib import Path
from contextlib import asynccontextmanager

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("greenthumb")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
MODEL_PATH = BASE_DIR / "models" / "efficientnet_b0_best.pth"
KB_DIR = BASE_DIR / "knowledge_base" / "chromadb"

# ── PlantVillage class labels (38 classes, alphabetical as torchvision loads) ──
CLASS_NAMES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___healthy",
]

def parse_class_name(class_name: str):
    """Parse 'Tomato___Early_blight' → ('Tomato', 'Early blight')"""
    parts = class_name.split("___")
    crop = parts[0].replace("_", " ").strip()
    disease = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown"
    return crop, disease


# ── Ollama auto-start ──────────────────────────────────────────────────────────

def is_ollama_running() -> bool:
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def start_ollama():
    if is_ollama_running():
        logger.info("Ollama already running.")
        return
    logger.info("Starting Ollama server...")
    subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    )
    for _ in range(20):
        time.sleep(1)
        if is_ollama_running():
            logger.info("Ollama started successfully.")
            return
    logger.warning("Ollama did not start in time — LLM features may be unavailable.")


# ── EfficientNet model loader ──────────────────────────────────────────────────

def load_efficientnet(num_classes: int = 38):
    model = models.efficientnet_b0(weights=None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    if MODEL_PATH.exists():
        state = torch.load(MODEL_PATH, map_location="cpu")
        model.load_state_dict(state)
        logger.info(f"Loaded EfficientNet weights from {MODEL_PATH}")
    else:
        logger.warning(f"Model weights not found at {MODEL_PATH} — using random weights (for demo)")
    model.eval()
    return model

TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

# ── App lifecycle ──────────────────────────────────────────────────────────────

cv_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global cv_model
    logger.info("GreenThumb AI backend starting up...")
    start_ollama()
    cv_model = load_efficientnet()
    # Pre-warm ChromaDB + sentence transformer only (no LLM call)
    try:
        logger.info("Pre-warming ChromaDB + embeddings...")
        import sys
        sys.path.insert(0, str(BASE_DIR))
        from src.rag.rag_retriever import RAGRetriever
        _ = RAGRetriever()   # loads ChromaDB and sentence transformer
        logger.info("✅ ChromaDB ready.")
    except Exception as e:
        logger.warning(f"ChromaDB pre-warm skipped: {e}")
    yield
    logger.info("Shutting down.")

app = FastAPI(
    title="GreenThumb AI",
    description="Knowledge-Verified Visual Diagnosis for Plant Disease Detection",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── RAG pipeline (lazy import to avoid circular deps) ─────────────────────────

_rag_loaded = False

def run_rag_pipeline(crop: str, disease: str, confidence: float) -> dict:
    global _rag_loaded
    import sys
    sys.path.insert(0, str(BASE_DIR))
    
    # Import fresh each time until loaded — handles the HF init delay
    from src.rag.inference import diagnose
    return diagnose(crop, disease, confidence)
    
# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "ok", "message": "GreenThumb AI API is running"}

@app.get("/health")
def health():
    return {
        "api": "ok",
        "ollama": is_ollama_running(),
        "cv_model": cv_model is not None,
    }

@app.post("/diagnose")
async def diagnose_image(file: UploadFile = File(...)):
    """
    Main endpoint: receive image → CV → RAG → return diagnosis.
    """
    # 1. Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # 2. Load and preprocess image
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read image: {e}")

    # 3. CV inference
    try:
        tensor = TRANSFORM(image).unsqueeze(0)
        with torch.no_grad():
            logits = cv_model(tensor)
            probs  = torch.softmax(logits, dim=1)[0]
            top_conf, top_idx = torch.topk(probs, k=3)

        pred_idx   = top_idx[0].item()
        confidence = top_conf[0].item()
        pred_class = CLASS_NAMES[pred_idx]
        crop, disease = parse_class_name(pred_class)

        top3 = [
            {
                "class": CLASS_NAMES[top_idx[i].item()],
                "confidence": round(top_conf[i].item(), 4)
            }
            for i in range(3)
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CV inference failed: {e}")

    # 4. Handle healthy prediction — skip RAG
    if "healthy" in disease.lower():
        return {
            "status": "HEALTHY",
            "crop": crop,
            "disease": "Healthy",
            "cv_confidence": round(confidence, 4),
            "message": f"The {crop} plant appears healthy. No disease detected.",
            "top3_predictions": top3,
        }

    # 5. RAG pipeline
    try:
        rag_result = run_rag_pipeline(crop, disease, confidence)
    except Exception as e:
        logger.error(f"RAG pipeline error: {e}")
        # Graceful fallback — return CV result without RAG
        return {
            "status": "CV_ONLY",
            "crop": crop,
            "disease": disease,
            "cv_confidence": round(confidence, 4),
            "message": "RAG pipeline unavailable — CV prediction only.",
            "top3_predictions": top3,
        }

    # 6. Attach top3 to result and return
    rag_result["top3_predictions"] = top3
    return rag_result
