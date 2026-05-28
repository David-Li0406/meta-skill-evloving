# Generate Challenge Ideas

Discover new challenge ideas by analyzing Kubernetes documentation and comparing against existing coverage.

## Workflow

### 1. Fetch K8s Documentation

Use the Context7 MCP to navigate Kubernetes docs:

```
Library: /kubernetes/website
```

Browse sections like:
- `content/en/docs/concepts/`
- `content/en/docs/tasks/`
- `content/en/docs/tutorials/`

### 2. Analyze Coverage Gaps

First, get existing challenges:
```
kubeasy:get_challenges (no filters)
```

Build a coverage map:

| K8s Doc Section | Kubeasy Theme | Existing Challenges |
|-----------------|---------------|---------------------|
| workloads/pods | pods-containers | bad-config, lost-logs |
| services-networking | networking | partial-outage, traffic-jam |
| ... | ... | ... |

Identify sections with no corresponding challenges.

### 3. Map Documentation to Themes

| K8s Doc Path | Kubeasy Theme |
|--------------|---------------|
| `concepts/workloads/pods/` | pods-containers |
| `concepts/workloads/controllers/` | resources-scaling |
| `concepts/services-networking/` | networking |
| `concepts/services-networking/ingress/` | ingress-tls |
| `concepts/storage/` | volumes-secrets |
| `concepts/configuration/secret/` | volumes-secrets |
| `concepts/scheduling-eviction/` | scheduling-affinity |
| `concepts/security/` | rbac-security |
| `tasks/debug/` | monitoring-debugging |
| `concepts/workloads/controllers/job/` | jobs-cronjobs |

### 4. Determine Challenge Type

| Doc Content | Challenge Type |
|-------------|----------------|
| "Troubleshooting", "Debug", common errors | **fix** |
| "Create a...", step-by-step tutorials | **build** |
| Deprecation notices, version upgrades, API changes | **migrate** |

### 5. Estimate Difficulty

```
easy:   Single resource, no prerequisites, < 5 steps
medium: Multiple resources, some prerequisites, 5-10 steps
hard:   Complex interactions, many prerequisites, > 10 steps
```

### 6. Extract Challenge Ideas

For each promising doc section, extract:

- **Title**: From frontmatter or first H1
- **YAML examples**: Code blocks with `kind:` 
- **Prerequisites**: "Before you begin" → difficulty indicator
- **Common errors**: Troubleshooting sections → fix scenarios
- **Related concepts**: Links → theme connections

### 7. Validate Feasibility

Before proposing, check:

1. Can this be simulated in a Kind cluster?
2. Is there a clear "broken state" and "fixed state"?
3. Can we validate the outcome programmatically?
4. Are the required objective validators available?

### 8. Handle Missing Features

Si une idée de challenge nécessite une fonctionnalité manquante (validator, prerequisite, etc.) :

1. **Vérifier le schema** : `kubeasy:get_challenge_schema` pour les objective types disponibles
2. **Si manquant** : Ouvrir un ticket sur `kubeasy-dev/kubeasy-cli`

#### Template de ticket GitHub

```markdown
## Feature Request: [Nom de la feature]

### Context
Je travaille sur un challenge "[slug]" qui enseigne [concept].

### Besoin
[Description de ce qui manque]

### Cas d'usage
Le challenge nécessite de valider que [description de la validation].

### Proposition
Nouveau type d'objective ou paramètre :

```yaml
objectives:
  - key: example
    type: [nouveau_type]
    spec:
      [structure proposée]
```

### Alternatives considérées
[Autres approches possibles et pourquoi elles ne conviennent pas]
```

3. **Sauvegarder l'idée** avec le lien vers l'issue dans le champ `Related Issue`

### 9. Save Ideas

Write challenge ideas to `/Users/paul/Workspace/kubeasy/challenges_ideas/`:

```markdown
# Challenge Idea: <title>

## Source
- K8s Doc: <url>
- Section: <path>

## Concept
<what-this-teaches>

## Proposed Challenge

### Metadata
- **Theme**: <theme>
- **Type**: <fix|build|migrate>
- **Difficulty**: <easy|medium|hard>
- **Estimated Time**: <minutes>

### Scenario
<realistic-situation-description>

### Broken State
<what-manifests-would-look-like>

### Expected Solution
<what-user-should-discover>

### Objectives
<what-validations-needed>

## Feasibility
- [ ] Simulable in Kind
- [ ] Clear fix path
- [ ] Validators available
- [ ] No bypass possible

## Blockers
<any-issues-or-missing-features>

## Related Issue
<link-to-github-issue-if-opened>
```

## Prioritization

Rank ideas by:

1. **CKA/CKAD relevance**: Exam topics get priority
2. **Theme coverage**: Fill gaps in underrepresented themes
3. **Practical importance**: Real-world debugging scenarios
4. **Implementation feasibility**: Avoid ideas needing major CLI changes

## Example Gap Analysis

```
Themes with < 2 challenges:
- scheduling-affinity (0)
- ingress-tls (0)
- jobs-cronjobs (1)

Priority K8s docs to mine:
- concepts/scheduling-eviction/assign-pod-node/
- concepts/services-networking/ingress/
- concepts/workloads/controllers/cron-jobs/
```
