import { defineCommand } from 'citty'

import { sendCommand, printResult, handleError } from '../../client.ts'

export default defineCommand({
  meta: { description: 'Find variables by name pattern' },
  args: {
    query: { type: 'positional', description: 'Search query (substring match)', required: true },
    type: { type: 'string', description: 'Filter by type: COLOR, FLOAT, STRING, BOOLEAN' },
    limit: { type: 'string', description: 'Max results (default: 20)' },
    json: { type: 'boolean', description: 'Output as JSON' }
  },
  async run({ args }) {
    try {
      const result = await sendCommand('find-variables', {
        query: args.query,
        type: args.type,
        limit: args.limit ? Number(args.limit) : 20
      })
      printResult(result, args.json)
    } catch (e) {
      handleError(e)
    }
  }
})
