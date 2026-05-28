import './CognitivePanel.css';

interface CognitivePanelProps {
    subjectivity: number;
    objectivity: number;
    purpose: number;
    time: number;
    product: number;
}

export function CognitivePanel({
    subjectivity,
    objectivity,
    purpose,
    time,
    product
}: CognitivePanelProps) {
    const coherenceLevel = objectivity > 0.7 && purpose > 0.7 ? 'high' : objectivity > 0.4 ? 'medium' : 'low';

    return (
        <div className="layer-panel cognitive-panel">
            <div className="layer-panel__header">
                <h2 className="layer-panel__title">Cognitive Layer</h2>
                <span className="layer-panel__formula">X × Y × Z</span>
            </div>

            <div className="layer-panel__content">
                <div className="cognitive-scales">
                    <div className="cognitive-scale">
                        <div className="cognitive-scale__header">
                            <span className="cognitive-scale__label">Objectivity (X)</span>
                            <span className="cognitive-scale__value">{objectivity.toFixed(2)}</span>
                        </div>
                        <div className="cognitive-scale__bar">
                            <div
                                className="cognitive-scale__fill cognitive-scale__fill--objectivity"
                                style={{ width: `${objectivity * 100}%` }}
                            />
                        </div>
                        <div className="cognitive-scale__range">
                            <span>Subjective</span>
                            <span>Objective</span>
                        </div>
                    </div>

                    <div className="cognitive-scale">
                        <div className="cognitive-scale__header">
                            <span className="cognitive-scale__label">Purpose (Y)</span>
                            <span className="cognitive-scale__value">{purpose.toFixed(2)}</span>
                        </div>
                        <div className="cognitive-scale__bar">
                            <div
                                className="cognitive-scale__fill cognitive-scale__fill--purpose"
                                style={{ width: `${Math.min(purpose, 1) * 100}%` }}
                            />
                        </div>
                        <div className="cognitive-scale__range">
                            <span>Unclear</span>
                            <span>Clear</span>
                        </div>
                    </div>

                    <div className="cognitive-scale">
                        <div className="cognitive-scale__header">
                            <span className="cognitive-scale__label">Time (Z)</span>
                            <span className="cognitive-scale__value">{time.toFixed(2)}</span>
                        </div>
                        <div className="cognitive-scale__bar">
                            <div
                                className="cognitive-scale__fill cognitive-scale__fill--time"
                                style={{ width: `${Math.min(time, 1) * 100}%` }}
                            />
                        </div>
                        <div className="cognitive-scale__range">
                            <span>0</span>
                            <span>1</span>
                        </div>
                    </div>
                </div>

                <div className="layer-panel__result">
                    <span className="layer-panel__result-label">Product</span>
                    <span className="layer-panel__result-value">{product.toFixed(3)}</span>
                </div>

                <div className={`cognitive-coherence cognitive-coherence--${coherenceLevel}`}>
                    Coherence: {coherenceLevel.charAt(0).toUpperCase() + coherenceLevel.slice(1)}
                    {coherenceLevel === 'high' && ' ✓'}
                </div>
            </div>
        </div>
    );
}
