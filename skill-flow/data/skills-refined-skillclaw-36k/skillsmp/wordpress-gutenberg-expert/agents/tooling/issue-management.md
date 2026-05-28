---
name: issue-management
description: WordPress Issue Templates Expert
niveau: comment
workflows:
  - id: issue-template-creation
    template: wf-support
    phase: Réception
    name: Création templates issues
    duration: 0.5 jour
---

# WordPress Issue Templates Expert

Tu fournis les **templates d'issues techniques** pour les demandes WordPress sur GitHub/GitLab.

## Rôle (Niveau COMMENT)

> **Ce que tu fais** :
> - Fournir des templates d'issues prêts à l'emploi
> - Capturer les spécifications techniques pour l'implémentation
> - Standardiser le format des demandes WordPress
>
> **Ce que tu NE fais PAS** :
> - Clarifier le besoin métier → `direction-technique/specification/clarification-donnees`
> - Définir le process → `web-dev-process/agents/design/wordpress-data-mapping`

## Prérequis (Niveau POURQUOI)

> **IMPORTANT** : Ces templates sont à utiliser APRÈS la phase de clarification.
>
> Avant de créer une issue avec ces templates, s'assurer que :
> - [ ] Le besoin a été clarifié (`clarification-donnees.md`)
> - [ ] La décision "WordPress CPT" a été prise (`modelisation-donnees.md`)
> - [ ] Le mapping métier → WordPress est défini (`wordpress-data-mapping.md`)
>
> Ces templates capturent les **spécifications techniques** issues de la clarification.

---

> **Note** : Pour les templates génériques (bug report, feature request, security), voir `web-dev-process/templates/ISSUE_TEMPLATE/`.

## Ton Domaine

- Templates d'issues WordPress-spécifiques
- Block Gutenberg requests
- Custom Post Type requests
- Custom Taxonomy requests
- Custom Meta requests
- WordPress environment setup

## Sources

- **web-dev-process** : `../../../web-dev-process/templates/` pour les templates génériques
- **GitHub Issue Forms** : <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms>

## Templates WordPress-Spécifiques

### Block Gutenberg Request

```yaml
# .github/ISSUE_TEMPLATE/block_request.yml
name: 🧱 Block Gutenberg
description: Créer ou modifier un block Gutenberg
title: "[Block]: "
labels: ["block", "gutenberg", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Demande concernant un block Gutenberg.

  - type: dropdown
    id: type
    attributes:
      label: Type de demande
      options:
        - Nouveau block custom
        - Block variation
        - Block style
        - Modification block existant
        - Pattern (composition de blocks)
    validations:
      required: true

  - type: input
    id: block-name
    attributes:
      label: Nom du block
      description: Le nom technique du block
      placeholder: "my-namespace/my-block"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description
      description: À quoi sert ce block ?
      placeholder: "Ce block permet de..."
    validations:
      required: true

  - type: textarea
    id: attributes
    attributes:
      label: Attributs
      description: Quels attributs/options le block doit-il avoir ?
      placeholder: |
        - title (string) : Titre du block
        - showImage (boolean) : Afficher l'image
        - columns (number) : Nombre de colonnes
    validations:
      required: false

  - type: dropdown
    id: supports
    attributes:
      label: Block Supports
      description: Quelles options de l'éditeur activer ?
      multiple: true
      options:
        - color (background, text)
        - typography (fontSize, lineHeight)
        - spacing (margin, padding)
        - align (wide, full)
        - anchor
        - className
    validations:
      required: false

  - type: dropdown
    id: render
    attributes:
      label: Type de rendu
      options:
        - Statique (save en JS)
        - Dynamique (render_callback PHP)
        - Hybride (JS + PHP)
    validations:
      required: true

  - type: textarea
    id: design
    attributes:
      label: Design / Maquette
      description: Lien Figma ou captures d'écran
      placeholder: "https://figma.com/..."
    validations:
      required: false

  - type: textarea
    id: acceptance
    attributes:
      label: Critères d'acceptance
      value: |
        - [ ] Block visible dans l'inserter
        - [ ] Options fonctionnelles dans l'éditeur
        - [ ] Rendu frontend conforme à la maquette
        - [ ] Responsive mobile/tablet/desktop
        - [ ] Accessible (WCAG 2.1 AA)
    validations:
      required: false
```

### Custom Post Type Request

```yaml
# .github/ISSUE_TEMPLATE/wp_custom_post_type.yml
name: 📝 Custom Post Type
description: Créer un nouveau Custom Post Type
title: "[CPT]: "
labels: ["cpt", "wp-core", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Création d'un nouveau Custom Post Type WordPress.

  - type: input
    id: post-type
    attributes:
      label: Nom technique (slug)
      description: En minuscules, sans espaces (max 20 caractères)
      placeholder: "portfolio"
    validations:
      required: true

  - type: input
    id: singular
    attributes:
      label: Label singulier
      placeholder: "Projet"
    validations:
      required: true

  - type: input
    id: plural
    attributes:
      label: Label pluriel
      placeholder: "Projets"
    validations:
      required: true

  - type: dropdown
    id: public
    attributes:
      label: Visibilité
      options:
        - Public (visible frontend + admin)
        - Private (admin seulement)
        - Internal (API seulement)
    validations:
      required: true

  - type: checkboxes
    id: supports
    attributes:
      label: Supports (fonctionnalités)
      options:
        - label: title
        - label: editor (Gutenberg)
        - label: thumbnail (image mise en avant)
        - label: excerpt
        - label: author
        - label: custom-fields
        - label: revisions
        - label: page-attributes (ordre, parent)

  - type: checkboxes
    id: features
    attributes:
      label: Options
      options:
        - label: has_archive (page d'archive)
        - label: hierarchical (comme les pages)
        - label: show_in_rest (API REST + Gutenberg)
        - label: Menu admin dédié

  - type: input
    id: menu-icon
    attributes:
      label: Icône menu admin
      description: Dashicon ou URL
      placeholder: "dashicons-portfolio"

  - type: input
    id: rewrite-slug
    attributes:
      label: Slug URL (rewrite)
      placeholder: "projets"

  - type: textarea
    id: taxonomies
    attributes:
      label: Taxonomies associées
      placeholder: |
        - category (existante)
        - portfolio_category (à créer)

  - type: textarea
    id: acceptance
    attributes:
      label: Critères d'acceptance
      value: |
        - [ ] CPT enregistré et visible dans l'admin
        - [ ] Labels corrects (singulier/pluriel)
        - [ ] Supports configurés
        - [ ] Icône affichée dans le menu
        - [ ] URL rewrite fonctionnelle
        - [ ] API REST accessible (si activé)
        - [ ] Compatible Gutenberg (si editor activé)
```

### Custom Taxonomy Request

```yaml
# .github/ISSUE_TEMPLATE/wp_custom_taxonomy.yml
name: 🗂️ Custom Taxonomy
description: Créer une nouvelle taxonomie personnalisée
title: "[Taxonomy]: "
labels: ["taxonomy", "wp-core", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Création d'une nouvelle taxonomie WordPress.

  - type: input
    id: taxonomy
    attributes:
      label: Nom technique (slug)
      description: En minuscules, sans espaces (max 32 caractères)
      placeholder: "portfolio_category"
    validations:
      required: true

  - type: input
    id: singular
    attributes:
      label: Label singulier
      placeholder: "Catégorie de projet"
    validations:
      required: true

  - type: input
    id: plural
    attributes:
      label: Label pluriel
      placeholder: "Catégories de projets"
    validations:
      required: true

  - type: textarea
    id: post-types
    attributes:
      label: Post types associés
      placeholder: |
        - portfolio
        - post
    validations:
      required: true

  - type: dropdown
    id: hierarchical
    attributes:
      label: Type de taxonomie
      options:
        - Hiérarchique (comme les catégories)
        - Non-hiérarchique (comme les tags)
    validations:
      required: true

  - type: checkboxes
    id: options
    attributes:
      label: Options
      options:
        - label: public (visible frontend)
        - label: show_in_rest (API REST + Gutenberg)
        - label: show_admin_column (colonne dans la liste)
        - label: show_in_quick_edit
        - label: show_tagcloud

  - type: input
    id: rewrite-slug
    attributes:
      label: Slug URL (rewrite)
      placeholder: "categorie-projet"

  - type: textarea
    id: acceptance
    attributes:
      label: Critères d'acceptance
      value: |
        - [ ] Taxonomie enregistrée et visible dans l'admin
        - [ ] Associée aux bons post types
        - [ ] Labels corrects
        - [ ] Hiérarchie configurée
        - [ ] URL rewrite fonctionnelle
        - [ ] API REST accessible (si activé)
```

### Custom Post Meta Request

```yaml
# .github/ISSUE_TEMPLATE/wp_custom_meta.yml
name: 🏷️ Custom Post Meta
description: Créer des meta fields pour un post type
title: "[Meta]: "
labels: ["meta", "wp-core", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Création de meta fields personnalisés pour un post type.

  - type: input
    id: post-type
    attributes:
      label: Post Type cible
      placeholder: "portfolio"
    validations:
      required: true

  - type: textarea
    id: meta-fields
    attributes:
      label: Meta fields à créer
      description: Un champ par ligne avec format "meta_key | type | description"
      placeholder: |
        _portfolio_client | string | Nom du client
        _portfolio_url | url | URL du projet
        _portfolio_date | date | Date de réalisation
        _portfolio_featured | boolean | Projet mis en avant
    validations:
      required: true

  - type: dropdown
    id: ui-type
    attributes:
      label: Interface d'édition
      options:
        - Meta box custom (PHP)
        - Plugin ACF
        - Plugin CMB2
        - Plugin Meta Box
        - Sidebar Gutenberg (SlotFill)
    validations:
      required: true

  - type: checkboxes
    id: options
    attributes:
      label: Options
      options:
        - label: show_in_rest (exposer dans l'API REST)
        - label: single (valeur unique vs array)
        - label: sanitize_callback
        - label: auth_callback (permissions)

  - type: textarea
    id: acceptance
    attributes:
      label: Critères d'acceptance
      value: |
        - [ ] Meta fields enregistrés avec register_post_meta()
        - [ ] Interface d'édition fonctionnelle
        - [ ] Données sauvegardées correctement
        - [ ] Sanitization en place
        - [ ] Accessible via API REST (si activé)
        - [ ] Documentation des champs
```

### Custom Term Meta Request

```yaml
# .github/ISSUE_TEMPLATE/wp_term_meta.yml
name: 🔖 Custom Term Meta
description: Créer des meta fields pour une taxonomie
title: "[TermMeta]: "
labels: ["term-meta", "taxonomy", "wp-core", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Création de meta fields personnalisés pour les termes d'une taxonomie.

  - type: input
    id: taxonomy
    attributes:
      label: Taxonomie cible
      placeholder: "portfolio_category"
    validations:
      required: true

  - type: textarea
    id: meta-fields
    attributes:
      label: Meta fields à créer
      description: Un champ par ligne avec format "meta_key | type | description"
      placeholder: |
        _term_icon | string | Classe d'icône (dashicons)
        _term_color | string | Couleur HEX
        _term_image | attachment_id | Image de la catégorie
        _term_order | integer | Ordre d'affichage
    validations:
      required: true

  - type: checkboxes
    id: options
    attributes:
      label: Options
      options:
        - label: show_in_rest (exposer dans l'API REST)
        - label: Champs dans formulaire d'ajout
        - label: Champs dans formulaire d'édition
        - label: Colonne dans la liste des termes

  - type: textarea
    id: acceptance
    attributes:
      label: Critères d'acceptance
      value: |
        - [ ] Meta fields enregistrés avec register_term_meta()
        - [ ] Champs affichés dans le formulaire d'ajout de terme
        - [ ] Champs affichés dans le formulaire d'édition
        - [ ] Données sauvegardées correctement (add/edit)
        - [ ] Sanitization en place
        - [ ] Accessible via API REST (si activé)
```

### WordPress Dev Environment Setup

```yaml
# .github/ISSUE_TEMPLATE/wp_dev_environment.yml
name: 🛠️ WordPress Dev Environment
description: Mettre en place un environnement de développement WordPress
title: "[DevEnv]: "
labels: ["setup", "environment", "triage"]

body:
  - type: markdown
    attributes:
      value: |
        Configuration d'un environnement de développement WordPress.

  - type: dropdown
    id: env-type
    attributes:
      label: Type d'environnement
      options:
        - wp-env (@wordpress/env)
        - Docker Compose
        - Local by Flywheel
        - DDEV
        - Autre
    validations:
      required: true

  - type: input
    id: wp-version
    attributes:
      label: Version WordPress cible
      placeholder: "6.4"
    validations:
      required: true

  - type: input
    id: php-version
    attributes:
      label: Version PHP
      placeholder: "8.2"
    validations:
      required: true

  - type: checkboxes
    id: features
    attributes:
      label: Fonctionnalités requises
      options:
        - label: Debug mode (WP_DEBUG)
        - label: Query Monitor
        - label: Mailhog (emails)
        - label: phpMyAdmin
        - label: SSL local
        - label: Multisite

  - type: textarea
    id: plugins
    attributes:
      label: Plugins à pré-installer
      placeholder: |
        - query-monitor
        - debug-bar
        - plugin-custom

  - type: textarea
    id: acceptance
    attributes:
      label: Critères d'acceptance
      value: |
        - [ ] Environnement démarre sans erreur
        - [ ] WordPress accessible sur localhost
        - [ ] Admin accessible (admin/password)
        - [ ] Debug mode activé
        - [ ] Plugins dev installés et activés
        - [ ] Documentation README mise à jour
```

## Labels WordPress-Spécifiques

À ajouter aux labels génériques de `web-dev-process` :

```yaml
# Labels WordPress spécifiques
- name: block
  color: "7057ff"
  description: "Gutenberg block related"

- name: gutenberg
  color: "7057ff"
  description: "Gutenberg/Block Editor"

- name: cpt
  color: "0075ca"
  description: "Custom Post Type"

- name: taxonomy
  color: "0075ca"
  description: "Custom Taxonomy"

- name: meta
  color: "0075ca"
  description: "Post/Term Meta"

- name: theme
  color: "0075ca"
  description: "Theme related"

- name: plugin
  color: "008672"
  description: "Plugin related"

- name: wp-core
  color: "21759b"
  description: "WordPress Core functionality"

- name: wp-rest-api
  color: "21759b"
  description: "WordPress REST API"
```

## Usage

### Combiner avec web-dev-process

```bash
# Copier les templates génériques
cp -r .web-agency/skills/web-dev-process/templates/ISSUE_TEMPLATE/* .github/ISSUE_TEMPLATE/

# Ajouter les templates WordPress
# (copier le contenu YAML ci-dessus dans les fichiers appropriés)
```

### Structure finale

```
.github/
├── ISSUE_TEMPLATE/
│   ├── config.yml              # De web-dev-process
│   ├── bug_report.md           # De web-dev-process
│   ├── feature_request.md      # De web-dev-process
│   ├── task.md                 # De web-dev-process
│   ├── block_request.yml       # WordPress-spécifique
│   ├── wp_custom_post_type.yml # WordPress-spécifique
│   ├── wp_custom_taxonomy.yml  # WordPress-spécifique
│   ├── wp_custom_meta.yml      # WordPress-spécifique
│   ├── wp_term_meta.yml        # WordPress-spécifique
│   └── wp_dev_environment.yml  # WordPress-spécifique
└── PULL_REQUEST_TEMPLATE.md    # De web-dev-process
```

## Checklist

- [ ] Templates génériques copiés depuis web-dev-process
- [ ] Templates WordPress ajoutés
- [ ] Labels WordPress configurés
- [ ] CONTRIBUTING.md référence les deux sources

## Livrables

| Livrable | Description |
|----------|-------------|
| Issue templates | Templates GitHub/GitLab pour bugs, features, questions |
| PR templates | Templates de pull request |
| Labels configuration | Labels configurés pour WordPress et général |
| CONTRIBUTING.md | Guide de contribution au projet |
| Workflow documentation | Documentation du workflow d'issues et PRs |
