import getSlug from "speakingurl";

import { BUILTIN_MODULES } from "./constants/builtins";
import { type ParsedName, type ValidationResult } from "./types";

const SCOPED_PACKAGE_PATTERN = /^(?:@([^/]+?)\/)?([^/]+?)$/;
const SPECIAL_CHARS_PATTERN = /[~'!()*]/;
const EXCLUSION_LIST = new Set(["node_modules", "favicon.ico"]);

/**
 * Checks if a string is URL-safe (can be used in URLs without encoding).
 */
export const isUrlSafe = (name: string): boolean =>
  encodeURIComponent(name) === name;

/**
 * Parses an npm package name into its components.
 */
export const parseName = (name: string): ParsedName => {
  const match = name.match(SCOPED_PACKAGE_PATTERN);

  if (!match) {
    return {
      full: name,
      isScoped: false,
      name,
      scope: null,
    };
  }

  const scope = match[1] ?? null;
  const packageName = match[2] ?? name;
  const isScopedPkg = scope !== null;

  return {
    full: name,
    isScoped: isScopedPkg,
    name: packageName,
    scope,
  };
};

/**
 * Generate suggestions for fixing invalid package names.
 */
const generateSuggestions = (
  name: string,
  hasUppercase: boolean,
  hasUrlUnsafe: boolean
): string[] => {
  const suggestions: string[] = [];

  if (hasUppercase) {
    suggestions.push(name.toLowerCase());
  }

  if (hasUrlUnsafe) {
    const slug = getSlug(name, { lang: "en", separator: "-" });
    if (slug && slug !== name && slug.length > 0) {
      suggestions.push(slug);
    }
  }

  return [...new Set(suggestions)];
};

/**
 * Creates the validation result object.
 */
const createResult = (
  warnings: string[],
  errors: string[],
  suggestions?: string[]
): ValidationResult => {
  const result: ValidationResult = {
    errors,
    valid: errors.length === 0 && warnings.length === 0,
    validForNewPackages: errors.length === 0 && warnings.length === 0,
    validForOldPackages: errors.length === 0,
    warnings,
  };

  if (suggestions && suggestions.length > 0) {
    result.suggestions = suggestions;
  }

  return result;
};

/**
 * Type guard to check if the name is a valid string.
 */
const validateType = (name: unknown): name is string =>
  name !== null && name !== undefined && typeof name === "string";

/**
 * Gets the type error message for an invalid name.
 */
const getTypeError = (name: unknown): string => {
  if (name === null) {
    return "name cannot be null";
  }
  if (name === undefined) {
    return "name cannot be undefined";
  }
  return "name must be a string";
};

/**
 * Validates basic format - empty, start chars, whitespace.
 */
const validateBasicFormat = (name: string): string[] => {
  const checks: [boolean, string][] = [
    [name.length === 0, "name length must be greater than zero"],
    [name.startsWith("."), "name cannot start with a period"],
    [name.startsWith("-"), "name cannot start with a hyphen"],
    [name.startsWith("_"), "name cannot start with an underscore"],
    [name.trim() !== name, "name cannot contain leading or trailing spaces"],
  ];

  return checks
    .filter(([condition]) => condition)
    .map(([, message]) => message);
};

/**
 * Validates blocked names.
 */
const validateBlockedNames = (name: string): string[] =>
  EXCLUSION_LIST.has(name.toLowerCase())
    ? [`${name.toLowerCase()} is not a valid package name`]
    : [];

/**
 * Validates and collects warnings.
 */
const collectWarnings = (
  name: string
): { warnings: string[]; hasUppercase: boolean } => {
  const warnings: string[] = [];
  const hasUppercase = name.toLowerCase() !== name;
  const lastPart = name.split("/").at(-1);

  if (BUILTIN_MODULES.has(name.toLowerCase())) {
    warnings.push(`${name} is a core module name`);
  }
  if (name.length > 214) {
    warnings.push("name can no longer contain more than 214 characters");
  }
  if (hasUppercase) {
    warnings.push("name can no longer contain capital letters");
  }
  if (lastPart && SPECIAL_CHARS_PATTERN.test(lastPart)) {
    warnings.push('name can no longer contain special characters ("~\'!()*")');
  }

  return { hasUppercase, warnings };
};

/**
 * Validates URL safety and scoped packages.
 */
const validateUrlSafety = (
  name: string
): { errors: string[]; hasUrlUnsafe: boolean } => {
  if (isUrlSafe(name)) {
    return { errors: [], hasUrlUnsafe: false };
  }

  const errors: string[] = [];
  const nameMatch = name.match(SCOPED_PACKAGE_PATTERN);

  if (nameMatch) {
    const [, user, pkg] = nameMatch;
    if (pkg?.startsWith(".")) {
      errors.push("name cannot start with a period");
    }
    if (user && pkg && isUrlSafe(user) && isUrlSafe(pkg)) {
      return { errors, hasUrlUnsafe: true };
    }
  }

  errors.push("name can only contain URL-friendly characters");
  return { errors, hasUrlUnsafe: true };
};

/**
 * Validates an npm package name according to npm's naming rules.
 */
export const validate = (name: unknown): ValidationResult => {
  if (!validateType(name)) {
    return createResult([], [getTypeError(name)]);
  }

  const basicErrors = validateBasicFormat(name);
  const blockedErrors = validateBlockedNames(name);
  const { warnings, hasUppercase } = collectWarnings(name);
  const { errors: urlErrors, hasUrlUnsafe } = validateUrlSafety(name);

  const allErrors = [...basicErrors, ...blockedErrors, ...urlErrors];
  const suggestions = generateSuggestions(name, hasUppercase, hasUrlUnsafe);

  return createResult(warnings, allErrors, suggestions);
};

export const isScoped = (name: string): boolean =>
  name.startsWith("@") && name.includes("/");

/**
 * Checks if a name is an npm organization (e.g., "@org" without a package name).
 * Returns true for standalone organization names like "@babel", "@types".
 * Returns false for scoped packages like "@babel/core" or unscoped packages.
 */
export const isOrganization = (name: string): boolean =>
  /^@[\d\w][\w.-]*$/i.test(name);
