/**
 * ElevenLabs Music Generator
 *
 * Generate AI music with simple prompts or detailed composition plans
 */

import * as dotenv from "dotenv";
import * as path from "path";
import * as fs from "fs";

// Load environment variables
dotenv.config({ path: path.join(__dirname, ".env") });

const API_KEY = process.env.ELEVENLABS_API_KEY;
const MUSIC_URL = "https://api.elevenlabs.io/v1/music";
const DETAILED_MUSIC_URL = "https://api.elevenlabs.io/v1/music/detailed";

// ============================================
// Types
// ============================================

interface CompositionSection {
  section_name: string;
  positive_local_styles: string[];
  negative_local_styles: string[];
  duration_ms: number;
  lines: string[];
}

interface CompositionPlan {
  positive_global_styles: string[];
  negative_global_styles: string[];
  sections: CompositionSection[];
}

interface CompositionConfig {
  duration_ms: number;
  instrumental: boolean;
  positive_global_styles: string[];
  negative_global_styles: string[];
  sections: CompositionSection[];
}

interface Args {
  prompt?: string;
  composition?: string;
  duration?: number;
  output?: string;
  instrumental?: boolean;
  format?: string;
  listStyles?: boolean;
  help?: boolean;
}

// ============================================
// Argument Parsing
// ============================================

function parseArgs(): Args {
  const args = process.argv.slice(2);
  const result: Args = {};

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "-p":
      case "--prompt":
        result.prompt = args[++i];
        break;
      case "-c":
      case "--composition":
        result.composition = args[++i];
        break;
      case "-d":
      case "--duration":
        result.duration = parseInt(args[++i], 10);
        break;
      case "-o":
      case "--output":
        result.output = args[++i];
        break;
      case "-i":
      case "--instrumental":
        result.instrumental = true;
        break;
      case "-f":
      case "--format":
        result.format = args[++i];
        break;
      case "--list-styles":
        result.listStyles = true;
        break;
      case "-h":
      case "--help":
        result.help = true;
        break;
    }
  }

  return result;
}

// ============================================
// Help & Styles
// ============================================

function showHelp(): void {
  console.log(`
Music Generator - ElevenLabs AI Music

Usage:
  npx ts-node generate_music.ts [options]

Options:
  -p, --prompt <TEXT>        Text prompt for simple generation
  -c, --composition <PATH>   JSON file for detailed composition
  -d, --duration <SECONDS>   Duration in seconds (simple mode, default: 60)
  -o, --output <PATH>        Output file path (required)
  -i, --instrumental         Generate instrumental track (no vocals)
  -f, --format <FORMAT>      Output format (default: mp3_44100_192)
  --list-styles              Show available style suggestions
  -h, --help                 Show this help

Examples:
  # Simple prompt-based generation
  npx ts-node generate_music.ts -p "Uplifting corporate music" -d 60 -o music.mp3

  # Detailed composition from JSON
  npx ts-node generate_music.ts -c composition.json -o detailed.mp3

  # Instrumental with specific format
  npx ts-node generate_music.ts -p "Epic cinematic" -i -d 120 -o epic.mp3

Output Formats:
  mp3_44100_192     MP3, 44.1kHz, 192kbps (default, best quality)
  mp3_44100_128     MP3, 44.1kHz, 128kbps
  mp3_22050_32      MP3, 22kHz, 32kbps (smallest)

Duration Limits:
  Minimum: 15 seconds
  Maximum: 330 seconds (5.5 minutes)
`);
}

function showStyles(): void {
  console.log(`
=== Available Music Styles ===

MOODS:
  uplifting, inspiring, motivational, peaceful, energetic
  dramatic, epic, emotional, nostalgic, mysterious
  playful, cheerful, romantic, melancholic, dark
  tense, suspenseful, relaxing, meditative

GENRES:
  corporate, cinematic, electronic, ambient, orchestral
  pop, rock, jazz, classical, world music
  lo-fi, hip-hop, EDM, acoustic, folk
  synthwave, chillhop, trap, house, techno

INSTRUMENTS:
  piano, guitar, strings, synths, drums
  brass, woodwinds, percussion, bass
  violin, cello, flute, saxophone, trumpet

TEMPO/ENERGY:
  slow, moderate, fast, driving
  calm, building, intense, explosive

SECTION STYLES (for compositions):
  Intros: soft opening, building momentum, atmospheric, gentle start
  Peaks: energetic peak, driving rhythm, powerful, emotional climax
  Outros: gentle fade, triumphant ending, resolution, hopeful conclusion

NEGATIVE STYLES (what to avoid):
  aggressive, dark, scary, chaotic
  heavy metal, death metal, harsh noise
  explicit, profane, distorted

Example Prompts:
  "Uplifting corporate music with modern electronic elements"
  "Peaceful ambient soundscape with piano and strings"
  "Energetic workout music with driving beats"
  "Cinematic orchestral theme with epic brass"
  "Lo-fi hip-hop beats for studying and relaxation"
`);
}

// ============================================
// API Functions
// ============================================

async function generateSimpleMusic(
  prompt: string,
  durationSeconds: number,
  instrumental: boolean,
  outputFormat: string
): Promise<Buffer> {
  console.log("\n=== Generating Music (Simple Mode) ===");
  console.log(`Prompt: "${prompt.substring(0, 80)}${prompt.length > 80 ? "..." : ""}"`);
  console.log(`Duration: ${durationSeconds} seconds`);
  console.log(`Instrumental: ${instrumental}`);
  console.log(`Format: ${outputFormat}`);
  console.log("\nGenerating... (this may take 30-60 seconds)\n");

  const response = await fetch(MUSIC_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "xi-api-key": API_KEY!,
    },
    body: JSON.stringify({
      prompt,
      duration_ms: durationSeconds * 1000,
      instrumental,
      output_format: outputFormat,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Music API failed: ${response.status} - ${errorText}`);
  }

  return Buffer.from(await response.arrayBuffer());
}

async function generateDetailedMusic(
  config: CompositionConfig,
  outputFormat: string
): Promise<Buffer> {
  console.log("\n=== Generating Music (Detailed Mode) ===");
  console.log(`Duration: ${config.duration_ms / 1000} seconds`);
  console.log(`Instrumental: ${config.instrumental}`);
  console.log(`Sections: ${config.sections.length}`);
  config.sections.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.section_name} (${s.duration_ms / 1000}s)`);
  });
  console.log(`Format: ${outputFormat}`);
  console.log("\nGenerating... (this may take 30-90 seconds)\n");

  const compositionPlan: CompositionPlan = {
    positive_global_styles: config.positive_global_styles,
    negative_global_styles: config.negative_global_styles,
    sections: config.sections,
  };

  const response = await fetch(DETAILED_MUSIC_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "xi-api-key": API_KEY!,
    },
    body: JSON.stringify({
      instrumental: config.instrumental,
      duration_ms: config.duration_ms,
      composition_plan: compositionPlan,
      output_format: outputFormat,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Music API failed: ${response.status} - ${errorText}`);
  }

  // Handle response (may be multipart)
  const contentType = response.headers.get("content-type") || "";
  const arrayBuffer = await response.arrayBuffer();
  let audioBuffer = Buffer.from(arrayBuffer);

  if (contentType.includes("multipart")) {
    const boundaryMatch = contentType.match(/boundary=([^\s;]+)/);
    const boundary = boundaryMatch ? boundaryMatch[1] : null;

    if (boundary) {
      const bytes = new Uint8Array(arrayBuffer);
      const text = new TextDecoder("latin1").decode(bytes);
      const parts = text.split(`--${boundary}`);

      for (const part of parts) {
        if (part.includes("Content-Type: audio/") || part.includes("application/octet-stream")) {
          const headerEnd = part.indexOf("\r\n\r\n");
          if (headerEnd !== -1) {
            const body = part.substring(headerEnd + 4).replace(/\r\n$/, "");
            audioBuffer = Buffer.from(body, "latin1");
            break;
          }
        }
      }
    }
  }

  return audioBuffer;
}

// ============================================
// Main
// ============================================

async function main(): Promise<void> {
  // Validate API key
  if (!API_KEY) {
    console.error("Error: Missing ELEVENLABS_API_KEY in .env file");
    console.error("Create .env file with: ELEVENLABS_API_KEY=your_key_here");
    process.exit(1);
  }

  const args = parseArgs();

  // Show help
  if (args.help) {
    showHelp();
    process.exit(0);
  }

  // List styles
  if (args.listStyles) {
    showStyles();
    process.exit(0);
  }

  // Validate output
  if (!args.output) {
    console.error("Error: --output is required");
    showHelp();
    process.exit(1);
  }

  // Validate mode
  if (!args.prompt && !args.composition) {
    console.error("Error: Either --prompt or --composition is required");
    showHelp();
    process.exit(1);
  }

  const outputFormat = args.format || "mp3_44100_192";

  try {
    let audioBuffer: Buffer;

    if (args.composition) {
      // Detailed composition mode
      const configPath = path.resolve(args.composition);
      if (!fs.existsSync(configPath)) {
        console.error(`Error: Composition file not found: ${configPath}`);
        process.exit(1);
      }

      const configContent = fs.readFileSync(configPath, "utf-8");
      const config: CompositionConfig = JSON.parse(configContent);

      // Validate composition config
      if (!config.sections || config.sections.length === 0) {
        console.error("Error: Composition must have at least one section");
        process.exit(1);
      }

      // Ensure all sections have required fields
      for (const section of config.sections) {
        if (!section.lines) {
          section.lines = [];
        }
        if (!section.positive_local_styles) {
          section.positive_local_styles = [];
        }
        if (!section.negative_local_styles) {
          section.negative_local_styles = [];
        }
      }

      audioBuffer = await generateDetailedMusic(config, outputFormat);
    } else {
      // Simple prompt mode
      const duration = args.duration || 60;

      // Validate duration
      if (duration < 15) {
        console.error("Error: Minimum duration is 15 seconds");
        process.exit(1);
      }
      if (duration > 330) {
        console.error("Error: Maximum duration is 330 seconds (5.5 minutes)");
        process.exit(1);
      }

      audioBuffer = await generateSimpleMusic(
        args.prompt!,
        duration,
        args.instrumental || false,
        outputFormat
      );
    }

    // Ensure output directory exists
    const outputDir = path.dirname(args.output);
    if (outputDir && !fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Save the file
    fs.writeFileSync(args.output, audioBuffer);

    const fileSizeMB = (audioBuffer.length / 1024 / 1024).toFixed(2);
    console.log(`\n✅ Music generated successfully!`);
    console.log(`📁 Output: ${args.output}`);
    console.log(`📊 Size: ${fileSizeMB} MB`);

  } catch (error) {
    console.error("\nError generating music:", error);
    process.exit(1);
  }
}

main();
