import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path/posix';

// Interface for dependency injection
export interface FileOps {
  existsSync: typeof existsSync;
  readFileSync: typeof readFileSync;
  writeFileSync: typeof writeFileSync;
}

const defaultFileOps: FileOps = {
  existsSync,
  readFileSync,
  writeFileSync,
};

export class ClaudeMdHelpers {
  private fileOps: FileOps;

  constructor(fileOps?: FileOps) {
    this.fileOps = fileOps || defaultFileOps;
  }

  /**
   * Get the path to CLAUDE.md file
   */
  getClaudeMdPath(projectRoot: string): string {
    return join(projectRoot, 'CLAUDE.md');
  }

  /**
   * Get the active task file name from CLAUDE.md (e.g., "TASK_001")
   * Returns null if no active task or file doesn't exist
   */
  getActiveTaskFile(projectRoot: string): string | null {
    const claudeMdPath = this.getClaudeMdPath(projectRoot);
    if (!this.fileOps.existsSync(claudeMdPath)) {
      return null;
    }

    const content = this.fileOps.readFileSync(claudeMdPath, 'utf-8');

    // Check for spec pattern: @.cc-track/specs/NNN-feature-name/spec.md
    const specMatch = content.match(/@\.cc-track\/specs\/(\d+)-[^/]+\/spec\.md/);
    if (specMatch) {
      return `TASK_${specMatch[1]}`;
    }

    return null;
  }

  /**
   * Get the active task ID from CLAUDE.md (e.g., "TASK_001")
   * Returns null if no active task
   */
  getActiveTaskId(projectRoot: string): string | null {
    const taskFile = this.getActiveTaskFile(projectRoot);
    if (!taskFile) {
      return null;
    }

    const match = taskFile.match(/TASK_(\d+)/);
    return match ? `TASK_${match[1]}` : null;
  }
}

// Lazy initialization to avoid module loading timing issues
let defaultClaudeMdHelpers: ClaudeMdHelpers | null = null;

function getDefaultInstance(): ClaudeMdHelpers {
  if (!defaultClaudeMdHelpers) {
    defaultClaudeMdHelpers = new ClaudeMdHelpers();
  }
  return defaultClaudeMdHelpers;
}

// Standalone function for getActiveTaskId
export function getActiveTaskId(projectRoot: string): string | null {
  return getDefaultInstance().getActiveTaskId(projectRoot);
}
