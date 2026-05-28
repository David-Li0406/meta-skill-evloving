#!/usr/bin/env npx tsx

/**
 * Voice Scoring System
 *
 * Scores content against the voice profile for consistency.
 * Can be run standalone or imported as a module.
 */

import * as fs from "fs/promises";
import * as path from "path";

const UPDIKE_DIR = path.join(process.env.HOME || "~", ".updike");
const VOICE_DIR = path.join(UPDIKE_DIR, "voice");

interface VoiceProfile {
  stylometrics: {
    avg_sentence_length: number;
    sentence_length_stddev: number;
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
    humor_frequency: number;
    formality_score: number;
  };
  taboos: {
    hard_fail: string[];
    soft_warning: string[];
  };
}

interface VoiceScore {
  overall: number;
  passed: boolean;
  categories: {
    sentence_structure: number;
    vocabulary_match: number;
    tone_consistency: number;
    hook_usage: number;
    taboo_violations: number;
  };
  flags: string[];
  suggestions: string[];
}

// Taboo detection patterns
const TABOO_PATTERNS = {
  hashtags: /#\w+/g,
  corporate_jargon: /\b(synergy|leverage|disrupt|innovative|paradigm|holistic|bandwidth|circle back|touch base|deep dive)\b/gi,
  excessive_emojis: /[\u{1F300}-\u{1F9FF}]/gu,
};

async function loadProfile(): Promise<VoiceProfile | null> {
  try {
    const profilePath = path.join(VOICE_DIR, "profile.json");
    const content = await fs.readFile(profilePath, "utf-8");
    return JSON.parse(content);
  } catch {
    return null;
  }
}

function scoreSentenceStructure(content: string, profile: VoiceProfile): number {
  const sentences = content.split(/[.!?]+/).filter((s) => s.trim());
  if (sentences.length === 0) return 50;

  const lengths = sentences.map(
    (s) => s.trim().split(/\s+/).filter((w) => w).length
  );
  const avgLength = lengths.reduce((a, b) => a + b, 0) / lengths.length;

  const targetLength = profile.stylometrics.avg_sentence_length;
  const tolerance = profile.stylometrics.sentence_length_stddev;

  // Score based on how close we are to target
  const diff = Math.abs(avgLength - targetLength);
  if (diff <= tolerance) return 100;
  if (diff <= tolerance * 2) return 80;
  if (diff <= tolerance * 3) return 60;
  return 40;
}

function scoreVocabulary(content: string, profile: VoiceProfile): number {
  const lowerContent = content.toLowerCase();
  let score = 50; // Start at baseline

  // Check for signature phrases (+15 each, max 45)
  let phraseMatches = 0;
  for (const phrase of profile.vocabulary.signature_phrases) {
    if (lowerContent.includes(phrase.toLowerCase())) {
      phraseMatches++;
    }
  }
  score += Math.min(phraseMatches * 15, 45);

  // Check for high-frequency words (+1 each, max 10)
  let wordMatches = 0;
  for (const word of profile.vocabulary.high_frequency.slice(0, 20)) {
    if (lowerContent.includes(word.toLowerCase())) {
      wordMatches++;
    }
  }
  score += Math.min(wordMatches, 10);

  // Penalize avoided words (-10 each)
  for (const word of profile.vocabulary.avoided_words) {
    const regex = new RegExp(`\\b${word}\\b`, "gi");
    const matches = content.match(regex);
    if (matches) {
      score -= matches.length * 10;
    }
  }

  return Math.max(0, Math.min(100, score));
}

function scoreToneConsistency(content: string, profile: VoiceProfile): number {
  let score = 70; // Start above baseline assuming generally good

  // Check for formality indicators
  const formalIndicators = /\b(therefore|however|furthermore|moreover|consequently|nevertheless)\b/gi;
  const casualIndicators = /\b(like|kinda|sorta|gonna|wanna|basically|honestly|literally)\b/gi;

  const formalCount = (content.match(formalIndicators) || []).length;
  const casualCount = (content.match(casualIndicators) || []).length;

  // Target formality_score of 2 means we want mostly casual
  if (profile.tone.formality_score <= 2) {
    // Penalize formal language
    score -= formalCount * 5;
    // Slight bonus for casual (but not too much)
    score += Math.min(casualCount * 2, 10);
  }

  // Check for self-deprecating humor patterns
  const selfDeprecating = /\b(i (was|am) (wrong|stupid|dumb|an idiot)|my mistake|i messed up|i screwed up)\b/gi;
  if (content.match(selfDeprecating)) {
    score += 10;
  }

  // Check for direct address
  const directAddress = /\b(you|your|you're|you've)\b/gi;
  const directMatches = (content.match(directAddress) || []).length;
  if (directMatches >= 2) {
    score += 5;
  }

  return Math.max(0, Math.min(100, score));
}

function scoreHookUsage(content: string): number {
  // Check if the content starts with a strong hook
  const firstSentence = content.split(/[.!?]/)[0]?.trim() || "";

  // Hook patterns
  const hookPatterns = [
    /^here's (the thing|what)/i,
    /^let me tell you/i,
    /^i (learned|discovered|realized)/i,
    /^the (truth|reality|thing) is/i,
    /^when i was/i,
    /^\d+ (things|lessons|mistakes)/i,
    /^everyone (thinks|says|believes)/i,
    /^most people (don't|never|won't)/i,
    /^what (if|nobody)/i,
    /^i used to/i,
  ];

  for (const pattern of hookPatterns) {
    if (pattern.test(firstSentence)) {
      return 100;
    }
  }

  // Check for question hook
  if (firstSentence.endsWith("?")) {
    return 85;
  }

  // Check for story hook (starts with context)
  if (/^(in|back in|last|years? ago)/i.test(firstSentence)) {
    return 80;
  }

  // Generic start
  return 50;
}

function scoreTabooViolations(content: string): { score: number; violations: string[] } {
  const violations: string[] = [];

  // Check for hashtags (HARD FAIL)
  const hashtags = content.match(TABOO_PATTERNS.hashtags);
  if (hashtags) {
    return {
      score: 0,
      violations: [`Contains hashtags: ${hashtags.slice(0, 3).join(", ")}`],
    };
  }

  // Check for corporate jargon (HARD FAIL)
  const jargon = content.match(TABOO_PATTERNS.corporate_jargon);
  if (jargon && jargon.length >= 2) {
    return {
      score: 0,
      violations: [`Contains corporate jargon: ${[...new Set(jargon)].slice(0, 3).join(", ")}`],
    };
  }

  let score = 100;

  // Single jargon word is a warning
  if (jargon && jargon.length === 1) {
    score -= 20;
    violations.push(`Contains jargon word: ${jargon[0]}`);
  }

  // Check for excessive emojis
  const emojis = content.match(TABOO_PATTERNS.excessive_emojis);
  if (emojis && emojis.length > 3) {
    score -= 30;
    violations.push("Contains excessive emojis");
  } else if (emojis && emojis.length > 1) {
    score -= 10;
    violations.push("Multiple emojis (consider reducing)");
  }

  return { score, violations };
}

function generateSuggestions(
  categories: VoiceScore["categories"],
  content: string,
  profile: VoiceProfile
): string[] {
  const suggestions: string[] = [];

  if (categories.sentence_structure < 70) {
    const sentences = content.split(/[.!?]+/).filter((s) => s.trim());
    const lengths = sentences.map(
      (s) => s.trim().split(/\s+/).filter((w) => w).length
    );
    const avgLength = lengths.reduce((a, b) => a + b, 0) / lengths.length;

    if (avgLength > profile.stylometrics.avg_sentence_length + 5) {
      suggestions.push("Sentences are too long. Break them up for punchier delivery.");
    } else if (avgLength < profile.stylometrics.avg_sentence_length - 5) {
      suggestions.push("Sentences are very short. Consider combining some for better flow.");
    }
  }

  if (categories.vocabulary_match < 70) {
    suggestions.push(
      `Consider using signature phrases like: "${profile.vocabulary.signature_phrases[0]}"`
    );
  }

  if (categories.hook_usage < 70) {
    suggestions.push(
      'Start with a stronger hook. Try: "Here\'s the thing:", "Let me tell you a story:", or a provocative question.'
    );
  }

  if (categories.tone_consistency < 70) {
    suggestions.push(
      "Tone feels off. Aim for conversational and direct. Add a personal anecdote."
    );
  }

  return suggestions;
}

export async function scoreContent(content: string): Promise<VoiceScore> {
  const profile = await loadProfile();

  if (!profile) {
    // Return a basic score if no profile exists
    const tabooResult = scoreTabooViolations(content);
    return {
      overall: tabooResult.score > 0 ? 60 : 0,
      passed: tabooResult.score > 0,
      categories: {
        sentence_structure: 60,
        vocabulary_match: 60,
        tone_consistency: 60,
        hook_usage: scoreHookUsage(content),
        taboo_violations: tabooResult.score,
      },
      flags: tabooResult.violations.length > 0
        ? ["No voice profile found - using basic scoring", ...tabooResult.violations]
        : ["No voice profile found - using basic scoring"],
      suggestions: ["Run '/updike voice' to generate a voice profile for better scoring"],
    };
  }

  // Score each category
  const tabooResult = scoreTabooViolations(content);

  // If hard taboo violation, fail immediately
  if (tabooResult.score === 0) {
    return {
      overall: 0,
      passed: false,
      categories: {
        sentence_structure: 0,
        vocabulary_match: 0,
        tone_consistency: 0,
        hook_usage: 0,
        taboo_violations: 0,
      },
      flags: ["HARD FAIL: " + tabooResult.violations[0]],
      suggestions: ["Remove the taboo element and regenerate"],
    };
  }

  const categories = {
    sentence_structure: scoreSentenceStructure(content, profile),
    vocabulary_match: scoreVocabulary(content, profile),
    tone_consistency: scoreToneConsistency(content, profile),
    hook_usage: scoreHookUsage(content),
    taboo_violations: tabooResult.score,
  };

  // Calculate weighted overall score
  const weights = {
    sentence_structure: 0.2,
    vocabulary_match: 0.25,
    tone_consistency: 0.3,
    hook_usage: 0.15,
    taboo_violations: 0.1,
  };

  const overall = Math.round(
    Object.entries(categories).reduce(
      (sum, [key, value]) => sum + value * weights[key as keyof typeof weights],
      0
    )
  );

  const flags = tabooResult.violations;
  const suggestions = generateSuggestions(categories, content, profile);

  return {
    overall,
    passed: overall >= 70,
    categories,
    flags,
    suggestions,
  };
}

// CLI interface
async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log("Usage: npx tsx score-content.ts <content>");
    console.log("       npx tsx score-content.ts --file <filepath>");
    return;
  }

  let content: string;

  if (args[0] === "--file") {
    content = await fs.readFile(args[1], "utf-8");
  } else {
    content = args.join(" ");
  }

  const score = await scoreContent(content);

  console.log("\n=== Voice Score ===\n");
  console.log(`Overall: ${score.overall}/100 ${score.passed ? "✓ PASS" : "✗ FAIL"}`);
  console.log("\nCategories:");
  console.log(`  Sentence Structure: ${score.categories.sentence_structure}/100`);
  console.log(`  Vocabulary Match:   ${score.categories.vocabulary_match}/100`);
  console.log(`  Tone Consistency:   ${score.categories.tone_consistency}/100`);
  console.log(`  Hook Usage:         ${score.categories.hook_usage}/100`);
  console.log(`  Taboo Violations:   ${score.categories.taboo_violations}/100`);

  if (score.flags.length > 0) {
    console.log("\nFlags:");
    for (const flag of score.flags) {
      console.log(`  ⚠️  ${flag}`);
    }
  }

  if (score.suggestions.length > 0) {
    console.log("\nSuggestions:");
    for (const suggestion of score.suggestions) {
      console.log(`  → ${suggestion}`);
    }
  }
}

// Run if called directly
if (process.argv[1]?.includes("score-content")) {
  main().catch(console.error);
}
