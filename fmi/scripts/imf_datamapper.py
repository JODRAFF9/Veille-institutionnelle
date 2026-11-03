#!/usr/bin/env python3
"""Télécharge un indicateur du FMI via DataMapper.

Usage : imf_datamapper.py INDICATEUR PAYS
Les années futures sont des prévisions du WEO.
"""
import json
import sys
import urllib.request

BASE = "https://www.imf.org/external/datamapper/api/v1"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    ind, country = sys.argv[1:]
    with urllib.request.urlopen(f"{BASE}/{ind}/{country}", timeout=30) as r:
        values = json.load(r)["values"][ind][country]
    for year in sorted(values):
        print(year, values[year])


if __name__ == "__main__":
    main()
