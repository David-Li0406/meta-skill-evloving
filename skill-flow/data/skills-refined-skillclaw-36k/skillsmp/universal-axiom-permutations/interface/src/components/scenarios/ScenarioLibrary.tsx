import { useState } from 'react';
import { SCENARIOS, Scenario } from './scenarios';
import { ScenarioCard } from './ScenarioCard';
import { AxiomParams } from '../../hooks/useAxiom';
import './ScenarioLibrary.css';

interface ScenarioLibraryProps {
    onLoadScenario: (params: AxiomParams) => void;
    currentScenario: Scenario | null;
    onScenarioSelect: (scenario: Scenario) => void;
}

export function ScenarioLibrary({
    onLoadScenario,
    currentScenario,
    onScenarioSelect
}: ScenarioLibraryProps) {
    const [filter, setFilter] = useState<'all' | 'educational' | 'real-world' | 'dynamic'>('all');

    const filteredScenarios = filter === 'all'
        ? SCENARIOS
        : SCENARIOS.filter(s => s.category === filter);

    const handleLoad = (scenario: Scenario) => {
        onScenarioSelect(scenario);
        onLoadScenario(scenario.params);
    };

    return (
        <div className="scenario-library">
            <div className="scenario-library__header">
                <h3 className="scenario-library__title">Explore Scenarios</h3>
                <div className="scenario-library__filters">
                    <button
                        className={`scenario-filter ${filter === 'all' ? 'scenario-filter--active' : ''}`}
                        onClick={() => setFilter('all')}
                    >
                        All
                    </button>
                    <button
                        className={`scenario-filter ${filter === 'educational' ? 'scenario-filter--active' : ''}`}
                        onClick={() => setFilter('educational')}
                    >
                        Educational
                    </button>
                    <button
                        className={`scenario-filter ${filter === 'real-world' ? 'scenario-filter--active' : ''}`}
                        onClick={() => setFilter('real-world')}
                    >
                        Real-World
                    </button>
                    <button
                        className={`scenario-filter ${filter === 'dynamic' ? 'scenario-filter--active' : ''}`}
                        onClick={() => setFilter('dynamic')}
                    >
                        Dynamic
                    </button>
                </div>
            </div>

            <div className="scenario-library__list">
                {filteredScenarios.map(scenario => (
                    <ScenarioCard
                        key={scenario.id}
                        scenario={scenario}
                        onLoad={handleLoad}
                        isActive={currentScenario?.id === scenario.id}
                    />
                ))}
            </div>
        </div>
    );
}
