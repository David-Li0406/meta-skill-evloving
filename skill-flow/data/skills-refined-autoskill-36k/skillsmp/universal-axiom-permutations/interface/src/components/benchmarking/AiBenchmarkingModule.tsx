import { useEffect, useMemo, useState, type ChangeEvent } from 'react'
import './AiBenchmarkingModule.css'

type AiBenchmarkingModuleProps = {
  onBackToMenu?: () => void
}

export function AiBenchmarkingModule({ onBackToMenu }: AiBenchmarkingModuleProps) {
  const [inputs, setInputs] = useState({
    a: 0.82,
    b: 0.76,
    c: 0.68,
    x: 0.9,
    y: 0.88,
    z: 0.94,
    en: 1.2,
    fn: 3,
  })
  const [iterations, setIterations] = useState(25)
  const [isRunning, setIsRunning] = useState(true)
  const [tick, setTick] = useState(0)
  const [visibleModels, setVisibleModels] = useState({
    cognitive: true,
    stability: true,
    emergence: true,
  })

  useEffect(() => {
    if (!isRunning) {
      return
    }
    const interval = window.setInterval(() => {
      setTick((prev) => prev + 1)
    }, 600)
    return () => window.clearInterval(interval)
  }, [isRunning])

  const fibonacci = useMemo(() => [1, 1, 2, 3, 5, 8, 13, 21, 34, 55], [])

  const intelligence = useMemo(() => {
    const { a, b, c, x, y, z, en, fn } = inputs
    return en * (1 + fn) * x * y * z * (a * b * c)
  }, [inputs])

  const modelSeries = useMemo(() => {
    const base = intelligence
    const length = 12
    const buildSeries = (modifier: number, phase: number) =>
      Array.from({ length }, (_, index) => {
        const time = index + tick * 0.35 + phase
        const fibo = fibonacci[(index + tick) % fibonacci.length]
        const oscillation = 1 + Math.sin(time / 2) * 0.12 + Math.cos(time / 4) * 0.08
        return base * modifier * oscillation * (1 + fibo / 144)
      })

    return {
      cognitive: buildSeries(1.05, 0),
      stability: buildSeries(0.92, 1.7),
      emergence: buildSeries(1.18, 3.1),
    }
  }, [fibonacci, intelligence, tick])

  const distribution = useMemo(() => {
    const { a, b, c, x, y, z, en, fn } = inputs
    return [
      { label: 'A', value: a },
      { label: 'B', value: b },
      { label: 'C', value: c },
      { label: 'X', value: x },
      { label: 'Y', value: y },
      { label: 'Z', value: z },
      { label: 'Eₙ', value: en / 2 },
      { label: 'Fₙ', value: fn / 10 },
    ]
  }, [inputs])

  const buildPolyline = (values: number[], width = 600, height = 200, padding = 20) => {
    const min = Math.min(...values)
    const max = Math.max(...values)
    const range = max - min || 1
    return values
      .map((value, index) => {
        const x = padding + (index / (values.length - 1)) * (width - padding * 2)
        const y = height - padding - ((value - min) / range) * (height - padding * 2)
        return `${x},${y}`
      })
      .join(' ')
  }

  const handleInputChange = (key: keyof typeof inputs) => (event: ChangeEvent<HTMLInputElement>) => {
    setInputs((prev) => ({
      ...prev,
      [key]: Number(event.target.value),
    }))
  }

  const toggleModel = (key: keyof typeof visibleModels) => {
    setVisibleModels((prev) => ({
      ...prev,
      [key]: !prev[key],
    }))
  }

  return (
    <div className="benchmarking">
      <header className="benchmarking__header">
        <div>
          <p className="benchmarking__eyebrow">Benchmarking Suite</p>
          <h1 className="benchmarking__title">AI Benchmarking Module</h1>
          <p className="benchmarking__subtitle">
            Configure evaluation runs, compare output coherence, and export multi-model performance summaries.
          </p>
        </div>
        {onBackToMenu && (
          <button type="button" className="benchmarking__back-btn" onClick={onBackToMenu}>
            ← Main Menu
          </button>
        )}
      </header>

      <section className="benchmarking__overview">
        <div className="benchmarking__stat">
          <span className="benchmarking__stat-label">Active Scenarios</span>
          <span className="benchmarking__stat-value">12</span>
        </div>
        <div className="benchmarking__stat">
          <span className="benchmarking__stat-label">Models Loaded</span>
          <span className="benchmarking__stat-value">4</span>
        </div>
        <div className="benchmarking__stat">
          <span className="benchmarking__stat-label">Run Status</span>
          <span className="benchmarking__stat-value benchmarking__stat-value--ready">Ready</span>
        </div>
      </section>

      <section className="benchmarking__grid">
        <article className="benchmarking__panel">
          <h2>Scenario Library</h2>
          <p>Select benchmark modes aligned to reasoning, memory, and stability tests.</p>
          <ul>
            <li>Universal Axiom reasoning stack</li>
            <li>Multi-step coherence checks</li>
            <li>Conflict resolution stress test</li>
          </ul>
        </article>
        <article className="benchmarking__panel">
          <h2>Evaluation Metrics</h2>
          <p>Track performance metrics with emphasis on cross-language parity.</p>
          <ul>
            <li>Intelligence delta vs baseline</li>
            <li>Consistency across runs</li>
            <li>Fibonacci regulation adherence</li>
          </ul>
        </article>
        <article className="benchmarking__panel">
          <h2>Run Configuration</h2>
          <p>Adjust run count, model roster, and export targets before launch.</p>
          <div className="benchmarking__controls">
            <label>
              Iterations
              <input
                type="number"
                value={iterations}
                min={5}
                max={100}
                onChange={(event) => setIterations(Number(event.target.value))}
              />
            </label>
            <label>
              Output Format
              <select defaultValue="summary">
                <option value="summary">Summary Report</option>
                <option value="full">Full Trace</option>
                <option value="csv">CSV Export</option>
              </select>
            </label>
          </div>
        </article>
      </section>

      <section className="benchmarking__simulations">
        <header className="benchmarking__simulations-header">
          <div>
            <p className="benchmarking__eyebrow">Dynamic Simulation Lab</p>
            <h2>Interactive Axiom Applications</h2>
            <p>
              Adjust the Universal Axiom variables and watch multi-model behaviors evolve in real time across
              stability, cognition, and emergent systems.
            </p>
          </div>
          <div className="benchmarking__simulations-actions">
            <button
              type="button"
              className="benchmarking__action-btn"
              onClick={() => setIsRunning((prev) => !prev)}
            >
              {isRunning ? 'Pause Simulation' : 'Resume Simulation'}
            </button>
            <button type="button" className="benchmarking__action-btn" onClick={() => setTick(0)}>
              Reset Waveform
            </button>
          </div>
        </header>

        <div className="benchmarking__simulations-grid">
          <article className="benchmarking__card">
            <h3>Axiom Control Surface</h3>
            <p>Map each variable to real-time influence curves and observe Intelligenceₙ modulation.</p>
            <div className="benchmarking__sliders">
              {(
                [
                  { key: 'a', label: 'A — Impulses' },
                  { key: 'b', label: 'B — Elements' },
                  { key: 'c', label: 'C — Pressure' },
                  { key: 'x', label: 'X — Subjectivity' },
                  { key: 'y', label: 'Y — Purpose' },
                  { key: 'z', label: 'Z — TimeSphere' },
                ] as const
              ).map(({ key, label }) => (
                <label key={key}>
                  <span>{label}</span>
                  <input
                    type="range"
                    min={0.4}
                    max={1.4}
                    step={0.02}
                    value={inputs[key]}
                    onChange={handleInputChange(key)}
                  />
                  <strong>{inputs[key].toFixed(2)}</strong>
                </label>
              ))}
              <label>
                <span>Eₙ — Exponential Growth</span>
                <input type="range" min={0.6} max={2} step={0.05} value={inputs.en} onChange={handleInputChange('en')} />
                <strong>{inputs.en.toFixed(2)}</strong>
              </label>
              <label>
                <span>Fₙ — Fibonacci Regulator</span>
                <input type="range" min={1} max={8} step={1} value={inputs.fn} onChange={handleInputChange('fn')} />
                <strong>{inputs.fn}</strong>
              </label>
            </div>
            <div className="benchmarking__intelligence">
              <div>
                <span>Intelligenceₙ</span>
                <strong>{intelligence.toFixed(3)}</strong>
              </div>
              <div>
                <span>Iterations</span>
                <strong>{iterations}</strong>
              </div>
              <div>
                <span>Wave Tick</span>
                <strong>{tick}</strong>
              </div>
            </div>
          </article>

          <article className="benchmarking__card benchmarking__card--chart">
            <div className="benchmarking__card-header">
              <div>
                <h3>Multi-Model Intelligence Curves</h3>
                <p>Simulated benchmarks combining oscillation, Fibonacci regulation, and Eₙ amplification.</p>
              </div>
              <div className="benchmarking__toggles">
                {(
                  [
                    { key: 'cognitive', label: 'Cognitive' },
                    { key: 'stability', label: 'Stability' },
                    { key: 'emergence', label: 'Emergence' },
                  ] as const
                ).map(({ key, label }) => (
                  <button
                    key={key}
                    type="button"
                    className={`benchmarking__toggle ${visibleModels[key] ? 'is-active' : ''}`}
                    onClick={() => toggleModel(key)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>
            <div className="benchmarking__chart">
              <svg viewBox="0 0 600 200" role="img" aria-label="Intelligence curves">
                <defs>
                  <linearGradient id="benchmarking-grid" x1="0" x2="1" y1="0" y2="0">
                    <stop offset="0%" stopColor="rgba(126, 243, 177, 0.1)" />
                    <stop offset="100%" stopColor="rgba(98, 175, 255, 0.1)" />
                  </linearGradient>
                </defs>
                <rect x="0" y="0" width="600" height="200" fill="url(#benchmarking-grid)" rx="16" />
                <g className="benchmarking__grid-lines">
                  {[40, 80, 120, 160].map((y) => (
                    <line key={y} x1="24" x2="576" y1={y} y2={y} />
                  ))}
                </g>
                {visibleModels.cognitive && (
                  <polyline
                    className="benchmarking__line benchmarking__line--cognitive"
                    points={buildPolyline(modelSeries.cognitive)}
                  />
                )}
                {visibleModels.stability && (
                  <polyline
                    className="benchmarking__line benchmarking__line--stability"
                    points={buildPolyline(modelSeries.stability)}
                  />
                )}
                {visibleModels.emergence && (
                  <polyline
                    className="benchmarking__line benchmarking__line--emergence"
                    points={buildPolyline(modelSeries.emergence)}
                  />
                )}
              </svg>
              <div className="benchmarking__legend">
                <span className="legend--cognitive">Cognitive</span>
                <span className="legend--stability">Stability</span>
                <span className="legend--emergence">Emergence</span>
              </div>
            </div>
          </article>

          <article className="benchmarking__card">
            <h3>Contribution Distribution</h3>
            <p>Visualize how each variable contributes to the composite intelligence signal.</p>
            <div className="benchmarking__bars">
              {distribution.map((item) => (
                <div key={item.label} className="benchmarking__bar">
                  <span>{item.label}</span>
                  <div className="benchmarking__bar-track">
                    <div className="benchmarking__bar-fill" style={{ width: `${Math.min(item.value * 70, 100)}%` }} />
                  </div>
                  <strong>{item.value.toFixed(2)}</strong>
                </div>
              ))}
            </div>
            <div className="benchmarking__signal-grid">
              {modelSeries.emergence.slice(0, 8).map((value, index) => (
                <div key={`${value}-${index}`} className="benchmarking__signal">
                  <span>Node {index + 1}</span>
                  <strong>{value.toFixed(2)}</strong>
                  <div className="benchmarking__signal-pulse" style={{ animationDelay: `${index * 0.3}s` }} />
                </div>
              ))}
            </div>
          </article>
        </div>
      </section>

      <section className="benchmarking__cta">
        <div>
          <h3>Launch Benchmark Run</h3>
          <p>Start a new benchmarking cycle and sync the results to the analytics console.</p>
        </div>
        <button type="button" className="benchmarking__run-btn">Start Run</button>
      </section>
    </div>
  )
}
