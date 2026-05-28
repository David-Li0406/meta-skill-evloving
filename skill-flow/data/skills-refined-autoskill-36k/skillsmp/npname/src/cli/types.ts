export interface CliFlags {
  validate: boolean;
  check: boolean;
  registry?: string;
  timeout: number;
  json: boolean;
  quiet: boolean;
  concurrency: number;
}

export interface CliResult {
  name: string;
  available: boolean | null;
  valid: boolean;
  validForNewPackages: boolean;
  errors: string[];
  warnings: string[];
  suggestions?: string[];
  error?: string;
}
