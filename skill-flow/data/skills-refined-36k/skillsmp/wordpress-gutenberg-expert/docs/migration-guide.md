# Guide de Migration

Ce guide aide à migrer les anciens patterns WordPress vers les approches modernes.

## Table des Matières

1. [Classic Theme → Block Theme](#classic-theme--block-theme)
2. [Shortcodes → Blocks](#shortcodes--blocks)
3. [Widgets → Blocks](#widgets--blocks)
4. [Meta Boxes → Sidebar Panels](#meta-boxes--sidebar-panels)
5. [AJAX → REST API](#ajax--rest-api)
6. [jQuery → Vanilla JS / React](#jquery--vanilla-js--react)
7. [Options Page → Settings API moderne](#options-page--settings-api-moderne)
8. [Custom Fields → Block Attributes](#custom-fields--block-attributes)

---

## Classic Theme → Block Theme

### Structure des fichiers

**Avant (Classic Theme)** :

```
theme/
├── header.php
├── footer.php
├── sidebar.php
├── index.php
├── single.php
├── page.php
├── functions.php
└── style.css
```

**Après (Block Theme)** :

```
theme/
├── parts/
│   ├── header.html
│   ├── footer.html
│   └── sidebar.html
├── templates/
│   ├── index.html
│   ├── single.html
│   └── page.html
├── patterns/
│   └── hero.php
├── styles/
│   └── dark.json
├── functions.php
├── style.css
└── theme.json
```

### Migration du Header

**Avant** (`header.php`) :

```php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo( 'charset' ); ?>">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<header class="site-header">
    <div class="logo">
        <?php the_custom_logo(); ?>
        <h1><?php bloginfo( 'name' ); ?></h1>
    </div>
    <nav>
        <?php wp_nav_menu( array( 'theme_location' => 'primary' ) ); ?>
    </nav>
</header>
```

**Après** (`parts/header.html`) :

```html
<!-- wp:group {"tagName":"header","className":"site-header","layout":{"type":"constrained"}} -->
<header class="wp-block-group site-header">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:site-logo /-->
        <!-- wp:site-title /-->
    </div>
    <!-- /wp:group -->
    <!-- wp:navigation {"ref":123} /-->
</header>
<!-- /wp:group -->
```

### Migration des Styles

**Avant** (`style.css` + `functions.php`) :

```css
/* style.css */
:root {
    --primary-color: #0073aa;
    --secondary-color: #23282d;
}
.site-header { padding: 20px; }
```

```php
// functions.php
function theme_customize_register( $wp_customize ) {
    $wp_customize->add_setting( 'primary_color', array(
        'default' => '#0073aa',
    ) );
    // ...
}
```

**Après** (`theme.json`) :

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "settings": {
        "color": {
            "palette": [
                { "slug": "primary", "color": "#0073aa", "name": "Primary" },
                { "slug": "secondary", "color": "#23282d", "name": "Secondary" }
            ]
        }
    },
    "styles": {
        "blocks": {
            "core/group": {
                "spacing": {
                    "padding": { "top": "20px", "bottom": "20px" }
                }
            }
        }
    }
}
```

---

## Shortcodes → Blocks

### Shortcode Simple

**Avant** :

```php
// Shortcode [my_button text="Click" url="#"]
add_shortcode( 'my_button', function( $atts ) {
    $atts = shortcode_atts( array(
        'text' => 'Button',
        'url'  => '#',
    ), $atts );

    return sprintf(
        '<a href="%s" class="my-button">%s</a>',
        esc_url( $atts['url'] ),
        esc_html( $atts['text'] )
    );
} );
```

**Après** (Block) :

`block.json` :

```json
{
    "apiVersion": 3,
    "name": "my-plugin/button",
    "title": "My Button",
    "category": "widgets",
    "attributes": {
        "text": { "type": "string", "default": "Button" },
        "url": { "type": "string", "default": "#" }
    }
}
```

`edit.js` :

```jsx
import { RichText, URLInput } from '@wordpress/block-editor';

export default function Edit( { attributes, setAttributes } ) {
    return (
        <>
            <RichText
                tagName="span"
                value={ attributes.text }
                onChange={ ( text ) => setAttributes( { text } ) }
            />
            <URLInput
                value={ attributes.url }
                onChange={ ( url ) => setAttributes( { url } ) }
            />
        </>
    );
}
```

`save.js` :

```jsx
import { RichText } from '@wordpress/block-editor';

export default function Save( { attributes } ) {
    return (
        <a href={ attributes.url } className="my-button">
            <RichText.Content value={ attributes.text } />
        </a>
    );
}
```

### Shortcode avec Contenu Imbriqué

**Avant** :

```php
// [my_box title="Title"]Content[/my_box]
add_shortcode( 'my_box', function( $atts, $content ) {
    $atts = shortcode_atts( array( 'title' => '' ), $atts );
    return sprintf(
        '<div class="my-box"><h3>%s</h3><div>%s</div></div>',
        esc_html( $atts['title'] ),
        do_shortcode( $content )
    );
} );
```

**Après** (Block avec InnerBlocks) :

```jsx
import { InnerBlocks, RichText } from '@wordpress/block-editor';

export function Edit( { attributes, setAttributes } ) {
    return (
        <div className="my-box">
            <RichText
                tagName="h3"
                value={ attributes.title }
                onChange={ ( title ) => setAttributes( { title } ) }
            />
            <InnerBlocks />
        </div>
    );
}

export function Save( { attributes } ) {
    return (
        <div className="my-box">
            <RichText.Content tagName="h3" value={ attributes.title } />
            <InnerBlocks.Content />
        </div>
    );
}
```

### Transformer Shortcode en Block

```jsx
// Permettre la conversion automatique
transforms: {
    from: [
        {
            type: 'shortcode',
            tag: 'my_button',
            attributes: {
                text: {
                    type: 'string',
                    shortcode: ( { named: { text } } ) => text,
                },
                url: {
                    type: 'string',
                    shortcode: ( { named: { url } } ) => url,
                },
            },
        },
    ],
},
```

---

## Widgets → Blocks

### Widget Simple

**Avant** :

```php
class My_Widget extends WP_Widget {
    public function __construct() {
        parent::__construct( 'my_widget', 'My Widget' );
    }

    public function widget( $args, $instance ) {
        echo $args['before_widget'];
        echo '<h3>' . esc_html( $instance['title'] ) . '</h3>';
        echo '<p>' . esc_html( $instance['content'] ) . '</p>';
        echo $args['after_widget'];
    }

    public function form( $instance ) {
        ?>
        <p>
            <label>Title:</label>
            <input type="text" name="<?php echo $this->get_field_name( 'title' ); ?>"
                   value="<?php echo esc_attr( $instance['title'] ); ?>">
        </p>
        <?php
    }

    public function update( $new_instance, $old_instance ) {
        return array(
            'title'   => sanitize_text_field( $new_instance['title'] ),
            'content' => sanitize_textarea_field( $new_instance['content'] ),
        );
    }
}
```

**Après** (Block) :

```jsx
// Le block peut être utilisé dans les zones de widgets
registerBlockType( 'my-plugin/info-box', {
    title: 'Info Box',
    category: 'widgets',
    attributes: {
        title: { type: 'string' },
        content: { type: 'string' },
    },
    edit: ( { attributes, setAttributes } ) => (
        <div className="info-box">
            <RichText
                tagName="h3"
                value={ attributes.title }
                onChange={ ( title ) => setAttributes( { title } ) }
            />
            <RichText
                tagName="p"
                value={ attributes.content }
                onChange={ ( content ) => setAttributes( { content } ) }
            />
        </div>
    ),
    save: ( { attributes } ) => (
        <div className="info-box">
            <RichText.Content tagName="h3" value={ attributes.title } />
            <RichText.Content tagName="p" value={ attributes.content } />
        </div>
    ),
} );
```

---

## Meta Boxes → Sidebar Panels

### Meta Box Classique

**Avant** :

```php
add_action( 'add_meta_boxes', function() {
    add_meta_box( 'my_meta', 'My Meta', 'render_my_meta', 'post' );
} );

function render_my_meta( $post ) {
    $value = get_post_meta( $post->ID, '_my_meta', true );
    wp_nonce_field( 'my_meta_action', 'my_meta_nonce' );
    ?>
    <input type="text" name="my_meta" value="<?php echo esc_attr( $value ); ?>">
    <?php
}

add_action( 'save_post', function( $post_id ) {
    if ( ! wp_verify_nonce( $_POST['my_meta_nonce'], 'my_meta_action' ) ) return;
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;

    update_post_meta( $post_id, '_my_meta', sanitize_text_field( $_POST['my_meta'] ) );
} );
```

**Après** (Sidebar Panel) :

`PHP - Enregistrer la meta` :

```php
register_post_meta( 'post', '_my_meta', array(
    'show_in_rest'  => true,
    'single'        => true,
    'type'          => 'string',
    'auth_callback' => function() {
        return current_user_can( 'edit_posts' );
    },
) );
```

`JavaScript - Panel` :

```jsx
import { PluginDocumentSettingPanel } from '@wordpress/edit-post';
import { TextControl } from '@wordpress/components';
import { useSelect, useDispatch } from '@wordpress/data';
import { useEntityProp } from '@wordpress/core-data';

function MyMetaPanel() {
    const postType = useSelect( ( select ) =>
        select( 'core/editor' ).getCurrentPostType()
    );

    const [ meta, setMeta ] = useEntityProp( 'postType', postType, 'meta' );

    return (
        <PluginDocumentSettingPanel
            name="my-meta-panel"
            title="My Meta"
        >
            <TextControl
                label="Value"
                value={ meta._my_meta || '' }
                onChange={ ( value ) => setMeta( { ...meta, _my_meta: value } ) }
            />
        </PluginDocumentSettingPanel>
    );
}

registerPlugin( 'my-meta-panel', { render: MyMetaPanel } );
```

---

## AJAX → REST API

### AJAX Classique

**Avant** :

```php
// PHP
add_action( 'wp_ajax_get_data', 'ajax_get_data' );
add_action( 'wp_ajax_nopriv_get_data', 'ajax_get_data' );

function ajax_get_data() {
    check_ajax_referer( 'my_nonce', 'nonce' );
    $data = get_option( 'my_data' );
    wp_send_json_success( $data );
}

// JavaScript
jQuery.ajax( {
    url: ajaxurl,
    type: 'POST',
    data: {
        action: 'get_data',
        nonce: myAjax.nonce,
    },
    success: function( response ) {
        console.log( response.data );
    },
} );
```

**Après** (REST API) :

```php
// PHP
add_action( 'rest_api_init', function() {
    register_rest_route( 'my-plugin/v1', '/data', array(
        'methods'             => 'GET',
        'callback'            => 'rest_get_data',
        'permission_callback' => '__return_true', // ou fonction de permission
    ) );
} );

function rest_get_data() {
    return rest_ensure_response( get_option( 'my_data' ) );
}
```

```js
// JavaScript moderne
const response = await fetch( '/wp-json/my-plugin/v1/data', {
    headers: {
        'X-WP-Nonce': wpApiSettings.nonce,
    },
} );
const data = await response.json();
```

```jsx
// Dans un block avec @wordpress/api-fetch
import apiFetch from '@wordpress/api-fetch';

const data = await apiFetch( { path: '/my-plugin/v1/data' } );
```

---

## jQuery → Vanilla JS / React

### Manipulation DOM

**Avant** (jQuery) :

```js
jQuery( document ).ready( function( $ ) {
    $( '.my-button' ).on( 'click', function() {
        $( this ).addClass( 'active' );
        $( '.my-content' ).slideToggle();
    } );
} );
```

**Après** (Vanilla JS) :

```js
document.addEventListener( 'DOMContentLoaded', () => {
    document.querySelectorAll( '.my-button' ).forEach( ( button ) => {
        button.addEventListener( 'click', () => {
            button.classList.add( 'active' );
            const content = document.querySelector( '.my-content' );
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        } );
    } );
} );
```

**Après** (Interactivity API) :

```html
<!-- view.html -->
<div data-wp-interactive="my-plugin">
    <button data-wp-on--click="actions.toggle" data-wp-class--active="state.isActive">
        Toggle
    </button>
    <div data-wp-bind--hidden="!state.isOpen" class="my-content">
        Content
    </div>
</div>
```

```js
// view.js
import { store } from '@wordpress/interactivity';

store( 'my-plugin', {
    state: {
        isActive: false,
        isOpen: false,
    },
    actions: {
        toggle() {
            const context = getContext();
            context.isActive = ! context.isActive;
            context.isOpen = ! context.isOpen;
        },
    },
} );
```

---

## Options Page → Settings API moderne

### Page d'Options Classique

**Avant** :

```php
add_action( 'admin_menu', function() {
    add_options_page( 'My Settings', 'My Plugin', 'manage_options', 'my-settings', 'render_settings' );
} );

function render_settings() {
    ?>
    <form method="post" action="options.php">
        <?php settings_fields( 'my_options' ); ?>
        <table class="form-table">
            <tr>
                <th>Option 1</th>
                <td><input type="text" name="my_option_1" value="<?php echo get_option( 'my_option_1' ); ?>"></td>
            </tr>
        </table>
        <?php submit_button(); ?>
    </form>
    <?php
}

add_action( 'admin_init', function() {
    register_setting( 'my_options', 'my_option_1' );
} );
```

**Après** (React Settings Page) :

`PHP` :

```php
add_action( 'admin_menu', function() {
    add_options_page( 'My Settings', 'My Plugin', 'manage_options', 'my-settings', function() {
        echo '<div id="my-settings-root"></div>';
    } );
} );

add_action( 'admin_enqueue_scripts', function( $hook ) {
    if ( 'settings_page_my-settings' !== $hook ) return;

    wp_enqueue_script( 'my-settings', plugin_dir_url( __FILE__ ) . 'build/settings.js', array( 'wp-element', 'wp-components', 'wp-api-fetch' ), '1.0', true );
} );

// REST endpoint pour les options
add_action( 'rest_api_init', function() {
    register_rest_route( 'my-plugin/v1', '/settings', array(
        array(
            'methods'             => 'GET',
            'callback'            => function() {
                return array( 'option1' => get_option( 'my_option_1' ) );
            },
            'permission_callback' => function() {
                return current_user_can( 'manage_options' );
            },
        ),
        array(
            'methods'             => 'POST',
            'callback'            => function( $request ) {
                update_option( 'my_option_1', sanitize_text_field( $request['option1'] ) );
                return array( 'success' => true );
            },
            'permission_callback' => function() {
                return current_user_can( 'manage_options' );
            },
        ),
    ) );
} );
```

`JavaScript (settings.js)` :

```jsx
import { useState, useEffect } from '@wordpress/element';
import { TextControl, Button, Panel, PanelBody } from '@wordpress/components';
import apiFetch from '@wordpress/api-fetch';
import { createRoot } from '@wordpress/element';

function SettingsPage() {
    const [ option1, setOption1 ] = useState( '' );
    const [ isSaving, setIsSaving ] = useState( false );

    useEffect( () => {
        apiFetch( { path: '/my-plugin/v1/settings' } ).then( ( data ) => {
            setOption1( data.option1 || '' );
        } );
    }, [] );

    const saveSettings = async () => {
        setIsSaving( true );
        await apiFetch( {
            path: '/my-plugin/v1/settings',
            method: 'POST',
            data: { option1 },
        } );
        setIsSaving( false );
    };

    return (
        <Panel>
            <PanelBody title="Settings">
                <TextControl
                    label="Option 1"
                    value={ option1 }
                    onChange={ setOption1 }
                />
                <Button isPrimary onClick={ saveSettings } isBusy={ isSaving }>
                    Save
                </Button>
            </PanelBody>
        </Panel>
    );
}

createRoot( document.getElementById( 'my-settings-root' ) ).render( <SettingsPage /> );
```

---

## Custom Fields → Block Attributes

### ACF / Custom Fields → Attributs de Block

**Avant** (ACF) :

```php
// Affichage dans template
$hero_title = get_field( 'hero_title' );
$hero_image = get_field( 'hero_image' );
?>
<div class="hero" style="background-image: url(<?php echo $hero_image; ?>)">
    <h1><?php echo $hero_title; ?></h1>
</div>
```

**Après** (Block Pattern ou Block Custom) :

`Pattern` :

```php
<!-- wp:cover {"url":"<?php echo esc_url( get_theme_file_uri( 'assets/hero.jpg' ) ); ?>","dimRatio":50} -->
<div class="wp-block-cover">
    <span class="wp-block-cover__background"></span>
    <img class="wp-block-cover__image-background" src="..."/>
    <div class="wp-block-cover__inner-container">
        <!-- wp:heading {"level":1} -->
        <h1>Hero Title</h1>
        <!-- /wp:heading -->
    </div>
</div>
<!-- /wp:cover -->
```

`Block Custom` :

```jsx
registerBlockType( 'my-theme/hero', {
    attributes: {
        title: { type: 'string' },
        imageUrl: { type: 'string' },
        imageId: { type: 'number' },
    },
    edit: ( { attributes, setAttributes } ) => {
        const { title, imageUrl, imageId } = attributes;

        return (
            <div className="hero" style={ { backgroundImage: `url(${ imageUrl })` } }>
                <MediaUpload
                    onSelect={ ( media ) => setAttributes( { imageUrl: media.url, imageId: media.id } ) }
                    value={ imageId }
                    render={ ( { open } ) => (
                        <Button onClick={ open }>Select Image</Button>
                    ) }
                />
                <RichText
                    tagName="h1"
                    value={ title }
                    onChange={ ( title ) => setAttributes( { title } ) }
                />
            </div>
        );
    },
} );
```

---

## Checklist de Migration

### Avant de migrer

- [ ] Sauvegarder la base de données
- [ ] Lister toutes les fonctionnalités à migrer
- [ ] Identifier les dépendances (plugins, thèmes)
- [ ] Créer un environnement de test

### Pendant la migration

- [ ] Migrer progressivement (pas tout d'un coup)
- [ ] Tester chaque fonctionnalité migrée
- [ ] Maintenir la rétrocompatibilité si nécessaire
- [ ] Documenter les changements

### Après la migration

- [ ] Tests complets (fonctionnels, visuels, performance)
- [ ] Mettre à jour la documentation
- [ ] Former les utilisateurs si nécessaire
- [ ] Planifier la suppression du code legacy
