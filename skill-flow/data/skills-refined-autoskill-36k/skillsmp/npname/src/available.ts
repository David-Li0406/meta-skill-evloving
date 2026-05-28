import { getAuthToken, getRegistryUrl, normalizeUrl } from "./registry";
import {
  type AvailabilityOptions,
  type BatchOptions,
  InvalidNameError,
} from "./types";
import { isOrganization, isScoped, validate } from "./validate";

const NPM_ORGANIZATION_URL = "https://www.npmjs.com/org/";
const DEFAULT_TIMEOUT = 10_000;
const DEFAULT_CONCURRENCY = 4;

const validatePackageName = (name: string, checkName: string): void => {
  const validation = validate(checkName);
  if (!validation.validForNewPackages) {
    const notices = [
      ...(validation.warnings ?? []),
      ...(validation.errors ?? []),
    ].map((v) => `- ${v}`);
    notices.unshift(`Invalid package name: ${name}`);
    throw new InvalidNameError(
      notices.join("\n"),
      validation.errors ?? [],
      validation.warnings ?? []
    );
  }
};

const buildPackageUrl = (
  isOrg: boolean,
  urlName: string,
  registryUrl: string
): string =>
  isOrg
    ? NPM_ORGANIZATION_URL + urlName.toLowerCase()
    : registryUrl + urlName.toLowerCase();

const buildHeaders = (
  registryUrl: string,
  isOrg: boolean
): Record<string, string> => {
  const authInfo = getAuthToken(registryUrl);
  const headers: Record<string, string> = {};
  if (authInfo && !isOrg) {
    headers.authorization = `${authInfo.type} ${authInfo.token}`;
  }
  return headers;
};

const handleFetchError = (error: unknown, timeout: number): never => {
  if (error instanceof Error) {
    if (error.name === "TimeoutError") {
      throw new Error(`Request timed out after ${timeout}ms`, { cause: error });
    }
    if (error.name === "AbortError") {
      throw new Error("Request was aborted", { cause: error });
    }
  }
  throw error;
};

const parseResponseStatus = (
  status: number,
  ok: boolean,
  isScopedOrOrg: boolean
): boolean | null => {
  if (ok) {
    return false;
  }
  if (status === 404) {
    return true;
  }
  // 401/403 for scoped packages means we can't determine availability (auth required)
  if (isScopedOrOrg && (status === 401 || status === 403)) {
    return null;
  }
  throw new Error(`Unexpected response status: ${status}`);
};

interface InternalCheckResult {
  name: string;
  available: boolean | null;
  error: Error | null;
}

const checkSinglePackage = async (
  name: string,
  options?: BatchOptions
): Promise<InternalCheckResult> => {
  try {
    const available = await checkAvailability(name, options);
    return { available, error: null, name };
  } catch (error) {
    const errorObj = error instanceof Error ? error : new Error(String(error));
    return { available: null, error: errorObj, name };
  }
};

interface PreparedRequest {
  packageUrl: string;
  headers: Record<string, string>;
  timeout: number;
  isScopedOrOrg: boolean;
}

const prepareRequest = (
  name: string,
  options?: AvailabilityOptions
): PreparedRequest => {
  const registryUrl = normalizeUrl(options?.registryUrl ?? getRegistryUrl());
  const timeout = options?.timeout ?? DEFAULT_TIMEOUT;
  const isOrg = isOrganization(name);
  const checkName = isOrg ? name.replaceAll(/[@/]/g, "") : name;

  validatePackageName(name, checkName);

  const isScopedPackage = isScoped(name);
  const isScopedOrOrg = isScopedPackage || isOrg;
  const urlName = isScopedPackage ? name.replaceAll("/", "%2f") : checkName;
  const headers = buildHeaders(registryUrl, isOrg);
  const packageUrl = buildPackageUrl(isOrg, urlName, registryUrl);

  return { headers, isScopedOrOrg, packageUrl, timeout };
};

const executeRequest = async (
  prepared: PreparedRequest
): Promise<boolean | null> => {
  try {
    const response = await fetch(prepared.packageUrl, {
      headers: prepared.headers,
      method: "HEAD",
      signal: AbortSignal.timeout(prepared.timeout),
    });
    return parseResponseStatus(
      response.status,
      response.ok,
      prepared.isScopedOrOrg
    );
  } catch (error) {
    return handleFetchError(error, prepared.timeout);
  }
};

/**
 * Check if a package name is available on npm.
 * Returns true if available, false if taken, null if unknown (auth required).
 */
export const checkAvailability = (
  name: string,
  options?: AvailabilityOptions
): Promise<boolean | null> => {
  if (typeof name !== "string" || name.length === 0) {
    return Promise.reject(new Error("Package name required"));
  }
  try {
    const prepared = prepareRequest(name, options);
    return executeRequest(prepared);
  } catch (error) {
    return Promise.reject(error);
  }
};

const createBatches = (names: string[], batchSize: number): string[][] => {
  const batches: string[][] = [];
  for (let i = 0; i < names.length; i += batchSize) {
    batches.push(names.slice(i, i + batchSize));
  }
  return batches;
};

const processBatchResults = (
  batchResults: InternalCheckResult[],
  results: Map<string, boolean | null>,
  errors: Error[]
): void => {
  for (const result of batchResults) {
    if (result.error) {
      errors.push(result.error);
    } else {
      results.set(result.name, result.available);
    }
  }
};

const processBatches = async (
  batches: string[][],
  options: BatchOptions | undefined,
  results: Map<string, boolean | null>,
  errors: Error[]
): Promise<void> => {
  for (const batch of batches) {
    const batchPromises = batch.map((name) =>
      checkSinglePackage(name, options)
    );
    const batchResults = await Promise.all(batchPromises);
    processBatchResults(batchResults, results, errors);
  }
};

/**
 * Check availability of multiple package names.
 * Returns true if available, false if taken, null if unknown (auth required).
 */
export const checkAvailabilityMany = async (
  names: string[],
  options?: BatchOptions
): Promise<Map<string, boolean | null>> => {
  if (!Array.isArray(names)) {
    throw new TypeError(`Expected an array of names, got ${typeof names}`);
  }

  const concurrency = options?.concurrency ?? DEFAULT_CONCURRENCY;
  const results = new Map<string, boolean | null>();
  const errors: Error[] = [];
  const batches = createBatches(names, concurrency);

  await processBatches(batches, options, results, errors);

  if (errors.length > 0) {
    throw new AggregateError(errors, "Some package checks failed");
  }
  return results;
};
