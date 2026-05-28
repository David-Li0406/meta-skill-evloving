/**
 * A2UI Smart Wrapper Template: Chart.js Integration
 * 
 * This template demonstrates the "Smart Wrapper" pattern for integrating
 * third-party visualization libraries with A2UI. The wrapper:
 * 
 * 1. Encapsulates the library (creates container elements)
 * 2. Bridges A2UI props to the library's API
 * 3. Handles reactive updates efficiently
 * 4. Cleans up resources on disconnect
 * 
 * Adapt this pattern for any library: D3, Mapbox, Three.js, etc.
 * 
 * @example Agent payload:
 * ```json
 * {
 *   "component": "Chart",
 *   "chartType": { "literalString": "line" },
 *   "data": { "path": "/metrics/sales" },
 *   "options": { "literalString": "{\"tension\": 0.4}" }
 * }
 * ```
 */

import { html, css, PropertyValues } from 'lit';
import { customElement, query } from 'lit/decorators.js';
import { DynamicComponent } from './DynamicComponent';

// Uncomment when Chart.js is installed:
// import Chart from 'chart.js/auto';

/**
 * Mock Chart type for template purposes.
 * Replace with actual Chart.js types when installed.
 */
interface MockChart {
    data: {
        labels: string[];
        datasets: Array<{ data: number[]; label?: string }>;
    };
    update(): void;
    destroy(): void;
}

/**
 * Smart Wrapper for Chart.js
 * 
 * Renders various chart types (line, bar, pie, etc.) based on
 * A2UI component definitions. Efficiently updates on data changes.
 */
@customElement('agui-chart-wrapper')
export class ChartWrapper extends DynamicComponent {
    static styles = css`
    :host {
      display: block;
      width: 100%;
      height: 300px;
      position: relative;
    }
    
    .chart-container {
      width: 100%;
      height: 100%;
    }
    
    canvas {
      max-width: 100%;
      max-height: 100%;
    }
    
    .loading {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: rgba(0, 0, 0, 0.5);
      font-family: var(--font-nf, sans-serif);
    }
    
    .error {
      color: #d32f2f;
      padding: 16px;
      background: rgba(211, 47, 47, 0.1);
      border-radius: 8px;
    }
  `;

    /**
     * Reference to the Chart.js instance.
     * Null until initialized.
     */
    private chartInstance: MockChart | null = null;

    /**
     * Query the canvas element in Shadow DOM.
     */
    @query('canvas')
    private canvas!: HTMLCanvasElement;

    /**
     * Error state for rendering feedback.
     */
    private error: string | null = null;

    /**
     * Lifecycle: Called when properties change.
     * This is where we bridge A2UI props to Chart.js.
     */
    updated(changedProps: PropertyValues): void {
        super.updated(changedProps);

        // Resolve properties from A2UI definition
        const def = this.componentDefinition?.component as Record<string, unknown> | undefined;
        if (!def) return;

        const chartDef = def['Chart'] as Record<string, unknown> | undefined;
        if (!chartDef) return;

        const chartType = this.resolve(chartDef['chartType'] as any) as string;
        const rawData = this.resolve(chartDef['data'] as any);
        const rawOptions = this.resolve(chartDef['options'] as any);

        // Parse data (expect array of numbers or structured data)
        let chartData: number[] = [];
        if (Array.isArray(rawData)) {
            chartData = rawData;
        } else if (typeof rawData === 'string') {
            try {
                chartData = JSON.parse(rawData);
            } catch {
                this.error = 'Invalid chart data format';
                return;
            }
        }

        // Parse options if provided as JSON string
        let options = {};
        if (typeof rawOptions === 'string') {
            try {
                options = JSON.parse(rawOptions);
            } catch {
                // Use defaults if options parsing fails
            }
        }

        // Bridge to Chart.js
        this.updateChart(chartType, chartData, options);
    }

    /**
     * Create or update the Chart.js instance.
     */
    private updateChart(type: string, data: number[], _options: Record<string, unknown>): void {
        if (!this.canvas) return;

        // Clear any previous errors
        this.error = null;

        if (!this.chartInstance) {
            // Initialize new chart
            // Uncomment when Chart.js is installed:
            /*
            this.chartInstance = new Chart(this.canvas, {
              type: type as any,
              data: {
                labels: data.map((_, i) => `${i + 1}`),
                datasets: [{
                  label: 'Data',
                  data: data,
                  borderColor: 'rgb(0, 0, 0)',
                  backgroundColor: 'rgba(0, 0, 0, 0.1)',
                  ...options
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: false
                  }
                }
              }
            });
            */
            console.log('[ChartWrapper] Would initialize chart:', { type, data });
        } else {
            // Update existing chart reactively
            this.chartInstance.data.datasets[0].data = data;
            this.chartInstance.data.labels = data.map((_, i) => `${i + 1}`);
            this.chartInstance.update();
        }
    }

    /**
     * Lifecycle: Cleanup when component is removed.
     * Critical for preventing memory leaks in SPAs.
     */
    disconnectedCallback(): void {
        super.disconnectedCallback();

        if (this.chartInstance) {
            this.chartInstance.destroy();
            this.chartInstance = null;
        }
    }

    render() {
        if (this.error) {
            return html`<div class="error">${this.error}</div>`;
        }

        if (!this.componentDefinition) {
            return html`<div class="loading">Loading chart...</div>`;
        }

        return html`
      <div class="chart-container">
        <canvas></canvas>
      </div>
    `;
    }
}

/**
 * Export for registration in ComponentRegistry:
 * 
 * componentRegistry.register('Chart', ChartWrapper, 'agui-chart-wrapper', {
 *   category: 'smart-wrapper',
 *   description: 'Chart.js visualization wrapper'
 * });
 */
export { ChartWrapper };
