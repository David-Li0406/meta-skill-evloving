import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { homedir } from "node:os";
import { mkdir, readFile, writeFile } from "node:fs/promises";

type Provider = "google" | "openai";
type Quality = "normal" | "2k";

type CliArgs = {
  prompt: string | null;
  promptFiles: string[];
  imagePath: string | null;
  provider: Provider | null;
  model: string | null;
  aspectRatio: string | null;
  size: string | null;
  quality: Quality;
  referenceImages: string[];
  n: number;
  json: boolean;
  help: boolean;
};

const GOOGLE_MULTIMODAL_MODELS = [
  "gemini-3-pro-image-preview",
  "gemini-2.0-flash-exp-image-generation",
  "gemini-2.5-flash-preview-native-audio-dialog",
];

const GOOGLE_IMAGEN_MODELS = ["imagen-3.0-generate-002", "imagen-3.0-generate-001"];

const OPENAI_IMAGE_MODELS = ["gpt-image-1.5", "gpt-image-1", "dall-e-3", "dall-e-2"];

function printUsage(): void {
  console.log(`Usage:
  npx -y bun scripts/main.ts --prompt "A cat" --image cat.png
  npx -y bun scripts/main.ts --prompt "A landscape" --image landscape.png --ar 16:9
  npx -y bun scripts/main.ts --promptfiles system.md content.md --image out.png

Options:
  -p, --prompt <text>       Prompt text
  --promptfiles <files...>  Read prompt from files (concatenated)
  --image <path>            Output image path (required)
  --provider google|openai  Force provider (auto-detect by default)
  -m, --model <id>          Model ID
  --ar <ratio>              Aspect ratio (e.g., 16:9, 1:1, 4:3)
  --size <WxH>              Size (e.g., 1024x1024)
  --quality normal|2k       Quality preset (default: normal)
  --ref <files...>          Reference images (Google multimodal only)
  --n <count>               Number of images (default: 1)
  --json                    JSON output
  -h, --help                Show help

Environment variables:
  OPENAI_API_KEY            OpenAI API key
  GOOGLE_API_KEY            Google API key
  OPENAI_IMAGE_MODEL        Default OpenAI model (gpt-image-1.5)
  GOOGLE_IMAGE_MODEL        Default Google model (gemini-3-pro-image-preview)
  OPENAI_BASE_URL           Custom OpenAI endpoint
  GOOGLE_BASE_URL           Custom Google endpoint

Env file load order: CLI args > process.env > <cwd>/.baoyu-skills/.env > ~/.baoyu-skills/.env`);
}

function parseArgs(argv: string[]): CliArgs {
  const out: CliArgs = {
    prompt: null,
    promptFiles: [],
    imagePath: null,
    provider: null,
    model: null,
    aspectRatio: null,
    size: null,
    quality: "normal",
    referenceImages: [],
    n: 1,
    json: false,
    help: false,
  };

  const positional: string[] = [];

  const takeMany = (i: number): { items: string[]; next: number } => {
    const items: string[] = [];
    let j = i + 1;
    while (j < argv.length) {
      const v = argv[j]!;
      if (v.startsWith("-")) break;
      items.push(v);
      j++;
    }
    return { items, next: j - 1 };
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]!;

    if (a === "--help" || a === "-h") {
      out.help = true;
      continue;
    }

    if (a === "--json") {
      out.json = true;
      continue;
    }

    if (a === "--prompt" || a === "-p") {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.prompt = v;
      continue;
    }

    if (a === "--promptfiles") {
      const { items, next } = takeMany(i);
      if (items.length === 0) throw new Error("Missing files for --promptfiles");
      out.promptFiles.push(...items);
      i = next;
      continue;
    }

    if (a === "--image") {
      const v = argv[++i];
      if (!v) throw new Error("Missing value for --image");
      out.imagePath = v;
      continue;
    }

    if (a === "--provider") {
      const v = argv[++i];
      if (v !== "google" && v !== "openai") throw new Error(`Invalid provider: ${v}`);
      out.provider = v;
      continue;
    }

    if (a === "--model" || a === "-m") {
      const v = argv[++i];
      if (!v) throw new Error(`Missing value for ${a}`);
      out.model = v;
      continue;
    }

    if (a === "--ar") {
      const v = argv[++i];
      if (!v) throw new Error("Missing value for --ar");
      out.aspectRatio = v;
      continue;
    }

    if (a === "--size") {
      const v = argv[++i];
      if (!v) throw new Error("Missing value for --size");
      out.size = v;
      continue;
    }

    if (a === "--quality") {
      const v = argv[++i];
      if (v !== "normal" && v !== "2k") throw new Error(`Invalid quality: ${v}`);
      out.quality = v;
      continue;
    }

    if (a === "--ref" || a === "--reference") {
      const { items, next } = takeMany(i);
      if (items.length === 0) throw new Error(`Missing files for ${a}`);
      out.referenceImages.push(...items);
      i = next;
      continue;
    }

    if (a === "--n") {
      const v = argv[++i];
      if (!v) throw new Error("Missing value for --n");
      out.n = parseInt(v, 10);
      if (isNaN(out.n) || out.n < 1) throw new Error(`Invalid count: ${v}`);
      continue;
    }

    if (a.startsWith("-")) {
      throw new Error(`Unknown option: ${a}`);
    }

    positional.push(a);
  }

  if (!out.prompt && out.promptFiles.length === 0 && positional.length > 0) {
    out.prompt = positional.join(" ");
  }

  return out;
}

async function loadEnvFile(p: string): Promise<Record<string, string>> {
  try {
    const content = await readFile(p, "utf8");
    const env: Record<string, string> = {};
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const idx = trimmed.indexOf("=");
      if (idx === -1) continue;
      const key = trimmed.slice(0, idx).trim();
      let val = trimmed.slice(idx + 1).trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      env[key] = val;
    }
    return env;
  } catch {
    return {};
  }
}

async function loadEnv(): Promise<void> {
  const home = homedir();
  const cwd = process.cwd();

  const homeEnv = await loadEnvFile(path.join(home, ".baoyu-skills", ".env"));
  const cwdEnv = await loadEnvFile(path.join(cwd, ".baoyu-skills", ".env"));

  for (const [k, v] of Object.entries(homeEnv)) {
    if (!process.env[k]) process.env[k] = v;
  }
  for (const [k, v] of Object.entries(cwdEnv)) {
    if (!process.env[k]) process.env[k] = v;
  }
}

async function readPromptFromFiles(files: string[]): Promise<string> {
  const parts: string[] = [];
  for (const f of files) {
    parts.push(await readFile(f, "utf8"));
  }
  return parts.join("\n\n");
}

async function readPromptFromStdin(): Promise<string | null> {
  if (process.stdin.isTTY) return null;
  try {
    const t = await Bun.stdin.text();
    const v = t.trim();
    return v.length > 0 ? v : null;
  } catch {
    return null;
  }
}

function normalizeOutputImagePath(p: string): string {
  const full = path.resolve(p);
  const ext = path.extname(full);
  if (ext) return full;
  return `${full}.png`;
}

function detectProvider(args: CliArgs): Provider {
  if (args.provider) return args.provider;

  const hasGoogle = !!process.env.GOOGLE_API_KEY;
  const hasOpenai = !!process.env.OPENAI_API_KEY;

  if (hasGoogle && !hasOpenai) return "google";
  if (hasOpenai && !hasGoogle) return "openai";
  if (hasGoogle && hasOpenai) return "google";

  throw new Error(
    "No API key found. Set GOOGLE_API_KEY or OPENAI_API_KEY.\n" +
      "Create ~/.baoyu-skills/.env or <cwd>/.baoyu-skills/.env with your keys."
  );
}

function getDefaultModel(provider: Provider): string {
  if (provider === "google") {
    return process.env.GOOGLE_IMAGE_MODEL || "gemini-3-pro-image-preview";
  }
  return process.env.OPENAI_IMAGE_MODEL || "gpt-image-1.5";
}

function isGoogleMultimodal(model: string): boolean {
  return GOOGLE_MULTIMODAL_MODELS.some((m) => model.includes(m));
}

function isGoogleImagen(model: string): boolean {
  return GOOGLE_IMAGEN_MODELS.some((m) => model.includes(m));
}

function buildPromptWithAspect(prompt: string, ar: string | null, quality: Quality): string {
  let result = prompt;
  if (ar) {
    result += ` Aspect ratio: ${ar}.`;
  }
  if (quality === "2k") {
    result += " High resolution 2048px.";
  }
  return result;
}

function parseAspectRatio(ar: string): { width: number; height: number } | null {
  const match = ar.match(/^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$/);
  if (!match) return null;
  const w = parseFloat(match[1]!);
  const h = parseFloat(match[2]!);
  if (w <= 0 || h <= 0) return null;
  return { width: w, height: h };
}

function getOpenAISize(ar: string | null, quality: Quality): string {
  const base = quality === "2k" ? 2048 : 1024;

  if (!ar) return `${base}x${base}`;

  const parsed = parseAspectRatio(ar);
  if (!parsed) return `${base}x${base}`;

  const ratio = parsed.width / parsed.height;

  if (Math.abs(ratio - 1) < 0.1) return `${base}x${base}`;
  if (ratio > 1.5) return quality === "2k" ? "2048x1024" : "1792x1024";
  if (ratio < 0.67) return quality === "2k" ? "1024x2048" : "1024x1792";
  return `${base}x${base}`;
}

async function readImageAsBase64(p: string): Promise<{ data: string; mimeType: string }> {
  const buf = await readFile(p);
  const ext = path.extname(p).toLowerCase();
  let mimeType = "image/png";
  if (ext === ".jpg" || ext === ".jpeg") mimeType = "image/jpeg";
  else if (ext === ".gif") mimeType = "image/gif";
  else if (ext === ".webp") mimeType = "image/webp";
  return { data: buf.toString("base64"), mimeType };
}

async function generateWithGoogleMultimodal(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const { generateText } = await import("ai");
  const { createGoogleGenerativeAI } = await import("@ai-sdk/google");

  const google = createGoogleGenerativeAI({
    apiKey: process.env.GOOGLE_API_KEY,
    baseURL: process.env.GOOGLE_BASE_URL,
  });

  const fullPrompt = buildPromptWithAspect(prompt, args.aspectRatio, args.quality);

  const messages: any[] = [];
  const content: any[] = [];

  for (const refPath of args.referenceImages) {
    const { data, mimeType } = await readImageAsBase64(refPath);
    content.push({ type: "image", image: data, mimeType });
  }
  content.push({ type: "text", text: fullPrompt });

  messages.push({ role: "user", content });

  const result = await generateText({
    model: google(model, { useSearchGrounding: false }),
    messages,
    providerOptions: {
      google: {
        responseModalities: ["TEXT", "IMAGE"],
      },
    },
  });

  const files = (result as any).files;
  if (!files || files.length === 0) {
    const expRes = (result as any).response?.body?.candidates?.[0]?.content?.parts;
    if (expRes) {
      for (const part of expRes) {
        if (part.inlineData?.data) {
          return Uint8Array.from(Buffer.from(part.inlineData.data, "base64"));
        }
      }
    }
    throw new Error("No image in response");
  }

  const img = files[0];
  if (img.uint8Array) return img.uint8Array;
  if (img.base64) return Uint8Array.from(Buffer.from(img.base64, "base64"));

  throw new Error("Cannot extract image data");
}

async function generateWithGoogleImagen(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const { experimental_generateImage: generateImage } = await import("ai");
  const { createGoogleGenerativeAI } = await import("@ai-sdk/google");

  const google = createGoogleGenerativeAI({
    apiKey: process.env.GOOGLE_API_KEY,
    baseURL: process.env.GOOGLE_BASE_URL,
  });

  const fullPrompt = buildPromptWithAspect(prompt, args.aspectRatio, args.quality);

  const result = await generateImage({
    model: google.image(model),
    prompt: fullPrompt,
    n: args.n,
    aspectRatio: args.aspectRatio || undefined,
  });

  const img = result.images[0];
  if (!img) throw new Error("No image in response");

  if (img.uint8Array) return img.uint8Array;
  if (img.base64) return Uint8Array.from(Buffer.from(img.base64, "base64"));

  throw new Error("Cannot extract image data");
}

async function generateWithOpenAI(
  prompt: string,
  model: string,
  args: CliArgs
): Promise<Uint8Array> {
  const baseURL = process.env.OPENAI_BASE_URL || "https://api.openai.com/v1";
  const apiKey = process.env.OPENAI_API_KEY;

  if (!apiKey) throw new Error("OPENAI_API_KEY is required");

  const size = args.size || getOpenAISize(args.aspectRatio, args.quality);

  const body: Record<string, any> = {
    model,
    prompt,
    size,
  };

  if (model.includes("dall-e-3")) {
    body.quality = args.quality === "2k" ? "hd" : "standard";
  }

  const res = await fetch(`${baseURL}/images/generations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`OpenAI API error: ${err}`);
  }

  const result = (await res.json()) as { data: Array<{ url?: string; b64_json?: string }> };
  const img = result.data[0];

  if (img?.b64_json) {
    return Uint8Array.from(Buffer.from(img.b64_json, "base64"));
  }

  if (img?.url) {
    const imgRes = await fetch(img.url);
    if (!imgRes.ok) throw new Error("Failed to download image");
    const buf = await imgRes.arrayBuffer();
    return new Uint8Array(buf);
  }

  throw new Error("No image in response");
}

async function generate(
  provider: Provider,
  model: string,
  prompt: string,
  args: CliArgs
): Promise<Uint8Array> {
  if (provider === "google") {
    if (isGoogleMultimodal(model)) {
      return generateWithGoogleMultimodal(prompt, model, args);
    }
    if (isGoogleImagen(model)) {
      if (args.referenceImages.length > 0) {
        console.error("Warning: Reference images not supported with Imagen models, ignoring.");
      }
      return generateWithGoogleImagen(prompt, model, args);
    }
    return generateWithGoogleMultimodal(prompt, model, args);
  }

  if (args.referenceImages.length > 0) {
    console.error("Warning: Reference images not supported with OpenAI, ignoring.");
  }
  return generateWithOpenAI(prompt, model, args);
}

async function main(): Promise<void> {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printUsage();
    return;
  }

  await loadEnv();

  let prompt: string | null = args.prompt;
  if (!prompt && args.promptFiles.length > 0) prompt = await readPromptFromFiles(args.promptFiles);
  if (!prompt) prompt = await readPromptFromStdin();

  if (!prompt) {
    console.error("Error: Prompt is required");
    printUsage();
    process.exitCode = 1;
    return;
  }

  if (!args.imagePath) {
    console.error("Error: --image is required");
    printUsage();
    process.exitCode = 1;
    return;
  }

  const provider = detectProvider(args);
  const model = args.model || getDefaultModel(provider);
  const outputPath = normalizeOutputImagePath(args.imagePath);

  let imageData: Uint8Array;
  let retried = false;

  while (true) {
    try {
      imageData = await generate(provider, model, prompt, args);
      break;
    } catch (e) {
      if (!retried) {
        retried = true;
        console.error("Generation failed, retrying...");
        continue;
      }
      throw e;
    }
  }

  const dir = path.dirname(outputPath);
  await mkdir(dir, { recursive: true });
  await writeFile(outputPath, imageData);

  if (args.json) {
    console.log(
      JSON.stringify(
        {
          savedImage: outputPath,
          provider,
          model,
          prompt: prompt.slice(0, 200),
        },
        null,
        2
      )
    );
  } else {
    console.log(outputPath);
  }
}

main().catch((e) => {
  const msg = e instanceof Error ? e.message : String(e);
  console.error(msg);
  process.exit(1);
});
