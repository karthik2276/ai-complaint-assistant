# ⬡ AI Complaint Assistant

> A production-quality **RAG-based complaint management system** using the **Endee vector database**, Sentence Transformers, FLAN-T5, FastAPI, and React + Vite.

---

## Project Overview

The AI Complaint Assistant allows users to store, search, and query customer complaints using natural language. It demonstrates a complete Retrieval-Augmented Generation (RAG) pipeline:

```
User Query → SentenceTransformer → Endee DB → FLAN-T5 → AI Response
```

---

## Features

- **Complaint Ingestion** — convert complaint text to embeddings and store in Endee
- **Semantic Search** — retrieve top-K similar complaints by cosine similarity
- **RAG Pipeline** — Endee retrieval + FLAN-T5 generation in one flow
- **AI Chat UI** — conversational interface with retrieved context explorer
- **Category Filtering** — filter search results by complaint category
- **Live Health Bar** — shows backend status, model info, complaint count
- **25 Sample Complaints** — pre-seeded across 6 categories

---

## Tech Stack

| Layer | Technology |
|---|---|
| Vector Database | Endee (local, JSONL-backed) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| LLM | `google/flan-t5-base` (offline) |
| Backend | Python · FastAPI · Pydantic v2 · Uvicorn |
| Frontend | React 18 · Vite · TypeScript · CSS Modules |

---

## How Endee is Used

Endee is imported directly from the `/endee` directory (the cloned `endee-io/endee` repo).

```python
from endee import EndeeDB

db = EndeeDB("./data/complaints.jsonl")

# Store a complaint embedding
db.insert(id="c1", vector=embedding, metadata={"text": "...", "category": "billing"})

# Semantic search
results = db.search(vector=query_embedding, top_k=5)
for r in results:
    print(r.score, r.metadata["text"])
```

---

## Project Structure

```
ai-complaint-assistant-v2/
├── endee/                    ← Endee vector DB (endee-io/endee)
│   ├── __init__.py
│   └── db.py
├── backend/
│   ├── main.py               ← FastAPI app entry point
│   ├── config.py             ← Settings from .env
│   ├── requirements.txt
│   ├── .env
│   ├── routers/
│   │   ├── complaints.py     ← POST /add-complaint
│   │   ├── search.py         ← POST /search
│   │   └── ask.py            ← POST /ask (RAG)
│   ├── models/
│   │   └── schemas.py        ← Pydantic schemas
│   └── utils/
│       ├── embeddings.py     ← SentenceTransformer singleton
│       ├── llm.py            ← FLAN-T5 singleton + prompt builder
│       └── vector_store.py   ← EndeeDB singleton
├── frontend/
│   ├── index.html
│   ├── vite.config.ts
│   ├── package.json
│   └── src/
│       ├── main.tsx          ← Entry point with ErrorBoundary
│       ├── ErrorBoundary.tsx ← Catches crashes, shows on screen
│       ├── App.tsx
│       ├── index.css
│       ├── components/
│       │   ├── StatusBar.tsx
│       │   ├── AskPanel.tsx
│       │   ├── SearchPanel.tsx
│       │   ├── AddComplaint.tsx
│       │   └── ComplaintCard.tsx
│       ├── hooks/
│       │   └── useHealth.ts
│       └── utils/
│           └── api.ts
└── data/
    └── seed_complaints.py    ← Seeds 25 complaints into Endee
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- ~3 GB disk space for AI models

### Step 1 — Clone repo and set up Endee

```bash
git clone <your-repo-url>
cd ai-complaint-assistant-v2

# Replace the bundled endee stub with the real repo:
rm -rf endee/
git clone https://github.com/endee-io/endee.git endee
```

### Step 2 — Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3 — Seed sample data

```bash
# Run from the project root
cd ..
python data/seed_complaints.py
```

### Step 4 — Start backend

```bash
cd ai-complaint-assistant-v2
uvicorn backend.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Step 5 — Start frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### Step 6 — Verify

```bash
curl http://localhost:8000/health
# {"status":"ok","total_complaints":25,...}
```

---

## API Endpoints

### POST /add-complaint
```json
{ "text": "Order arrived damaged.", "category": "delivery" }
```

### POST /search
```json
{ "query": "late shipment damaged box", "top_k": 5 }
```

### POST /ask
```json
{ "question": "What delivery issues are most common?" }
```

### GET /health
```json
{ "status": "ok", "total_complaints": 25 }
```

---

## License

MIT
