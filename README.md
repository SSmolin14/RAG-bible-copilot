# RAG-bible-copilot
World-English-Bible (WEB) based RAG Copilot

# 📖 RAG Bible Copilot (WEB)

An open-source, full-stack **Retrieval Augmented Generation (RAG)** system built from the ground up using the **World English Bible (WEB)**.

This project demonstrates how to design and deploy a **production-ready RAG architecture**, including custom text chunking, embedding workflows, multi-backend vector search, and a web-based API/UI layer.

---

## 🎯 Project Goals

This repository is intended to:

- Build a **domain-specific RAG system** from first principles
- Demonstrate **best practices** for:
  - Text ingestion & chunking
  - Embedding pipelines
  - Vector search (FAISS, ChromaDB)
  - Prompt engineering
  - RESTful APIs
  - Containerized deployment
- Serve as a **learning resource** and **portfolio-quality project**

---

## 📚 Data Source

- **Bible Translation:** World English Bible (WEB)
- **License:** Public Domain
- **Why WEB?**
  - Modern English
  - Clean formatting
  - Fully redistributable
  - Suitable for open-source NLP and RAG systems

> ⚠️ Note: Other translations (e.g., NIV, ESV) are copyrighted and are **not included** in this repository.  
> The system is designed so licensed texts can be ingested locally without code changes.

---

## 🧠 System Architecture (High-Level)

```text
                ┌────────────────────┐
                │  Bible Text (WEB)   │
                └─────────┬──────────┘
                          │
                   Custom Chunking
                          │
                ┌─────────▼──────────┐
                │  Embedding Models   │
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
                │  LLM Generation     │
                └─────────┬──────────┘
                          │
                  REST API / UI

