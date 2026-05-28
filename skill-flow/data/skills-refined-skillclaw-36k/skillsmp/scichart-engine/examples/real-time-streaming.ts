import { createChart } from 'scichart-engine';

/**
 * High-performance real-time streaming example
 */
export const startStreaming = (container: HTMLDivElement) => {
    const chart = createChart({
        container,
        xAxis: { auto: true, label: 'Time (s)' },
        yAxis: { auto: true, label: 'Sensor Value' },
        theme: 'electrochemistry'
    });

    chart.addSeries({
        id: 'live',
        type: 'line',
        data: { x: new Float32Array(0), y: new Float32Array(0) },
        style: { color: '#00ff88', width: 2 }
    });

    let time = 0;
    const interval = setInterval(() => {
        // Generate new points
        const newX = new Float32Array([time]);
        const newY = new Float32Array([Math.sin(time * 2) * 50 + Math.random() * 10]);

        // Append data efficiently without recreating the entire series
        // use maxPoints to keep a rolling window
        chart.updateSeries('live', {
            x: newX,
            y: newY,
            append: true,
            maxPoints: 1000
        });

        time += 0.05;
    }, 50);

    // Return a cleanup function
    return () => {
        clearInterval(interval);
        chart.destroy();
    };
};
