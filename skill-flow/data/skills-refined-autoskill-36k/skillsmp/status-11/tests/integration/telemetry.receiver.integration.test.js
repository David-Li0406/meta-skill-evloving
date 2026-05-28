const path = require('path')
const fs = require('fs')
const { spawn } = require('child_process')
const http = require('http')

const RECEIVER = path.join(__dirname, '../../server/telemetry/receiver.js')
const OUTFILE = path.join(__dirname, '../../server/telemetry/events.ndjson')

function waitForFile(file, timeout = 3000) {
  const start = Date.now()
  return new Promise((resolve, reject) => {
    ;(function poll() {
      if (fs.existsSync(file) && fs.statSync(file).size > 0) return resolve(true)
      if (Date.now() - start > timeout) return reject(new Error('timeout'))
      setTimeout(poll, 100)
    })()
  })
}

describe('telemetry receiver', () => {
  let child
  beforeAll((done) => {
    // remove outfile if exists
    try { fs.unlinkSync(OUTFILE) } catch (e) {}
    child = spawn(process.execPath, [RECEIVER], { stdio: ['ignore', 'pipe', 'pipe'], env: process.env })
    child.stdout.on('data', (d) => {
      const s = d.toString()
      if (/listening/.test(s)) done()
    })
    child.stderr.on('data', (d) => {})
  })

  afterAll(() => { if (child) child.kill() })

  test('POST director_decision is persisted to ndjson', async () => {
    const payload = JSON.stringify({ type: 'director_decision', proposal_id: 'p-test', decision: 'approve' })
    await new Promise((res, rej) => {
      const req = http.request({ method: 'POST', port: 4005, path: '/', headers: { 'Content-Type': 'application/json' } }, (r) => {
        expect(r.statusCode).toBe(200)
        res()
      })
      req.on('error', rej)
      req.write(payload)
      req.end()
    })

    await waitForFile(OUTFILE)
    const lines = fs.readFileSync(OUTFILE, 'utf8').trim().split('\n')
    const last = JSON.parse(lines[lines.length - 1])
    expect(last.payload.type).toBe('director_decision')
    expect(last.payload.proposal_id).toBe('p-test')
  })
})
