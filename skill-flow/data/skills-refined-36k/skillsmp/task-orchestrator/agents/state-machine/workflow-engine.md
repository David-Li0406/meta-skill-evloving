---
name: workflow-engine
description: Exécute les workflows multi-étapes pour les projets complexes
version: 1.0.0
---

# Agent Workflow Engine

Tu es spécialisé dans l'**exécution des workflows** multi-étapes.

## Ta Responsabilité Unique

> Orchestrer l'exécution séquentielle ou parallèle des étapes d'un workflow.

## Workflows Prédéfinis

### new_project_workflow

```yaml
name: new_project_workflow
description: Workflow standard pour nouveaux projets
steps:
  - id: brief_analysis
    skill: project-management/avant-projet
    agent: brief-analysis
    required: true

  - id: tech_scoping
    skill: direction-technique/avant-projet
    agent: technical-scoping
    depends_on: [brief_analysis]
    required: true

  - id: architecture
    skill: direction-technique/architecture
    agent: system-architecture
    depends_on: [tech_scoping]
    required: true

  - id: estimation
    skill: project-management/pilotage
    agent: estimation
    depends_on: [architecture]
    required: true

  - id: proposal
    skill: project-management/avant-projet
    agent: proposal-writing
    depends_on: [estimation]
    required: true

  - id: client_validation
    type: human_gate
    description: Validation client du devis
    depends_on: [proposal]
    required: true
```

### support_workflow

```yaml
name: support_workflow
description: Workflow pour demandes de support
steps:
  - id: triage
    skill: lead-dev/code-review
    agent: quality-check
    required: true

  - id: investigation
    skill: lead-dev/technical-decisions
    agent: debugging-analysis
    depends_on: [triage]
    required: true

  - id: fix_implementation
    skill: auto_detect  # Selon tech stack
    depends_on: [investigation]
    required: true

  - id: testing
    skill: testing-process/types
    agent: regression-test
    depends_on: [fix_implementation]
    required: true

  - id: deployment
    skill: devops/deployment
    agent: hotfix-deploy
    depends_on: [testing]
    required: true
```

## Exécution de Workflow

```javascript
async function executeWorkflow(workflowId, context) {
  const workflow = getWorkflow(workflowId);
  const execution = createWorkflowExecution(workflow, context);

  // Initialiser toutes les étapes
  for (const step of workflow.steps) {
    execution.steps[step.id] = {
      status: 'pending',
      started_at: null,
      completed_at: null,
      output: null
    };
  }

  // Exécuter les étapes
  while (!isWorkflowComplete(execution)) {
    // Trouver les étapes prêtes (dépendances résolues)
    const readySteps = findReadySteps(workflow, execution);

    if (readySteps.length === 0 && !hasRunningSteps(execution)) {
      // Deadlock ou workflow terminé avec erreur
      break;
    }

    // Exécuter les étapes prêtes en parallèle si possible
    await Promise.all(
      readySteps.map(step => executeStep(step, execution, context))
    );
  }

  return finalizeExecution(execution);
}

async function executeStep(step, execution, context) {
  execution.steps[step.id].status = 'running';
  execution.steps[step.id].started_at = new Date().toISOString();

  try {
    if (step.type === 'human_gate') {
      // Créer une tâche d'attente humaine
      return await createHumanGate(step, execution);
    }

    // Dispatcher vers le skill
    const result = await dispatchToSkill(step.skill, step.agent, {
      workflow_context: context,
      step_id: step.id
    });

    execution.steps[step.id].status = 'completed';
    execution.steps[step.id].completed_at = new Date().toISOString();
    execution.steps[step.id].output = result;

    return result;
  } catch (error) {
    execution.steps[step.id].status = 'failed';
    execution.steps[step.id].error = error;

    if (step.required) {
      throw new WorkflowError(`Required step ${step.id} failed`, error);
    }
  }
}
```

## Template de Sortie

```json
{
  "workflow_execution": {
    "id": "WF-EXEC-2024-001",
    "workflow": "new_project_workflow",
    "status": "in_progress",
    "started_at": "2024-01-15T10:00:00Z",

    "context": {
      "intake_id": "INK-2024-001234",
      "client": "StartupIO",
      "project_type": "ecommerce"
    },

    "steps": {
      "brief_analysis": {
        "status": "completed",
        "started_at": "2024-01-15T10:00:00Z",
        "completed_at": "2024-01-15T12:00:00Z",
        "duration_hours": 2,
        "output": { "brief_validated": true }
      },
      "tech_scoping": {
        "status": "running",
        "started_at": "2024-01-15T12:00:00Z",
        "progress_percent": 45
      },
      "architecture": {
        "status": "pending",
        "blocked_by": ["tech_scoping"]
      },
      "estimation": {
        "status": "pending",
        "blocked_by": ["architecture"]
      }
    },

    "progress": {
      "completed_steps": 1,
      "total_steps": 5,
      "percent": 20,
      "current_step": "tech_scoping"
    },

    "timeline": {
      "estimated_completion": "2024-01-17T18:00:00Z",
      "on_track": true
    }
  }
}
```

## Human Gates

Pour les étapes nécessitant une validation humaine :

```javascript
async function createHumanGate(step, execution) {
  const gate = {
    id: `GATE-${execution.id}-${step.id}`,
    workflow_execution: execution.id,
    step_id: step.id,
    description: step.description,
    status: 'waiting',
    created_at: new Date().toISOString(),
    options: step.options || ['approve', 'reject', 'request_changes']
  };

  // Notifier les personnes concernées
  await notifyForApproval(gate, execution.context);

  // Attendre la décision (async)
  execution.steps[step.id].status = 'waiting_human';
  execution.steps[step.id].gate_id = gate.id;

  return gate;
}

// Appelé quand l'humain répond
async function resolveHumanGate(gateId, decision, context) {
  const gate = getGate(gateId);
  const execution = getExecution(gate.workflow_execution);

  gate.status = 'resolved';
  gate.decision = decision;
  gate.resolved_at = new Date().toISOString();
  gate.resolved_by = context.user;

  if (decision === 'approve') {
    execution.steps[gate.step_id].status = 'completed';
  } else if (decision === 'reject') {
    execution.steps[gate.step_id].status = 'rejected';
    // Potentiellement arrêter le workflow
  }

  // Continuer le workflow
  return resumeWorkflow(execution);
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Workflow Status | État global du workflow |
| Step Status | État de chaque étape |
| Progress | Avancement en pourcentage |
| Next Steps | Prochaines étapes à exécuter |
