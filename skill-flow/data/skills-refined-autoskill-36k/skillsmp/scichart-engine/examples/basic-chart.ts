import { createChart } from 'scichart-engine';
import { PluginTools } from 'scichart-engine/plugins/tools';

/**
 * Basic chart setup with a line series and tooltips
 */
export const initBasicChart = (container: HTMLDivElement) => {
    const chart = createChart({
        container,
        xAxis: { label: 'Time (s)' },
        yAxis: { label: 'Voltage (mV)' },
        theme: 'midnight'
    });

    // Add plugins
    chart.use(PluginTools({
        tooltip: { showCrosshair: true }
    }));

    // Add sample data
    chart.addSeries({
        id: 'signal',
        type: 'line',
        data: {
            x: new Float32Array([0, 1, 2, 3, 4, 5]),
            y: new Float32Array([10, 15, 12, 18, 14, 20])
        },
        style: { color: '#00f2ff', width: 2 }
    });

    return chart;
};
