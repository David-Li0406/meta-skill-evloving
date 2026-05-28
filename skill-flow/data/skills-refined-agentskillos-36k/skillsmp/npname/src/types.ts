export interface ValidationResult {
  valid: boolean;
  validForNewPackages: boolean;
  validForOldPackages: boolean;
  errors: string[];
  warnings: string[];
  suggestions?: string[];
}

export interface AvailabilityOptions {
  registryUrl?: string;
  timeout?: number;
}

export interface BatchOptions extends AvailabilityOptions {
  concurrency?: number;
}

export interface CheckResult {
  name: string;
  available: boolean | null;
  validation: ValidationResult;
  error?: Error;
}

export interface AuthInfo {
  token: string;
  type: "Bearer" | "Basic";
  username?: string;
  password?: string;
}

export interface ParsedName {
  scope: string | null;
  name: string;
  full: string;
  isScoped: boolean;
}

export class InvalidNameError extends Error {
  name = "InvalidNameError";
  warnings: string[];
  errors: string[];

  constructor(message: string, errors: string[], warnings: string[]) {
    super(message);
    this.errors = errors;
    this.warnings = warnings;
  }
}
