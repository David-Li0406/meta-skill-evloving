import { checkAvailability, checkAvailabilityMany } from "./available";
import { getAuthToken, getRegistryUrl } from "./registry";
import {
  InvalidNameError,
  type AuthInfo,
  type AvailabilityOptions,
  type BatchOptions,
  type CheckResult,
  type ParsedName,
  type ValidationResult,
} from "./types";
import { parseName, validate } from "./validate";

/**
 * Check if an npm package name is available on the registry.
 * Returns true if available, false if taken, null if unknown (auth required).
 */
const npname = (
  name: string,
  options?: AvailabilityOptions
): Promise<boolean | null> => checkAvailability(name, options);

/**
 * Check availability of multiple package names in parallel.
 * Returns true if available, false if taken, null if unknown (auth required).
 */
npname.many = (
  names: string[],
  options?: BatchOptions
): Promise<Map<string, boolean | null>> =>
  checkAvailabilityMany(names, options);

/**
 * Validate a package name without checking registry availability.
 */
npname.validate = (name: unknown): ValidationResult => validate(name);

/**
 * Full check: validate and check availability.
 */
npname.check = async (
  name: string,
  options?: AvailabilityOptions
): Promise<CheckResult> => {
  const validation = validate(name);

  if (!validation.validForNewPackages) {
    return {
      available: null,
      error: new InvalidNameError(
        `Invalid package name: ${name}`,
        validation.errors,
        validation.warnings
      ),
      name,
      validation,
    };
  }

  try {
    const available = await checkAvailability(name, options);
    return { available, name, validation };
  } catch (error) {
    return {
      available: null,
      error: error instanceof Error ? error : new Error(String(error)),
      name,
      validation,
    };
  }
};

/**
 * Parse a package name into its components.
 */
npname.parse = (name: string): ParsedName => parseName(name);

/**
 * Get the registry URL for a scope or the default registry.
 */
npname.registry = (scope?: string): string => getRegistryUrl(scope);

/**
 * Get the authentication token for a registry URL.
 */
npname.auth = (registryUrl: string): AuthInfo | undefined =>
  getAuthToken(registryUrl);

export default npname;

// Named exports for direct access
export { isOrganization, isScoped, parseName, validate } from "./validate";
export { checkAvailability, checkAvailabilityMany } from "./available";
export {
  DEFAULT_REGISTRY,
  expandEnvVars,
  getAuthToken,
  getRegistryUrl,
  normalizeUrl,
  parseNpmrc,
} from "./registry";
export type {
  AuthInfo,
  AvailabilityOptions,
  BatchOptions,
  CheckResult,
  ParsedName,
  ValidationResult,
} from "./types";
export { InvalidNameError } from "./types";
