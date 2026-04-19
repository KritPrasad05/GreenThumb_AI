# src/rag/rag_retriever.py
import os
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
KB_DIR = os.path.join(BASE_DIR, "knowledge_base")


class RAGRetriever:
    def __init__(self, top_k: int = 3):
        self.top_k = top_k
        client = chromadb.PersistentClient(path=os.path.join(KB_DIR, "chromadb"))
        emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = client.get_collection(
            name="plant_disease_kb",
            embedding_function=emb_fn
        )

    def retrieve(self, crop: str, pred_disease: str, confidence: float) -> dict:
        """
        Query ChromaDB with a natural language query built from CV output.
        Returns top-k results with documents and metadata.
        """
        query = f"{crop} {pred_disease} plant disease symptoms causes treatment pathogen"
    
        results = self.collection.query(
            query_texts=[query],
            n_results=self.top_k,
            where={"crop": crop},       # ← HARD FILTER by crop metadata
            include=["documents", "metadatas", "distances"]
        )

        hits = []
        for i in range(len(results["ids"][0])):
            hits.append({
                "rank": i + 1,
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                # Convert distance to similarity score (ChromaDB uses L2 by default)
                "similarity": round(1 / (1 + results["distances"][0][i]), 4)
            })

        return {
            "query": query,
            "crop": crop,
            "pred_disease": pred_disease,
            "cv_confidence": confidence,
            "hits": hits,
            "top_hit": hits[0] if hits else None
        }

    def retrieve_by_query(self, enriched_query: str, crop: str,
                          pred_disease: str, confidence: float) -> dict:
        """Same as retrieve() but uses a pre-built enriched query string."""
        results = self.collection.query(
            query_texts=[enriched_query],
            n_results=self.top_k,
            include=["documents", "metadatas", "distances"]
        )
        hits = []
        for i in range(len(results["ids"][0])):
            hits.append({
                "rank": i + 1,
                "id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "similarity": round(1 / (1 + results["distances"][0][i]), 4)
            })
        return {
            "query": enriched_query,
            "crop": crop,
            "pred_disease": pred_disease,
            "cv_confidence": confidence,
            "hits": hits,
            "top_hit": hits[0] if hits else None
        }