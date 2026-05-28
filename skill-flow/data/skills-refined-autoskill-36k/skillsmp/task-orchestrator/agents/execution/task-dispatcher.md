---
name: task-dispatcher
description: Dispatche les tâches vers les skills cibles pour exécution
version: 1.0.0
---

# Agent Task Dispatcher

Tu es spécialisé dans le **dispatch des tâches** vers les skills appropriés.

## Ta Responsabilité Unique

> Envoyer les tâches prêtes aux skills cibles et suivre leur prise en charge.

## Processus de Dispatch

```javascript
async function dispatch(task) {
  // 1. Valider que la tâche est dispatchable
  if (task.state.current !== 'SCHEDULED') {
    return { error: 'task_not_scheduled' };
  }

  // 2. Résoudre le skill cible
  const target = resolveTarget(task.definition);

  // 3. Préparer le contexte d'exécution
  const executionContext = {
    task_id: task.id,
    intake_id: task.intake_id,
    skill: target.skill,
    agent: target.agent,
    input: prepareInput(task),
    config: {
      timeout_ms: getTimeout(task),
      retries: task.execution.max_retries || 3,
      callback_url: getCallbackUrl(task.id)
    }
  };

  // 4. Transition vers IN_PROGRESS
  await transitionState(task, 'IN_PROGRESS', {
    dispatched_at: new Date().toISOString()
  });

  // 5. Dispatcher
  const dispatchResult = await sendToSkill(target, executionContext);

  // 6. Enregistrer le dispatch
  task.execution.dispatched_at = new Date().toISOString();
  task.execution.dispatch_id = dispatchResult.dispatch_id;
  task.execution.target = target;

  return {
    success: true,
    dispatch_id: dispatchResult.dispatch_id,
    target,
    estimated_completion: dispatchResult.eta
  };
}
```

## Résolution du Target

```javascript
function resolveTarget(definition) {
  // Cible explicite
  if (definition.skill_target && definition.entry_point) {
    return {
      skill: definition.skill_target,
      agent: definition.entry_point
    };
  }

  // Résolution par type
  const typeMapping = {
    'brief_analysis': { skill: 'project-management', agent: 'avant-projet/brief-analysis' },
    'tech_scoping': { skill: 'direction-technique', agent: 'avant-projet/technical-scoping' },
    'code_review': { skill: 'lead-dev', agent: 'code-review/quality-check' },
    // ...
  };

  return typeMapping[definition.type] || resolveByKeywords(definition);
}
```

## Préparation de l'Input

```javascript
function prepareInput(task) {
  return {
    // Contexte de la tâche
    task_context: {
      id: task.id,
      type: task.definition.type,
      description: task.definition.description
    },

    // Données du client
    client_context: task.context.client,

    // Données du projet
    project_context: task.context.project,

    // Requirements extraits
    requirements: task.context.requirements,

    // Outputs des tâches précédentes (si workflow)
    previous_outputs: task.context.previous_outputs || [],

    // Configuration spécifique
    config: task.definition.config || {}
  };
}
```

## Template de Sortie

```json
{
  "dispatch": {
    "task_id": "TASK-2024-001234",
    "dispatch_id": "DSP-2024-001234",
    "dispatched_at": "2024-01-15T11:00:00Z",

    "target": {
      "skill": "project-management",
      "agent": "avant-projet/brief-analysis",
      "version": "1.0.0"
    },

    "input": {
      "task_context": {
        "id": "TASK-2024-001234",
        "type": "brief_analysis"
      },
      "client_context": {
        "name": "StartupIO",
        "contact": "Marie Martin"
      }
    },

    "config": {
      "timeout_ms": 3600000,
      "retries": 3,
      "callback_url": "https://orchestrator/callback/TASK-2024-001234"
    },

    "acknowledgment": {
      "received_by": "project-management",
      "ack_at": "2024-01-15T11:00:05Z",
      "estimated_duration_ms": 7200000
    },

    "status": "dispatched"
  }
}
```

## Gestion des Timeouts

```javascript
const timeoutConfig = {
  // Par type de tâche
  brief_analysis: 2 * 60 * 60 * 1000,    // 2h
  tech_scoping: 4 * 60 * 60 * 1000,       // 4h
  code_review: 1 * 60 * 60 * 1000,        // 1h
  development: 8 * 60 * 60 * 1000,        // 8h
  testing: 4 * 60 * 60 * 1000,            // 4h

  // Défaut
  default: 2 * 60 * 60 * 1000             // 2h
};

async function monitorTimeout(task) {
  const timeout = getTimeout(task);
  const startTime = new Date(task.execution.dispatched_at);

  setTimeout(async () => {
    const currentTask = await getTask(task.id);

    if (currentTask.state.current === 'IN_PROGRESS') {
      // Timeout atteint, tâche toujours en cours
      await handleTimeout(currentTask);
    }
  }, timeout);
}

async function handleTimeout(task) {
  // Notifier le skill
  await sendTimeoutWarning(task);

  // Attendre un grace period
  await sleep(5 * 60 * 1000); // 5 min

  const updatedTask = await getTask(task.id);
  if (updatedTask.state.current === 'IN_PROGRESS') {
    // Toujours pas de réponse, marquer comme failed
    await transitionState(task, 'FAILED', {
      reason: 'timeout',
      timeout_ms: getTimeout(task)
    });
  }
}
```

## Communication avec les Skills

```javascript
// Interface de communication
const skillInterface = {
  // Dispatch synchrone (pour tâches courtes)
  sync: async (target, context) => {
    const response = await invokeSkill(target.skill, target.agent, context);
    return { type: 'sync', result: response };
  },

  // Dispatch asynchrone (pour tâches longues)
  async: async (target, context) => {
    const dispatchId = await queueForSkill(target.skill, target.agent, context);
    return { type: 'async', dispatch_id: dispatchId };
  }
};

// Callback quand le skill termine
async function handleSkillCallback(dispatchId, result) {
  const task = await getTaskByDispatchId(dispatchId);

  await collectResult(task, result);
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Dispatch ID | Identifiant unique du dispatch |
| Target | Skill et agent ciblés |
| Acknowledgment | Confirmation de prise en charge |
| Status | État du dispatch |
