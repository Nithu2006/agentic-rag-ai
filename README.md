# Agentic RAG AI

An Agentic Retrieval-Augmented Generation (RAG) system for intelligent document question answering using multiple AI agents, local vector search, web fallback, verification, and conversational memory.

---

## 📌 Project Overview

Agentic RAG AI is an intelligent question-answering system that combines Retrieval-Augmented Generation with a multi-agent architecture.

Instead of directly asking an LLM to generate an answer, the system first retrieves relevant information from uploaded documents and then uses that information as evidence for generating the response.

If sufficient information cannot be found in the local knowledge base, the system can use web search as a fallback.

The generated answer is then passed through a verification stage to estimate how well the response is supported by the available evidence.

---

## 🎯 Objectives

- Provide intelligent question answering over uploaded documents
- Retrieve relevant information using semantic vector search
- Improve retrieval using reranking
- Use multiple specialized agents
- Use web search when local information is insufficient
- Generate answers using a local LLM
- Provide source citations
- Verify generated answers against available evidence
- Maintain conversational context
- Provide an interactive web interface

---

## 🏗️ System Architecture

```text
                         USER
                           |
                           v
                     FRONTEND UI
                           |
                           v
                       FASTAPI
                           |
                           v
                    PLANNER AGENT
                           |
                           v
                  RETRIEVAL AGENT
                           |
                           v
               +----------------------+
               |                      |
               v                      v
        LOCAL KNOWLEDGE         WEB SEARCH
             BASE                 FALLBACK
               |                      |
               v                      |
          EMBEDDINGS                  |
               |                      |
               v                      |
             FAISS <------------------+
               |
               v
           RERANKING
               |
               v
        RESPONSE AGENT
               |
               v
       CONVERSATION MEMORY
               |
               v
       LOCAL LLM (OLLAMA)
               |
               v
      VERIFICATION AGENT
               |
               v
       CITATIONS + METRICS
               |
               v
             USER