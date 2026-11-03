#!/usr/bin/env python3
"""Teste tous les liens des ressources et écrit un rapport Markdown.

Usage : python3 outils/verifier_liens.py [rapport.md]
Les liens qui répondent 401, 403 ou 429 sont signalés comme bloqués aux robots, pas comme cassés.
Code de sortie : 0 toujours (le rapport sert de base à l'issue hebdomadaire).
"""
import sys

from generer import libelle, tester, toutes_urls
from concurrent.futures import ThreadPoolExecutor


def main():
    urls = toutes_urls()
    with ThreadPoolExecutor(max_workers=12) as ex:
        statuts = dict(zip(urls, ex.map(tester, urls)))
    ok = [u for u, c in statuts.items() if 200 <= c < 400]
    bloques = [u for u, c in statuts.items() if c in (401, 403, 429)]
    casses = [(u, c) for u, c in statuts.items() if c not in range(200, 400) and c not in (401, 403, 429)]
    lignes = [f"**{len(urls)} liens testés** : {len(ok)} OK, {len(bloques)} bloqués aux robots (à vérifier à la main), {len(casses)} cassés.", ""]
    if casses:
        lignes.append("### Liens cassés à corriger dans `outils/donnees_veille.py`")
        lignes += [f"- {libelle(c)} : {u}" for u, c in casses]
    else:
        lignes.append("Aucun lien cassé.")
    texte = "\n".join(lignes) + "\n"
    if len(sys.argv) > 1:
        open(sys.argv[1], "w", encoding="utf-8").write(texte)
    print(texte)


if __name__ == "__main__":
    main()
