---
name: gestion-secrets
description: Politique de gestion sécurisée des secrets et credentials (Niveau POURQUOI)
workflows:
  - id: wf-creation
    phase: Production
---

# Politique de Gestion des Secrets

Tu définis les **politiques et objectifs** de gestion sécurisée des secrets.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les RÈGLES de gestion des secrets et les standards
> **Ce que tu ne fais pas** : Implémenter les solutions de gestion de secrets (code)
>
> → Process de sécurité : `web-dev-process/agents/setup/secrets-management`
> → Implémentation : Skills technologiques spécialisés

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi ces règles ? Pour protéger les accès"              │
│  → "Politiques : rotation, stockage, accès"                     │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi mettre en place ? Vault, env vars, CI/CD secrets"      │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (skills technologiques)                     │
│  → "Code : AWS Secrets Manager, Vault API, Zod validation..."   │
└─────────────────────────────────────────────────────────────────┘
```

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quels types de données sensibles sont manipulées ?
- Existe-t-il une politique de sécurité existante ?
- Y a-t-il eu des incidents de sécurité précédents ?
- Quels sont les audits de sécurité déjà réalisés ?

### Objectifs
- Quelles sont les exigences de conformité ? (RGPD, ISO 27001, SOC2)
- Quelle est la surface d'attaque actuelle ?
- Quels sont les systèmes critiques à protéger en priorité ?
- Y a-t-il des contraintes réglementaires spécifiques ?

### Risques
- Quels sont les vecteurs d'attaque identifiés ?
- Y a-t-il des dépendances vulnérables connues ?
- Quel est le niveau de maturité sécurité de l'équipe ?
- Y a-t-il des données personnelles stockées ?

---

## Principes Fondamentaux

### Règles Absolues

| Règle | Impact si Violée |
|-------|------------------|
| **Jamais de secrets dans le code source** | Fuite si repo exposé |
| **Jamais de secrets commités** | Historique Git permanent |
| **Jamais de secrets dans les logs** | Exposition via logs |
| **Jamais de secrets dans les URLs** | Exposition dans historique navigateur, logs serveur |
| **Jamais de secrets en clair en prod** | Accès non autorisé |

### Classification des Secrets

| Type | Exemples | Criticité |
|------|----------|-----------|
| **Credentials de production** | DB prod, API keys live | Critique |
| **Clés de chiffrement** | JWT secret, encryption keys | Critique |
| **Credentials d'infrastructure** | AWS, GCP, Azure credentials | Haute |
| **Tokens d'intégration** | Stripe, Twilio, SendGrid | Haute |
| **Credentials de dev/test** | DB locale, API keys test | Moyenne |
| **Credentials de CI/CD** | Deploy tokens, registry | Haute |

---

## Politique de Stockage

### Méthodes Autorisées

| Méthode | Usage | Sécurité |
|---------|-------|----------|
| **Secret Manager Cloud** | Production | ★★★★★ |
| **HashiCorp Vault** | Multi-cloud, on-premise | ★★★★★ |
| **Variables CI/CD** | Déploiement | ★★★★☆ |
| **Variables d'environnement** | Runtime | ★★★☆☆ |
| **Fichiers .env (ignorés)** | Développement local | ★★☆☆☆ |

### Méthodes Interdites

| Méthode | Raison |
|---------|--------|
| Code source (hardcoded) | Commité, visible |
| Fichiers .env commités | Historique permanent |
| Fichiers de config commités | Idem |
| Base de données en clair | Accessible si DB compromise |
| Variables d'env non chiffrées en prod | Visible dans process list |

### Structure de Fichiers

```
project/
├── .env.example        # Template SANS secrets (commité)
├── .env.development    # Secrets locaux (ignoré)
├── .env.test           # Secrets de test (ignoré)
├── .env.production     # N'existe PAS - utiliser secret manager
└── .gitignore          # DOIT contenir .env*
```

---

## Politique de Rotation

### Fréquences Obligatoires

| Type de Secret | Fréquence | Justification |
|----------------|-----------|---------------|
| **Mots de passe DB production** | 90 jours | Limiter l'exposition |
| **API Keys production** | 180 jours | Limiter l'exposition |
| **JWT Secrets** | 30 jours | Sessions courtes |
| **Service Accounts** | 365 jours | Rotation annuelle |
| **Après incident** | Immédiat | Compromission possible |
| **Après départ employé** | Immédiat | Révocation d'accès |

### Procédure de Rotation

```
1. Générer nouveau secret
         │
         ▼
2. Configurer le nouveau (sans supprimer l'ancien)
         │
         ▼
3. Déployer avec les deux secrets valides
         │
         ▼
4. Migrer tous les services vers nouveau secret
         │
         ▼
5. Vérifier qu'aucun service n'utilise l'ancien
         │
         ▼
6. Invalider l'ancien secret
         │
         ▼
7. Supprimer l'ancien du secret manager
```

---

## Politique d'Accès

### Principe du Moindre Privilège

| Environnement | Qui a Accès | Type d'Accès |
|---------------|-------------|--------------|
| **Production** | DevOps/SRE séniors uniquement | Lecture via secret manager |
| **Staging** | Développeurs + DevOps | Lecture via CI/CD |
| **Développement** | Développeurs | Fichiers locaux personnels |
| **CI/CD** | Pipelines automatisés | Variables d'environnement |

### Audit d'Accès

| Événement | Logging Requis |
|-----------|----------------|
| Lecture d'un secret | Oui, avec identité |
| Création d'un secret | Oui, avec identité |
| Modification d'un secret | Oui, avec identité |
| Suppression d'un secret | Oui, avec identité |
| Accès refusé | Oui, avec alerte |

---

## Politique de Détection

### Outils Obligatoires

| Niveau | Outil | Objectif |
|--------|-------|----------|
| **Pre-commit** | gitleaks, detect-secrets | Bloquer avant commit |
| **CI** | gitleaks en pipeline | Bloquer avant merge |
| **Repo** | GitHub Secret Scanning | Alertes temps réel |
| **Audit** | Scans réguliers | Détecter l'historique |

### Réponse à une Exposition

| Étape | Action | Délai |
|-------|--------|-------|
| 1 | Révoquer le secret exposé | Immédiat |
| 2 | Générer un nouveau secret | < 15 min |
| 3 | Déployer le nouveau secret | < 1h |
| 4 | Nettoyer l'historique Git (si possible) | < 24h |
| 5 | Auditer les accès potentiels | < 48h |
| 6 | Documenter l'incident | < 1 semaine |

---

## Politique par Environnement

### Développement Local

| Règle | Détail |
|-------|--------|
| Fichier `.env.example` | Template commité, sans vraies valeurs |
| Fichier `.env` | Ignoré par Git, secrets personnels |
| Secrets de dev | Différents de staging/prod |
| Accès limité | Chaque dev a ses propres credentials |

### CI/CD

| Règle | Détail |
|-------|--------|
| Secrets dans variables CI | Pas dans le code |
| Masquage dans logs | Activé par défaut |
| Accès restreint | Seuls les admins configurent |
| Rotation | Après changement d'équipe |

### Production

| Règle | Détail |
|-------|--------|
| Secret Manager obligatoire | AWS Secrets Manager, Vault, etc. |
| Rotation automatique | Configurée pour secrets critiques |
| Audit d'accès | Logs centralisés |
| Chiffrement | At-rest et in-transit |

---

## Checklist Secrets

### Setup Projet

- [ ] `.env.example` créé et commité (sans secrets)
- [ ] `.env*` dans `.gitignore`
- [ ] Validation des variables au démarrage
- [ ] Secret manager configuré pour prod
- [ ] gitleaks/detect-secrets en pre-commit

### Déploiement

- [ ] Secrets injectés par CI/CD ou secret manager
- [ ] Pas de secrets en dur dans le code
- [ ] Pas de secrets dans les logs
- [ ] Rotation configurée si applicable
- [ ] Accès audités

### Incident

- [ ] Secret exposé identifié
- [ ] Révocation immédiate effectuée
- [ ] Nouveau secret généré et déployé
- [ ] Historique Git nettoyé (si applicable)
- [ ] Audit des accès réalisé
- [ ] Incident documenté

---

## Points d'Escalade

| Situation | Action | Délai | Responsable |
|-----------|--------|-------|-------------|
| Secret commité | Révoquer, nettoyer, nouveau secret | Immédiat | Dev + DevOps |
| Secret de prod exposé | War room, rotation, audit | < 1h | CTO + DevOps |
| Accès suspect détecté | Investigation + rotation | < 2h | Security + DevOps |
| Doute sur exposition | Rotation préventive | < 24h | DevOps |

---

## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Process de setup secrets | `web-dev-process/agents/setup/secrets-management` |
| Variables d'environnement | `web-dev-process/agents/setup/env-variables` |
| Sécurité applicative | `securite/securite-applicative` |
| Implémentation | Skills technologiques spécialisés |

### Ressources Externes

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)

## Livrables

| Livrable | Description |
|----------|-------------|
| Stratégie de gestion des secrets | Document définissant la solution choisie (Vault, Secrets Manager, etc.) |
| Inventaire des secrets | Liste exhaustive des credentials, clés API et certificats avec rotation |
| Procédures de rotation | Guide de renouvellement périodique des secrets avec fréquence et alertes |
