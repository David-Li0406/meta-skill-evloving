import { Command } from 'commander';
import { AtlasIndexer } from '../core/indexer';
import { AtlasPacker } from '../core/packer';
import { AtlasGuardrails } from '../core/guardrails';
import { RalphyIntegration } from '../core/ralphy';
import { AtlasUpdater } from '../core/updater';

import pkg from '../../package.json';

const VERSION = pkg.version;

// EARLY REDIRECTION: If we are in MCP mode, silence stdout immediately
if (process.argv.includes('mcp')) {
  console.log = (...args) => {
    process.stderr.write(args.map(String).join(' ') + '\n');
  };
  // Also redirect stdout.write to stderr if possible, but that's risky for the protocol
  // Better to just ensure commander doesn't use it.
}

/* eslint-disable no-useless-escape */
export const BANNER = `
\x1b[36m
      ___           ___           ___           ___           ___     
     /\\  \\         /\\  \\         /\\__\\         /::\\  \\       /::\\  \   
    /::\\  \\        \\:\\  \\       /:/  /        /:/\\:\\  \\     /:/\\ \\  \  
   /:/\\:\\  \\        \\:\\  \\     /:/  /        /::\\~\\:\\  \\   _\\:\~\\ \\  \ 
  /::\\~\\:\\  \\       /::\\  \\   /:/  /        /:/\\:\\ \\:\\__\ /\\ \\:\\ \\ \__\ 
 /:/\\:\\ \\:\\__\     /:/\\:\\__\ /:/__/        /:/\\:\\ \\:\\__\ /\\ \\:\\ \\ \__\ 
 \/__\\:\/:/  /    /:/  \/__/ \:\  \        \/__\\:\/:/  / \\:\\ \\:\\ \/__/
      \\::/  /    /:/  /       \\:\  \            \\::/  /   \\:\\ \\:\\__\  
      /:/  /    /:/  /         \\:\  \           /:/  /     \\:\/:/  /  
     /:/  /    /:/  /           \\:\__\         /:/  /       \\::/  /   
     \/__/     \/__/             \/__/         \/__/         \/__/    
\x1b[0m
   \x1b[1mATLAS GUARDRAILS\x1b[0m - \x1b[2mStop the Entropy\x1b[0m
`;

const isMcp = process.argv.includes('mcp');
const program = new Command();

program
  .name('atlas')
  .description('Atlas Guardrails CLI')
  .version(VERSION)
  .configureOutput({
    writeOut: (str) => (isMcp ? process.stderr.write(str) : process.stdout.write(str)),
    writeErr: (str) => process.stderr.write(str),
    outputError: (str, write) => write('\x1b[31m' + str + '\x1b[0m'),
  });

async function cliSetup() {
  // Only print banner and check updates for human CLI usage
  process.stderr.write(BANNER + '\n');
  await AtlasUpdater.checkForUpdates(VERSION, true).catch(() => {});
}

program
  .command('update')
  .description('Check for and install updates')
  .action(async () => {
    await AtlasUpdater.checkForUpdates(VERSION, false);
  });

program
  .command('index')
  .description('Index the repository')
  .action(async () => {
    await cliSetup();
    const indexer = new AtlasIndexer(process.cwd());
    await indexer.index();
  });

program
  .command('pack')
  .description('Create a context pack for a task')
  .requiredOption('-t, --task <string>', 'Task description')
  .option('-b, --budget <number>', 'Token budget', '50000')
  .action(async (options) => {
    await cliSetup();
    const packer = new AtlasPacker(process.cwd());
    const pack = packer.pack({
      task: options.task,
      budget: parseInt(options.budget),
      mode: 'feature',
    });
    // Ensure this goes to stderr if it's logging, but here it's CLI output
    process.stderr.write(`Packed ${pack.files.length} files into pack.json\n`);
  });

program
  .command('find-duplicates')
  .description('Find potential duplicates')
  .option('-i, --intent <string>', 'Intent description')
  .action(async (options) => {
    await cliSetup();
    const guard = new AtlasGuardrails(process.cwd());
    const results = guard.findDuplicates(options.intent || '');
    console.log(JSON.stringify(results, null, 2));
  });

program
  .command('check')
  .description('Run drift and policy checks')
  .action(async () => {
    await cliSetup();
    const guard = new AtlasGuardrails(process.cwd());
    const result = await guard.checkDrift();
    if (result.status === 'fail') {
      process.stderr.write(`Check failed: ${result.reason}\n`);
      process.exit(1);
    } else {
      process.stderr.write('Checks passed.\n');
    }
  });

program
  .command('ralphy-init')
  .description('Initialize Ralphy configuration')
  .action(async () => {
    await cliSetup();
    RalphyIntegration.init(process.cwd());
  });

program
  .command('mcp')
  .description('Start the MCP server (stdio)')
  .action(async () => {
    // IMPORTANT: Absolutely no output to stdout here.
    // Console.log is already redirected in server.ts
    await import('../mcp/server');
  });

export { program };
