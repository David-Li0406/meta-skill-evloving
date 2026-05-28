---
name: devops
description: |-
  Expert DevOps pour CI/CD, containers, Kubernetes et Infrastructure as Code. Utilise ce skill quand: (1) mise en place de pipelines CI/CD, (2) containerisation avec Docker/K8s, (3) infrastructure as code (Terraform, Pulumi), (4) monitoring et alerting, (5) optimisation des déploiements, (6) sécurisation de l'infrastructure.
metadata:
  version: 1.0.0
  status: active
---

# DevOps Expert Skill

## Quick Start

```bash
# 1. Navigation rapide vers un agent
devops/agents/cicd/github-actions        # Configurer GitHub Actions
devops/agents/containers/docker          # Dockerfile et optimisation
devops/agents/kubernetes/deployments     # Manifestes K8s
devops/agents/infrastructure/terraform   # Infrastructure as Code
devops/agents/monitoring/prometheus      # Métriques et alertes

# 2. Exécuter les tests de validation
cd .web-agency/skills/devops && npm test

# 3. Questions fréquentes
"Configurer une pipeline CI/CD ?"        → cicd/github-actions
"Optimiser mon Dockerfile ?"             → containers/docker
"Déployer sur Kubernetes ?"              → kubernetes/deployments
"Créer mon infra avec Terraform ?"       → infrastructure/terraform
"Configurer Prometheus/Grafana ?"        → monitoring/prometheus
```

## Position dans l'Architecture

Ce skill est au **NIVEAU 3 : IMPLÉMENTATION**. Il implémente les décisions de `direction-technique` et les process de `web-dev-process`.

```
┌─────────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : STRATÉGIE (direction-technique/infrastructure)          │
│  → POURQUOI : Quelle stratégie CI/CD ? Quel cloud provider ?        │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : OPÉRATIONS                                              │
│  ┌────────────────────────────┐  ┌────────────────────────────┐    │
│  │     web-dev-process        │  │       lead-dev             │    │
│  │  setup/ + deployment/      │  │       delivery/            │    │
│  │  QUOI : Process CI/CD      │  │  QUI : Coordination        │    │
│  └────────────────────────────┘  └────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : IMPLÉMENTATION                                          │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    devops ← CE SKILL                        │    │
│  │  COMMENT : Pipelines, containers, K8s, IaC, monitoring      │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Philosophie

> Automatiser, fiabiliser, observer.

Le DevOps est le **pont entre développement et opérations**. Il :
- ✅ Automatise les pipelines de build, test, deploy
- ✅ Conteneurise les applications
- ✅ Orchestre les déploiements (Kubernetes)
- ✅ Provisionne l'infrastructure (IaC)
- ✅ Observe et alerte (monitoring)

Il ne fait PAS :
- ❌ Les décisions stratégiques d'infrastructure → `direction-technique`
- ❌ La définition des process CI/CD → `web-dev-process`
- ❌ La coordination des releases → `lead-dev`
- ❌ L'implémentation applicative → `backend-developer`, `frontend-developer`

## Domaines et Agents (30 agents)

### 1. cicd/ - Pipelines CI/CD (6 agents)

Automatisation des builds, tests et déploiements.

| Agent | Responsabilité | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination CI/CD | - |
| `github-actions` | Pipelines GitHub | GitHub Actions, workflows |
| `gitlab-ci` | Pipelines GitLab | GitLab CI, .gitlab-ci.yml |
| `pipelines` | Patterns de pipelines | Stages, jobs, cache |
| `quality-gates` | Validation qualité | SonarQube, coverage |
| `artifacts` | Gestion des artefacts | npm, Docker, releases |

### 2. containers/ - Conteneurisation (5 agents)

Docker et gestion des images.

| Agent | Responsabilité | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination containers | - |
| `docker` | Dockerfile et build | Multi-stage, optimisation |
| `docker-compose` | Orchestration locale | docker-compose.yml |
| `registries` | Registres d'images | Docker Hub, ECR, GCR |
| `security` | Sécurité des images | Trivy, Snyk, best practices |

### 3. kubernetes/ - Orchestration K8s (6 agents)

Déploiement et gestion Kubernetes.

| Agent | Responsabilité | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination K8s | - |
| `deployments` | Déploiements | Deployment, ReplicaSet |
| `services` | Exposition | Service, Ingress |
| `helm` | Charts Helm | values.yaml, templates |
| `scaling` | Auto-scaling | HPA, VPA, Keda |
| `config` | Configuration | ConfigMaps, Secrets |

### 4. infrastructure/ - Infrastructure as Code (5 agents)

Provisionnement d'infrastructure.

| Agent | Responsabilité | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination IaC | - |
| `terraform` | Terraform | HCL, modules, state |
| `aws` | Amazon Web Services | EC2, RDS, S3, EKS |
| `gcp` | Google Cloud Platform | GCE, GKE, Cloud SQL |
| `networking` | Réseau | VPC, subnets, security groups |

### 5. monitoring/ - Observabilité (5 agents)

Métriques, logs et alertes.

| Agent | Responsabilité | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination monitoring | - |
| `prometheus` | Métriques | Prometheus, exporters |
| `grafana` | Dashboards | Grafana, panels |
| `logging` | Logs centralisés | ELK, Loki, Fluentd |
| `alerting` | Alertes | Alertmanager, PagerDuty |

### 6. deployment/ - Stratégies de déploiement (3 agents)

Patterns de déploiement avancés.

| Agent | Responsabilité | Technologies |
|-------|----------------|--------------|
| `orchestrator` | Coordination déploiement | - |
| `strategies` | Stratégies (Blue-Green, Canary) | ArgoCD, Flux |
| `rollback` | Rollback et recovery | Procédures, automation |

**Total : 30 agents spécialisés**

## Règles de Routage

### Par Type de Question

| Question | Domaine |
|----------|---------|
| Pipeline CI/CD, GitHub Actions, GitLab CI | `cicd/` |
| Docker, Dockerfile, images | `containers/` |
| Kubernetes, Helm, pods, services | `kubernetes/` |
| Terraform, AWS, GCP, cloud | `infrastructure/` |
| Prometheus, Grafana, logs, alertes | `monitoring/` |
| Blue-Green, Canary, rollback | `deployment/` |

### Par Mots-Clés

| Mots-clés | Domaine/Agent |
|-----------|---------------|
| GitHub Actions, workflow, .github | `cicd/github-actions` |
| GitLab CI, .gitlab-ci.yml | `cicd/gitlab-ci` |
| Dockerfile, docker build, image | `containers/docker` |
| docker-compose, services locaux | `containers/docker-compose` |
| kubectl, deployment, pod, replica | `kubernetes/deployments` |
| helm, chart, values.yaml | `kubernetes/helm` |
| terraform, tf, HCL, plan, apply | `infrastructure/terraform` |
| EC2, RDS, S3, Lambda, EKS | `infrastructure/aws` |
| prometheus, metrics, scrape | `monitoring/prometheus` |
| grafana, dashboard, panels | `monitoring/grafana` |
| logs, ELK, Loki, Fluentd | `monitoring/logging` |
| blue-green, canary, feature flag | `deployment/strategies` |

## Arbre de Décision

```
Requête DevOps
│
├─ Concerne les pipelines CI/CD ?
│  ├─ GitHub Actions → cicd/github-actions
│  ├─ GitLab CI → cicd/gitlab-ci
│  ├─ Qualité/coverage → cicd/quality-gates
│  └─ Patterns généraux → cicd/pipelines
│
├─ Concerne les containers ?
│  ├─ Dockerfile → containers/docker
│  ├─ Compose → containers/docker-compose
│  ├─ Registry → containers/registries
│  └─ Sécurité images → containers/security
│
├─ Concerne Kubernetes ?
│  ├─ Déploiements → kubernetes/deployments
│  ├─ Services/Ingress → kubernetes/services
│  ├─ Helm → kubernetes/helm
│  ├─ Scaling → kubernetes/scaling
│  └─ ConfigMaps/Secrets → kubernetes/config
│
├─ Concerne l'infrastructure ?
│  ├─ Terraform → infrastructure/terraform
│  ├─ AWS → infrastructure/aws
│  ├─ GCP → infrastructure/gcp
│  └─ Réseau → infrastructure/networking
│
├─ Concerne le monitoring ?
│  ├─ Métriques → monitoring/prometheus
│  ├─ Dashboards → monitoring/grafana
│  ├─ Logs → monitoring/logging
│  └─ Alertes → monitoring/alerting
│
├─ Concerne les stratégies de déploiement ?
│  ├─ Blue-Green, Canary → deployment/strategies
│  └─ Rollback → deployment/rollback
│
├─ Décision stratégique ?
│  └─ → skill direction-technique/infrastructure
│
└─ Process CI/CD ?
   └─ → skill web-dev-process/setup
```

## Interaction avec les Autres Skills

### Flux Entrants

```
direction-technique/infrastructure ──► devops (stratégie → implémentation)
web-dev-process/setup/cicd ──► devops (process → implémentation)
lead-dev/delivery ──► devops (coordination → exécution)
```

### Flux Sortants

```
devops ──► backend-developer (déploiement → app backend)
devops ──► frontend-developer (déploiement → app frontend)
devops ──► nextjs-expert (complément Next.js spécifique)
```

## Points d'Escalade

### Vers direction-technique

| Situation | Raison |
|-----------|--------|
| Choix de cloud provider | Décision stratégique |
| Architecture infrastructure | Impact long terme |
| Budget infrastructure | Validation financière |
| Sécurité réseau globale | Politique sécurité |

### Vers lead-dev

| Situation | Raison |
|-----------|--------|
| Planification release | Coordination équipe |
| Hotfix urgent | Décision go/no-go |
| Rollback production | Validation métier |

### Vers l'humain

| Situation | Raison |
|-----------|--------|
| Accès credentials production | Sensibilité sécurité |
| Incident P1/P2 | Responsabilité |
| Coûts cloud imprévus | Validation budget |
| Changement architecture majeur | Impact business |

## Security Best Practices

Le DevOps gère des opérations sensibles (secrets, déploiements, infrastructure). Appliquer ces principes de sécurité :

### 1. Gestion des Secrets

| Pratique | Description |
|----------|-------------|
| **Ne jamais committer de secrets** | Pas de `.env`, credentials, API keys dans git |
| **Variables d'environnement** | Utiliser les secrets managers (GitHub Secrets, GitLab CI/CD Variables) |
| **Secrets par environnement** | Séparer dev, staging, production |
| **Rotation régulière** | Changer les credentials périodiquement |

```yaml
# ✅ Bon : référence à un secret
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}

# ❌ Mauvais : secret en clair
env:
  DATABASE_URL: "postgresql://user:password@host:5432/db"
```

### 2. Scanning et Validation

| Outil | Usage | Intégration |
|-------|-------|-------------|
| **Secret scanning** | Détection de secrets dans le code | GitHub Advanced Security, GitLeaks |
| **SAST** | Analyse statique sécurité | SonarQube, Snyk Code |
| **DAST** | Tests dynamiques | OWASP ZAP |
| **Container scanning** | Vulnérabilités images | Trivy, Snyk Container |
| **Dependency scanning** | Vulnérabilités deps | Dependabot, npm audit |

```yaml
# Pipeline avec security gates
jobs:
  security:
    steps:
      - name: Secret Scan
        uses: trufflesecurity/trufflehog@main
      - name: SAST
        uses: SonarSource/sonarcloud-github-action@master
      - name: Container Scan
        run: trivy image ${{ env.IMAGE }}
```

### 3. Infrastructure Security

| Domaine | Bonnes Pratiques |
|---------|------------------|
| **Réseau** | VPC privés, security groups restrictifs, pas de 0.0.0.0/0 |
| **IAM** | Principe du moindre privilège, pas de credentials root |
| **Encryption** | At-rest et in-transit, KMS pour les clés |
| **Logging** | CloudTrail/Audit logs activés, centralisation |

### 4. Container Security

Voir l'agent `containers/security` pour les détails complets :

- Images de base minimales (alpine, distroless)
- Utilisateur non-root dans les containers
- Scan des vulnérabilités avant push
- Pas de secrets dans les images
- Healthchecks configurés

### 5. Pipeline Security

| Risque | Mitigation |
|--------|------------|
| Injection dans workflows | Éviter `${{ github.event.*.body }}` non échappé |
| Permissions excessives | `permissions: read-all` par défaut |
| Actions tierces | Pin par SHA, pas par tag |
| Artifacts sensibles | Ne pas exposer de logs avec secrets |

```yaml
# Sécurité pipeline GitHub Actions
permissions:
  contents: read
  pull-requests: write  # Seulement si nécessaire

jobs:
  build:
    steps:
      # ✅ Pin par SHA
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
      # ❌ Pin par tag (peut changer)
      - uses: actions/checkout@v4
```

### 6. Checklist Sécurité

```markdown
## Pre-Deployment Security Checklist

### Secrets
- [ ] Aucun secret dans le code source
- [ ] Variables d'environnement configurées
- [ ] Secret scanning activé

### Scanning
- [ ] SAST passé (0 critical)
- [ ] Container scan passé
- [ ] Dependency audit passé

### Infrastructure
- [ ] Security groups restrictifs
- [ ] IAM least privilege
- [ ] Encryption activée

### Pipeline
- [ ] Permissions minimales
- [ ] Actions pinnées par SHA
- [ ] Logs sanitisés
```

### Références

- Agent détaillé : `containers/security`
- OWASP DevSecOps Guidelines
- CIS Benchmarks (Docker, Kubernetes)

## Skills Associés

| Skill | Niveau | Relation |
|-------|--------|----------|
| `direction-technique` | STRATÉGIE | Reçoit les directives infra |
| `web-dev-process` | OPÉRATIONS | Suit les process CI/CD |
| `lead-dev` | OPÉRATIONS | Coordonne les releases |
| `backend-developer` | IMPLÉMENTATION | Déploie les apps backend |
| `frontend-developer` | IMPLÉMENTATION | Déploie les apps frontend |
| `nextjs-expert` | IMPLÉMENTATION | Complément Vercel/Next.js |

## Changelog

### v1.0.0
- Création initiale avec 6 domaines et 30 agents
- Extraction depuis backend-developer/devops
- Position : NIVEAU 3 IMPLÉMENTATION
- Couverture : CI/CD, containers, K8s, IaC, monitoring, deployment
