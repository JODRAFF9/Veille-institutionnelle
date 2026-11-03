# Veille institutionnelle

Dépôt de veille et d'étude : comprendre en profondeur comment chaque institution fonctionne, comment elle produit et expose ses données, et suivre ses publications. Fréquence de veille actuelle : **hebdomadaire**.

| Dossier | Contenu |
|---|---|
| [banque-mondiale/](banque-mondiale/README.md) | 11 thèmes, sous-dossiers par site de données, présentation globale |
| [fmi/](fmi/README.md) | 12 thèmes, sous-dossiers par site de données, présentation globale |
| [banque-africaine-de-developpement/](banque-africaine-de-developpement/README.md) | BAD : 11 thèmes, sous-dossiers par portail de données |
| [union-africaine/](union-africaine/README.md) | UA : 10 thèmes, communautés économiques régionales, Agenda 2063 |
| [ocde/](ocde/README.md) | OCDE : 11 thèmes, normes, examens par les pairs, sous-dossiers par portail de données |
| [commissions-economiques-regionales/](commissions-economiques-regionales/README.md) | Cinq commissions régionales de l'ONU, un sous-dossier par commission |
| [veille/](veille/README.md) | Routine hebdomadaire, calendrier des publications, journal de veille |
| [comparaison/](comparaison/01-comparaison.md) | Différences, pièges d'analyse, glossaire |
| [outils/](outils/) | Source du contenu, générateur Excel et Beamer, vérificateur de liens |

Dans chaque dossier thématique :

- `README.md` : explication du thème
- `ressources.xlsx` : liens de compréhension, rythme de publication, fréquence de veille, statut du lien
- `presentation.tex` et `presentation.pdf` : présentation Beamer

Chaque institution a aussi une `presentation-globale.tex` (et son PDF). Pour ajouter une institution : [CONVENTIONS.md](CONVENTIONS.md).

## Démarrage rapide

```bash
python3 banque-mondiale/scripts/wb_indicator.py FRA NY.GDP.MKTP.CD 2015 2024
python3 fmi/scripts/imf_datamapper.py NGDPD FRA
python3 outils/generer.py --pdf
```

Python 3.9+ (openpyxl pour les Excel) et pdflatex pour les PDF. Dernière vérification des liens et API : 3 novembre 2026.
