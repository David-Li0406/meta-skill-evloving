/**
 * Utilities for truncating git diffs while preserving file boundaries
 */

export interface TruncationResult {
  diff: string;
  truncated: boolean;
  originalSize: number;
  truncatedSize: number;
  filesOmitted: number;
  linesOmitted: number;
}

/**
 * Truncate a git diff at file boundaries to stay under the size limit
 */
export function truncateGitDiff(diff: string, maxSize: number): TruncationResult {
  const originalSize = diff.length;

  if (originalSize <= maxSize) {
    return {
      diff,
      truncated: false,
      originalSize,
      truncatedSize: originalSize,
      filesOmitted: 0,
      linesOmitted: 0,
    };
  }

  // Split diff into file sections
  const filePattern = /^diff --git a\/.+ b\/.+$/gm;
  const matches = Array.from(diff.matchAll(filePattern));

  if (matches.length === 0) {
    // No file headers found, just truncate at character limit
    const truncatedDiff = diff.substring(0, maxSize - 100); // Leave room for truncation message
    const linesOmitted = (diff.match(/\n/g) || []).length - (truncatedDiff.match(/\n/g) || []).length;

    return {
      diff: `${truncatedDiff}\n\n... [diff truncated due to size limit] ...`,
      truncated: true,
      originalSize,
      truncatedSize: truncatedDiff.length,
      filesOmitted: 0,
      linesOmitted,
    };
  }

  // Find how many complete files we can include
  let includedSize = 0;
  let lastIncludedFile = 0;

  for (let i = 0; i < matches.length; i++) {
    const fileStart = matches[i].index ?? 0;
    const fileEnd = i < matches.length - 1 ? (matches[i + 1].index ?? diff.length) : diff.length;
    const fileContent = diff.substring(fileStart, fileEnd);

    if (includedSize + fileContent.length <= maxSize - 100) {
      // Leave room for truncation message
      includedSize += fileContent.length;
      lastIncludedFile = i + 1;
    } else {
      break;
    }
  }

  const filesOmitted = matches.length - lastIncludedFile;

  if (lastIncludedFile === 0) {
    // Can't even fit the first file, truncate it
    const firstFileEnd = matches.length > 1 ? (matches[1].index ?? diff.length) : diff.length;
    const firstFile = diff.substring(0, firstFileEnd);
    const truncatedFirst = firstFile.substring(0, maxSize - 100);
    const linesOmitted = (firstFile.match(/\n/g) || []).length - (truncatedFirst.match(/\n/g) || []).length;

    return {
      diff: `${truncatedFirst}\n\n... [file truncated due to size limit] ...`,
      truncated: true,
      originalSize,
      truncatedSize: truncatedFirst.length,
      filesOmitted: filesOmitted,
      linesOmitted,
    };
  }

  // Include complete files up to the limit
  const lastFileEnd =
    lastIncludedFile < matches.length ? (matches[lastIncludedFile].index ?? diff.length) : diff.length;
  const truncatedDiff = diff.substring(0, lastFileEnd);

  const remainingLines = diff.substring(lastFileEnd).split('\n').length - 1;

  const truncationMessage = `\n\n... [${filesOmitted} files omitted due to size limit (${remainingLines} lines)] ...`;

  return {
    diff: truncatedDiff + truncationMessage,
    truncated: true,
    originalSize,
    truncatedSize: truncatedDiff.length + truncationMessage.length,
    filesOmitted,
    linesOmitted: remainingLines,
  };
}
