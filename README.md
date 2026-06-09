# Multi-Agent-Research-Assistant
# Research-Assistant-Agent

AI-powered Research Assistant Agent built using:

- LangGraph
- LangChain
- Google Gemini (via `langchain-google-genai`)
- Tavily Search API
- FAISS Vector Database (for PDF-based RAG)
- HuggingFace / Embedding Models (for semantic search)

This project implements an **agentic research workflow** that:

- routes the user query into the appropriate pipeline (PDF RAG / Simple Web / Deep Research)
- rewrites the query for better retrieval (web workflows)
- performs task planning for complex research queries (deep workflow)
- searches the web and gathers evidence using external tools (Tavily API)
- performs PDF-based semantic retrieval using FAISS for document queries
- synthesizes a final grounded answer from retrieved context
- verifies and validates the response to reduce hallucinations
- returns the final response in structured markdown format (as per prompt requirements)
---

# Features

## Current Features

- AI-powered research assistant
- Query rewriting for search optimization
- Task planning for multi-step research
- Web search + webpage extraction via Tavily
- Evidence-based answer synthesis
- Deep (workflow-based) orchestration with LangGraph
- Modular architecture (nodes/services/agents)

---

# Project Architecture

```text
                        ┌──────────────────────┐
                        │      USER INPUT      │
                        └─────────┬────────────┘
                                  │
                  ┌───────────────┴────────────────┐
                  │                                │
            PDF INPUT                         TEXT QUERY
                  │                                │
                  ▼                                ▼
     ┌──────────────────────┐        ┌────────────────────────┐
     │  pdf_workflow_node   │        │     router_node        │
     └─────────┬────────────┘        └─────────┬──────────────┘
               │                                │
               ▼                                ▼
   ┌──────────────────────┐       ┌──────────────────────────┐
   │   FAISS RAG PIPELINE │       │  SIMPLE / DEEP ROUTING   │
   └─────────┬────────────┘       └─────────┬────────────────┘
               │                                │
               ▼                                ▼
     ┌──────────────────────┐     ┌──────────────────────────┐
     │ Retrieval + Context  │     │ Web RAG (Tavily / LLM)   │
     └─────────┬────────────┘     └─────────┬────────────────┘
               │                                │
               └──────────────┬─────────────────┘
                              ▼
                 ┌────────────────────────┐
                 │  VERIFICATION AGENT   │
                 └─────────┬──────────────┘
                           ▼
                     FINAL ANSWER
```

---

# Tech Stack

- Python
- LangGraph
- LangChain
- Google Gemini
- Tavily Search API

---

# Folder Structure (approx.)

```text
Research-Assistant-Agent
│
├── app/
│
├── core/
│   ├── logging.py
│   ├── settings.py
│
├── graph/
│   ├── state.py
│   ├── builder.py
│
│   ├── workflows/
│   │   ├── research_router.py   # decides: simple / deep / pdf
│   │   ├── simple_research.py   # lightweight web flow
│   │   ├── deep_research.py     # planner + multi-step reasoning
│   │   ├── pdf_workflow.py      # NEW: RAG pipeline
│
│   ├── nodes/
│   │   ├── router_node.py
│   │   ├── query_rewrite_node.py
│   │   ├── search_node.py
│   │   ├── planner_node.py
│   │   ├── evidence_node.py
│   │   ├── extract_node.py
│   │   ├── formatter_node.py
│   │   ├── answer_node.py
│   │   ├── synthesis_context.py
│   │   ├── pdf_workflow_node.py   # NEW
│   │   ├── embedding_node.py      # NEW (FAISS embeddings)
│   │   ├── retrieval_node.py      # NEW (vector search)
│   │   ├── verification_node.py   # NEW (final checker)
│
├── ingestion/
│   ├── chunking.py
│   ├── ingest.py
│   ├── pdf_loader.py
│
├── vectorstore/
│   ├── faiss_store.py
│
├── services/
│   ├── query_rewriter.py
│   ├── citation.py
│   ├── formatter.py
│   ├── document_saver.py
│
├── tools/
│   ├── web_search.py
│   ├── pdf_reader.py
│
├── memory/
│   ├── postgres_memory.py
│
├── prompts/
│   ├── research_prompt.py
│
├── .env
├── requirements.txt
└── README.md
```
---

# Agents Overview (Table Format)

# Core AI Agents

| # | Agent Name           | File                                      | Responsibility                                                                     |
| - | -------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------- |
| 1 | Router Agent         | `router_node.py`                          | Decides whether to use PDF, Simple Research, or Deep Research workflow             |
| 2 | Query Rewriter Agent | `query_rewrite_node.py`                   | Rewrites user queries for better search quality and retrieval accuracy             |
| 3 | Planner Agent        | `planner.py` / `planner_node.py`          | Breaks complex questions into structured research tasks                            |
| 4 | Research Agent       | `researcher.py`                           | Searches the web, gathers evidence, and collects relevant information              |
| 5 | Synthesizer Agent    | `synthesizer.py` / `synthesis_context.py` | Combines evidence from multiple sources into a final research answer               |
| 6 | PDF QA Agent         | `pdf_answer_node.py`                      | Answers questions using semantically retrieved PDF chunks from the vector database |
| 7 | Verification Agent   | `verification_node.py`                    | Detects hallucinations, validates answers, and generates confidence scores         |

> These agents work together to provide web research, PDF-based RAG (Retrieval-Augmented Generation), answer synthesis, and response verification in a unified multi-agent architecture.

#  Supporting Workflow Components

| Component           | File                    | Purpose                                                                      |
| ------------------- | ----------------------- | ---------------------------------------------------------------------------- |
| PDF Extraction Node | `pdf_extract_node.py`   | Extracts raw text from uploaded PDF documents                                |
| PDF Embedding Node  | `pdf_embedding_node.py` | Chunks PDF content, generates embeddings, and stores vectors in FAISS        |
| PDF Retriever Node  | `pdf_retriever_node.py` | Performs semantic similarity search and retrieves relevant chunks from FAISS |
| Search Node         | `search_node.py`        | Executes web searches using Tavily Search API                                |
| Extract Node        | `extract_node.py`       | Extracts and cleans webpage content from search results                      |
| Formatter Node      | `formatter_node.py`     | Formats extracted content into structured markdown                           |
| Answer Node         | `answer_node.py`        | Generates final answers in the Simple Research workflow                      |

> These components support the core AI agents by handling data ingestion, retrieval, content extraction, formatting, and answer generation across both Web Research and PDF-RAG workflows.

---



---

# Installation

## Clone Repository

```bash
git clone https://github.com/DrNikitaB/Multi-Agent-Research-Assistant.git
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
TAVILY_API_KEY=your_api_key
```

---

# Run Project

```bash
python -m app.main
```

---

# Example Query

```text
What is Retrieval-Augmented Generation?
```

---

# Current Workflow (router selects workflow)

This repo supports **three LangGraph pipelines**. A `router` node classifies the query and then runs either:

- **deep** (`deep_research`)
- **simple** (`simple_research`)
- **pdf**

---

# Deep Workflow (deep_research)

```text
query_rewrite_node → planner_node → evidence_node → synthesis_context → verification → END
```

---

# Simple Workflow (simple_research)

```text
query_rewrite_node → search_node → extract_node → formatter_node → answer_node → verification → END
```
---

# pdf Workflow (simple_research)

```text
pdf_workflow_node → chunking → embeddings → FAISS retrieval → context building → LLM answer → verification → END
```

---




# Author

Built for learning and research in modern AI engineering and agentic systems.

