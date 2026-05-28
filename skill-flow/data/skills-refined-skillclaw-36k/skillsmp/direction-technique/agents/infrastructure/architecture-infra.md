---
name: architecture-infra
description: Politique d'architecture infrastructure cloud (Niveau POURQUOI)
workflows:
  - id: wf-creation
  phase: Conception
---

# Politique d'Architecture Infrastructure

Tu définis les **politiques et standards** pour l'architecture d'infrastructure cloud.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les STANDARDS d'architecture infra et les critères de choix
> **Ce que tu ne fais pas** : Écrire le code Terraform/Pulumi ou configurer les services cloud
>
> → Process de setup infra : `web-dev-process/agents/setup/infrastructure`
> → Implémentation : Skills technologiques spécialisés

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi ces choix ? Pour fiabilité, scalabilité, coût"     │
│  → "Standards : patterns, composants, bonnes pratiques"         │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi déployer ? VPC, ECS, RDS, CDN"                         │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (skills technologiques)                     │
│  → "Code : Terraform HCL, Pulumi TypeScript, CloudFormation"    │
└─────────────────────────────────────────────────────────────────┘
```

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quels sont les environnements actuels et leur configuration ?
- Existe-t-il des contraintes cloud spécifiques ? (Multi-cloud, vendor lock-in)
- Quel est le budget infrastructure disponible ?
- Y a-t-il des systèmes legacy à intégrer ?

### Objectifs
- Quels sont les SLA requis pour chaque environnement ?
- Quelle est la scalabilité cible ? (Utilisateurs, charge)
- Quels sont les objectifs de disponibilité ? (Uptime, RTO, RPO)
- Y a-t-il des exigences de conformité ? (ISO, SOC2, HDS)

### Risques
- Quels sont les points de défaillance critiques identifiés ?
- Y a-t-il des contraintes de migration depuis l'existant ?
- Quel est le niveau de maturité de l'équipe sur l'IaC ?
- Y a-t-il des dépendances externes critiques ?

---

## Politique Infrastructure as Code (IaC)

### Outils Recommandés

| Outil | Cas d'Usage | Complexité |
|-------|-------------|------------|
| **Terraform** | Multi-cloud, équipes matures | Moyenne |
| **Pulumi** | Développeurs TypeScript/Python | Moyenne |
| **CloudFormation** | AWS-only, équipes AWS | Faible |
| **CDK** | AWS + TypeScript | Moyenne |

### Principes IaC Obligatoires

| Principe | Description |
|----------|-------------|
| **Tout en code** | Aucune configuration manuelle en prod |
| **Versionné** | Git avec historique complet |
| **Reviewé** | PR obligatoire pour changements |
| **Testé** | Validation en staging avant prod |
| **Immutable** | Pas de modifications in-place |

## Patterns d'Architecture

### Three-Tier Architecture

```
                    Internet
                        │
                        ▼
               ┌────────────────┐
               │   CloudFront   │  CDN / WAF
               └────────┬───────┘
                        │
               ┌────────▼───────┐
               │    ALB/NLB     │  Load Balancer
               └────────┬───────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐
   │  App 1  │    │  App 2  │    │  App 3  │  Application
   └────┬────┘    └────┬────┘    └────┬────┘
        │              │              │
        └──────────────┼──────────────┘
                       ▼
               ┌───────────────┐
               │    RDS/Cache  │  Data
               └───────────────┘
```

### Serverless Architecture

```
       API Gateway
            │
            ▼
    ┌───────────────┐
    │    Lambda     │───► DynamoDB
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │     SQS       │───► Lambda Worker
    └───────────────┘
```

### Critères de Choix d'Architecture

| Architecture | Taille Équipe | Complexité | Scalabilité |
|--------------|---------------|------------|-------------|
| **Three-Tier** | 1-10 devs | Faible | Verticale |
| **Serverless** | 1-5 devs | Moyenne | Automatique |
| **Microservices** | 10+ devs | Élevée | Horizontale |
| **Monolithe modulaire** | 5-15 devs | Moyenne | Verticale |

## Composants par Provider

### AWS

| Besoin | Service | Alternative |
|--------|---------|-------------|
| Compute | ECS Fargate | EC2, Lambda |
| Database | RDS PostgreSQL | Aurora, DynamoDB |
| Cache | ElastiCache Redis | DAX |
| Storage | S3 | EFS |
| CDN | CloudFront | - |
| DNS | Route 53 | - |
| Secrets | Secrets Manager | Parameter Store |
| Queue | SQS | EventBridge |

### GCP

| Besoin | Service |
|--------|---------|
| Compute | Cloud Run |
| Database | Cloud SQL |
| Cache | Memorystore |
| Storage | Cloud Storage |
| CDN | Cloud CDN |
| DNS | Cloud DNS |

## Bonnes Pratiques

### Sécurité

- [ ] VPC avec subnets privés
- [ ] Security Groups restrictifs
- [ ] Chiffrement at rest et in transit
- [ ] IAM roles (pas de credentials)
- [ ] Secrets Manager pour les secrets

### Haute Disponibilité

- [ ] Multi-AZ (au minimum)
- [ ] Auto-scaling configuré
- [ ] Health checks
- [ ] Backup automatisés
- [ ] DR plan documenté

### Coût

- [ ] Right-sizing des instances
- [ ] Spot/Preemptible pour workloads tolerants
- [ ] Reserved instances pour stable
- [ ] Monitoring des coûts (AWS Cost Explorer)
- [ ] Tags pour allocation

---

## Checklist Infrastructure

### Setup Initial

- [ ] IaC outil choisi et configuré
- [ ] Environnements définis (dev, staging, prod)
- [ ] VPC et réseau configurés
- [ ] Sécurité : IAM, Security Groups
- [ ] Monitoring et alerting
- [ ] Backup et DR

### Par Déploiement

- [ ] Review IaC avant apply
- [ ] Plan vérifié
- [ ] Rollback plan prêt
- [ ] Tests post-déploiement

---

## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| Besoin multi-region | Architecture + coûts à valider | Tech Lead + CTO |
| Compliance spécifique | Consultation sécurité/légal | Security + Legal |
| Migration cloud | Plan détaillé + POC | DevOps + Tech Lead |
| Coût > budget | Optimisation ou arbitrage | Tech Lead + Finance |
| Incident infra | War room, communication | On-call + Management |

---

## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Process setup infra | `web-dev-process/agents/setup/infrastructure` |
| Environnements | `infrastructure/environnements` |
| Déploiement | `infrastructure/strategie-deploiement` |
| Sécurité | `securite/securite-applicative` |
| Implémentation | Skills technologiques spécialisés |

### Ressources Externes

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [The Twelve-Factor App](https://12factor.net/)

## Livrables

| Livrable | Description |
|----------|-------------|
| Diagramme d'architecture infrastructure | Schémas des composants cloud/serveurs avec flux réseau et dépendances |
| Document de stratégie infrastructure | Choix de providers, régions, services et justifications |
| Plan de haute disponibilité | Stratégie de résilience, backup, disaster recovery et RTO/RPO |
