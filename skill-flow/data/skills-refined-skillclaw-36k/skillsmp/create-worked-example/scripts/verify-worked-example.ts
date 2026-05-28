#!/usr/bin/env tsx

/**
 * Worked Example Verification Script
 *
 * Validates structural requirements for a worked example presentation.
 * This script checks for FILES and METADATA - it does NOT validate
 * pedagogical quality (that requires human/AI review).
 *
 * What this script checks:
 * - All required slide files exist
 * - metadata.json has required fields
 * - Progress file has been cleaned up
 *
 * What this script does NOT check (requires manual review):
 * - Strategy consistency across slides
 * - CFU question quality
 * - Visual stability
 * - Scaffolding removal on practice slides
 *
 * Usage:
 *   npx tsx verify-worked-example.ts --slug <slug>
 *   npx tsx verify-worked-example.ts --slug <slug> --verbose
 */

import * as fs from 'fs';
import * as path from 'path';

interface Metadata {
  title?: string;
  slug?: string;
  mathConcept?: string;
  gradeLevel?: string | number;
  unitNumber?: number;
  lessonNumber?: number;
  strategyName?: string;
  strategySteps?: string[];
  learningGoals?: string[];
  scenarios?: string[];
}

interface VerificationResult {
  passed: boolean;
  errors: string[];
  warnings: string[];
  info: string[];
  summary: {
    slideCount: number;
    strategyName: string | null;
    metadataValid: boolean;
    progressFileClean: boolean;
  };
}

const PRESENTATIONS_DIR = 'src/app/presentations';
const PROGRESS_FILE = '.worked-example-progress.json';

function parseArgs(): { slug: string; verbose: boolean } {
  const args = { slug: '', verbose: false };

  for (let i = 2; i < process.argv.length; i++) {
    const arg = process.argv[i];
    if (arg === '--slug' && i + 1 < process.argv.length) {
      args.slug = process.argv[++i];
    } else if (arg === '--verbose') {
      args.verbose = true;
    }
  }

  if (!args.slug) {
    console.error('Error: --slug is required');
    console.log('Usage: npx tsx verify-worked-example.ts --slug <slug>');
    process.exit(1);
  }

  return args;
}

function findSlideFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];

  return fs.readdirSync(dir)
    .filter(f => /^slide-\d+\.html$/.test(f))
    .sort((a, b) => {
      const numA = parseInt(a.match(/slide-(\d+)\.html/)?.[1] || '0');
      const numB = parseInt(b.match(/slide-(\d+)\.html/)?.[1] || '0');
      return numA - numB;
    });
}

function readMetadata(dir: string): Metadata | null {
  const metadataPath = path.join(dir, 'metadata.json');
  if (!fs.existsSync(metadataPath)) return null;

  try {
    return JSON.parse(fs.readFileSync(metadataPath, 'utf-8'));
  } catch {
    return null;
  }
}

function validateMetadata(metadata: Metadata): { valid: boolean; missing: string[] } {
  const required: (keyof Metadata)[] = [
    'title', 'slug', 'strategyName', 'strategySteps',
    'unitNumber', 'lessonNumber'
  ];

  const missing = required.filter(field => {
    const value = metadata[field];
    if (value === undefined || value === null) return true;
    if (Array.isArray(value) && value.length === 0) return true;
    return false;
  });

  return { valid: missing.length === 0, missing };
}

function verify(slug: string): VerificationResult {
  const result: VerificationResult = {
    passed: true,
    errors: [],
    warnings: [],
    info: [],
    summary: {
      slideCount: 0,
      strategyName: null,
      metadataValid: false,
      progressFileClean: true
    }
  };

  const presentationDir = path.join(PRESENTATIONS_DIR, slug);

  // Check directory exists
  if (!fs.existsSync(presentationDir)) {
    result.passed = false;
    result.errors.push(`Presentation directory not found: ${presentationDir}`);
    return result;
  }

  // Check slide files
  const slideFiles = findSlideFiles(presentationDir);
  result.summary.slideCount = slideFiles.length;

  if (slideFiles.length === 0) {
    result.passed = false;
    result.errors.push('No slide files found');
  } else if (slideFiles.length < 7) {
    result.passed = false;
    result.errors.push(`Too few slides: found ${slideFiles.length}, need at least 7`);
  } else if (slideFiles.length > 10) {
    result.warnings.push(`Many slides: ${slideFiles.length} (typical is 9)`);
  } else {
    result.info.push(`Slide count: ${slideFiles.length}`);
  }

  // Check sequential numbering
  for (let i = 0; i < slideFiles.length; i++) {
    const expected = `slide-${i + 1}.html`;
    if (slideFiles[i] !== expected) {
      result.warnings.push(`Gap in slide numbering at position ${i + 1}`);
      break;
    }
  }

  // Check metadata
  const metadata = readMetadata(presentationDir);
  if (!metadata) {
    result.passed = false;
    result.errors.push('metadata.json not found or invalid JSON');
  } else {
    const validation = validateMetadata(metadata);
    result.summary.metadataValid = validation.valid;
    result.summary.strategyName = metadata.strategyName || null;

    if (!validation.valid) {
      result.passed = false;
      result.errors.push(`Missing metadata fields: ${validation.missing.join(', ')}`);
    } else {
      result.info.push(`Strategy: ${metadata.strategyName}`);
      result.info.push(`Steps: ${metadata.strategySteps?.join(' → ')}`);
    }

    if (metadata.scenarios && metadata.scenarios.length !== 3) {
      result.warnings.push(`Expected 3 scenarios, found ${metadata.scenarios.length}`);
    }
  }

  // Check progress file is cleaned up
  const progressPath = path.join(presentationDir, PROGRESS_FILE);
  if (fs.existsSync(progressPath)) {
    result.summary.progressFileClean = false;
    result.warnings.push('Progress file still exists (should be deleted after completion)');
  }

  return result;
}

function printResult(result: VerificationResult, verbose: boolean): void {
  console.log('');
  console.log('═'.repeat(50));
  console.log('  WORKED EXAMPLE VERIFICATION');
  console.log('═'.repeat(50));
  console.log('');

  // Status
  console.log(`Status: ${result.passed ? '✅ PASSED' : '❌ FAILED'}`);
  console.log('');

  // Summary
  console.log('Summary:');
  console.log(`  Slides: ${result.summary.slideCount}`);
  console.log(`  Strategy: ${result.summary.strategyName || '(not found)'}`);
  console.log(`  Metadata: ${result.summary.metadataValid ? 'Valid' : 'Invalid'}`);
  console.log(`  Cleanup: ${result.summary.progressFileClean ? 'Done' : 'Pending'}`);

  // Errors
  if (result.errors.length > 0) {
    console.log('');
    console.log('Errors:');
    result.errors.forEach(e => console.log(`  ❌ ${e}`));
  }

  // Warnings
  if (result.warnings.length > 0) {
    console.log('');
    console.log('Warnings:');
    result.warnings.forEach(w => console.log(`  ⚠️  ${w}`));
  }

  // Info (verbose only)
  if (verbose && result.info.length > 0) {
    console.log('');
    console.log('Info:');
    result.info.forEach(i => console.log(`  ℹ️  ${i}`));
  }

  console.log('');
  console.log('═'.repeat(50));
  console.log('');

  // Remind about manual review
  if (result.passed) {
    console.log('📋 MANUAL REVIEW REQUIRED');
    console.log('');
    console.log('This script only checks file structure.');
    console.log('Before completing, verify:');
    console.log('  □ Strategy name appears consistently across all slides');
    console.log('  □ CFU questions ask "why/how" not computational "what"');
    console.log('  □ Visual stays in same position on slides 2-6');
    console.log('  □ Practice slides have ZERO scaffolding');
    console.log('  □ All math is accurate');
    console.log('');
  }
}

function main(): void {
  const args = parseArgs();
  const result = verify(args.slug);

  printResult(result, args.verbose);

  process.exit(result.passed ? 0 : 1);
}

main();
