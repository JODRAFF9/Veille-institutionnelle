#!/usr/bin/env python3
"""Télécharge un indicateur de la Banque mondiale pour un pays.

Usage : wb_indicator.py PAYS INDICATEUR [DEBUT FIN]
"""
import json
import sys
import time
import urllib.request

BASE = "https://api.worldbank.org/v2"


def fetch(country, indicator, start=None, end=None):
    url = f"{BASE}/country/{country}/indicator/{indicator}?format=json&per_page=1000"
    if start and end:
        url += f"&date={start}:{end}"
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                meta, data = json.load(r)
            return meta, data or []
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    start = sys.argv[3] if len(sys.argv) > 3 else None
    end = sys.argv[4] if len(sys.argv) > 4 else None
    meta, data = fetch(sys.argv[1], sys.argv[2], start, end)
    print(f"# base mise à jour le {meta['lastupdated']}, {meta['total']} observations")
    for o in sorted(data, key=lambda x: x["date"]):
        print(o["date"], o["value"])


if __name__ == "__main__":
    main()
