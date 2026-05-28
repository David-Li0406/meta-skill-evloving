---
name: add-i18n
description: Adds translation keys to both en.json and fr.json files simultaneously. Use /i18n [key] [english] [french] to add translations. Prevents missing translations.
allowed-tools: Read, Edit
---

# Add i18n Skill

## Overview

Manages translation keys by adding them to both language files simultaneously:
- Prevents missing translations between languages
- Maintains consistent key structure
- Supports nested keys

## Command

`/i18n [key] [english] [french]`

**Examples:**
- `/i18n orders.title "Orders" "Commandes"`
- `/i18n orders.status.pending "Pending" "En attente"`
- `/i18n validation.required "This field is required" "Ce champ est obligatoire"`

## Bulk Add

`/i18n-bulk [namespace]`

Then provide key-value pairs:
```
title: Orders | Commandes
status.pending: Pending | En attente
status.completed: Completed | Terminé
```

## Translation Files

**Locations:**
- English: `public/locales/en.json`
- French: `public/locales/fr.json`

## Key Naming Convention

Use dot notation for namespacing:

```
{namespace}.{subnamespace}.{key}
```

**Standard Namespaces:**
- `common.*` - Shared across app (save, cancel, edit, delete)
- `validation.*` - Form validation messages
- `errors.*` - Error messages
- `nav.*` - Navigation labels
- `dashboard.*` - Dashboard page
- `inventory.*` - Inventory module
- `sales.*` - Sales module
- `expenses.*` - Expenses module
- `production.*` - Production/baking module
- `customers.*` - Customer management
- `settings.*` - Settings page

## Process

When user invokes `/i18n [key] [english] [french]`:

1. **Parse the key** to determine nesting:
   - `orders.title` → `{ "orders": { "title": "..." } }`
   - `orders.status.pending` → `{ "orders": { "status": { "pending": "..." } } }`

2. **Read both translation files**:
   - `public/locales/en.json`
   - `public/locales/fr.json`

3. **Add the key to both files** at the correct nested location

4. **Preserve existing structure** - only add/update the specific key

5. **Report what was added**

## Example Workflow

User: `/i18n orders.emptyState "No orders yet" "Aucune commande pour le moment"`

Claude:
1. Reads `public/locales/en.json`
2. Reads `public/locales/fr.json`
3. Adds to en.json under `orders.emptyState`
4. Adds to fr.json under `orders.emptyState`
5. Reports:
   ```
   Added translations:
   - en: orders.emptyState = "No orders yet"
   - fr: orders.emptyState = "Aucune commande pour le moment"
   ```

## Common Translation Patterns

### CRUD Operations
```
/i18n {namespace}.add "Add {Item}" "Ajouter {Item}"
/i18n {namespace}.edit "Edit {Item}" "Modifier {Item}"
/i18n {namespace}.delete "Delete {Item}" "Supprimer {Item}"
/i18n {namespace}.view "View {Item}" "Voir {Item}"
```

### Status Labels
```
/i18n {namespace}.status.pending "Pending" "En attente"
/i18n {namespace}.status.approved "Approved" "Approuvé"
/i18n {namespace}.status.rejected "Rejected" "Rejeté"
```

### Form Labels
```
/i18n {namespace}.form.name "Name" "Nom"
/i18n {namespace}.form.description "Description" "Description"
/i18n {namespace}.form.amount "Amount" "Montant"
/i18n {namespace}.form.date "Date" "Date"
```

### Messages
```
/i18n {namespace}.success.created "{Item} created successfully" "{Item} créé avec succès"
/i18n {namespace}.success.updated "{Item} updated successfully" "{Item} mis à jour avec succès"
/i18n {namespace}.success.deleted "{Item} deleted successfully" "{Item} supprimé avec succès"
/i18n {namespace}.error.notFound "{Item} not found" "{Item} introuvable"
```

## Usage in Components

```tsx
import { useLocale } from '@/components/providers/LocaleProvider'

function MyComponent() {
  const { t } = useLocale()

  return (
    <div>
      <h1>{t('orders.title')}</h1>
      <p>{t('orders.emptyState')}</p>
      <button>{t('common.save')}</button>
    </div>
  )
}
```

## Tips

- Always add translations when creating new UI text
- Use descriptive keys: `orders.confirmDelete` not `orders.msg1`
- Group related translations under the same namespace
- Check existing keys before adding duplicates
- French translations should be grammatically correct (gender, plurals)

## Common Existing Keys

These keys already exist - use them instead of creating duplicates:

```
common.save, common.cancel, common.edit, common.delete
common.add, common.update, common.create, common.close
common.loading, common.error, common.success
common.yes, common.no, common.confirm
common.search, common.filter, common.sort
common.name, common.date, common.amount, common.status
common.actions, common.noData
validation.required, validation.invalid
```
