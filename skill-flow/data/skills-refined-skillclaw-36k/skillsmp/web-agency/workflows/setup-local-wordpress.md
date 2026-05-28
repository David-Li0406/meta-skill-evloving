# Workflow : Setup Environnement Local WordPress

Ce workflow guide le processus complet pour mettre en place un environnement de développement WordPress local, de la création de l'issue à l'implémentation autonome.

---

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        WORKFLOW SETUP LOCAL WORDPRESS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. ISSUE          2. POURQUOI         3. QUOI           4. COMMENT         │
│  ────────────      ────────────        ────────────      ────────────       │
│  Créer le          Justifier           Définir le        Implémenter        │
│  ticket            le besoin           process           concrètement       │
│                                                                              │
│  ┌──────────┐     ┌──────────┐        ┌──────────┐      ┌──────────┐       │
│  │ GitHub   │ ──▶ │direction-│ ──▶    │web-dev-  │ ──▶  │wordpress-│       │
│  │ Issue    │     │technique │        │process   │      │gutenberg │       │
│  └──────────┘     └──────────┘        └──────────┘      └──────────┘       │
│                                                                              │
│  issue-management  environnements     setup/environment  tooling/local-dev  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Étape 1 : Créer l'Issue GitHub

### Template à Utiliser

**Fichier** : `wordpress-gutenberg-expert/agents/tooling/issue-management.md`
**Template** : `wp_dev_environment.yml`

### Contenu de l'Issue

```yaml
Titre: [DevEnv]: Setup environnement local WordPress

Type d'environnement: wp-env (@wordpress/env)
Version WordPress: 6.4
Version PHP: 8.2

Fonctionnalités requises:
  ✅ Debug mode (WP_DEBUG)
  ✅ Query Monitor
  ☐ Mailhog (optionnel)
  ☐ phpMyAdmin (optionnel)

Plugins à pré-installer:
  - query-monitor
  - debug-bar

Critères d'acceptance:
  - [ ] Environnement démarre sans erreur
  - [ ] WordPress accessible sur localhost
  - [ ] Admin accessible (admin/password)
  - [ ] Debug mode activé
  - [ ] Plugins dev installés et activés
  - [ ] Documentation README mise à jour
```

### Section POURQUOI dans l'Issue

> **Pourquoi ce setup ?**
> - Permettre aux développeurs de travailler en local sans dépendance serveur
> - Garantir la parité avec la production (PHP 8.2, WP 6.4)
> - Objectif : nouveau dev opérationnel en < 15 min
>
> **Références** : Voir politique `direction-technique/infrastructure/environnements`

---

## Étape 2 : Consulter les Politiques (POURQUOI)

### Agent à Consulter

**Fichier** : `direction-technique/infrastructure/environnements.md`

### Points Clés à Valider

| Politique | Vérification | Status |
|-----------|--------------|--------|
| Données en local | Fictives uniquement | ☐ |
| Parité versions | PHP/WP identiques à prod | ☐ |
| Temps de setup | < 15 min cible | ☐ |
| Reproductibilité | Aucune config manuelle | ☐ |

### Questions à Se Poser

1. **Parité** : Les versions PHP/WP/MySQL sont-elles identiques à la prod ?
2. **Données** : Utilise-t-on des fixtures ou un dump anonymisé ?
3. **Secrets** : Comment gérer les clés API en local ?
4. **Documentation** : Le README sera-t-il mis à jour ?

---

## Étape 3 : Définir le Process (QUOI)

### Agent à Consulter

**Fichier** : `web-dev-process/agents/setup/environment.md`

### Checklist Process

```markdown
## Setup Environnement - Checklist QUOI

### Fichiers à Créer/Configurer
- [ ] `.wp-env.json` - Configuration wp-env
- [ ] `.wp-env.override.json.example` - Template pour overrides personnels
- [ ] `.gitignore` - Exclure .wp-env.override.json
- [ ] `README.md` - Section "Getting Started"

### Outils à Mettre en Place
- [ ] @wordpress/env (recommandé) OU Docker Compose OU Local
- [ ] WP-CLI pour les commandes WordPress
- [ ] Scripts npm pour simplifier les commandes

### Scripts à Créer
- [ ] `npm run start` → Démarrer l'environnement
- [ ] `npm run stop` → Arrêter l'environnement
- [ ] `npm run reset` → Reset complet
- [ ] `npm run seed` → Charger les données de démo
```

---

## Étape 4 : Implémenter (COMMENT)

### Agent à Consulter

**Fichier** : `wordpress-gutenberg-expert/agents/tooling/local-dev.md`

### Implémentation Complète

#### 1. Installer wp-env

```bash
npm install --save-dev @wordpress/env
```

#### 2. Créer .wp-env.json

```json
{
    "core": "WordPress/WordPress#6.4",
    "phpVersion": "8.2",
    "plugins": [
        "./wp-content/plugins/mon-plugin",
        "https://downloads.wordpress.org/plugin/query-monitor.latest-stable.zip"
    ],
    "themes": [
        "./wp-content/themes/mon-theme"
    ],
    "config": {
        "WP_DEBUG": true,
        "WP_DEBUG_LOG": true,
        "SCRIPT_DEBUG": true,
        "WP_ENVIRONMENT_TYPE": "development"
    },
    "port": 8888
}
```

#### 3. Ajouter Scripts package.json

```json
{
  "scripts": {
    "wp-env": "wp-env",
    "start": "wp-env start",
    "stop": "wp-env stop",
    "reset": "wp-env destroy && wp-env start",
    "cli": "wp-env run cli",
    "seed": "wp-env run cli wp plugin activate --all"
  }
}
```

#### 4. Mettre à Jour README.md

```markdown
## Getting Started

### Prérequis
- Node.js 18+
- Docker Desktop

### Installation
\`\`\`bash
git clone [repo]
cd [project]
npm install
npm run start
\`\`\`

### Accès
- Site : http://localhost:8888
- Admin : http://localhost:8888/wp-admin
- Credentials : admin / password

### Commandes Utiles
- `npm run stop` - Arrêter l'environnement
- `npm run reset` - Reset complet
- `npm run cli wp [command]` - Exécuter WP-CLI
```

---

## Validation Finale

### Checklist de Validation

```markdown
## Validation Setup Local

### Fonctionnel
- [ ] `npm run start` démarre sans erreur
- [ ] WordPress accessible sur http://localhost:8888
- [ ] Login admin/password fonctionne
- [ ] WP_DEBUG activé (erreurs affichées)
- [ ] Query Monitor visible dans la barre admin

### Documentation
- [ ] README.md mis à jour avec Getting Started
- [ ] .wp-env.json commité
- [ ] .wp-env.override.json dans .gitignore

### Conformité Politiques
- [ ] Pas de données de production
- [ ] Versions PHP/WP identiques à prod
- [ ] Setup testé par un autre dev (< 15 min)

### Issue GitHub
- [ ] Critères d'acceptance validés
- [ ] Issue fermée avec commentaire de résolution
```

---

## Flux IA Autonome

Pour une implémentation autonome par l'IA :

```
1. Lire l'issue GitHub
   ↓
2. Consulter direction-technique/infrastructure/environnements.md
   → Extraire : versions cibles, politique données
   ↓
3. Consulter web-dev-process/agents/setup/environment.md
   → Extraire : checklist fichiers à créer
   ↓
4. Consulter wordpress-gutenberg-expert/agents/tooling/local-dev.md
   → Extraire : code .wp-env.json, scripts, commandes
   ↓
5. Implémenter :
   - Créer .wp-env.json
   - Modifier package.json (scripts)
   - Mettre à jour README.md
   - Créer .wp-env.override.json.example
   ↓
6. Valider :
   - Exécuter npm run start
   - Vérifier accès localhost:8888
   - Tester login admin
   ↓
7. Commiter et fermer l'issue
```

---

## Agents Impliqués

| Étape | Skill | Agent | Niveau |
|-------|-------|-------|--------|
| Issue | wordpress-gutenberg-expert | `tooling/issue-management.md` | COMMENT |
| Politique | direction-technique | `infrastructure/environnements.md` | POURQUOI |
| Process | web-dev-process | `setup/environment.md` | QUOI |
| Code | wordpress-gutenberg-expert | `tooling/local-dev.md` | COMMENT |
