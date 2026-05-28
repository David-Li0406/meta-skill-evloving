# Exemples de Widgets ChatWidget

Ce document contient des exemples copiables de widgets ChatWidget pour différents cas d'usage.

## 1. Widget Boutons (Actions rapides)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-actions-001",
    "type": "button",
    "label": "Actions disponibles",
    "actions": [
      {
        "id": "a-open-linear",
        "label": "Ouvrir dans Linear",
        "action": "open_url",
        "payload": { "url": "https://linear.app/org/issue/APP-123" }
      },
      {
        "id": "a-navigate",
        "label": "Voir les détails",
        "action": "navigate",
        "payload": { "path": "/requests/uuid-ticket" }
      },
      {
        "id": "a-copy-link",
        "label": "Copier le lien",
        "action": "copy_to_clipboard",
        "payload": { "text": "https://example.com/requests/uuid-ticket" }
      }
    ]
  }
}
```

## 2. Widget Formulaire (Collecte d'infos)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-ticket-form-001",
    "type": "form",
    "label": "Compléter la demande",
    "data": {
      "description": "Merci de compléter ces informations avant création.",
      "fields": [
        { "name": "titre", "type": "text", "label": "Titre", "required": true },
        { "name": "description", "type": "textarea", "label": "Description", "required": true },
        { "name": "impact", "type": "text", "label": "Impact", "required": false },
        { "name": "email", "type": "email", "label": "Email de contact", "required": false }
      ],
      "titre": "Erreur sur fiche client",
      "description": "Quand on ouvre une fiche client, un message d'erreur apparaît.",
      "impact": "Blocage partiel"
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

## 3. Widget Select (Choix unique)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-priority-001",
    "type": "select",
    "label": "Choisir la priorité",
    "data": {
      "options": [
        { "value": "P0", "label": "P0 (Critique)" },
        { "value": "P1", "label": "P1 (Haute)" },
        { "value": "P2", "label": "P2 (Normale)" },
        { "value": "P3", "label": "P3 (Faible)" }
      ],
      "value": "P2"
    },
    "actions": [
      { "id": "a-set-priority", "label": "Confirmer", "action": "set_priority" }
    ]
  }
}
```

## 4. Widget Checkbox (Choix multiples)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-flags-001",
    "type": "checkbox",
    "label": "Informations disponibles",
    "data": {
      "options": [
        { "value": "logs", "label": "Logs d'erreur" },
        { "value": "steps", "label": "Étapes pour reproduire" },
        { "value": "screenshot", "label": "Capture d'écran" },
        { "value": "video", "label": "Enregistrement vidéo" }
      ]
    },
    "actions": [
      { "id": "a-submit-flags", "label": "Continuer", "action": "confirm_flags" }
    ]
  }
}
```

## 5. Widget Radio (Choix unique)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-type-001",
    "type": "radio",
    "label": "Type de demande",
    "data": {
      "options": [
        { "value": "incident", "label": "Incident" },
        { "value": "question", "label": "Question" },
        { "value": "amelioration", "label": "Amélioration" },
        { "value": "bug", "label": "Bug" }
      ],
      "value": "incident"
    },
    "actions": [
      { "id": "a-confirm-type", "label": "Confirmer", "action": "set_type" }
    ]
  }
}
```

## 6. Widget Summary Confirm (Résumé + Confirmation)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-orchestrator-validation-001",
    "type": "summary_confirm",
    "data": {
      "title": "✅ Demande — Bug",
      "understood": [
        "Quand vous cliquez sur \"Client\", vous arrivez sur une page blanche.",
        "Vous vous attendiez à voir la fiche client s'afficher normalement.",
        "Le problème survient uniquement sur Chrome."
      ],
      "confirmation": "Pouvez-vous confirmer que c'est bien ça ? OK / à corriger",
      "next_step": "Parfait, votre demande est prise en charge par l'équipe et sera traitée rapidement."
    },
    "actions": [
      {
        "id": "a-confirm-orchestrator",
        "label": "Confirmé",
        "action": "confirm_orchestrator",
        "payload": { "confirmed": true }
      }
    ]
  }
}
```

## 7. Widget Formulaire Complexe (Multi-étapes)

```json
{
  "type": "widget",
  "widget": {
    "id": "w-contact-form-001",
    "type": "form",
    "label": "Informations de contact",
    "data": {
      "description": "Nous avons besoin de quelques informations pour vous contacter.",
      "fields": [
        { "name": "nom", "type": "text", "label": "Nom complet", "required": true },
        { "name": "entreprise", "type": "text", "label": "Entreprise", "required": false },
        { "name": "telephone", "type": "text", "label": "Téléphone", "required": false },
        { "name": "message", "type": "textarea", "label": "Message", "required": true }
      ]
    },
    "actions": [
      {
        "id": "a-submit-contact",
        "label": "Envoyer",
        "action": "submit_contact_form",
        "payload": { "source": "chatwindow" }
      }
    ]
  }
}
```

## 8. Widget Select avec Auto-trigger

```json
{
  "type": "widget",
  "widget": {
    "id": "w-status-001",
    "type": "select",
    "label": "Statut de la demande",
    "data": {
      "options": [
        { "value": "open", "label": "Ouverte" },
        { "value": "in_progress", "label": "En cours" },
        { "value": "resolved", "label": "Résolue" },
        { "value": "closed", "label": "Fermée" }
      ]
    },
    "actions": [
      { "id": "a-update-status", "label": "Mettre à jour", "action": "update_status" }
    ]
  }
}
```

## Notes d'utilisation

- **Copier-coller** : Ces exemples peuvent être copiés directement dans le Playground (`/admin/widget-playground`)
- **Modifier** : Adapter les IDs, labels, et données selon votre cas d'usage
- **Tester** : Toujours tester dans le Playground avant d'intégrer dans un workflow
- **Valider** : Vérifier 0 erreur console après chaque modification

## Références

- Contrat complet : `agentbuilder/WIDGETS_CONTRACT.md`
- Types TypeScript : `src/types/chat.ts`
- Renderer : `src/components/chat/ChatWidget.tsx`
