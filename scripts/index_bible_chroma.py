import json
import os
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def build_chroma_index(input_path, db_path):
    # 1. Initialize Chroma Client
    # 'PersistentClient' ensures the data is saved to disk
    client = chromadb.PersistentClient(path=db_path)
    
    # 2. Create (or get) a collection
    # We use a specific distance function (cosine) to match our FAISS setup
    collection = client.get_or_create_collection(
        name="bible_web",
        metadata={"hnsw:space": "cosine"} 
    )

    # 3. Load Chunks
    print(f"Loading chunks from {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        chunks = [json.loads(line) for line in f]

    # 4. Prepare data for Chroma
    # Chroma handles IDs, Metadata, and Text all in one go
    documents = [c['text'] for c in chunks]
    metadatas = [c['metadata'] for c in chunks]
    ids = [c['chunk_id'] for c in chunks]

    # 5. Load Model and Generate Embeddings
    print("Generating embeddings and adding to Chroma...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    # 6. Add to Collection
    # We add in batches to be safe with memory
    batch_size = 1000
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            documents=documents[i:i+batch_size]
        )

    print(f"--- SUCCESS ---")
    print(f"ChromaDB collection count: {collection.count()}")

if __name__ == "__main__":
    CHUNK_FILE = "data/processed/web_chunks.jsonl"
    CHROMA_DIR = "data/vectorstore/chroma_db"
    build_chroma_index(CHUNK_FILE, CHROMA_DIR)