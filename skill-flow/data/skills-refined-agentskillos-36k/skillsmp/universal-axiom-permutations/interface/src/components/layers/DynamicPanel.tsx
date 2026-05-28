import './DynamicPanel.css';

interface DynamicPanelProps {
    n: number;
    E_n: number;
    F_n: number;
    product: number;
}

export function DynamicPanel({ n, E_n, F_n, product }: DynamicPanelProps) {
    return (
        <div className="layer-panel dynamic-panel">
            <div className="layer-panel__header">
                <h2 className="layer-panel__title">Dynamic Layer</h2>
                <span className="layer-panel__formula">E<sub>n</sub> · (1 + F<sub>n</sub>)</span>
            </div>

            <div className="layer-panel__content">
                <div className="dynamic-values">
                    <div className="dynamic-value">
                        <span className="dynamic-value__label">E<sub>n</sub></span>
                        <span className="dynamic-value__number">{E_n.toLocaleString()}</span>
                        <span className="dynamic-value__formula">2·3<sup>{n}</sup> − 1</span>
                    </div>
                    <div className="dynamic-value">
                        <span className="dynamic-value__label">F<sub>n</sub></span>
                        <span className="dynamic-value__number">{F_n.toLocaleString()}</span>
                        <span className="dynamic-value__formula">Fibonacci</span>
                    </div>
                </div>

                <div className="layer-panel__result">
                    <span className="layer-panel__result-label">Product</span>
                    <span className="layer-panel__result-value layer-panel__result-value--positive">
                        {product.toLocaleString()}
                    </span>
                </div>

                <div className="dynamic-stage">
                    <span className="dynamic-stage__label">Growth Stage</span>
                    <span className="dynamic-stage__value">n = {n}</span>
                </div>
            </div>
        </div>
    );
}
