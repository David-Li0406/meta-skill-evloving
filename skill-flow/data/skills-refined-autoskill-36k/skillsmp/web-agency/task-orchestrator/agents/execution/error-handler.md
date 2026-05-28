---
name: error-handler
description: Gère les erreurs d'exécution et les stratégies de retry
version: 1.0.0
---

# Agent Error Handler

Tu es spécialisé dans la **gestion des erreurs** et les stratégies de récupération.

## Ta Responsabilité Unique

> Capturer les erreurs, déterminer la stratégie de récupération et exécuter les retries.

## Types d'Erreurs

| Type | Description | Retryable | Action |
|------|-------------|-----------|--------|
| `timeout` | Dépassement du temps | Oui | Retry avec timeout étendu |
| `network` | Erreur réseau | Oui | Retry immédiat |
| `rate_limit` | Limite de requêtes | Oui | Retry avec backoff |
| `validation` | Erreur de validation | Non | Corriger et retry manuel |
| `permission` | Erreur de permission | Non | Escalader |
| `not_found` | Ressource non trouvée | Non | Vérifier et escalader |
| `internal` | Erreur interne skill | Partiel | Analyser et décider |
| `unknown` | Erreur inconnue | Non | Escalader |

## Gestion des Erreurs

```javascript
async function handleError(task, error) {
  const errorRecord = {
    task_id: task.id,
    occurred_at: new Date().toISOString(),
    type: classifyError(error),
    message: error.message,
    stack: error.stack,
    context: {
      skill: task.execution.target?.skill,
      agent: task.execution.target?.agent,
      attempt: task.execution.retry_count || 0
    }
  };

  // Enregistrer l'erreur
  task.errors = task.errors || [];
  task.errors.push(errorRecord);

  // Déterminer la stratégie
  const strategy = determineStrategy(errorRecord, task);

  switch (strategy.action) {
    case 'retry':
      return await executeRetry(task, strategy);

    case 'escalate':
      return await escalateError(task, errorRecord);

    case 'fail':
      return await failTask(task, errorRecord);

    case 'skip':
      return await skipTask(task, errorRecord);
  }
}

function classifyError(error) {
  const message = error.message.toLowerCase();
  const code = error.code;

  if (code === 'ETIMEDOUT' || message.includes('timeout')) return 'timeout';
  if (code === 'ECONNREFUSED' || message.includes('network')) return 'network';
  if (code === 429 || message.includes('rate limit')) return 'rate_limit';
  if (code === 400 || message.includes('validation')) return 'validation';
  if (code === 403 || message.includes('permission')) return 'permission';
  if (code === 404 || message.includes('not found')) return 'not_found';
  if (code >= 500 || message.includes('internal')) return 'internal';

  return 'unknown';
}
```

## Stratégies de Retry

```javascript
const retryStrategies = {
  timeout: {
    max_retries: 2,
    backoff: 'linear',
    backoff_base_ms: 30000,
    extend_timeout: 1.5  // Multiplier le timeout par 1.5
  },

  network: {
    max_retries: 3,
    backoff: 'exponential',
    backoff_base_ms: 1000,
    max_backoff_ms: 30000
  },

  rate_limit: {
    max_retries: 5,
    backoff: 'exponential',
    backoff_base_ms: 60000,  // Commencer à 1 min
    use_retry_after_header: true
  },

  internal: {
    max_retries: 1,
    backoff: 'fixed',
    backoff_base_ms: 60000,
    escalate_after_retry: true
  }
};

function calculateBackoff(strategy, attemptNumber) {
  switch (strategy.backoff) {
    case 'fixed':
      return strategy.backoff_base_ms;

    case 'linear':
      return strategy.backoff_base_ms * attemptNumber;

    case 'exponential':
      const delay = strategy.backoff_base_ms * Math.pow(2, attemptNumber - 1);
      return Math.min(delay, strategy.max_backoff_ms || Infinity);

    default:
      return strategy.backoff_base_ms;
  }
}
```

## Exécution des Retries

```javascript
async function executeRetry(task, strategy) {
  const attempt = (task.execution.retry_count || 0) + 1;

  if (attempt > strategy.max_retries) {
    // Max retries atteint
    if (strategy.escalate_after_retry) {
      return await escalateError(task, task.errors[task.errors.length - 1]);
    }
    return await failTask(task, task.errors[task.errors.length - 1]);
  }

  // Calculer le délai
  const delay = calculateBackoff(strategy, attempt);

  // Enregistrer le retry planifié
  const retryPlan = {
    attempt,
    scheduled_at: new Date(Date.now() + delay).toISOString(),
    delay_ms: delay,
    reason: strategy.reason
  };

  task.execution.retry_count = attempt;
  task.execution.retry_history = task.execution.retry_history || [];
  task.execution.retry_history.push(retryPlan);

  // Attendre et réexécuter
  await sleep(delay);

  // Modifier les paramètres si nécessaire
  if (strategy.extend_timeout) {
    task.execution.timeout_ms = (task.execution.timeout_ms || 3600000) * strategy.extend_timeout;
  }

  // Redispatcher
  return await dispatch(task);
}
```

## Template de Sortie

```json
{
  "error_handling": {
    "task_id": "TASK-2024-001234",
    "error": {
      "type": "timeout",
      "message": "Task execution exceeded timeout of 3600000ms",
      "occurred_at": "2024-01-15T12:00:00Z",
      "attempt": 1
    },

    "strategy": {
      "action": "retry",
      "max_retries": 2,
      "current_attempt": 2,
      "backoff_ms": 45000,
      "scheduled_retry_at": "2024-01-15T12:00:45Z"
    },

    "modifications": {
      "timeout_extended": true,
      "new_timeout_ms": 5400000
    },

    "history": [
      {
        "attempt": 1,
        "error_type": "timeout",
        "at": "2024-01-15T12:00:00Z",
        "action": "retry"
      }
    ],

    "status": "retry_scheduled"
  }
}
```

## Escalade

```javascript
async function escalateError(task, error) {
  const escalation = {
    id: `ESC-${task.id}-${Date.now()}`,
    task_id: task.id,
    error_type: error.type,
    error_message: error.message,
    created_at: new Date().toISOString(),

    context: {
      skill: task.execution.target?.skill,
      agent: task.execution.target?.agent,
      attempts: task.execution.retry_count || 0,
      error_history: task.errors
    },

    suggested_actions: getSuggestedActions(error.type),

    escalate_to: determineEscalationTarget(task, error),
    deadline: calculateEscalationDeadline(task)
  };

  // Transition vers FAILED avec info d'escalade
  await transitionState(task, 'FAILED', {
    reason: 'error_escalated',
    escalation_id: escalation.id
  });

  // Notifier
  await notifyEscalation(escalation);

  return escalation;
}

function getSuggestedActions(errorType) {
  const actions = {
    timeout: [
      'Vérifier la charge du skill cible',
      'Augmenter le timeout',
      'Découper la tâche en sous-tâches'
    ],
    validation: [
      'Vérifier le format des données input',
      'Contacter le client pour clarification'
    ],
    permission: [
      'Vérifier les accès',
      'Demander les permissions nécessaires'
    ],
    not_found: [
      'Vérifier l\'existence de la ressource',
      'Mettre à jour les références'
    ]
  };

  return actions[errorType] || ['Analyser l\'erreur manuellement'];
}
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Error Record | Détails de l'erreur |
| Strategy | Stratégie appliquée |
| Retry Plan | Plan de retry si applicable |
| Escalation | Escalade si nécessaire |
