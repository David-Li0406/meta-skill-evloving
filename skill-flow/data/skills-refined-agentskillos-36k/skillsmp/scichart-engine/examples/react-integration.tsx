import React, { useEffect, useRef } from 'react';
import { createChart, type Chart } from 'scichart-engine';

/**
 * React Component pattern for SciChart Engine
 */
export const SciChartComponent: React.FC = () => {
    const containerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<Chart | null>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        // Initialize chart
        const chart = createChart({
            container: containerRef.current,
            theme: 'midnight',
            xAxis: { auto: true },
            yAxis: { auto: true }
        });

        chartRef.current = chart;

        // Optional: Add initial series or load data

        return () => {
            // CRITICAL: Cleanup to prevent WebGL context leaks
            chart.destroy();
            chartRef.current = null;
        };
    }, []);

    return <div ref={containerRef} style={{ width: '100%', height: '500px' }} />;
};
