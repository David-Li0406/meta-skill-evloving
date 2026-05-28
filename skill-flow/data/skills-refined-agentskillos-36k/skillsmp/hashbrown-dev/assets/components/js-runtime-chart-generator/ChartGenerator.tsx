import { useChat, useRuntime, useRuntimeFunction, useToolJavaScript } from '@hashbrownai/react'
import { Chart as ChartJS, registerables } from 'chart.js'
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { s } from '@hashbrownai/core'

ChartJS.register(...registerables)

// Mock data fetching function - in a real app, this would fetch from a server
const mockData: Record<string, number[]> = {
  'Product A': [12, 19, 3, 5, 2, 3],
  'Product B': [7, 11, 5, 8, 3, 7],
  'Product C': [15, 8, 12, 4, 6, 9],
}
const mockLabels = ['January', 'February', 'March', 'April', 'May', 'June']

const dataSchema = s.object('Chart Data', {
  labels: s.array('Labels for the chart', s.string('A label')),
  datasets: s.array(
    'Datasets for the chart',
    s.object('A dataset', {
      label: s.string('The label for the dataset'),
      data: s.array('Data points for the dataset', s.number('A data point')),
      backgroundColor: s.string('Background color for the dataset'),
    })
  ),
})

export const ChartGenerator: React.FC = () => {
  const [inputValue, setInputValue] = useState('Show me a bar chart for Product A and Product B')
  const [chartConfig, setChartConfig] = useState<any>(null)
  const chartRef = useRef<HTMLCanvasElement>(null)
  const chartInstanceRef = useRef<ChartJS | null>(null)

  // Define runtime functions that the AI can call from its generated JS code
  const getData = useRuntimeFunction({
    name: 'getData',
    description: 'Gets sales data for a list of products.',
    args: s.object('Product Query', {
      productNames: s.array(
        'An array of product names to fetch data for.',
        s.string('A product name')
      ),
    }),
    result: dataSchema,
    handler: async args => {
      const datasets = args.productNames.map((name, index) => ({
        label: name,
        data: mockData[name] || [],
        backgroundColor: `rgba(${index * 100}, 100, 150, 0.6)`,
      }))
      return { labels: mockLabels, datasets }
    },
    deps: [],
  })

  const renderChart = useRuntimeFunction({
    name: 'renderChart',
    description: 'Renders a chart with the given Chart.js configuration.',
    args: s.object('Chart.js Config', {
      type: s.string('The type of chart (e.g., "bar", "line")'),
      data: dataSchema,
    }),
    handler: async config => {
      setChartConfig(config)
      return { success: true }
    },
    deps: [setChartConfig],
  })

  const runtime = useRuntime({ functions: [getData, renderChart] })
  const jsTool = useToolJavaScript({ runtime })

  const { sendMessage, isLoading } = useChat({
    model: 'gpt-4o-mini',
    system:
      "You are an expert at creating Chart.js configurations in JavaScript. Use the provided `getData` and `renderChart` functions to fulfill the user's request. Only generate JavaScript code inside a `javascript` tool call.",
    tools: [jsTool],
  })

  const handleSubmit = useCallback(() => {
    if (inputValue.trim()) {
      setChartConfig(null)
      sendMessage({ role: 'user', content: inputValue })
    }
  }, [inputValue, sendMessage])

  useEffect(() => {
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy()
    }
    if (chartRef.current && chartConfig) {
      chartInstanceRef.current = new ChartJS(chartRef.current, chartConfig)
    }
  }, [chartConfig])

  return (
    <div
      style={{
        maxWidth: '800px',
        margin: 'auto',
        padding: '16px',
        border: '1px solid #ccc',
        borderRadius: '8px',
      }}
    >
      <h2 style={{ marginTop: 0 }}>JS Runtime Chart Generator</h2>
      <p>
        Describe the chart you want to see. The AI will write and execute JavaScript to generate it.
      </p>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        <input
          type="text"
          value={inputValue}
          onChange={e => setInputValue(e.target.value)}
          style={{ flex: 1, padding: '8px', borderRadius: '8px', border: '1px solid #ccc' }}
          placeholder="e.g., Create a line chart for all products"
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          style={{
            padding: '8px 16px',
            borderRadius: '8px',
            border: 'none',
            backgroundColor: '#007bff',
            color: 'white',
            cursor: 'pointer',
          }}
        >
          {isLoading ? 'Generating...' : 'Generate Chart'}
        </button>
      </div>
      <div style={{ height: '400px' }}>
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  )
}
