import React, { useRef } from 'react';
import { SciChart, type SciChartRef } from 'scichart-engine/react';

/**
 * Declarative React pattern using the built-in SciChart component
 */
export const DeclarativeChart: React.FC = () => {
    const chartRef = useRef<SciChartRef>(null);

    const series = [
        {
            id: 'sensor-a',
            x: new Float32Array([0, 1, 2, 3, 4]),
            y: new Float32Array([10, 15, 12, 18, 14]),
            color: '#00f2ff',
            name: 'Sensor A'
        },
        {
            id: 'sensor-b',
            x: new Float32Array([0, 1, 2, 3, 4]),
            y: new Float32Array([5, 8, 15, 10, 12]),
            color: '#ff00ff',
            name: 'Sensor B'
        }
    ];

    const handleExport = () => {
        const chart = chartRef.current?.getChart();
        if (chart) {
            const dataUrl = chart.exportImage('png');
            const link = document.createElement('a');
            link.download = 'chart-snapshot.png';
            link.href = dataUrl;
            link.click();
        }
    };

    return (
        <div style={{ width: '100%', height: '500px', display: 'flex', flexDirection: 'column' }}>
            <button onClick={handleExport} style={{ alignSelf: 'flex-start', marginBottom: '10px' }}>
                Export Snapshot
            </button>
            <SciChart
                ref={chartRef}
                series={series}
                xAxis={{ label: 'Time (s)', auto: true }}
                yAxis={{ label: 'Voltage (V)', auto: true }}
                theme="midnight"
                showLegend={true}
                showControls={true}
            />
        </div>
    );
};
