# Banque mondiale et FMI : fonctionnement et données

Dépôt d'étude pour comprendre comment les deux institutions fonctionnent, produisent leurs données et les exposent.

## Structure

| Dossier | Contenu |
|---|---|
| [banque-mondiale/](banque-mondiale/README.md) | Fonctionnement global, sites, API Indicateurs, script |
| [fmi/](fmi/README.md) | Fonctionnement global, sites, DataMapper et SDMX, scripts |
| [comparaison/](comparaison/01-comparaison.md) | Différences, pièges d'analyse, glossaire |
| `data/raw/` | Extractions locales (ignorées par git) |
| `notebooks/` | Analyses |

## Idée directrice

- **Banque mondiale** : prêteur de développement. Ses données décrivent le développement (pauvreté, santé, éducation, secteurs), annuelles, assemblées à partir de sources nationales, d'organisations partenaires et d'enquêtes propres.
- **FMI** : gardien de la stabilité financière. Ses données sont des statistiques macroéconomiques et financières déclarées par les pays membres, plus ses propres prévisions (WEO, deux fois par an).

## Démarrage rapide

```bash
python3 banque-mondiale/scripts/wb_indicator.py FRA NY.GDP.MKTP.CD 2015 2024
python3 fmi/scripts/imf_datamapper.py NGDPD FRA
```

Python 3.9+, aucune dépendance. Dernière vérification des API : 3 novembre 2026.
