---
name: plan-validation
description: Interactive plan validation loop with modification and regeneration options
order: 5

skip_if:
  - flag: "--continue"

next:
  default: implement
  conditions:
    - if: "user_choice == 'stop'"
      then: STOP
    - if: "flag == '--plan-only'"
      then: STOP

tools:
  - Read
  - Write
  - AskUserQuestion
---

# Step: Plan Validation

<context>
This step presents the plan to the user and handles validation, modification,
or regeneration requests. In AUTO mode, the plan is auto-validated.
In REFINE mode, extended options for challenging the plan are available.
</context>

## Instructions

<instructions>

### 1. Load Plan

Read `.claude/feature/{ticket-id}/plan.md`

### 2. Display Plan Summary

```markdown
# Plan d'implementation: {ticket-id}

## Ticket
- **ID**: {ticket-id}
- **Titre**: {title}
- **Source**: {source}

## Analyse
- **Complexite**: {level}
- **Workflow**: {workflow_type}

## Plan
- **Phases**: {N}
- **Fichier**: .claude/feature/{ticket-id}/plan.md

---

{Full plan content}
```

### 3. Handle AUTO Mode

If `--auto` flag:
1. Auto-validate the plan
2. Update status: `state = "plan_validated"`, `plan_validated_at = "{timestamp}"`
3. Continue to next step

### 4. Handle PLAN-ONLY Mode

If `--plan-only` flag (after auto-validation):

Display next steps:
```markdown
---

## Prochaines etapes

Le plan est sauvegarde dans `.claude/feature/{ticket-id}/plan.md`

**Options**:

1. **Raffiner le plan** (recommande pour les epics complexes):
   ```bash
   /resolve {ticket-id} --refine-plan
   ```

2. **Implementer directement**:
   ```bash
   solo-implement.sh --feature {ticket-id}
   ```
```

**STOP** after displaying.

### 5. INTERACTIVE Mode Options

Apply skill: `~/.claude/skills/plan-validation/SKILL.md`

Present options:

```yaml
AskUserQuestion:
  question: "Que souhaitez-vous faire avec ce plan ?"
  header: "Plan"
  options:
    - label: "Valider et implementer"
      description: "Confirmer le plan, /compact et lancer l'implementation"
    - label: "Valider et arreter"
      description: "Confirmer le plan, continuer plus tard via --continue"
    - label: "Modifier le plan"
      description: "Apporter des changements au plan"
    - label: "Regenerer le plan"
      description: "Relancer la generation avec nouvelles instructions"
```

### 6. REFINE Mode Options

Extended options for `--refine-plan`:

```yaml
AskUserQuestion:
  question: "Comment souhaitez-vous raffiner ce plan ?"
  header: "Raffiner"
  options:
    - label: "Poser des questions"
      description: "Claude identifie les zones d'ombre"
    - label: "Challenger le plan"
      description: "Discuter des choix, trouver les edge cases"
    - label: "Modifier le plan"
      description: "Apporter des changements"
    - label: "Regenerer le plan"
      description: "Relancer avec nouvelles instructions"
```

### 7. Handle User Choice

| Choice | Action |
|--------|--------|
| Valider et implementer | Execute `/compact`, continue to implement |
| Valider et arreter | Update status, STOP |
| Modifier le plan | Apply changes, loop back |
| Regenerer le plan | Delete plan, return to create-plan |
| Poser des questions | Claude analyzes and questions, loop |
| Challenger le plan | Discussion mode, loop |

### 8. Update Status on Validation

```json
{
  "state": "plan_validated",
  "plan_validated_at": "{ISO timestamp}",
  "refined": true  // if REFINE mode
}
```

</instructions>

## Output

<output>
- Status: `state = "plan_validated"`, `plan_validated_at = "{timestamp}"`
- Next: `implement` or `STOP` based on user choice
</output>

## Auto Behavior

<auto_behavior>
- Auto-validate without user interaction
- If `--plan-only`: display plan and STOP
- Otherwise: continue to implement
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
- Display full plan
- Present validation options
- Handle modification/regeneration loops
- Execute `/compact` before implementation
</interactive_behavior>
