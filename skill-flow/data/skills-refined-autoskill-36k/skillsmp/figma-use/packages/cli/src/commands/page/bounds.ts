import { defineCommand } from 'citty'

import { sendCommand, printResult, handleError } from '../../client.ts'

export default defineCommand({
  meta: { description: 'Get bounding box of all objects on current page' },
  args: {
    json: { type: 'boolean', description: 'Output as JSON' }
  },
  async run({ args }) {
    try {
      const result = await sendCommand('get-page-bounds', {})
      printResult(result, args.json)
    } catch (e) {
      handleError(e)
    }
  }
})
