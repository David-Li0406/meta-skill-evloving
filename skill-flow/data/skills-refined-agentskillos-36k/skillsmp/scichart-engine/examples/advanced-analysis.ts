import { createChart } from 'scichart-engine';
import { PluginAnalysis } from 'scichart-engine/plugins/analysis';

/**
 * Advanced analysis: Peak detection and FFT
 */
export const runAnalysis = async (container: HTMLDivElement) => {
    const chart = createChart({
        container,
        xAxis: { label: 'Frequency (Hz)' },
        yAxis: { label: 'Magnitude (dB)' },
        theme: 'midnight'
    });

    await chart.use(PluginAnalysis());

    const data = generateOscillatingData();
    chart.addSeries({
        id: 'signal',
        type: 'line',
        data,
        style: { color: '#00f2ff' }
    });

    // 1. FFT Analysis
    const fftResult = chart.analysis.fft('signal');
    chart.addSeries({
        id: 'fft',
        type: 'line',
        data: fftResult,
        style: { color: '#ff00ff' }
    });

    // 2. Peak Detection
    const peaks = chart.analysis.detectPeaks('signal', {
        threshold: 0.5,
        minDistance: 10
    });

    // Add markers for peaks using annotations
    peaks.forEach((peak, i) => {
        chart.addAnnotation({
            id: `peak-${i}`,
            type: 'text',
            x: peak.x,
            y: peak.y,
            text: '▼',
            style: { color: 'red', fontSize: 20 }
        });
    });

    return chart;
};

function generateOscillatingData() {
    const n = 1024;
    const x = new Float32Array(n);
    const y = new Float32Array(n);
    for (let i = 0; i < n; i++) {
        x[i] = i;
        y[i] = Math.sin(i * 0.1) + Math.sin(i * 0.05) + Math.random() * 0.2;
    }
    return { x, y };
}
