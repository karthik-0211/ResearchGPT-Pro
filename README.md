# ResearchGPT Pro

An AI-powered research assistant that turns a single query (or an uploaded PDF) into a fact-checked, well-structured report. It's built as a multi-agent pipeline on **LangGraph**, with **LangSmith** integration for tracing and monitoring every step of the workflow.

**Live demo:** [research-gpt-frontend.onrender.com](https://research-gpt-frontend.onrender.com)

---

## How it works

Every query flows through a chain of specialized agents orchestrated by LangGraph:

```
Planner → Researcher → PDF Agent → Summarizer → Fact-Checker → Report Generator
```

- **Planner Agent** – reformulates the user's query (using conversation history) into a standalone search query plus internal planning notes.
- **Researcher Agent** – gathers information from live web search and a retrieval-augmented (RAG) knowledge base, then compiles structured internal research notes.
- **PDF Agent** – if a document is uploaded, extracts and incorporates its content into the research context.
- **Summarizer Agent** – condenses the research notes into a coherent summary.
- **Fact-Check Agent** – verifies claims in the summary against the gathered sources to reduce hallucination.
- **Report Agent** – produces the final, polished, Markdown-formatted answer shown to the user.

The whole graph is traced via LangSmith, so every agent hand-off, prompt, and output can be inspected for debugging and quality monitoring.

## Features

- 🔎 **Web-grounded research** — live web search (DuckDuckGo) with a Wikipedia/news fallback chain so a query rarely comes back empty.
- 📄 **PDF-aware conversations** — upload a document and ask questions about it directly, or blend it with web research.
- 🧠 **RAG knowledge base** — a Chroma vector store with HuggingFace embeddings for retrieval over ingested documents.
- ✅ **Fact-checking pass** — a dedicated agent cross-checks claims before the final report is generated.
- 💬 **Persistent chat sessions** — session history, pinning, and saved reports backed by Redis.
- 📡 **Streaming responses** — answers are streamed token-by-token to the frontend via a FastAPI `StreamingResponse`.
- 🖥️ **React chat UI** — sidebar with session history/saved reports, live agent-status timeline, markdown rendering, and file upload.

## Tech stack

**Backend**
- FastAPI + Uvicorn
- LangGraph / LangChain (agent orchestration)
- Groq (`llama-3.3-70b-versatile`) as the LLM
- LangSmith (tracing/observability)
- ChromaDB + LangChain-HuggingFace embeddings (RAG)
- Redis (chat history, sessions, saved reports)
- DuckDuckGo Search, BeautifulSoup, httpx/requests (web research)
- pypdf, python-docx, reportlab, markdown (document handling/report export)

**Frontend**
- React 19 + Vite
- react-markdown + remark-gfm (rendering formatted reports)
- Axios

## Project structure

```
ResearchGPT-Pro/
├── backend/
│   ├── agents/          # planner, researcher, pdf, summarizer, factcheck, report agents + LLM client
│   ├── api/             # FastAPI app (main.py) — sessions, reports, /research endpoint
│   ├── memory/          # Redis-backed chat history + session store
│   ├── rag/             # document ingestion + Chroma vector store
│   ├── reports/         # saved report storage
│   ├── tools/           # web search, PDF reader, citation tool, notes tool
│   ├── workflows/        # LangGraph graph definition (graph.py)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/  # Sidebar, ChatWorkspace, ChatMessage, AgentTimeline, FileUpload,
    │   │                 MarkdownViewer, SavedReports, SessionHistory, TypingAnimation
    │   ├── App.jsx
    │   └── config.js    # API base URL
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A running Redis instance
- API keys: [Groq](https://console.groq.com/) (LLM), optionally [LangSmith](https://smith.langchain.com/) (tracing) and a HuggingFace token (embeddings for RAG)

### Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file inside `backend/` with:

```env
GROQ_API_KEY=your_groq_api_key
REDIS_URL=redis://localhost:6379          # or REDIS_HOST / REDIS_PORT
LANGCHAIN_TRACING_V2=true                 # optional, for LangSmith tracing
LANGCHAIN_API_KEY=your_langsmith_api_key  # optional
LANGCHAIN_PROJECT=researchgpt-pro         # optional
HF_TOKEN=your_huggingface_token           # optional, for RAG embeddings
```

Run the API:

```bash
uvicorn api.main:app --reload
```

The backend will be available at `http://localhost:8000`.

### Frontend setup

```bash
cd frontend
npm install
```

Create a `.env` file inside `frontend/` (optional — defaults to `http://localhost:8000`):

```env
VITE_API_URL=http://localhost:8000
```

Run the dev server:

```bash
npm run dev
```

## API overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/research` | Submit a query (+ optional PDF), get a streamed answer |
| `GET` | `/sessions` | List all chat sessions |
| `GET` | `/session/{session_id}` | Load a specific session |
| `DELETE` | `/session/{session_id}` | Delete a session |
| `POST` | `/session/{session_id}/pin` | Pin/unpin a session as a report |
| `GET` | `/reports` | List saved reports (+ pinned chats) |
| `GET` | `/report/{report_id}` | Get a specific report |
| `POST` | `/save-report` | Save a report (title + content) |
| `DELETE` | `/report/{report_id}` | Delete or unpin a report |

## Deployment

The live demo frontend is deployed on Render at [research-gpt-frontend.onrender.com](https://research-gpt-frontend.onrender.com). The FastAPI backend can be deployed similarly on Render (or any host supporting Python/Uvicorn), with `VITE_API_URL` pointed at the deployed backend URL.
