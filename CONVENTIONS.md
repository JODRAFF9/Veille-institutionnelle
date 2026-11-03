# Convention pour ajouter une institution

Chaque institution a son dossier à la racine (minuscules, tirets), organisé en sous-dossiers thématiques numérotés.

## Thèmes de base (à adapter)

1. `histoire-et-mission`
2. `gouvernance` (et `groupe-et-institutions` si structure complexe)
3. `financement`
4. `activites-principales` (projets, surveillance, prêts, programmes)
5. `recherche-et-publications`
6. `donnees` : un sous-dossier par site ou portail (portail, catalogue, API, médiathèque : blogs, vidéos, podcasts, tutoriels)
7. `classifications`
8. `evaluation-et-controle`
9. `plans-strategiques`
10. `critiques-et-debats`

## Contenu de chaque dossier thématique

- `README.md`
- `ressources.xlsx` : généré, liens, rythme de publication, fréquence de veille, statut
- `presentation.tex` et `presentation.pdf` : Beamer, bleu #0000FF, fond crème, sans ornements

## Procédure

1. Ajouter l'institution dans `outils/donnees_veille.py` (thèmes, points clés, ressources, calendrier, sous-dossiers).
2. Lancer `python3 outils/generer.py --pdf`.
3. Écrire le `README.md` de l'institution et de chaque thème.
4. Ajouter une ligne dans `comparaison/` et dans le README racine.

## Règles

- Chaque chiffre contestable porte « à vérifier » et une date.
- Liens testés avant publication. Les sites qui bloquent les robots (HTTP 403) sont marqués « à vérifier à la main », sans contournement.
- Scripts Python standard avec nouvelle tentative réseau.
- Textes sans tirets longs, sources et dates systématiques.
