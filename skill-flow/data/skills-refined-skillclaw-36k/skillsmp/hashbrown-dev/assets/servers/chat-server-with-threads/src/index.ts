import express from 'express'
import cors from 'cors'
import { Chat } from '@hashbrownai/core'
import { HashbrownOpenAI } from '@hashbrownai/openai'
import { loadThread, saveThread } from './database'

const app = express()
app.use(cors())
app.use(express.json())

const port = process.env.PORT || 3000
const openAIApiKey = process.env.OPENAI_API_KEY

if (!openAIApiKey) {
  throw new Error('The OPENAI_API_KEY environment variable is not set.')
}

app.post('/api/chat', async (req, res) => {
  try {
    const request = req.body as Chat.Api.CompletionCreateParams

    const stream = HashbrownOpenAI.stream.text({
      apiKey: openAIApiKey,
      request,
      // Implement persistence by providing the loadThread and saveThread handlers
      loadThread: async threadId => {
        console.log(`Loading thread: ${threadId}`)
        return loadThread(threadId)
      },
      saveThread: async (threadId, messages) => {
        console.log(`Saving thread: ${threadId}`)
        saveThread(threadId, messages)
      },
    })

    res.header('Content-Type', 'application/octet-stream')

    for await (const chunk of stream) {
      res.write(chunk)
    }

    res.end()
  } catch (error) {
    console.error('Error processing chat request:', error)
    res.status(500).json({ error: 'Internal Server Error' })
  }
})

app.listen(port, () => {
  console.log(`Server listening on port ${port}`)
})
