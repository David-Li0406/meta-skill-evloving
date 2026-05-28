/**
 * Weather tool result card
 * Example of server-side tool with generative UI
 */
'use client'

import type { MyUIMessagePart } from '../../types/message'

type WeatherToolPart = Extract<MyUIMessagePart, { type: 'tool-getWeatherInfo' }>

interface WeatherCardProps {
  part: WeatherToolPart
}

export function WeatherCard({ part }: WeatherCardProps) {
  const weatherIcons: Record<string, string> = {
    sunny: '☀️',
    cloudy: '☁️',
    rainy: '🌧️',
    'partly cloudy': '⛅',
  }

  switch (part.state) {
    case 'input-streaming':
      return (
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 rounded-full text-sm">
          <div className="w-3 h-3 border border-gray-400 border-t-transparent rounded-full animate-spin" />
          <span className="text-gray-500">Loading weather...</span>
        </div>
      )

    case 'input-available':
      return (
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-100 rounded-full text-sm">
          <div className="w-3 h-3 border border-blue-400 border-t-transparent rounded-full animate-spin" />
          <span className="text-blue-600">
            Getting weather for {part.input.location}...
          </span>
        </div>
      )

    case 'output-available':
      const icon = weatherIcons[part.output.condition] || '🌡️'
      return (
        <div className="inline-flex items-center gap-3 px-4 py-2 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-lg">
          <span className="text-2xl">{icon}</span>
          <div>
            <p className="font-medium text-gray-800">{part.output.location}</p>
            <p className="text-sm text-gray-600">
              {part.output.condition}, {part.output.temperature}°
              {part.output.unit === 'celsius' ? 'C' : 'F'}
            </p>
          </div>
        </div>
      )

    case 'output-error':
      return (
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-red-100 text-red-600 rounded-full text-sm">
          <span>❌</span>
          <span>{part.errorText}</span>
        </div>
      )

    default:
      return null
  }
}
