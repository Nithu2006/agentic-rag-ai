# 🤖 Agentic RAG AI

### Multi-Agent Retrieval-Augmented Generation System with Local LLM, FAISS, Web Search & Answer Verification

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)](https://github.com/facebookresearch/faiss)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black)](https://ollama.com/)
[![RAG](https://img.shields.io/badge/AI-RAG-purple)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
[![Tests](https://img.shields.io/badge/Tests-8%20Passed-success)](#testing)

> An AI-powered Agentic RAG application that combines document retrieval, intelligent reranking, web-search fallback, local LLM generation, conversation memory, citations, and answer verification into a single system.

---

## 📌 Overview

**Agentic RAG AI** is a multi-agent Retrieval-Augmented Generation system designed to provide answers grounded in available information sources.

Instead of directly asking an LLM to generate an answer, the system follows an agent-based workflow:

```text
User Query
     │
     ▼
┌─────────────────┐
│  Planner Agent  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Retrieval Agent     │
│ Local FAISS Search  │
└──────────┬──────────┘
           │
           ▼
      Reranking
           │
           ▼
   Relevant Evidence?
      │           │
     YES          NO
      │           │
      │     ┌───────────────┐
      │     │ Web Search    │
      │     │ Agent         │
      │     └───────┬───────┘
      │             │
      └──────┬──────┘
             ▼
    ┌──────────────────┐
    │ Response Agent   │
    │ Local Ollama LLM │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │ Verification     │
    │ Agent            │
    └────────┬─────────┘
             │
             ▼
   Answer + Confidence
       + Citations
       + Evaluation
```

---

## ✨ Key Features

### 🧠 Multi-Agent Architecture

The system separates responsibilities into specialized agents:

- **Planner Agent** — creates the execution plan
- **Retrieval Agent** — searches the local knowledge base
- **Web Search Agent** — provides external search fallback
- **Response Agent** — generates the final response
- **Verification Agent** — checks textual support for the generated answer

---

### 📚 Document-Based RAG

Supported document types:

- PDF
- TXT

The document pipeline performs:

```text
Document
   ↓
Loading
   ↓
Cleaning
   ↓
Chunking
   ↓
Embedding
   ↓
FAISS Index
   ↓
Semantic Retrieval
```

---

### 🔎 FAISS Vector Search

The project uses **FAISS** for local vector similarity search.

Advantages:

- Local processing
- No external vector database required
- Fast similarity search
- Suitable for experimentation and academic projects

---

### 🧩 Local Embeddings

The project uses **FastEmbed** with:

```text
BAAI/bge-small-en-v1.5
```

This allows the application to generate document and query embeddings locally.

---

### 🎯 Document Reranking

Retrieved documents are reranked using a combination of:

- Semantic similarity
- Keyword overlap

The final ranking score combines both signals to improve the ordering of retrieved evidence.

---

### 🌐 Web Search Fallback

When relevant information cannot be sufficiently retrieved from the local knowledge base, the system can invoke the Web Search Agent.

Current implementation uses:

```text
DuckDuckGo HTML Search
```

This allows the system to obtain additional web snippets without requiring a separate search API key.

---

### 🦙 Local LLM

The response generation layer uses **Ollama** with:

```text
llama3.2:3b
```

This provides local LLM inference without requiring a paid external LLM API.

---

### 💬 Conversation Memory

The system maintains conversation history during the current application session.

This allows follow-up questions such as:

```text
User:
What is Artificial Intelligence?

AI:
Artificial Intelligence is...

User:
What does it focus on?

AI:
It focuses on creating systems...
```

The previous conversation is provided to the response-generation model as context.

---

### 🛡️ Answer Verification

The Verification Agent compares the generated answer against available evidence.

It produces:

- Verification status
- Support score
- Evidence availability
- Evidence count

Possible verification states include:

```text
verified
partially_verified
low_support
```

> Note: The current verification implementation is a lightweight textual-support check based on word overlap. It is not a complete semantic fact-checking system.

---

### 🔗 Citations

The system generates citation information from:

- Local documents
- Web search results

Web results can contain:

- Source title
- Source URL

---

### 📊 Evaluation

The API response includes evaluation information for the generated answer and retrieved evidence.

This makes it possible to inspect the system beyond simply displaying an answer.

---

## 🏗️ Project Architecture

```text
agentic-rag-ai/
│
├── app/
│   │
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── retrieval_agent.py
│   │   ├── web_search_agent.py
│   │   ├── response_agent.py
│   │   ├── verification_agent.py
│   │   └── orchestrator.py
│   │
│   ├── rag/
│   │   ├── document_loader.py
│   │   ├── document_processor.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── reranker.py
│   │
│   ├── services/
│   │   ├── citation_service.py
│   │   ├── evaluation_service.py
│   │   ├── llm_service.py
│   │   ├── search_service.py
│   │   ├── document_service.py
│   │   └── conversation_memory.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   └── logger.py
│   │
│   ├── config.py
│   ├── main.py
│   └── __init__.py
│
├── data/
│   ├── documents/
│   │   └── sample.txt
│   └── vector_db/
│
├── frontend/
│   └── index.html
│
├── tests/
│   ├── test_documents.py
│   ├── test_memory.py
│   └── test_reranker.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
├── run.py
└── README.md
```

---

## 🔄 RAG Pipeline

### Step 1 — Document Ingestion

PDF or TXT documents are uploaded through the API.

### Step 2 — Document Processing

Text is cleaned and normalized.

### Step 3 — Chunking

Large documents are divided into smaller chunks using a recursive text splitter.

### Step 4 — Embedding Generation

Each chunk is converted into a numerical vector using FastEmbed.

### Step 5 — Vector Storage

Vectors are stored in a local FAISS index.

### Step 6 — Retrieval

A user's query is embedded and compared against the stored vectors.

### Step 7 — Reranking

Retrieved results are reranked using semantic and keyword relevance.

### Step 8 — Web Fallback

If local evidence is insufficient, the Web Search Agent can search for additional information.

### Step 9 — Response Generation

The retrieved evidence is passed to the local Ollama model.

### Step 10 — Verification

The generated answer is checked against available evidence.

### Step 11 — Final Response

The API returns:

```text
Answer
Confidence
Citations
Verification
Evaluation
Execution Plan
```

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| API Server | Uvicorn |
| LLM | Ollama / Llama 3.2 3B |
| RAG | Retrieval-Augmented Generation |
| Embeddings | FastEmbed |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Vector Database | FAISS |
| Document Processing | LangChain |
| PDF Processing | PyPDF |
| Web Search | DuckDuckGo HTML |
| Frontend | HTML / CSS / JavaScript |
| Testing | Pytest |
| Version Control | Git / GitHub |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nithu2006/agentic-rag-ai.git
cd agentic-rag-ai
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama and download the model:

```powershell
ollama pull llama3.2:3b
```

Make sure Ollama is running before using the query endpoint.

---

## ▶️ Running the Application

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

Returns:

```json
{
  "message": "Agentic RAG API is running",
  "status": "success"
}
```

---

### Upload Document

```http
POST /upload
```

Supported:

```text
.pdf
.txt
```

The uploaded document is processed and added to the local FAISS knowledge base.

---

### Ask a Question

```http
POST /query
```

Example request:

```json
{
  "query": "What is Machine Learning?"
}
```

Example response structure:

```json
{
  "query": "What is Machine Learning?",
  "plan": [],
  "answer": "...",
  "confidence": 0.0,
  "citations": [],
  "evaluation": {},
  "verification": {}
}
```

---

## 🧪 Testing

The project includes automated tests for:

- Document processing
- Conversation memory
- Document reranking

Run:

```powershell
python -m pytest
```

Current test status:

```text
8 passed
```

---

## 🔐 Environment Variables

Create a `.env` file if environment-specific configuration is required.

Example:

```env
DEEPSEEK_API_KEY=
```

The current implementation uses a local Ollama model for response generation, so a DeepSeek API key is **not required** for the current LLM pipeline.

Never commit `.env` or API keys to GitHub.

---

## 📈 Current System Capabilities

```text
                AGENTIC RAG AI
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     LOCAL RAG     WEB SEARCH     MEMORY
        │              │              │
     FAISS         DuckDuckGo     Session
        │              │              │
        └──────────────┼──────────────┘
                       │
                 LOCAL LLM
                  Ollama
                       │
                       ▼
                VERIFICATION
                       │
                       ▼
            ANSWER + CITATIONS
```

---

## ⚠️ Current Limitations

The current version has several intentionally lightweight components:

- Conversation memory is session-based and is lost when the application restarts.
- Retrieval does not yet rewrite queries using conversation history.
- Answer verification uses textual overlap rather than a full semantic fact-checking model.
- Confidence is a heuristic score and is not statistically calibrated.
- Web search depends on availability of the DuckDuckGo HTML endpoint.
- The current frontend is a lightweight HTML/JavaScript interface.

These components can be further improved in future versions.

---

## 🚀 Future Enhancements

Planned improvements include:

- [ ] Persistent conversation memory
- [ ] Conversation-aware query rewriting
- [ ] Hybrid keyword + vector retrieval
- [ ] Advanced semantic reranking
- [ ] Improved claim-level verification
- [ ] Streaming LLM responses
- [ ] User authentication
- [ ] Document management dashboard
- [ ] Advanced evaluation metrics
- [ ] Docker deployment
- [ ] Production deployment
- [ ] Improved frontend experience
- [ ] Automated CI/CD pipeline
- [ ] More comprehensive test coverage

---

## 🎓 Academic Project

This project is developed as a **final-year Artificial Intelligence & Data Science project**.

### Domain

```text
Artificial Intelligence
Generative AI
Natural Language Processing
Information Retrieval
Agentic AI
Retrieval-Augmented Generation
```

### Main Objective

To develop an intelligent question-answering system that can retrieve relevant information from documents, use web search when necessary, generate responses using a local LLM, and verify the generated answer against available evidence.

---

## 📚 Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation
- Multi-agent system design
- Vector similarity search
- Embeddings
- Document processing
- LLM integration
- Prompt engineering
- Information retrieval
- Answer verification
- API development
- Automated testing
- Git/GitHub workflow

---

## 👩‍💻 Author

**Nithya S**

Artificial Intelligence & Data Science

GitHub:  
https://github.com/Nithu2006

---

## ⭐ If you find this project useful

Feel free to explore the repository, experiment with the RAG pipeline, and extend the architecture with additional agents and retrieval strategies.

---

## 📄 License

This project is intended primarily for academic and educational purposes.