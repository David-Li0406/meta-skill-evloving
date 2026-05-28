import express from 'express'
import cors from 'cors'
import { Chat } from '@hashbrownai/core'
import { HashbrownOpenAI } from '@hashbrownai/openai'
import data from './data.json'

const app = express()
app.use(cors())
app.use(express.json())

const port = process.env.PORT || 3000
const openAIApiKey = process.env.OPENAI_API_KEY

if (!openAIApiKey) {
  throw new Error('The OPENAI_API_KEY environment variable is not set.')
}

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const request = req.body as Chat.Api.CompletionCreateParams

    const stream = HashbrownOpenAI.stream.text({
      apiKey: openAIApiKey,
      request,
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

// Data endpoint
app.get('/api/data', (req, res) => {
  res.json(data)
})

app.listen(port, () => {
  console.log(`Server listening on port ${port}`)
})
