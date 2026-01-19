import faiss
import json
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import Config

class BibleRetriever:
    def __init__(self, mode="chroma"):
        self.mode = mode
        # Load the same model used during indexing
        self.model = SentenceTransformer(Config.MODEL_NAME)
        
        if mode == "faiss":
            self.index = faiss.read_index(f"{Config.FAISS_PATH}/bible_index.faiss")
            self.metadata = []
            with open(f"{Config.FAISS_PATH}/metadata.jsonl", 'r', encoding='utf-8') as f:
                for line in f:
                    self.metadata.append(json.loads(line))
        
        elif mode == "chroma":
            self.client = chromadb.PersistentClient(path=Config.CHROMA_PATH)
            self.collection = self.client.get_collection(name="bible_web")

    def search(self, query, k=4):
        if self.mode == "faiss":
            query_vector = self.model.encode([query])
            faiss.normalize_L2(query_vector)
            distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
            
            results = []
            for i in range(k):
                idx = indices[0][i]
                results.append({
                    "text": self.metadata[idx]["text"],
                    "citation": self.metadata[idx]["metadata"]["citation"]
                })
            return results

        elif self.mode == "chroma":
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "text": results['documents'][0][i],
                    "citation": results['metadatas'][0][i]['citation']
                })
            return formatted_results