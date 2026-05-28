/** @jest-environment ./tests/helpers/node-no-webstorage-environment.js */
const cp = require('child_process')
const path = require('path')
const fs = require('fs')
const os = require('os')

const CLI = path.resolve(__dirname, '../../scripts/validate-story.js')

function runCLI(args, env = {}){
  const res = cp.spawnSync(process.execPath, [CLI, ...args], {
    encoding: 'utf8',
    env: { ...process.env, ...env },
  })
  return res
}

describe('validate-story CLI integration', () => {
  const fixturesDir = path.resolve(__dirname, '../fixtures')
  const valid = path.join(fixturesDir, 'valid.ink')
  const invalid = path.join(fixturesDir, 'invalid.ink')
  const runtimeErr = path.join(fixturesDir, 'runtime_err.ink')
  const branching = path.join(fixturesDir, 'validate-story', 'branching.ink')

  test('parse failure returns non-zero and error field', () => {
    const r = runCLI(['--story', invalid, '--output', 'stdout'])
    expect(r.status).not.toBe(0)
    const out = r.stdout.trim()
    let parsed = JSON.parse(out)
    if (Array.isArray(parsed) && parsed.length === 1) parsed = parsed[0]
    expect(parsed.error).toBeDefined()
    expect(parsed.pass).toBe(false)
  })

  test('successful run outputs pass true and steps > 0', () => {
    const r = runCLI(['--story', valid, '--seed', '42', '--output', 'stdout'])
    expect(r.status).toBe(0)
    let parsed = JSON.parse(r.stdout.trim())
    if (Array.isArray(parsed) && parsed.length === 1) parsed = parsed[0]
    expect(parsed.pass).toBe(true)
    expect(parsed.steps).toBeGreaterThan(0)
  })

  test('deterministic seeded runs produce same path', () => {
    const r1 = runCLI(['--story', valid, '--seed', '123', '--output', 'stdout', '--state-disabled'])
    const r2 = runCLI(['--story', valid, '--seed', '123', '--output', 'stdout', '--state-disabled'])
    let p1 = JSON.parse(r1.stdout.trim())
    let p2 = JSON.parse(r2.stdout.trim())
    if (Array.isArray(p1) && p1.length === 1) p1 = p1[0]
    if (Array.isArray(p2) && p2.length === 1) p2 = p2[0]
    expect(p1.path).toEqual(p2.path)
  })

  test('state rotation avoids previous choice when alternatives exist', () => {
    const tmpState = path.join(os.tmpdir(), `validate-state-${Date.now()}.json`)
    // first run
    const r1 = runCLI(['--story', branching, '--seed', '7', '--state-file', tmpState, '--output', 'stdout'])
    expect(r1.status).toBe(0)
    let p1 = JSON.parse(r1.stdout.trim())
    // second run should avoid previous choice when alternative exists
    const r2 = runCLI(['--story', branching, '--seed', '7', '--state-file', tmpState, '--output', 'stdout'])
    let p2 = JSON.parse(r2.stdout.trim())
    if (Array.isArray(p1) && p1.length === 1) p1 = p1[0]
    if (Array.isArray(p2) && p2.length === 1) p2 = p2[0]
    expect(p1.path).not.toEqual(p2.path)
    fs.unlinkSync(tmpState)
  })

  test('multi-story glob runs produce aggregated output', () => {
    const r = runCLI(['--story', fixturesDir + '/*.ink', '--output', 'stdout'])
    const parsed = JSON.parse(r.stdout.trim())
    // Expect an array of results
    expect(Array.isArray(parsed)).toBe(true)
    expect(parsed.length).toBeGreaterThanOrEqual(2)
    const anyFail = parsed.some(p => p.pass === false)
    if (anyFail) {
      expect(r.status).not.toBe(0)
    } else {
      expect(r.status).toBe(0)
    }
  })
})
