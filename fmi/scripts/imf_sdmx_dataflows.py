#!/usr/bin/env python3
"""Liste les jeux de données (dataflows) de l'API SDMX du FMI."""
import json
import urllib.request

URL = "https://api.imf.org/external/sdmx/2.1/dataflow"


def main():
    req = urllib.request.Request(URL, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        flows = json.load(r)["data"]["dataflows"]
    for f in flows:
        print(f["id"], "|", f["name"])


if __name__ == "__main__":
    main()
