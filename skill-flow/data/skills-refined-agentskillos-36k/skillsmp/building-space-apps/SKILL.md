---
name: building-space-apps
description: Use when creating custom UI for Agency spaces, configuring app.json manifests, building HTML apps with agentBridge, or setting up web-based dashboards
---

# Building Space Apps

Space Apps provide custom interfaces for Agency spaces - from simple configuration to full web applications.

## When to Use

- Creating custom UI for a space (dashboards, forms, visualizations)
- Configuring `.manifest/app.json` for space behavior
- Building HTML/JS apps that communicate with agents via `agentBridge`
- Setting up web views that persist data or access files

## App Modes

Configure in `.manifest/app.json`:

| Mode | Description |
|------|-------------|
| `default` | Standard tabs + chat UI |
| `configured` | Standard UI with custom manifest settings |
| `extended` | Standard UI + custom HTML sections |
| `fullReplace` | Web app completely replaces UI |

```json
{
  "appMode": "fullReplace",
  "htmlApp": {
    "path": "app.html",
    "capabilities": ["chat", "context", "storage"],
    "sandboxLevel": "standard"
  }
}
```

## Creating a Web App

### 1. Create HTML file

Create `.manifest/app.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Space App</title>
    <style>
        body { font-family: system-ui; padding: 20px; }
    </style>
</head>
<body>
    <input id="msg" type="text" placeholder="Ask...">
    <button onclick="send()">Send</button>
    <div id="response"></div>

    <script>
        async function send() {
            const result = await agentBridge.sendMessage(
                document.getElementById('msg').value
            );
            document.getElementById('response').textContent = result.text;
        }
        agentBridge.onActivate(() => console.log('Active'));
    </script>
</body>
</html>
```

### 2. Configure manifest

Create `.manifest/app.json`:

```json
{
  "space": { "name": "My Space", "icon": "star.fill" },
  "appMode": "fullReplace",
  "htmlApp": {
    "path": "app.html",
    "capabilities": ["chat", "context", "storage"],
    "sandboxLevel": "standard"
  }
}
```

## agentBridge API

The `agentBridge` object is automatically injected:

### Chat Operations

```javascript
// Send message to agent
const response = await agentBridge.sendMessage("Help me...");
// response = { text: "...", toolCalls: [...] }

// Listen for messages
agentBridge.onMessage((msg) => console.log(msg.text));

// Get history
const history = await agentBridge.getHistory({ limit: 50 });
```

### Context Operations

```javascript
const space = await agentBridge.getSpace();      // { id, name, path }
const guidelines = await agentBridge.getGuidelines();
const config = await agentBridge.getConfig();
```

### Storage (Per-Space SQLite)

```javascript
await agentBridge.storage.set("key", { any: "value" });
const val = await agentBridge.storage.get("key");
const keys = await agentBridge.storage.keys();
const all = await agentBridge.storage.all();
await agentBridge.storage.clear();
```

### File Operations

Requires `files` capability:

```javascript
const files = await agentBridge.files.list("docs");
const content = await agentBridge.files.read("notes.md");
// Writes create DecisionCard for approval
await agentBridge.files.write("out.md", "# Content");
```

### Lifecycle Hooks

```javascript
agentBridge.onActivate(() => loadData());
agentBridge.onDeactivate(() => saveState());
```

## Capabilities

| Capability | Description |
|------------|-------------|
| `chat` | Send/receive messages |
| `context` | Access space info, guidelines |
| `storage` | Persist data in SQLite |
| `files` | Read/write space files |
| `notifications` | System notifications |
| `agent` | Advanced control (pause/resume) |

## Sandbox Levels

| Level | Description |
|-------|-------------|
| `strict` | No external resources |
| `standard` | Local only, no network |
| `permissive` | External allowed (user consent) |

## Linked Spaces

Access context from related spaces:

```json
{
  "links": [
    { "space": "Research", "access": "readonly", "reason": "Access findings" },
    { "space": "DevOps", "access": "a2a", "reason": "Delegate deployments" }
  ]
}
```

| Access | Description |
|--------|-------------|
| `readonly` | Read files and context |
| `a2a` | Delegate tasks to linked agent |

## Quick Reference

**Minimal web app setup:**
1. Create `.manifest/app.html` with your UI
2. Create `.manifest/app.json` with `appMode: "fullReplace"`
3. Declare capabilities needed
4. Use `agentBridge` for agent communication

**Common patterns:**
- Dashboard: storage for state, chat for actions
- Form: collect input, sendMessage to process
- Viewer: files.list + files.read for content

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using innerHTML with user data | Use `textContent` or DOM APIs |
| Missing capability declaration | Add to `htmlApp.capabilities` array |
| Relying on in-memory state | Use `agentBridge.storage` for persistence |
| Starting with fullReplace | Start with `configured`, add complexity gradually |
