import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Config:
    LLM_TYPE = os.getenv("LLM_TYPE", "gemini").lower()
    LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "llama3")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "chroma")
    MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    
    # Paths
    CHROMA_PATH = "data/vectorstore/chroma_db"
    FAISS_PATH = "data/vectorstore/faiss_index"