/**
 * Proposal data part card
 * Shows progressive loading states via data part reconciliation
 */
'use client'

import type { DataParts } from '../../types/message'

interface ProposalCardProps {
  data: DataParts['proposal']
}

export function ProposalCard({ data }: ProposalCardProps) {
  switch (data.status) {
    case 'loading':
      return (
        <div className="border rounded-lg p-4 bg-blue-50 animate-pulse">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-blue-700">Loading proposal...</span>
          </div>
          {data.title && (
            <p className="text-sm text-blue-600 mt-2">{data.title}</p>
          )}
        </div>
      )

    case 'generating':
      return (
        <div className="border rounded-lg p-4 bg-yellow-50">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-yellow-700 font-medium">
              Generating proposal...
            </span>
          </div>
          {data.title && (
            <p className="text-sm text-yellow-600 mt-2">{data.title}</p>
          )}
        </div>
      )

    case 'complete':
      const content = data.content as {
        coverage: string
        amount: number
        premium: number
        generatedAt: string
        details?: string
      } | null

      return (
        <div className="border border-green-300 rounded-lg overflow-hidden">
          <div className="bg-green-500 text-white px-4 py-2 flex items-center gap-2">
            <span>✓</span>
            <span className="font-medium">{data.title || 'Proposal Ready'}</span>
          </div>
          {content && (
            <div className="p-4 bg-white space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Coverage</p>
                  <p className="font-medium">{content.coverage}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Amount</p>
                  <p className="font-medium">
                    ${content.amount.toLocaleString()}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Premium</p>
                  <p className="font-medium text-green-600">
                    ${content.premium.toLocaleString()}/year
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Generated</p>
                  <p className="font-medium text-sm">
                    {new Date(content.generatedAt).toLocaleString()}
                  </p>
                </div>
              </div>
              {content.details && (
                <div className="pt-3 border-t">
                  <p className="text-sm text-gray-500">Details</p>
                  <p className="text-sm">{content.details}</p>
                </div>
              )}
            </div>
          )}
        </div>
      )

    case 'error':
      return (
        <div className="border border-red-300 rounded-lg p-4 bg-red-50">
          <div className="flex items-center gap-2 text-red-600">
            <span>❌</span>
            <span className="font-medium">Proposal Generation Failed</span>
          </div>
          {data.error && (
            <p className="text-sm text-red-500 mt-2">{data.error}</p>
          )}
        </div>
      )

    default:
      return null
  }
}
