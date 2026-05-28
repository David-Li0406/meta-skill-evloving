import './DynamicContext.css';
import { Scenario, SCENARIOS } from '../scenarios/scenarios';
import { AxiomParams } from '../../hooks/useAxiom';

interface DynamicContextProps {
    scenario: Scenario | null;
    currentParams: AxiomParams;
}

export function DynamicContext({ scenario, currentParams }: DynamicContextProps) {
    const title = scenario ? scenario.title : 'The Architecture of Organic Intelligence';
    const subtitle = scenario ? scenario.subtitle : 'Principles of The Universal Axiom';

    // Default narrative
    const defaultText = 'At its core, organic intelligence is a living balance. It starts with raw "Impulses" (Your Drive) and "Elements" (Your Facts). These are your raw materials. The "Cognitive Layer" then filters these through "Objectivity" and "Purpose." When everything aligns, intelligence flows. When they clash, you get "Internal Friction" or bias.';

    const content = scenario ? scenario.detailedContext : defaultText;
    const cta = scenario ? scenario.cta : 'Experiment with the "Growth Stage (n)" slider to see how intelligence compounds over time.';

    /**
     * Contextual Logic Engine
     * Prioritizes scenario-specific insights, then drifts, then general state feedback.
     */
    const getReactiveInsight = () => {
        if (scenario) {
            const base = scenario.params;
            const insights = scenario.reactiveInsights;
            const diffs = {
                impulses: currentParams.impulses - base.impulses,
                pressure: currentParams.pressure - base.pressure,
                subjectivity: currentParams.subjectivity - base.subjectivity,
                purpose: currentParams.purpose - base.purpose
            };

            // 1. Check for Contextual Drift (Am I becoming a different scenario?)
            // We search for a scenario that matches our current params better than the active one
            const driftScenario = SCENARIOS.find(s => {
                if (s.id === scenario.id) return false;
                const dist = Math.sqrt(
                    Math.pow(currentParams.impulses - s.params.impulses, 2) +
                    Math.pow(currentParams.pressure - s.params.pressure, 2) +
                    Math.pow(currentParams.subjectivity * 10 - s.params.subjectivity * 10, 2) +
                    Math.pow(currentParams.purpose * 10 - s.params.purpose * 10, 2)
                );
                return dist < 1.5; // Threshold for drift detection
            });

            if (driftScenario) {
                return `🌀 Drift Detected: Your current balance is beginning to resemble "${driftScenario.title}." ${insights.drift || "The context is shifting."}`;
            }

            // 2. Scenario-Specific Reactions
            if (diffs.pressure > 3 && insights.highPressure) return insights.highPressure;
            if (diffs.subjectivity > 0.4 && insights.highBias) return insights.highBias;
            if (currentParams.purpose < 0.2 && insights.lowPurpose) return insights.lowPurpose;
            if (currentParams.purpose > 1.2 && insights.highPurpose) return insights.highPurpose;
            if (currentParams.impulses < base.impulses - 4 && insights.lowImpulse) return insights.lowImpulse;

            // 3. Fallback to specific but generic alerts if scenario insight is missing
            if (diffs.pressure > 4) return `⚠️ High Pressure Alert: You've added a lot of internal friction to this ${scenario.title}. It's getting harder for the cognitive layer to synthesize a clear output.`;

            return `🎯 Live State: Currently tracking close to the ${scenario.title} ideal. Keep exploring!`;
        } else {
            // General balance feedback for default view
            if (currentParams.pressure > 7 && currentParams.subjectivity > 0.6) return "🧱 Stuck State: High Pressure and High Bias usually mean you're in a rabbit hole. Try lowering both to see clearly.";
            if (currentParams.purpose > 1.2) return "🏹 Focused Drive: Your Purpose is exceptionally high. This is where breakthroughs happen.";
            if (currentParams.impulses < 1) return "💤 Dormant Mind: Without foundational impulse, the multipliers have nothing to work with.";
            if (currentParams.pressure < 1 && currentParams.subjectivity < 0.1 && currentParams.purpose > 0.9) return "💎 Peak Coherence: You've found a state of high clarity. Everything is flowing perfectly.";
            return "🌱 Balanced Flux: The system is in a healthy state of discovery. Tune the dials to find a specific scenario.";
        }
    };

    const reactiveInsight = getReactiveInsight();

    return (
        <div className="dynamic-context">
            <div className="dynamic-context__header">
                <div className="dynamic-context__icon">
                    {scenario ? scenario.icon : '🧠'}
                </div>
                <div className="dynamic-context__titles">
                    <h3 className="dynamic-context__title">{title}</h3>
                    <p className="dynamic-context__subtitle">{subtitle}</p>
                </div>
            </div>

            <div className="dynamic-context__body">
                <p className="dynamic-context__text">{content}</p>

                <div className="dynamic-context__reactive" key={reactiveInsight}>
                    <span>{reactiveInsight}</span>
                </div>

                <div className="dynamic-context__cta">
                    <span className="dynamic-context__cta-icon">💡</span>
                    <span className="dynamic-context__cta-text">{cta}</span>
                </div>
            </div>

            <div className="dynamic-context__footer">
                <div className="dynamic-context__tags">
                    <span className="dynamic-context__tag">{scenario ? 'Scenario Analysis' : 'System Overview'}</span>
                    <span className="dynamic-context__tag dynamic-context__tag--live">Live Intelligence Feed</span>
                </div>
            </div>
        </div>
    );
}
