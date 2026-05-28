'use strict'

function emit(event) {
  // keep a concise log format
  try {
    console.log('[TELEMETRY]', event.type, event.timestamp, JSON.stringify(event.payload))
  } catch (e) {
    console.log('[TELEMETRY]', event.type, event.timestamp)
  }
}

module.exports = { emit }
