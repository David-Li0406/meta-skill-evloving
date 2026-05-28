import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";

import { type AuthInfo } from "./types";

export const DEFAULT_REGISTRY = "https://registry.npmjs.org/";

// Regex patterns as module-level constants
const ENV_VAR_BRACES_PATTERN = /\$\{([^}]+)\}/g;
const ENV_VAR_DOLLAR_PATTERN = /\$([A-Za-z_][A-Za-z0-9_]*)/g;
const TRAILING_SLASH_PATTERN = /\/$/;

/**
 * Normalize a URL to always have a trailing slash
 */
export const normalizeUrl = (url: string): string =>
  url.endsWith("/") ? url : `${url}/`;

/**
 * Expand environment variables in a string
 * Supports both \${VAR} and $VAR patterns
 */
export const expandEnvVars = (value: string): string => {
  // Handle ${VAR} pattern
  let result = value.replaceAll(
    ENV_VAR_BRACES_PATTERN,
    (_, envVar) => process.env[envVar] ?? ""
  );

  // Handle $VAR pattern (not followed by { and not part of ${})
  result = result.replaceAll(
    ENV_VAR_DOLLAR_PATTERN,
    (_, envVar) => process.env[envVar] ?? ""
  );

  return result;
};

/**
 * Check if a line is a comment or empty
 */
const isCommentOrEmpty = (line: string): boolean =>
  !line || line.startsWith("#") || line.startsWith(";");

/**
 * Check if a line has a valid key=value format
 */
const isValidKeyValueLine = (line: string): boolean => line.includes("=");

/**
 * Extract key from a key=value line
 */
const extractKey = (line: string): string => {
  const eqIndex = line.indexOf("=");
  return line.slice(0, eqIndex).trim();
};

/**
 * Extract value from a key=value line
 */
const extractValue = (line: string): string => {
  const eqIndex = line.indexOf("=");
  return line.slice(eqIndex + 1).trim();
};

/**
 * Parse a single line from .npmrc content
 */
const parseLine = (
  line: string,
  result: Record<string, string>
): Record<string, string> => {
  const trimmed = line.trim();

  if (isCommentOrEmpty(trimmed) || !isValidKeyValueLine(trimmed)) {
    return result;
  }

  const key = extractKey(trimmed);
  if (key) {
    result[key] = expandEnvVars(extractValue(trimmed));
  }

  return result;
};

/**
 * Parse .npmrc content into key-value pairs
 * Handles comments (# and ;) and trims whitespace
 */
export const parseNpmrc = (content: string): Record<string, string> => {
  const result: Record<string, string> = {};

  for (const line of content.split(/\r?\n/)) {
    parseLine(line, result);
  }

  return result;
};

/**
 * Find .npmrc file by walking up directory tree
 */
const findNpmrcInTree = (): string | undefined => {
  let currentDir = process.cwd();

  while (currentDir !== dirname(currentDir)) {
    const npmrcPath = join(currentDir, ".npmrc");
    if (existsSync(npmrcPath)) {
      return npmrcPath;
    }
    currentDir = dirname(currentDir);
  }

  return undefined;
};

/**
 * Find .npmrc file by walking up directory tree, then check home directory
 */
const findNpmrc = (): string | undefined => {
  const treeNpmrc = findNpmrcInTree();
  if (treeNpmrc) {
    return treeNpmrc;
  }

  // Check home directory
  const homeNpmrc = join(homedir(), ".npmrc");
  if (existsSync(homeNpmrc)) {
    return homeNpmrc;
  }

  return undefined;
};

/**
 * Read and parse .npmrc file
 */
const readNpmrc = (): Record<string, string> => {
  const npmrcPath = findNpmrc();
  if (!npmrcPath) {
    return {};
  }

  try {
    const content = readFileSync(npmrcPath, "utf8");
    return parseNpmrc(content);
  } catch {
    return {};
  }
};

/**
 * Get the registry URL for a given scope
 *
 * Resolution priority:
 * 1. npm_config_registry env var (lowercase)
 * 2. NPM_CONFIG_REGISTRY env var (uppercase)
 * 3. .npmrc scoped registry
 * 4. .npmrc global registry
 * 5. Default: https://registry.npmjs.org/
 */
export const getRegistryUrl = (scope?: string): string => {
  // Check environment variables first (lowercase takes priority)
  const envRegistry =
    process.env.npm_config_registry ?? process.env.NPM_CONFIG_REGISTRY;

  // If no scope and env var is set, return early for performance
  if (!scope && envRegistry) {
    return normalizeUrl(envRegistry);
  }

  const npmrc = readNpmrc();

  // Check for scoped registry
  if (scope) {
    const scopeKey = `${scope}:registry`;
    if (npmrc[scopeKey]) {
      return normalizeUrl(npmrc[scopeKey]);
    }
  }

  // Return env registry, global npmrc registry, or default
  return normalizeUrl(envRegistry ?? npmrc.registry ?? DEFAULT_REGISTRY);
};

/**
 * Extract the registry key from a URL for .npmrc lookup
 * Converts https://registry.npmjs.org/ to //registry.npmjs.org
 */
const getRegistryKey = (registryUrl: string): string => {
  try {
    const url = new URL(registryUrl);
    return `//${url.host}${url.pathname.replace(TRAILING_SLASH_PATTERN, "")}`;
  } catch {
    return "";
  }
};

/**
 * Get Bearer auth token from npmrc
 */
const getBearerAuth = (
  npmrc: Record<string, string>,
  regKey: string
): AuthInfo | undefined => {
  const bearerToken =
    npmrc[`${regKey}/:_authToken`] ?? npmrc[`${regKey}:_authToken`];

  if (bearerToken) {
    return {
      token: bearerToken,
      type: "Bearer",
    };
  }

  return undefined;
};

/**
 * Get Basic auth token from npmrc (username + password)
 */
const getBasicAuth = (
  npmrc: Record<string, string>,
  regKey: string
): AuthInfo | undefined => {
  const username = npmrc[`${regKey}/:username`] ?? npmrc[`${regKey}:username`];
  const encodedPassword =
    npmrc[`${regKey}/:_password`] ?? npmrc[`${regKey}:_password`];

  if (username && encodedPassword) {
    const password = (() => {
      try {
        return Buffer.from(encodedPassword, "base64").toString("utf8");
      } catch {
        return "";
      }
    })();
    const token = Buffer.from(`${username}:${password}`, "utf8").toString(
      "base64"
    );

    return {
      token,
      type: "Basic",
    };
  }

  return undefined;
};

/**
 * Get legacy auth token from npmrc
 */
const getLegacyAuth = (npmrc: Record<string, string>): AuthInfo | undefined => {
  const legacyAuth = npmrc._auth;

  if (legacyAuth) {
    return {
      token: legacyAuth,
      type: "Basic",
    };
  }

  return undefined;
};

/**
 * Get auth token for a registry URL
 *
 * Auth token formats:
 * 1. Bearer: //registry.url/:_authToken=token
 * 2. Basic: //registry.url/:username + :_password (base64 encoded)
 * 3. Legacy: _auth=base64token (global)
 */
export const getAuthToken = (registryUrl: string): AuthInfo | undefined => {
  const npmrc = readNpmrc();
  const regKey = getRegistryKey(registryUrl);

  return (
    getBearerAuth(npmrc, regKey) ??
    getBasicAuth(npmrc, regKey) ??
    getLegacyAuth(npmrc)
  );
};
