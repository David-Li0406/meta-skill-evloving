import { defineCommand } from 'citty'

import { sendCommand, printResult, handleError } from '../../client.ts'

export default defineCommand({
  meta: { description: 'Get ancestor chain from node to page root' },
  args: {
    id: { type: 'positional', description: 'Node ID', required: true },
    depth: { type: 'string', description: 'Max ancestors to return (default: 10)' },
    json: { type: 'boolean', description: 'Output as JSON' }
  },
  async run({ args }) {
    try {
      const result = await sendCommand('get-ancestors', {
        id: args.id,
        depth: args.depth ? Number(args.depth) : 10
      })
      printResult(result, args.json)
    } catch (e) {
      handleError(e)
    }
  }
})
