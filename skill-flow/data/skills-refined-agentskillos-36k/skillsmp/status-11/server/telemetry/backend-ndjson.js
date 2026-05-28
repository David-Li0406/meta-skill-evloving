'use strict'

const fs = require('fs')
const path = require('path')

const LOG_DIR = path.join(__dirname)
const LOG_FILE = path.join(LOG_DIR, 'events.ndjson')

function ensureDir() {
  if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true })
}

function emit(event) {
  try {
    ensureDir()
    // If event looks like a wrapped { received_at, payload } keep that shape
    if (event && event.received_at && event.payload) fs.appendFileSync(LOG_FILE, JSON.stringify(event) + '\n', 'utf8')
    else fs.appendFileSync(LOG_FILE, JSON.stringify({ received_at: new Date().toISOString(), payload: event }) + '\n', 'utf8')
  } catch (e) {
    console.error('ndjson backend write failed', e)
  }
}

module.exports = { emit }
