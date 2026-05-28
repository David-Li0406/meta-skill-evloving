#!/usr/bin/env npx ts-node
/**
 * Transcribe audio/video to SRT using ElevenLabs Scribe v2
 */

import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import { program } from 'commander';

dotenv.config();

const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
const ELEVENLABS_BASE_URL = 'https://api.elevenlabs.io';

interface Word {
  word: string;
  start: number;
  end: number;
}

interface TranscriptResult {
  text: string;
  words: Word[];
  duration: number;
  language: string;
}

interface SubtitleEntry {
  index: number;
  start: number;
  end: number;
  text: string;
}

function secondsToSrtTime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  const millis = Math.floor((seconds % 1) * 1000);
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${millis.toString().padStart(3, '0')}`;
}

async function transcribe(inputPath: string, language?: string): Promise<TranscriptResult> {
  if (!ELEVENLABS_API_KEY) {
    throw new Error('ELEVENLABS_API_KEY not set in .env');
  }

  if (!fs.existsSync(inputPath)) {
    throw new Error(`Input file not found: ${inputPath}`);
  }

  console.log(`Transcribing: ${path.basename(inputPath)}`);
  console.log(`Language: ${language || 'auto-detect'}`);

  const formData = new FormData();
  const fileBuffer = fs.readFileSync(inputPath);
  const blob = new Blob([fileBuffer]);
  formData.append('file', blob, path.basename(inputPath));
  formData.append('model_id', 'scribe_v2');
  formData.append('tag_audio_events', 'false');

  if (language) {
    formData.append('language_code', language);
  }

  const response = await fetch(`${ELEVENLABS_BASE_URL}/v1/speech-to-text`, {
    method: 'POST',
    headers: {
      'xi-api-key': ELEVENLABS_API_KEY,
    },
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Transcription failed: ${response.status} - ${errorText}`);
  }

  const result = await response.json() as any;

  const words: Word[] = (result.words || []).map((w: any) => ({
    word: w.text || w.word || '',
    start: w.start || 0,
    end: w.end || 0,
  }));

  const duration = words.length > 0 ? Math.max(...words.map(w => w.end)) : 0;

  console.log(`Done: ${words.length} words, ${duration.toFixed(1)}s`);

  return {
    text: result.text || '',
    words,
    duration,
    language: result.language_code || language || 'unknown',
  };
}

function generateSrt(
  words: Word[],
  options: {
    maxWords: number;
    maxDuration: number;
    maxChars: number;
    timingOffset: number;
  }
): SubtitleEntry[] {
  const entries: SubtitleEntry[] = [];
  let currentWords: Word[] = [];
  let currentStart: number | null = null;

  for (const word of words) {
    const wordText = word.word.trim();
    if (!wordText) continue;

    if (currentStart === null) {
      currentStart = word.start;
    }

    const testText = [...currentWords.map(w => w.word), wordText].join(' ');
    const entryDuration = word.end - currentStart;

    const shouldBreak =
      testText.length > options.maxChars ||
      entryDuration > options.maxDuration ||
      currentWords.length >= options.maxWords;

    if (shouldBreak && currentWords.length > 0) {
      const lastWord = currentWords[currentWords.length - 1];
      const entryEnd = lastWord.end;
      const text = currentWords.map(w => w.word).join(' ');

      entries.push({
        index: entries.length + 1,
        start: currentStart + options.timingOffset,
        end: entryEnd + options.timingOffset,
        text,
      });

      currentWords = [word];
      currentStart = word.start;
    } else {
      currentWords.push(word);
    }
  }

  // Add final entry
  if (currentWords.length > 0 && currentStart !== null) {
    const lastWord = currentWords[currentWords.length - 1];
    const text = currentWords.map(w => w.word).join(' ');

    entries.push({
      index: entries.length + 1,
      start: currentStart + options.timingOffset,
      end: lastWord.end + options.timingOffset,
      text,
    });
  }

  return entries;
}

function writeSrt(entries: SubtitleEntry[], outputPath: string): void {
  const lines: string[] = [];

  for (const entry of entries) {
    lines.push(entry.index.toString());
    lines.push(`${secondsToSrtTime(entry.start)} --> ${secondsToSrtTime(entry.end)}`);
    lines.push(entry.text);
    lines.push('');
  }

  fs.writeFileSync(outputPath, lines.join('\n'), 'utf-8');
  console.log(`Written: ${outputPath} (${entries.length} entries)`);
}

async function main() {
  program
    .requiredOption('-i, --input <path>', 'Input audio/video file')
    .requiredOption('-o, --output <path>', 'Output SRT file path')
    .option('-l, --language <code>', 'Language code (en, he, ar, etc.)')
    .option('--max-words <n>', 'Max words per subtitle', '5')
    .option('--max-duration <s>', 'Max duration per subtitle in seconds', '3.0')
    .option('--max-chars <n>', 'Max characters per subtitle', '70')
    .option('--timing-offset <s>', 'Timing offset in seconds', '0.25')
    .option('--json', 'Also output raw transcript JSON')
    .parse();

  const opts = program.opts();

  try {
    const transcript = await transcribe(opts.input, opts.language);

    const entries = generateSrt(transcript.words, {
      maxWords: parseInt(opts.maxWords),
      maxDuration: parseFloat(opts.maxDuration),
      maxChars: parseInt(opts.maxChars),
      timingOffset: parseFloat(opts.timingOffset),
    });

    writeSrt(entries, opts.output);

    if (opts.json) {
      const jsonPath = opts.output.replace(/\.srt$/i, '_transcript.json');
      fs.writeFileSync(jsonPath, JSON.stringify(transcript, null, 2), 'utf-8');
      console.log(`Written: ${jsonPath}`);
    }

    console.log('\n✓ Transcription complete!');
  } catch (error) {
    console.error('Error:', (error as Error).message);
    process.exit(1);
  }
}

main();
