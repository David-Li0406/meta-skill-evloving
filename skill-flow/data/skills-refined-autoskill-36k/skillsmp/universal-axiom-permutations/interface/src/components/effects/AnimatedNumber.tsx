import { useEffect, useRef, useState } from 'react';
import './AnimatedNumber.css';

interface AnimatedNumberProps {
    value: number;
    duration?: number;
    formatOptions?: Intl.NumberFormatOptions;
    className?: string;
}

export function AnimatedNumber({
    value,
    duration = 500,
    formatOptions = { maximumFractionDigits: 2 },
    className = ''
}: AnimatedNumberProps) {
    const [displayValue, setDisplayValue] = useState(value);
    const previousValue = useRef(value);
    const animationRef = useRef<number | undefined>(undefined);

    useEffect(() => {
        const startValue = previousValue.current;
        const endValue = value;
        const startTime = performance.now();

        const animate = (currentTime: number) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function (ease-out cubic)
            const eased = 1 - Math.pow(1 - progress, 3);

            const current = startValue + (endValue - startValue) * eased;
            setDisplayValue(current);

            if (progress < 1) {
                animationRef.current = requestAnimationFrame(animate);
            } else {
                previousValue.current = endValue;
            }
        };

        animationRef.current = requestAnimationFrame(animate);

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [value, duration]);

    const isIncreasing = value > previousValue.current;
    const isDecreasing = value < previousValue.current;

    return (
        <span
            className={`animated-number ${className} ${isIncreasing ? 'animated-number--increasing' : ''} ${isDecreasing ? 'animated-number--decreasing' : ''}`}
        >
            {displayValue.toLocaleString(undefined, formatOptions)}
        </span>
    );
}
