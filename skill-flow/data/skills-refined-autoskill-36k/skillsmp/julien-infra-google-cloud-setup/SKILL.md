---
name: julien-infra-google-cloud-setup
description: >
  Guide automatisé pour créer un projet Google Cloud de bout en bout avec OAuth.
  Inclut création projet, activation APIs (Calendar, Drive, Sheets, YouTube),
  configuration OAuth consent screen, credentials, test users et publication.
  Use when setting up Google API access, creating OAuth credentials, or configuring Google Cloud projects.
version: "1.0.0"
license: Apache-2.0
user-invocable: true
mode: interactive
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__hydraspecter__browser
triggers:
  # Keywords
  - "google cloud"
  - "google api"
  - "oauth"
  - "credentials.json"
  - "google console"
  - "gcp"

  # Action phrases (FR)
  - "créer projet google"
  - "configurer google api"
  - "setup oauth google"
  - "créer credentials google"
  - "activer api google"
  - "télécharger credentials"

  # Action phrases (EN)
  - "create google cloud project"
  - "setup google oauth"
  - "configure google api"
  - "enable google api"
  - "download credentials"

  # Problem phrases
  - "j'ai besoin d'accéder à google calendar"
  - "comment créer un projet google cloud"
  - "google api authentication"
  - "token google expiré"

metadata:
  author: "Julien Fernandez"
  category: "infrastructure"
  keywords: ["google", "cloud", "oauth", "api", "credentials"]
---

# Google Cloud Project Setup

Guide automatisé pour créer un projet Google Cloud avec OAuth, de la création à la première authentification.

## When to Use

- Besoin d'accéder à une API Google (Calendar, Drive, Sheets, YouTube...)
- Création d'un nouveau projet Google Cloud
- Configuration OAuth pour une application Desktop ou Web
- Renouvellement de credentials expirés

## Observability

**First**: At the beginning of execution, display:
```
🔧 Skill "julien-infra-google-cloud-setup" activated
```

## Prerequisites

- Compte Google avec accès à la console cloud
- Browser automation disponible (HydraSpecter)
- Dossier de destination pour les credentials

## Execution Steps

### Step 1: Création du projet

**URL directe**: `https://console.cloud.google.com/projectcreate`

```
Browser actions:
1. Naviguer vers l'URL
2. Remplir "Project name" (ex: "my-app-sync")
3. Cliquer "Create"
4. Attendre ~30 secondes la création
```

**Nommage recommandé**: `{app-name}-{purpose}` (ex: `notion-gcal-sync`)

**IMPORTANT**: Noter le Project ID généré (visible après création)

### Step 2: Activation des APIs

**Navigation**: APIs & Services → Library

**URLs directes par API**:
| API | URL |
|-----|-----|
| Google Calendar | `https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project=PROJECT_ID` |
| Google Drive | `https://console.cloud.google.com/apis/library/drive.googleapis.com?project=PROJECT_ID` |
| Google Sheets | `https://console.cloud.google.com/apis/library/sheets.googleapis.com?project=PROJECT_ID` |
| YouTube Data API v3 | `https://console.cloud.google.com/apis/library/youtube.googleapis.com?project=PROJECT_ID` |
| Gmail | `https://console.cloud.google.com/apis/library/gmail.googleapis.com?project=PROJECT_ID` |

**Actions pour chaque API**:
1. Naviguer vers l'URL (remplacer PROJECT_ID)
2. Cliquer "Enable"
3. Attendre confirmation

### Step 3: OAuth Consent Screen

**URL**: `https://console.cloud.google.com/apis/credentials/consent?project=PROJECT_ID`

**Configuration**:

| Champ | Valeur recommandée |
|-------|-------------------|
| User Type | **External** (usage personnel) ou **Internal** (Google Workspace) |
| App name | Nom de votre application |
| User support email | Votre email |
| Developer contact | Votre email |

**Scopes à ajouter** (selon les APIs activées):
- Calendar: `https://www.googleapis.com/auth/calendar`
- Drive: `https://www.googleapis.com/auth/drive`
- Sheets: `https://www.googleapis.com/auth/spreadsheets`
- YouTube: `https://www.googleapis.com/auth/youtube.readonly`

**PIÈGE COURANT**: En mode "Testing", les tokens expirent après **7 jours** et limité à **100 test users**.

### Step 4: Création des Credentials OAuth 2.0

**URL**: `https://console.cloud.google.com/apis/credentials?project=PROJECT_ID`

**Actions**:
1. Cliquer "+ CREATE CREDENTIALS"
2. Sélectionner "OAuth client ID"
3. Choisir le type d'application:

| Type | Usage |
|------|-------|
| **Desktop app** | Scripts locaux, CLI, automation |
| **Web application** | Apps web avec callback URL |

4. Nommer le client (ex: "Desktop Client" ou "Web Client")
5. Pour Web app: ajouter les Authorized redirect URIs
6. Cliquer "Create"

**Téléchargement**:
- Cliquer sur l'icône de téléchargement (⬇️) à côté du client créé
- Sauvegarder comme `credentials.json`

### Step 5: Ajout des Test Users

**URL**: `https://console.cloud.google.com/apis/credentials/consent?project=PROJECT_ID`

**Section**: "Test users" → "+ ADD USERS"

**Actions**:
1. Ajouter votre email Google
2. Ajouter les emails des autres testeurs (max 100)
3. Sauvegarder

**IMPORTANT**: Sans test user, l'authentification OAuth échouera avec "Access denied".

### Step 6: Publication en Production (Optionnel mais recommandé)

**Avantages**:
- Tokens ne expirent plus après 7 jours
- Pas de limite de 100 users
- Pas besoin de vérification Google pour usage "internal"

**Actions**:
1. Sur la page OAuth consent screen
2. Cliquer "PUBLISH APP"
3. Confirmer la publication

**Note**: Pour usage personnel, Google n'exige pas de vérification.

### Step 7: Première authentification

**Code Python typique**:
```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Sauvegarder le token pour réutilisation
with open('token.json', 'w') as token:
    token.write(creds.to_json())
```

**Ce qui se passe**:
1. Un navigateur s'ouvre
2. Connexion avec le compte Google (test user)
3. Accepter les permissions
4. `token.json` est créé automatiquement

## Expected Output

**Fichiers créés**:
- `credentials.json` - Client OAuth (ne change jamais)
- `token.json` - Token d'accès (généré à la première auth)

**Structure credentials.json**:
```json
{
  "installed": {
    "client_id": "xxx.apps.googleusercontent.com",
    "client_secret": "GOCSPX-xxx",
    "redirect_uris": ["http://localhost"]
  }
}
```

## Error Handling

| Erreur | Cause | Solution |
|--------|-------|----------|
| "Access denied" | User pas dans test users | Ajouter l'email dans OAuth consent screen → Test users |
| "Token expired" | App en mode Testing | Publier l'app en Production |
| "API not enabled" | API pas activée | Activer l'API dans Library |
| "Invalid client" | credentials.json invalide | Re-télécharger depuis la console |
| "Redirect URI mismatch" | URI non autorisée (Web app) | Ajouter l'URI dans Authorized redirect URIs |

## Examples

### Example 1: Setup pour Google Calendar sync

**User request**: "Je veux synchroniser Notion avec Google Calendar"

**APIs à activer**: Google Calendar API

**Scopes**: `https://www.googleapis.com/auth/calendar`

**Type de credentials**: Desktop app

### Example 2: Setup pour YouTube Data

**User request**: "Je veux récupérer des infos de vidéos YouTube"

**APIs à activer**: YouTube Data API v3

**Scopes**: `https://www.googleapis.com/auth/youtube.readonly`

**Type de credentials**: Desktop app (pour scripts) ou Web app (pour site)

## Skill Chaining

### Skills Required Before
- None (entry point skill)

### Input Expected
- **Format**: Nom du projet souhaité, APIs à activer
- **Source**: User input
- **Validation**: Vérifier que l'utilisateur a un compte Google

### Output Produced
- **Format**: `credentials.json` et `token.json`
- **Location**: Dossier projet spécifié
- **Duration**: 5-10 minutes (interactif)

### Compatible Skills After
- **notion-gcal-sync**: Pour configurer la synchronisation Notion/Calendar
- Tout projet nécessitant des APIs Google

### Visual Workflow

```
User Request: "Setup Google Cloud for Calendar"
    ↓
[THIS SKILL]
    ├─► Create Project
    ├─► Enable APIs
    ├─► Configure OAuth
    ├─► Create Credentials
    ├─► Add Test Users
    └─► Download credentials.json
    ↓
credentials.json + token.json
    ↓
[Your App / Next Skill]
```

## Browser Automation Tips

**Sélecteurs fiables pour Google Console**:
- Bouton Create: `button:has-text("Create")`
- Bouton Enable: `button:has-text("Enable")`
- Input Project name: `input[aria-label="Project name"]`

**Timeouts recommandés**:
- Création projet: 30-60s
- Activation API: 5-10s
- Téléchargement credentials: immédiat

**Astuce**: Utiliser les URLs directes plutôt que la navigation par menu pour éviter les problèmes de sélecteurs dynamiques.
