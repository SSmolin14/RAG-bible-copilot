import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def build_index(input_path, index_dir, model_name='all-MiniLM-L6-v2'):
    # 1. Setup paths
    os.makedirs(index_dir, exist_ok=True)
    index_file = os.path.join(index_dir, "bible_index.faiss")
    metadata_file = os.path.join(index_dir, "metadata.jsonl")

    # 2. Load Chunks
    print(f"Loading chunks from {input_path}...")
    chunks = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            chunks.append(json.loads(line))

    texts = [c['text'] for c in chunks]

    # 3. Load Model
    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)

    # 4. Generate Embeddings
    print(f"Generating embeddings for {len(texts)} chunks. This may take a minute...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Normalize embeddings for cosine similarity (best for text search)
    embeddings = np.array(embeddings).astype('float32')
    faiss.normalize_L2(embeddings)

    # 5. Build FAISS Index
    dimension = embeddings.shape[1]
    # IndexFlatIP uses Inner Product (Cosine Similarity since we normalized)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    # 6. Save Index and Metadata
    print(f"Saving index to {index_file}...")
    faiss.write_index(index, index_file)

    # We save the metadata separately because FAISS only stores the vectors
    print(f"Saving metadata to {metadata_file}...")
    with open(metadata_file, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            # We don't need the full text in the index if we want to save space, 
            # but for a portfolio project, keeping it here makes retrieval easier.
            f.write(json.dumps(chunk) + '\n')

    print("--- SUCCESS ---")
    print(f"Index size: {index.ntotal} vectors")

if __name__ == "__main__":
    CHUNK_FILE = "data/processed/web_chunks.jsonl"
    INDEX_DIR = "data/vectorstore/faiss_index"
    
    build_index(CHUNK_FILE, INDEX_DIR)