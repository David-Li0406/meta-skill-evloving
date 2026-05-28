import express from 'express'
import cors from 'cors'
import { OpenAIChat } from '@hashbrown/openai'
import { apiKeyAuth } from './middleware'

const app = express()
app.use(cors())
app.use(express.json())

const port = 3000

const chat = new OpenAIChat({
  apiKey: process.env.OPENAI_API_KEY,
})

app.post('/chat', apiKeyAuth, async (req, res) => {
  const { messages } = req.body
  const result = await chat.completion(messages)
  res.json(result)
})

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`)
})
