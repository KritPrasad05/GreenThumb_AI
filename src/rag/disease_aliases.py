# disease_aliases.py — keyed by (plant, disease) to avoid collisions

DISEASE_TO_PATHOGEN = {
    # Apple
    ("Apple", "Apple scab"): "Venturia inaequalis",
    ("Apple", "Black rot"): "Botryosphaeria obtusa",
    ("Apple", "Cedar apple rust"): "Gymnosporangium juniperi-virginianae",

    # Cherry
    ("Cherry (including sour)", "Powdery mildew"): "Podosphaera clandestina",

    # Corn
    ("Corn (maize)", "Northern Leaf Blight"): "Exserohilum turcicum",
    ("Corn (maize)", "Cercospora leaf spot Gray leaf spot"): "Cercospora zeae-maydis",
    ("Corn (maize)", "Common rust"): "Puccinia sorghi",

    # Grape
    ("Grape", "Black rot"): "Guignardia bidwellii",
    ("Grape", "Esca (Black Measles)"): "Phaeomoniella chlamydospora",
    ("Grape", "Leaf blight (Isariopsis Leaf Spot)"): "Isariopsis clavispora",

    # Orange
    ("Orange", "Haunglongbing (Citrus greening)"): "Candidatus Liberibacter asiaticus",

    # Peach
    ("Peach", "Bacterial spot"): "Xanthomonas arboricola",

    # Pepper
    ("Pepper, bell", "Bacterial spot"): "Xanthomonas euvesicatoria",

    # Potato
    ("Potato", "Early blight"): "Alternaria solani",
    ("Potato", "Late blight"): "Phytophthora infestans",

    # Squash
    ("Squash", "Powdery mildew"): "Podosphaera xanthii",

    # Strawberry
    ("Strawberry", "Leaf scorch"): "Diplocarpon earlianum",

    # Tomato
    ("Tomato", "Bacterial spot"): "Xanthomonas perforans",
    ("Tomato", "Early blight"): "Alternaria solani",
    ("Tomato", "Late blight"): "Phytophthora infestans",
    ("Tomato", "Spider mites Two-spotted spider mite"): "Tetranychus urticae",
    ("Tomato", "Target Spot"): "Corynespora cassiicola",
    ("Tomato", "Leaf Mold"): "Passalora fulva",
}

def resolve_pathogen(plant: str, disease: str) -> str:
    """Resolve (plant, disease) → pathogen name. Falls back to disease name."""
    return DISEASE_TO_PATHOGEN.get((plant, disease), disease)