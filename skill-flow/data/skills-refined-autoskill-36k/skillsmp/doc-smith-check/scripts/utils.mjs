import { readFile, access, stat } from "node:fs/promises";
import { constants } from "node:fs";
import { parse as yamlParse } from "yaml";
import { resolve } from "node:path";
import { parseArgs } from "node:util";

/**
 * Get base paths (based on .aigne/doc-smith directory under execution directory)
 */
export function getPaths() {
  const workspaceBase = resolve(process.cwd(), ".aigne/doc-smith");
  return {
    WORKSPACE_BASE: workspaceBase,
    DOCUMENT_STRUCTURE: resolve(workspaceBase, "planning/document-structure.yaml"),
    DOCS_DIR: resolve(workspaceBase, "docs"),
    CONFIG: resolve(workspaceBase, "config.yaml"),
  };
}

/**
 * Error code constants
 */
export const ERROR_CODES = {
  FILE_NOT_FOUND: "FILE_NOT_FOUND",
  MISSING_STRUCTURE_FILE: "MISSING_STRUCTURE_FILE",
  INVALID_STRUCTURE_FILE: "INVALID_STRUCTURE_FILE",
  MISSING_CONFIG_FILE: "MISSING_CONFIG_FILE",
  MISSING_LOCALE: "MISSING_LOCALE",
  SOURCE_LOCALE_MISMATCH: "SOURCE_LOCALE_MISMATCH",
  MISSING_TRANSLATE_LANGUAGE: "MISSING_TRANSLATE_LANGUAGE",
  INVALID_LINK_FORMAT: "INVALID_LINK_FORMAT",
  UNREPLACED_IMAGE_SLOT: "UNREPLACED_IMAGE_SLOT",
  IMAGE_PATH_LEVEL_ERROR: "IMAGE_PATH_LEVEL_ERROR",
  MISSING_SLOT_IMAGE: "MISSING_SLOT_IMAGE",
  ABSOLUTE_IMAGE_PATH_NOT_ALLOWED: "ABSOLUTE_IMAGE_PATH_NOT_ALLOWED",
};

/**
 * Parse command line arguments
 * @param {string[]} args - Command line argument array
 * @returns {Object} - Parsed argument object
 */
export function parseCliArgs(args = process.argv.slice(2)) {
  const { values } = parseArgs({
    args,
    options: {
      path: {
        type: "string",
        short: "p",
        multiple: true,
      },
      "check-slots": {
        type: "boolean",
        default: false,
      },
    },
    allowPositionals: false,
    strict: false,
  });

  return {
    paths: values.path || [],
    checkSlots: values["check-slots"] || false,
  };
}

/**
 * Recursively collect document paths
 * @param {Array} docs - Document array
 * @param {Object} options - Collection options
 * @returns {Set|Array} - Path set or path object array
 */
export function collectDocumentPaths(docs, options = {}) {
  const { includeBothFormats = false, collectMetadata = false } = options;

  const paths = collectMetadata ? [] : new Set();

  function collect(documents) {
    for (const doc of documents) {
      if (doc.path) {
        const normalized = doc.path.startsWith("/") ? doc.path.slice(1) : doc.path;

        if (collectMetadata) {
          paths.push({
            path: normalized,
            displayPath: `/${normalized}`,
            title: doc.title || "",
            description: doc.description || "",
          });
        } else {
          paths.add(normalized);
          if (includeBothFormats) {
            paths.add(`/${normalized}`);
          }
        }
      }

      if (doc.children && Array.isArray(doc.children)) {
        collect(doc.children);
      }
    }
  }

  collect(docs);
  return paths;
}

/**
 * Load all paths from document structure
 * @param {Object} options - Load options
 * @returns {Promise<Set|Array>} - Set of all valid paths
 */
export async function loadDocumentPaths(options = {}) {
  const PATHS = getPaths();
  const {
    yamlPath = PATHS.DOCUMENT_STRUCTURE,
    includeBothFormats = false,
    collectMetadata = false,
  } = options;

  try {
    await access(yamlPath, constants.F_OK | constants.R_OK);
  } catch (_error) {
    throw new Error(ERROR_CODES.MISSING_STRUCTURE_FILE);
  }

  const content = await readFile(yamlPath, "utf8");
  const data = yamlParse(content);

  if (!data.documents || !Array.isArray(data.documents)) {
    throw new Error(ERROR_CODES.INVALID_STRUCTURE_FILE);
  }

  return collectDocumentPaths(data.documents, {
    includeBothFormats,
    collectMetadata,
  });
}

/**
 * Load configuration file
 * @returns {Promise<Object|null>} - Config object or null
 */
export async function loadConfigFromFile() {
  const PATHS = getPaths();
  try {
    await access(PATHS.CONFIG, constants.F_OK);
    const configContent = await readFile(PATHS.CONFIG, "utf8");
    return yamlParse(configContent);
  } catch (_error) {
    return null;
  }
}

/**
 * Check if path is /sources/... absolute path
 * @param {string} imagePath - Image path
 * @returns {boolean}
 */
export function isSourcesAbsolutePath(imagePath) {
  return imagePath.startsWith("/sources/");
}

/**
 * Parse /sources/... absolute path
 * @param {string} absolutePath - Absolute path
 * @returns {string | null} - Relative path
 */
export function parseSourcesPath(absolutePath) {
  const match = absolutePath.match(/^\/sources\/(.+)$/);
  if (!match) return null;

  const relativePath = match[1];

  // Security check: reject path traversal
  if (relativePath.includes("..")) {
    return null;
  }

  return relativePath;
}

/**
 * Resolve sources path to physical path
 * @param {string} absolutePath - Virtual absolute path
 * @param {Array} sourcesConfig - Sources configuration
 * @param {string} workspaceBase - Workspace root directory
 * @returns {Promise<{physicalPath: string, sourceName: string} | null>}
 */
export async function resolveSourcesPath(absolutePath, sourcesConfig, workspaceBase) {
  const relativePath = parseSourcesPath(absolutePath);
  if (!relativePath) return null;

  for (const source of sourcesConfig) {
    let physicalPath;

    if (source.type === "local-path") {
      physicalPath = resolve(workspaceBase, source.path, relativePath);
    } else if (source.type === "git-clone") {
      physicalPath = resolve(workspaceBase, "sources", source.name, relativePath);
    } else {
      continue;
    }

    try {
      await stat(physicalPath);
      return { physicalPath, sourceName: source.name };
    } catch (_error) {}
  }

  return null;
}
