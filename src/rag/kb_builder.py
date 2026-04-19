import os, json
import re
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_DIR  = os.path.join(BASE_DIR, "knowledge_base", "raw_eppo")
KB_DIR   = os.path.join(BASE_DIR, "knowledge_base")

def build_rag_text(profile: dict) -> str:
    ctx      = profile.get("plant_context", {})
    crop     = ctx.get("crop", "Unknown")
    disease  = ctx.get("disease", "Unknown")
    pathogen = ctx.get("pathogen", "Unknown")
    code     = profile.get("eppo_code", "N/A")
    seed     = profile.get("seed", {})
    overview = profile.get("overview_text", "")
    # Remove the JS warning block
    overview = re.sub(
        r"Your browser doesn't support JavaScript.*?JavaScript is required on this site\.",
        "",
        overview,
        flags=re.DOTALL | re.IGNORECASE
    ).strip()
    # Also strip "Toggle navigation" and menu noise
    overview = re.sub(r"Toggle navigation.*?Overview", "", overview, flags=re.DOTALL).strip()
    # Collapse excess whitespace
    overview = re.sub(r"\s{2,}", " ", overview).strip()

    # Host plants from whichever source worked
    hosts_web = profile.get("hosts_web", [])
    hosts_api = profile.get("hosts_api") or []
    host_names = hosts_web or [h.get("full_name","") for h in hosts_api if h]
    hosts_str = ", ".join(host_names[:8]) if host_names else "See EPPO database"

    # Synonyms from names endpoint
    names_block = profile.get("names") or []
    synonyms = [n.get("fullname","") for n in names_block
                if n.get("fullname") and not n.get("preferred")][:4]

    text = f"""PLANT DISEASE KNOWLEDGE ENTRY
    ============================
    Disease: {disease}
    Crop: {crop}
    Causal Agent: {pathogen}
    EPPO Code: {code}
    Synonyms: {", ".join(synonyms) if synonyms else "None listed"}
    Known Host Plants: {hosts_str}
    
    SYMPTOMS
    {seed.get("symptoms", overview[:400] if overview else "See EPPO datasheet.")}
    
    CAUSES & EPIDEMIOLOGY
    {seed.get("causes", "See EPPO datasheet.")}
    
    TREATMENT OPTIONS
    {seed.get("treatment", "Consult local agricultural extension service.")}
    
    PREVENTION STRATEGIES
    {seed.get("prevention", "Consult local agricultural extension service.")}
    
    Source: EPPO Global Database + Expert Curation
    """
    return text.strip()

def build_chroma_kb():
    print("[START] Building ChromaDB KB")
    client = chromadb.PersistentClient(path=os.path.join(KB_DIR, "chromadb"))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    col = client.get_or_create_collection("plant_disease_kb", embedding_function=emb_fn)

    ids, docs, metas = [], [], []
    for fname in os.listdir(RAW_DIR):
        if not fname.endswith(".json"): continue
        with open(os.path.join(RAW_DIR, fname)) as f:
            profile = json.load(f)
        ctx = profile.get("plant_context", {})
        doc_id = f"{profile.get('eppo_code','NA')}__{ctx.get('crop','')}_{ctx.get('disease','')}".replace(" ","_")
        ids.append(doc_id)
        docs.append(build_rag_text(profile))
        metas.append({
            "eppo_code": profile.get("eppo_code") or "UNKNOWN",
            "crop": ctx.get("crop", ""),
            "disease": ctx.get("disease", ""),
            "pathogen": ctx.get("pathogen", ""),
        })

    col.upsert(ids=ids, documents=docs, metadatas=metas)
    print(f"✅ {len(ids)} documents in ChromaDB 'plant_disease_kb'")
    print("Sample document:\n")
    print(docs[0])

if __name__ == "__main__":
    build_chroma_kb()