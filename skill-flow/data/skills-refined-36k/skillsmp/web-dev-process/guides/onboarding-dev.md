# Guide d'Onboarding Développeur

Bienvenue dans l'équipe ! Ce guide vous accompagne dans votre prise en main du projet et de nos pratiques de développement.

## Table des Matières

1. [Premier Jour](#premier-jour)
2. [Configuration de l'Environnement](#configuration-de-lenvironnement)
3. [Architecture du Projet](#architecture-du-projet)
4. [Workflow de Développement](#workflow-de-développement)
5. [Ressources](#ressources)
6. [Checklist d'Intégration](#checklist-dintégration)

---

## Premier Jour

### Accès à Obtenir

- [ ] Accès au repository Git (GitHub/GitLab)
- [ ] Accès à l'outil de gestion de projet (Jira/Linear/GitHub Projects)
- [ ] Accès aux environnements (staging, production si applicable)
- [ ] Accès aux outils de communication (Slack/Teams)
- [ ] Accès aux outils de documentation (Notion/Confluence)
- [ ] Accès aux secrets/credentials nécessaires (vault, .env)

### Personnes à Rencontrer

| Rôle | Nom | Sujet de Discussion |
|------|-----|---------------------|
| Tech Lead | ___ | Architecture, standards |
| Product Owner | ___ | Vision produit, priorités |
| Buddy/Mentor | ___ | Questions quotidiennes |
| DevOps | ___ | Déploiement, infrastructure |

---

## Configuration de l'Environnement

### Prérequis

```bash
# Versions requises (à adapter selon le projet)
node --version  # v20+
pnpm --version  # v8+
git --version   # v2.40+
```

### Installation

```bash
# 1. Cloner le repository
git clone <repo-url>
cd <project-name>

# 2. Installer les dépendances
pnpm install

# 3. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos credentials

# 4. Configurer les hooks Git
pnpm prepare

# 5. Vérifier l'installation
pnpm dev        # Démarrer en mode développement
pnpm test       # Lancer les tests
pnpm lint       # Vérifier le code
```

### Configuration IDE Recommandée

#### VS Code

Extensions obligatoires :
- ESLint
- Prettier - Code formatter
- EditorConfig for VS Code
- GitLens

Extensions recommandées :
- Error Lens
- Auto Import
- Better Comments

Settings recommandés (`.vscode/settings.json`) :
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  }
}
```

---

## Architecture du Projet

### Structure des Dossiers

```
project/
├── src/                    # Code source
│   ├── components/         # Composants réutilisables
│   ├── features/           # Modules fonctionnels
│   ├── lib/                # Utilitaires et helpers
│   ├── services/           # Appels API et services
│   └── types/              # Types TypeScript
├── tests/                  # Tests
│   ├── unit/               # Tests unitaires
│   ├── integration/        # Tests d'intégration
│   └── e2e/                # Tests end-to-end
├── docs/                   # Documentation
│   ├── adr/                # Architecture Decision Records
│   └── api/                # Documentation API
├── scripts/                # Scripts utilitaires
└── config/                 # Configurations
```

### Technologies Clés

| Catégorie | Technologie | Documentation |
|-----------|-------------|---------------|
| Frontend | ___ | ___ |
| Backend | ___ | ___ |
| Base de données | ___ | ___ |
| Tests | ___ | ___ |
| CI/CD | ___ | ___ |

### Concepts Importants

Prenez le temps de comprendre :

1. **Architecture globale** : Consultez les ADRs dans `docs/adr/`
2. **Patterns utilisés** : ___
3. **Conventions de nommage** : Voir [code-conventions.md](./code-conventions.md)
4. **Flux de données** : ___

---

## Workflow de Développement

### Cycle de Développement

```
Issue → Branch → Code → Tests → PR → Review → Merge → Deploy
```

### Conventions de Branches

```bash
# Format : type/description-courte
feat/user-authentication
fix/login-validation-bug
docs/api-documentation
refactor/payment-service
```

### Conventions de Commits

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/) :

```bash
# Format : type(scope): description
feat(auth): add password reset functionality
fix(cart): resolve quantity update bug
docs(api): update authentication examples
```

### Process de Code Review

1. **Créer une PR** avec le template fourni
2. **Auto-review** : Relisez votre code avant de demander une review
3. **Assigner des reviewers** : Au moins 1 reviewer requis
4. **Répondre aux commentaires** : Discutez et corrigez
5. **Merge** : Après approbation et CI verte

### Definition of Done

Voir [definition-of-done.md](./definition-of-done.md) pour les critères.

---

## Ressources

### Documentation

- [ ] README du projet
- [ ] Documentation technique (`/docs`)
- [ ] ADRs (Architecture Decision Records)
- [ ] API documentation
- [ ] Wiki de l'équipe

### Lectures Recommandées

Pour se familiariser avec nos pratiques :

- [ ] CONTRIBUTING.md
- [ ] Guides de ce dossier
- [ ] ADRs existants
- [ ] Historique des PRs récentes

### Contacts Utiles

| Question | Contact |
|----------|---------|
| Architecture | Tech Lead |
| Produit | Product Owner |
| DevOps/Infra | DevOps |
| Process/Méthodologie | Scrum Master |

---

## Checklist d'Intégration

### Semaine 1

- [ ] Environnement de dev fonctionnel
- [ ] Accès à tous les outils
- [ ] Lecture de la documentation principale
- [ ] Premier commit (fix mineur ou amélioration doc)
- [ ] Participation au daily standup
- [ ] Rencontre avec les membres clés

### Semaine 2

- [ ] Première feature ou bugfix complète
- [ ] Première code review effectuée
- [ ] Compréhension de l'architecture globale
- [ ] Familiarisation avec le backlog

### Premier Mois

- [ ] Autonomie sur les tâches standard
- [ ] Contribution aux discussions techniques
- [ ] Proposition d'améliorations
- [ ] Feedback sur l'onboarding (pour améliorer ce guide)

---

## Questions Fréquentes

### Comment démarrer sur une nouvelle feature ?

1. Lire et comprendre l'issue/ticket
2. Poser des questions si besoin
3. Créer une branche depuis `main`
4. Développer avec des commits atomiques
5. Créer une PR dès que possible (même en draft)

### Que faire si je suis bloqué ?

1. Chercher dans la documentation
2. Chercher dans les issues/PRs existantes
3. Demander à votre buddy
4. Poster dans le channel d'équipe
5. Escalader au Tech Lead si nécessaire

### Comment signaler un bug ?

Utiliser le template de bug report dans GitHub Issues avec :
- Steps to reproduce
- Comportement attendu vs actuel
- Screenshots si applicable
- Environnement (browser, OS, version)

---

**Bienvenue dans l'équipe ! N'hésitez pas à poser des questions - il n'y a pas de question stupide.**
