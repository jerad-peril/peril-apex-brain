# Apex Brain — RAG Knowledge Base API

Retrieval-Augmented Generation engine for Peril Adjusters LLC. Serves the internal knowledge vault (Airtable schemas, SOPs, competitive intelligence) to AI agents via semantic search.

**Owner:** Peril Adjusters LLC
**Stack:** Python 3.11 / FastAPI / ChromaDB / SentenceTransformers
**Deployment:** Railway (Docker, auto-deploy from `main`)
**Embedding model:** all-MiniLM-L6-v2 (384-dim, 79MB ONNX, local — no API key)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Make.com — Jarvis Webhook Scenarios                        │
│  (Trisha: 4592587 / Hank: 4592592 / Master: 4570100)       │
│                                                             │
│  Module N: HTTP POST → Apex Brain /query                    │
│  Module N+1: Claude takes chunks as context → answers user  │
└────────────────────┬────────────────────────────────────────┘
                     │  POST /query {"query":"...", "n_results":3}
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Apex Brain (Railway Container)                             │
│                                                             │
│  FastAPI (uvicorn)                                          │
│  ├── GET  /health    → status + chunk count                 │
│  ├── POST /query     → semantic search over vault           │
│  └── POST /reindex   → rebuild from .md files               │
│                                                             │
│  ChromaDB (PersistentClient)                                │
│  └── Collection: apex_brain                                 │
│      └── 31 chunks (500 char, 80 overlap)                   │
│      └── Embeddings: all-MiniLM-L6-v2 (local ONNX)         │
│                                                             │
│  Vault Documents (markdown)                                 │
│  ├── 01_Architecture/    → Airtable schema, system maps     │
│  ├── 02_SOPs_and_Compliance/ → operating procedures         │
│  └── 03_Competitor_Intel/    → market intelligence           │
└─────────────────────────────────────────────────────────────┘
```

**Data flow:** Jarvis receives a voice/text command from an employee → Make.com webhook fires → HTTP module POSTs the question to Apex Brain → ChromaDB returns the 3 most relevant knowledge chunks → Claude module synthesizes a natural language answer from the chunks → response sent back to the employee.

**Isolation:** Each employee (Trisha, Hank, Jerad) has their own Jarvis webhook scenario with a unique URL. They share the same Apex Brain backend and Airtable connections, but their task/calendar contexts are separated at the Make.com routing layer.

---

## API Reference

### `GET /health`

```bash
curl https://YOUR-RAILWAY-URL/health
```
```json
{"service": "apex-brain-rag", "status": "ok", "chunks_indexed": 31}
```

### `POST /query`

```bash
curl -X POST https://YOUR-RAILWAY-URL/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Airtable field ID for Insurance Carrier?", "n_results": 3}'
```
```json
{
  "query": "What is the Airtable field ID for Insurance Carrier?",
  "results": [
    {
      "text": "| 3 | fld3CAC49jdt2EyYj | Insurance Carrier | multipleRecordLinks ...",
      "source": "01_Architecture/Peril_Airtable_Schema.md",
      "heading": "Claims",
      "distance": 1.1471
    }
  ],
  "total_chunks": 31
}
```

**Distance scoring:** Lower = more relevant.
- `< 1.2` — HIGH (direct match)
- `1.2 - 1.5` — MEDIUM (related context)
- `> 1.5` — LOW (tangential)

### `POST /reindex`

Rebuilds the entire vector store from all `.md` files in the vault. Use after adding or modifying documents.

```bash
curl -X POST https://YOUR-RAILWAY-URL/reindex
```
```json
{"status": "reindexed", "chunks": 31}
```

---

## Local Development

### Prerequisites

- Python 3.11+
- ~200MB disk for ChromaDB + ONNX model

### Makefile Commands

```bash
make install      # pip install -r requirements.txt
make dev          # uvicorn on :9090 with hot reload
make simulate     # test query against local server
make stress       # 10 concurrent requests (load test)
make reindex      # rebuild vector DB from vault .md files
make snapshot     # zip chromadb_store for backup
make ingest FILE=path/to/doc.md   # add single document
```

### First Run

```bash
cd APEX_BRAIN_VAULT
make install
make dev
# In another terminal:
make simulate
```

The server builds the vector index on startup (~5s for the ONNX model load, then instant for 31 chunks). Subsequent requests are sub-second.

### Testing Tools

**Jarvis Simulator** — replicates the exact Make.com HTTP module POST:
```bash
python3 jarvis_simulator.py http://localhost:9090 "What fields track carrier info?"
```
Reports response time, relevance scores per chunk, and raw JSON.

**Stress Tester** — fires N concurrent requests to measure throughput:
```bash
python3 stress_test.py http://localhost:9090 25
```
Reports avg/min/max/P95 latency, throughput (req/s), and Make.com timeout pass/fail (40s threshold).

---

## Day 2 Operations: Adding Knowledge

### Adding a Single Document

```bash
python3 ingest_document.py 02_SOPs_and_Compliance/Blueprint_Patching_Rules.md
```

Output:
```
File:     Blueprint_Patching_Rules.md
Chunks:   12 generated, 12 new / 0 updated
Index:    31 → 43 total chunks
Ingestion complete.
```

The script chunks the file (500 char / 80 overlap, heading-aware), generates content-hash IDs (safe to re-run without duplicates), and upserts into the existing ChromaDB collection.

### Adding Multiple Documents

Drop `.md` files into the appropriate vault subdirectory, then:
```bash
make reindex
```
This rebuilds the entire index from scratch. All `.md` files in all subdirectories are included.

### Vault Directory Structure

| Directory | Purpose | Status |
|---|---|---|
| `01_Architecture/` | Airtable schemas, Make.com scenario maps | 1 file (158 fields) |
| `02_SOPs_and_Compliance/` | Engineering rules, patching procedures | Empty (pending) |
| `03_Competitor_Intel/` | Market positioning, competitor analysis | Empty (pending) |

### Verifying New Knowledge

After ingestion, test that the new content is searchable:
```bash
python3 jarvis_simulator.py http://localhost:9090 "your test query about the new content"
```

---

## Disaster Recovery

### Creating a Snapshot

```bash
make snapshot
# or
python3 snapshot_vault.py
```

Creates a timestamped zip archive in `vault_snapshots/`:
```
vault_snapshots/chroma_snapshot_20260331_232505.zip  (0.15 MB)
```

Contains the full ChromaDB persistent store: all chunks, embeddings, metadata, and collection configuration.

### Restoring from a Snapshot

```bash
# Stop the server
# Remove corrupted store
rm -rf chromadb_store/

# Restore from snapshot
unzip vault_snapshots/chroma_snapshot_YYYYMMDD_HHMMSS.zip -d .

# Restart server — index loads from restored store
make dev
```

### Nuclear Option: Full Rebuild

If snapshots are unavailable, rebuild from source documents:
```bash
rm -rf chromadb_store/
make reindex   # rebuilds from all .md files in vault
make dev       # start server with fresh index
```

This takes ~10 seconds. The ONNX embedding model downloads automatically on first run (~79MB).

### Make.com Blueprint Backups

The `make_backups/` directory contains JSON snapshots of critical Make.com scenario blueprints. Restore via API:

```bash
# Double-stringify the blueprint before PATCHing (per MASTER_BIBLE rules)
python3 -c "
import json
with open('make_backups/4488407_....json') as f:
    bp = json.load(f)['response']['blueprint']
body = json.dumps({'blueprint': json.dumps(bp)})
print(body)
" | curl -X PATCH \
  -H 'Authorization: Token [MAKE_TOKEN]' \
  -H 'Content-Type: application/json' \
  'https://us2.make.com/api/v2/scenarios/4488407?teamId=1962205' \
  -d @-
```

---

## Cloud Deployment (Railway)

### Build Process

Railway detects the `Dockerfile` and builds:
1. `python:3.11-slim` base image
2. `pip install` from `requirements.txt`
3. Copies vault documents + chromadb_store into container
4. Runs `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. On startup: re-indexes all .md files, loads ONNX model, serves API

### Deploying Updates

Push to `main` branch → Railway auto-deploys:
```bash
git add .
git commit -m "feat: add new SOP document"
git push origin main
```

Railway rebuilds the container in ~2-3 minutes. The vector index rebuilds from the `.md` files included in the Docker image.

### Environment

- No environment variables required (no API keys — embeddings are local)
- Railway injects `$PORT` automatically
- Container needs ~512MB RAM (ONNX model + ChromaDB)

### Make.com HTTP Module Configuration

| Setting | Value |
|---|---|
| URL | `https://[RAILWAY-URL]/query` |
| Method | POST |
| Content-Type | `application/json` |
| Body | `{"query":"{{1.text}}","n_results":3}` |
| Parse response | Yes |
| Timeout | 30 seconds |

---

## File Reference

```
APEX_BRAIN_VAULT/
├── main.py                     # FastAPI app — /health, /query, /reindex
├── apex_vector_builder.py      # Chunks .md → ChromaDB embeddings
├── ingest_document.py          # CLI: add single doc to existing index
├── jarvis_simulator.py         # CLI: replicate Make.com HTTP POST
├── stress_test.py              # CLI: async load tester (aiohttp)
├── snapshot_vault.py           # CLI: zip chromadb_store for backup
├── requirements.txt            # Python deps
├── Dockerfile                  # Railway container build
├── Procfile                    # Railway entry point (uvicorn)
├── Makefile                    # Unified operations interface
├── .gitignore                  # Excludes chromadb_store/, snapshots
├── .dockerignore               # Excludes venv, snapshots, backups
├── README.md                   # This file
├── 01_Architecture/
│   └── Peril_Airtable_Schema.md
├── 02_SOPs_and_Compliance/     # Pending: engineering SOPs
├── 03_Competitor_Intel/        # Pending: market data
├── chromadb_store/             # Local vector DB (gitignored)
├── vault_snapshots/            # Timestamped zip backups (gitignored)
├── make_backups/               # Make.com blueprint snapshots
└── patched_make_blueprints/    # airtable2→airtable3 patched versions
```
