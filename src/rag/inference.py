# src/rag/inference.py  (updated)
from src.rag.rag_retriever import RAGRetriever
from src.rag.decision_gate import run_decision_gate
from src.rag.llm_client import rewrite_query, synthesize_diagnosis

retriever = RAGRetriever(top_k=3)


def diagnose(crop: str, pred_disease: str, confidence: float) -> dict:

    # Step 1: LLM enriches the query (used for synthesis, NOT for retrieval)
    enriched_query = rewrite_query(crop, pred_disease, confidence)

    # Step 2: Retrieve using DIRECT query — stable and deterministic
    # This prevents different LLMs from pulling different KB entries
    retrieval = retriever.retrieve(crop, pred_disease, confidence)
    top_hit = retrieval["top_hit"]

    # Step 3: Decision gate (unchanged)
    gate = run_decision_gate(crop, pred_disease, confidence, top_hit)

    # Step 4: LLM synthesizes reasoning using the STABLY retrieved document
    kb_doc = top_hit["document"] if top_hit else ""
    llm_reasoning = synthesize_diagnosis(
        crop, pred_disease, confidence, kb_doc,
        gate.consistency_score, gate.decision
    )

    if gate.decision == "ACCEPT":
        kb_meta = top_hit["metadata"]
        def extract_section(doc, header):
            import re
            try:
                start = doc.index(header) + len(header)
                next_h = re.search(r'\n[A-Z &]+\n', doc[start:])
                end = start + next_h.start() if next_h else start + 400
                return doc[start:end].strip()
            except ValueError:
                return "See EPPO database."

        return {
            "status": "ACCEPTED",
            "disease": kb_meta.get("disease", pred_disease),
            "crop": crop,
            "pathogen": kb_meta.get("pathogen", "Unknown"),
            "eppo_code": kb_meta.get("eppo_code", "N/A"),
            "cv_confidence": round(confidence, 4),
            "consistency_score": gate.consistency_score,
            "llm_reasoning": llm_reasoning,          # ← LLM-generated
            "enriched_query": enriched_query,         # ← for transparency
            "component_scores": {
                "label_match":      gate.label_match,
                "conf_alignment":   gate.conf_alignment,
                "evidence_overlap": gate.evidence_overlap,
                "evidence_strength":gate.evidence_strength,
            },
            "supporting_evidence": {
                "symptoms":   extract_section(kb_doc, "SYMPTOMS\n"),
                "causes":     extract_section(kb_doc, "CAUSES & EPIDEMIOLOGY\n"),
                "treatment":  extract_section(kb_doc, "TREATMENT OPTIONS\n"),
                "prevention": extract_section(kb_doc, "PREVENTION STRATEGIES\n"),
            },
            "kb_source": "EPPO Global Database + Expert Curation",
        }

    else:
        return {
            "status": "REFUSED",
            "pred_disease": pred_disease,
            "crop": crop,
            "cv_confidence": round(confidence, 4),
            "consistency_score": gate.consistency_score,
            "llm_reasoning": llm_reasoning,
            "component_scores": {
                "label_match":      gate.label_match,
                "conf_alignment":   gate.conf_alignment,
                "evidence_overlap": gate.evidence_overlap,
                "evidence_strength":gate.evidence_strength,
            },
            "possible_matches": [
                {"rank": h["rank"], "disease": h["metadata"].get("disease"),
                 "similarity": h["similarity"]}
                for h in retrieval["hits"]
            ],
            "suggestions": [
                "Re-upload a clearer, well-lit image of the affected leaf.",
                "Ensure the diseased area is centered and in focus.",
                "Avoid images with soil, multiple leaves, or heavy shadows.",
            ]
        }