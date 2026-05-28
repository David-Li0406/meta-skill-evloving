/**
 * Batch Session State Management
 *
 * Stores answers from initial batch configuration and reuses them
 * across all widgets in the batch session, eliminating repetitive questions.
 */

import * as fs from 'fs';
import * as path from 'path';

export interface BatchSessionAnswers {
  detection_type?: 'generic' | 'monorepo-service' | 'nx-app' | 'turborepo-package' | 'lerna-package';
  route?: 'greenfield' | 'brownfield';
  brownfield_mode?: 'standard' | 'upgrade';
  transmission?: 'manual' | 'cruise-control';
  clarifications_strategy?: 'defer' | 'prompt' | 'skip';
  implementation_scope?: 'none' | 'p0' | 'p0_p1' | 'all';
  spec_output_location?: string;
  target_stack?: string;
  build_location?: string;
  build_location_type?: 'subfolder' | 'separate' | 'replace';
}

export interface BatchSessionState {
  sessionId: string;
  startedAt: string;
  batchRootDirectory: string;
  totalRepos: number;
  batchSize: number;
  answers: BatchSessionAnswers;
  processedRepos: string[];
}

const BATCH_SESSION_FILENAME = '.stackshift-batch-session.json';

/**
 * Find batch session file by checking current directory and walking up
 * Similar to how .git directories are found
 */
function findBatchSessionFile(startDir: string = process.cwd()): string | null {
  let currentDir = path.resolve(startDir);
  const root = path.parse(currentDir).root;

  while (currentDir !== root) {
    const batchSessionPath = path.join(currentDir, BATCH_SESSION_FILENAME);
    if (fs.existsSync(batchSessionPath)) {
      return batchSessionPath;
    }
    currentDir = path.dirname(currentDir);
  }

  return null;
}

/**
 * Get batch session file path for a directory
 */
function getBatchSessionPath(directory: string = process.cwd()): string {
  return path.join(directory, BATCH_SESSION_FILENAME);
}

/**
 * Create a new batch session with initial answers
 */
export function createBatchSession(
  batchRootDirectory: string,
  totalRepos: number,
  batchSize: number,
  answers: BatchSessionAnswers
): BatchSessionState {
  const session: BatchSessionState = {
    sessionId: `batch-${Date.now()}`,
    startedAt: new Date().toISOString(),
    batchRootDirectory: path.resolve(batchRootDirectory),
    totalRepos,
    batchSize,
    answers,
    processedRepos: []
  };

  const sessionPath = getBatchSessionPath(batchRootDirectory);
  fs.writeFileSync(sessionPath, JSON.stringify(session, null, 2));

  return session;
}

/**
 * Get current batch session if it exists
 * Searches current directory and walks up to find batch session
 */
export function getBatchSession(startDir: string = process.cwd()): BatchSessionState | null {
  try {
    const sessionPath = findBatchSessionFile(startDir);
    if (!sessionPath) {
      return null;
    }

    const content = fs.readFileSync(sessionPath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error('Error reading batch session:', error);
    return null;
  }
}

/**
 * Check if we're currently in a batch session
 * Searches current directory and walks up
 */
export function hasBatchSession(startDir: string = process.cwd()): boolean {
  return findBatchSessionFile(startDir) !== null;
}

/**
 * Update batch session with processed repo
 */
export function markRepoProcessed(repoName: string, startDir: string = process.cwd()): void {
  const sessionPath = findBatchSessionFile(startDir);
  if (!sessionPath) {
    return;
  }

  try {
    const content = fs.readFileSync(sessionPath, 'utf-8');
    const session: BatchSessionState = JSON.parse(content);

    if (!session.processedRepos.includes(repoName)) {
      session.processedRepos.push(repoName);
    }

    fs.writeFileSync(sessionPath, JSON.stringify(session, null, 2));
  } catch (error) {
    console.error('Error updating batch session:', error);
  }
}

/**
 * Clear batch session in specific directory
 */
export function clearBatchSession(directory: string = process.cwd()): boolean {
  try {
    const sessionPath = getBatchSessionPath(directory);
    if (fs.existsSync(sessionPath)) {
      fs.unlinkSync(sessionPath);
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error clearing batch session:', error);
    return false;
  }
}

/**
 * Get batch session progress
 */
export function getBatchProgress(startDir: string = process.cwd()): string {
  const session = getBatchSession(startDir);
  if (!session) {
    return 'No active batch session';
  }

  const processed = session.processedRepos.length;
  const total = session.totalRepos;
  const percentage = Math.round((processed / total) * 100);

  return `Batch Progress: ${processed}/${total} repos (${percentage}%)`;
}

/**
 * Format batch session for display
 */
export function formatBatchSession(session: BatchSessionState): string {
  const duration = Date.now() - new Date(session.startedAt).getTime();
  const hours = Math.floor(duration / 3600000);
  const minutes = Math.floor((duration % 3600000) / 60000);

  return `
📦 Active Batch Session

Session ID: ${session.sessionId}
Batch Root: ${session.batchRootDirectory}
Started: ${new Date(session.startedAt).toLocaleString()}
Duration: ${hours}h ${minutes}m
Total Repos: ${session.totalRepos}
Batch Size: ${session.batchSize}
Processed: ${session.processedRepos.length}/${session.totalRepos}

Configuration:
  Route: ${session.answers.route || 'not set'}
  Transmission: ${session.answers.transmission || 'not set'}
  Spec Output: ${session.answers.spec_output_location || 'current directory'}
  Build Location: ${session.answers.build_location || 'greenfield/'}
  Target Stack: ${session.answers.target_stack || 'not set'}

Session File: ${session.batchRootDirectory}/${BATCH_SESSION_FILENAME}
`.trim();
}
