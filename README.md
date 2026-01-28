
   📖 RAG Bible Copilot (WEB)
An open-source, full-stack Retrieval Augmented Generation (RAG) system built from the ground up using the World English Bible (WEB).

This project demonstrates a production-ready RAG architecture, featuring custom text chunking, embedding workflows, a dual-backend vector search (ChromaDB/FAISS), and a modern FastAPI + React interface.

🎯 Project Goals
Domain-Specific RAG: Built a specialized system for scripture analysis.

Hybrid LLM Support: Seamlessly switch between Gemini 1.5 (Cloud) and Ollama/Llama 3 (Local).

Multi-Backend Vector Search: Implemented adapters for both ChromaDB and FAISS.

Full-Stack Implementation: Decoupled FastAPI REST API and a Vite-powered React UI.

🧠 System Architecture
Plaintext
                ┌────────────────────┐
                │  Bible Text (WEB)   │
                └─────────┬──────────┘
                          │
                   Custom Chunking
                          │
                ┌─────────▼──────────┐
                │  Embedding Models  │
                └─────────┬──────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
     FAISS Vector DB                 ChromaDB
          │                               │
          └───────────────┬───────────────┘
                          │
                  Semantic Retrieval
                          │
                ┌─────────▼──────────┐
                │  LLM Generation    │
                └─────────┬──────────┘
                          │
                    FastAPI + React
🧩 Key Features
RAG Core
Bible-Aware Chunking: Logic optimized for book, chapter, and verse structures.

The "Bible Scholar" Persona: Advanced prompt engineering to ensure academic, grounded responses with citations.

Metadata-Rich Retrieval: Every answer includes specific scripture references.

Full-Stack Layer
FastAPI Backend: Asynchronous endpoints with CORS support for secure frontend communication.

React + Vite Frontend: Modern, responsive chat interface using Tailwind CSS and Lucide icons.

🚀 Quick Start
1. Prerequisites
Python 3.10+ & Node.js (LTS)

A Gemini API Key (Optional: Can use Ollama for 100% local execution).

2. Installation & Setup
Bash
# Clone the repository
git clone https://github.com/SSmolin14/RAG-bible-copilot.git
cd RAG-bible-copilot

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install Backend dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
3. Running the Application
You will need two terminals open:

Terminal A: The Backend (API)

Bash
uvicorn app.api.main:app --reload
Terminal B: The Frontend (UI)

Bash
cd frontend
npm install
npm run dev
Visit http://localhost:5173 to start chatting with the Bible Scholar!

📂 Repository Structure
Plaintext
rag-bible-copilot/
├── app/
│   ├── api/             # FastAPI routes & CORS config
│   ├── core/            # RAG logic & LLM Strategy
│   ├── prompts/         # Bible Scholar system templates
│   └── config.py        # Environment management
├── data/
│   └── raw/             # WEB Bible source text
├── frontend/            # React + Vite + Tailwind UI
├── requirements.txt     # Python dependencies
└── .gitignore           # Securely excludes .env and .venv