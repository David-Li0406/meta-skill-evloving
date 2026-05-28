# Serveurs MCP — Modèle de documentation (générique)

Ce fichier sert de **template** pour documenter les serveurs MCP de votre projet (URLs, rôles, outils disponibles).

## Base URL (exemple Supabase Edge Functions)

- **Project ID** : `votre-project-id`
- **Base URL** : `https://votre-project-id.supabase.co/functions/v1`

## Exemple d’entrée serveur

### Contacts

- **Edge Function** : `contacts-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/contacts-mcp/sse`
- **Description** : Gestion des contacts (CRUD, recherche, etc.)
- **Outils** : `contacts_list`, `contacts_get`, `contacts_create`, ...

## Authentification (à adapter)

Selon votre infra, vous aurez typiquement :
- `Authorization: Bearer <jwt>` (session user/agent)
- `apikey: <anon_key>` (si Supabase Edge Functions)

## Checklist

- [ ] URLs correctes (prod + dev si applicable)
- [ ] Auth documentée (headers requis)
- [ ] Liste d’outils à jour (`tools/list`)
- [ ] Exemples de snippets Cursor / Agent Builder / n8n (si utilisés)

