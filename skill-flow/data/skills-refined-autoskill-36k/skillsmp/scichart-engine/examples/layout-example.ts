/**
 * Layout Configuration Example
 * 
 * Demonstrates the layout system for fine-grained control over
 * chart component positioning and behavior.
 */
import { createChart, type LayoutOptions } from 'scichart-engine';

// Create chart with comprehensive layout configuration
const chart = createChart({
    container: document.getElementById('chart-container') as HTMLDivElement,
    theme: 'midnight',

    // Detailed layout configuration
    layout: {
        // Chart title
        title: {
            text: 'Scientific Data Analysis',
            visible: true,
            fontSize: 18,
            fontWeight: 600,
            color: '#ffffff',
            position: 'top',
            align: 'center',
            padding: { top: 12, bottom: 8 },
        },

        // Legend configuration
        legend: {
            visible: true,
            position: 'top-right',
            width: 140,
            // Don't change color on hover (default)
            highlightOnHover: false,
            // Bring series to front on hover (default)
            bringToFrontOnHover: true,
            draggable: true,
            resizable: true,
        },

        // Crosshair configuration
        crosshair: {
            enabled: true,
            showVertical: true,
            showHorizontal: true,
            // Display mode: 'disabled' | 'corner' | 'floating'
            valueDisplayMode: 'corner',
            // Corner position when mode is 'corner'
            cornerPosition: 'top-left',
            valueFormat: {
                xPrecision: 4,
                yPrecision: 4,
            },
        },

        // Toolbar position
        toolbarPosition: 'top-center',

        // Chart margins (space between container and chart)
        margins: {
            top: 40,     // Extra space for title
            right: 30,
            bottom: 60,  // Space for x-axis labels
            left: 80,    // Space for y-axis labels
        },

        // Plot area padding
        plotPadding: {
            top: 5,
            right: 5,
            bottom: 5,
            left: 5,
        },

        // X-axis layout spacing
        xAxisLayout: {
            titleGap: 12,   // Distance from axis line to title
            labelGap: 6,    // Distance from tick labels to axis
            tickGap: 2,     // Distance from tick marks to axis
        },

        // Y-axis layout spacing
        yAxisLayout: {
            titleGap: 10,
            labelGap: 4,
            tickGap: 2,
        },
    },

    xAxis: { label: 'Time (s)', auto: true },
    yAxis: { label: 'Current (µA)', auto: true },
});

// Add sample data
const x = new Float32Array(1000);
const y = new Float32Array(1000);
for (let i = 0; i < 1000; i++) {
    x[i] = i * 0.01;
    y[i] = Math.sin(x[i] * 2 * Math.PI) + Math.random() * 0.1;
}

chart.addSeries({
    id: 'signal',
    name: 'Signal',
    type: 'line',
    data: { x, y },
    style: { color: '#4fc3f7', width: 2 },
});

// Example: Enable color highlighting on legend hover
// chart.layout.legend.highlightOnHover = true;

// Example: Change crosshair to floating mode
// chart.layout.crosshair.valueDisplayMode = 'floating';
