# FMI : données et API

## DataMapper (simple)

`https://www.imf.org/external/datamapper/api/v1/{indicateur}/{pays}`

- Exemple : `.../NGDPD/FRA` (PIB nominal en milliards USD).
- Réponse : `{"values": {indicateur: {pays: {année: valeur}}}}`.
- Contient les prévisions du WEO : les années futures sont des projections.
- Liste des indicateurs : `.../api/v1/indicators`.

## API SDMX

Base : `https://api.imf.org/external/sdmx/2.1/`

- `dataflow` : catalogue des jeux de données. Vérifié : renvoie du XML SDMX 2.1, ou du JSON avec l'en-tête `Accept: application/json`.
- Identifiants de la forme `IMF.STA:NSDP(7.0.0)` : agence, identifiant, version.
- Exemples de jeux : NSDP (page récapitulative nationale), GS_CGI.
- Le modèle SDMX : dataflow, structure (dimensions, attributs), clé de série, observations.

## Ancienne API

`dataservices.imf.org/REST/SDMX_JSON.svc/` : le nom d'hôte ne se résout plus (test du 3 novembre 2026). À considérer comme retirée ; les anciens tutoriels ne fonctionnent plus.

## Jeux de données majeurs

| Sigle | Contenu |
|---|---|
| WEO | Perspectives de l'économie mondiale, avec prévisions, avril et octobre |
| IFS | Statistiques financières internationales |
| BOP | Balance des paiements |
| DOTS | Commerce par partenaire |
| GFS | Finances publiques |
| COFER | Composition des réserves de change |
| CPI | Prix à la consommation |
