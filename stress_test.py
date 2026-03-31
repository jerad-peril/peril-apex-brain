#!/usr/bin/env python3
"""Apex Brain — Async Load Tester
Fires N concurrent POST /query requests to measure throughput and latency
under Make.com batch webhook conditions.

Usage:
    python3 stress_test.py <BASE_URL> <CONCURRENT_REQUESTS>
    python3 stress_test.py http://localhost:9090 10
    python3 stress_test.py https://your-app.up.railway.app 25
"""

import sys
import time
import asyncio
import aiohttp
import json


PAYLOAD = {"query": "What are the Loss Type options?", "n_results": 3}
TIMEOUT_SECONDS = 40  # Make.com timeout threshold


async def fire_request(session, url, request_id):
    """Send a single POST and return (id, status, elapsed_ms, chunk_count)."""
    t0 = time.time()
    try:
        async with session.post(
            url,
            json=PAYLOAD,
            timeout=aiohttp.ClientTimeout(total=TIMEOUT_SECONDS),
        ) as resp:
            elapsed = (time.time() - t0) * 1000
            body = await resp.json()
            chunks = len(body.get("results", []))
            return (request_id, resp.status, elapsed, chunks, None)
    except asyncio.TimeoutError:
        elapsed = (time.time() - t0) * 1000
        return (request_id, 0, elapsed, 0, "TIMEOUT")
    except Exception as e:
        elapsed = (time.time() - t0) * 1000
        return (request_id, 0, elapsed, 0, str(e)[:80])


async def run_load_test(base_url, n):
    url = f"{base_url.rstrip('/')}/query"

    print(f"Target:      {url}")
    print(f"Concurrent:  {n}")
    print(f"Payload:     {json.dumps(PAYLOAD)}")
    print(f"Timeout:     {TIMEOUT_SECONDS}s")
    print(f"{'─'*60}")
    print(f"Firing {n} concurrent requests...")

    async with aiohttp.ClientSession() as session:
        t_start = time.time()
        tasks = [fire_request(session, url, i) for i in range(n)]
        results = await asyncio.gather(*tasks)
        t_total = (time.time() - t_start) * 1000

    # Analyze
    successes = [r for r in results if r[1] == 200]
    failures = [r for r in results if r[1] != 200]
    times = [r[2] for r in results]
    ok_times = [r[2] for r in successes]

    print(f"{'─'*60}")
    print(f"RESULTS")
    print(f"{'─'*60}")
    print(f"  Total wall time:   {t_total:,.0f}ms")
    print(f"  Succeeded (200):   {len(successes)}/{n}")
    print(f"  Failed:            {len(failures)}/{n}")

    if ok_times:
        avg = sum(ok_times) / len(ok_times)
        print(f"  Avg response:      {avg:,.0f}ms")
        print(f"  Fastest:           {min(ok_times):,.0f}ms")
        print(f"  Slowest:           {max(ok_times):,.0f}ms")
        print(f"  P95:               {sorted(ok_times)[int(len(ok_times)*0.95)]:,.0f}ms")
        print(f"  Throughput:        {len(successes)/(t_total/1000):.1f} req/s")

        make_ok = max(ok_times) < TIMEOUT_SECONDS * 1000
        print(f"\n  Make.com safe:     {'PASS' if make_ok else 'FAIL'} (slowest {'<' if make_ok else '>'} {TIMEOUT_SECONDS}s)")
    else:
        print(f"  No successful responses.")

    if failures:
        print(f"\n  FAILURES:")
        for rid, status, elapsed, _, err in failures:
            print(f"    req#{rid}: HTTP {status} {elapsed:,.0f}ms — {err}")

    # Per-request detail
    print(f"\n{'─'*60}")
    print(f"{'Req':>4s} {'Status':>7s} {'Time':>8s} {'Chunks':>7s}")
    print(f"{'─'*60}")
    for rid, status, elapsed, chunks, err in sorted(results, key=lambda r: r[0]):
        s = f"{status}" if status == 200 else f"{err or status}"
        print(f"  {rid:>3d}   {s:>7s} {elapsed:>7.0f}ms  {chunks:>5d}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 stress_test.py <BASE_URL> <CONCURRENT_REQUESTS>")
        print("Example: python3 stress_test.py http://localhost:9090 10")
        sys.exit(1)

    base_url = sys.argv[1]
    n = int(sys.argv[2])
    asyncio.run(run_load_test(base_url, n))


if __name__ == "__main__":
    main()
