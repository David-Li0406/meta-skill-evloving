// ABOUTME: Helpers for managing spec-driven development workflow - metadata, directory structure, and spec folder operations
// ABOUTME: Provides functions to create/read/update .metadata.json files and manage .cc-track/specs/ directory structure

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path/posix';

export interface SpecMetadata {
  task_id: string;
  feature_name: string;
  branch: string;
  github?: {
    issue: number;
    url: string;
  };
  status: 'draft' | 'in_progress' | 'completed' | 'blocked';
  started: string; // ISO 8601 timestamp
  completed?: string; // ISO 8601 timestamp
}

export interface SpecFileOperations {
  existsSync: typeof existsSync;
  mkdirSync: typeof mkdirSync;
  readFileSync: typeof readFileSync;
  writeFileSync: typeof writeFileSync;
}

// Helper for testing - allows injecting readdirSync
export function _readSpecDirs(specsDir: string): Array<{ name: string; isDirectory: () => boolean }> {
  return readdirSync(specsDir, { withFileTypes: true }) as Array<{ name: string; isDirectory: () => boolean }>;
}

/**
 * Generate the next available task ID (e.g., "001", "002")
 */
export function getNextTaskId(
  projectRoot: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
  readDirs: typeof _readSpecDirs = _readSpecDirs,
): string {
  const specsDir = join(projectRoot, '.cc-track', 'specs');

  if (!fileOps.existsSync(specsDir)) {
    return '001';
  }

  // Find existing spec directories
  const dirs = readDirs(specsDir)
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);

  // Extract task IDs from directory names (format: "001-feature-name")
  const taskIds = dirs
    .map((dir: string) => {
      const match = dir.match(/^(\d{3})-/);
      return match ? parseInt(match[1], 10) : 0;
    })
    .filter((id: number) => id > 0);

  if (taskIds.length === 0) {
    return '001';
  }

  const maxId = Math.max(...taskIds);
  return String(maxId + 1).padStart(3, '0');
}

/**
 * Create a spec directory with the given task ID and feature name
 */
export function createSpecDirectory(
  projectRoot: string,
  taskId: string,
  featureName: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): string {
  const specsDir = join(projectRoot, '.cc-track', 'specs');
  const specDir = join(specsDir, `${taskId}-${featureName}`);

  // Create .cc-track/specs if it doesn't exist
  if (!fileOps.existsSync(specsDir)) {
    fileOps.mkdirSync(specsDir, { recursive: true });
  }

  // Create the specific spec directory
  if (!fileOps.existsSync(specDir)) {
    fileOps.mkdirSync(specDir, { recursive: true });
  }

  return specDir;
}

/**
 * Create a metadata file for a spec
 */
export function createMetadata(
  specDir: string,
  metadata: SpecMetadata,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const metadataPath = join(specDir, '.metadata.json');
  fileOps.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2));
}

/**
 * Read metadata from a spec directory
 */
export function readMetadata(
  specDir: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): SpecMetadata | null {
  const metadataPath = join(specDir, '.metadata.json');

  if (!fileOps.existsSync(metadataPath)) {
    return null;
  }

  try {
    const content = fileOps.readFileSync(metadataPath, 'utf-8');
    return JSON.parse(content) as SpecMetadata;
  } catch (error) {
    console.error(`Failed to read metadata from ${metadataPath}:`, error);
    return null;
  }
}

/**
 * Update metadata in a spec directory
 */
export function updateMetadata(
  specDir: string,
  updates: Partial<SpecMetadata>,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const existing = readMetadata(specDir, fileOps);
  if (!existing) {
    throw new Error(`No metadata found in ${specDir}`);
  }

  const updated = { ...existing, ...updates };
  createMetadata(specDir, updated, fileOps);
}

/**
 * Get the spec directory path for a given task ID
 */
export function getSpecDirectory(
  projectRoot: string,
  taskId: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
  readDirs: typeof _readSpecDirs = _readSpecDirs,
): string | null {
  const specsDir = join(projectRoot, '.cc-track', 'specs');

  if (!fileOps.existsSync(specsDir)) {
    return null;
  }

  // Find directory matching the task ID pattern
  const dirs = readDirs(specsDir)
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);

  const matchingDir = dirs.find((dir: string) => dir.startsWith(`${taskId}-`));
  if (!matchingDir) {
    return null;
  }

  return join(specsDir, matchingDir);
}

/**
 * Get the active spec directory (from CLAUDE.md)
 */
export function getActiveSpecDirectory(
  projectRoot: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): string | null {
  const claudeMdPath = join(projectRoot, 'CLAUDE.md');

  if (!fileOps.existsSync(claudeMdPath)) {
    return null;
  }

  const content = fileOps.readFileSync(claudeMdPath, 'utf-8');

  // Look for active task reference: @.cc-track/specs/001-feature-name/spec.md
  const match = content.match(/@\.cc-track\/specs\/([^/]+)\/spec\.md/);
  if (!match) {
    return null;
  }

  const specDirName = match[1];
  return join(projectRoot, '.cc-track', 'specs', specDirName);
}

/**
 * Get metadata for the currently active spec
 */
export function getActiveMetadata(
  projectRoot: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): SpecMetadata | null {
  const specDir = getActiveSpecDirectory(projectRoot, fileOps);
  if (!specDir) {
    return null;
  }

  return readMetadata(specDir, fileOps);
}

/**
 * Create a spec file from template
 */
export function createSpecFile(
  specDir: string,
  content: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const specPath = join(specDir, 'spec.md');
  fileOps.writeFileSync(specPath, content);
}

/**
 * Create a plan file from template
 */
export function createPlanFile(
  specDir: string,
  content: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const planPath = join(specDir, 'plan.md');
  fileOps.writeFileSync(planPath, content);
}

/**
 * Create a tasks file from template
 */
export function createTasksFile(
  specDir: string,
  content: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const tasksPath = join(specDir, 'tasks.md');
  fileOps.writeFileSync(tasksPath, content);
}

/**
 * Create a progress file from template
 */
export function createProgressFile(
  specDir: string,
  content: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const progressPath = join(specDir, 'progress.md');
  fileOps.writeFileSync(progressPath, content);
}

/**
 * Read a file from the spec directory
 */
export function readSpecFile(
  specDir: string,
  filename: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): string | null {
  const filePath = join(specDir, filename);

  if (!fileOps.existsSync(filePath)) {
    return null;
  }

  return fileOps.readFileSync(filePath, 'utf-8');
}

/**
 * Write a file to the spec directory
 */
export function writeSpecFile(
  specDir: string,
  filename: string,
  content: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
): void {
  const filePath = join(specDir, filename);
  fileOps.writeFileSync(filePath, content);
}

/**
 * Generate a feature name slug from a title
 * Example: "Add User Authentication" -> "add-user-authentication"
 */
export function generateFeatureName(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 50); // Limit length
}

/**
 * Get all spec directories in the project
 */
export function getAllSpecDirectories(
  projectRoot: string,
  fileOps: SpecFileOperations = { existsSync, mkdirSync, readFileSync, writeFileSync },
  readDirs: typeof _readSpecDirs = _readSpecDirs,
): string[] {
  const specsDir = join(projectRoot, '.cc-track', 'specs');

  if (!fileOps.existsSync(specsDir)) {
    return [];
  }

  return readDirs(specsDir)
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => join(specsDir, dirent.name));
}
