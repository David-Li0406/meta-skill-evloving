# Checklists par Phase

Utilisez ces checklists pour vous assurer que chaque phase est complète avant de passer à la suivante.

---

## Phase 1: Discovery ✓

### Objectifs
- [ ] Problème à résoudre clairement identifié
- [ ] Utilisateurs cibles définis
- [ ] Objectifs business documentés

### Livrables
- [ ] Brief projet rédigé
- [ ] Liste des exigences (fonctionnelles et non-fonctionnelles)
- [ ] User stories avec critères d'acceptation
- [ ] Définition du MVP (scope in/out)
- [ ] Priorisation MoSCoW effectuée

### Validation
- [ ] Stakeholders ont validé le scope
- [ ] Équipe technique a confirmé la faisabilité
- [ ] Budget et délais alignés

---

## Phase 2: Design ✓

### Architecture
- [ ] Style d'architecture choisi et documenté
- [ ] ADR (Architecture Decision Record) rédigé
- [ ] Diagramme d'architecture créé
- [ ] Stack technique définie

### Données
- [ ] Modèle de données conçu (ERD)
- [ ] Types de base de données choisis
- [ ] Stratégie de migration définie

### API
- [ ] Design d'API documenté
- [ ] Spécification OpenAPI/GraphQL schema prêt
- [ ] Conventions de nommage définies
- [ ] Stratégie de versioning choisie

### UI/UX
- [ ] Wireframes/maquettes créés
- [ ] Design system identifié
- [ ] Accessibilité prise en compte (WCAG)
- [ ] Responsive design planifié

### Validation
- [ ] Revue technique effectuée
- [ ] Équipe alignée sur les choix

---

## Phase 3: Setup ✓

### Repository
- [ ] Repo Git initialisé
- [ ] .gitignore configuré
- [ ] Stratégie de branches définie
- [ ] Protection de branches activée
- [ ] Templates PR/Issues créés

### Environnement
- [ ] .env.example créé et documenté
- [ ] Docker/Docker Compose configuré (si applicable)
- [ ] Environnements dev/staging/prod définis
- [ ] Secrets gérés de manière sécurisée

### Qualité
- [ ] ESLint/Linter configuré
- [ ] Prettier/Formatter configuré
- [ ] Pre-commit hooks (Husky) actifs
- [ ] Commitlint configuré
- [ ] EditorConfig créé

### CI/CD
- [ ] Pipeline CI configuré
- [ ] Tests automatisés dans CI
- [ ] Build automatisé
- [ ] Déploiement staging automatique

### Validation
- [ ] Nouveau développeur peut setup en < 30 min
- [ ] Documentation de setup à jour

---

## Phase 4: Development ✓

### Standards
- [ ] Conventions de code documentées
- [ ] Structures de fichiers définies
- [ ] Patterns de code identifiés

### Workflow
- [ ] Process de PR documenté
- [ ] Guidelines de code review partagées
- [ ] Conventional commits utilisés
- [ ] Branch naming convention suivie

### Documentation
- [ ] README à jour
- [ ] Documentation technique rédigée
- [ ] ADRs pour les décisions importantes
- [ ] Commentaires code où nécessaire

### Validation
- [ ] Code review systématique
- [ ] Pas de code mergé sans tests
- [ ] Documentation mise à jour avec le code

---

## Phase 5: Testing ✓

### Tests Unitaires
- [ ] Tests unitaires écrits
- [ ] Couverture > 80% sur code critique
- [ ] Mocks/stubs appropriés

### Tests d'Intégration
- [ ] Tests API écrits
- [ ] Tests BDD si applicable
- [ ] Environnement de test isolé

### Tests E2E
- [ ] Parcours critiques couverts
- [ ] Tests cross-browser (si applicable)
- [ ] Tests mobile (si applicable)

### Qualité
- [ ] Tests de performance (si applicable)
- [ ] Tests d'accessibilité passent
- [ ] Audit de sécurité effectué
- [ ] Pas de vulnérabilités connues

### Validation
- [ ] Tous les tests passent en CI
- [ ] Pas de tests flaky
- [ ] Couverture de code satisfaisante

---

## Phase 6: Deployment ✓

### Staging
- [ ] Environnement staging fonctionnel
- [ ] Données de test en place
- [ ] Smoke tests passent
- [ ] QA manuelle effectuée

### Production
- [ ] Checklist pré-déploiement complétée
- [ ] Backup base de données effectué
- [ ] Migrations testées
- [ ] Health checks configurés

### Monitoring
- [ ] Métriques collectées
- [ ] Alertes configurées
- [ ] Logs accessibles
- [ ] Dashboard créé

### Rollback
- [ ] Plan de rollback documenté
- [ ] Rollback testé
- [ ] Équipe disponible post-déploiement

### Validation
- [ ] Déploiement réussi
- [ ] Smoke tests prod OK
- [ ] Métriques stables
- [ ] Communication effectuée (changelog)

---

## Phase 7: Maintenance ✓

### Monitoring
- [ ] Golden Signals surveillés (latency, traffic, errors, saturation)
- [ ] Alertes fonctionnelles
- [ ] Logs structurés
- [ ] Traces distribuées (si applicable)

### Bug Tracking
- [ ] Processus de triage défini
- [ ] SLA par priorité définis
- [ ] Error tracking (Sentry) configuré
- [ ] Status page opérationnelle

### Updates
- [ ] npm audit clean (0 vulnérabilités)
- [ ] Dépendances à jour
- [ ] Renovate/Dependabot configuré
- [ ] Dette technique documentée

### Récurrent
- [ ] Revue hebdomadaire des alertes
- [ ] Mise à jour mensuelle des dépendances
- [ ] Audit trimestriel de sécurité
- [ ] Sprint de maintenance régulier (20% du temps)

---

## Checklist Globale - Avant Release

```
PRE-RELEASE CHECKLIST

□ Discovery complète et validée
□ Design reviewé et approuvé
□ Environnement configuré et documenté
□ Code développé selon les standards
□ Tests passent à 100%
□ Staging validé
□ Production prête
□ Monitoring en place
□ Plan de rollback prêt
□ Équipe notifiée
□ Documentation à jour

GO / NO-GO: ____________
Date: ____________
Responsable: ____________
```

---

## Utilisation

1. **Nouveau projet** : Suivre les phases dans l'ordre
2. **Projet existant** : Identifier les phases incomplètes
3. **Amélioration continue** : Revue régulière des checklists

Adaptez ces checklists à votre contexte - tous les items ne sont pas nécessaires pour tous les projets.
