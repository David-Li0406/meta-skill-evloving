// Telemetry emitter: emits events to available backends and provides an in-memory/queryable store for tests.
'use strict'

const { redact } = require('./redact')

const DEFAULT_BUFFER_SIZE = 1000

class Telemetry {
  constructor(opts = {}) {
    this.bufferSize = opts.bufferSize || DEFAULT_BUFFER_SIZE
    this.events = [] // circular buffer
    this.backends = []
  }

  addBackend(backend) {
    if (backend && typeof backend.emit === 'function') this.backends.push(backend)
  }

  emit(type, payload = {}) {
    const ts = new Date().toISOString()
    const redacted = redact(payload)
    const event = { type, timestamp: ts, payload: redacted }
    // validate against schema if available
    try {
      const { validate } = require('./schema')
      const res = validate(type, redacted)
      if (!res.valid) {
        // emit a validation event instead of storing the invalid payload
        const v = { type: 'validation', timestamp: ts, payload: { valid: false, errors: res.errors, originalType: type } }
        this._push(v)
        for (const b of this.backends) { try { b.emit(v) } catch (e) {} }
        return
      }
    } catch (e) {
      // ignore schema failures
    }

    this._push(event)
    for (const b of this.backends) {
      try { b.emit(event) } catch (e) { console.error('telemetry backend emit failed', e) }
    }
  }

  _push(event) {
    this.events.push(event)
    if (this.events.length > this.bufferSize) this.events.shift()
  }

  query(filterFn) {
    if (!filterFn) return this.events.slice()
    return this.events.filter(filterFn)
  }

  clear() { this.events = [] }
}

// Singleton for browser/demo usage
const defaultTelemetry = new Telemetry()

module.exports = { Telemetry, defaultTelemetry }
