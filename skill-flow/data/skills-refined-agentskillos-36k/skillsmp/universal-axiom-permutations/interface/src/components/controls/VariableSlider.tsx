import './VariableSlider.css';

interface VariableSliderProps {
    label: string;
    sublabel?: string;
    value: number;
    min: number;
    max: number;
    step: number;
    onChange: (value: number) => void;
    color?: 'foundation' | 'dynamic' | 'cognitive';
}

export function VariableSlider({
    label,
    sublabel,
    value,
    min,
    max,
    step,
    onChange,
    color = 'foundation'
}: VariableSliderProps) {
    const percentage = ((value - min) / (max - min)) * 100;

    return (
        <div className={`variable-slider variable-slider--${color}`}>
            <div className="variable-slider__header">
                <span className="variable-slider__label">
                    {label}
                    {sublabel && <span className="variable-slider__sublabel">{sublabel}</span>}
                </span>
                <span className="variable-slider__value">{value.toFixed(2)}</span>
            </div>
            <div className="variable-slider__track-container">
                <input
                    type="range"
                    className="variable-slider__input"
                    min={min}
                    max={max}
                    step={step}
                    value={value}
                    onChange={(e) => onChange(parseFloat(e.target.value))}
                    style={{
                        '--progress': `${percentage}%`
                    } as React.CSSProperties}
                />
            </div>
            <div className="variable-slider__range">
                <span>{min}</span>
                <span>{max}</span>
            </div>
        </div>
    );
}
