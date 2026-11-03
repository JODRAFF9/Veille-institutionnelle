# Banque mondiale : données et API

Base : `https://api.worldbank.org/v2/`

## Requêtes utiles

```
/country/FRA/indicator/NY.GDP.MKTP.CD?format=json&date=2020:2022
/country/all/indicator/SP.POP.TOTL?format=json&date=2023&per_page=300
/country?format=json&per_page=300          # liste des pays et agrégats
/indicator?format=json&source=2&per_page=100  # indicateurs d'une source
/source?format=json                        # liste des sources (2 = WDI)
```

## Forme de la réponse

Un tableau de deux éléments :

1. métadonnées de pagination (`page`, `pages`, `per_page`, `total`, `sourceid`, `lastupdated`) ;
2. liste d'observations (`indicator`, `country`, `countryiso3code`, `date`, `value`, `obs_status`).

Exemple vérifié : PIB de la France 2022 = 2 794 788 137 066,94 USD courants.

## Points d'attention

- `per_page` vaut 50 par défaut : paginer avec `page` ou monter `per_page`.
- Les valeurs manquantes sont `null`.
- Les agrégats (WLD, EUU, HIC...) sont mêlés aux pays : utiliser `/country` pour filtrer (`region.id != "NA"`).
- Codes d'indicateur : `NY.GDP.MKTP.CD` (PIB courant), `NY.GDP.MKTP.KD.ZG` (croissance), `SP.POP.TOTL` (population).
- Le champ `lastupdated` indique la version de la base.
