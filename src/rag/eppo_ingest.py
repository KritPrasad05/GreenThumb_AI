import os, json
from src.rag.eppo_client import EPPOClient
from src.rag.disease_aliases import resolve_pathogen
from src.rag.eppo_mapping import extract_matches, rank_eppo_candidates
from src.rag.plantvillage_classes import extract_plantvillage_classes
from src.rag.disease_seed import get_seed

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATASET_ROOT = os.path.join(BASE_DIR, "data", "plantvillage dataset", "color")
RAW_EPPO_DIR = os.path.join(BASE_DIR, "knowledge_base", "raw_eppo")
os.makedirs(RAW_EPPO_DIR, exist_ok=True)

def safe_fn(text): return text.replace(" ", "_").replace("/", "_").replace("(","").replace(")","")

def ingest_eppo_data():
    client = EPPOClient()
    classes = extract_plantvillage_classes(DATASET_ROOT)
    ok, fail = 0, []

    for crop, disease in classes:
        if disease.lower() == "healthy":
            continue
        print(f"\n[>] {crop} | {disease}")

        # Step 1: resolve pathogen name
        pathogen = resolve_pathogen(crop, disease)
        print(f"    pathogen → {pathogen}")

        # Step 2: get EPPO code
        raw = client.name_to_codes(pathogen)
        matches = extract_matches(raw) if raw else []
        if not matches:
            print(f"    [WARN] No EPPO match — using seed only")
            eppo_code = None
            profile = {"eppo_code": None, "taxon": None, "names": None,
                       "hosts_api": None, "categorization": None,
                       "hosts_web": [], "overview_text": ""}
        else:
            ranked = rank_eppo_candidates(matches)
            eppo_code = ranked[0].get("eppocode")
            print(f"    code → {eppo_code}")
            profile = client.get_full_profile(eppo_code)

        # Step 3: attach context + seed knowledge
        profile["plant_context"] = {"crop": crop, "disease": disease, "pathogen": pathogen}
        profile["seed"] = get_seed(crop, disease)

        fname = f"{safe_fn(crop)}__{safe_fn(disease)}.json"
        with open(os.path.join(RAW_EPPO_DIR, fname), "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)
        print(f"    [SAVED] {fname}")
        ok += 1

    print(f"\n✅ Done. {ok} saved, {len(fail)} failed.")

if __name__ == "__main__":
    ingest_eppo_data()