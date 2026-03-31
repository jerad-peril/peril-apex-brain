#!/usr/bin/env python3
"""Apex Brain — Vector Vault Snapshot Utility
Compresses the ChromaDB store into a timestamped zip archive for
disaster recovery. Run manually or via cron before risky deployments.

Usage:
    python3 snapshot_vault.py
"""

import os
import shutil
from datetime import datetime

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(VAULT_DIR, "chromadb_store")
SNAPSHOT_DIR = os.path.join(VAULT_DIR, "vault_snapshots")


def create_snapshot():
    if not os.path.isdir(CHROMA_DIR):
        print(f"ERROR: ChromaDB directory not found at {CHROMA_DIR}")
        print("Run the vector builder first: python3 apex_vector_builder.py")
        return None

    os.makedirs(SNAPSHOT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"chroma_snapshot_{timestamp}"
    archive_path = os.path.join(SNAPSHOT_DIR, archive_name)

    print(f"Source:  {CHROMA_DIR}")
    print(f"Target:  {archive_path}.zip")

    result = shutil.make_archive(archive_path, "zip", VAULT_DIR, "chromadb_store")

    size_mb = os.path.getsize(result) / (1024 * 1024)
    print(f"Snapshot created: {result} ({size_mb:.2f} MB)")
    return result


if __name__ == "__main__":
    path = create_snapshot()
    if path:
        print("Vault snapshot secured.")
