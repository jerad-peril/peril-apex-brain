"""Apex Brain — Vector Builder
Chunks all .md files in the vault subdirectories and embeds them into a
local ChromaDB collection using Chroma's default SentenceTransformer model.
Run once at startup or whenever vault content changes.
"""

import os
import glob
import hashlib
import chromadb

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(VAULT_DIR, "chromadb_store")
COLLECTION_NAME = "apex_brain"
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 80


def _chunk_text(text: str, source: str) -> list[dict]:
    """Split text into overlapping chunks with metadata."""
    chunks = []
    lines = text.split("\n")
    current_heading = ""
    buffer = ""

    for line in lines:
        if line.startswith("## "):
            current_heading = line.strip("# ").strip()
        buffer += line + "\n"

        if len(buffer) >= CHUNK_SIZE:
            chunks.append({
                "text": buffer.strip(),
                "source": source,
                "heading": current_heading,
            })
            # Keep overlap
            buffer = buffer[-CHUNK_OVERLAP:]

    if buffer.strip():
        chunks.append({
            "text": buffer.strip(),
            "source": source,
            "heading": current_heading,
        })

    return chunks


def build_index(client=None) -> int:
    """Scan vault for .md files, chunk them, and upsert into ChromaDB.
    Accepts an optional pre-initialized ChromaDB client.
    Returns the number of chunks indexed."""

    md_files = glob.glob(os.path.join(VAULT_DIR, "**", "*.md"), recursive=True)
    if not md_files:
        print("No .md files found in vault.")
        return 0

    all_chunks = []
    for filepath in md_files:
        rel_path = os.path.relpath(filepath, VAULT_DIR)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        file_chunks = _chunk_text(text, source=rel_path)
        all_chunks.extend(file_chunks)

    if not all_chunks:
        print("No chunks generated.")
        return 0

    # Initialize ChromaDB with persistent storage (use provided client or create new)
    if client is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete and recreate collection for clean rebuild
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Apex Brain RAG knowledge base"},
    )

    # Build IDs, documents, metadata
    ids = []
    documents = []
    metadatas = []
    for i, chunk in enumerate(all_chunks):
        chunk_id = hashlib.md5(
            f"{chunk['source']}:{i}:{chunk['text'][:50]}".encode()
        ).hexdigest()
        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append({
            "source": chunk["source"],
            "heading": chunk["heading"],
            "chunk_index": i,
        })

    # Upsert in batches of 100
    for start in range(0, len(ids), 100):
        end = min(start + 100, len(ids))
        collection.upsert(
            ids=ids[start:end],
            documents=documents[start:end],
            metadatas=metadatas[start:end],
        )

    print(f"Indexed {len(ids)} chunks from {len(md_files)} files into '{COLLECTION_NAME}'")
    return len(ids)


if __name__ == "__main__":
    count = build_index()
    print(f"Build complete: {count} chunks")
