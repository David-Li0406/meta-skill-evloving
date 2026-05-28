# AskUserQuestion Tool

Interactive prompts with selectable options.

## How It Works in Skills

Claude reads skill text, understands the intent, and calls the actual tool. **JSON in skills is documentation, not configuration** - it shows Claude what parameters to use.

Two equivalent approaches:

**Prose style** (Claude infers parameters):

```
Ask the user which environment to deploy to. Offer "Staging" and "Production" as options.
```

**JSON example style** (Claude follows exactly):

```
Use AskUserQuestion with:
- question: "Which environment?"
- header: "Env"
- options: Staging, Production
```

Both work. JSON is more precise when you need exact parameters.

## Schema

```typescript
AskUserQuestion({
  questions: [
    {
      question: string, // The question to ask
      header: string, // Max 12 chars, shown as chip
      options: [
        {
          label: string, // Option text
          description: string, // Help text
        },
      ], // Max 4 options
      multiSelect: boolean, // Allow multiple selections
    },
  ],
});
```

## Examples

**Choose deployment target:**

```yaml
---
name: deployer
description: Deploys application to environments
---
# Deployer

Before deploying, ask user which environment using AskUserQuestion:
  - question: "Which environment should I deploy to?"
  - header: "Environment"
  - options:
      - Staging (Test environment)
      - Production (Live environment - requires approval)
  - multiSelect: false
```

**Select features to enable:**

```yaml
---
name: feature-setup
description: Configures feature flags
---
Ask which features to enable using AskUserQuestion:
  - question: "Which features should I enable?"
  - header: "Features"
  - options:
      - Dark mode (UI theme support)
      - Analytics (Usage tracking)
      - Notifications (Push alerts)
  - multiSelect: true
```

## Links

- Issues:
  - [#12420](https://github.com/anthropics/claude-code/issues/12420) - 4 option limit too restrictive
  - [#12030](https://github.com/anthropics/claude-code/issues/12030) - multiSelect Enter key bug
  - [#10346](https://github.com/anthropics/claude-code/issues/10346) - Missing documentation
