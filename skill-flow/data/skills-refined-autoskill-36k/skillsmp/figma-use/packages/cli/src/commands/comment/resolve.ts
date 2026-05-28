import { defineCommand } from 'citty'

import { resolveComment } from '../../cdp-api.ts'
import { handleError } from '../../client.ts'
import { ok } from '../../format.ts'

export default defineCommand({
  meta: { description: 'Resolve a comment' },
  args: {
    id: { type: 'positional', description: 'Comment ID', required: true },
    file: { type: 'string', description: 'File key (default: current file)' }
  },
  async run({ args }) {
    try {
      await resolveComment(args.id, args.file)
      console.log(ok(`Resolved comment ${args.id}`))
    } catch (e) {
      handleError(e)
    }
  }
})
