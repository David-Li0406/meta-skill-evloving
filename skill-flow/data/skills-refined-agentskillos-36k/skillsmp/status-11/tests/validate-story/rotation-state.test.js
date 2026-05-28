/** @jest-environment ./tests/helpers/node-no-webstorage-environment.js */
const fs = require('fs')
const path = require('path')
const os = require('os')
const cp = require('child_process')

const CLI = path.resolve(__dirname, '../../scripts/validate-story.js')

function runCLI(args, env = {}) {
  return cp.spawnSync(process.execPath, [CLI, ...args], { encoding: 'utf8', env: { ...process.env, ...env } })
}

describe('validate-story state and rotation', () => {
  const fixturesDir = path.resolve(__dirname, '../fixtures')
  const branching = path.join(fixturesDir, 'validate-story', 'branching.ink')
  const singleChoice = path.join(fixturesDir, 'validate-story', 'single-choice.ink')

  test('creates state file and records lastPath/runCount', () => {
    const tmpState = path.join(os.tmpdir(), `validate-state-${Date.now()}.json`)
    const r1 = runCLI(['--story', branching, '--state-file', tmpState, '--output', 'stdout'])
    expect(r1.status).toBe(0)
    const state = JSON.parse(fs.readFileSync(tmpState, 'utf8'))
    expect(state[branching]).toBeDefined()
    expect(Array.isArray(state[branching].lastPath)).toBe(true)
    expect(typeof state[branching].lastRunAt).toBe('string')
    expect(state[branching].runCount).toBe(1)

    const r2 = runCLI(['--story', branching, '--state-file', tmpState, '--output', 'stdout'])
    expect(r2.status).toBe(0)
    const state2 = JSON.parse(fs.readFileSync(tmpState, 'utf8'))
    expect(state2[branching].runCount).toBe(2)
    fs.unlinkSync(tmpState)
  })

  test('avoids repeating last choice when alternatives exist', () => {
    const tmpState = path.join(os.tmpdir(), `validate-state-${Date.now()}.json`)
    const first = runCLI(['--story', branching, '--state-file', tmpState, '--output', 'stdout', '--seed', '2'])
    expect(first.status).toBe(0)
    const second = runCLI(['--story', branching, '--state-file', tmpState, '--output', 'stdout', '--seed', '2'])
    const p1 = JSON.parse(first.stdout.trim())
    const p2 = JSON.parse(second.stdout.trim())
    const r1 = Array.isArray(p1) ? p1[0] : p1
    const r2 = Array.isArray(p2) ? p2[0] : p2
    expect(r1.path).not.toEqual(r2.path)
    fs.unlinkSync(tmpState)
  })

  test('exits non-zero when no alternate choice remains', () => {
    const tmpState = path.join(os.tmpdir(), `validate-state-${Date.now()}.json`)
    const first = runCLI(['--story', singleChoice, '--state-file', tmpState, '--output', 'stdout', '--seed', '1'])
    expect(first.status).toBe(0)
    const second = runCLI(['--story', singleChoice, '--state-file', tmpState, '--output', 'stdout', '--seed', '1', '--max-retries', '1'])
    expect(second.status).not.toBe(0)
    const parsed = JSON.parse(second.stdout.trim())
    const res = Array.isArray(parsed) ? parsed[0] : parsed
    expect(res.pass).toBe(false)
    expect(res.error).toMatch(/No alternative/)
    fs.unlinkSync(tmpState)
  })
})
