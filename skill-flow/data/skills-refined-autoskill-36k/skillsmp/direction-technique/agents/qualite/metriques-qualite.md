---
name: metriques-qualite
description: Politique de métriques qualité (Niveau POURQUOI)
workflows:
  - id: wf-audit
    phase: Analyse
    recurrence: hebdomadaire
---

# Politique de Métriques Qualité

Tu définis les **politiques et standards** de suivi des métriques de qualité technique.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les MÉTRIQUES à suivre et les seuils cibles
> **Ce que tu ne fais pas** : Configurer SonarQube ou écrire les scripts de collecte
>
> → Process de qualité : `web-dev-process/agents/testing/*`
> → Implémentation : Skills technologiques spécialisés

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi mesurer ? Pour garantir et améliorer la qualité"   │
│  → "Standards : métriques, seuils, actions"                     │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi mesurer ? Coverage, smells, vulnérabilités"            │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (skills technologiques)                     │
│  → "Code : SonarQube config, GitHub Actions, scripts"           │
└─────────────────────────────────────────────────────────────────┘
```

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quels sont les standards qualité existants dans l'équipe ?
- Existe-t-il déjà une Definition of Done ?
- Quelles sont les métriques qualité actuelles ?
- Y a-t-il une dette technique documentée ?

### Objectifs
- Quels sont les objectifs de qualité à atteindre ? (Coverage, complexité)
- Quelle est la maturité souhaitée de l'équipe ?
- Y a-t-il des exigences client spécifiques sur la qualité ?
- Quels sont les critères de release ?

### Risques
- Quel est le niveau de dette technique actuel ?
- Y a-t-il des zones de code legacy critiques ?
- Quels sont les points de non-qualité récurrents ?
- Y a-t-il des contraintes de délai vs qualité ?

---

## Catégories de Métriques

### 1. Couverture de Tests

| Métrique | Cible | Minimum | Outil |
|----------|-------|---------|-------|
| Coverage global | > 80% | 70% | Jest, PHPUnit |
| Coverage branches | > 70% | 60% | Idem |
| Coverage fonctions | > 85% | 75% | Idem |
| Coverage lignes | > 80% | 70% | Idem |

### 2. Qualité du Code

| Métrique | Cible | Alerte | Outil |
|----------|-------|--------|-------|
| Code smells | < 5/kloc | > 10/kloc | SonarQube |
| Duplication | < 3% | > 5% | SonarQube |
| Complexité cyclomatique | < 10/fonction | > 15 | ESLint, SonarQube |
| Maintainability Index | > 20 | < 10 | SonarQube |
| Technical Debt Ratio | < 5% | > 10% | SonarQube |

### 3. Sécurité

| Métrique | Cible | Action si Non-Conforme |
|----------|-------|------------------------|
| Vulnérabilités critiques | 0 | Bloquer deploy |
| Vulnérabilités hautes | 0 | Bloquer deploy |
| Vulnérabilités moyennes | < 5 | Corriger sous 1 semaine |
| Security Hotspots | 100% reviewed | Review obligatoire |
| Dépendances outdated | < 20% | Mise à jour mensuelle |

### 4. Performance (Core Web Vitals)

| Métrique | Bon | À Améliorer | Mauvais |
|----------|-----|-------------|---------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| FID (First Input Delay) | < 100ms | 100-300ms | > 300ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |
| TTFB (Time To First Byte) | < 600ms | 600-1000ms | > 1000ms |
| Score Lighthouse | > 90 | 70-90 | < 70 |

### 5. Fiabilité

| Métrique | Cible | Outil |
|----------|-------|-------|
| Bugs en production | < 5/mois | Jira, Sentry |
| MTTR | < 4h | Incident tracking |
| Disponibilité | > 99.9% | Monitoring |
| Taux d'erreur API | < 0.1% | APM |

---

## Quality Gate

### Critères Obligatoires

| Condition | Seuil | Action si Échec |
|-----------|-------|-----------------|
| Coverage on New Code | ≥ 80% | Bloquer merge |
| Duplicated Lines on New Code | ≤ 3% | Bloquer merge |
| Maintainability Rating | A | Warning |
| Reliability Rating | A | Bloquer merge |
| Security Rating | A | Bloquer merge |
| Security Hotspots Reviewed | 100% | Bloquer merge |

### Niveaux de Rating

| Rating | Description |
|--------|-------------|
| A | Optimal |
| B | Acceptable |
| C | À améliorer |
| D | Problématique |
| E | Critique |

---

## Seuils d'Alerte

| Métrique | Warning | Critical | Action |
|----------|---------|----------|--------|
| Coverage | < 75% | < 60% | Bloquer merge |
| Bugs | > 0 | > 2 | Fix immédiat |
| Vulnérabilités | > 0 medium | > 0 high | Bloquer deploy |
| Lighthouse | < 80 | < 60 | Investigation |
| Tech Debt | > 10% sprint | > 20% sprint | Escalade |

---

## Reporting Qualité

### Contenu Rapport Hebdomadaire

| Section | Éléments |
|---------|----------|
| **Résumé** | Comparaison semaine N vs N-1 |
| **Highlights** | Améliorations et points d'attention |
| **Tendances** | Graphique évolution |
| **Actions** | Responsable et deadline |

### Contenu Rapport Sprint

| Section | Éléments |
|---------|----------|
| **Quality Gate** | PASSED/FAILED |
| **Coverage par module** | Table avec tendances |
| **Code Quality** | Bugs, smells, duplication |
| **Performance** | Métriques par page |
| **Recommandations** | Priorités haute/moyenne/basse |

---

## Dashboard de Qualité

### Panneaux Obligatoires

| Panneau | Contenu |
|---------|---------|
| **Coverage** | Gauge avec tendance |
| **Tests** | Passing/failing count |
| **Code Smells** | Nombre et tendance |
| **Duplication** | Pourcentage |
| **Security** | Issues par sévérité |
| **Lighthouse** | Score par page |
| **Tech Debt** | Estimation en heures |

### Indicateurs Visuels

| Status | Description |
|--------|-------------|
| ✅ | Dans la cible |
| 🟠 | Attention (proche du seuil) |
| 🔴 | Critique (hors cible) |
| ↗️ | Amélioration |
| → | Stable |
| ↘️ | Dégradation |

---

## Checklist Qualité

### Par PR

- [ ] Tests ajoutés pour nouveau code
- [ ] Coverage maintenue ou améliorée
- [ ] Pas de nouveaux bugs
- [ ] Pas de nouvelles vulnérabilités
- [ ] Complexité acceptable

### Par Sprint

- [ ] Quality Gate passé
- [ ] Tech debt stable ou en diminution
- [ ] Rapport qualité produit
- [ ] Actions identifiées et assignées

---

## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| Quality Gate failed | Bloquer merge, corriger | Développeur |
| Coverage en chute libre | Rétrospective + plan | Tech Lead |
| Vulnérabilité critique | Patch immédiat | Équipe |
| Performance dégradée | Investigation urgente | Tech Lead |

---

## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Process de test | `web-dev-process/agents/testing/*` |
| Code review | `qualite/code-review` |
| Conventions | `qualite/conventions-code` |
| Implémentation | Skills technologiques spécialisés |

### Ressources Externes

- [SonarQube Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [Google Core Web Vitals](https://web.dev/vitals/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Livrables

| Livrable | Description |
|----------|-------------|
| Tableau de bord qualité | Métriques temps réel (couverture, duplication, complexité, vulns) |
| Quality gates | Seuils de qualité bloquants configurés dans CI/CD |
| Rapports d'évolution qualité | Tendances et alertes sur dégradation des métriques |
