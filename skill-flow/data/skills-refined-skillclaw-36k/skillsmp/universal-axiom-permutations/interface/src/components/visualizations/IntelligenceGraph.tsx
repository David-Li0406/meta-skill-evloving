import { useMemo } from 'react';
import { UniversalAxiom } from '../../core/axiom';
import './IntelligenceGraph.css';

interface IntelligenceGraphProps {
    currentParams: {
        impulses: number;
        elements: number;
        pressure: number;
        subjectivity: number;
        purpose: number;
        time: number;
    };
    currentN: number;
    maxN?: number;
}

export function IntelligenceGraph({
    currentParams,
    currentN,
    maxN = 12
}: IntelligenceGraphProps) {
    const dataPoints = useMemo(() => {
        const points: { n: number; intelligence: number }[] = [];

        for (let n = 1; n <= maxN; n++) {
            const axiom = new UniversalAxiom({
                ...currentParams,
                n
            });
            points.push({
                n,
                intelligence: axiom.computeIntelligence()
            });
        }

        return points;
    }, [currentParams, maxN]);

    const maxIntelligence = Math.max(...dataPoints.map(p => p.intelligence));
    const minIntelligence = Math.min(...dataPoints.map(p => p.intelligence));
    const range = maxIntelligence - minIntelligence || 1;

    // SVG dimensions
    const width = 100;
    const height = 60;
    const padding = { top: 5, right: 5, bottom: 5, left: 5 };
    const graphWidth = width - padding.left - padding.right;
    const graphHeight = height - padding.top - padding.bottom;

    // Generate path
    const pathD = dataPoints.map((point, i) => {
        const x = padding.left + (i / (maxN - 1)) * graphWidth;
        const y = padding.top + graphHeight - ((point.intelligence - minIntelligence) / range) * graphHeight;
        return `${i === 0 ? 'M' : 'L'} ${x} ${y}`;
    }).join(' ');

    // Area fill path
    const areaD = pathD +
        ` L ${padding.left + graphWidth} ${padding.top + graphHeight}` +
        ` L ${padding.left} ${padding.top + graphHeight} Z`;

    // Current position
    const currentPoint = dataPoints.find(p => p.n === currentN);
    const currentX = padding.left + ((currentN - 1) / (maxN - 1)) * graphWidth;
    const currentY = currentPoint
        ? padding.top + graphHeight - ((currentPoint.intelligence - minIntelligence) / range) * graphHeight
        : padding.top + graphHeight / 2;

    return (
        <div className="intelligence-graph">
            <div className="intelligence-graph__header">
                <h3 className="intelligence-graph__title">Intelligence Evolution</h3>
                <span className="intelligence-graph__subtitle">Intelligence as n increases</span>
            </div>

            <div className="intelligence-graph__container">
                <svg
                    viewBox={`0 0 ${width} ${height}`}
                    className="intelligence-graph__svg"
                    preserveAspectRatio="none"
                >
                    <defs>
                        <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="var(--color-foundation)" />
                            <stop offset="50%" stopColor="var(--color-dynamic)" />
                            <stop offset="100%" stopColor="var(--color-cognitive)" />
                        </linearGradient>
                        <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor="var(--color-cognitive)" stopOpacity="0.3" />
                            <stop offset="100%" stopColor="var(--color-cognitive)" stopOpacity="0" />
                        </linearGradient>
                        <filter id="glow">
                            <feGaussianBlur stdDeviation="1" result="coloredBlur" />
                            <feMerge>
                                <feMergeNode in="coloredBlur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    {/* Area fill */}
                    <path
                        d={areaD}
                        fill="url(#areaGradient)"
                        className="intelligence-graph__area"
                    />

                    {/* Main line */}
                    <path
                        d={pathD}
                        fill="none"
                        stroke="url(#lineGradient)"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="intelligence-graph__line"
                        filter="url(#glow)"
                    />

                    {/* Data points */}
                    {dataPoints.map((point, i) => {
                        const x = padding.left + (i / (maxN - 1)) * graphWidth;
                        const y = padding.top + graphHeight - ((point.intelligence - minIntelligence) / range) * graphHeight;
                        return (
                            <circle
                                key={point.n}
                                cx={x}
                                cy={y}
                                r={point.n === currentN ? 3 : 1.5}
                                className={`intelligence-graph__point ${point.n === currentN ? 'intelligence-graph__point--active' : ''}`}
                            />
                        );
                    })}

                    {/* Current position indicator */}
                    <circle
                        cx={currentX}
                        cy={currentY}
                        r="4"
                        className="intelligence-graph__current-pulse"
                    />
                </svg>

                {/* X-axis labels */}
                <div className="intelligence-graph__x-axis">
                    <span>n=1</span>
                    <span>n={Math.floor(maxN / 2)}</span>
                    <span>n={maxN}</span>
                </div>
            </div>

            {/* Stats */}
            <div className="intelligence-graph__stats">
                <div className="intelligence-graph__stat">
                    <span className="intelligence-graph__stat-label">Min (n=1)</span>
                    <span className="intelligence-graph__stat-value">
                        {dataPoints[0]?.intelligence.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </span>
                </div>
                <div className="intelligence-graph__stat">
                    <span className="intelligence-graph__stat-label">Current (n={currentN})</span>
                    <span className="intelligence-graph__stat-value intelligence-graph__stat-value--highlight">
                        {currentPoint?.intelligence.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </span>
                </div>
                <div className="intelligence-graph__stat">
                    <span className="intelligence-graph__stat-label">Max (n={maxN})</span>
                    <span className="intelligence-graph__stat-value">
                        {dataPoints[maxN - 1]?.intelligence.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                    </span>
                </div>
            </div>
        </div>
    );
}
