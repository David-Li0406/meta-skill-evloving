---
name: plan-validation
description: Interactive plan validation loop for /resolve. Displays plan, offers modification/regeneration options, handles validation states.
---

# Plan Validation Skill

Interactive validation loop for implementation plans. Allows users to review, modify, regenerate, or validate plans before implementation.

## Input Requirements

- `ticket_id`: The ticket identifier
- `plan_path`: Path to plan file (`.claude/feature/{ticket-id}/plan.md`)
- `status_path`: Path to status file (`.claude/feature/{ticket-id}/status.json`)
- `mode`: Either "interactive", "auto", or "refine"

## Behavior by Mode

### AUTO Mode

In AUTO mode, the plan is validated automatically without user interaction:

1. Mark plan as validated
2. Update status:
   ```json
   {
     "state": "plan_validated",
     "plan_validated_at": "{ISO timestamp}"
   }
   ```
3. Return `continue_to_implement: true`

### INTERACTIVE Mode

In INTERACTIVE mode, enter the validation loop described below.

### REFINE Mode

REFINE mode is similar to INTERACTIVE mode but with additional options for deep plan analysis:

1. Display plan summary (same as INTERACTIVE)
2. Present extended options including "Poser des questions" and "Challenger le plan"
3. Enter refinement loop (see "Refine-Specific Options" below)

## Validation Loop

### 1. Display Plan Summary

```markdown
# Plan d'implementation: {ticket-id}

## Ticket
- **ID**: {ticket-id}
- **Titre**: {title}
- **Source**: {source}

## Analyse
- **Complexite**: {level}
- **Workflow**: {workflow_type}
- **Exploration**: {exploration_status}

## Plan
- **Phases**: {N}
- **Fichier**: .claude/feature/{ticket-id}/plan.md
```

Display the full plan content from the plan file.

### 2. Present Options

**INTERACTIVE mode options:**

```
AskUserQuestion:
  question: "Que souhaitez-vous faire avec ce plan ?"
  header: "Plan"
  options:
    - label: "Valider et implementer"
      description: "Confirmer le plan, executer /compact et lancer l'implementation"
    - label: "Valider et arreter"
      description: "Confirmer le plan, continuer plus tard via --continue"
    - label: "Modifier le plan"
      description: "Apporter des changements au plan"
    - label: "Regenerer le plan"
      description: "Relancer la generation avec nouvelles instructions"
```

**REFINE mode options (extended):**

```
AskUserQuestion:
  question: "Comment souhaitez-vous raffiner ce plan ?"
  header: "Raffiner"
  options:
    - label: "Poser des questions"
      description: "Claude identifie les zones d'ombre et pose des questions"
    - label: "Challenger le plan"
      description: "Discuter des choix techniques, trouver les edge cases"
    - label: "Modifier le plan"
      description: "Apporter des changements au plan"
    - label: "Regenerer le plan"
      description: "Relancer la generation avec nouvelles instructions"

# After refinement discussion:
AskUserQuestion:
  question: "Que faire maintenant ?"
  header: "Suite"
  options:
    - label: "Continuer le raffinement"
      description: "Continuer a challenger et affiner le plan"
    - label: "Valider et implementer"
      description: "Confirmer le plan, /compact et lancer l'implementation"
    - label: "Valider et arreter"
      description: "Confirmer le plan, continuer plus tard via --continue"
```

### 3. Handle User Choice

#### Option: "Poser des questions" (REFINE mode only)

Claude analyzes the plan and identifies potential issues, edge cases, and unclear areas:

1. **Analyze the plan** for:
   - Ambiguous requirements or missing details
   - Edge cases not covered
   - Error handling gaps
   - Performance considerations
   - Security implications
   - Testing scenarios missing

2. **Present questions** to the user:
   ```markdown
   ## Questions sur le plan

   En analysant le plan, j'ai identifie les points suivants:

   ### Edge Cases
   1. Que se passe-t-il si {scenario X} ?
   2. Comment gerer le cas ou {condition Y} ?

   ### Clarifications necessaires
   3. Dans la phase 2, {question about implementation detail}
   4. Pour {component}, avez-vous une preference pour {option A vs B} ?

   ### Risques potentiels
   5. {potential risk} - comment souhaitez-vous le gerer ?
   ```

3. **Discuss answers** with user and update plan if needed

4. Return to options menu (REFINE mode options)

#### Option: "Challenger le plan" (REFINE mode only)

Interactive discussion mode where the user challenges the plan:

1. **Prompt for challenge**:
   ```markdown
   ## Challenger le plan

   Vous pouvez:
   - Questionner les choix techniques
   - Proposer des alternatives
   - Identifier des problemes potentiels
   - Demander des justifications

   Qu'est-ce qui vous preoccupe ou que souhaitez-vous challenger ?
   ```

2. **Claude responds** to challenges:
   - Defends choices with reasoning
   - Acknowledges valid concerns
   - Proposes modifications when appropriate
   - Identifies trade-offs

3. **Apply changes** to plan if agreed upon

4. **Continue discussion** or return to options menu

Example challenge flow:
```
User: "Je pense que la phase 2 est trop complexe, on pourrait simplifier"
Claude: "Vous avez raison, la phase 2 fait X, Y et Z. On pourrait:
  - Option A: Fusionner Y et Z
  - Option B: Deplacer Z en phase 3
  Quelle approche preferez-vous?"
User: "Option A"
Claude: *updates plan* "J'ai mis a jour le plan. Voulez-vous challenger autre chose?"
```

5. Return to options menu when done

#### Option: "Modifier le plan"

```
AskUserQuestion:
  question: "Quelles modifications souhaitez-vous apporter ?"
  header: "Modifications"
  options:
    - label: "Ajouter une phase"
      description: "Inserer une nouvelle etape dans le plan"
    - label: "Modifier une phase"
      description: "Changer le contenu d'une phase existante"
    - label: "Supprimer une phase"
      description: "Retirer une etape du plan"
    - label: "Autre modification"
      description: "Decrire librement les changements"
```

After user describes modifications:
1. Apply changes to plan file
2. Re-display the updated plan
3. Return to step 2 (loop)

#### Option: "Regenerer le plan"

```
AskUserQuestion:
  question: "Quelles instructions pour la nouvelle generation ?"
  header: "Instructions"
  options:
    - label: "Plus simple"
      description: "Reduire le nombre de phases, approche minimaliste"
    - label: "Plus detaille"
      description: "Ajouter plus de details et sous-etapes"
    - label: "Approche differente"
      description: "Utiliser une autre strategie d'implementation"
    - label: "Instructions specifiques"
      description: "Decrire precisement ce que vous voulez"
```

After receiving instructions:
1. Delete current plan
2. Return `regenerate_plan: true` with regeneration context
3. Caller should regenerate plan and call this skill again

#### Option: "Valider et arreter"

1. Update status:
   ```json
   {
     "state": "plan_validated",
     "plan_validated_at": "{ISO timestamp}"
   }
   ```

2. Display next steps:
   ```markdown
   ## Plan Valide

   Le plan a ete enregistre. Pour lancer l'implementation :

   1. Creez d'abord votre branche/worktree:
      ```bash
      git checkout -b {prefix}/{ticket-id}-{slug}
      ```

   2. Puis lancez l'implementation:
      ```bash
      /resolve {ticket-id} --continue
      ```

   Le workflow reprendra avec /compact puis implementation.
   ```

3. Return `stop: true` - Do not continue to implementation

#### Option: "Valider et implementer"

1. Update status:
   ```json
   {
     "state": "plan_validated",
     "plan_validated_at": "{ISO timestamp}"
   }
   ```

2. Remind user about branch:
   ```markdown
   ## Pre-Implementation

   Avant de continuer, assurez-vous d'avoir cree votre branche:
     git checkout -b {prefix}/{ticket-id}-{slug}
   ```

3. Confirm branch ready:
   ```
   AskUserQuestion:
     question: "Branche creee ? Pret pour l'implementation ?"
     header: "Confirm"
     options:
       - label: "Oui, lancer /compact et implementer"
         description: "Vider le contexte et demarrer l'implementation"
       - label: "Annuler"
         description: "Revenir aux options du plan"
   ```

4. If confirmed:
   - Execute `/compact` to clear context
   - Return `continue_to_implement: true`

5. If cancelled:
   - Return to step 2 (loop)

## Output

The skill returns one of:

| Output | Meaning |
|--------|---------|
| `continue_to_implement: true` | Proceed to implementation (after /compact in interactive mode) |
| `stop: true` | Stop workflow, user will resume later via --continue |
| `regenerate_plan: true` | Caller should regenerate plan with provided context |

## Status Updates

This skill updates `.claude/feature/{ticket-id}/status.json`:

**INTERACTIVE mode:**
```json
{
  "state": "plan_validated",
  "plan_validated_at": "2025-01-19T10:30:00+01:00"
}
```

**REFINE mode:**
```json
{
  "state": "plan_validated",
  "plan_validated_at": "2025-01-19T10:30:00+01:00",
  "refined": true
}
```
