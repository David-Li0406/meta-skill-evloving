# Create a Challenge

Workflow for creating new Kubeasy challenges.

## Prerequisites

1. Call `kubeasy:get_challenge_schema` for the YAML schema
2. Call `kubeasy:get_challenges_types` for available types
3. Call `kubeasy:get_challenges_themes` for available themes
4. Read `CHALLENGE_GUIDELINES.md` from the repo

## Workflow

### 1. Gather Requirements

Ask the user:
- **Concept**: What Kubernetes skill to teach?
- **Type**: fix (debug), build (create), or migrate (transform)
- **Theme**: From MCP results
- **Difficulty**: easy (10-15min), medium (15-20min), hard (20-30min)

### 2. Design with Mystery

Apply the philosophy from CHALLENGE_GUIDELINES.md:

| Field | Do | Don't |
|-------|-----|-------|
| `description` | Describe symptoms | Reveal the root cause |
| `initialSituation` | What user observes | What's broken |
| `objective` | Goal to achieve | How to fix it |
| `objectives[].title` | Outcome checked | The specific fix |

### 3. Write challenge.yaml

```yaml
title: Short Catchy Title
description: |
  Intriguing description of symptoms.
  Something is wrong, but what?
theme: <from-mcp>
difficulty: easy|medium|hard
type: <from-mcp>
estimatedTime: 15
starterFriendly: false  # true only for easy, beginner-appropriate challenges

initialSituation: |
  What the user finds when starting.
  Observable symptoms, not the bug.

objective: |
  What success looks like.
  Not how to achieve it.

objectives:
  - key: unique-key
    title: "Outcome Title"
    description: "What this validates"
    order: 1
    type: status|log|event|metrics|connectivity
    spec:
      # Type-specific - see schema from MCP
```

### 4. Create Manifests

In `<slug>/manifests/`:
- Use realistic resource names
- Bug should be subtle but discoverable via kubectl
- Include all resources for the broken state

### 5. Add Bypass Protection (optional)

Kyverno policies in `<slug>/policies/` to prevent:
- Replacing container images
- Trivial delete/recreate
- Other cheats

Example:
```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: protect-<slug>-image
spec:
  validationFailureAction: Enforce
  rules:
    - name: preserve-image
      match:
        resources:
          kinds: ["Deployment"]
          namespaces: ["challenge-*"]
      validate:
        message: "Cannot change the application image"
        pattern:
          spec:
            template:
              spec:
                containers:
                  - name: app
                    image: "original/image:tag"
```

## Publishing

### 6. Sync to Database

```bash
cd /Users/paul/Workspace/kubeasy/challenges
API_URL=http://localhost:3000/api/admin API_TOKEN=$(cat /Users/paul/Workspace/kubeasy/api_key) node .github/scripts/sync.js
```

### 7. Push to Feature Branch

```bash
cd /Users/paul/Workspace/kubeasy/challenges
git checkout -b challenge/<slug>
git add <slug>/
git commit -m "feat: add challenge <slug>"
git push -u origin challenge/<slug>
```

### 8. Update CLI Branch

Edit `/Users/paul/Workspace/kubeasy/kubeasy-cli/internal/constants/constants.go`:
- Find `ChallengesBranch` or similar constant
- Set to `challenge/<slug>`

### 9. Recompile CLI

```bash
cd /Users/paul/Workspace/kubeasy/kubeasy-cli
go build -o kubeasy-cli .
```

### 10. Test

```bash
cd /Users/paul/Workspace/kubeasy/kubeasy-cli
./kubeasy-cli challenge start <slug>
# Attempt to solve...
./kubeasy-cli challenge submit <slug>
```

## Anti-patterns Checklist

Before publishing, verify:

- [ ] Description doesn't reveal the fix
- [ ] Objectives check outcomes, not implementations
- [ ] Realistic scenario (could happen in production)
- [ ] No trivial bypasses possible
- [ ] Estimated time is accurate
- [ ] Difficulty matches actual effort

## Handling Blockers

Si pendant la création tu rencontres une limitation (validator manquant, prerequisite non supporté, bug CLI) :

### 1. Vérifier si c'est vraiment bloquant

- Peut-on contourner avec les validators existants ?
- Peut-on simplifier le challenge pour éviter le besoin ?

### 2. Ouvrir un ticket sur `kubeasy-dev/kubeasy-cli`

```markdown
## [Bug|Feature Request]: [Titre court]

### Context
Création du challenge "[slug]" sur le thème [theme].

### Problème
[Description du blocage]

### Reproduction (si bug)
```bash
# Commandes pour reproduire
```

### Besoin (si feature)
[Ce qui manque et pourquoi c'est nécessaire]

### Proposition
[Solution suggérée si applicable]

### Workaround actuel
[Comment contourner en attendant, si possible]
```

### 3. Documenter le blocage

Ajouter dans le challenge.yaml (commentaire) ou dans un README :

```yaml
# BLOCKED: Waiting for https://github.com/kubeasy-dev/kubeasy-cli/issues/XXX
# Workaround: Using log objective instead of custom validator
```
