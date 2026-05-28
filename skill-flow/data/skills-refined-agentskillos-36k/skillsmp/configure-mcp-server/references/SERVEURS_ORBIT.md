# Serveurs MCP Orbit - Référence complète

Ce document liste tous les serveurs MCP disponibles dans le projet Orbit avec leurs URLs, descriptions et outils disponibles.

⚠️ **Note (somtech-pack)** : ce fichier est un **exemple** (inspiré d’un projet réel). Toutes les URLs utilisent des **placeholders** : remplacez `votre-project-id` par votre Project Ref Supabase.

## Base URL Supabase

**Project ID** : `votre-project-id`  
**Base URL** : `https://votre-project-id.supabase.co/functions/v1`

## Serveurs disponibles

### Documents

- **Edge Function** : `documents-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/documents-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/documents-mcp/sse`
- **Description** : Gestion des documents avec recherche et ajout
- **Outils** : Recherche de documents, ajout de documents, gestion des métadonnées

### Contacts

- **Edge Function** : `contacts-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/contacts-mcp/sse`
- **Description** : Gestion des contacts (personnes) - CRUD complet
- **Outils** : `app_contacts_list`, `app_contacts_get`, `app_contacts_create`, `app_contacts_update`, `app_contacts_delete`

### Entreprises

- **Edge Function** : `entreprises-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/entreprises-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/entreprises-mcp/sse`
- **Description** : Gestion des entreprises (clients) - CRUD complet
- **Outils** : `app_entreprises_list`, `app_entreprises_get`, `app_entreprises_create`, `app_entreprises_update`, `app_entreprises_delete`

### Opportunités

- **Edge Function** : `opportunites-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/opportunites-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/opportunites-mcp/sse`
- **Description** : Gestion des opportunités
- **Outils** : `app_opportunites_list`, `app_opportunites_get`, `app_opportunites_create`, `app_opportunites_update`, `app_opportunites_delete`

### Projets

- **Edge Function** : `projets-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/projets-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/projets-mcp/sse`
- **Description** : Gestion des projets
- **Outils** : `app_projets_list`, `app_projets_get`, `app_projets_create`, `app_projets_update`, `app_projets_delete`

### Tâches

- **Edge Function** : `taches-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/taches-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/taches-mcp/sse`
- **Description** : Gestion des tâches
- **Outils** : `app_taches_list`, `app_taches_get`, `app_taches_create`, `app_taches_update`, `app_taches_delete`

### Applications

- **Edge Function** : `applications-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/applications-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/applications-mcp/sse`
- **Description** : Gestion des applications
- **Outils** : `app_applications_list`, `app_applications_get`, `app_applications_create`, `app_applications_update`, `app_applications_delete`

### Interactions

- **Edge Function** : `interactions-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/interactions-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/interactions-mcp/sse`
- **Description** : Gestion des interactions
- **Outils** : `app_interactions_list`, `app_interactions_get`, `app_interactions_create`, `app_interactions_update`, `app_interactions_delete`

### Publications

- **Edge Function** : `publications-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/publications-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/publications-mcp/sse`
- **Description** : Gestion des publications
- **Outils** : `app_publications_list`, `app_publications_get`, `app_publications_create`, `app_publications_update`, `app_publications_delete`

### Tickets

- **Edge Function** : `tickets-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/tickets-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/tickets-mcp/sse`
- **Description** : Gestion du support
- **Outils** : `app_tickets_list`, `app_tickets_get`, `app_tickets_create`, `app_tickets_update`, `app_tickets_delete`

### Livrables

- **Edge Function** : `livrables-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/livrables-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/livrables-mcp/sse`
- **Description** : Gestion des livrables
- **Outils** : `app_livrables_list`, `app_livrables_get`, `app_livrables_create`, `app_livrables_update`, `app_livrables_delete`

### Commandes

- **Edge Function** : `commande-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/commande-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/commande-mcp/sse`
- **Description** : Gestion des commandes maquettes
- **Outils** : Spécifiques aux commandes

### Clients (Legacy)

- **Edge Function** : `clients-mcp`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/clients-mcp/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/clients-mcp/sse`
- **Description** : Compat legacy: outils app_clients_* (mappés sur contacts)
- **Outils** : `app_clients_list`, `app_clients_get`, `app_clients_create`, `app_clients_update`, `app_clients_delete`

### Docs Reader

- **Edge Function** : `docs-reader`
- **URL MCP** : `https://votre-project-id.supabase.co/functions/v1/docs-reader/mcp`
- **URL Agent Builder** : `https://votre-project-id.supabase.co/functions/v1/docs-reader/sse`
- **Description** : Lecture des PRD (global et par module) depuis GitHub
- **Outils** : Lecture de fichiers PRD depuis le dépôt GitHub

## Authentification

Tous les serveurs Supabase Edge Functions nécessitent :
- **Header `apikey`** : Clé anonyme Supabase (`VITE_SUPABASE_ANON_KEY`)
- **Header `Authorization`** : Bearer token JWT (session utilisateur ou token d'agent)

Pour Agent Builder, utiliser un JWT authentifié (idéalement un token d'agent dédié).

## Health Checks

Tous les serveurs exposent des endpoints de health check :
- `GET /` : Health check principal
- `GET /health` : Health check (compatibilité monitoring)
- `GET /elf` : ELF check (compatibilité ChatGPT)
- `GET /check` : Check alternatif

## Endpoints MCP

- `POST /mcp` : Endpoint MCP canonique (JSON-RPC Streamable HTTP)
- `GET /mcp` : Infos (ou SSE si `Accept: text/event-stream`)
- `GET /sse` : Bootstrap SSE (compat OpenAI Agent Builder)
- `GET /tools` : Liste des outils disponibles
- `POST /tools/call` : Appel d'outil via HTTP bridge
