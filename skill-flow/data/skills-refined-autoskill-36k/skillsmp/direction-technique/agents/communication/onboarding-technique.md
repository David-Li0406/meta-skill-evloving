---
name: onboarding-technique
description: Intégration des nouveaux développeurs dans l'équipe
workflows:
  - id: wf-creation
  phase: Production
---

# Onboarding Technique

Tu guides l'**intégration des nouveaux développeurs** pour qu'ils deviennent productifs rapidement.

## Tu NE fais PAS

- ❌ Développer à la place du nouveau → `frontend-developer`, `backend-developer`
- ❌ Gérer les aspects RH (contrat, matériel) → RH, IT
- ❌ Faire les code reviews quotidiennes → `lead-dev/code-review`
- ❌ Assigner les tâches et gérer les sprints → `lead-dev`, `project-management/pilotage`

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quelles sont les audiences cibles ? (Devs internes, externes, product)
- Existe-t-il une documentation existante ?
- Quels sont les formats de documentation préférés ?
- Quels outils de documentation sont déjà en place ?

### Objectifs
- Quelle est la fréquence de mise à jour souhaitée ?
- Quels sont les types de communication requis ? (Technique, fonctionnelle)
- Y a-t-il des standards de documentation à respecter ?
- Quel niveau de détail est attendu ?

### Risques
- Y a-t-il un risque de documentation obsolète ?
- Quel est le temps disponible pour documenter ?
- Y a-t-il des contraintes de confidentialité ?
- Qui maintient la documentation à long terme ?

## Programme d'Onboarding

### Timeline

```
Jour 1-2: Setup & Découverte
    │
    ▼
Jour 3-5: Codebase & Première Contribution
    │
    ▼
Semaine 2: Premières Features
    │
    ▼
Semaine 3-4: Autonomie Progressive
    │
    ▼
Mois 2+: Productivité Normale
```

## Jour 1-2: Setup & Découverte

### Checklist Administrative

- [ ] Accès email et Slack/Teams
- [ ] Comptes créés (GitHub, Jira, Confluence, etc.)
- [ ] Invitations aux channels pertinents
- [ ] Accès aux environnements (VPN, AWS, etc.)
- [ ] Clés SSH générées et ajoutées
- [ ] 2FA configuré partout

### Checklist Technique

- [ ] Machine configurée (Mac/Linux/Windows)
- [ ] IDE installé et configuré (VSCode, extensions)
- [ ] Git configuré (nom, email, signing)
- [ ] Node.js/Python/etc. installé (version correcte)
- [ ] Docker installé et fonctionnel
- [ ] Repos clonés
- [ ] Environnement local qui tourne

### Guide Setup

## Note ADR-005

> **NIVEAU 1 - POURQUOI** : Cet agent définit la STRATÉGIE et les DÉCISIONS d'onboarding.
> Les exemples de configuration ci-dessous sont fournis à titre de RÉFÉRENCE.
> L'IMPLÉMENTATION concrète doit être déléguée au skill technique approprié :
> - Configuration environnement → `devops/` (pour setup infrastructure)
> - Documentation technique → `lead-dev/` (pour guides et conventions)
> - Code d'exemple → `frontend-developer` ou `backend-developer`

```markdown
# Setup Développeur

## 1. Outils de Base

\`\`\`bash
# macOS avec Homebrew
brew install git node@20 docker docker-compose

# Vérifier les versions
git --version    # >= 2.40
node --version   # >= 20.0
docker --version # >= 24.0
\`\`\`

## 2. Configuration Git

\`\`\`bash
git config --global user.name "Prénom Nom"
git config --global user.email "prenom.nom@company.com"
git config --global pull.rebase true
git config --global init.defaultBranch main
\`\`\`

## 3. Clés SSH

\`\`\`bash
ssh-keygen -t ed25519 -C "prenom.nom@company.com"
cat ~/.ssh/id_ed25519.pub
# Copier dans GitHub > Settings > SSH Keys
\`\`\`

## 4. Cloner les Repos

\`\`\`bash
mkdir -p ~/work/company
cd ~/work/company
git clone git@github.com:company/frontend.git
git clone git@github.com:company/backend.git
git clone git@github.com:company/infrastructure.git
\`\`\`

## 5. Lancer le Projet

\`\`\`bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
# Ouvrir http://localhost:3000
\`\`\`
```

## Jour 3-5: Codebase & Première Contribution

### Architecture Overview

```markdown
# Architecture du Projet

## Vision Globale

Notre application est un [type d'application] qui permet à [utilisateurs]
de [action principale]. Elle est composée de :

- **Frontend** : Next.js 14, React 18, TypeScript
- **Backend** : Node.js, Express, PostgreSQL
- **Infrastructure** : AWS (ECS, RDS, S3)

## Structure Frontend

\`\`\`
frontend/
├── src/
│   ├── app/           # Routes Next.js (App Router)
│   ├── components/    # Composants réutilisables
│   │   ├── ui/        # Composants UI génériques
│   │   └── features/  # Composants métier
│   ├── lib/           # Utilitaires et configuration
│   ├── hooks/         # Custom React hooks
│   └── services/      # Appels API
├── public/            # Assets statiques
└── tests/             # Tests
\`\`\`

## Flux de Données

\`\`\`
User Action
    │
    ▼
Component (useState/useReducer)
    │
    ▼
Service Layer (API call)
    │
    ▼
Backend API
    │
    ▼
Database
\`\`\`

## Conventions Clés

- Commits : format Conventional Commits
- Branches : feature/xxx, fix/xxx, chore/xxx
- PR : minimum 1 reviewer, tests requis
- Code style : ESLint + Prettier (auto-formaté)
```

### Première Tâche

```markdown
## Ta Première PR 🎉

### Objectif
Une tâche simple pour découvrir le workflow :
- Ajouter ton nom à la page "Équipe"
- Ou corriger une typo dans la documentation

### Étapes

1. **Créer une branche**
   \`\`\`bash
   git checkout main
   git pull origin main
   git checkout -b feature/add-my-name
   \`\`\`

2. **Faire la modification**
   - Ouvrir le fichier approprié
   - Faire le changement

3. **Committer**
   \`\`\`bash
   git add .
   git commit -m "feat: add [ton nom] to team page"
   \`\`\`

4. **Pousser et créer la PR**
   \`\`\`bash
   git push -u origin feature/add-my-name
   \`\`\`
   - Aller sur GitHub et créer la PR
   - Demander une review à ton buddy

5. **Merger après approbation**

### Ce que tu vas apprendre
- Le workflow Git de l'équipe
- Le process de code review
- Comment fonctionne la CI/CD
```

## Semaine 2: Premières Features

### Pair Programming

| Durée | Activité |
|-------|----------|
| 2h | Session avec un senior sur une feature |
| 1h | Débriefing et questions |
| 2h | Travail autonome (même pattern) |
| 30min | Review ensemble |

### Checklist Technique Avancée

- [ ] Comprend le data model principal
- [ ] Sait naviguer dans la codebase
- [ ] A écrit et fait passer des tests
- [ ] A déployé en staging
- [ ] Comprend le monitoring (logs, errors)
- [ ] Connaît les conventions de l'équipe

## Ressources d'Apprentissage

### Documentation Interne

| Document | Contenu |
|----------|---------|
| `README.md` | Setup et commandes |
| `ARCHITECTURE.md` | Vue d'ensemble technique |
| `CONTRIBUTING.md` | Workflow et conventions |
| `docs/` | Documentation détaillée |
| Wiki | ADRs et décisions |

### Sessions Recommandées

```markdown
## Semaine 1

- [ ] **Lundi** : Onboarding RH + Setup (9h-12h)
- [ ] **Lundi** : Rencontre équipe + Présentation projet (14h-16h)
- [ ] **Mardi** : Setup technique avec buddy (9h-12h)
- [ ] **Mardi** : Exploration codebase (14h-17h)
- [ ] **Mercredi** : Architecture overview avec Tech Lead (10h-11h30)
- [ ] **Mercredi** : Première PR simple (14h-17h)
- [ ] **Jeudi** : Process & outils avec PM (10h-11h)
- [ ] **Jeudi** : Pair programming (14h-17h)
- [ ] **Vendredi** : Questions & débrief semaine (16h-17h)

## Semaine 2

- [ ] **Lundi** : Première vraie tâche assignée
- [ ] **Mercredi** : Point mi-semaine avec buddy
- [ ] **Vendredi** : Review de la première feature
```

## Système de Buddy

### Rôle du Buddy

| Responsabilité | Fréquence |
|----------------|-----------|
| Point quotidien (15 min) | Jours 1-5 |
| Disponible pour questions | Permanent |
| Review des premières PRs | Semaines 1-2 |
| Pair programming | 2-3 sessions |
| Feedback constructif | Fin semaine 1 et 2 |

### Questions Fréquentes

```markdown
## FAQ Nouveau Développeur

### "Où trouver X ?"
- Code : chercher dans VSCode (Cmd+Shift+F)
- Documentation : Wiki / docs/
- Décisions : ADRs dans le repo

### "Comment faire X ?"
- Regarder si un pattern similaire existe
- Demander au buddy ou dans le channel tech
- Consulter la documentation

### "C'est normal que... ?"
- Oui, demande ! Aucune question n'est bête
- Préfère Slack public pour que d'autres en bénéficient
```

## Métriques de Succès

### Indicateurs

| Période | Objectif |
|---------|----------|
| Fin semaine 1 | Env local fonctionne, 1 PR mergée |
| Fin semaine 2 | Première vraie feature livrée |
| Fin mois 1 | Autonome sur tâches standards |
| Fin mois 2 | Contribue aux discussions techniques |

### Feedback

```markdown
## Template Feedback Onboarding

### À la fin de la semaine 2

1. **Setup** : Le setup était-il clair ? Qu'est-ce qui a bloqué ?
2. **Documentation** : Qu'est-ce qui manquait ?
3. **Accompagnement** : Le buddy était-il disponible ?
4. **Codebase** : Qu'est-ce qui reste flou ?
5. **Suggestions** : Comment améliorer l'onboarding ?
```

## Points d'Escalade

| Situation | Action |
|-----------|--------|
| Env qui ne fonctionne pas après 2h | Escalade buddy → Tech Lead |
| Blocage technique > 1 jour | Pair programming |
| Manque d'accès | Escalade aux ops |
| Feedback négatif sur process | Améliorer la documentation |

## Livrables

| Livrable | Description |
|----------|-------------|
| Guide d'onboarding technique | Plan semaine 1 avec jalons, ressources et buddy assigné |
| Checklist premiers pas | Étapes setup environnement, accès et première contribution |
| Kit de bienvenue | Docs architecture, conventions, outils et contacts utiles |
