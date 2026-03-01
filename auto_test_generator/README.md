# 🤖 AI-Driven Automated Test Generator

> Transform PDF requirements into executable `pytest` scripts using a RAG pipeline powered by n8n, Qdrant, and local LLMs via Ollama.

---

## 🌟 Overview

This project bridges the gap between functional documentation and technical validation. Using a **Retrieval-Augmented Generation (RAG)** architecture, the system ensures generated test suites are strictly grounded in your business requirements — not hallucinated from thin air.

The pipeline follows an **Actor-Critic design pattern**:

- The **Actor** (Generation Agent) drafts a Python test script by retrieving relevant context from the vector store.
- The **Critic** (Review Agent) validates the output for requirement coverage and PEP 8 compliance before anything touches the disk.

---

## 🏗️ System Architecture

The workflow is orchestrated through **n8n** and flows through three distinct layers:

```
PDF Requirements
      │
      ▼
┌─────────────────────┐
│   Ingestion Layer   │  PDFs → parsed → vectorized → Qdrant
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│  Generation Layer   │  LLM (Llama 3 / Mistral) + Qdrant context → draft .py
│     (The Actor)     │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│    Review Layer     │  Base64 decode → LLM review → outputs review.txt
│    (The Critic)     │
└─────────────────────┘
      │
      ▼
  review.txt saved to filesystem
  (contains coverage & PEP 8 review points)
```

---

## 📂 Project Structure

```
auto_test_generator/
├── docker-compose.yml       # Orchestrates Qdrant, Ollama, and RAG services
├── .gitignore               # Excludes binary/local data from version control
├── README.md                # You are here
│
├── n8n_data/                # n8n workflow logic
│   └── nodes/               # Exported workflow JSON files
│
├── rag-service/             # Core backend
│   ├── data/                # Input: requirement PDFs go here
│   ├── main.py              # RAG execution engine
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Service containerization
│
├── qdrant_data/             # (git-ignored) Persistent vector DB storage
└── ollama_data/             # (git-ignored) Local LLM model weights
```

---

## 🛠️ Installation & Setup

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [Python 3.10+](https://www.python.org/)
- A running [n8n](https://n8n.io/) instance

---

### 1. Launch Infrastructure

Spin up Qdrant, Ollama, and supporting services from the root directory:

```bash
docker-compose up -d
```

---

### 2. Set Up the Python Service

```bash
cd rag-service

python -m venv .venv

# Activate the virtual environment:
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

---

### 3. Add Your Requirements

Drop your PDF requirement documents into:

```
rag-service/data/
```

Then run the ingestion script to parse and vectorize them into Qdrant:

```bash
python main.py
```

---

### 4. Import the n8n Workflow

1. Open your n8n instance.
2. Import the JSON file located in `n8n_data/nodes/`.
3. Update any **Read from Disk** nodes to point to your local `auto_test_generator/` paths.
4. Activate the workflow.

---

## 📝 Key Technical Highlights

**Multi-Container Orchestration** — A centralized `docker-compose.yml` handles service discovery between n8n, Qdrant, and Ollama with zero manual networking.

**Base64 Decoding** — Custom JavaScript nodes in n8n translate binary file streams into readable UTF-8 strings for LLM inspection.

**Separation of Concerns** — Persistent state (`qdrant_data/`, `ollama_data/`) is fully decoupled from orchestration logic, keeping the repository portable and clean.

**Agentic Review Loop** — An automated "Peer Review" step reduces LLM hallucinations by running a second model pass before any file is written to disk.

---

## 🔧 Tech Stack

| Component | Role |
|---|---|
| [n8n](https://n8n.io/) | Workflow orchestration |
| [Qdrant](https://qdrant.tech/) | Vector database |
| [Ollama](https://ollama.com/) | Local LLM runtime |
| Llama 3 / Mistral | Generation & review models |
| Python + pytest | Test script generation target |
| Docker Compose | Infrastructure management |

---

## 🚀 Roadmap

- [ ] Add support for multiple PDF ingestion in a single run
- [ ] Configurable model selection per layer (actor vs. critic)
- [ ] Web UI for uploading PDFs and downloading generated test files
- [ ] GitHub Actions integration for CI-triggered test regeneration

---

## 📄 License

This project is open source. See `LICENSE` for details.