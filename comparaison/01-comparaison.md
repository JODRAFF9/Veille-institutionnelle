# Banque mondiale et FMI : comparaison

| Aspect | Banque mondiale | FMI |
|---|---|---|
| Fonction des données | Développement, pauvreté, secteurs | Macroéconomie, finance, surveillance |
| Origine | Instituts nationaux, ONU, enquêtes propres | Déclarations des pays membres, services du FMI |
| Prévisions | Peu (Global Economic Prospects, janvier et juin) | WEO, avril et octobre |
| Fréquence dominante | Annuelle | Mensuelle, trimestrielle, annuelle |
| Codes pays | ISO alpha-2 et alpha-3 | Alpha-3 (DataMapper), codes propres selon la base |
| Format API | JSON simple, deux éléments | JSON DataMapper ou SDMX |
| Versionnement | Base datée (`lastupdated`) | Millésime (WEO avril 2026, etc.) |

## Conséquence pratique

Un même agrégat (PIB, dette, inflation) peut différer entre les deux sources : champ de définition, année de base, taux de change, date de mise à jour. Toujours noter la source, l'indicateur et la date d'extraction.
