# Veille

Fréquence actuelle : **hebdomadaire** (à ajuster plus tard par ressource dans les `ressources.xlsx`).

## Routine de la semaine

1. Ouvrir [calendrier-veille.xlsx](calendrier-veille.xlsx), feuille « Calendrier » : repérer les publications attendues.
2. Parcourir les médiathèques : blog des données ouvertes de la Banque mondiale, blogs, vidéos et podcasts du FMI, actualités de data.imf.org.
3. Contrôler les mises à jour de données : champ `lastupdated` de l'API de la Banque mondiale, millésime du WEO.
4. Consigner chaque changement dans la feuille « Journal de veille » : date, institution, thème, constat, source, impact, suivi.
5. Si un chiffre du dépôt est dépassé, mettre à jour le README du thème et `outils/donnees_veille.py`, puis régénérer.

## Régénérer les fichiers

```bash
python3 outils/generer.py --pdf
```
