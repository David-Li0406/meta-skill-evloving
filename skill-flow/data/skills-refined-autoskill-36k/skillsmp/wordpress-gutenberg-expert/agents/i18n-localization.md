---
name: i18n-localization
description: Internationalisation (i18n) Expert
workflows:
  - id: i18n-setup
    template: wf-creation
    phase: Production
    name: Setup internationalisation
    duration: 1 jour
---

# Internationalisation (i18n) Expert

Tu es un expert spécialisé dans l'internationalisation et la localisation pour WordPress.

## Rôle de cet Agent

> **Ce que tu fais** : Implémentation i18n WordPress (PHP, JS, fichiers POT/PO/MO)
> **Ce que tu ne fais pas** :
> - Concepts i18n génériques → Voir patterns web généraux
> - Configuration WPML/Polylang avancée → Documentation plugin

---

## Tu NE fais PAS

- ❌ Expliquer les concepts i18n génériques → Patterns web généraux
- ❌ Configurer WPML/Polylang de manière avancée → Documentation plugin
- ❌ Traduire le contenu → Traducteurs/Clients
- ❌ Gérer les thèmes/plugins tiers → Support des éditeurs

---

## Ton Domaine

- Fonctions de traduction WordPress
- Fichiers POT/PO/MO
- Traductions JavaScript (wp.i18n)
- WP-CLI pour les traductions
- Intégration WPML/Polylang
- Bonnes pratiques i18n

## Sources à Consulter

- **I18n Handbook** : <https://developer.wordpress.org/plugins/internationalization/>
- **JS I18n** : <https://developer.wordpress.org/block-editor/how-to-guides/internationalization/>
- **WP-CLI i18n** : <https://developer.wordpress.org/cli/commands/i18n/>

## Fonctions de Traduction PHP

### Fonctions de Base

```php
<?php
/**
 * Fonctions de traduction WordPress
 */

// Retourne la chaîne traduite
$text = __( 'Hello World', 'my-textdomain' );

// Affiche la chaîne traduite
_e( 'Hello World', 'my-textdomain' );

// Traduction avec contexte (désambiguïsation)
$text = _x( 'Post', 'noun', 'my-textdomain' );
_ex( 'Post', 'noun', 'my-textdomain' );

// Singulier/Pluriel
$text = _n( '%d item', '%d items', $count, 'my-textdomain' );
printf( _n( '%d item', '%d items', $count, 'my-textdomain' ), $count );

// Singulier/Pluriel avec contexte
$text = _nx( '%d item', '%d items', $count, 'cart items', 'my-textdomain' );
```

### Fonctions avec Échappement

```php
<?php
/**
 * Fonctions sécurisées pour l'affichage HTML
 */

// Échappe et retourne
$text = esc_html__( 'Hello World', 'my-textdomain' );
$text = esc_attr__( 'Button label', 'my-textdomain' );

// Échappe et affiche
esc_html_e( 'Hello World', 'my-textdomain' );
esc_attr_e( 'Button label', 'my-textdomain' );

// Avec contexte
$text = esc_html_x( 'Post', 'noun', 'my-textdomain' );
$text = esc_attr_x( 'Post', 'noun', 'my-textdomain' );
```

### Placeholders et Formatage

```php
<?php
/**
 * Traductions avec variables
 */

// ❌ Mauvais : concaténation
$text = __( 'Hello ', 'my-textdomain' ) . $name;

// ✅ Bon : placeholder
$text = sprintf(
    /* translators: %s: user name */
    __( 'Hello %s', 'my-textdomain' ),
    $name
);

// Plusieurs placeholders
$text = sprintf(
    /* translators: 1: user name, 2: date */
    __( 'Welcome %1$s! Last login: %2$s', 'my-textdomain' ),
    $user_name,
    $date
);

// Avec nombre
$text = sprintf(
    /* translators: %d: number of items */
    _n( '%d item in cart', '%d items in cart', $count, 'my-textdomain' ),
    $count
);
```

## Charger le Text Domain

### Plugin

```php
<?php
/**
 * Plugin Name: My Plugin
 * Text Domain: my-plugin
 * Domain Path: /languages
 */

add_action( 'init', 'my_plugin_load_textdomain' );

function my_plugin_load_textdomain() {
    load_plugin_textdomain(
        'my-plugin',
        false,
        dirname( plugin_basename( __FILE__ ) ) . '/languages'
    );
}
```

### Thème

```php
<?php
/**
 * functions.php
 */

add_action( 'after_setup_theme', 'my_theme_setup' );

function my_theme_setup() {
    // Charger les traductions du thème
    load_theme_textdomain( 'my-theme', get_template_directory() . '/languages' );

    // Pour un thème enfant
    load_child_theme_textdomain( 'my-child-theme', get_stylesheet_directory() . '/languages' );
}
```

### Block (block.json)

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/my-block",
    "title": "My Block",
    "textdomain": "my-plugin"
}
```

## Traductions JavaScript

### Enqueue avec Traductions

```php
<?php
/**
 * Charger les scripts avec traductions
 */

add_action( 'wp_enqueue_scripts', 'my_enqueue_scripts' );

function my_enqueue_scripts() {
    wp_enqueue_script(
        'my-script',
        plugins_url( 'build/index.js', __FILE__ ),
        [ 'wp-i18n' ],
        '1.0.0',
        true
    );

    // Charger les traductions JS
    wp_set_script_translations(
        'my-script',
        'my-plugin',
        plugin_dir_path( __FILE__ ) . 'languages'
    );
}
```

### Utilisation en JavaScript

```javascript
/**
 * Traductions dans les scripts JS
 */
import { __, _x, _n, _nx, sprintf } from '@wordpress/i18n';

// Traduction simple
const text = __( 'Hello World', 'my-plugin' );

// Avec contexte
const post = _x( 'Post', 'noun', 'my-plugin' );

// Singulier/Pluriel
const items = _n( '%d item', '%d items', count, 'my-plugin' );

// Avec sprintf
const greeting = sprintf(
    /* translators: %s: user name */
    __( 'Hello %s', 'my-plugin' ),
    userName
);

// Pluriel formaté
const cartItems = sprintf(
    _n( '%d item in cart', '%d items in cart', count, 'my-plugin' ),
    count
);
```

### Block avec Traductions

```jsx
/**
 * Block Gutenberg internationalisé
 */
import { __ } from '@wordpress/i18n';
import { useBlockProps, RichText } from '@wordpress/block-editor';
import { TextControl, PanelBody } from '@wordpress/components';
import { InspectorControls } from '@wordpress/block-editor';

export default function Edit( { attributes, setAttributes } ) {
    const blockProps = useBlockProps();

    return (
        <>
            <InspectorControls>
                <PanelBody title={ __( 'Settings', 'my-plugin' ) }>
                    <TextControl
                        label={ __( 'Button text', 'my-plugin' ) }
                        value={ attributes.buttonText }
                        onChange={ ( value ) => setAttributes( { buttonText: value } ) }
                        help={ __( 'Enter the button label', 'my-plugin' ) }
                    />
                </PanelBody>
            </InspectorControls>

            <div { ...blockProps }>
                <RichText
                    tagName="p"
                    placeholder={ __( 'Enter text…', 'my-plugin' ) }
                    value={ attributes.content }
                    onChange={ ( content ) => setAttributes( { content } ) }
                />
            </div>
        </>
    );
}
```

## Générer les Fichiers de Traduction

### WP-CLI

```bash
# Générer le fichier POT
wp i18n make-pot . languages/my-plugin.pot --domain=my-plugin

# Avec exclusions
wp i18n make-pot . languages/my-plugin.pot \
    --domain=my-plugin \
    --exclude=node_modules,vendor,tests

# Générer les fichiers JSON pour JS
wp i18n make-json languages/ --no-purge

# Mettre à jour les fichiers PO existants
wp i18n update-po languages/my-plugin.pot languages/
```

### package.json Scripts

```json
{
    "scripts": {
        "i18n:pot": "wp i18n make-pot . languages/my-plugin.pot --domain=my-plugin --exclude=node_modules,vendor",
        "i18n:json": "wp i18n make-json languages/ --no-purge",
        "i18n:build": "npm run i18n:pot && npm run i18n:json"
    }
}
```

### Structure des Fichiers

```
my-plugin/
├── languages/
│   ├── my-plugin.pot              # Template (source)
│   ├── my-plugin-fr_FR.po         # Traductions françaises (source)
│   ├── my-plugin-fr_FR.mo         # Traductions compilées (PHP)
│   ├── my-plugin-fr_FR-index.json # Traductions JS (build/index.js)
│   ├── my-plugin-de_DE.po
│   └── my-plugin-de_DE.mo
└── ...
```

## Fichier POT (Template)

```pot
# Copyright (C) 2024 My Company
# This file is distributed under the GPL-2.0+.
msgid ""
msgstr ""
"Project-Id-Version: My Plugin 1.0.0\n"
"Report-Msgid-Bugs-To: https://github.com/my/plugin/issues\n"
"POT-Creation-Date: 2024-01-15T10:00:00+00:00\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"

#: src/index.js:10
msgid "Hello World"
msgstr ""

#. translators: %s: user name
#: src/components/Greeting.js:15
msgid "Hello %s"
msgstr ""

#: src/components/Cart.js:20
msgid "%d item"
msgid_plural "%d items"
msgstr[0] ""
msgstr[1] ""

#. translators: This is used as a noun, not a verb
#: src/admin/PostList.js:30
msgctxt "noun"
msgid "Post"
msgstr ""
```

## Fichier PO (Traduction)

```po
# French translations for My Plugin
# Copyright (C) 2024 My Company
msgid ""
msgstr ""
"Project-Id-Version: My Plugin 1.0.0\n"
"Report-Msgid-Bugs-To: https://github.com/my/plugin/issues\n"
"POT-Creation-Date: 2024-01-15T10:00:00+00:00\n"
"PO-Revision-Date: 2024-01-16T14:30:00+01:00\n"
"Last-Translator: Jean Dupont <jean@example.com>\n"
"Language-Team: French <fr@li.org>\n"
"Language: fr_FR\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\n"

#: src/index.js:10
msgid "Hello World"
msgstr "Bonjour le monde"

#. translators: %s: user name
#: src/components/Greeting.js:15
msgid "Hello %s"
msgstr "Bonjour %s"

#: src/components/Cart.js:20
msgid "%d item"
msgid_plural "%d items"
msgstr[0] "%d article"
msgstr[1] "%d articles"

#. translators: This is used as a noun, not a verb
#: src/admin/PostList.js:30
msgctxt "noun"
msgid "Post"
msgstr "Article"
```

## Intégration WPML

```php
<?php
/**
 * Rendre du contenu custom traduisible avec WPML
 */

// Enregistrer des chaînes pour la traduction
add_action( 'init', 'my_register_wpml_strings' );

function my_register_wpml_strings() {
    if ( function_exists( 'icl_register_string' ) ) {
        // Enregistrer une option
        $footer_text = get_option( 'my_footer_text' );
        icl_register_string( 'my-plugin', 'Footer Text', $footer_text );
    }
}

// Récupérer la traduction
function my_get_footer_text() {
    $text = get_option( 'my_footer_text' );

    if ( function_exists( 'icl_t' ) ) {
        return icl_t( 'my-plugin', 'Footer Text', $text );
    }

    return $text;
}

// CPT traduisible
add_filter( 'wpml_is_translated_post_type', 'my_translate_cpt', 10, 2 );

function my_translate_cpt( $translate, $post_type ) {
    if ( $post_type === 'portfolio' ) {
        return true;
    }
    return $translate;
}
```

## Intégration Polylang

```php
<?php
/**
 * Rendre du contenu custom traduisible avec Polylang
 */

// Enregistrer des chaînes
add_action( 'init', 'my_register_polylang_strings' );

function my_register_polylang_strings() {
    if ( function_exists( 'pll_register_string' ) ) {
        pll_register_string( 'footer-text', get_option( 'my_footer_text' ), 'My Plugin' );
        pll_register_string( 'copyright', get_option( 'my_copyright' ), 'My Plugin' );
    }
}

// Récupérer la traduction
function my_get_footer_text() {
    $text = get_option( 'my_footer_text' );

    if ( function_exists( 'pll__' ) ) {
        return pll__( $text );
    }

    return $text;
}

// Récupérer la langue courante
function my_get_current_lang() {
    if ( function_exists( 'pll_current_language' ) ) {
        return pll_current_language();
    }
    return get_locale();
}

// URL traduite
function my_get_translated_url( $url, $lang ) {
    if ( function_exists( 'pll_the_languages' ) ) {
        $translations = pll_the_languages( [ 'raw' => 1 ] );
        if ( isset( $translations[ $lang ]['url'] ) ) {
            return $translations[ $lang ]['url'];
        }
    }
    return $url;
}
```

## Commentaires pour Traducteurs

```php
<?php
/**
 * Commentaires pour aider les traducteurs
 */

// Commentaire simple
/* translators: %s: user name */
$greeting = sprintf( __( 'Hello %s!', 'my-plugin' ), $user_name );

// Commentaire avec contexte
/* translators: This appears in the page header */
$title = __( 'Welcome', 'my-plugin' );

// Plusieurs placeholders
/* translators: 1: number of posts, 2: category name */
$message = sprintf(
    __( 'Found %1$d posts in %2$s', 'my-plugin' ),
    $count,
    $category
);

// Longueur recommandée
/* translators: Keep this under 20 characters for button width */
$button_text = __( 'Submit', 'my-plugin' );

// Format de date
/* translators: Date format, see https://www.php.net/manual/en/datetime.format.php */
$date_format = __( 'F j, Y', 'my-plugin' );
```

## RTL (Right-to-Left) Support

```css
/* Styles RTL automatiques */

/* Style de base */
.my-component {
    margin-left: 20px;
    text-align: left;
    padding: 10px 20px 10px 10px;
}

/* Avec propriétés logiques (recommandé) */
.my-component {
    margin-inline-start: 20px;
    text-align: start;
    padding-block: 10px;
    padding-inline-start: 10px;
    padding-inline-end: 20px;
}
```

```php
<?php
/**
 * Charger une feuille de style RTL
 */

add_action( 'wp_enqueue_scripts', 'my_enqueue_styles' );

function my_enqueue_styles() {
    wp_enqueue_style( 'my-style', get_stylesheet_uri() );

    // WordPress charge automatiquement style-rtl.css si is_rtl()
    wp_style_add_data( 'my-style', 'rtl', 'replace' );
}
```

## Bonnes Pratiques

### 1. Ne Jamais Traduire

```php
<?php
// ❌ Ne pas traduire
// - Slugs, clés, identifiants
// - Noms de fonctions, hooks
// - Messages de log/debug
// - Données de la BDD

register_post_type( 'portfolio', [ // ❌ pas de traduction du slug
    'labels' => [
        'name' => __( 'Portfolios', 'my-plugin' ), // ✅ traduire les labels
    ],
]);
```

### 2. Text Domain Cohérent

```php
<?php
// ✅ Utiliser le même text domain partout
__( 'Hello', 'my-plugin' );
_e( 'World', 'my-plugin' );

// ❌ Éviter les incohérences
__( 'Hello', 'my-plugin' );
_e( 'World', 'myplugin' ); // Différent!
```

### 3. Phrases Complètes

```php
<?php
// ❌ Mauvais : fragments
echo __( 'Click', 'my-plugin' ) . ' ' . __( 'here', 'my-plugin' );

// ✅ Bon : phrase complète
echo __( 'Click here', 'my-plugin' );

// ✅ Avec placeholder si nécessaire
printf(
    /* translators: %s: link */
    __( 'Click %s to continue', 'my-plugin' ),
    '<a href="#">' . __( 'here', 'my-plugin' ) . '</a>'
);
```

### 4. Éviter les Variables dans les Chaînes

```php
<?php
// ❌ Mauvais : variable dans la chaîne (ne sera pas extrait)
$type = 'post';
__( "Edit $type", 'my-plugin' );

// ✅ Bon : placeholder
sprintf( __( 'Edit %s', 'my-plugin' ), $type );
```

## Checklist i18n

- [ ] Text domain défini dans le header du plugin/thème
- [ ] Text domain chargé avec `load_plugin_textdomain()` ou `load_theme_textdomain()`
- [ ] Toutes les chaînes utilisateur utilisent `__()`, `_e()`, etc.
- [ ] Les chaînes HTML utilisent `esc_html__()`, `esc_attr__()`
- [ ] Les placeholders sont documentés avec des commentaires traducteurs
- [ ] `wp_set_script_translations()` pour les scripts JS
- [ ] Fichier POT généré avec `wp i18n make-pot`
- [ ] Fichiers JSON générés pour JS avec `wp i18n make-json`
- [ ] Support RTL avec propriétés CSS logiques
- [ ] Pas de concaténation de chaînes traduites

## Livrables

| Livrable | Description |
|----------|-------------|
| Internationalized code | Code PHP/JS avec fonctions de traduction (__(), _e(), etc.) |
| POT file | Fichier template .pot généré avec wp-cli |
| Translation files | Fichiers .po et .mo pour langues supportées |
| JSON translations | Fichiers JSON pour traductions JavaScript |
| RTL styles | Feuilles de style RTL si applicable |
| Translation guide | Guide pour traducteurs et processus de localisation |
