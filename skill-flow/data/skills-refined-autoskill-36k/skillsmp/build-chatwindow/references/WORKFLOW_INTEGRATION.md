# Intégration des Widgets dans les Workflows

Ce document explique comment intégrer des widgets ChatWidget dans les workflows OpenAI Agent Builder et n8n.

## Vue d'ensemble

Les widgets sont renvoyés par les workflows via le routeur SSE (`chatkit` Edge Function). Le workflow doit renvoyer un événement SSE au format :

```json
{
  "type": "widget",
  "widget": { /* ChatWidget */ }
}
```

## OpenAI Agent Builder

### Format de réponse

Dans le prompt de l'agent OpenAI, inclure le widget dans la réponse au format JSON :

```json
{
  "type": "widget",
  "widget": {
    "id": "w-ticket-form-001",
    "type": "form",
    "label": "Compléter la demande",
    "data": {
      "fields": [
        { "name": "titre", "type": "text", "label": "Titre", "required": true }
      ]
    },
    "actions": [
      {
        "id": "a-create-ticket",
        "label": "Créer",
        "action": "create_ticket",
        "payload": { "module": "clients" }
      }
    ]
  }
}
```

### Exemple de prompt

```
Lorsque l'utilisateur demande à créer un ticket, renvoie un widget formulaire 
au format suivant :

{
  "type": "widget",
  "widget": {
    "id": "w-ticket-form-001",
    "type": "form",
    "label": "Compléter la demande",
    "data": {
      "description": "Merci de compléter ces informations.",
      "fields": [
        { "name": "titre", "type": "text", "label": "Titre", "required": true },
        { "name": "description", "type": "textarea", "label": "Description", "required": true }
      ]
    },
    "actions": [
      {
        "id": "a-create-ticket",
        "label": "Créer la demande",
        "action": "create_ticket",
        "payload": { "module": "clients" }
      }
    ]
  }
}
```

### Traitement par le routeur SSE

Le routeur SSE (`chatkit`) :
1. Reçoit la réponse de l'agent OpenAI
2. Parse le JSON pour détecter `{ "type": "widget", ... }`
3. Stream l'événement SSE au frontend
4. Le frontend (`useChatKit`) parse et affiche le widget

## n8n Workflow

### Format de réponse webhook

Dans le webhook n8n, renvoyer :

```json
{
  "content": "Message texte de l'assistant",
  "widget": {
    "id": "w-ticket-form-001",
    "type": "form",
    "label": "Compléter la demande",
    "data": {
      "fields": [
        { "name": "titre", "type": "text", "label": "Titre", "required": true }
      ]
    },
    "actions": [
      {
        "id": "a-create-ticket",
        "label": "Créer",
        "action": "create_ticket",
        "payload": { "module": "clients" }
      }
    ]
  }
}
```

### Exemple n8n (Node "Respond to Webhook")

Dans le nœud "Respond to Webhook" de n8n :

```json
{
  "content": "Voici le formulaire pour créer votre demande.",
  "widget": {
    "id": "w-ticket-form-001",
    "type": "form",
    "label": "Compléter la demande",
    "data": {
      "description": "Merci de compléter ces informations.",
      "fields": [
        { "name": "titre", "type": "text", "label": "Titre", "required": true },
        { "name": "description", "type": "textarea", "label": "Description", "required": true }
      ]
    },
    "actions": [
      {
        "id": "a-create-ticket",
        "label": "Créer la demande",
        "action": "create_ticket",
        "payload": { "module": "clients", "priority": "P1" }
      }
    ]
  }
}
```

### Traitement par le routeur SSE

Le routeur SSE (`chatkit`) :
1. Appelle le webhook n8n
2. Reçoit la réponse avec `content` et `widget`
3. Stream le `content` comme message assistant
4. Stream le `widget` comme événement `{ type: "widget", widget: ... }`
5. Le frontend parse et affiche le widget

## Gestion des actions

### Format de requête d'action

Quand un utilisateur déclenche une action, le frontend envoie :

```json
{
  "type": "threads.add_user_message",
  "params": {
    "thread_id": "uuid-thread",
    "input": {
      "content": [/* contenu optionnel */]
    },
    "context": {
      "workflow_id": "uuid-workflow",
      "action_id": "a-create-ticket",
      "payload": {
        "module": "clients",
        "priority": "P1",
        "titre": "Erreur sur fiche client",
        "description": "Quand on ouvre une fiche client..."
      }
    }
  }
}
```

### Traitement dans le workflow

Le workflow doit :
1. Détecter `context.action_id` pour identifier l'action
2. Utiliser `context.payload` pour traiter l'action
3. Renvoyer une réponse (message + widget optionnel)

### Exemple OpenAI Agent Builder

```
Si context.action_id === "create_ticket", alors :
1. Extraire les données de context.payload
2. Créer le ticket dans la base de données
3. Renvoyer un message de confirmation avec un widget summary_confirm
```

### Exemple n8n

Dans le workflow n8n :
1. Nœud "If" pour vérifier `context.action_id`
2. Nœud "Create Ticket" (API call) avec `context.payload`
3. Nœud "Respond to Webhook" avec message de confirmation + widget

## Bonnes pratiques

### IDs stables

- Utiliser des IDs déterministes pour les widgets et actions
- Format : `w-{type}-{purpose}-{number}` pour widgets
- Format : `a-{action}-{purpose}` pour actions

### Payload vs FormData

- **`payload`** : Valeurs fixes (ex: `{ module: "clients", priority: "P1" }`)
- **`formData`** : Valeurs saisies par l'utilisateur (fusionnées automatiquement)

### Gestion d'erreurs

- Si le widget est invalide, le frontend l'ignore silencieusement
- Vérifier toujours dans le Playground avant d'intégrer
- Logger les erreurs côté backend pour déboguer

## Références

### Fichiers type dans votre projet

- **Routeur SSE** : Votre Edge Function ou API qui stream les réponses (ex: `supabase/functions/chatkit/index.ts` ou équivalent)
- **Hook frontend** : Votre hook qui gère les messages et widgets (ex: `src/hooks/useChatKit.ts` ou équivalent)
- **Documentation backend** : Votre documentation sur le backend SSE (ex: `docs/chatbot/04-backend.md` ou équivalent)
- **Documentation workflows** : Votre documentation sur les workflows (ex: `docs/chatbot/06-workflows.md` ou équivalent)

> **Note** : Adaptez ces chemins selon la structure de votre projet. L'important est de comprendre le flux de données décrit dans ce document.
