import { useRef } from 'react'
import './MainMenu.css'

type MainMenuProps = {
  onSelectDashboard: () => void
  onSelectBenchmarking: () => void
  onSelectMathSolutions: () => void
}

export function MainMenu({
  onSelectDashboard,
  onSelectBenchmarking,
  onSelectMathSolutions,
}: MainMenuProps) {
  const sliderRef = useRef<HTMLDivElement>(null)

  const slides = [
    {
      tag: 'Intro · Axiom',
      title: 'The Universal Axiom',
      description:
        'A single intelligence equation that fuses impulses, elements, and pressure with exponential growth, Fibonacci regulation, and cognitive axes.',
      icon: '✨',
      gradient: 'linear-gradient(135deg, #fef9c3 0%, #38bdf8 45%, #a855f7 100%)',
    },
    {
      tag: 'Intro · Application',
      title: 'How it applies',
      description:
        'Use the axiom to orchestrate system states, score emergent behavior, and map reasoning layers across models, agents, and research signals.',
      icon: '🛰️',
      gradient: 'linear-gradient(135deg, #22c55e 0%, #06b6d4 50%, #1d4ed8 100%)',
    },
    {
      tag: 'Intro · Difference',
      title: 'Why it is different',
      description:
        'It treats intelligence as a living waveform: calibrated by growth, bounded by natural regulation, and aligned to purpose and time.',
      icon: '🧬',
      gradient: 'linear-gradient(135deg, #f97316 0%, #ec4899 45%, #8b5cf6 100%)',
    },
    {
      tag: 'Visual · Foundation',
      title: 'Impulse vectors',
      description: 'Trace A, B, C alignment and watch the base layer energize every downstream signal.',
      icon: '🧭',
      gradient: 'linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%)',
    },
    {
      tag: 'Visual · Dynamics',
      title: 'Exponential surge',
      description: 'Monitor Eₙ acceleration curves and anticipate nonlinear inflection points.',
      icon: '📈',
      gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
    },
    {
      tag: 'Visual · Regulation',
      title: 'Fibonacci gating',
      description: 'Use natural sequencing to dampen volatility while sustaining momentum.',
      icon: '🌀',
      gradient: 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)',
    },
    {
      tag: 'Visual · Cognition',
      title: 'Subjectivity scale',
      description: 'Place intelligence outputs on the 7-level objectivity ladder.',
      icon: '🧠',
      gradient: 'linear-gradient(135deg, #14b8a6 0%, #0ea5e9 100%)',
    },
    {
      tag: 'Visual · Purpose',
      title: 'Why-axis intent',
      description: 'Align every decision with the mission vector and purpose-weighted reasoning.',
      icon: '🎯',
      gradient: 'linear-gradient(135deg, #fb7185 0%, #facc15 100%)',
    },
    {
      tag: 'Visual · TimeSphere',
      title: 'Temporal continuity',
      description: 'Stitch past, present, and emergent forecasts into a coherent timeline.',
      icon: '⏳',
      gradient: 'linear-gradient(135deg, #38bdf8 0%, #34d399 100%)',
    },
    {
      tag: 'Visual · Signals',
      title: 'Signal coherence',
      description: 'Blend live telemetry with axiom outputs to verify system integrity.',
      icon: '📡',
      gradient: 'linear-gradient(135deg, #f472b6 0%, #818cf8 100%)',
    },
    {
      tag: 'Visual · Synthesis',
      title: 'Cross-layer synthesis',
      description: 'Aggregate intelligence pulses from every layer into a single score.',
      icon: '🧩',
      gradient: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
    },
    {
      tag: 'Visual · Calibration',
      title: 'Calibration lens',
      description: 'Tune parameters and see immediate shifts in Intelligenceₙ.',
      icon: '🎛️',
      gradient: 'linear-gradient(135deg, #f97316 0%, #fb7185 100%)',
    },
    {
      tag: 'Visual · Benchmark',
      title: 'Benchmark overlay',
      description: 'Compare models side-by-side using the same axiom snapshot.',
      icon: '⚖️',
      gradient: 'linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%)',
    },
    {
      tag: 'Visual · Mission',
      title: 'Mission arc',
      description: 'Project long-horizon objectives and track convergence to intent.',
      icon: '🚀',
      gradient: 'linear-gradient(135deg, #facc15 0%, #f97316 100%)',
    },
    {
      tag: 'Visual · Coordination',
      title: 'Agent choreography',
      description: 'Map how agents hand off reasoning while staying axiom-aligned.',
      icon: '🤝',
      gradient: 'linear-gradient(135deg, #34d399 0%, #2dd4bf 100%)',
    },
    {
      tag: 'Visual · Proof',
      title: 'Proof archives',
      description: 'Link derivations, evidence, and math solutions into a living library.',
      icon: '📚',
      gradient: 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)',
    },
  ]

  const scrollSlides = (direction: 'left' | 'right') => {
    const slider = sliderRef.current
    if (!slider) return
    const scrollAmount = slider.clientWidth * 0.75
    slider.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth',
    })
  }

  return (
    <div className="main-menu">
      <header className="main-menu__header">
        <p className="main-menu__eyebrow">Universal Axiom Interface</p>
        <h1 className="main-menu__title">Command the Intelligence Stack</h1>
        <p className="main-menu__subtitle">
          Orchestrate the Universal Axiom engine and benchmark emergent systems from a single launchpad.
        </p>
        <div className="main-menu__highlights">
          <div className="main-menu__highlight">
            <p className="main-menu__highlight-label">Engine sync</p>
            <p className="main-menu__highlight-value">98% coherence · live data feed</p>
          </div>
          <div className="main-menu__highlight">
            <p className="main-menu__highlight-label">Active modules</p>
            <p className="main-menu__highlight-value">Dashboard · Benchmarks · Math Solutions</p>
          </div>
          <div className="main-menu__highlight">
            <p className="main-menu__highlight-label">Last pulse</p>
            <p className="main-menu__highlight-value">Moments ago · all signals green</p>
          </div>
        </div>
      </header>

      <section className="main-menu__story">
        <div className="main-menu__story-header">
          <div>
            <p className="main-menu__story-eyebrow">Intro slides</p>
            <h2 className="main-menu__story-title">Explore the axiom before launching modules</h2>
            <p className="main-menu__story-subtitle">
              Swipe horizontally to review the core framework, then dive into the operational modules.
            </p>
          </div>
          <div className="main-menu__story-controls">
            <button
              type="button"
              className="main-menu__story-btn"
              onClick={() => scrollSlides('left')}
              aria-label="Scroll slides left"
            >
              ←
            </button>
            <button
              type="button"
              className="main-menu__story-btn"
              onClick={() => scrollSlides('right')}
              aria-label="Scroll slides right"
            >
              →
            </button>
          </div>
        </div>
        <div className="main-menu__story-track" ref={sliderRef}>
          {slides.map((slide) => (
            <article key={slide.title} className="main-menu__slide">
              <div className="main-menu__slide-visual" style={{ background: slide.gradient }}>
                <span className="main-menu__slide-icon">{slide.icon}</span>
                <span className="main-menu__slide-glow" aria-hidden="true" />
              </div>
              <div className="main-menu__slide-body">
                <p className="main-menu__slide-tag">{slide.tag}</p>
                <h3 className="main-menu__slide-title">{slide.title}</h3>
                <p className="main-menu__slide-text">{slide.description}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <div className="main-menu__grid">
        <button type="button" className="main-menu__card" onClick={onSelectDashboard}>
          <div className="main-menu__card-header">
            <span className="main-menu__card-icon">📊</span>
            <h2 className="main-menu__card-title">Intelligence Ops Dashboard</h2>
          </div>
          <p className="main-menu__card-description">
            Tune A/B/C, trace Intelligence<sub>n</sub>, and watch coherence react in real time across the stack.
          </p>
          <span className="main-menu__card-action">Enter command view →</span>
        </button>

        <button type="button" className="main-menu__card" onClick={onSelectBenchmarking}>
          <div className="main-menu__card-header">
            <span className="main-menu__card-icon">⚡</span>
            <h2 className="main-menu__card-title">Model Benchmark Lab</h2>
          </div>
          <p className="main-menu__card-description">
            Stage scenarios, compare outputs, and capture performance deltas with ready-to-share summaries.
          </p>
          <span className="main-menu__card-action">Open benchmarking →</span>
        </button>

        <button type="button" className="main-menu__card" onClick={onSelectMathSolutions}>
          <div className="main-menu__card-header">
            <span className="main-menu__card-icon">🧠</span>
            <h2 className="main-menu__card-title">Math Solutions Hub</h2>
          </div>
          <p className="main-menu__card-description">
            Curate Erdos problem proofs, align insights to the axiom, and coordinate your reasoning workflow.
          </p>
          <span className="main-menu__card-action">Open math solutions →</span>
        </button>
      </div>

      <section className="main-menu__footer">
        <div className="main-menu__status">
          <div>
            <h3>System pulse</h3>
            <p>All modules synced. Telemetry steady. Ready for your next directive.</p>
          </div>
          <div className="main-menu__status-pill">Online</div>
        </div>
      </section>
    </div>
  )
}
