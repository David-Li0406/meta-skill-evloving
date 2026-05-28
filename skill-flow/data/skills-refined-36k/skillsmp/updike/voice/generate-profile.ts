#!/usr/bin/env npx tsx

/**
 * Voice Profile Generator
 *
 * Analyzes content from all sources to build a comprehensive voice profile.
 * Run with: npx tsx ~/.updike/voice/generate-profile.ts
 */

import * as fs from "fs/promises";
import * as path from "path";
import Anthropic from "@anthropic-ai/sdk";

const UPDIKE_DIR = path.join(process.env.HOME || "~", ".updike");
const CONTENT_DIR = path.join(UPDIKE_DIR, "content");
const VOICE_DIR = path.join(UPDIKE_DIR, "voice");

interface VoiceProfile {
  version: string;
  generated_at: string;
  source_stats: {
    tweets_analyzed: number;
    newsletters_analyzed: number;
    book_chapters_analyzed: number;
    youtube_transcripts_analyzed: number;
    total_words: number;
  };
  stylometrics: {
    avg_sentence_length: number;
    sentence_length_stddev: number;
    avg_paragraph_length: number;
    fragment_ratio: number;
    question_ratio: number;
  };
  vocabulary: {
    high_frequency: string[];
    signature_phrases: string[];
    industry_terms: string[];
    avoided_words: string[];
  };
  tone: {
    primary: string;
    secondary: string[];
    humor_frequency: number;
    formality_score: number;
  };
  structural: {
    common_hooks: string[];
    closing_patterns: string[];
  };
  platform_adaptations: {
    x: {
      max_length_used: number;
      thread_frequency: number;
      emoji_usage: string;
    };
    linkedin: {
      typical_length: number;
      uses_line_breaks: boolean;
      personal_story_ratio: number;
    };
  };
  taboos: {
    hard_fail: string[];
    soft_warning: string[];
  };
}

async function readAllContent(): Promise<{ source: string; content: string }[]> {
  const allContent: { source: string; content: string }[] = [];

  const sources = ["tweets", "newsletters", "book", "youtube"];

  for (const source of sources) {
    const sourceDir = path.join(CONTENT_DIR, source);
    try {
      const files = await fs.readdir(sourceDir);
      for (const file of files) {
        if (file.endsWith(".md")) {
          const content = await fs.readFile(path.join(sourceDir, file), "utf-8");
          // Strip frontmatter
          const body = content.replace(/^---[\s\S]*?---\n/, "");
          allContent.push({ source: source.replace(/s$/, ""), content: body });
        }
      }
    } catch {
      // Directory doesn't exist yet
    }
  }

  return allContent;
}

function calculateBasicStats(texts: string[]): {
  avgSentenceLength: number;
  sentenceLengthStddev: number;
  avgParagraphLength: number;
  fragmentRatio: number;
  questionRatio: number;
  totalWords: number;
} {
  const allSentences: number[] = [];
  const allParagraphs: number[] = [];
  let totalQuestions = 0;
  let totalFragments = 0;
  let totalWords = 0;

  for (const text of texts) {
    // Split into paragraphs
    const paragraphs = text.split(/\n\n+/).filter((p) => p.trim());
    allParagraphs.push(paragraphs.length);

    // Split into sentences (rough approximation)
    const sentences = text.split(/[.!?]+/).filter((s) => s.trim());

    for (const sentence of sentences) {
      const words = sentence.trim().split(/\s+/).filter((w) => w);
      if (words.length > 0) {
        allSentences.push(words.length);
        totalWords += words.length;

        // Check for fragments (very short "sentences")
        if (words.length <= 3) {
          totalFragments++;
        }
      }
    }

    // Count questions
    totalQuestions += (text.match(/\?/g) || []).length;
  }

  const avgSentenceLength =
    allSentences.length > 0
      ? allSentences.reduce((a, b) => a + b, 0) / allSentences.length
      : 0;

  const sentenceLengthStddev =
    allSentences.length > 0
      ? Math.sqrt(
          allSentences
            .map((x) => Math.pow(x - avgSentenceLength, 2))
            .reduce((a, b) => a + b, 0) / allSentences.length
        )
      : 0;

  const avgParagraphLength =
    allParagraphs.length > 0
      ? allParagraphs.reduce((a, b) => a + b, 0) / allParagraphs.length
      : 0;

  return {
    avgSentenceLength: Math.round(avgSentenceLength * 10) / 10,
    sentenceLengthStddev: Math.round(sentenceLengthStddev * 10) / 10,
    avgParagraphLength: Math.round(avgParagraphLength * 10) / 10,
    fragmentRatio:
      allSentences.length > 0
        ? Math.round((totalFragments / allSentences.length) * 100) / 100
        : 0,
    questionRatio:
      allSentences.length > 0
        ? Math.round((totalQuestions / allSentences.length) * 100) / 100
        : 0,
    totalWords,
  };
}

function findHighFrequencyWords(texts: string[], topN: number = 20): string[] {
  const wordCounts: Record<string, number> = {};
  const stopWords = new Set([
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "by",
    "from",
    "is",
    "was",
    "are",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "must",
    "can",
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    "i",
    "you",
    "he",
    "she",
    "we",
    "they",
    "me",
    "him",
    "her",
    "us",
    "them",
    "my",
    "your",
    "his",
    "our",
    "their",
    "what",
    "which",
    "who",
    "when",
    "where",
    "why",
    "how",
    "all",
    "each",
    "every",
    "both",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "just",
    "about",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "between",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "if",
    "because",
    "as",
    "until",
    "while",
  ]);

  for (const text of texts) {
    const words = text.toLowerCase().match(/\b[a-z']+\b/g) || [];
    for (const word of words) {
      if (!stopWords.has(word) && word.length > 2) {
        wordCounts[word] = (wordCounts[word] || 0) + 1;
      }
    }
  }

  return Object.entries(wordCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN)
    .map(([word]) => word);
}

function findPhrases(texts: string[]): string[] {
  // Look for common multi-word patterns
  const phraseCounts: Record<string, number> = {};

  // Known hook patterns to look for
  const hookPatterns = [
    /here's the thing/gi,
    /let me tell you/gi,
    /i learned this/gi,
    /the hard way/gi,
    /here's what/gi,
    /the truth is/gi,
    /i used to/gi,
    /when i was/gi,
    /one thing i/gi,
    /the best advice/gi,
    /what i've learned/gi,
    /the biggest mistake/gi,
  ];

  for (const text of texts) {
    for (const pattern of hookPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        for (const match of matches) {
          const normalized = match.toLowerCase();
          phraseCounts[normalized] = (phraseCounts[normalized] || 0) + 1;
        }
      }
    }
  }

  return Object.entries(phraseCounts)
    .filter(([, count]) => count >= 2)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([phrase]) => phrase);
}

async function analyzeWithClaude(
  allContent: { source: string; content: string }[]
): Promise<Partial<VoiceProfile>> {
  const anthropic = new Anthropic();

  // Sample content for analysis (to fit in context)
  const sampleSize = 20;
  const samples = allContent
    .sort(() => Math.random() - 0.5)
    .slice(0, sampleSize)
    .map((c) => `[${c.source}]\n${c.content.slice(0, 1000)}`)
    .join("\n\n---\n\n");

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 2000,
    messages: [
      {
        role: "user",
        content: `Analyze this writing sample from Andrew Wilkinson to extract voice characteristics.

SAMPLES:
${samples}

Return a JSON object with these fields:
{
  "tone": {
    "primary": "single word describing dominant tone",
    "secondary": ["2-3 secondary tone descriptors"],
    "humor_frequency": 0.0-1.0,
    "formality_score": 1-5 (1=very casual, 5=very formal)
  },
  "structural": {
    "common_hooks": ["list of opening patterns you see"],
    "closing_patterns": ["list of closing patterns you see"]
  },
  "vocabulary": {
    "industry_terms": ["business/tech terms used frequently"],
    "avoided_words": ["corporate jargon NOT used that similar writers often use"]
  }
}

Be specific to this author's style. Return ONLY valid JSON.`,
      },
    ],
  });

  const text = response.content[0].type === "text" ? response.content[0].text : "";

  // Extract JSON from response
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch {
      console.error("Failed to parse Claude response as JSON");
    }
  }

  return {};
}

async function generateProfile(): Promise<void> {
  console.log("Reading content from all sources...");
  const allContent = await readAllContent();

  if (allContent.length === 0) {
    console.log("No content found. Run ingestion first:");
    console.log("  /updike scan");
    return;
  }

  console.log(`Found ${allContent.length} content pieces`);

  // Count by source
  const sourceCounts = {
    tweets_analyzed: allContent.filter((c) => c.source === "tweet").length,
    newsletters_analyzed: allContent.filter((c) => c.source === "newsletter")
      .length,
    book_chapters_analyzed: allContent.filter((c) => c.source === "book").length,
    youtube_transcripts_analyzed: allContent.filter((c) => c.source === "youtube")
      .length,
    total_words: 0,
  };

  // Calculate basic statistics
  console.log("Calculating stylometric features...");
  const texts = allContent.map((c) => c.content);
  const stats = calculateBasicStats(texts);
  sourceCounts.total_words = stats.totalWords;

  // Find high-frequency words
  console.log("Analyzing vocabulary patterns...");
  const highFrequency = findHighFrequencyWords(texts);
  const signaturePhrases = findPhrases(texts);

  // Use Claude for deeper analysis
  console.log("Running AI analysis...");
  const claudeAnalysis = await analyzeWithClaude(allContent);

  // Assemble profile
  const profile: VoiceProfile = {
    version: "1.0",
    generated_at: new Date().toISOString(),
    source_stats: sourceCounts,
    stylometrics: {
      avg_sentence_length: stats.avgSentenceLength,
      sentence_length_stddev: stats.sentenceLengthStddev,
      avg_paragraph_length: stats.avgParagraphLength,
      fragment_ratio: stats.fragmentRatio,
      question_ratio: stats.questionRatio,
    },
    vocabulary: {
      high_frequency: highFrequency,
      signature_phrases:
        signaturePhrases.length > 0
          ? signaturePhrases
          : [
              "Here's the thing:",
              "Let me tell you a story:",
              "I learned this the hard way:",
            ],
      industry_terms: claudeAnalysis.vocabulary?.industry_terms || [
        "startup",
        "founder",
        "acquired",
        "bootstrap",
        "exit",
      ],
      avoided_words: claudeAnalysis.vocabulary?.avoided_words || [
        "synergy",
        "leverage",
        "disrupt",
        "innovative",
        "paradigm",
      ],
    },
    tone: {
      primary: claudeAnalysis.tone?.primary || "conversational",
      secondary: claudeAnalysis.tone?.secondary || [
        "self-deprecating",
        "direct",
        "reflective",
      ],
      humor_frequency: claudeAnalysis.tone?.humor_frequency || 0.12,
      formality_score: claudeAnalysis.tone?.formality_score || 2,
    },
    structural: {
      common_hooks: claudeAnalysis.structural?.common_hooks || [
        'Number-based ("3 things I learned...")',
        'Story-based ("When I was 25...")',
        'Contrarian ("Everyone says X. I disagree.")',
      ],
      closing_patterns: claudeAnalysis.structural?.closing_patterns || [
        "Call to reflection",
        "Single line takeaway",
        "Question to reader",
      ],
    },
    platform_adaptations: {
      x: {
        max_length_used: 280,
        thread_frequency: 0.1,
        emoji_usage: "minimal",
      },
      linkedin: {
        typical_length: 800,
        uses_line_breaks: true,
        personal_story_ratio: 0.7,
      },
    },
    taboos: {
      hard_fail: ["hashtags", "corporate_jargon", "excessive_emojis"],
      soft_warning: ["too_formal", "generic_advice", "clickbait"],
    },
  };

  // Save profile
  await fs.mkdir(VOICE_DIR, { recursive: true });
  const profilePath = path.join(VOICE_DIR, "profile.json");
  await fs.writeFile(profilePath, JSON.stringify(profile, null, 2));

  console.log(`\nVoice profile generated: ${profilePath}`);
  console.log("\nSummary:");
  console.log(`  Sources analyzed: ${allContent.length} pieces`);
  console.log(`  Total words: ${sourceCounts.total_words.toLocaleString()}`);
  console.log(`  Avg sentence length: ${profile.stylometrics.avg_sentence_length} words`);
  console.log(`  Primary tone: ${profile.tone.primary}`);
  console.log(`  Signature phrases: ${profile.vocabulary.signature_phrases.slice(0, 3).join(", ")}`);
}

// Run if called directly
generateProfile().catch(console.error);
