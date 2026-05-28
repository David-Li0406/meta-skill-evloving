// Minimal telemetry schema validator. Keeps rules simple to avoid runtime deps.
'use strict'

function missing(field) { return `missing required field: ${field}` }

const SCHEMAS = {
  generation: {
    required: ['sessionId'],
  },
  validation: {
    required: ['valid'],
  },
  director_decision: {
    required: ['proposal_id', 'decision'],
  },
  presentation: {
    required: ['content'],
  },
  choice: {
    required: ['choice_id', 'text'],
  },
  outcome: {
    required: ['outcome_type'],
  }
}

function validate(type, payload) {
  const schema = SCHEMAS[type]
  if (!schema) return { valid: false, errors: [`unknown event type: ${type}`] }
  const errors = []
  for (const f of (schema.required || [])) {
    if (payload == null || (typeof payload === 'object' && !(f in payload))) errors.push(missing(f))
  }
  return { valid: errors.length === 0, errors }
}

module.exports = { validate }
