#!/usr/bin/env bun
import * as fs from "fs"
import * as path from "path"

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY

if (!OPENROUTER_API_KEY) {
  console.error("Error: OPENROUTER_API_KEY environment variable is required")
  process.exit(1)
}

const args = process.argv.slice(2)

if (args.length < 2) {
  console.error("Usage: analyze.ts <prompt> <file1> [file2] ...")
  console.error("Example: analyze.ts 'What is this document about?' document.pdf")
  process.exit(1)
}

const prompt = args[0]
const filePaths = args.slice(1)

function getMediaType(
  filePath: string
): "application/pdf" | "image/png" | "image/jpeg" | "image/gif" | "image/webp" {
  const ext = path.extname(filePath).toLowerCase()
  const mimeTypes: Record<
    string,
    "application/pdf" | "image/png" | "image/jpeg" | "image/gif" | "image/webp"
  > = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
  }
  return mimeTypes[ext] || "application/pdf"
}

async function analyzeFiles(prompt: string, files: string[]) {
  const content: Array<
    | { type: "text"; text: string }
    | {
        type: "image_url"
        image_url: {
          url: string
        }
      }
    | {
        type: "file"
        file: {
          filename: string
          file_data: string
        }
      }
  > = []

  for (const filePath of files) {
    const absolutePath = path.resolve(filePath)

    if (!fs.existsSync(absolutePath)) {
      console.error(`Error: File not found: ${absolutePath}`)
      process.exit(1)
    }

    const fileBuffer = fs.readFileSync(absolutePath)
    const base64Data = fileBuffer.toString("base64")
    const mediaType = getMediaType(filePath)
    const fileName = path.basename(filePath)

    if (mediaType === "application/pdf") {
      content.push({
        type: "file",
        file: {
          filename: fileName,
          file_data: `data:${mediaType};base64,${base64Data}`,
        },
      })
    } else {
      content.push({
        type: "image_url",
        image_url: {
          url: `data:${mediaType};base64,${base64Data}`,
        },
      })
    }
  }

  content.push({
    type: "text",
    text: prompt,
  })

  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
      "HTTP-Referer": "https://github.com/matixlol/monitoreo-panama",
      "X-Title": "Monitoreo Panama PDF Analyzer",
    },
    body: JSON.stringify({
      model: "google/gemini-3-flash-preview",
      messages: [
        {
          role: "user",
          content,
        },
      ],
      max_tokens: 16000,
    }),
  })

  if (!response.ok) {
    const errorText = await response.text()
    console.error(`API Error (${response.status}): ${errorText}`)
    process.exit(1)
  }

  const data = (await response.json()) as {
    choices: Array<{
      message: {
        content: string
      }
    }>
  }

  if (data.choices && data.choices[0]?.message?.content) {
    console.log(data.choices[0].message.content)
  } else {
    console.error("Unexpected response format:", JSON.stringify(data, null, 2))
    process.exit(1)
  }
}

analyzeFiles(prompt, filePaths).catch((err) => {
  console.error("Error:", err.message)
  process.exit(1)
})
