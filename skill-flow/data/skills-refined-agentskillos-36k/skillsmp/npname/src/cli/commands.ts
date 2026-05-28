import ora from "ora";

import npname, { validate } from "../index";
import { type ValidationResult } from "../types";
import { COLORS, EXIT_CODES } from "./constants";
import {
  formatJson,
  formatQuiet,
  formatResult,
  formatSummary,
  formatValidation,
} from "./output";
import { type CliFlags, type CliResult } from "./types";

/**
 * Convert a validation result to a CLI result.
 */
const toCliResult = (
  name: string,
  validation: ValidationResult | undefined,
  available: boolean | null = null,
  error?: string
): CliResult => ({
  available,
  error,
  errors: validation?.errors ?? [],
  name,
  suggestions: validation?.suggestions,
  valid: validation?.valid ?? false,
  validForNewPackages: validation?.validForNewPackages ?? false,
  warnings: validation?.warnings ?? [],
});

/**
 * Merge results from multiple maps in order, with fallback.
 */
const mergeResultsInOrder = (
  names: string[],
  validationMap: Map<string, ValidationResult>,
  resultMaps: Map<string, CliResult>[]
): CliResult[] =>
  names.map((name) => {
    for (const map of resultMaps) {
      const result = map.get(name);
      if (result) {
        return result;
      }
    }
    return toCliResult(name, validationMap.get(name));
  });

/**
 * Process names for validation only (synchronous).
 */
export const processValidateOnly = (names: string[]): CliResult[] =>
  names.map((name) => toCliResult(name, validate(name)));

/**
 * Check availability for valid names and return results.
 */
const checkValidNamesAvailability = async (
  validNames: string[],
  validationMap: Map<string, ValidationResult>,
  flags: CliFlags,
  onError: () => void
): Promise<CliResult[]> => {
  if (validNames.length === 0) {
    return [];
  }

  try {
    const availabilityMap = await npname.many(validNames, {
      concurrency: flags.concurrency,
      registryUrl: flags.registry,
      timeout: flags.timeout,
    });

    return validNames.map((name) =>
      toCliResult(
        name,
        validationMap.get(name),
        availabilityMap.get(name) ?? null
      )
    );
  } catch (error) {
    onError();
    const errorMessage = error instanceof Error ? error.message : String(error);
    return validNames.map((name) =>
      toCliResult(name, validationMap.get(name), null, errorMessage)
    );
  }
};

/**
 * Process names for availability check (batch mode).
 */
export const processAvailability = async (
  names: string[],
  flags: CliFlags
): Promise<CliResult[]> => {
  const showSpinner = !flags.quiet && !flags.json;
  const spinner = showSpinner
    ? ora({ spinner: "dots", text: "Checking availability..." }).start()
    : null;

  // First validate all names and store in a Map for efficient lookup
  const validationMap = new Map(names.map((name) => [name, validate(name)]));

  // Separate valid and invalid names
  const validNames = names.filter(
    (name) => validationMap.get(name)?.validForNewPackages
  );

  const invalidResults = new Map(
    names
      .filter((name) => !validationMap.get(name)?.validForNewPackages)
      .map((name) => [name, toCliResult(name, validationMap.get(name))])
  );

  // Check availability for valid names only
  const availabilityResults = await checkValidNamesAvailability(
    validNames,
    validationMap,
    flags,
    () => spinner?.fail("Failed to check availability")
  );

  spinner?.stop();

  const availabilityResultsMap = new Map(
    availabilityResults.map((r) => [r.name, r])
  );

  return mergeResultsInOrder(names, validationMap, [
    invalidResults,
    availabilityResultsMap,
  ]);
};

/**
 * Process names with full detailed check.
 */
export const processFullCheck = async (
  names: string[],
  flags: CliFlags
): Promise<CliResult[]> => {
  const showSpinner = !flags.quiet && !flags.json;
  const results: CliResult[] = [];

  for (const name of names) {
    const spinner = showSpinner
      ? ora({
          spinner: "dots",
          text: `Checking ${COLORS.name(name)}...`,
        }).start()
      : null;

    try {
      const checkResult = await npname.check(name, {
        registryUrl: flags.registry,
        timeout: flags.timeout,
      });

      spinner?.stop();

      results.push({
        available: checkResult.available,
        error: checkResult.error?.message,
        errors: checkResult.validation.errors,
        name: checkResult.name,
        suggestions: checkResult.validation.suggestions,
        valid: checkResult.validation.valid,
        validForNewPackages: checkResult.validation.validForNewPackages,
        warnings: checkResult.validation.warnings,
      });
    } catch (error) {
      spinner?.fail(`Failed to check ${name}`);
      results.push(
        toCliResult(
          name,
          validate(name),
          null,
          error instanceof Error ? error.message : String(error)
        )
      );
    }
  }

  return results;
};

/**
 * Output results based on flags.
 */
export const outputResults = (results: CliResult[], flags: CliFlags): void => {
  if (flags.json) {
    console.log(formatJson(results));
    return;
  }

  if (flags.quiet) {
    const output = formatQuiet(results);
    if (output) {
      console.log(output);
    }
    return;
  }

  // Normal output mode
  for (const result of results) {
    if (flags.validate) {
      console.log(formatValidation(result));
    } else {
      console.log(formatResult(result));
    }
  }

  // Show summary for multiple results
  if (results.length > 1) {
    console.log();
    console.log(formatSummary(results, flags.validate ? "validate" : "check"));
  }
};

/**
 * Determine the exit code based on results and mode.
 */
export const determineExitCode = (
  results: CliResult[],
  flags: CliFlags
): number => {
  // Check for any errors first
  const hasErrors = results.some((r) => r.error !== undefined);
  if (hasErrors) {
    return EXIT_CODES.ERROR;
  }

  if (flags.validate) {
    // Validate mode: success if all names are valid for new packages
    const allValid = results.every((r) => r.validForNewPackages);
    return allValid ? EXIT_CODES.SUCCESS : EXIT_CODES.UNAVAILABLE;
  }

  // Check mode: success if all names are available
  const allAvailable = results.every((r) => r.available === true);
  return allAvailable ? EXIT_CODES.SUCCESS : EXIT_CODES.UNAVAILABLE;
};

/**
 * Validate CLI input and flags, exit with error if invalid.
 */
const validateCliInput = (input: string[], flags: CliFlags): void => {
  if (flags.concurrency < 1) {
    console.error(COLORS.error("Error: --concurrency must be at least 1"));
    process.exit(EXIT_CODES.ERROR);
  }

  if (flags.timeout <= 0) {
    console.error(COLORS.error("Error: --timeout must be greater than 0"));
    process.exit(EXIT_CODES.ERROR);
  }

  if (input.length === 0) {
    console.error(COLORS.error("Error: No package names provided"));
    console.error(COLORS.dim("Usage: npname <name> [names...]"));
    process.exit(EXIT_CODES.ERROR);
  }
};

/**
 * Main CLI entry point.
 */
export const runCli = async (
  input: string[],
  flags: CliFlags
): Promise<never> => {
  // Validate input and flags
  validateCliInput(input, flags);

  // Process based on flags
  let results: CliResult[];

  if (flags.validate) {
    results = processValidateOnly(input);
  } else if (flags.check) {
    results = await processFullCheck(input, flags);
  } else {
    results = await processAvailability(input, flags);
  }

  // Output results
  outputResults(results, flags);

  // Exit with appropriate code
  const exitCode = determineExitCode(results, flags);
  process.exit(exitCode);
};
