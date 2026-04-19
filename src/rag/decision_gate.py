# src/rag/decision_gate.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class GateResult:
    decision: str           # "ACCEPT" or "REFUSE"
    consistency_score: float
    label_match: float
    conf_alignment: float
    evidence_overlap: float
    evidence_strength: float
    reasoning: str


def compute_label_match(pred_disease: str, kb_disease: str) -> float:
    """
    f1: Do CV prediction and KB top hit agree on the disease label?
    Exact match → 1.0, partial word overlap → partial score, no match → 0.0
    """
    pred_tokens = set(pred_disease.lower().split())
    kb_tokens   = set(kb_disease.lower().split())
    overlap = pred_tokens & kb_tokens
    if not overlap:
        return 0.0
    return len(overlap) / max(len(pred_tokens), len(kb_tokens))


def compute_conf_alignment(cv_confidence: float, similarity: float) -> float:
    """
    f2: Are CV confidence and KB retrieval similarity both high and consistent?
    Penalizes cases where one is high and the other is low.
    """
    # Both should be high for a reliable prediction
    agreement = 1.0 - abs(cv_confidence - similarity)
    return round(agreement * min(cv_confidence, similarity), 4)


def compute_evidence_overlap(pred_disease: str, kb_document: str) -> float:
    """
    f3: How much of the predicted disease name appears in the retrieved document?
    """
    pred_tokens = set(pred_disease.lower().split())
    doc_lower = kb_document.lower()
    found = sum(1 for token in pred_tokens if token in doc_lower and len(token) > 3)
    return round(found / max(len(pred_tokens), 1), 4)


def compute_evidence_strength(similarity: float, cv_confidence: float) -> float:
    """
    f4: Overall strength of retrieved evidence.
    High similarity + high CV confidence = strong evidence.
    """
    return round((similarity + cv_confidence) / 2, 4)


def run_decision_gate(
    pred_crop: str,
    pred_disease: str,
    cv_confidence: float,
    top_hit: Optional[dict],
    threshold: float = 0.70,
    weights: tuple = (0.35, 0.25, 0.20, 0.20)
) -> GateResult:
    """
    Implements Equations 8 & 9 from the paper.

    S = w1*LabelMatch + w2*ConfAlignment + w3*EvidenceOverlap + w4*EvidenceStrength
    Decision = ACCEPT if S >= threshold, REFUSE if S < threshold
    """
    w1, w2, w3, w4 = weights

    if top_hit is None:
        return GateResult(
            decision="REFUSE",
            consistency_score=0.0,
            label_match=0.0,
            conf_alignment=0.0,
            evidence_overlap=0.0,
            evidence_strength=0.0,
            reasoning="No knowledge base entry could be retrieved for this prediction."
        )

    kb_disease  = top_hit["metadata"].get("disease", "")
    kb_crop     = top_hit["metadata"].get("crop", "")      # ← NEW
    similarity  = top_hit["similarity"]
    kb_document = top_hit["document"]

    # ── Hard veto: crop mismatch kills the prediction immediately ──────────
    crop_match = compute_crop_match(pred_crop, kb_crop)
    if crop_match == 0.0:
        return GateResult(
            decision="REFUSE",
            consistency_score=0.0,
            label_match=0.0,
            conf_alignment=0.0,
            evidence_overlap=0.0,
            evidence_strength=0.0,
            reasoning=(
                f"CROP MISMATCH: CV predicted crop '{pred_crop}' but the best "
                f"knowledge base match is for '{kb_crop}'. This disease-crop "
                f"combination is not valid. Prediction refused regardless of confidence."
            )
        )

    f1 = compute_label_match(pred_disease, kb_disease)
    f2 = compute_conf_alignment(cv_confidence, similarity)
    f3 = compute_evidence_overlap(pred_disease, kb_document)
    f4 = compute_evidence_strength(similarity, cv_confidence)

    # Apply crop match as a multiplier — partial match (0.5) dampens the score
    S = round(crop_match * (w1*f1 + w2*f2 + w3*f3 + w4*f4), 4)
    decision = "ACCEPT" if S >= threshold else "REFUSE"

    reasoning = (
        f"Crop match '{pred_crop}' vs KB crop '{kb_crop}': {crop_match:.2f}. "
        f"Label match between '{pred_disease}' and KB entry '{kb_disease}': {f1:.2f}. "
        f"Confidence alignment (CV={cv_confidence:.2f}, KB similarity={similarity:.2f}): {f2:.2f}. "
        f"Evidence overlap: {f3:.2f}. Evidence strength: {f4:.2f}. "
        f"Weighted consistency score S={S:.3f} vs threshold τ=0.70 → {decision}."
    )

    return GateResult(
        decision=decision,
        consistency_score=S,
        label_match=f1,
        conf_alignment=f2,
        evidence_overlap=f3,
        evidence_strength=f4,
        reasoning=reasoning
    )

def compute_crop_match(pred_crop: str, kb_crop: str) -> float:
    """
    f0 (hard constraint): Does the predicted crop match the KB entry's crop?
    This is a prerequisite check — a mismatch should heavily penalize the score.
    Exact match → 1.0, partial match → 0.5, no match → 0.0
    """
    pred = pred_crop.lower().strip()
    kb   = kb_crop.lower().strip()

    if pred == kb:
        return 1.0

    # Handle common partial matches e.g. "Corn (maize)" vs "Corn"
    pred_tokens = set(pred.replace("(","").replace(")","").split())
    kb_tokens   = set(kb.replace("(","").replace(")","").split())
    overlap = pred_tokens & kb_tokens
    if overlap:
        return 0.5

    return 0.0