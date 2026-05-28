# Guide de Démarrage Rapide

Ce guide vous permet de démarrer rapidement avec le développement WordPress et Gutenberg.

## Table des Matières

1. [Configuration de l'Environnement](#configuration-de-lenvironnement)
2. [Créer un Block Custom](#créer-un-block-custom)
3. [Créer un Plugin](#créer-un-plugin)
4. [Créer un Block Theme](#créer-un-block-theme)
5. [Cheatsheets](#cheatsheets)

---

## Configuration de l'Environnement

### Option 1 : wp-env (Recommandé)

```bash
# Prérequis : Node.js 18+ et Docker

# Installer wp-env globalement
npm install -g @wordpress/env

# Dans votre projet
cd mon-projet
wp-env start

# WordPress disponible sur http://localhost:8888
# Admin : admin / password
```

**`.wp-env.json`** :

```json
{
    "core": null,
    "phpVersion": "8.2",
    "plugins": [ "." ],
    "themes": [ "./theme" ],
    "config": {
        "WP_DEBUG": true,
        "WP_DEBUG_LOG": true
    }
}
```

### Option 2 : Local by Flywheel

1. Télécharger [Local](https://localwp.com/)
2. Créer un nouveau site
3. Lier votre dossier plugin/theme

### Option 3 : Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    volumes:
      - ./wp-content:/var/www/html/wp-content
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DEBUG: 1
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: root
```

```bash
docker-compose up -d
```

---

## Créer un Block Custom

### Étape 1 : Scaffolding

```bash
# Créer le block
npx @wordpress/create-block mon-block

# Structure générée :
mon-block/
├── build/
├── src/
│   ├── block.json
│   ├── edit.js
│   ├── editor.scss
│   ├── index.js
│   ├── save.js
│   └── style.scss
├── mon-block.php
└── package.json
```

### Étape 2 : Configurer block.json

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "mon-plugin/mon-block",
    "version": "1.0.0",
    "title": "Mon Block",
    "category": "widgets",
    "icon": "smiley",
    "description": "Un block personnalisé.",
    "attributes": {
        "message": {
            "type": "string",
            "default": "Hello World!"
        }
    },
    "supports": {
        "color": {
            "background": true,
            "text": true
        },
        "spacing": {
            "padding": true,
            "margin": true
        }
    },
    "textdomain": "mon-block",
    "editorScript": "file:./index.js",
    "editorStyle": "file:./index.css",
    "style": "file:./style-index.css"
}
```

### Étape 3 : Éditer le Block (edit.js)

```jsx
import { __ } from '@wordpress/i18n';
import { useBlockProps, RichText } from '@wordpress/block-editor';
import './editor.scss';

export default function Edit( { attributes, setAttributes } ) {
    const blockProps = useBlockProps();

    return (
        <div { ...blockProps }>
            <RichText
                tagName="p"
                value={ attributes.message }
                onChange={ ( message ) => setAttributes( { message } ) }
                placeholder={ __( 'Écrivez quelque chose...', 'mon-block' ) }
            />
        </div>
    );
}
```

### Étape 4 : Sauvegarder le Block (save.js)

```jsx
import { useBlockProps, RichText } from '@wordpress/block-editor';

export default function Save( { attributes } ) {
    const blockProps = useBlockProps.save();

    return (
        <div { ...blockProps }>
            <RichText.Content tagName="p" value={ attributes.message } />
        </div>
    );
}
```

### Étape 5 : Build et Test

```bash
npm run build    # Build production
npm run start    # Watch mode
```

---

## Créer un Plugin

### Structure Minimale

```
mon-plugin/
├── build/
├── src/
│   └── blocks/
│       └── mon-block/
├── includes/
│   └── class-mon-plugin.php
├── mon-plugin.php
├── package.json
└── composer.json
```

### Fichier Principal (mon-plugin.php)

```php
<?php
/**
 * Plugin Name: Mon Plugin
 * Description: Description du plugin
 * Version: 1.0.0
 * Author: Votre Nom
 * License: GPL-2.0-or-later
 * Text Domain: mon-plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'MON_PLUGIN_VERSION', '1.0.0' );
define( 'MON_PLUGIN_PATH', plugin_dir_path( __FILE__ ) );
define( 'MON_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

// Charger les dépendances
require_once MON_PLUGIN_PATH . 'includes/class-mon-plugin.php';

// Initialiser
function mon_plugin_init() {
    return Mon_Plugin::instance();
}
add_action( 'plugins_loaded', 'mon_plugin_init' );

// Activation
register_activation_hook( __FILE__, array( 'Mon_Plugin', 'activate' ) );

// Désactivation
register_deactivation_hook( __FILE__, array( 'Mon_Plugin', 'deactivate' ) );
```

### Classe Principale (includes/class-mon-plugin.php)

```php
<?php
class Mon_Plugin {
    private static $instance = null;

    public static function instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->init_hooks();
    }

    private function init_hooks() {
        add_action( 'init', array( $this, 'register_blocks' ) );
        add_action( 'init', array( $this, 'register_post_types' ) );
    }

    public function register_blocks() {
        register_block_type( MON_PLUGIN_PATH . 'build/blocks/mon-block' );
    }

    public function register_post_types() {
        register_post_type( 'mon_cpt', array(
            'labels'       => array( 'name' => 'Mon CPT' ),
            'public'       => true,
            'show_in_rest' => true,
            'supports'     => array( 'title', 'editor', 'thumbnail' ),
        ) );
    }

    public static function activate() {
        // Activation logic
        flush_rewrite_rules();
    }

    public static function deactivate() {
        // Désactivation logic
        flush_rewrite_rules();
    }
}
```

### package.json

```json
{
    "name": "mon-plugin",
    "version": "1.0.0",
    "scripts": {
        "build": "wp-scripts build",
        "start": "wp-scripts start",
        "lint:js": "wp-scripts lint-js",
        "lint:css": "wp-scripts lint-style"
    },
    "devDependencies": {
        "@wordpress/scripts": "^27.0.0"
    }
}
```

---

## Créer un Block Theme

### Structure Minimale

```
mon-theme/
├── parts/
│   ├── header.html
│   └── footer.html
├── templates/
│   └── index.html
├── functions.php
├── style.css
└── theme.json
```

### style.css

```css
/*
Theme Name: Mon Theme
Author: Votre Nom
Description: Un block theme moderne.
Version: 1.0.0
Requires at least: 6.0
Tested up to: 6.4
Requires PHP: 8.0
License: GNU General Public License v2 or later
Text Domain: mon-theme
*/
```

### theme.json

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "settings": {
        "appearanceTools": true,
        "layout": {
            "contentSize": "800px",
            "wideSize": "1200px"
        },
        "color": {
            "palette": [
                { "slug": "primary", "color": "#0073aa", "name": "Primary" },
                { "slug": "secondary", "color": "#23282d", "name": "Secondary" },
                { "slug": "background", "color": "#ffffff", "name": "Background" },
                { "slug": "foreground", "color": "#1e1e1e", "name": "Foreground" }
            ]
        },
        "typography": {
            "fontSizes": [
                { "slug": "small", "size": "0.875rem", "name": "Small" },
                { "slug": "medium", "size": "1rem", "name": "Medium" },
                { "slug": "large", "size": "1.5rem", "name": "Large" }
            ]
        }
    },
    "styles": {
        "color": {
            "background": "var(--wp--preset--color--background)",
            "text": "var(--wp--preset--color--foreground)"
        }
    }
}
```

### templates/index.html

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:query {"queryId":1,"query":{"inherit":true}} -->
    <div class="wp-block-query">
        <!-- wp:post-template -->
            <!-- wp:post-title {"isLink":true} /-->
            <!-- wp:post-excerpt /-->
        <!-- /wp:post-template -->
        <!-- wp:query-pagination -->
            <!-- wp:query-pagination-previous /-->
            <!-- wp:query-pagination-numbers /-->
            <!-- wp:query-pagination-next /-->
        <!-- /wp:query-pagination -->
    </div>
    <!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### parts/header.html

```html
<!-- wp:group {"tagName":"header","layout":{"type":"constrained"}} -->
<header class="wp-block-group">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:site-title /-->
        <!-- wp:navigation /-->
    </div>
    <!-- /wp:group -->
</header>
<!-- /wp:group -->
```

### functions.php

```php
<?php
function mon_theme_setup() {
    add_theme_support( 'automatic-feed-links' );
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_editor_style( 'style.css' );
}
add_action( 'after_setup_theme', 'mon_theme_setup' );
```

---

## Cheatsheets

### Hooks Essentiels

```php
// Initialisation
add_action( 'init', 'my_function' );                    // Chargement général
add_action( 'admin_init', 'my_admin_function' );        // Admin seulement

// Scripts
add_action( 'wp_enqueue_scripts', 'my_scripts' );       // Frontend
add_action( 'admin_enqueue_scripts', 'my_admin_scripts' ); // Admin
add_action( 'enqueue_block_editor_assets', 'my_editor_scripts' ); // Éditeur

// Contenu
add_filter( 'the_content', 'my_content_filter' );
add_filter( 'the_title', 'my_title_filter', 10, 2 );

// Posts
add_action( 'save_post', 'my_save_function', 10, 3 );
add_action( 'before_delete_post', 'my_delete_function' );
```

### Fonctions de Sécurité

```php
// Sanitization (INPUT)
sanitize_text_field( $input );        // Texte simple
sanitize_textarea_field( $input );    // Textarea
sanitize_email( $input );             // Email
esc_url_raw( $input );                // URL pour stockage
absint( $input );                     // Entier positif
wp_kses_post( $input );               // HTML autorisé posts

// Escaping (OUTPUT)
esc_html( $output );                  // HTML
esc_attr( $output );                  // Attribut HTML
esc_url( $output );                   // URL
esc_js( $output );                    // JavaScript
wp_kses_post( $output );              // HTML autorisé

// Nonces
wp_nonce_field( 'action', 'nonce_name' );           // Créer
wp_verify_nonce( $_POST['nonce'], 'action' );       // Vérifier
check_ajax_referer( 'action', 'nonce' );            // AJAX
```

### WP-CLI Commandes Essentielles

```bash
# Installation
wp core download
wp core install --url=example.com --title="Site" --admin_user=admin --admin_email=admin@example.com

# Plugins
wp plugin install query-monitor --activate
wp plugin list
wp plugin deactivate --all

# Themes
wp theme activate mon-theme
wp theme list

# Database
wp db export backup.sql
wp db import backup.sql
wp search-replace 'old.com' 'new.com'

# Cache
wp cache flush
wp transient delete --all

# Posts
wp post create --post_title="Test" --post_status=publish
wp post list --post_type=page

# Utilisateurs
wp user create bob bob@example.com --role=author
```

### Block Supports

```json
{
    "supports": {
        "align": true,
        "alignWide": true,
        "anchor": true,
        "className": true,
        "color": {
            "background": true,
            "text": true,
            "gradients": true,
            "link": true
        },
        "spacing": {
            "padding": true,
            "margin": true,
            "blockGap": true
        },
        "typography": {
            "fontSize": true,
            "lineHeight": true,
            "fontFamily": true
        },
        "border": {
            "color": true,
            "radius": true,
            "style": true,
            "width": true
        }
    }
}
```

### React Hooks WordPress

```jsx
// Données
import { useSelect, useDispatch } from '@wordpress/data';
import { useEntityProp } from '@wordpress/core-data';

// Sélectionner des données
const posts = useSelect( ( select ) => {
    return select( 'core' ).getEntityRecords( 'postType', 'post' );
} );

// Actions
const { savePost } = useDispatch( 'core/editor' );

// Meta du post actuel
const [ meta, setMeta ] = useEntityProp( 'postType', 'post', 'meta' );
```

---

## Ressources

### Documentation Officielle

- [Developer Resources](https://developer.wordpress.org/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)
- [Theme Handbook](https://developer.wordpress.org/themes/)
- [Plugin Handbook](https://developer.wordpress.org/plugins/)

### Outils

- [WordPress Playground](https://playground.wordpress.net/)
- [Theme Unit Test Data](https://github.com/WordPress/theme-test-data)
- [Gutenberg Storybook](https://wordpress.github.io/gutenberg/)

### Communauté

- [Make WordPress](https://make.wordpress.org/)
- [WordPress Stack Exchange](https://wordpress.stackexchange.com/)
- [WordPress Slack](https://make.wordpress.org/chat/)
