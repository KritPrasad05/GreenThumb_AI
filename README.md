# 🌿 GreenThumb AI

### Knowledge-Verified Visual Diagnosis for Plant Disease Detection

*A Research System Combining EfficientNet-B0 with Retrieval-Augmented Generation*

---

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-6B46C1?style=flat-square)](https://trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Research](https://img.shields.io/badge/Institution-SRM_University-navy?style=flat-square)](https://srmist.edu.in)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Research Context](#-research-context)
- [System Architecture](#-system-architecture)
- [Results](#-results)
- [Repository Structure](#-repository-structure)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Research Paper](#-research-paper)
- [Contributors](#-contributors)
- [Future Work](#-future-work)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🔬 Overview

**GreenThumb AI** is an academic research system that addresses a critical challenge in precision agriculture: *reliable, explainable plant disease diagnosis from leaf images*. Existing deep learning approaches achieve high accuracy on benchmark datasets but suffer from two well-documented failure modes — **overconfident predictions on out-of-distribution images** and **lack of verifiable, knowledge-grounded explanations**.

This system proposes a novel two-stage pipeline that combines:

1. **Computer Vision (EfficientNet-B0)** — fine-tuned on the PlantVillage dataset (38 classes, ~54,000 images) to classify plant diseases from leaf photographs with **99.73% validation accuracy** and **99.80% test accuracy**.

2. **Retrieval-Augmented Generation (RAG)** — a knowledge verification layer that cross-checks the CV model's prediction against a curated scientific knowledge base (sourced from the EPPO Global Database) before issuing a final diagnosis. An LLM (phi3:mini via Ollama) synthesises the evidence into a structured, human-readable report.

3. **Decision Gate** — a formal scoring function (Equations 8 & 9 in the paper) that computes a *consistency score* S ∈ [0, 1] across four components (label match, confidence alignment, evidence overlap, evidence strength). Predictions below the threshold τ = 0.70 are **explicitly refused** rather than silently passed through.

### What Problem Does It Solve?

| Challenge | Traditional CV | GreenThumb AI |
|-----------|---------------|---------------|
| Out-of-distribution images | Silent wrong answer | Explicit REFUSE |
| Explainability | Confidence score only | Full evidence report |
| Knowledge grounding | None | EPPO scientific database |
| Crop-disease consistency | Not checked | Hard veto enforced |
| LLM hallucination risk | N/A | Gate prevents unchecked output |

---

## 🎓 Research Context

This system was developed as part of an undergraduate research project at:

> **Department of Computer Science and Business Systems**
> **SRM Institute of Science and Technology, Kattankulathur**
> Academic Year 2024–25

The associated research paper, *"Knowledge-Verified Visual Diagnosis for Plant Disease Detection Using EfficientNet-B0 and Retrieval-Augmented Generation"*, has been submitted for publication. The full paper is available in this repository under [`docs/research_paper.pdf`](docs/research_paper.pdf).

The work contributes to the intersection of:
- **Precision Agriculture** and AI-assisted crop health monitoring
- **Trustworthy AI** — refusal mechanisms and uncertainty quantification
- **Retrieval-Augmented Generation** applied to domain-specific knowledge
- **Multi-modal knowledge systems** combining vision and text

---

## 🏗 System Architecture

```
Input Image
     │
     ▼
┌─────────────────────────────────────────────┐
│          STAGE 1 — COMPUTER VISION          │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  EfficientNet-B0 (fine-tuned)        │   │
│  │  PlantVillage Dataset — 38 classes   │   │
│  │  Input: 224×224 RGB leaf image       │   │
│  │  Output: class label + confidence    │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
     │
     │  pred_class, confidence ∈ [0,1]
     ▼
┌─────────────────────────────────────────────┐
│      STAGE 2 — RAG KNOWLEDGE RETRIEVAL      │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  Query Builder                       │   │
│  │  "{crop} {disease} symptoms ..."     │   │
│  └─────────────────┬────────────────────┘   │
│                    │                        │
│  ┌─────────────────▼────────────────────┐   │
│  │  ChromaDB Vector Store               │   │
│  │  all-MiniLM-L6-v2 embeddings         │   │
│  │  26 disease entries (EPPO + curated) │   │
│  │  Hard filter: WHERE crop = pred_crop │   │
│  └─────────────────┬────────────────────┘   │
└─────────────────────────────────────────────┘
     │
     │  top_hit: {document, metadata, similarity}
     ▼
┌─────────────────────────────────────────────┐
│         STAGE 3 — DECISION GATE             │
│                                             │
│  S = w1·LabelMatch + w2·ConfAlignment       │
│      + w3·EvidenceOverlap + w4·EvidenceStr  │
│                                             │
│  S ≥ 0.70 → ACCEPT   S < 0.70 → REFUSE      │
│  Crop mismatch → VETO (S = 0 always)        │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│        STAGE 4 — LLM SYNTHESIS              │
│                                             │
│  phi3:mini (Ollama) generates:              │
│  • Diagnostic reasoning paragraph           │
│  • Evidence summary                         │
│  • Enriched query (for transparency)        │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│              FINAL OUTPUT                   │
│                                             │
│  ACCEPTED → disease, pathogen, EPPO code,  │
│             symptoms, treatment, prevention │
│  REFUSED  → explanation + suggestions      │
│  HEALTHY  → confirmation message            │
└─────────────────────────────────────────────┘
```

### Component Weights (Decision Gate)

| Component | Symbol | Weight |
|-----------|--------|--------|
| Label Match | f₁ | 0.35 |
| Confidence Alignment | f₂ | 0.25 |
| Evidence Overlap | f₃ | 0.20 |
| Evidence Strength | f₄ | 0.20 |

---

## 📊 Results

### CV Model Performance (15-Epoch Training)

| Epoch | Train Loss | Val Loss | Val Accuracy |
|-------|-----------|---------|-------------|
| 1 | 0.4481 | 0.0387 | 98.88% |
| 5 | 0.0207 | 0.0169 | 99.58% |
| 10 | 0.0109 | 0.0094 | **99.73%** |
| 15 | 0.0035 | 0.0069 | **99.80%** |

### Confidence Distribution

| Split | Mean Confidence | Min Confidence |
|-------|----------------|----------------|
| In-Distribution (Test) | 99.94% | 53.31% |
| Out-of-Distribution (Perturbed) | 88.20% | 9.99% |

The OOD confidence distribution shows a clear leftward shift, validating that the Decision Gate's refusal mechanism activates appropriately on ambiguous inputs.

---

## 📁 Repository Structure

```
GreenThumb_AI/
│
├── 📂 assets/                    # Static assets
│   └── banner.png                # Repository banner image
│
├── 📂 backend/                   # FastAPI REST API
│   └── main.py                   # API endpoints, model loading, pipeline orchestration
│
├── 📂 frontend/                  # Streamlit web interface
│   └── app.py                    # Chat-style UI with camera/upload support
│
├── 📂 Notebooks/                 # Jupyter research notebooks
│   ├── 01_EDA.ipynb              # Dataset exploration & class distribution
│   ├── 02_Data_Pipeline.ipynb    # Augmentation pipeline & dataloader validation
│   ├── 03_Training.ipynb         # EfficientNet-B0 training with mixed precision
│   └── 04_Evaluation.ipynb       # Metrics, confusion matrix, confidence analysis
│
├── 📂 src/                       # Core source code
│   ├── 📂 data/                  # Data loading & transformation
│   │   ├── __init__.py
│   │   ├── datamodule.py         # Train/val/test split, DataLoader wrappers
│   │   ├── dataset.py            # PlantVillageDataset (PyTorch Dataset)
│   │   └── transforms.py        # ImageNet-normalised augmentation pipelines
│   │
│   └── 📂 rag/                   # Retrieval-Augmented Generation system
│       ├── decision_gate.py      # Consistency scoring & ACCEPT/REFUSE logic
│       ├── disease_aliases.py    # Disease → pathogen name resolution table
│       ├── disease_seed.py       # Expert-curated knowledge for 26 diseases
│       ├── eppo_client.py        # EPPO Global Database API client
│       ├── eppo_ingest.py        # One-time data ingestion from EPPO API
│       ├── eppo_mapping.py       # EPPO code lookup & candidate ranking
│       ├── inference.py          # End-to-end RAG inference pipeline
│       ├── kb_builder.py         # Builds ChromaDB vector store from raw EPPO data
│       ├── llm_client.py         # Ollama LLM integration (phi3:mini)
│       ├── plantvillage_classes.py # Dataset class name parsing
│       └── rag_retriever.py      # ChromaDB query with crop-level filtering
│
├── 📂 models/                    # Saved model weights (not tracked in git)
│   └── efficientnet_b0_best.pth  # Best checkpoint (99.80% test accuracy)
│
├── 📂 knowledge_base/            # RAG knowledge store
│   ├── 📂 raw_eppo/              # Raw JSON from EPPO API (26 disease files)
│   └── 📂 chromadb/              # Persisted ChromaDB vector index
│
├── 📂 data/                      # Dataset (not tracked in git)
│   └── plantvillage dataset/
│       └── color/                # 38 class folders, ~54,000 images
│
├── 📂 outputs/                   # Generated outputs from training/evaluation
│   ├── 📂 plots/                 # Loss curves, confusion matrix, confidence charts
│   └── 📂 metrics/               # CSV files with per-sample confidence scores
│
├── 📂 docs/                      # Research documentation
│   └── research_paper.pdf        # Full research paper (PDF)
│
├── run_app.py                    # One-command launcher (Ollama + FastAPI + Streamlit)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## ⚙️ Installation

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | 3.11 recommended |
| CUDA | 11.8+ | Optional — CPU inference supported |
| Ollama | Latest | Required for LLM synthesis |
| Git | Any | For cloning |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/KritPrasad05/GreenThumb_AI.git
cd GreenThumb_AI
```

### Step 2 — Create a Virtual Environment

```bash
# Using venv (recommended)
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

<details>
<summary>Core dependencies (click to expand)</summary>

```
torch>=2.0.0
torchvision>=0.15.0
fastapi>=0.100.0
uvicorn>=0.23.0
streamlit>=1.30.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
ollama>=0.1.0
Pillow>=10.0.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
pandas>=2.0.0
requests>=2.31.0
python-dotenv>=1.0.0
beautifulsoup4>=4.12.0
```

</details>

### Step 4 — Install and Configure Ollama

```bash
# Download Ollama from https://ollama.ai
# Then pull the required model:
ollama pull phi3:mini
```

### Step 5 — Download the Dataset

Download the [PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease) and place it at:

```
data/plantvillage dataset/color/
```

The directory should contain 38 class folders (e.g., `Tomato___Early_blight`, `Apple___healthy`, etc.).

### Step 6 — Build the Knowledge Base

The ChromaDB vector store must be built once before running the system:

```bash
python -m src.rag.kb_builder
```

Expected output:
```
[START] Building ChromaDB KB
✅ 26 documents in ChromaDB 'plant_disease_kb'
```

### Step 7 — (Optional) Train the CV Model

If you want to reproduce training from scratch (requires GPU + dataset):

```bash
# Run notebook interactively
jupyter notebook Notebooks/03_Training.ipynb
```

Pre-trained weights (`efficientnet_b0_best.pth`) can be downloaded from the [Releases](https://github.com/<your-username>/GreenThumb_AI/releases) page and placed in the `models/` directory.

---

## 🚀 Usage Guide

### Option A — One-Command Launch (Recommended)

This starts Ollama, FastAPI, and Streamlit in the correct order:

```bash
python run_app.py
```

Then open your browser at:
- **Frontend:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs

### Option B — Manual Launch

**Terminal 1 — Start Ollama:**
```bash
ollama serve
```

**Terminal 2 — Start FastAPI backend:**
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 3 — Start Streamlit frontend:**
```bash
streamlit run frontend/app.py --server.port 8501
```

### Option C — API Only (Programmatic Use)

```python
import requests

with open("leaf_image.jpg", "rb") as f:
    response = requests.post(
        "http://127.0.0.1:8000/diagnose",
        files={"file": ("leaf.jpg", f, "image/jpeg")},
        timeout=120
    )

result = response.json()
print(f"Status:      {result['status']}")
print(f"Disease:     {result.get('disease', 'N/A')}")
print(f"Confidence:  {result.get('cv_confidence', 0):.1%}")
print(f"Consistency: {result.get('consistency_score', 0):.2f}")
```

### Expected API Response — ACCEPTED

```json
{
  "status": "ACCEPTED",
  "disease": "Early blight",
  "crop": "Tomato",
  "pathogen": "Alternaria solani",
  "eppo_code": "ALTESO",
  "cv_confidence": 0.9987,
  "consistency_score": 0.83,
  "llm_reasoning": "The EfficientNet-B0 model's prediction of Early blight on Tomato is strongly supported by the retrieved knowledge base entry...",
  "component_scores": {
    "label_match": 0.90,
    "conf_alignment": 0.81,
    "evidence_overlap": 0.75,
    "evidence_strength": 0.84
  },
  "supporting_evidence": {
    "symptoms": "Concentric ring 'bull's eye' lesions on older lower leaves...",
    "causes": "Fungus Alternaria solani; favored by warm temperatures...",
    "treatment": "Chlorothalonil, mancozeb, or copper fungicides...",
    "prevention": "Crop rotation; mulching; adequate calcium and nitrogen..."
  },
  "top3_predictions": [
    {"class": "Tomato___Early_blight", "confidence": 0.9987},
    {"class": "Tomato___Septoria_leaf_spot", "confidence": 0.0008},
    {"class": "Tomato___Late_blight", "confidence": 0.0003}
  ]
}
```

### Expected API Response — REFUSED

```json
{
  "status": "REFUSED",
  "pred_disease": "Late blight",
  "crop": "Potato",
  "cv_confidence": 0.61,
  "consistency_score": 0.54,
  "llm_reasoning": "The prediction falls below the 0.70 consistency threshold...",
  "suggestions": [
    "Re-upload a clearer, well-lit image of the affected leaf.",
    "Ensure the diseased area is centered and in focus.",
    "Avoid images with soil, multiple leaves, or heavy shadows."
  ]
}
```

### Health Check

```bash
curl http://127.0.0.1:8000/health
```
```json
{"api": "ok", "ollama": true, "cv_model": true}
```

---

## 📄 Research Paper

The full research paper documenting the methodology, experiments, and findings is included in this repository:

**📥 [`docs/research_paper.pdf`](docs/research_paper.pdf)**

**Title:** *Knowledge-Verified Visual Diagnosis for Plant Disease Detection Using EfficientNet-B0 and Retrieval-Augmented Generation*

**Abstract summary:**
This paper presents a hybrid CV-RAG architecture for plant disease diagnosis that achieves 99.80% test accuracy on the PlantVillage dataset while incorporating an explicit knowledge-verification layer to prevent overconfident predictions. We propose a four-component consistency scoring function and a formal decision gate that either accepts, refuses, or escalates predictions based on alignment between visual evidence and a curated scientific knowledge base. Experiments demonstrate that the OOD confidence distribution shifts significantly (mean: 99.94% → 88.20%), validating the refusal mechanism's sensitivity to ambiguous inputs.

**Key Contributions:**
1. A novel CV + RAG pipeline for knowledge-grounded plant disease diagnosis
2. A formal decision gate with crop-level hard veto and four-component scoring
3. Comparative analysis of ID vs OOD confidence distributions
4. An open-source implementation with REST API and conversational frontend

---

## 👥 Contributors

| Name | Role | Contributions |
|------|------|--------------|
| **Krit Prasad** | Lead Developer & Researcher | CV Model · RAG Pipeline · System Architecture · API · Frontend |
| **Karthikeyan** | Research Contributor | Knowledge Base · Evaluation · EPPO Integration |
| **Badra** | Research Contributor | Data Pipeline · Experiments · Notebook Documentation |

*All contributors are B.Tech Computer Science & Business Systems students at SRM Institute of Science and Technology, Kattankulathur.*

---

## 🔭 Future Work

The following directions are identified for extending this research:

| Direction | Description | Priority |
|-----------|-------------|----------|
| **Field images** | Re-train on real-world field photographs rather than controlled laboratory images | High |
| **More crops** | Extend beyond PlantVillage's 14 crops to cover rice, wheat, and pulses | High |
| **Confidence calibration** | Apply temperature scaling to improve probability calibration | Medium |
| **Active learning** | Use refused predictions as training signal for continual learning | Medium |
| **Multilingual LLM** | Support diagnosis reports in regional Indian languages | Medium |
| **Mobile deployment** | Quantise EfficientNet-B0 for on-device inference (ONNX/TFLite) | Medium |
| **Multi-image input** | Accept multiple leaf images to improve diagnostic robustness | Low |
| **Severity grading** | Add disease severity estimation (mild / moderate / severe) | Low |
| **Feedback loop** | Collect expert corrections to iteratively improve the knowledge base | Low |

---

## 🤝 Contributing

Contributions to extend this research are welcome. Please follow these guidelines:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow the code style** — keep module separation clean (CV in `src/data/`, RAG in `src/rag/`, API in `backend/`).

3. **Document your changes** — update relevant docstrings and this README if adding new components.

4. **Add tests** if extending the decision gate or retrieval logic.

5. **Open a Pull Request** with a clear description of what was changed and why.

**Areas particularly welcoming contributions:**
- Additional disease entries for the knowledge base (`src/rag/disease_seed.py`)
- New crop categories and EPPO mappings
- Alternative embedding models for ChromaDB
- Improved LLM prompts for better reasoning quality
- Frontend improvements (accessibility, mobile responsiveness)

---

## 📬 Contact

For research collaboration, academic inquiries, or questions about this work:

**Krit Prasad**
- 🎓 B.Tech CSBS, SRM Institute of Science and Technology
- 💼 GitHub: [@KritPrasad05](https://github.com/KritPrasad05)

> *This project is academic research. If you use or build upon this work, please cite the associated research paper (see [`docs/research_paper.pdf`](docs/research_paper.pdf)).*

---

<div align="center">

**Made with 🌿 at SRM University**

*EfficientNet-B0 × ChromaDB × Ollama × FastAPI × Streamlit*

</div>
