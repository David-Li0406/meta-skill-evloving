# ADR-007 : Pattern d'Extraction de Skills

## Statut

Accepté

## Date

2024-12-28

## Contexte

L'analyse de séparation des préoccupations (SEPARATION-OF-CONCERNS-REVIEW.md) a identifié deux cas où des domaines étaient suffisamment importants pour justifier leur extraction en skills autonomes :

1. **DevOps** : 6 domaines dispersés dans `backend-developer`
2. **Testing** : 34 agents testing dispersés dans 6 skills différents

### Problèmes Identifiés

#### DevOps (avant extraction)
```
backend-developer/
├── agents/devops/          # Domaine complet mais enterré
│   ├── cicd/               # 6 agents
│   ├── containers/         # 5 agents
│   ├── kubernetes/         # 6 agents
│   ├── infrastructure/     # 5 agents
│   ├── monitoring/         # 5 agents
│   └── deployment/         # 3 agents
└── ... (autres domaines backend)
```

**Problème** : DevOps est un métier distinct du développement backend. L'imbrication créait :
- Confusion dans le routage
- Difficultés à trouver les agents DevOps
- Couplage artificiel avec les concepts backend

#### Testing (avant extraction)
```
Agents testing dispersés :
├── backend-developer/testing/       # 5 agents
├── frontend-developer/testing/      # 4 agents
├── react-expert/testing/            # 4 agents
├── nextjs-expert/testing/           # 5 agents
├── wordpress-gutenberg/testing/     # 6 agents
└── web-dev-process/testing/         # 10 agents
```

**Problème** : La méthodologie de test (QUOI/QUAND tester) était mélangée avec l'implémentation (COMMENT coder les tests). Cela créait :
- Duplication des concepts (pyramide, TDD, coverage)
- Incohérence des recommandations
- Pas de source unique de vérité pour la stratégie de tests

## Décision

### Critères d'Extraction

Un domaine justifie son extraction en skill autonome quand :

| Critère | Description | Seuil |
|---------|-------------|-------|
| **Taille** | Nombre d'agents potentiels | > 15 agents |
| **Cohésion** | Agents qui collaborent fortement entre eux | > 80% d'interactions internes |
| **Indépendance** | Peut fonctionner sans le skill parent | Autonomie > 70% |
| **Métier distinct** | Correspond à un rôle/expertise reconnu | Oui/Non |
| **Fragmentation** | Dispersé dans plusieurs skills | > 2 skills |

### Évaluation DevOps

| Critère | Évaluation | Score |
|---------|------------|-------|
| Taille | 30 agents potentiels | ✅ |
| Cohésion | CI/CD, containers, K8s très liés | ✅ |
| Indépendance | Peut déployer sans coder le backend | ✅ |
| Métier distinct | "DevOps Engineer" est un métier | ✅ |
| Fragmentation | Était uniquement dans backend-dev | ⚠️ |

**Décision** : Extraire en skill `devops` (NIVEAU 3 IMPLÉMENTATION)

### Évaluation Testing

| Critère | Évaluation | Score |
|---------|------------|-------|
| Taille | 34+ agents identifiés | ✅ |
| Cohésion | Stratégie tests cohérente | ✅ |
| Indépendance | Méthodologie indépendante de l'implémentation | ✅ |
| Métier distinct | "QA Engineer" est un métier | ✅ |
| Fragmentation | Dispersé dans 6 skills | ✅ |

**Décision** : Créer skill `testing-process` (NIVEAU 2 PROCESSUS)

### Pattern d'Extraction

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 : IDENTIFICATION                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • Inventorier tous les agents du domaine                                    │
│  • Évaluer les critères d'extraction                                         │
│  • Déterminer le niveau hiérarchique approprié                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 : SÉPARATION PROCESS/IMPLÉMENTATION                                 │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • PROCESS (QUOI/QUAND) → Nouveau skill NIVEAU 2 si approprié               │
│  • IMPLÉMENTATION (COMMENT) → Reste dans skills techniques                  │
│  • Éviter la duplication entre les deux                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 : CRÉATION DU NOUVEAU SKILL                                         │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • SKILL.md avec routage complet                                             │
│  • orchestrator.md avec délégation                                           │
│  • Agents organisés par domaine                                              │
│  • Tests de validation                                                       │
│  • CHANGELOG.md                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 : MISE À JOUR DES RÉFÉRENCES                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • Skill parent redirige vers nouveau skill                                  │
│  • web-agency inclut le nouveau skill                                        │
│  • routing.md et composition.md mis à jour                                   │
│  • dependency-graph.md mis à jour                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ÉTAPE 5 : VALIDATION                                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│  • Tests passent (100% agents)                                               │
│  • CI workflow fonctionne                                                    │
│  • Documentation cohérente                                                   │
│  • Pas de duplication                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Résultat de l'Extraction

### DevOps

```
.web-agency/skills/devops/              # NOUVEAU SKILL
├── SKILL.md                        # Définition complète
├── CHANGELOG.md                    # Historique
├── orchestrator.md                 # Délégation
├── agents/
│   ├── cicd/                       # 6 agents
│   ├── containers/                 # 5 agents
│   ├── kubernetes/                 # 6 agents
│   ├── infrastructure/             # 5 agents
│   ├── monitoring/                 # 5 agents
│   └── deployment/                 # 3 agents
└── tests/                          # Validation

backend-developer/                  # MODIFIÉ
└── [redirige queries DevOps vers skill devops]
```

### Testing-Process

```
.web-agency/skills/testing-process/     # NOUVEAU SKILL
├── SKILL.md                        # Définition complète
├── orchestrator.md                 # Délégation
├── agents/
│   ├── strategy/                   # 5 agents (pyramide, TDD/BDD, planning)
│   ├── types/                      # 5 agents (unit, integration, e2e)
│   ├── quality/                    # 4 agents (coverage, mutation, flaky)
│   ├── performance/                # 4 agents (load, frontend-perf)
│   ├── security/                   # 4 agents (OWASP, dependencies)
│   └── accessibility/              # 3 agents (WCAG, audit)
└── tests/                          # Validation

[autres skills]/testing/            # CONSERVÉS
└── [implémentation spécifique au framework]
```

## Distinction Clé : Process vs Implémentation

### Pour Testing

| testing-process (NIVEAU 2) | [skill]-developer/testing (NIVEAU 3) |
|----------------------------|--------------------------------------|
| QUOI tester | COMMENT tester |
| Pyramide de tests (70/20/10) | Configuration Vitest/Jest |
| Stratégie TDD/BDD | Mocks, fixtures spécifiques |
| Coverage targets | Coverage config framework |
| Types de tests à écrire | Patterns de tests framework |

### Pour DevOps

| direction-technique/infra (NIVEAU 1) | devops (NIVEAU 3) |
|--------------------------------------|-------------------|
| Choix cloud provider | Configuration Terraform AWS/GCP |
| Politique CI/CD | GitHub Actions YAML |
| Standards Kubernetes | Helm charts, manifests |

## Conséquences

### Positives

- **Clarté** : Chaque skill a une responsabilité unique claire
- **Découvrabilité** : Plus facile de trouver les bons agents
- **Cohérence** : Source unique de vérité pour chaque domaine
- **Scalabilité** : Nouveau skills peuvent être ajoutés sans toucher aux existants

### Négatives

- **Complexité** : Plus de skills à maintenir (12 vs 10 avant)
- **Routage** : Règles de routage plus nombreuses
- **Documentation** : Graphe de dépendances plus complexe

### Métriques

| Métrique | Avant | Après |
|----------|-------|-------|
| Nombre de skills | 10 | 12 |
| Agents total | 384 | 409 |
| Duplication testing | ~34 agents fragmentés | 25 agents consolidés |
| Routage DevOps | Implicite via backend | Explicite skill dédié |

## Non-Extraction : Sécurité

L'analyse a montré que les 21 agents sécurité sont déjà bien organisés par niveau :

```
direction-technique/securite (NIVEAU 1) → Politique
testing-process/security (NIVEAU 2) → Tests
backend-developer/auth-security (NIVEAU 3) → Implémentation
```

**Décision** : Pas d'extraction car la séparation des préoccupations est déjà respectée.

## Références

- [SEPARATION-OF-CONCERNS-REVIEW.md](../../../../docs/analysis/SEPARATION-OF-CONCERNS-REVIEW.md)
- [ADR-005 : Frontières de responsabilités](./005-skill-responsibility-boundaries.md)
- [ADR-006 : Hiérarchie lead-dev/web-dev-process](./006-hierarchy-clarification.md)
- [dependency-graph.md](../../orchestration/dependency-graph.md)
