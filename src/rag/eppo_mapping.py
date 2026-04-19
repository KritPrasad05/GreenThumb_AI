from typing import Dict, List
from src.rag.eppo_client import EPPOClient
from src.rag.disease_aliases import DISEASE_TO_PATHOGEN


def extract_matches(name2codes_response):
    """
    Handle both EPPO name2codes response formats:
    1. Direct list of matches
    2. Nested input → matches structure
    """

    matches = []

    for item in name2codes_response:
        # Case 1: Direct match
        if "eppocode" in item:
            matches.append(item)

        # Case 2: Nested matches
        elif "matches" in item:
            matches.extend(item.get("matches", []))

    return matches


def rank_eppo_candidates(candidates: List[Dict]) -> List[Dict]:
    """
    Rank EPPO candidates:
    1. preferred=True first
    2. alphabetical by EPPO code
    """
    return sorted(
        candidates,
        key=lambda x: (
            not x.get("preferred", False),
            x.get("eppocode", "")
        )
    )


def map_disease_to_eppo(disease_name: str, client: EPPOClient) -> Dict:
    """
    Map disease (or pathogen) name to EPPO primary + secondary codes.
    """
    
    disease_name = disease_name.strip()
    disease_name = disease_name.replace("_", " ")
    
    # Resolve disease → pathogen if needed
    pathogen_name = DISEASE_TO_PATHOGEN.get(disease_name, disease_name)

    raw_response = client.name_to_codes(pathogen_name)

    if not raw_response:
        return {
            "primary": None,
            "secondary": [],
            "note": "Empty EPPO response"
        }

    matches = extract_matches(raw_response)

    if not matches:
        return {
            "primary": None,
            "secondary": [],
            "note": "No EPPO matches found"
        }

    ranked = rank_eppo_candidates(matches)

    primary = ranked[0]
    secondary = ranked[1:] if len(ranked) > 1 else []

    return {
        "primary": {
            "eppo_code": primary.get("eppocode"),
            "name": primary.get("preferredName"),
            "preferred": primary.get("preferred", False),
            "type": primary.get("type")
        },
        "secondary": [
            {
                "eppo_code": m.get("eppocode"),
                "name": m.get("preferredName"),
                "type": m.get("type")
            }
            for m in secondary
        ]
    }
