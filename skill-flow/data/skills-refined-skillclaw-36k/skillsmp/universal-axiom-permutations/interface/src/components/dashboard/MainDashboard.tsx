import { useState } from 'react';
import { FoundationPanel } from '../layers/FoundationPanel';
import { DynamicPanel } from '../layers/DynamicPanel';
import { CognitivePanel } from '../layers/CognitivePanel';
import { VariableSlider } from '../controls/VariableSlider';
import { IntelligenceGraph } from '../visualizations/IntelligenceGraph';
import { ScenarioLibrary } from '../scenarios/ScenarioLibrary';
import { NarrativeOverlay } from '../scenarios/NarrativeOverlay';
import { AnimatedNumber } from '../effects/AnimatedNumber';
import { Scenario } from '../scenarios/scenarios';
import { useAxiom } from '../../hooks/useAxiom';
import { DynamicContext } from './DynamicContext';
import '../layers/LayerPanel.css';
import './MainDashboard.css';

type MainDashboardProps = {
    onBackToMenu?: () => void;
};

export function MainDashboard({ onBackToMenu }: MainDashboardProps) {
    const { params, state, coherence, setParam, setParams, resetParams } = useAxiom();
    const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
    const [showNarrative, setShowNarrative] = useState(false);

    const handleLoadScenario = (scenarioParams: typeof params) => {
        setParams(scenarioParams);
    };

    const handleScenarioSelect = (scenario: Scenario) => {
        setCurrentScenario(scenario);
        setShowNarrative(true);
    };

    const handleCloseNarrative = () => {
        setShowNarrative(false);
    };

    const handleReset = () => {
        resetParams();
        setCurrentScenario(null);
    };

    return (
        <div className="dashboard">
            <header className="dashboard__header">
                <div className="dashboard__title-group">
                    <h1 className="dashboard__title">The Universal Axiom</h1>
                    <span className="dashboard__subtitle">Dynamic Explorer</span>
                </div>
                <div className="dashboard__actions">
                    {onBackToMenu && (
                        <button className="dashboard__nav-btn" onClick={onBackToMenu}>
                            ← Main Menu
                        </button>
                    )}
                    {currentScenario && (
                        <span className="dashboard__scenario-badge">
                            {currentScenario.icon} {currentScenario.title}
                        </span>
                    )}
                    <button className="dashboard__reset-btn" onClick={handleReset}>
                        ↺ Reset
                    </button>
                </div>
            </header>

            <div className="dashboard__formula">
                <span className="formula">Intelligence<sub>n</sub> = E<sub>n</sub> · (1 + F<sub>n</sub>) · X · Y · Z · (A · B · C)</span>
            </div>

            <div className="dashboard__visualization">
                <IntelligenceGraph
                    currentParams={{
                        impulses: params.impulses,
                        elements: params.elements,
                        pressure: params.pressure,
                        subjectivity: params.subjectivity,
                        purpose: params.purpose,
                        time: params.time
                    }}
                    currentN={params.n}
                />
                <ScenarioLibrary
                    onLoadScenario={handleLoadScenario}
                    currentScenario={currentScenario}
                    onScenarioSelect={handleScenarioSelect}
                />
            </div>

            <div className="dashboard__layers">
                <FoundationPanel
                    impulses={state.foundation.A_impulses}
                    elements={state.foundation.B_elements}
                    pressure={state.foundation.C_pressure}
                    product={state.foundation.product}
                />
                <DynamicPanel
                    n={state.n}
                    E_n={state.dynamic.E_n}
                    F_n={state.dynamic.F_n}
                    product={state.dynamic.product}
                />
                <CognitivePanel
                    subjectivity={state.cognitive.X_subjectivity}
                    objectivity={state.cognitive.X_objectivity}
                    purpose={state.cognitive.Y_purpose}
                    time={state.cognitive.Z_time}
                    product={state.cognitive.product}
                />
            </div>

            <div className="dashboard__intelligence">
                <div className="intelligence-display">
                    <span className="intelligence-display__label">Intelligence</span>
                    <AnimatedNumber
                        value={state.intelligence}
                        className="intelligence-display__value"
                        formatOptions={{ maximumFractionDigits: 1 }}
                    />
                    <div className="intelligence-display__coherence">
                        <span>Coherence</span>
                        <div className="coherence-bar">
                            <div
                                className="coherence-bar__fill"
                                style={{ width: `${coherence * 100}%` }}
                            />
                        </div>
                        <span className="coherence-percent">{Math.round(coherence * 100)}%</span>
                    </div>
                </div>

                <DynamicContext scenario={currentScenario} currentParams={params} />
            </div>

            <div className="dashboard__controls">
                <div className="controls-section">
                    <h3 className="controls-section__title">Foundation Layer</h3>
                    <div className="controls-section__grid">
                        <VariableSlider
                            label="A"
                            sublabel="Impulses"
                            value={params.impulses}
                            min={-10}
                            max={10}
                            step={0.1}
                            onChange={(v) => setParam('impulses', v)}
                            color="foundation"
                        />
                        <VariableSlider
                            label="B"
                            sublabel="Elements"
                            value={params.elements}
                            min={-10}
                            max={10}
                            step={0.1}
                            onChange={(v) => setParam('elements', v)}
                            color="foundation"
                        />
                        <VariableSlider
                            label="C"
                            sublabel="Pressure"
                            value={params.pressure}
                            min={0}
                            max={10}
                            step={0.1}
                            onChange={(v) => setParam('pressure', v)}
                            color="foundation"
                        />
                    </div>
                </div>

                <div className="controls-section">
                    <h3 className="controls-section__title">Cognitive Layer</h3>
                    <div className="controls-section__grid">
                        <VariableSlider
                            label="X"
                            sublabel="Subjectivity"
                            value={params.subjectivity}
                            min={0}
                            max={1}
                            step={0.01}
                            onChange={(v) => setParam('subjectivity', v)}
                            color="cognitive"
                        />
                        <VariableSlider
                            label="Y"
                            sublabel="Purpose"
                            value={params.purpose}
                            min={0}
                            max={2}
                            step={0.01}
                            onChange={(v) => setParam('purpose', v)}
                            color="cognitive"
                        />
                        <VariableSlider
                            label="Z"
                            sublabel="Time"
                            value={params.time}
                            min={0}
                            max={2}
                            step={0.01}
                            onChange={(v) => setParam('time', v)}
                            color="cognitive"
                        />
                    </div>
                </div>

                <div className="controls-section">
                    <h3 className="controls-section__title">Dynamic Layer</h3>
                    <div className="controls-section__grid controls-section__grid--single">
                        <VariableSlider
                            label="n"
                            sublabel="Growth Stage"
                            value={params.n}
                            min={1}
                            max={15}
                            step={1}
                            onChange={(v) => setParam('n', v)}
                            color="dynamic"
                        />
                    </div>
                </div>
            </div>

            {showNarrative && (
                <NarrativeOverlay
                    scenario={currentScenario}
                    onClose={handleCloseNarrative}
                />
            )}
        </div>
    );
}
