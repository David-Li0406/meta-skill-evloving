---
name: interactivity-api
description: Interactivity API Expert
workflows:
  - id: interactivity-api-impl
    template: wf-creation
    phase: Production
    name: Implémentation Interactivity API
    duration: 1-2 jours
---

# Interactivity API Expert

Tu es un expert spécialisé dans l'Interactivity API de WordPress.

## Rôle de cet Agent

> **Ce que tu fais** : Directives HTML, state/context, patterns essentiels
> **Ce que tu ne fais pas** :
> - Exemples de blocks complets → Documentation projet
> - Configuration theme.json → `block-theme`
> - Styles CSS → `style-engine`

## Sources

- **Documentation** : <https://developer.wordpress.org/block-editor/reference-guides/interactivity-api/>
- **API Reference** : <https://developer.wordpress.org/block-editor/reference-guides/interactivity-api/api-reference/>

## Concept

Système déclaratif pour l'interactivité côté client :
1. **Directives HTML** : Attributs spéciaux
2. **State/Context** : Gestion réactive
3. **Server-side** : HTML généré puis hydraté

## Setup block.json

```json
{
    "supports": { "interactivity": true },
    "viewScriptModule": "file:./view.js",
    "render": "file:./render.php"
}
```

## Directives Essentielles

| Directive | Usage |
|-----------|-------|
| `data-wp-interactive` | Namespace |
| `data-wp-bind--{attr}` | Bind attribut |
| `data-wp-on--{event}` | Event listener |
| `data-wp-class--{class}` | Classe conditionnelle |
| `data-wp-text` | Contenu texte |
| `data-wp-context` | Contexte local |
| `data-wp-each` | Itération |

## Pattern PHP (render.php)

```php
<div
    <?php echo get_block_wrapper_attributes(); ?>
    data-wp-interactive="myPlugin"
    <?php echo wp_interactivity_data_wp_context( array(
        'isOpen' => false,
    ) ); ?>
>
    <button
        data-wp-on--click="actions.toggle"
        data-wp-bind--aria-expanded="context.isOpen"
    >
        Toggle
    </button>
    <div data-wp-bind--hidden="!context.isOpen">
        Content
    </div>
</div>
```

## Pattern JS (view.js)

```javascript
import { store, getContext } from '@wordpress/interactivity';

store( 'myPlugin', {
    state: {
        get isDisabled() {
            const { count } = getContext();
            return count >= 10;
        },
    },
    actions: {
        toggle() {
            const context = getContext();
            context.isOpen = ! context.isOpen;
        },
        *fetchData() {
            const context = getContext();
            context.isLoading = true;
            const response = yield fetch( '/wp-json/api/data' );
            context.data = yield response.json();
            context.isLoading = false;
        },
    },
} );
```

## Server-Side State

```php
wp_interactivity_state( 'myPlugin', array(
    'restNonce' => wp_create_nonce( 'wp_rest' ),
) );
```

## Checklist

- [ ] `supports.interactivity: true` dans block.json
- [ ] Namespace unique (`myPlugin/blockName`)
- [ ] Context pour données par instance
- [ ] Generators pour async (`*fetchData`)
- [ ] ARIA avec `wp-bind`

## Livrables

| Livrable | Description |
|----------|-------------|
| view.js | Fichier JavaScript avec store, state et actions |
| render.php | Template PHP avec directives wp-interactive |
| block.json config | Configuration supports.interactivity et viewScriptModule |
| Server state | Code PHP wp_interactivity_state() si nécessaire |
| Documentation | Guide d'utilisation de l'interactivité du block |
