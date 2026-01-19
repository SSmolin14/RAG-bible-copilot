import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def test_query(query_text, index_path, metadata_path, k=3):
    # 1. Load the model (must be the same one used for indexing)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Load FAISS index and metadata
    index = faiss.read_index(index_path)
    
    metadata = []
    with open(metadata_path, 'r', encoding='utf-8') as f:
        for line in f:
            metadata.append(json.loads(line))

    # 3. Encode the user query
    query_vector = model.encode([query_text])
    faiss.normalize_L2(query_vector) # Crucial: Match the normalization used in indexing

    # 4. Search
    # distances = similarity score, indices = position in our metadata list
    distances, indices = index.search(np.array(query_vector).astype('float32'), k)

    print(f"\n--- Results for: '{query_text}' ---")
    for i in range(k):
        meta = metadata[indices[0][i]]
        score = distances[0][i]
        print(f"[{i+1}] Score: {score:.4f} | {meta['metadata']['citation']}")
        print(f"    Text: {meta['text']}\n")

if __name__ == "__main__":
    INDEX_FILE = "data/vectorstore/faiss_index/bible_index.faiss"
    META_FILE = "data/vectorstore/faiss_index/metadata.jsonl"
    
    # Try a semantic query!
    user_query = input("Enter a search query: ")
    test_query(user_query, INDEX_FILE, META_FILE)