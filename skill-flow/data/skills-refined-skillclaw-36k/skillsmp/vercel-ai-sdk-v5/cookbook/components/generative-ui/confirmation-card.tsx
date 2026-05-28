/**
 * Human-in-the-loop confirmation card
 * Renders different states of the confirmAction tool
 */
'use client'

import type { MyUIMessagePart } from '../../types/message'

type ConfirmActionPart = Extract<MyUIMessagePart, { type: 'tool-confirmAction' }>

interface ConfirmationCardProps {
  part: ConfirmActionPart
  onConfirm: (confirmed: boolean, reason?: string) => void
}

export function ConfirmationCard({ part, onConfirm }: ConfirmationCardProps) {
  const severityColors = {
    low: 'border-gray-300 bg-gray-50',
    medium: 'border-yellow-300 bg-yellow-50',
    high: 'border-red-300 bg-red-50',
  }

  switch (part.state) {
    case 'input-streaming':
      return (
        <div className="border rounded-lg p-4 animate-pulse bg-gray-50">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
          <div className="h-4 bg-gray-200 rounded w-1/2" />
        </div>
      )

    case 'input-available':
      const severity = part.input.severity
      return (
        <div
          className={`border-2 rounded-lg p-4 ${severityColors[severity]}`}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">
              {severity === 'high' ? '⚠️' : severity === 'medium' ? '📋' : 'ℹ️'}
            </span>
            <h3 className="font-semibold">Confirmation Required</h3>
          </div>
          
          <p className="font-medium mb-1">{part.input.action}</p>
          <p className="text-gray-600 text-sm mb-4">{part.input.details}</p>
          
          <div className="flex gap-3">
            <button
              onClick={() => onConfirm(true)}
              className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
            >
              Confirm
            </button>
            <button
              onClick={() => onConfirm(false, 'User declined')}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400 transition"
            >
              Cancel
            </button>
          </div>
        </div>
      )

    case 'output-available':
      return (
        <div
          className={`border rounded-lg p-4 ${
            part.output.confirmed
              ? 'bg-green-50 border-green-300'
              : 'bg-red-50 border-red-300'
          }`}
        >
          <div className="flex items-center gap-2">
            <span>{part.output.confirmed ? '✅' : '❌'}</span>
            <span className="font-medium">
              {part.output.confirmed ? 'Confirmed' : 'Declined'}
            </span>
          </div>
          {part.output.reason && (
            <p className="text-sm text-gray-600 mt-1">{part.output.reason}</p>
          )}
        </div>
      )

    case 'output-error':
      return (
        <div className="border border-red-300 rounded-lg p-4 bg-red-50">
          <div className="flex items-center gap-2 text-red-600">
            <span>❌</span>
            <span>Error: {part.errorText}</span>
          </div>
        </div>
      )

    default:
      return null
  }
}
