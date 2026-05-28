# Changelog

Toutes les modifications notables de ce skill sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.1.1] - 2024-12-21

### Changed
- Optimisation CI : cache `node_modules` partagé entre jobs
- Nouveau job `install` dédié avec cache conditionnel
- Suppression des `pnpm install` redondants (~10-15s économisés par job)

---

## [1.1.0] - 2024-12-21

### Added
- 26 nouveaux agents focalisés suivant le Single Responsibility Principle (SRP)
- Agents qualité : `linting.md`, `formatting.md`, `git-hooks.md`, `commit-conventions.md`
- Agents CI/CD : `ci-principles.md`, `cd-principles.md`, `deployment-strategies.md`
- Agents environnement : `env-variables.md`, `docker.md`, `secrets-management.md`
- Agents repository : `git-config.md`, `branching-strategies.md`, `branch-protection.md`, `pr-templates.md`
- Agents documentation : `readme.md`, `adr.md`, `runbooks.md`
- Agents sécurité : `dependency-audit.md`, `security-headers.md`
- Agents monitoring : `metrics.md`, `logging.md`, `alerting.md`
- Agents UI/UX : `ux-principles.md`, `responsive-design.md`, `design-system.md`, `accessibility.md`

### Changed
- 8 agents volumineux convertis en orchestrateurs légers
- `quality-tools.md` → orchestrateur référençant 4 agents spécialisés
- `cicd.md` → orchestrateur référençant 3 agents spécialisés
- `environment.md` → orchestrateur référençant 3 agents spécialisés
- `repository.md` → orchestrateur référençant 4 agents spécialisés
- `documentation.md` → orchestrateur référençant 3 agents spécialisés
- `security.md` → orchestrateur référençant 2 agents spécialisés
- `monitoring.md` → orchestrateur référençant 3 agents spécialisés
- `ui-ux.md` → orchestrateur référençant 4 agents spécialisés

### Fixed
- Vulnérabilité d'injection de commande dans `audit-project.js`
- Gestion d'erreurs améliorée dans `init-project.js`
- Support multi-package-manager dans les workflows CI

## [1.0.0] - 2024-12-20

### Added
- Structure initiale avec 7 phases de développement
- 28 agents spécialisés couvrant tout le cycle de vie
- Templates de configuration (ESLint, Prettier, CommitLint, etc.)
- Workflows CI/CD pour GitHub Actions et GitLab CI
- Guides de bonnes pratiques
- Scripts utilitaires (`audit-project.js`, `init-project.js`, `check-process.js`)
- Tests unitaires (14 tests)

### Phases
1. **Discovery** : Analyse des besoins et user stories
2. **Design** : Architecture, modélisation, API design, UI/UX
3. **Setup** : Repository, environnements, CI/CD, outils qualité
4. **Development** : Standards de code, code review, documentation
5. **Testing** : Tests unitaires, intégration, E2E, performance, sécurité
6. **Deployment** : Staging, production, rollback
7. **Maintenance** : Monitoring, bug tracking, mises à jour
