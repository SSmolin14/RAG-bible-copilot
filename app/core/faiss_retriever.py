import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import Config
from .base_retriever import BaseRetriever

class FAISSRetriever(BaseRetriever):
    def __init__(self):
        self.model = SentenceTransformer(Config.MODEL_NAME)
        # Load index and metadata
        self.index = faiss.read_index(f"{Config.FAISS_PATH}/bible.index")
        with open(f"{Config.FAISS_PATH}/metadata.json", "r") as f:
            self.metadata = json.load(f)

    def search(self, query: str, k: int = 4):
        query_vec = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vec).astype('float32'), k)
        
        results = []
        for idx in indices[0]:
            results.append({
                "text": self.metadata[idx]["text"],
                "citation": self.metadata[idx]["citation"]
            })
        return results
    