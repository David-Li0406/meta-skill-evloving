# Types de Configuration MCP - Référence

Ce document décrit les différents types de configuration MCP supportés dans Cursor.

## 1. Configuration URL (HTTP/HTTPS)

Configuration la plus simple pour les serveurs MCP accessibles via HTTP.

```json
{
  "mcpServers": {
    "nom-serveur": {
      "url": "https://example.com/mcp"
    }
  }
}
```

**Utilisé pour** :
- Serveurs Supabase Edge Functions ⭐ (méthode recommandée)
- Serveurs n8n
- Tout serveur MCP accessible via HTTP
- Serveurs Railway (si votre projet utilise Railway)

**Avantages** :
- Configuration simple
- Pas d'installation locale nécessaire
- Toujours à jour (version hébergée)

## 2. Configuration Streamable HTTP

Configuration pour les serveurs utilisant le transport Streamable HTTP.

```json
{
  "mcpServers": {
    "nom-serveur": {
      "type": "streamable-http",
      "url": "https://example.com/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN"
      }
    }
  }
}
```

**Utilisé pour** :
- Serveurs n8n
- Serveurs nécessitant des headers d'authentification
- Serveurs Railway (si votre projet utilise Railway)

**Avantages** :
- Support des headers personnalisés
- Authentification via Bearer tokens
- Compatible avec les serveurs HTTP modernes

## 3. Configuration Command (npx/local)

Configuration pour les serveurs MCP exécutés localement via une commande.

```json
{
  "mcpServers": {
    "nom-serveur": {
      "command": "npx",
      "args": ["-y", "@package/nom-package"],
      "env": {
        "VARIABLE_ENV": "valeur"
      }
    }
  }
}
```

**Utilisé pour** :
- Serveurs Supabase MCP (option locale, développement)
- Tout serveur MCP disponible via npm/npx
- Serveurs Railway (si votre projet utilise Railway)

**Avantages** :
- Fonctionne hors ligne (après installation initiale)
- Plus de contrôle sur la version
- Accès aux variables d'environnement locales

**Paramètres** :
- `command` : Commande à exécuter (ex: `npx`, `node`, `python`)
- `args` : Arguments passés à la commande
- `env` : Variables d'environnement (optionnel)

## 4. Configuration avec Headers

Pour les serveurs nécessitant des headers d'authentification ou personnalisés.

```json
{
  "mcpServers": {
    "nom-serveur": {
      "url": "https://example.com/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN",
        "X-Custom-Header": "valeur"
      }
    }
  }
}
```

**Utilisé pour** :
- Authentification Bearer token
- Headers personnalisés requis par le serveur
- API keys dans les headers

## 5. Configuration Mixte

Combinaison de plusieurs types de serveurs dans un même fichier.

```json
{
  "mcpServers": {
    "supabase-contacts": {
      "url": "https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp"
    },
    "n8n": {
      "type": "streamable-http",
      "url": "https://n8n-instance.up.railway.app/mcp-server/http",
      "headers": {
        "Authorization": "Bearer N8N_MCP_ACCESS_TOKEN"
      }
    },
    "supabase-local": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref=votre-project-id"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_..."
      }
    }
  }
}
```

## Comparaison des types

| Type | Installation | Hors ligne | Authentification | Recommandé pour |
|------|--------------|------------|------------------|-----------------|
| URL | Non | Non | Via headers | Production, simplicité |
| Streamable HTTP | Non | Non | Via headers | Production, auth complexe |
| Command (npx) | Oui (auto) | Oui | Via env vars | Développement, contrôle version |

## Recommandations

### Pour Supabase (Edge Functions)

**Production** : Utiliser la configuration URL simple
```json
{
  "mcpServers": {
    "contacts": {
      "url": "https://votre-project-id.supabase.co/functions/v1/contacts-mcp/mcp"
    }
  }
}
```

**Développement** : Optionnellement utiliser npx pour plus de contrôle
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref=votre-project-id"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_..."
      }
    }
  }
}
```

### Pour Railway

**Configuration Railway** :
```json
{
  "mcpServers": {
    "railway": {
      "type": "streamable-http",
      "url": "https://railway-mcp.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer RAILWAY_TOKEN"
      }
    }
  }
}
```

### Pour n8n

**Recommandé** : Streamable HTTP avec MCP Access Token
```json
{
  "mcpServers": {
    "n8n": {
      "type": "streamable-http",
      "url": "https://n8n-instance.up.railway.app/mcp-server/http",
      "headers": {
        "Authorization": "Bearer N8N_MCP_ACCESS_TOKEN"
      }
    }
  }
}
```
