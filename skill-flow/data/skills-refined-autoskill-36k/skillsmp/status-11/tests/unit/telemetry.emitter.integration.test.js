const { defaultTelemetry } = require('../../src/telemetry/emitter')

describe('telemetry emitter buffer', () => {
  beforeEach(() => { defaultTelemetry.clear() })

  test('emit stores redacted events in buffer and backends are called', () => {
    const calls = []
    const fakeBackend = { emit: (ev) => calls.push(ev) }
    defaultTelemetry.addBackend(fakeBackend)

    defaultTelemetry.emit('generation', { sessionId: 's-1', userEmail: 'alice@example.com', choice: 'X' })

    const events = defaultTelemetry.query()
    expect(events.length).toBe(1)
    expect(events[0].type).toBe('generation')
    // redaction should replace email
    expect(JSON.stringify(events[0].payload)).toMatch('REDACTED')
    expect(calls.length).toBe(1)
  })
})
