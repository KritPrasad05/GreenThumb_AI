# disease_seed.py
# Manually curated knowledge for all 26 non-healthy PlantVillage disease classes.
# Used to enrich EPPO data in the RAG knowledge base.

DISEASE_SEED = {
    ("Apple", "Apple scab"): {
        "symptoms": "Olive-green to brown velvety spots on leaves; scabby, cracked lesions on fruit surface; premature defoliation in severe cases.",
        "causes": "Fungal pathogen Venturia inaequalis; spreads via ascospores during wet spring weather; overwinters in fallen infected leaves.",
        "treatment": "Apply fungicides (myclobutanil, captan, or mancozeb) at early green tip stage; repeat every 7-14 days during wet periods.",
        "prevention": "Remove and destroy fallen leaves; plant resistant cultivars (e.g., Liberty, Freedom); prune for canopy airflow.",
    },
    ("Apple", "Black rot"): {
        "symptoms": "Circular brown lesions with purple margins on leaves ('frog-eye' spots); mummified black fruit; cankers on bark.",
        "causes": "Fungus Botryosphaeria obtusa; infects through wounds and natural openings; spreads during warm, wet weather.",
        "treatment": "Prune out infected wood and mummified fruit; apply captan or thiophanate-methyl fungicides.",
        "prevention": "Remove dead wood and mummified fruit; avoid wounding trees; maintain tree vigor.",
    },
    ("Apple", "Cedar apple rust"): {
        "symptoms": "Bright orange-yellow spots on upper leaf surface; tube-like structures (aecia) on lower surface; distorted fruit.",
        "causes": "Fungus Gymnosporangium juniperi-virginianae; requires two hosts (apple/crabapple AND Eastern red cedar/juniper) to complete life cycle.",
        "treatment": "Apply myclobutanil or triadimefon fungicides during primary infection period (pink bud through petal fall).",
        "prevention": "Remove nearby juniper/red cedar hosts; plant rust-resistant apple cultivars.",
    },
    ("Cherry", "Powdery mildew"): {
        "symptoms": "White powdery fungal coating on young leaves, shoots, and fruit; leaf curling and distortion; reduced photosynthesis.",
        "causes": "Fungus Podosphaera clandestina; thrives in warm dry days and cool nights; spreads via airborne conidia.",
        "treatment": "Apply sulfur-based or potassium bicarbonate fungicides; sterol-inhibiting fungicides (myclobutanil) for severe infections.",
        "prevention": "Ensure good air circulation; avoid excessive nitrogen; remove infected tissue.",
    },
    ("Corn (maize)", "Cercospora leaf spot Gray leaf spot"): {
        "symptoms": "Rectangular gray to tan lesions with distinct borders running parallel to leaf veins; lesions may coalesce killing large leaf areas.",
        "causes": "Fungus Cercospora zeae-maydis; overwinters in crop residue; favored by warm, humid conditions and extended dew periods.",
        "treatment": "Foliar fungicides (strobilurins, triazoles) applied at or before tasseling.",
        "prevention": "Rotate crops; till residue; plant resistant hybrids; use reduced tillage cautiously in high-risk areas.",
    },
    ("Corn (maize)", "Common rust"): {
        "symptoms": "Small, circular to elongate, brick-red to brown pustules (uredia) on both leaf surfaces; severe infections cause leaf yellowing.",
        "causes": "Fungus Puccinia sorghi; airborne urediniospores spread from southern overwintering sites; favored by cool, moist weather.",
        "treatment": "Foliar fungicides (triazoles, strobilurins) most effective when applied early.",
        "prevention": "Plant resistant hybrids; early planting to escape peak spore dispersal periods.",
    },
    ("Corn (maize)", "Northern Leaf Blight"): {
        "symptoms": "Long (up to 15 cm), cigar-shaped gray-green to tan lesions on leaves; may kill entire leaves and reduce yield significantly.",
        "causes": "Fungus Exserohilum turcicum; overwinters in crop residue; spreads via wind-borne conidia in cool, moist conditions.",
        "treatment": "Fungicide applications (triazoles, strobilurins) at tasseling if disease is severe.",
        "prevention": "Crop rotation; resistant hybrids; residue management.",
    },
    ("Grape", "Black rot"): {
        "symptoms": "Small tan spots with dark brown margins on leaves; infected berries turn brown then hard, black, and mummified.",
        "causes": "Fungus Guignardia bidwellii; overwinters in mummified berries and cane lesions; spreads during warm, wet weather.",
        "treatment": "Apply myclobutanil, mancozeb, or captan from early shoot growth through veraison.",
        "prevention": "Remove mummified berries and infected canes; improve canopy airflow through pruning.",
    },
    ("Grape", "Esca (Black Measles)"): {
        "symptoms": "Interveinal chlorosis and necrosis creating 'tiger stripe' pattern on leaves; dark streaking inside woody tissue; fruit with dark spots.",
        "causes": "Wood-rotting fungi complex including Phaeomoniella chlamydospora and Phaeoacremonium species; enters via pruning wounds.",
        "treatment": "No fully curative treatment; wound protectants (sodium arsenite banned in EU); remove and burn affected wood.",
        "prevention": "Protect pruning wounds with fungicide paste; prune during dry weather; avoid large wounds.",
    },
    ("Grape", "Leaf blight (Isariopsis Leaf Spot)"): {
        "symptoms": "Irregular dark brown spots on leaves, often with lighter centers; defoliation in severe cases affecting fruit maturation.",
        "causes": "Fungus Isariopsis clavispora (syn. Pseudocercospora vitis); favored by warm humid conditions.",
        "treatment": "Copper-based or mancozeb fungicides; maintain spray schedule with other grape disease programs.",
        "prevention": "Canopy management for airflow; remove infected debris.",
    },
    ("Orange", "Haunglongbing (Citrus greening)"): {
        "symptoms": "Asymmetric yellowing of leaves (huanglongbing means 'yellow dragon disease'); small, lopsided, bitter fruit; twig dieback; tree decline.",
        "causes": "Bacterial pathogen Candidatus Liberibacter asiaticus; transmitted by Asian citrus psyllid (Diaphorina citri); no cure once infected.",
        "treatment": "No cure; remove and destroy infected trees; control psyllid vector with insecticides.",
        "prevention": "Use certified disease-free planting material; apply systemic insecticides to control psyllid; install wind barriers; quarantine measures.",
    },
    ("Peach", "Bacterial spot"): {
        "symptoms": "Water-soaked spots on leaves becoming angular necrotic lesions; fruit with sunken, dark, cracked lesions; shot-hole appearance on leaves.",
        "causes": "Bacterium Xanthomonas arboricola pv. pruni; spreads through rain splash and wind during wet weather.",
        "treatment": "Copper-based bactericides applied preventively; oxytetracycline where permitted.",
        "prevention": "Plant resistant varieties; avoid overhead irrigation; prune for airflow; windbreaks to reduce spread.",
    },
    ("Pepper, bell", "Bacterial spot"): {
        "symptoms": "Small water-soaked lesions on leaves turning necrotic with yellow halos; raised, scabby spots on fruit; defoliation.",
        "causes": "Bacterium Xanthomonas euvesicatoria; spread by rain splash, contaminated seed, and infected transplants.",
        "treatment": "Copper hydroxide sprays; avoid working in wet fields; remove infected plant debris.",
        "prevention": "Use certified disease-free seed; copper seed treatments; resistant varieties; crop rotation.",
    },
    ("Potato", "Early blight"): {
        "symptoms": "Dark brown concentric ring lesions with yellow halos on older leaves ('target board' pattern); premature defoliation.",
        "causes": "Fungus Alternaria solani; thrives in warm weather with alternating wet/dry periods; overwinters in soil and debris.",
        "treatment": "Fungicides (chlorothalonil, mancozeb, azoxystrobin) applied preventively at first symptom appearance.",
        "prevention": "Crop rotation; destroy infected debris; adequate plant nutrition especially nitrogen; certified seed.",
    },
    ("Potato", "Late blight"): {
        "symptoms": "Water-soaked pale green lesions turning brown-black with white sporulating border under humid conditions; rapid complete plant collapse possible.",
        "causes": "Oomycete Phytophthora infestans; caused the Irish Potato Famine; spreads extremely rapidly in cool, wet conditions.",
        "treatment": "Fungicides (metalaxyl, cymoxanil, mancozeb) applied preventively; monitor using disease forecasting models.",
        "prevention": "Plant certified disease-free seed tubers; resistant varieties; destroy volunteer plants; do not use infected tubers.",
    },
    ("Squash", "Powdery mildew"): {
        "symptoms": "White powdery fungal patches on upper and lower leaf surfaces; yellowing and premature senescence of leaves.",
        "causes": "Fungus Podosphaera xanthii; unlike most powdery mildews, does NOT require leaf wetness; spread by airborne spores.",
        "treatment": "Sulfur, potassium bicarbonate, or triazole fungicides; neem oil as organic option.",
        "prevention": "Plant resistant varieties; maintain plant spacing for airflow; avoid excessive nitrogen fertilization.",
    },
    ("Strawberry", "Leaf scorch"): {
        "symptoms": "Irregular dark purple spots on leaves; central tissue dies giving scorched appearance; severe infection leads to defoliation.",
        "causes": "Fungus Diplocarpon earlianum; spreads via rain splash; favored by warm, wet conditions.",
        "treatment": "Captan or myclobutanil fungicides; remove infected leaves.",
        "prevention": "Plant in well-drained sites; avoid overhead irrigation; use disease-free transplants; mulch to reduce splash.",
    },
    ("Tomato", "Bacterial spot"): {
        "symptoms": "Small water-soaked spots on leaves, fruit, and stems; spots turn brown-necrotic with yellow halos; scabby fruit lesions.",
        "causes": "Bacterium Xanthomonas perforans; spread by rain splash, infected seed, and transplants.",
        "treatment": "Copper bactericides; reduce leaf wetness; remove infected debris.",
        "prevention": "Disease-free seed; crop rotation; resistant varieties; avoid overhead irrigation.",
    },
    ("Tomato", "Early blight"): {
        "symptoms": "Concentric ring 'bull's eye' lesions on older lower leaves; yellowing around lesions; stem lesions near soil line.",
        "causes": "Fungus Alternaria solani; favored by warm temperatures and alternating wet/dry; worsened by nutritional stress.",
        "treatment": "Chlorothalonil, mancozeb, or copper fungicides applied at 7-10 day intervals.",
        "prevention": "Crop rotation; mulching; adequate calcium and nitrogen; remove infected plant matter.",
    },
    ("Tomato", "Late blight"): {
        "symptoms": "Greasy gray-green water-soaked patches on leaves; white sporulation on undersides; rapid brown-black collapse of tissue; firm dark fruit lesions.",
        "causes": "Oomycete Phytophthora infestans; same pathogen as potato late blight; spreads explosively in cool, humid conditions.",
        "treatment": "Fungicides with metalaxyl, dimethomorph, or mancozeb; destroy infected plants immediately.",
        "prevention": "Resistant varieties; destroy infected debris; avoid wetting foliage; early season planting.",
    },
    ("Tomato", "Leaf Mold"): {
        "symptoms": "Pale green-yellow spots on upper leaf surface; olive-green to gray-brown velvety mold on lower surface; leaves curl and die.",
        "causes": "Fungus Passalora fulva (syn. Cladosporium fulvum); primarily a greenhouse disease; requires high humidity (>85%) and poor ventilation.",
        "treatment": "Fungicides (chlorothalonil, mancozeb); improve greenhouse ventilation; reduce humidity.",
        "prevention": "Resistant varieties; maintain humidity below 85%; prune lower leaves; sterilize greenhouse between crops.",
    },
    ("Tomato", "Spider mites Two-spotted spider mite"): {
        "symptoms": "Fine stippling/bronzing on leaf surface; fine webbing on undersides; leaves turn yellow, dry out, and drop; mites visible under magnification.",
        "causes": "Pest Tetranychus urticae (Two-spotted spider mite); thrives in hot, dry conditions; builds resistance quickly to acaricides.",
        "treatment": "Acaricides (abamectin, bifenazate); insecticidal soap or neem oil; predatory mites (Phytoseiidae) as biocontrol.",
        "prevention": "Maintain plant moisture; avoid dusty conditions; monitor undersides of leaves early; avoid broad-spectrum insecticides that kill natural predators.",
    },
    ("Tomato", "Target Spot"): {
        "symptoms": "Brown circular lesions with concentric rings and yellow halos on leaves; dark brown fruit lesions; defoliation under severe infection.",
        "causes": "Fungus Corynespora cassiicola; thrives in warm, humid, poorly ventilated conditions.",
        "treatment": "Fungicides (azoxystrobin, difenoconazole); remove infected plant debris.",
        "prevention": "Crop rotation; canopy management; avoid overhead irrigation.",
    },
    ("Tomato", "Septoria leaf spot"): {
        "symptoms": "Small circular spots with dark brown margins, gray-white centers, and tiny black pycnidia on lower leaves first; rapid upward spread causing defoliation.",
        "causes": "Fungus Septoria lycopersici; overwinters on infected debris and solanaceous weeds; spreads via rain splash during warm wet weather.",
        "treatment": "Fungicides (chlorothalonil, mancozeb, copper) applied preventively every 7-10 days; remove infected lower leaves.",
        "prevention": "Crop rotation; mulching to reduce splash; stake plants for airflow; destroy crop debris after harvest.",
    },
    ("Tomato", "Tomato mosaic virus"): {
        "symptoms": "Mosaic pattern of light and dark green on leaves; leaf distortion and blistering; stunted growth; fruit with internal browning.",
        "causes": "Tomato mosaic virus (ToMV); transmitted mechanically via contaminated tools, hands, and infected seed; highly stable in plant debris.",
        "treatment": "No cure once infected; remove and destroy infected plants; disinfect tools with 10% bleach or trisodium phosphate solution.",
        "prevention": "Use certified virus-free seed; resistant varieties (Tm-2 gene); wash hands before handling plants.",
    },
    ("Tomato", "Tomato Yellow Leaf Curl Virus"): {
        "symptoms": "Upward curling and yellowing of leaf margins; small cupped leaves; severe stunting; flower drop and very poor fruit set.",
        "causes": "Tomato Yellow Leaf Curl Virus (TYLCV); transmitted exclusively by silverleaf whitefly (Bemisia tabaci); cannot spread mechanically.",
        "treatment": "No cure; remove and destroy infected plants immediately; apply systemic insecticides (imidacloprid, thiamethoxam) to control whitefly vector.",
        "prevention": "Reflective mulches to repel whiteflies; yellow sticky traps; resistant varieties (Ty-1, Ty-3 genes); insect-proof netting in nurseries.",
    },
}

def get_seed(crop: str, disease: str) -> dict:
    """Return curated knowledge for a (crop, disease) pair, or empty dict."""
    return DISEASE_SEED.get((crop, disease), {})