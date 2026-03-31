#!/usr/bin/env python3
"""Jarvis Webhook Simulator
Replicates the exact POST request Make.com sends to the Apex Brain RAG API.

Usage:
    python3 jarvis_simulator.py <URL> "<query>"
    python3 jarvis_simulator.py http://localhost:9090 "What is the field ID for Insurance Carrier?"
    python3 jarvis_simulator.py https://your-app.up.railway.app "DocuSign contract status fields"
"""

import sys
import time
import json
import requests


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 jarvis_simulator.py <BASE_URL> \"<query>\"")
        print("Example: python3 jarvis_simulator.py http://localhost:9090 \"What fields track carrier info?\"")
        sys.exit(1)

    base_url = sys.argv[1].rstrip("/")
    query = " ".join(sys.argv[2:])

    # Exact payload Make.com HTTP module will send
    payload = {"query": query, "n_results": 3}
    headers = {"Content-Type": "application/json"}

    # Health check
    print(f"Target: {base_url}")
    print(f"Query:  \"{query}\"")
    print(f"{'─'*60}")

    try:
        t0 = time.time()
        h = requests.get(f"{base_url}/health", timeout=10)
        health_ms = (time.time() - t0) * 1000
        hdata = h.json()
        print(f"Health: {hdata.get('status')} | {hdata.get('chunks_indexed')} chunks | {health_ms:.0f}ms")
    except Exception as e:
        print(f"Health check failed: {e}")
        sys.exit(1)

    # Query — timed
    print(f"{'─'*60}")
    try:
        t0 = time.time()
        r = requests.post(f"{base_url}/query", json=payload, headers=headers, timeout=40)
        query_ms = (time.time() - t0) * 1000
    except requests.Timeout:
        print("TIMEOUT — response took >40s (Make.com would fail)")
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    if r.status_code != 200:
        print(f"HTTP {r.status_code}: {r.text[:300]}")
        sys.exit(1)

    data = r.json()

    # Response summary
    make_ok = "PASS" if query_ms < 40000 else "FAIL (>40s)"
    speed = "FAST" if query_ms < 2000 else "OK" if query_ms < 10000 else "SLOW"
    print(f"Response: {query_ms:.0f}ms ({speed}) | Make.com timeout check: {make_ok}")
    print(f"Total chunks in index: {data.get('total_chunks', '?')}")
    print(f"Results returned: {len(data.get('results', []))}")
    print(f"{'─'*60}")

    # Print each chunk
    for i, chunk in enumerate(data.get("results", [])):
        dist = chunk.get("distance", 0)
        relevance = "HIGH" if dist < 1.2 else "MEDIUM" if dist < 1.5 else "LOW"
        print(f"\n[{i+1}] distance={dist:.4f} ({relevance})")
        print(f"    source:  {chunk.get('source', '?')}")
        print(f"    heading: {chunk.get('heading', '?')}")
        print(f"    text:    {chunk.get('text', '')[:250]}...")

    # Raw JSON for debugging
    print(f"\n{'─'*60}")
    print("RAW JSON (for Make.com module testing):")
    print(json.dumps(data, indent=2)[:1500])


if __name__ == "__main__":
    main()
