# Apex Brain — RAG Knowledge Base API

Retrieval-Augmented Generation engine for Peril Adjusters LLC. Serves the internal knowledge vault (Airtable schemas, SOPs, competitive intelligence) to AI agents via semantic search.

---

## Architecture

```
Make.com (Jarvis Webhook)
    │
    ▼  POST /query {"query": "...", "n_results": 3}
┌──────────────────────────────────┐
│  FastAPI (uvicorn)               │
│  ├── /health     → status check  │
│  ├── /query      → semantic search│
│  └── /reindex    → rebuild index  │
│                                  │
│  ChromaDB (PersistentClient)     │
│  └── Collection: apex_brain      │
│      └── 31 chunks (500 char ea) │
│                                  │
│  Embeddings: all-MiniLM-L6-v2    │
│  (SentenceTransformer, local)    │
└──────────────────────────────────┘
    │
    ▼  JSON response with top N chunks
Make.com (Claude module builds answer from context)
```

**Stack:** Python 3.12 / FastAPI / ChromaDB / SentenceTransformers
**Deployment:** Railway (auto-deploy from GitHub `main` branch)
**Embedding model:** `all-MiniLM-L6-v2` (79MB ONNX, runs locally, no API key required)

---

## Endpoints

### `GET /health`

Returns service status and chunk count.

```json
{
  "service": "apex-brain-rag",
  "status": "ok",
  "chunks_indexed": 31
}
```

### `POST /query`

Semantic search over the knowledge vault. Returns the top N most relevant text chunks.

**Request:**
```json
{
  "query": "What is the Airtable field ID for Insurance Carrier?",
  "n_results": 3
}
```

**Response:**
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

**Distance scoring:** Lower = more relevant. Typical ranges:
- `< 1.2` — HIGH relevance (direct match)
- `1.2 - 1.5` — MEDIUM relevance (related context)
- `> 1.5` — LOW relevance (tangential)

### `POST /reindex`

Rebuilds the vector store from all `.md` files in the vault subdirectories. Use after adding new documents.

```json
{"status": "reindexed", "chunks": 31}
```

---

## Vault Structure

```
APEX_BRAIN_VAULT/
├── main.py                    # FastAPI application
├── apex_vector_builder.py     # Chunking + ChromaDB indexer
├── jarvis_simulator.py        # Make.com HTTP module simulator
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway entry point
├── README.md                  # This file
├── .gitignore
├── 01_Architecture/
│   └── Peril_Airtable_Schema.md   # 158 fields, Claims + Timeline tables
├── 02_SOPs_and_Compliance/        # Future: operating procedures
├── 03_Competitor_Intel/           # Future: market intelligence
├── chromadb_store/                # Local vector DB (gitignored)
└── make_backups/                  # Make.com blueprint snapshots
    ├── 4488407_Automated_Contracting_DocuSign_LOR.json
    ├── 4550325_Integration_Tools_SEO_Engine.json
    └── 4438573_Weather_PDF_Generator.json
```

---

## Vector Database

| Property | Value |
|---|---|
| Engine | ChromaDB (PersistentClient) |
| Collection | `apex_brain` |
| Chunks indexed | 31 |
| Source files | 1 (`Peril_Airtable_Schema.md`) |
| Chunk size | 500 characters |
| Chunk overlap | 80 characters |
| Embedding model | `all-MiniLM-L6-v2` |
| Embedding dimensions | 384 |
| Storage | `chromadb_store/` (persistent, gitignored) |

The index rebuilds automatically on server startup via the `lifespan` event. Adding new `.md` files to any vault subdirectory and calling `POST /reindex` (or restarting) will incorporate them.

---

## Make.com Integration

The Jarvis webhook scenarios call this API via an HTTP module. Configuration for the Make.com HTTP module:

| Setting | Value |
|---|---|
| URL | `https://[RAILWAY_URL]/query` |
| Method | POST |
| Content-Type | `application/json` |
| Body | `{"query":"{{1.text}}","n_results":3}` |
| Parse response | Yes |
| Timeout | 30 seconds |

The response is parsed by Make.com and the `results[].text` values are concatenated and passed to the Claude module as context for answering the user's question.

---

## Testing

### Jarvis Simulator

Replicates the exact Make.com HTTP module request locally:

```bash
# Against local instance
python3 jarvis_simulator.py http://localhost:9090 "What fields track carrier info?"

# Against Railway production
python3 jarvis_simulator.py https://[RAILWAY_URL] "DocuSign contract status fields"
```

Output includes response time measurement (Make.com times out at 40s), relevance scoring per chunk, and raw JSON for debugging.

### Direct Python Test

```bash
cd /root/trading-bot/APEX_BRAIN_VAULT
python3 apex_vector_builder.py   # Build/rebuild index
python3 -c "
import chromadb
client = chromadb.PersistentClient(path='chromadb_store')
col = client.get_collection('apex_brain')
results = col.query(query_texts=['Insurance Carrier field ID'], n_results=3)
print(results['documents'][0][0][:200])
"
```

---

## Make.com Blueprint Backups

The `make_backups/` directory contains JSON snapshots of critical Make.com scenario blueprints. These can be restored via the Make.com API:

```bash
curl -X PATCH \
  -H "Authorization: Token [MAKE_TOKEN]" \
  -H "Content-Type: application/json" \
  "https://us2.make.com/api/v2/scenarios/[ID]?teamId=1962205" \
  -d @make_backups/[FILENAME].json
```

| File | Scenario | Modules |
|---|---|---|
| `4488407_...DocuSign_LOR.json` | Automated Contracting | 4 |
| `4550325_...SEO_Engine.json` | Integration Tools | 5 |
| `4438573_...Weather_PDF.json` | Weather PDF Generator | 5 |

---

## Adding Knowledge

To expand the brain's knowledge:

1. Write a new `.md` file covering the topic
2. Place it in the appropriate subdirectory (`01_Architecture/`, `02_SOPs_and_Compliance/`, or `03_Competitor_Intel/`)
3. Call `POST /reindex` or restart the server
4. Verify with the simulator: `python3 jarvis_simulator.py [URL] "your test query"`

Planned additions:
- `Peril_Make_Architecture_V2.md` — full Make.com scenario map
- `Apex_Brain_Public_SOPs.md` — engineering rules and procedures
- `Apex_Brain_Competitor_Matrix.md` — market positioning data
