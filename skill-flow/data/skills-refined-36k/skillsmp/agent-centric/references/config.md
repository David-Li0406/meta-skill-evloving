# Config Reference

Configuration options for the Agent Centric framework.

## File Location

`.agents/config.json`

## Structure

```json
{
  "tags": [],
  "disableAutoUpdateScripts": []
}
```

## Fields

### tags

Array of allowed tag names. Tags represent system scopes (e.g., module names, components).

```json
{
  "tags": ["core", "auth", "api", "database"]
}
```

The validation script rejects files with undefined tags.

### disableAutoUpdateScripts

Controls automatic script updates from the skill directory.

**Disable specific scripts:**

```json
{
  "disableAutoUpdateScripts": ["validate-agds.py", "utils.py"]
}
```

**Disable all updates:**

```json
{
  "disableAutoUpdateScripts": true
}
```

**Enable all updates (default):**

```json
{
  "disableAutoUpdateScripts": []
}
```

## Directory Structure

```
.agents/
├── decisions/
│   └── .gitkeep
├── scripts/
│   ├── utils.py
│   ├── validate-agds.py
│   └── generate-index.py
├── config.json
├── INDEX-TAGS.md
├── INDEX-AGD-RELATIONS.md
└── CLAUDE.md
```
