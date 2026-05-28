#!/usr/bin/env node
import meow from "meow";

import { runCli } from "./commands";
import { type CliFlags } from "./types";

const cli = meow(
  `
  Usage
    $ npname <name> [names...]

  Commands
    <default>           Check if package name(s) are available
    --validate, -v      Only validate name(s), no network check
    --check, -c         Full check: validate + availability + details

  Options
    --registry, -r      Custom registry URL
    --timeout, -t       Request timeout in milliseconds (default: 10000)
    --json, -j          Output as JSON for scripting
    --quiet, -q         Minimal output, just exit codes
    --concurrency       Parallel requests for batch checks (default: 4)
    --help              Show this help message
    --version           Show version number

  Exit Codes
    0                   All names available/valid
    1                   Some names unavailable or invalid
    2                   Invalid arguments or errors

  Examples
    $ npname my-package
    $ npname pkg1 pkg2 pkg3
    $ npname @scope/package --registry https://npm.pkg.github.com/
    $ npname "my pkg" --validate
    $ npname foo bar baz --json
`,
  {
    autoHelp: true,
    autoVersion: true,
    flags: {
      check: { default: false, shortFlag: "c", type: "boolean" },
      concurrency: { default: 4, type: "number" },
      json: { default: false, shortFlag: "j", type: "boolean" },
      quiet: { default: false, shortFlag: "q", type: "boolean" },
      registry: { shortFlag: "r", type: "string" },
      timeout: { default: 10_000, shortFlag: "t", type: "number" },
      validate: { default: false, shortFlag: "v", type: "boolean" },
    },
    importMeta: import.meta,
  }
);

const flags: CliFlags = {
  check: cli.flags.check,
  concurrency: cli.flags.concurrency,
  json: cli.flags.json,
  quiet: cli.flags.quiet,
  registry: cli.flags.registry,
  timeout: cli.flags.timeout,
  validate: cli.flags.validate,
};

const main = async (): Promise<void> => {
  try {
    await runCli(cli.input, flags);
  } catch (error) {
    console.error(error);
    process.exit(2);
  }
};

// eslint-disable-next-line jest/require-hook -- CLI entry point, not a test file
main();
