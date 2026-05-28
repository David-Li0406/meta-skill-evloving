import { useEffect, useState } from 'react';
import { Scenario } from './scenarios';
import './NarrativeOverlay.css';

interface NarrativeOverlayProps {
    scenario: Scenario | null;
    onClose: () => void;
}

export function NarrativeOverlay({ scenario, onClose }: NarrativeOverlayProps) {
    const [displayedNarrative, setDisplayedNarrative] = useState('');
    const [showInsight, setShowInsight] = useState(false);

    useEffect(() => {
        if (!scenario) {
            setDisplayedNarrative('');
            setShowInsight(false);
            return;
        }

        // Typewriter effect
        let index = 0;
        setDisplayedNarrative('');
        setShowInsight(false);

        const typeInterval = setInterval(() => {
            if (index < scenario.narrative.length) {
                setDisplayedNarrative(scenario.narrative.slice(0, index + 1));
                index++;
            } else {
                clearInterval(typeInterval);
                setTimeout(() => setShowInsight(true), 300);
            }
        }, 20);

        return () => clearInterval(typeInterval);
    }, [scenario]);

    if (!scenario) return null;

    return (
        <div className="narrative-overlay" onClick={onClose}>
            <div className="narrative-overlay__content" onClick={e => e.stopPropagation()}>
                <button className="narrative-overlay__close" onClick={onClose}>×</button>

                <div className="narrative-overlay__header">
                    <span className="narrative-overlay__icon">{scenario.icon}</span>
                    <div>
                        <h2 className="narrative-overlay__title">{scenario.title}</h2>
                        <span className="narrative-overlay__subtitle">{scenario.subtitle}</span>
                    </div>
                </div>

                <div className="narrative-overlay__narrative">
                    <p>{displayedNarrative}<span className="narrative-cursor">|</span></p>
                </div>

                <div className={`narrative-overlay__insight ${showInsight ? 'narrative-overlay__insight--visible' : ''}`}>
                    <span className="narrative-overlay__insight-label">💡 Key Insight</span>
                    <p>{scenario.insight}</p>
                </div>

                <div className="narrative-overlay__params">
                    <span className="narrative-overlay__params-label">Configuration</span>
                    <div className="narrative-overlay__params-grid">
                        <div className="narrative-param">
                            <span className="narrative-param__label">A</span>
                            <span className="narrative-param__value">{scenario.params.impulses}</span>
                        </div>
                        <div className="narrative-param">
                            <span className="narrative-param__label">B</span>
                            <span className="narrative-param__value">{scenario.params.elements}</span>
                        </div>
                        <div className="narrative-param">
                            <span className="narrative-param__label">C</span>
                            <span className="narrative-param__value">{scenario.params.pressure}</span>
                        </div>
                        <div className="narrative-param">
                            <span className="narrative-param__label">X</span>
                            <span className="narrative-param__value">{scenario.params.subjectivity}</span>
                        </div>
                        <div className="narrative-param">
                            <span className="narrative-param__label">Y</span>
                            <span className="narrative-param__value">{scenario.params.purpose}</span>
                        </div>
                        <div className="narrative-param">
                            <span className="narrative-param__label">n</span>
                            <span className="narrative-param__value">{scenario.params.n}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
