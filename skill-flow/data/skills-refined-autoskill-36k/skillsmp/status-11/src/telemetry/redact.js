// Minimal PII redaction utilities used by the telemetry emitter.
'use strict'

const PII_KEY_RE = /(email|name|ssn|phone|address|credit|card|cc|token)/i
const EMAIL_RE = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i

function isPlainObject(v) {
  return v && typeof v === 'object' && !Array.isArray(v)
}

function redactValue(v) {
  if (typeof v !== 'string') return v
  if (EMAIL_RE.test(v)) return '[REDACTED_EMAIL]'
  // crude phone/credit detection
  if (/\b\d{3}[- ]?\d{2,4}[- ]?\d{2,4}\b/.test(v)) return '[REDACTED]'
  return v
}

function redact(obj) {
  if (Array.isArray(obj)) return obj.map(redact)
  if (!isPlainObject(obj)) return redactValue(obj)

  const out = {}
  for (const k of Object.keys(obj)) {
    const v = obj[k]
    if (PII_KEY_RE.test(k)) {
      out[k] = typeof v === 'string' ? redactValue(v) : '[REDACTED]'
      continue
    }
    if (Array.isArray(v)) out[k] = v.map(item => (isPlainObject(item) ? redact(item) : redactValue(item)))
    else if (isPlainObject(v)) out[k] = redact(v)
    else out[k] = redactValue(v)
  }
  return out
}

module.exports = { redact }
