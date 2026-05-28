import express from 'express'
import cors from 'cors'
import { OpenAIChat } from '@hashbrown/openai'
import { StreamingTextResponse } from '@hashbrown/core'

const app = express()
app.use(cors())
app.use(express.json())

const port = 3000

const chat = new OpenAIChat({
  apiKey: process.env.OPENAI_API_KEY,
})

app.post('/chat', async (req, res) => {
  const { messages } = req.body

  const result = await chat.completion(messages, {
    stream: true,
  })

  const stream = new StreamingTextResponse(result.stream)

  res.setHeader('Content-Type', 'text/event-stream')
  res.setHeader('Cache-Control', 'no-cache')
  res.setHeader('Connection', 'keep-alive')

  for await (const chunk of stream.readable) {
    res.write(`data: ${JSON.stringify(chunk)}

`)
    res.flush()
  }
})

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`)
})
