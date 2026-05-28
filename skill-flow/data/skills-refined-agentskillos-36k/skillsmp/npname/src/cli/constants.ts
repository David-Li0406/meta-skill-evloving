import chalk from "chalk";

export const SYMBOLS = {
  available: chalk.green("\u2714"),
  info: chalk.blue("\u2139"),
  invalid: chalk.red("\u2716"),
  unavailable: chalk.red("\u2716"),
  warning: chalk.yellow("\u26A0"),
} as const;

export const COLORS = {
  bold: chalk.bold,
  dim: chalk.dim,
  error: chalk.red,
  name: chalk.cyan,
  success: chalk.green,
  suggestion: chalk.blue,
  warning: chalk.yellow,
} as const;

export const EXIT_CODES = {
  ERROR: 2,
  SUCCESS: 0,
  UNAVAILABLE: 1,
} as const;
