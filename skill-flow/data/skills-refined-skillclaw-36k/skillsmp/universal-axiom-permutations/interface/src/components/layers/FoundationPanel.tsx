import './FoundationPanel.css';

interface FoundationPanelProps {
    impulses: number;
    elements: number;
    pressure: number;
    product: number;
}

function getSign(value: number): 'positive' | 'negative' | 'near-zero' {
    if (Math.abs(value) < 0.1) return 'near-zero';
    return value > 0 ? 'positive' : 'negative';
}

export function FoundationPanel({
    impulses,
    elements,
    pressure,
    product
}: FoundationPanelProps) {
    const productSign = getSign(product);

    return (
        <div className="layer-panel foundation-panel">
            <div className="layer-panel__header">
                <h2 className="layer-panel__title">Foundation Layer</h2>
                <span className="layer-panel__formula">A × B × C</span>
            </div>

            <div className="layer-panel__content">
                <div className="foundation-blocks">
                    <div className={`foundation-block foundation-block--${getSign(impulses)}`}>
                        <span className="foundation-block__label">A</span>
                        <span className="foundation-block__value">{impulses.toFixed(1)}</span>
                        <span className="foundation-block__name">Impulses</span>
                    </div>
                    <span className="foundation-operator">×</span>
                    <div className={`foundation-block foundation-block--${getSign(elements)}`}>
                        <span className="foundation-block__label">B</span>
                        <span className="foundation-block__value">{elements.toFixed(1)}</span>
                        <span className="foundation-block__name">Elements</span>
                    </div>
                    <span className="foundation-operator">×</span>
                    <div className={`foundation-block foundation-block--${getSign(pressure)}`}>
                        <span className="foundation-block__label">C</span>
                        <span className="foundation-block__value">{pressure.toFixed(1)}</span>
                        <span className="foundation-block__name">Pressure</span>
                    </div>
                </div>

                <div className="layer-panel__result">
                    <span className="layer-panel__result-label">Product</span>
                    <span className={`layer-panel__result-value layer-panel__result-value--${productSign}`}>
                        {product.toFixed(2)}
                    </span>
                </div>

                <div className={`layer-panel__status layer-panel__status--${productSign}`}>
                    {productSign === 'positive' && '✓ Positive'}
                    {productSign === 'negative' && '⚠ Negative'}
                    {productSign === 'near-zero' && '⚠ Near Zero'}
                </div>
            </div>
        </div>
    );
}
