"""Apex Brain — RAG API
FastAPI wrapper that serves the ChromaDB-backed knowledge base.
Called by Make.com Jarvis HTTP modules via POST /query.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from apex_vector_builder import build_index, CHROMA_DIR, COLLECTION_NAME

# ── Shared state ────────────────────────────────────────────────────────
_client = None
_collection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _client, _collection
    print("Apex Brain starting — building vector index...")
    _client = chromadb.PersistentClient(path=CHROMA_DIR)
    count = build_index(client=_client)
    print(f"Index ready: {count} chunks")
    _collection = _client.get_collection(COLLECTION_NAME)
    print(f"Collection loaded: {_collection.count()} documents")
    yield
    print("Apex Brain shutting down.")


app = FastAPI(
    title="Apex Brain RAG API",
    version="1.0.0",
    description="Retrieval-Augmented Generation over Peril Adjusters knowledge vault",
    lifespan=lifespan,
)


# ── Models ──────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    query: str
    n_results: int = 3


class ChunkResult(BaseModel):
    text: str
    source: str
    heading: str
    distance: float


class QueryResponse(BaseModel):
    query: str
    results: list[ChunkResult]
    total_chunks: int


# ── Endpoints ───────────────────────────────────────────────────────────
@app.get("/health")
def health():
    chunk_count = _collection.count() if _collection else 0
    return {
        "service": "apex-brain-rag",
        "status": "ok",
        "chunks_indexed": chunk_count,
    }


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    if not _collection:
        raise HTTPException(status_code=503, detail="Index not ready")
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = _collection.query(
        query_texts=[req.query],
        n_results=min(req.n_results, 10),
    )

    chunks = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    for doc, meta, dist in zip(docs, metas, dists):
        chunks.append(ChunkResult(
            text=doc,
            source=meta.get("source", ""),
            heading=meta.get("heading", ""),
            distance=round(dist, 4),
        ))

    return QueryResponse(
        query=req.query,
        results=chunks,
        total_chunks=_collection.count(),
    )


@app.post("/reindex")
def reindex():
    """Force a full re-index of the vault. Use after adding new .md files."""
    global _collection
    count = build_index(client=_client)
    _collection = _client.get_collection(COLLECTION_NAME)
    return {"status": "reindexed", "chunks": count}
