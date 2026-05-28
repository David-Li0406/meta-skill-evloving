#!/usr/bin/env bun
import { writeFile, readFile } from "fs/promises";
import { existsSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { callGeminiImage, type GeminiImageResult } from "../../../utils";
import type { Image } from "@google/genai";

const __dirname = dirname(fileURLToPath(import.meta.url));
const STYLES_PATH = resolve(__dirname, "../../../styles/styles.json");

interface Style {
  id: string;
  shortName: string;
  name: string;
  promptHints: string;
}

interface StylesRegistry {
  styles: Style[];
}

async function loadStyle(styleId: string): Promise<Style | null> {
  if (!existsSync(STYLES_PATH)) {
    console.error("Warning: styles.json not found, ignoring --style");
    return null;
  }
  const content = await readFile(STYLES_PATH, "utf-8");
  const registry: StylesRegistry = JSON.parse(content);
  const style = registry.styles.find(
    (s) => s.id === styleId || s.shortName === styleId
  );
  if (!style) {
    console.error(`Warning: Style "${styleId}" not found`);
    return null;
  }
  return style;
}

async function loadImage(filePath: string): Promise<Image | null> {
  if (!existsSync(filePath)) {
    console.error(`Warning: Image not found: ${filePath}`);
    return null;
  }
  const buffer = await readFile(filePath);
  const base64 = buffer.toString("base64");
  const ext = filePath.toLowerCase().split(".").pop();
  const mimeType = ext === "jpg" || ext === "jpeg" ? "image/jpeg"
    : ext === "webp" ? "image/webp"
    : "image/png";
  return { imageBytes: base64, mimeType };
}

const args = process.argv.slice(2);

function getApiKey(): string {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.error("Error: GEMINI_API_KEY environment variable is not set.");
    process.exit(1);
  }
  return apiKey;
}

function parseArgs(): { prompt: string; options: any; styleId?: string; inputPaths: string[] } {
  const parsed: Record<string, any> = { _: [] };
  const inputPaths: string[] = [];

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const nextArg = args[i + 1];
      if (nextArg && !nextArg.startsWith("--")) {
        // Collect multiple --input flags
        if (key === "input") {
          inputPaths.push(nextArg);
        } else {
          parsed[key] = nextArg;
        }
        i++;
      } else {
        parsed[key] = true;
      }
    } else {
      parsed._.push(arg);
    }
  }

  const prompt = parsed._.join(" ");
  if (!prompt) {
    console.error("Error: Prompt required");
    console.error("Usage: bun run generate.ts \"prompt\" [options]");
    console.error("Options:");
    console.error("  --input <path>    Reference image (can specify multiple times, up to 14)");
    console.error("  --style <id>      Apply style from styles.json");
    console.error("  --size <1K|2K|4K> Image size (default: 2K)");
    console.error("  --aspect <ratio>  Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4");
    console.error("  --negative <text> Negative prompt");
    console.error("  --count <n>       Number of images (1-4)");
    console.error("  --seed <n>        Random seed");
    console.error("  --output <path>   Output file path");
    process.exit(1);
  }

  // API expects string values directly
  const sizeMap: Record<string, string> = {
    "1K": "1024",
    "2K": "2048",
    "4K": "4096",
  };

  // Valid aspect ratios per API: 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
  const validAspects = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"];

  const options: any = {};
  // Default to 1K for fast drafts (nano-banana-pro pattern)
  options.imageSize = sizeMap[parsed.size || "1K"];
  if (parsed.aspect) {
    if (validAspects.includes(parsed.aspect)) {
      options.aspectRatio = parsed.aspect;
    } else {
      console.error(`Warning: Invalid aspect ratio "${parsed.aspect}". Valid: ${validAspects.join(", ")}`);
    }
  }
  if (parsed.negative) options.negativePrompt = parsed.negative;
  if (parsed.count) options.numberOfImages = parseInt(parsed.count);
  if (parsed.guidance) options.guidanceScale = parseFloat(parsed.guidance);
  if (parsed.seed) options.seed = parseInt(parsed.seed);

  return { prompt, options, styleId: parsed.style, inputPaths };
}

function generateTimestampFilename(descriptor?: string): string {
  const now = new Date();
  const pad = (n: number) => n.toString().padStart(2, '0');
  const timestamp = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}-${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`;
  const suffix = descriptor ? `-${descriptor.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 30)}` : '';
  return `${timestamp}${suffix}.png`;
}

async function saveImage(data: string, mimeType: string, outputPath?: string, descriptor?: string): Promise<string> {
  const ext = mimeType.split("/")[1] || "png";
  const path = outputPath || generateTimestampFilename(descriptor);
  const buffer = Buffer.from(data, "base64");
  await writeFile(path, buffer);
  return path;
}

const apiKey = getApiKey();
const { prompt, options, styleId, inputPaths } = parseArgs();

// Load input images
if (inputPaths.length > 0) {
  console.error(`Loading ${inputPaths.length} reference image(s)...`);
  const inputImages: Image[] = [];
  for (const path of inputPaths) {
    const img = await loadImage(path);
    if (img) {
      inputImages.push(img);
      console.error(`  ✓ ${path}`);
    }
  }
  if (inputImages.length > 0) {
    options.inputImages = inputImages;
  }
}

let finalPrompt = prompt;
if (styleId) {
  const style = await loadStyle(styleId);
  if (style) {
    console.error(`Applying style: ${style.name}\n`);
    finalPrompt = `${style.promptHints}, ${prompt}`;
  }
}

console.error("Generating image...\n");
const result: GeminiImageResult = await callGeminiImage(apiKey, finalPrompt, options);

if (result.text) {
  console.log(`Model comment: ${result.text}\n`);
}

for (let i = 0; i < result.images.length; i++) {
  const img = result.images[i];
  const outputPath = args.find(a => a === "--output")
    ? args[args.indexOf("--output") + 1]
    : undefined;
  const finalPath = outputPath && result.images.length > 1
    ? outputPath.replace(/(\.\w+)$/, `_${i + 1}$1`)
    : outputPath;
  // Use first few words of prompt as descriptor for auto-generated filenames
  const descriptor = prompt.split(' ').slice(0, 4).join(' ');
  const savedPath = await saveImage(img.data, img.mimeType, finalPath, descriptor);
  console.log(`✓ Saved: ${savedPath}`);
}

// Output only the path - do not read the image back
// This allows efficient iteration without Claude loading large image data
