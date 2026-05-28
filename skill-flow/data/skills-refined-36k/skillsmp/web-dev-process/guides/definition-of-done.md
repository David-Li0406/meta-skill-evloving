# Definition of Done (DoD)

Ce document définit les critères à respecter pour considérer une tâche comme terminée. La DoD garantit un niveau de qualité constant et évite les allers-retours.

---

## Principes

1. **Une tâche non terminée n'est pas terminée** : Pas de "presque fini"
2. **La DoD est non-négociable** : Tous les critères doivent être remplis
3. **La DoD évolue** : Elle s'adapte aux besoins de l'équipe

---

## DoD par Type de Tâche

### Feature (Nouvelle fonctionnalité)

#### Code
- [ ] Le code compile sans erreur
- [ ] Le code respecte les conventions du projet
- [ ] Pas de `console.log`, `debugger`, ou code de debug
- [ ] Pas de code commenté sans raison
- [ ] Les types TypeScript sont corrects (pas de `any` sauf justifié)
- [ ] Les edge cases sont gérés
- [ ] Les erreurs sont gérées proprement

#### Tests
- [ ] Tests unitaires écrits et passent
- [ ] Tests d'intégration si applicable
- [ ] Couverture de code maintenue (seuil du projet)
- [ ] Tous les tests existants passent

#### Review
- [ ] Code review approuvée par au moins 1 reviewer
- [ ] Tous les commentaires de review traités
- [ ] Auto-review effectuée avant demande de review

#### Documentation
- [ ] README mis à jour si nécessaire
- [ ] JSDoc/TSDoc pour les fonctions complexes
- [ ] CHANGELOG mis à jour
- [ ] ADR créé si décision architecturale

#### Qualité
- [ ] Linter passe sans erreur
- [ ] Formatage correct (Prettier)
- [ ] Pas de warnings TypeScript
- [ ] Pas de dépendances inutiles ajoutées

#### Déploiement
- [ ] CI passe au vert
- [ ] Testé en environnement de staging
- [ ] Pas de régression détectée

---

### Bug Fix (Correction de bug)

#### Code
- [ ] Le bug est corrigé
- [ ] La cause racine est identifiée et traitée
- [ ] Pas de régression introduite
- [ ] Le code respecte les conventions

#### Tests
- [ ] Test de non-régression ajouté
- [ ] Le test reproduit le bug avant fix
- [ ] Le test passe après fix
- [ ] Tous les tests existants passent

#### Review
- [ ] Code review approuvée
- [ ] Reproduction du bug confirmée par reviewer

#### Documentation
- [ ] CHANGELOG mis à jour
- [ ] Commentaire expliquant le fix si logique non évidente

---

### Refactoring

#### Code
- [ ] Le comportement est identique (pas de changement fonctionnel)
- [ ] Le code est plus lisible/maintenable
- [ ] Les performances sont égales ou meilleures
- [ ] Pas de dette technique ajoutée

#### Tests
- [ ] Tous les tests existants passent
- [ ] Nouveaux tests si couverture améliorée
- [ ] Tests de performance si applicable

#### Review
- [ ] Code review approuvée
- [ ] Justification du refactoring claire

---

### Documentation

#### Contenu
- [ ] Information correcte et à jour
- [ ] Exemples de code fonctionnels
- [ ] Liens valides
- [ ] Pas de fautes d'orthographe

#### Format
- [ ] Markdown valide
- [ ] Structure claire avec headings
- [ ] Table des matières si document long

#### Review
- [ ] Relu par au moins 1 personne
- [ ] Accessible aux nouveaux arrivants

---

## Checklist Universelle

Cette checklist s'applique à TOUTE tâche :

```markdown
## Avant de marquer comme terminé

### Code & Qualité
- [ ] `pnpm lint` passe
- [ ] `pnpm typecheck` passe
- [ ] `pnpm test` passe
- [ ] Pas de TODO sans ticket associé

### Git
- [ ] Commits suivent Conventional Commits
- [ ] Historique propre (pas de "fix typo" x10)
- [ ] Branch à jour avec main

### Review
- [ ] PR créée avec template rempli
- [ ] Reviewers assignés
- [ ] Review approuvée
- [ ] CI au vert

### Documentation
- [ ] CHANGELOG si changement visible
- [ ] README si nouveau setup nécessaire
```

---

## Anti-patterns

### Ce qui n'est PAS "Done"

❌ "C'est mergé" (sans tests)
❌ "Ça marche chez moi" (pas testé ailleurs)
❌ "On fera les tests plus tard"
❌ "La doc sera faite dans une autre PR"
❌ "Y'a juste ce bug mineur à fixer"
❌ "Le reviewer va corriger ça"

### Signaux d'Alerte

- PR qui traîne depuis plus de 3 jours
- Trop de "minor fix" après review
- Tests désactivés ou skippés
- Coverage qui baisse

---

## Exceptions

### Quand peut-on déroger à la DoD ?

1. **Hotfix critique** : Peut être mergé avec DoD partielle, mais une PR de suivi doit compléter la DoD dans les 24h
2. **Prototype/Spike** : Clairement identifié comme tel, avec ticket de suivi pour le cleanup

### Process d'Exception

1. Documenter pourquoi la DoD n'est pas respectée
2. Créer un ticket pour le travail restant
3. Obtenir l'accord du Tech Lead
4. Ne pas répéter

---

## Métriques

Pour suivre le respect de la DoD :

| Métrique | Cible |
|----------|-------|
| PRs mergées sans CI verte | 0% |
| Features sans tests | 0% |
| Bugs réouverts | < 5% |
| Temps moyen de review | < 24h |
| PRs avec exceptions DoD | < 5% |

---

## Évolution de la DoD

La DoD est revue :
- À chaque rétrospective
- Quand un bug de prod révèle un manque
- Quand l'équipe grandit

Pour proposer un changement :
1. Discuter en rétrospective
2. Documenter le changement
3. Communiquer à toute l'équipe
4. Mettre à jour ce document

---

**Rappel : La qualité n'est pas négociable. Une tâche bien faite maintenant évite des heures de debug plus tard.**
