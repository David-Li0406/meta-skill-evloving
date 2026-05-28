# Guide de Dépannage

Ce guide couvre les problèmes courants rencontrés lors du développement WordPress et Gutenberg.

## Table des Matières

1. [Problèmes Gutenberg / Blocks](#problèmes-gutenberg--blocks)
2. [Problèmes PHP / WordPress Core](#problèmes-php--wordpress-core)
3. [Problèmes de Build / Tooling](#problèmes-de-build--tooling)
4. [Problèmes REST API](#problèmes-rest-api)
5. [Problèmes de Performance](#problèmes-de-performance)
6. [Problèmes d'Environnement](#problèmes-denvironnement)

---

## Problèmes Gutenberg / Blocks

### Le block n'apparaît pas dans l'éditeur

**Symptômes** : Le block est enregistré mais invisible dans l'inserter.

**Causes possibles** :

1. **Script non chargé**

```php
// Vérifier que le script est enqueued
add_action( 'enqueue_block_editor_assets', function() {
    wp_enqueue_script(
        'my-block',
        plugins_url( 'build/index.js', __FILE__ ),
        array( 'wp-blocks', 'wp-element', 'wp-editor' ),
        filemtime( plugin_dir_path( __FILE__ ) . 'build/index.js' )
    );
} );
```

2. **Erreur JavaScript** - Ouvrir la console du navigateur (F12)

3. **Mauvaise catégorie**

```js
// Vérifier que la catégorie existe
registerBlockType( 'my-plugin/my-block', {
    category: 'widgets', // Utiliser une catégorie existante
} );
```

4. **Post type non supporté**

```js
// Le block est limité à certains post types
supports: {
    inserter: true, // Doit être true
},
```

### Erreur "Block validation failed"

**Symptômes** : Message d'erreur dans l'éditeur, block invalide.

**Causes** :

1. **Différence save() vs rendu** - Le HTML sauvegardé ne correspond pas

```js
// Le save() doit produire exactement le même HTML
save: ( { attributes } ) => {
    // Utiliser les mêmes classes, attributs, structure
    return <div className="my-block">{ attributes.content }</div>;
},
```

2. **Attribut modifié sans migration**

```js
// Ajouter une migration pour les anciennes versions
deprecated: [
    {
        attributes: { /* anciens attributs */ },
        save: ( { attributes } ) => { /* ancien save */ },
        migrate: ( attributes ) => {
            return { ...attributes, newAttr: 'default' };
        },
    },
],
```

### useSelect retourne undefined

**Symptômes** : Les données sont undefined malgré un sélecteur correct.

**Solutions** :

```js
// 1. Vérifier le nom du store
const post = useSelect( ( select ) => {
    return select( 'core/editor' ).getCurrentPost(); // Pas 'editor'
} );

// 2. Gérer le chargement
const { post, isLoading } = useSelect( ( select ) => {
    const { getEntityRecord, isResolving } = select( 'core' );
    return {
        post: getEntityRecord( 'postType', 'post', postId ),
        isLoading: isResolving( 'getEntityRecord', [ 'postType', 'post', postId ] ),
    };
} );

if ( isLoading ) return <Spinner />;
```

### InnerBlocks ne sauvegarde pas

**Symptômes** : Les blocks enfants disparaissent après sauvegarde.

**Solution** :

```js
// save() doit inclure InnerBlocks.Content
save: () => {
    return (
        <div className="my-wrapper">
            <InnerBlocks.Content />
        </div>
    );
},
```

---

## Problèmes PHP / WordPress Core

### Hook non déclenché

**Symptômes** : Le callback n'est jamais exécuté.

**Vérifications** :

```php
// 1. Vérifier le timing
add_action( 'init', 'my_function' ); // OK
add_action( 'init', 'my_function', 10, 2 ); // Avec priorité et args

// 2. Vérifier que le hook existe
if ( has_action( 'my_custom_hook' ) ) {
    // Hook enregistré
}

// 3. Vérifier l'ordre d'exécution
add_action( 'plugins_loaded', function() {
    // S'assurer que le plugin ciblé est chargé
    if ( function_exists( 'other_plugin_function' ) ) {
        // ...
    }
} );

// 4. Debug - lister les callbacks
global $wp_filter;
var_dump( $wp_filter['init'] );
```

### Nonce invalide

**Symptômes** : "Security check failed" ou formulaire rejeté.

**Causes** :

```php
// 1. Action différente
wp_nonce_field( 'my_action', 'my_nonce' ); // Création
wp_verify_nonce( $_POST['my_nonce'], 'my_action' ); // Vérification - MÊME action

// 2. Nonce expiré (24h par défaut)
// Régénérer le nonce à chaque chargement de page

// 3. Cache de page
// Les nonces ne fonctionnent pas avec le cache de page complet
// Utiliser AJAX pour les formulaires sur pages cachées
```

### Meta non sauvegardée

**Symptômes** : `update_post_meta` semble fonctionner mais la valeur est vide.

**Vérifications** :

```php
// 1. Vérifier autosave
if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
    return; // Ne pas sauvegarder pendant autosave
}

// 2. Vérifier les permissions
if ( ! current_user_can( 'edit_post', $post_id ) ) {
    return;
}

// 3. Vérifier le nom du champ
if ( isset( $_POST['my_field'] ) ) { // Vérifier le name=""
    update_post_meta( $post_id, '_my_meta', sanitize_text_field( $_POST['my_field'] ) );
}

// 4. Vérifier si la meta est protégée
// Les meta commençant par _ sont "protected"
// Utiliser show_in_rest et auth_callback pour REST API
```

### CPT non accessible (404)

**Symptômes** : Les pages du CPT retournent 404.

**Solutions** :

```php
// 1. Flush les rewrite rules
// Après avoir modifié les rewrite rules, aller dans
// Réglages > Permaliens et cliquer "Enregistrer"

// Ou via code (seulement à l'activation du plugin)
register_activation_hook( __FILE__, function() {
    my_register_cpt();
    flush_rewrite_rules();
} );

// 2. Vérifier public et publicly_queryable
register_post_type( 'book', array(
    'public'             => true,
    'publicly_queryable' => true, // Doit être true pour les URLs
    'rewrite'            => array( 'slug' => 'books' ),
) );
```

---

## Problèmes de Build / Tooling

### npm run build échoue

**Erreurs courantes** :

```bash
# 1. Node version incorrecte
node -v  # Vérifier la version
nvm use 20  # Utiliser Node 20

# 2. Dépendances manquantes
rm -rf node_modules package-lock.json
npm install

# 3. Erreur de syntaxe JSX
# Vérifier que les fichiers ont l'extension .js ou .jsx
# et que @wordpress/scripts est installé

# 4. Import manquant
# Error: Cannot find module '@wordpress/blocks'
npm install @wordpress/blocks --save
```

### wp-env ne démarre pas

**Solutions** :

```bash
# 1. Docker non démarré
docker info  # Vérifier que Docker tourne

# 2. Ports utilisés
docker ps  # Voir les containers
# Changer le port dans .wp-env.json
{
    "port": 8889
}

# 3. Reset complet
wp-env destroy
wp-env start

# 4. Logs
wp-env logs
```

### Erreur "wp-scripts: command not found"

```bash
# 1. Installation locale
npm install @wordpress/scripts --save-dev

# 2. Utiliser npx
npx wp-scripts build

# 3. Ou dans package.json
{
    "scripts": {
        "build": "wp-scripts build"
    }
}
```

---

## Problèmes REST API

### Erreur 401 Unauthorized

```php
// 1. Vérifier l'authentification
// Pour les endpoints protégés, utiliser le nonce
wp_localize_script( 'my-script', 'wpApiSettings', array(
    'root'  => esc_url_raw( rest_url() ),
    'nonce' => wp_create_nonce( 'wp_rest' ),
) );

// JavaScript
fetch( wpApiSettings.root + 'wp/v2/posts', {
    headers: {
        'X-WP-Nonce': wpApiSettings.nonce,
    },
} );
```

### Erreur 403 Forbidden

```php
// 1. Vérifier permission_callback
register_rest_route( 'my-plugin/v1', '/data', array(
    'methods'             => 'GET',
    'callback'            => 'my_callback',
    'permission_callback' => function() {
        return current_user_can( 'edit_posts' );
        // Ou pour accès public :
        // return true;
    },
) );

// 2. Pour les utilisateurs non connectés
'permission_callback' => '__return_true', // Endpoint public
```

### Champ custom non visible dans REST

```php
// 1. Pour les post meta
register_post_meta( 'post', 'my_meta', array(
    'show_in_rest' => true,  // Requis !
    'single'       => true,
    'type'         => 'string',
) );

// 2. Pour les CPT
register_post_type( 'book', array(
    'show_in_rest' => true,  // Requis !
    'rest_base'    => 'books',
) );

// 3. Pour les taxonomies
register_taxonomy( 'genre', 'book', array(
    'show_in_rest' => true,  // Requis !
) );
```

---

## Problèmes de Performance

### Éditeur lent

**Optimisations** :

```js
// 1. Mémoriser les sélecteurs
const posts = useSelect(
    ( select ) => select( 'core' ).getEntityRecords( 'postType', 'post' ),
    [] // Dépendances vides = ne recalcule pas
);

// 2. Éviter les re-renders
const MemoizedComponent = memo( MyComponent );

// 3. Charger les données en lazy
const { data, isLoading } = useSelect( ( select ) => {
    // Ne charger que si nécessaire
    if ( ! shouldLoad ) return { data: null, isLoading: false };
    // ...
} );
```

### Requêtes SQL lentes

```php
// 1. Utiliser le cache
$cached = wp_cache_get( 'my_data', 'my_plugin' );
if ( false === $cached ) {
    $cached = expensive_query();
    wp_cache_set( 'my_data', $cached, 'my_plugin', 3600 );
}

// 2. Limiter les requêtes
$query = new WP_Query( array(
    'posts_per_page' => 10,      // Pas -1 !
    'no_found_rows'  => true,    // Désactiver le comptage total
    'fields'         => 'ids',   // Si seuls les IDs sont nécessaires
) );

// 3. Éviter les meta_query non indexées
// Créer une table custom pour les données fréquemment requêtées
```

---

## Problèmes d'Environnement

### Différences Local / Staging / Production

**Checklist** :

```php
// 1. Constantes d'environnement
if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    // Code de debug uniquement
}

// 2. URLs absolues dans la BDD
// Utiliser WP-CLI pour rechercher/remplacer
wp search-replace 'http://local.test' 'https://production.com' --dry-run

// 3. Permissions fichiers
// Local : 755/644
// Serveur : parfois plus restrictif

// 4. PHP version
phpinfo(); // Vérifier la version
```

### Erreurs après mise à jour WordPress

```php
// 1. Vider les caches
wp cache flush

// 2. Vérifier les dépréciations
// Activer WP_DEBUG et WP_DEBUG_LOG
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );

// 3. Consulter debug.log
tail -f wp-content/debug.log

// 4. Désactiver les plugins un par un
wp plugin deactivate --all
wp plugin activate plugin-name
```

---

## Outils de Diagnostic

### Query Monitor

```php
// Plugin pour analyser :
// - Requêtes SQL
// - Hooks exécutés
// - Erreurs PHP
// - Performance
// https://wordpress.org/plugins/query-monitor/
```

### Debug Bar

```php
// Informations de debug dans la admin bar
// https://wordpress.org/plugins/debug-bar/
```

### WP-CLI Debug

```bash
# Vérifier l'installation
wp core verify-checksums

# Lister les erreurs de transients
wp transient list --expired

# Vérifier la config
wp config list

# Réparer la BDD
wp db repair
```

---

## Ressources

- [WordPress Debugging](https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/)
- [Block Editor Handbook - Troubleshooting](https://developer.wordpress.org/block-editor/contributors/develop/troubleshooting/)
- [WP-CLI Commands](https://developer.wordpress.org/cli/commands/)
