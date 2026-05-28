import { COLORS, SYMBOLS } from "./constants";
import { type CliResult } from "./types";

const formatErrors = (errors: string[]): string =>
  errors.length === 0
    ? ""
    : errors.map((error) => `  ${SYMBOLS.invalid} ${error}`).join("\n");

const formatWarnings = (warnings: string[]): string =>
  warnings.length === 0
    ? ""
    : warnings.map((warning) => `  ${SYMBOLS.warning} ${warning}`).join("\n");

const formatSuggestions = (suggestions?: string[]): string => {
  if (!suggestions || suggestions.length === 0) {
    return "";
  }
  const header = COLORS.dim("  Suggestions:");
  const items = suggestions
    .map((suggestion) => `    ${SYMBOLS.info} ${COLORS.suggestion(suggestion)}`)
    .join("\n");
  return `${header}\n${items}`;
};

const formatErrorLine = (result: CliResult): string =>
  `${SYMBOLS.invalid} ${COLORS.name(result.name)} ${COLORS.error(result.error ?? "")}`;

const appendDetails = (lines: string[], result: CliResult): void => {
  const errors = formatErrors(result.errors);
  const warnings = formatWarnings(result.warnings);
  const suggestions = formatSuggestions(result.suggestions);

  if (errors) {
    lines.push(errors);
  }
  if (warnings) {
    lines.push(warnings);
  }
  if (suggestions) {
    lines.push(suggestions);
  }
};

const getAvailabilitySymbolAndStatus = (
  available: boolean | null
): { symbol: string; status: string } => {
  if (available === null) {
    return { status: COLORS.dim("unknown"), symbol: SYMBOLS.warning };
  }
  return {
    status: available
      ? COLORS.success("available")
      : COLORS.error("unavailable"),
    symbol: available ? SYMBOLS.available : SYMBOLS.unavailable,
  };
};

const getValidationSymbolAndStatus = (
  result: CliResult
): { symbol: string; status: string } => {
  if (result.validForNewPackages) {
    return {
      status: COLORS.success("valid for new packages"),
      symbol: SYMBOLS.available,
    };
  }
  if (result.valid) {
    return {
      status: COLORS.warning("valid for old packages only"),
      symbol: SYMBOLS.warning,
    };
  }
  return {
    status: COLORS.error("invalid"),
    symbol: SYMBOLS.invalid,
  };
};

export const formatResult = (result: CliResult): string => {
  if (result.error) {
    return formatErrorLine(result);
  }

  const lines: string[] = [];
  const { symbol, status } = getAvailabilitySymbolAndStatus(result.available);

  lines.push(`${symbol} ${COLORS.name(result.name)} ${status}`);
  appendDetails(lines, result);

  return lines.join("\n");
};

export const formatValidation = (result: CliResult): string => {
  if (result.error) {
    return formatErrorLine(result);
  }

  const lines: string[] = [];
  const { symbol, status } = getValidationSymbolAndStatus(result);

  lines.push(`${symbol} ${COLORS.name(result.name)} ${status}`);
  appendDetails(lines, result);

  return lines.join("\n");
};

export const formatJson = (results: CliResult[]): string => {
  const output = results.length === 1 ? results[0] : results;
  return JSON.stringify(output, null, 2);
};

export const formatQuiet = (results: CliResult[]): string =>
  results
    .filter((result) => result.available === true)
    .map((result) => result.name)
    .join("\n");

const formatCheckSummary = (results: CliResult[]): string => {
  const available = results.filter((r) => r.available === true).length;
  const taken = results.filter((r) => r.available === false).length;
  const errored = results.filter((r) => r.error).length;

  const parts: string[] = [
    COLORS.success(`${available} available`),
    COLORS.error(`${taken} taken`),
  ];

  if (errored > 0) {
    parts.push(COLORS.dim(`${errored} errored`));
  }

  return `\n${COLORS.bold("Summary:")} ${parts.join(", ")}`;
};

const formatValidateSummary = (results: CliResult[]): string => {
  const validForNew = results.filter((r) => r.validForNewPackages).length;
  const validOldOnly = results.filter(
    (r) => r.valid && !r.validForNewPackages
  ).length;
  const invalid = results.filter((r) => !r.valid).length;

  const parts: string[] = [COLORS.success(`${validForNew} valid`)];

  if (validOldOnly > 0) {
    parts.push(COLORS.warning(`${validOldOnly} legacy only`));
  }

  parts.push(COLORS.error(`${invalid} invalid`));

  return `\n${COLORS.bold("Summary:")} ${parts.join(", ")}`;
};

export const formatSummary = (
  results: CliResult[],
  mode: "check" | "validate"
): string =>
  mode === "check"
    ? formatCheckSummary(results)
    : formatValidateSummary(results);
