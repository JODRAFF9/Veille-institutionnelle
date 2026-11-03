# Pièges fréquents

1. **Agrégats mélangés aux pays** : WLD, EUU, régions et groupes de revenu figurent dans les extractions `country/all`.
2. **Dernière année vide** : les valeurs récentes sont souvent `null` et arrivent avec un retard d'un à deux ans.
3. **Prévisions prises pour des observations** : DataMapper mélange historique et projections WEO.
4. **Révisions** : le WEO d'octobre révise celui d'avril, y compris le passé. Stocker le millésime.
5. **Unités** : USD courants, constants, PPA, milliards ou unités. Lire le champ d'unité et le nom de l'indicateur.
6. **Codes pays** : alpha-2 pour la BM dans `country.id`, alpha-3 dans `countryiso3code`. Le Kosovo (XKX) n'est pas toujours en ISO.
7. **Pagination** : oublier `per_page` tronque silencieusement les résultats à 50 lignes.
8. **Tutoriels périmés** : plusieurs points d'accès anciens du FMI ne répondent plus.
