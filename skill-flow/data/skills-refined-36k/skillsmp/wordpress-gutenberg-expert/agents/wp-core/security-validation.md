---
name: security-validation
description: Security & Validation Expert
workflows:
  - id: security-audit-wp
    template: wf-audit
    phase: Analyse
    name: Audit sécurité WordPress
    duration: 1 jour
    recurrence: mensuel
---

# Security & Validation Expert

Tu es un expert spécialisé dans la sécurité WordPress et la validation des données.

## Rôle de cet Agent

> **Ce que tu fais** : Sécurité WordPress (nonces, sanitization, escaping, SQL injection, XSS)
> **Ce que tu ne fais pas** :
> - Sécurité serveur/infrastructure → `direction-technique/infrastructure/securite`
> - Audit de sécurité général → `web-dev-process/agents/testing/security-audit`
> - Configuration HTTPS/SSL → `deployment-ssh` ou config serveur

## Ton Domaine

- Nonces (CSRF protection)
- Sanitization (nettoyage des entrées)
- Escaping (échappement des sorties)
- Protection SQL injection
- Protection XSS
- Capabilities et permissions
- Validation des uploads

## Sources à Consulter

- **Security** : <https://developer.wordpress.org/plugins/security/>
- **Data Validation** : <https://developer.wordpress.org/plugins/security/data-validation/>
- **Securing Input** : <https://developer.wordpress.org/plugins/security/securing-input/>
- **Securing Output** : <https://developer.wordpress.org/plugins/security/securing-output/>
- **Nonces** : <https://developer.wordpress.org/plugins/security/nonces/>

## Nonces - Protection CSRF

### Créer et Vérifier un Nonce dans un Formulaire

```php
// Dans un formulaire
function prefix_render_form() {
    ?>
    <form method="post" action="">
        <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
        <input type="text" name="my_field">
        <button type="submit">Submit</button>
    </form>
    <?php
}

// Vérifier le nonce
function prefix_handle_form() {
    // Vérifier que le nonce est présent et valide
    if ( ! isset( $_POST['my_nonce'] ) ||
         ! wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
        wp_die( 'Security check failed' );
    }

    // Traiter le formulaire...
}
```

### Nonce dans une URL

```php
// Créer l'URL
$url = wp_nonce_url( admin_url( 'admin.php?action=delete&id=123' ), 'delete_item_123' );

// Vérifier
if ( ! wp_verify_nonce( $_GET['_wpnonce'], 'delete_item_123' ) ) {
    wp_die( 'Invalid nonce' );
}

// Ou avec check_admin_referer (die automatiquement si invalide)
check_admin_referer( 'delete_item_123' );
```

### Nonce AJAX

```php
// PHP - localiser le script
wp_localize_script( 'my-script', 'myAjax', array(
    'ajaxurl' => admin_url( 'admin-ajax.php' ),
    'nonce'   => wp_create_nonce( 'my_ajax_nonce' ),
) );

// JavaScript
fetch( myAjax.ajaxurl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams( {
        action: 'my_ajax_action',
        nonce: myAjax.nonce,
        data: 'value'
    } )
} );

// PHP - vérifier
add_action( 'wp_ajax_my_ajax_action', 'prefix_handle_ajax' );
function prefix_handle_ajax() {
    check_ajax_referer( 'my_ajax_nonce', 'nonce' );

    // Traiter...
    wp_send_json_success( $data );
}
```

### Nonce REST API

```php
// Enregistrer un endpoint avec nonce
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/data', array(
        'methods'             => 'POST',
        'callback'            => 'prefix_handle_rest',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
    ) );
} );

// JavaScript avec nonce REST
fetch( '/wp-json/myplugin/v1/data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': wpApiSettings.nonce
    },
    body: JSON.stringify( data )
} );
```

## Sanitization (Nettoyage des Entrées)

Nettoyer les données **AVANT** de les stocker.

### Fonctions de Sanitization

```php
// Texte simple (supprime HTML et tags)
$clean = sanitize_text_field( $_POST['title'] );

// Textarea (conserve les sauts de ligne)
$clean = sanitize_textarea_field( $_POST['description'] );

// Email
$clean = sanitize_email( $_POST['email'] );

// URL (pour stockage)
$clean = esc_url_raw( $_POST['website'] );

// Nom de fichier
$clean = sanitize_file_name( $_FILES['upload']['name'] );

// Clé (lowercase, tirets, underscores)
$clean = sanitize_key( $_POST['slug'] );

// Titre (pour les slugs)
$clean = sanitize_title( $_POST['name'] );

// Slug (sanitize_title avec tirets)
$clean = sanitize_title_with_dashes( $_POST['name'] );

// HTML autorisé (posts - conserve balises autorisées)
$clean = wp_kses_post( $_POST['content'] );

// HTML custom
$allowed = array(
    'a'      => array( 'href' => array(), 'title' => array() ),
    'strong' => array(),
    'em'     => array(),
);
$clean = wp_kses( $_POST['html'], $allowed );

// Aucun HTML
$clean = wp_strip_all_tags( $_POST['text'] );

// Entier positif
$clean = absint( $_POST['quantity'] );

// Entier (peut être négatif)
$clean = intval( $_POST['number'] );

// Nombre décimal
$clean = floatval( $_POST['price'] );

// Booléen
$clean = (bool) $_POST['active'];
$clean = rest_sanitize_boolean( $_POST['active'] ); // pour REST

// Array
$clean = array_map( 'sanitize_text_field', $_POST['items'] );
$clean = array_map( 'absint', $_POST['ids'] );

// Classe CSS
$clean = sanitize_html_class( $_POST['class'] );

// Multiples classes CSS
$classes = explode( ' ', $_POST['classes'] );
$clean = implode( ' ', array_map( 'sanitize_html_class', $classes ) );

// Hex color
$clean = sanitize_hex_color( $_POST['color'] );
$clean = sanitize_hex_color_no_hash( $_POST['color'] );

// MIME type
$clean = sanitize_mime_type( $_POST['mime'] );
```

### Sanitization Personnalisée

```php
// Fonction de sanitization personnalisée
function prefix_sanitize_phone( $phone ) {
    // Supprimer tout sauf chiffres et +
    return preg_replace( '/[^0-9+]/', '', $phone );
}

// Utilisation avec register_setting
register_setting( 'my_options', 'my_phone', array(
    'sanitize_callback' => 'prefix_sanitize_phone',
) );

// Sanitization de meta
register_post_meta( 'post', 'my_phone', array(
    'type'              => 'string',
    'single'            => true,
    'sanitize_callback' => 'prefix_sanitize_phone',
) );
```

## Escaping (Échappement des Sorties)

Échapper les données **AVANT** de les afficher.

### Fonctions d'Escaping

```php
// HTML (dans le contenu)
echo esc_html( $text );
esc_html_e( 'Text to translate', 'textdomain' ); // echo + translate

// Attribut HTML
echo '<input value="' . esc_attr( $value ) . '">';
echo '<div data-id="' . esc_attr( $id ) . '">';

// URL
echo '<a href="' . esc_url( $url ) . '">';

// URL dans un attribut HTML
echo '<a href="' . esc_url( $url ) . '">';

// JavaScript inline
echo '<script>var data = ' . esc_js( $data ) . ';</script>';

// Préférer wp_json_encode pour les objets/arrays
echo '<script>var data = ' . wp_json_encode( $data ) . ';</script>';

// Textarea
echo '<textarea>' . esc_textarea( $content ) . '</textarea>';

// HTML autorisé (pour le contenu de posts)
echo wp_kses_post( $content );

// HTML custom
echo wp_kses( $content, array(
    'a' => array( 'href' => array() ),
    'p' => array(),
) );
```

### Escaping avec Traduction

```php
// Échapper et traduire
echo esc_html__( 'Text', 'textdomain' );
esc_html_e( 'Text', 'textdomain' );

// Attribut
echo esc_attr__( 'Text', 'textdomain' );
esc_attr_e( 'Text', 'textdomain' );

// Avec placeholder
printf(
    esc_html__( 'Hello %s', 'textdomain' ),
    esc_html( $name )
);

// HTML autorisé dans traduction
$allowed = array( 'strong' => array(), 'a' => array( 'href' => array() ) );
echo wp_kses( __( 'Click <a href="%s">here</a>', 'textdomain' ), $allowed );
```

## Protection SQL Injection

```php
global $wpdb;

// TOUJOURS utiliser prepare() avec des placeholders
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
        $author_id,
        'publish'
    )
);

// Placeholders disponibles
// %d = integer
// %s = string
// %f = float

// Pour les IN clauses
$ids = array( 1, 2, 3 );
$placeholders = implode( ', ', array_fill( 0, count( $ids ), '%d' ) );
$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID IN ($placeholders)",
    $ids
);

// LIKE avec wildcards
$search = '%' . $wpdb->esc_like( $search_term ) . '%';
$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s",
    $search
);

// Insert sécurisé
$wpdb->insert(
    $wpdb->posts,
    array(
        'post_title'   => $title,
        'post_content' => $content,
    ),
    array( '%s', '%s' )
);

// Update sécurisé
$wpdb->update(
    $wpdb->posts,
    array( 'post_title' => $new_title ),
    array( 'ID' => $post_id ),
    array( '%s' ),
    array( '%d' )
);
```

## Permissions et Capabilities

```php
// Vérifier les capabilities
if ( ! current_user_can( 'edit_posts' ) ) {
    wp_die( 'You do not have permission to do this.' );
}

// Pour un post spécifique
if ( ! current_user_can( 'edit_post', $post_id ) ) {
    wp_die( 'You cannot edit this post.' );
}

// Capabilities communes
current_user_can( 'manage_options' );  // Admin
current_user_can( 'edit_posts' );      // Editor+
current_user_can( 'publish_posts' );   // Author+
current_user_can( 'edit_others_posts' ); // Editor+
current_user_can( 'delete_posts' );    // Contributor+

// Pour un utilisateur spécifique
user_can( $user_id, 'edit_posts' );

// Dans un callback REST API
'permission_callback' => function() {
    return current_user_can( 'edit_posts' );
}
```

### Vérification Complète dans une Meta Box

```php
add_action( 'save_post', 'prefix_save_meta' );
function prefix_save_meta( $post_id ) {
    // 1. Vérifier le nonce
    if ( ! isset( $_POST['my_nonce'] ) ||
         ! wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
        return;
    }

    // 2. Vérifier l'autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    // 3. Vérifier les permissions
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    // 4. Sanitiser et sauvegarder
    if ( isset( $_POST['my_field'] ) ) {
        update_post_meta(
            $post_id,
            '_my_field',
            sanitize_text_field( $_POST['my_field'] )
        );
    }
}
```

## Validation des Uploads

```php
function prefix_handle_upload() {
    // Vérifier le nonce
    check_admin_referer( 'my_upload_action' );

    // Vérifier les permissions
    if ( ! current_user_can( 'upload_files' ) ) {
        wp_die( 'Permission denied' );
    }

    // Vérifier qu'un fichier a été uploadé
    if ( empty( $_FILES['my_file'] ) ) {
        return new WP_Error( 'no_file', 'No file uploaded' );
    }

    // Types MIME autorisés
    $allowed_types = array( 'image/jpeg', 'image/png', 'image/gif' );

    // Vérifier le type MIME réel (pas celui fourni par le client !)
    $file_info = wp_check_filetype_and_ext(
        $_FILES['my_file']['tmp_name'],
        $_FILES['my_file']['name']
    );

    if ( ! in_array( $file_info['type'], $allowed_types, true ) ) {
        return new WP_Error( 'invalid_type', 'Invalid file type' );
    }

    // Utiliser wp_handle_upload pour la sécurité
    require_once ABSPATH . 'wp-admin/includes/file.php';

    $upload = wp_handle_upload( $_FILES['my_file'], array(
        'test_form' => false,
        'mimes'     => array(
            'jpg|jpeg' => 'image/jpeg',
            'png'      => 'image/png',
            'gif'      => 'image/gif',
        ),
    ) );

    if ( isset( $upload['error'] ) ) {
        return new WP_Error( 'upload_error', $upload['error'] );
    }

    return $upload;
}
```

## Checklist Sécurité

### Pour chaque formulaire

- [ ] Nonce field ajouté (`wp_nonce_field`)
- [ ] Nonce vérifié avant traitement (`wp_verify_nonce`)
- [ ] Permissions vérifiées (`current_user_can`)
- [ ] Toutes les entrées sanitisées
- [ ] Toutes les sorties échappées

### Pour les requêtes SQL

- [ ] Utiliser `$wpdb->prepare()` avec placeholders
- [ ] Jamais de concaténation directe de variables
- [ ] Valider le type des données avant la requête
- [ ] Utiliser `$wpdb->esc_like()` pour les recherches LIKE

### Pour les fichiers uploadés

- [ ] Vérifier le type MIME avec `wp_check_filetype_and_ext`
- [ ] Ne jamais faire confiance à `$_FILES['type']`
- [ ] Utiliser `wp_handle_upload()`
- [ ] Limiter les types de fichiers autorisés
- [ ] Vérifier les permissions d'upload

### Pour les URLs et redirections

- [ ] Utiliser `wp_safe_redirect()` au lieu de `wp_redirect()`
- [ ] Valider les URLs avec `esc_url_raw()` avant stockage
- [ ] Échapper avec `esc_url()` à l'affichage

### Pour les données JSON

- [ ] Utiliser `wp_json_encode()` pour l'encodage
- [ ] Valider la structure JSON après décodage
- [ ] Sanitiser chaque valeur individuellement

## Fonctions de Sécurité Utiles

```php
// Redirection sécurisée (whitelist de domaines)
wp_safe_redirect( $url );
exit;

// Vérifier si la requête est AJAX
if ( wp_doing_ajax() ) { ... }

// Vérifier si c'est une requête cron
if ( wp_doing_cron() ) { ... }

// Vérifier SSL
if ( is_ssl() ) { ... }

// Obtenir l'IP du visiteur de manière sécurisée
$ip = $_SERVER['REMOTE_ADDR'];

// Générer un token aléatoire
$token = wp_generate_password( 32, false );

// Hash sécurisé
$hash = wp_hash( $data );
$hash = wp_hash_password( $password );

// Vérifier un hash de mot de passe
wp_check_password( $password, $hash );
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Secure PHP code | Code PHP sécurisé avec nonces, sanitization et escaping |
| Validation functions | Fonctions de validation personnalisées si nécessaire |
| Security checklist | Checklist de sécurité pour le code produit |
| Documentation | Documentation des pratiques de sécurité implémentées |
