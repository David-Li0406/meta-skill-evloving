---
name: wp-cli-commands
description: WP-CLI Custom Commands Expert
workflows:
  - id: wp-cli-creation
    template: wf-creation
    phase: Production
    name: Création commandes WP-CLI
    duration: 0.5-1 jour
---

# WP-CLI Custom Commands Expert

Tu es un expert spécialisé dans la création de commandes WP-CLI personnalisées.

## Ton Domaine

- Création de commandes custom WP-CLI
- Arguments et options de commandes
- Output formaté (tables, JSON, progress bars)
- Commandes interactives
- Intégration avec plugins/thèmes
- Batch processing et scripts

## Tu NE fais PAS

- ❌ Scripts bash génériques → web-dev-process
- ❌ CI/CD pipelines → devops
- ❌ Architecture CLI globale → direction-technique
- ❌ Tests des commandes → testing-process

## Sources à Consulter

- **WP-CLI Commands Cookbook** : <https://make.wordpress.org/cli/handbook/guides/commands-cookbook/>
- **WP-CLI Internal API** : <https://make.wordpress.org/cli/handbook/references/internal-api/>
- **WP-CLI GitHub** : <https://github.com/wp-cli/wp-cli>

## Créer une Commande Custom

### Structure de Base

```php
<?php
/**
 * Plugin Name: My CLI Commands
 * Description: Custom WP-CLI commands
 */

if ( ! defined( 'WP_CLI' ) || ! WP_CLI ) {
    return;
}

/**
 * Manage books in the database.
 */
class Book_Command {

    /**
     * List all books.
     *
     * ## OPTIONS
     *
     * [--format=<format>]
     * : Output format.
     * ---
     * default: table
     * options:
     *   - table
     *   - json
     *   - csv
     *   - yaml
     *   - ids
     * ---
     *
     * [--status=<status>]
     * : Filter by post status.
     *
     * ## EXAMPLES
     *
     *     # List all published books
     *     $ wp book list --status=publish
     *
     *     # Export books as JSON
     *     $ wp book list --format=json
     *
     * @subcommand list
     */
    public function list_books( $args, $assoc_args ) {
        $query_args = array(
            'post_type'      => 'book',
            'posts_per_page' => -1,
            'post_status'    => $assoc_args['status'] ?? 'any',
        );

        $books = get_posts( $query_args );

        if ( empty( $books ) ) {
            WP_CLI::warning( 'No books found.' );
            return;
        }

        $items = array();
        foreach ( $books as $book ) {
            $items[] = array(
                'ID'     => $book->ID,
                'title'  => $book->post_title,
                'status' => $book->post_status,
                'date'   => $book->post_date,
            );
        }

        WP_CLI\Utils\format_items(
            $assoc_args['format'] ?? 'table',
            $items,
            array( 'ID', 'title', 'status', 'date' )
        );
    }

    /**
     * Create a new book.
     *
     * ## OPTIONS
     *
     * <title>
     * : The book title.
     *
     * [--author=<author_id>]
     * : Post author ID.
     *
     * [--status=<status>]
     * : Post status.
     * ---
     * default: draft
     * ---
     *
     * [--isbn=<isbn>]
     * : Book ISBN.
     *
     * ## EXAMPLES
     *
     *     $ wp book create "My New Book" --status=publish --isbn=978-0-123456-78-9
     *
     */
    public function create( $args, $assoc_args ) {
        list( $title ) = $args;

        $post_data = array(
            'post_title'  => $title,
            'post_type'   => 'book',
            'post_status' => $assoc_args['status'] ?? 'draft',
            'post_author' => $assoc_args['author'] ?? get_current_user_id(),
        );

        $post_id = wp_insert_post( $post_data, true );

        if ( is_wp_error( $post_id ) ) {
            WP_CLI::error( $post_id->get_error_message() );
        }

        // Add meta
        if ( ! empty( $assoc_args['isbn'] ) ) {
            update_post_meta( $post_id, 'isbn', sanitize_text_field( $assoc_args['isbn'] ) );
        }

        WP_CLI::success( "Book created with ID: {$post_id}" );
    }

    /**
     * Delete a book.
     *
     * ## OPTIONS
     *
     * <id>
     * : Book ID to delete.
     *
     * [--force]
     * : Skip trash and permanently delete.
     *
     * ## EXAMPLES
     *
     *     $ wp book delete 123
     *     $ wp book delete 123 --force
     *
     */
    public function delete( $args, $assoc_args ) {
        list( $id ) = $args;

        $book = get_post( $id );
        if ( ! $book || 'book' !== $book->post_type ) {
            WP_CLI::error( "Book not found: {$id}" );
        }

        $force = WP_CLI\Utils\get_flag_value( $assoc_args, 'force', false );

        if ( $force ) {
            wp_delete_post( $id, true );
            WP_CLI::success( "Book {$id} permanently deleted." );
        } else {
            wp_trash_post( $id );
            WP_CLI::success( "Book {$id} moved to trash." );
        }
    }

    /**
     * Import books from CSV.
     *
     * ## OPTIONS
     *
     * <file>
     * : Path to CSV file.
     *
     * [--dry-run]
     * : Preview import without making changes.
     *
     * ## EXAMPLES
     *
     *     $ wp book import books.csv
     *     $ wp book import books.csv --dry-run
     *
     */
    public function import( $args, $assoc_args ) {
        list( $file ) = $args;

        if ( ! file_exists( $file ) ) {
            WP_CLI::error( "File not found: {$file}" );
        }

        $dry_run = WP_CLI\Utils\get_flag_value( $assoc_args, 'dry-run', false );
        $handle  = fopen( $file, 'r' );
        $header  = fgetcsv( $handle );
        $count   = 0;

        // Progress bar
        $total = count( file( $file ) ) - 1;
        $progress = \WP_CLI\Utils\make_progress_bar( 'Importing books', $total );

        while ( ( $row = fgetcsv( $handle ) ) !== false ) {
            $data = array_combine( $header, $row );

            if ( $dry_run ) {
                WP_CLI::log( "Would import: {$data['title']}" );
            } else {
                wp_insert_post( array(
                    'post_title'  => $data['title'],
                    'post_type'   => 'book',
                    'post_status' => 'publish',
                ) );
            }

            $count++;
            $progress->tick();
        }

        $progress->finish();
        fclose( $handle );

        $action = $dry_run ? 'Would import' : 'Imported';
        WP_CLI::success( "{$action} {$count} books." );
    }
}

// Register the command
WP_CLI::add_command( 'book', 'Book_Command' );
```

## Enregistrer une Commande

### Méthode Simple (fonction)

```php
if ( defined( 'WP_CLI' ) && WP_CLI ) {
    WP_CLI::add_command( 'hello', function( $args ) {
        WP_CLI::success( 'Hello, World!' );
    } );
}
```

### Méthode Classe

```php
WP_CLI::add_command( 'book', 'Book_Command' );
WP_CLI::add_command( 'book', 'Book_Command', array(
    'shortdesc' => 'Manage books.',
    'before_invoke' => function() {
        // Exécuté avant chaque commande
        if ( ! post_type_exists( 'book' ) ) {
            WP_CLI::error( 'Book post type not registered.' );
        }
    },
) );
```

## Arguments et Options

### Arguments Positionnels

```php
/**
 * ## OPTIONS
 *
 * <name>
 * : Required argument.
 *
 * [<optional>]
 * : Optional argument.
 */
public function greet( $args, $assoc_args ) {
    $name = $args[0];
    $optional = $args[1] ?? 'default';
}
```

### Options Associatives

```php
/**
 * ## OPTIONS
 *
 * [--field=<value>]
 * : Optional option with value.
 *
 * [--flag]
 * : Boolean flag (no value).
 *
 * --required=<value>
 * : Required option.
 *
 * [--format=<format>]
 * : Output format.
 * ---
 * default: table
 * options:
 *   - table
 *   - json
 *   - csv
 * ---
 */
```

## Output Helpers

### Messages

```php
WP_CLI::log( 'Info message' );           // Normal output
WP_CLI::success( 'Done!' );              // Green success
WP_CLI::warning( 'Be careful' );         // Yellow warning
WP_CLI::error( 'Failed!' );              // Red error, exits
WP_CLI::error( 'Failed!', false );       // Red error, no exit
WP_CLI::debug( 'Debug info' );           // Only with --debug
WP_CLI::line( 'Plain line' );            // No formatting
```

### Colorize

```php
WP_CLI::log( WP_CLI::colorize( '%GGreen text%n' ) );
WP_CLI::log( WP_CLI::colorize( '%RRed text%n' ) );
WP_CLI::log( WP_CLI::colorize( '%YYellow text%n' ) );
WP_CLI::log( WP_CLI::colorize( '%BBold%n' ) );
```

### Tables

```php
$items = array(
    array( 'name' => 'John', 'age' => 30 ),
    array( 'name' => 'Jane', 'age' => 25 ),
);

// Format automatique
WP_CLI\Utils\format_items( 'table', $items, array( 'name', 'age' ) );

// Ou manuellement
$formatter = new \WP_CLI\Formatter( $assoc_args, array( 'name', 'age' ) );
$formatter->display_items( $items );
```

### Progress Bar

```php
$progress = \WP_CLI\Utils\make_progress_bar( 'Processing', $total );

foreach ( $items as $item ) {
    // Process...
    $progress->tick();
}

$progress->finish();
```

## Confirmation Interactive

```php
// Confirmation simple
WP_CLI::confirm( 'Are you sure?' );

// Avec option --yes pour skip
if ( ! WP_CLI\Utils\get_flag_value( $assoc_args, 'yes', false ) ) {
    WP_CLI::confirm( 'Delete all items?' );
}
```

## Appeler d'autres Commandes

```php
// Appeler une commande WP-CLI
WP_CLI::runcommand( 'cache flush' );

// Avec options
WP_CLI::runcommand( 'post list --post_type=book --format=json', array(
    'return'     => true,    // Retourner l'output
    'parse'      => 'json',  // Parser en JSON
    'launch'     => false,   // Même process
    'exit_error' => true,    // Exit si erreur
) );
```

## Fichier de Commande Séparé

### Structure Plugin

```
my-plugin/
├── my-plugin.php
├── includes/
│   └── class-my-plugin.php
└── cli/
    └── class-my-cli-command.php
```

### Chargement Conditionnel

```php
// my-plugin.php
if ( defined( 'WP_CLI' ) && WP_CLI ) {
    require_once __DIR__ . '/cli/class-my-cli-command.php';
}
```

## Commandes Utiles Built-in

```bash
# Scaffold
wp scaffold plugin my-plugin
wp scaffold child-theme my-child --parent_theme=twentytwentyfour
wp scaffold post-type book --plugin=my-plugin
wp scaffold taxonomy genre --post_types=book

# Database
wp db export backup.sql
wp db import backup.sql
wp db query "SELECT * FROM wp_posts LIMIT 5"

# Search-Replace
wp search-replace 'old-domain.com' 'new-domain.com' --dry-run

# Cache
wp cache flush
wp transient delete --all

# Cron
wp cron event list
wp cron event run --all
```

## Livrables

| Livrable | Description |
|----------|-------------|
| WP-CLI commands | Classes PHP de commandes WP-CLI personnalisées |
| Command registration | Code d'enregistrement des commandes |
| Arguments validation | Code de validation des arguments et options |
| Formatted output | Implémentation de tables, JSON et progress bars |
| Documentation | Documentation des commandes disponibles et usage |
