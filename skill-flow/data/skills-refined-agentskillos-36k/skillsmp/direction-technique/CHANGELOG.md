# Changelog

Toutes les modifications notables de ce skill sont documentées ici.

Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

## [2.1.0] - 2025-12-22

### Added
- Infrastructure JSON pour sortie CI (`OUTPUT_FORMAT=json`)
- Classe `TestReporter` pour rapport structuré
- Script `npm run test:json` pour intégration CI
- Permissions d'exécution sur les fichiers de test
- CHANGELOG.md avec historique et guide de migration
- tests/README.md avec documentation complète
- `.gitattributes` pour line endings consistants (LF)
- `.editorconfig` pour formatage uniforme

### Changed
- Migration de tous les tests vers `TestReporter` pour JSON natif
- Amélioration du contexte d'erreur (chemins complets)
- package.json: `private: true` et documentation zéro-dépendance
- Regex code blocks : `[\w-]*` pour langages avec tirets (`objective-c`, `shell-session`)
- Liste langages étendue : `c`, `cpp`, `makefile`, `promql`, `diff`, etc.
- CI workflow: utilise JSON output pour extraction fiable des compteurs

### Fixed
- Comparaison CSRF timing-safe avec `crypto.timingSafeEqual()`
- Documentation seuils de validation dans config.js

### Security
- CSP nonce-based au lieu de `'unsafe-inline'`
- Protection CSRF Double Submit Cookie avec :
  - Comparaison timing-safe (évite timing attacks)
  - Warnings sur pièges courants
  - Table des alternatives par framework
- Anonymisation RGPD avec ID aléatoire sans lien userId
- Sanitisation des erreurs Zod pour éviter l'exposition de secrets

## [2.0.1] - 2025-12-22

### Added
- Workflows et diagrammes pour les 7 orchestrators incomplets
- Sections Entrées/Sorties pour chaque orchestrator
- Sections Désambiguïsation pour mots-clés partagés
- Documentation des conventions de nommage
- Documentation de la gestion de casse des mots-clés

### Changed
- Regex pour supporter les chiffres dans les noms (`[a-z0-9-]+`)
- Validation du routing exclut les sections désambiguïsation

## [2.0.0] - 2025-12-22

### Added
- CI workflow GitHub Actions (`.github/workflows/direction-technique-tests.yml`)
- Section "Priorité des Mots-Clés" dans SKILL.md
- Support multi-ligne et arrays dans parseFrontmatter
- Gestion d'erreur robuste dans les tests

### Changed
- Regex code blocks : `/```(\w*)[ \t]*(?:\n|$)/g`
- Pattern frontmatter plus robuste

## [1.0.0] - 2025-12-22

### Added
- Restructuration du skill "technical" en "direction-technique"
- 10 domaines spécialisés :
  - `avant-projet` - Audits, POC, études de faisabilité
  - `specification` - Specs techniques, API, modélisation
  - `architecture` - ADR, patterns, microservices
  - `estimation` - Chiffrage, planning, risques
  - `qualite` - Tests, code review, dette technique
  - `securite` - OWASP, RGPD, gestion secrets
  - `performance` - Optimisation, caching, monitoring
  - `infrastructure` - CI/CD, Docker, cloud
  - `communication` - Documentation, vulgarisation
  - `support` - Debug, incidents, maintenance
- 52 agents spécialisés au total
- Suite de tests complète (6 validateurs)
- Orchestrators avec tables de routage

---

## Migration depuis "technical"

Si vous utilisiez l'ancien skill `technical`, mettez à jour vos références :

```diff
- Utiliser le skill `technical`
+ Utiliser le skill `direction-technique`
```

### Mapping des anciens agents

| Ancien | Nouveau |
|--------|---------|
| `technical/audit` | `direction-technique/avant-projet/audit-existant` |
| `technical/architecture` | `direction-technique/architecture/architecture-applicative` |
| `technical/security` | `direction-technique/securite/securite-applicative` |
| `technical/testing` | `direction-technique/qualite/strategie-test` |
| `technical/devops` | `direction-technique/infrastructure/ci-cd` |
| `technical/documentation` | `direction-technique/communication/documentation-technique` |
