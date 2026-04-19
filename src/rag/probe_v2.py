# probe_v2.py — run this FIRST to see what v2 exposes
import requests, json

TOKEN = "3c5ddfb4e49f4459afb451877f759dbd"
HEADERS = {"X-API-Key": TOKEN, "Accept": "application/json"}
BASE = "https://api.eppo.int/gd/v2"

code = "PHYTIN"  # Phytophthora infestans

endpoints_to_try = [
    f"/taxon/{code}",
    f"/taxon/{code}/names",
    f"/taxon/{code}/hosts",
    f"/taxon/{code}/categorization",
    f"/taxon/{code}/taxonomy",
    f"/taxon/{code}/distribution",
    f"/taxon/{code}/datasheets",
]

for ep in endpoints_to_try:
    r = requests.get(BASE + ep, headers=HEADERS)
    print(f"\n{'='*50}")
    print(f"GET {ep} → {r.status_code}")
    if r.status_code == 200:
        print(json.dumps(r.json(), indent=2)[:500])  # first 500 chars
    else:
        print(r.text[:200])