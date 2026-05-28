#!/usr/bin/env node

import { GoogleGenAI, Modality } from "@google/genai";
import fs from "fs";
import path from "path";

const MODELS = {
  flash: "gemini-2.5-flash-image",
  pro: "imagen-4.0-generate-001",
};

function parseArgs(args) {
  const result = {
    model: "flash",
    prompt: null,
    input: null,
    out: "outputs/output.png",
    aspect: "1:1",
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--model" && args[i + 1]) {
      result.model = args[++i];
    } else if (arg === "--prompt" && args[i + 1]) {
      result.prompt = args[++i];
    } else if (arg === "--input" && args[i + 1]) {
      result.input = args[++i];
    } else if (arg === "--out" && args[i + 1]) {
      result.out = args[++i];
    } else if (arg === "--aspect" && args[i + 1]) {
      result.aspect = args[++i];
    }
  }

  return result;
}

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
  };
  return mimeTypes[ext] || "image/png";
}

async function generateWithFlash(client, prompt, inputPath) {
  const contents = [];

  if (inputPath) {
    const imageData = fs.readFileSync(inputPath);
    const base64Image = imageData.toString("base64");
    const mimeType = getMimeType(inputPath);

    contents.push({
      inlineData: {
        mimeType: mimeType,
        data: base64Image,
      },
    });
  }

  contents.push({ text: prompt });

  const response = await client.models.generateContent({
    model: MODELS.flash,
    contents: [{ role: "user", parts: contents }],
    generationConfig: {
      responseModalities: [Modality.TEXT, Modality.IMAGE],
    },
  });

  return response;
}

async function generateWithPro(client, prompt, aspectRatio) {
  const response = await client.models.generateImages({
    model: MODELS.pro,
    prompt: prompt,
    config: {
      numberOfImages: 1,
      aspectRatio: aspectRatio,
    },
  });

  return response;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.prompt) {
    console.log(JSON.stringify({ ok: false, error: "Missing --prompt" }));
    process.exit(1);
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.log(JSON.stringify({ ok: false, error: "Missing GEMINI_API_KEY environment variable" }));
    process.exit(1);
  }

  const client = new GoogleGenAI({ apiKey });

  try {
    let imageData = null;
    let mimeType = "image/png";

    if (args.model === "flash") {
      const response = await generateWithFlash(client, args.prompt, args.input);

      if (response.candidates && response.candidates[0]) {
        const parts = response.candidates[0].content.parts;
        for (const part of parts) {
          if (part.inlineData) {
            imageData = Buffer.from(part.inlineData.data, "base64");
            mimeType = part.inlineData.mimeType || "image/png";
            break;
          }
        }
      }
    } else if (args.model === "pro") {
      if (args.input) {
        console.log(JSON.stringify({ ok: false, error: "Pro model (Imagen 3) does not support image editing. Use flash model instead." }));
        process.exit(1);
      }

      const response = await generateWithPro(client, args.prompt, args.aspect);

      if (response.generatedImages && response.generatedImages[0]) {
        imageData = Buffer.from(response.generatedImages[0].image.imageBytes, "base64");
      }
    } else {
      console.log(JSON.stringify({ ok: false, error: `Unknown model: ${args.model}. Use 'flash' or 'pro'` }));
      process.exit(1);
    }

    if (!imageData) {
      console.log(JSON.stringify({ ok: false, error: "No image generated. Try a more explicit prompt or different model." }));
      process.exit(1);
    }

    const outDir = path.dirname(args.out);
    if (outDir && !fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }

    fs.writeFileSync(args.out, imageData);

    console.log(JSON.stringify({
      ok: true,
      outFiles: [args.out],
      model: args.model,
      prompt: args.prompt.substring(0, 100) + (args.prompt.length > 100 ? "..." : "")
    }));

  } catch (error) {
    console.log(JSON.stringify({
      ok: false,
      error: error.message,
      details: error.toString()
    }));
    process.exit(1);
  }
}

main();
