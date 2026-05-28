const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
  console.error("Error: GEMINI_API_KEY environment variable is not set.");
  process.exit(1);
}

// Parse arguments
const args = process.argv.slice(2);
let model = "gemini-2.5-flash-image";
const inputs = [];
let aspectRatio = undefined;
let candidateCount = undefined;
let seed = undefined;
let useGoogleSearch = false;
let imageSize = undefined;
let outputPath = undefined;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === "--model") {
    if (i + 1 < args.length) {
      model = args[i + 1];
      i++;
    } else {
      console.error("Error: --model flag requires a value.");
      process.exit(1);
    }
  } else if (arg === "--aspectRatio" || arg === "--ar") {
    if (i + 1 < args.length) {
      aspectRatio = args[i + 1];
      i++;
    } else {
      console.error("Error: --aspectRatio flag requires a value.");
      process.exit(1);
    }
  } else if (arg === "--count") {
    if (i + 1 < args.length) {
      candidateCount = parseInt(args[i + 1], 10);
      i++;
    } else {
      console.error("Error: --count flag requires a value.");
      process.exit(1);
    }
  } else if (arg === "--seed") {
    if (i + 1 < args.length) {
      seed = parseInt(args[i + 1], 10);
      i++;
    } else {
      console.error("Error: --seed flag requires a value.");
      process.exit(1);
    }
  } else if (arg === "--imageSize") {
    if (i + 1 < args.length) {
      imageSize = args[i + 1];
      i++;
    } else {
      console.error("Error: --imageSize flag requires a value.");
      process.exit(1);
    }
  } else if (arg === "--output" || arg === "-o") {
    if (i + 1 < args.length) {
      outputPath = args[i + 1];
      i++;
    } else {
      console.error("Error: --output flag requires a value.");
      process.exit(1);
    }
  } else if (arg === "--googleSearch") {
    useGoogleSearch = true;
  } else {
    inputs.push(arg);
  }
}

if (inputs.length === 0) {
  console.error(
    "Usage: node nanobanana.js [--model <model_name>] [--aspectRatio <ratio>] [--count <number>] [--seed <number>] [--imageSize <size>] [--output <path>] [--googleSearch] <text_prompt> <image_path> ..."
  );
  process.exit(1);
}

const defaultOutputDir = "./nanobanana-outputs";
if (!outputPath && !fs.existsSync(defaultOutputDir)) {
  fs.mkdirSync(defaultOutputDir, { recursive: true });
}

// Helper to determine mime type
function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case ".png":
      return "image/png";
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".webp":
      return "image/webp";
    case ".heic":
      return "image/heic";
    case ".heif":
      return "image/heif";
    default:
      return "application/octet-stream";
  }
}

async function run() {
  const parts = [];

  for (const input of inputs) {
    if (fs.existsSync(input)) {
      try {
        const stats = fs.statSync(input);
        if (stats.isFile()) {
          const mimeType = getMimeType(input);
          if (mimeType.startsWith("image/")) {
            const imageData = fs.readFileSync(input).toString("base64");
            parts.push({
              inline_data: {
                mime_type: mimeType,
                data: imageData,
              },
            });
            continue;
          }
        }
      } catch (err) {}
    }
    parts.push({ text: input });
  }

  const generationConfig = {
    responseModalities: ["TEXT", "IMAGE"],
  };
  const imageConfig = {};
  if (aspectRatio) imageConfig.aspectRatio = aspectRatio;
  if (imageSize) imageConfig.imageSize = imageSize;

  if (Object.keys(imageConfig).length > 0) {
    generationConfig.imageConfig = imageConfig;
  }

  if (candidateCount) generationConfig.candidateCount = candidateCount;
  if (seed !== undefined) generationConfig.seed = seed;

  const requestBody = {
    contents: [
      {
        parts: parts,
      },
    ],
    generationConfig:
      Object.keys(generationConfig).length > 0 ? generationConfig : undefined,
  };

  if (useGoogleSearch) {
    requestBody.tools = [{ google_search: {} }];
  }

  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`;

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": apiKey,
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error (${response.status}):`, errorText);
      return;
    }

    const data = await response.json();

    if (data.error) {
      console.error("API Error:", JSON.stringify(data.error, null, 2));
      return;
    }

    if (
      data.candidates &&
      data.candidates[0] &&
      data.candidates[0].content
    ) {
      let imageIndex = 0;
      for (const part of data.candidates[0].content.parts) {
        if (part.text) {
          console.log(part.text);
        } else if (part.inlineData) {
          const imageData = part.inlineData.data;
          const buffer = Buffer.from(imageData, "base64");
          
          let finalPath;
          const uuid = crypto.randomUUID();

          if (outputPath) {
            const ext = path.extname(outputPath);
            if (ext) {
              // It's a file path
              const dir = path.dirname(outputPath);
              if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

              if (imageIndex === 0 && (!data.candidates[0].content.parts.filter(p => p.inlineData).length > 1 && !candidateCount || candidateCount === 1)) {
                 finalPath = outputPath;
              } else {
                 const name = path.basename(outputPath, ext);
                 finalPath = path.join(dir, `${name}-${imageIndex + 1}${ext}`);
              }
            } else {
              // It's a directory
               if (!fs.existsSync(outputPath)) fs.mkdirSync(outputPath, { recursive: true });
               finalPath = path.join(outputPath, `image-${uuid}.png`);
            }
          } else {
             // Default behavior
             finalPath = path.join(defaultOutputDir, `image-${uuid}.png`);
          }

          fs.writeFileSync(finalPath, buffer);
          console.log(`Image saved as ${finalPath}`);
          imageIndex++;
        }
      }
    } else {
      console.log(
        "No content in response:",
        JSON.stringify(data, null, 2)
      );
    }
  } catch (e) {
    console.error(`Problem with request: ${e.message}`);
    process.exit(1);
  }
}

run();
