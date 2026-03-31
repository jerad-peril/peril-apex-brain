#!/usr/bin/env python3
"""Apex Brain — Document Ingestion CLI
Adds a new markdown/text file to the existing ChromaDB collection
without rebuilding the entire index.

Usage:
    python3 ingest_document.py <filepath>
    python3 ingest_document.py 02_SOPs_and_Compliance/New_SOP.md
    python3 ingest_document.py /tmp/airtable_update.txt
"""

import os
import sys
import hashlib
import chromadb

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(VAULT_DIR, "chromadb_store")
COLLECTION_NAME = "apex_brain"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80


def chunk_file(filepath):
    """Read and chunk a file into overlapping segments with heading awareness."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    filename = os.path.basename(filepath)
    chunks = []
    heading = ""
    buffer = ""

    for line in text.split("\n"):
        if line.startswith("## "):
            heading = line.strip("# ").strip()
        buffer += line + "\n"

        if len(buffer) >= CHUNK_SIZE:
            chunks.append({
                "id": hashlib.md5(f"{filename}:{len(chunks)}:{buffer[:50]}".encode()).hexdigest(),
                "text": buffer.strip(),
                "metadata": {"source": filename, "heading": heading, "chunk_index": len(chunks)},
            })
            buffer = buffer[-CHUNK_OVERLAP:]

    if buffer.strip():
        chunks.append({
            "id": hashlib.md5(f"{filename}:{len(chunks)}:{buffer[:50]}".encode()).hexdigest(),
            "text": buffer.strip(),
            "metadata": {"source": filename, "heading": heading, "chunk_index": len(chunks)},
        })

    return chunks


def ingest(filepath):
    if not os.path.isfile(filepath):
        print(f"ERROR: File not found: {filepath}")
        return 0

    chunks = chunk_file(filepath)
    if not chunks:
        print("ERROR: No chunks generated from file.")
        return 0

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Apex Brain RAG knowledge base"},
    )

    before = collection.count()

    collection.upsert(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )

    after = collection.count()
    new = after - before
    filename = os.path.basename(filepath)

    print(f"File:     {filename}")
    print(f"Chunks:   {len(chunks)} generated, {new} new / {len(chunks) - new} updated")
    print(f"Index:    {before} → {after} total chunks")
    return len(chunks)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ingest_document.py <filepath>")
        print("Example: python3 ingest_document.py 02_SOPs_and_Compliance/New_SOP.md")
        sys.exit(1)

    filepath = sys.argv[1]
    count = ingest(filepath)
    if count:
        print(f"Ingestion complete.")


if __name__ == "__main__":
    main()
