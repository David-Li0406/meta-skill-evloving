import { Scenario } from './scenarios';
import './ScenarioCard.css';

interface ScenarioCardProps {
    scenario: Scenario;
    onLoad: (scenario: Scenario) => void;
    isActive?: boolean;
}

export function ScenarioCard({ scenario, onLoad, isActive = false }: ScenarioCardProps) {
    return (
        <div
            className={`scenario-card scenario-card--${scenario.category} ${isActive ? 'scenario-card--active' : ''}`}
            onClick={() => onLoad(scenario)}
        >
            <div className="scenario-card__icon">{scenario.icon}</div>
            <div className="scenario-card__content">
                <h4 className="scenario-card__title">{scenario.title}</h4>
                <span className="scenario-card__subtitle">{scenario.subtitle}</span>
            </div>
            <div className="scenario-card__arrow">→</div>
        </div>
    );
}
