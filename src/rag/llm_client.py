# src/rag/llm_client.py
import ollama

MODEL = "phi3:mini"  # "deepseek-r1:7b" # change to mistral or phi3:mini if needed


def rewrite_query(crop: str, pred_disease: str, confidence: float) -> str:
    try:
        import ollama
        prompt = f"""You are a plant pathology expert.
A CV model predicted: {pred_disease} on {crop} (confidence: {confidence:.1%}).
Write a 1-2 sentence search query to find relevant plant disease knowledge.
Include disease name, crop, likely pathogen, and key symptoms. Be specific.
Query:"""
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1}
        )
        return response["message"]["content"].strip()
    except Exception as e:
        # Fallback: use simple template query if LLM unavailable
        return f"{crop} {pred_disease} plant disease symptoms causes treatment pathogen"


def synthesize_diagnosis(crop, pred_disease, cv_confidence,
                         kb_document, consistency_score, gate_decision) -> str:
    try:
        import ollama
        prompt = f"""You are a plant pathology diagnostic expert.
        CV model predicted: {pred_disease} on {crop} (confidence: {cv_confidence:.1%}).
        Consistency score: {consistency_score:.2f}/1.00  |  Decision: {gate_decision}
        
        Retrieved knowledge:
        {kb_document[:600]}
        
        Write a concise 3-4 sentence diagnostic reasoning paragraph confirming or
        questioning the CV prediction, highlighting key evidence, noting any caveats.
        Reasoning:"""
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.2}
        )
        return response["message"]["content"].strip()
    except Exception as e:
        # Graceful fallback — return rule-based reasoning without LLM
        if gate_decision == "ACCEPT":
            return (
                f"The computer vision model predicted {pred_disease} on {crop} "
                f"with {cv_confidence:.0%} confidence. The knowledge base "
                f"cross-check produced a consistency score of {consistency_score:.2f}, "
                f"which exceeds the acceptance threshold of 0.70, confirming the diagnosis."
            )
        else:
            return (
                f"The prediction of {pred_disease} on {crop} "
                f"({cv_confidence:.0%} confidence) yielded a consistency score of "
                f"{consistency_score:.2f}, which is below the 0.70 threshold. "
                f"The visual evidence does not sufficiently align with the knowledge base entry."
            )


def synthesize_diagnosis(
    crop: str,
    pred_disease: str,
    cv_confidence: float,
    kb_document: str,
    consistency_score: float,
    gate_decision: str
) -> str:
    """
    Role 2: Generate a coherent, evidence-grounded reasoning paragraph.
    """
    prompt = f"""You are a plant pathology diagnostic expert. 

A computer vision model predicted: {pred_disease} on {crop} (confidence: {cv_confidence:.1%}).

Retrieved knowledge base entry:
{kb_document[:800]}

Consistency score between visual prediction and knowledge: {consistency_score:.2f}/1.00
Gate decision: {gate_decision}

Write a concise 3-4 sentence diagnostic reasoning paragraph that:
1. Confirms or questions the CV prediction based on the knowledge
2. Highlights the key evidence supporting this diagnosis
3. Notes any important caveats or uncertainty

Reasoning:"""

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2}
    )
    return response["message"]["content"].strip()