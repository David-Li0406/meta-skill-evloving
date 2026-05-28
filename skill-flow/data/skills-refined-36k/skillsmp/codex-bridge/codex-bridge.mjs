#!/usr/bin/env node
/**
 * codex-bridge.mjs - Node.js bridge to call Codex CLI programmatically
 *
 * Usage as CLI:
 *   node codex-bridge.mjs "Your prompt here" [--full-auto] [--json] [--model MODEL]
 *
 * Usage as module:
 *   import { callCodex } from './codex-bridge.mjs';
 *   const response = await callCodex("Your prompt");
 */

import { spawn, execFile } from 'child_process';
import { tmpdir } from 'os';
import { join } from 'path';
import { writeFileSync, readFileSync, unlinkSync, existsSync } from 'fs';
import { randomUUID } from 'crypto';

const isWindows = process.platform === 'win32';

// CLI argument length limit (Windows: 8191, use 7000 for safety margin)
const CLI_ARG_LIMIT = 7000;

/**
 * Call Codex CLI with a prompt and return the response
 * @param {string} prompt - The prompt to send to Codex
 * @param {Object} options - Configuration options
 * @param {string} [options.model] - Model to use
 * @param {boolean} [options.fullAuto=false] - Enable full automation mode
 * @param {boolean} [options.json=false] - Return raw JSON output
 * @param {string} [options.workingDir] - Working directory
 * @param {number} [options.timeout=1200000] - Timeout in milliseconds (20 minutes)
 * @returns {Promise<{success: boolean, response: string, raw?: object[]}>}
 */
export async function callCodex(prompt, options = {}) {
    const {
        model,
        fullAuto = false,
        json = false,
        workingDir,
        timeout = 1200000
    } = options;

    // Build command arguments
    const args = ['exec', '--skip-git-repo-check'];

    if (fullAuto) {
        args.push('--full-auto');
    }

    if (model) {
        args.push('--model', model);
    }

    if (workingDir) {
        args.push('--cd', workingDir);
    }

    // Always use JSON for parsing
    args.push('--json');

    // Create temp file for response
    const tempFile = join(tmpdir(), `codex-response-${randomUUID()}.txt`);
    args.push('--output-last-message', tempFile);

    // Use file-based input only for long prompts (exceeds CLI limit)
    let promptFile = null;
    if (prompt.length > CLI_ARG_LIMIT) {
        promptFile = join(workingDir || process.cwd(), '.codex-bridge-prompt.txt');
        writeFileSync(promptFile, prompt, 'utf8');
        args.push('Read the instructions in .codex-bridge-prompt.txt and respond accordingly. The file contains the full prompt/task.');
    } else {
        args.push(prompt);
    }

    return new Promise((resolve, reject) => {
        const chunks = [];
        const errorChunks = [];

        // Use spawn with shell on Windows, execFile on Unix for proper argument handling
        let proc;
        if (isWindows) {
            // On Windows, use cmd /c with properly escaped arguments
            const escapedArgs = args.map(arg => {
                if (arg.includes(' ') || arg.includes('"')) {
                    return `"${arg.replace(/"/g, '\\"')}"`;
                }
                return arg;
            });
            proc = spawn('cmd', ['/c', 'codex', ...escapedArgs], {
                cwd: workingDir || process.cwd(),
                env: process.env,
                windowsHide: true
            });
        } else {
            proc = spawn('codex', args, {
                cwd: workingDir || process.cwd(),
                env: process.env
            });
        }

        const timeoutId = setTimeout(() => {
            proc.kill('SIGTERM');
            reject(new Error(`Codex CLI timed out after ${timeout}ms`));
        }, timeout);

        proc.stdout.on('data', (data) => {
            chunks.push(data);
        });

        proc.stderr.on('data', (data) => {
            errorChunks.push(data);
        });

        proc.on('close', (code) => {
            clearTimeout(timeoutId);

            const stdout = Buffer.concat(chunks).toString('utf8');
            const stderr = Buffer.concat(errorChunks).toString('utf8');

            // Cleanup temp files
            const cleanup = () => {
                try {
                    if (existsSync(tempFile)) {
                        unlinkSync(tempFile);
                    }
                    if (promptFile && existsSync(promptFile)) {
                        unlinkSync(promptFile);
                    }
                } catch (e) {
                    // Ignore cleanup errors
                }
            };

            if (code !== 0) {
                cleanup();
                resolve({
                    success: false,
                    response: stderr || `Codex CLI exited with code ${code}`,
                    exitCode: code
                });
                return;
            }

            try {
                // Parse JSON events
                const events = stdout
                    .split('\n')
                    .filter(line => line.trim().startsWith('{'))
                    .map(line => {
                        try {
                            return JSON.parse(line);
                        } catch {
                            return null;
                        }
                    })
                    .filter(Boolean);

                // Get response from temp file or parse from events
                let response = '';

                if (existsSync(tempFile)) {
                    response = readFileSync(tempFile, 'utf8');
                } else {
                    // Extract last assistant message
                    const assistantMessages = events.filter(
                        e => e.type === 'message' && e.role === 'assistant'
                    );
                    if (assistantMessages.length > 0) {
                        response = assistantMessages[assistantMessages.length - 1].content || '';
                    }
                }

                cleanup();

                if (json) {
                    resolve({
                        success: true,
                        response: response,
                        raw: events
                    });
                } else {
                    resolve({
                        success: true,
                        response: response.trim()
                    });
                }
            } catch (parseError) {
                cleanup();
                resolve({
                    success: true,
                    response: stdout,
                    parseError: parseError.message
                });
            }
        });

        proc.on('error', (err) => {
            clearTimeout(timeoutId);
            reject(new Error(`Failed to spawn codex: ${err.message}`));
        });
    });
}

/**
 * Simple function to ask Codex a question and get a string response
 * @param {string} prompt - The question/prompt
 * @returns {Promise<string>} - The response text
 */
export async function askCodex(prompt) {
    const result = await callCodex(prompt);
    if (!result.success) {
        throw new Error(result.response);
    }
    return result.response;
}

// CLI mode
if (process.argv[1].endsWith('codex-bridge.mjs') || process.argv[1].endsWith('codex-bridge')) {
    const args = process.argv.slice(2);

    if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
        console.log(`
codex-bridge.mjs - Node.js bridge for Codex CLI

USAGE:
    node codex-bridge.mjs "Your prompt here" [OPTIONS]

OPTIONS:
    --model MODEL     Override AI model
    --full-auto       Enable full automation mode
    --json            Output raw JSON events
    --working-dir DIR Set working directory
    --timeout MS      Timeout in milliseconds (default: 1200000, 20 min)
    -h, --help        Show this help

EXAMPLES:
    node codex-bridge.mjs "Explain this code"
    node codex-bridge.mjs "Fix errors" --full-auto
    node codex-bridge.mjs "Analyze" --json --model gpt-4o

AS A MODULE:
    import { callCodex, askCodex } from './codex-bridge.mjs';

    // Full options
    const result = await callCodex("Your prompt", { fullAuto: true });

    // Simple usage
    const answer = await askCodex("What is 2+2?");
`);
        process.exit(0);
    }

    // Parse CLI arguments
    let prompt = '';
    const options = {};

    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--model':
                options.model = args[++i];
                break;
            case '--full-auto':
                options.fullAuto = true;
                break;
            case '--json':
                options.json = true;
                break;
            case '--working-dir':
                options.workingDir = args[++i];
                break;
            case '--timeout':
                options.timeout = parseInt(args[++i], 10);
                break;
            default:
                if (!args[i].startsWith('-')) {
                    prompt = args[i];
                }
        }
    }

    if (!prompt) {
        console.error('ERROR: No prompt provided');
        process.exit(2);
    }

    try {
        const result = await callCodex(prompt, options);

        if (options.json) {
            console.log(JSON.stringify(result, null, 2));
        } else {
            console.log(result.response);
        }

        process.exit(result.success ? 0 : 1);
    } catch (error) {
        console.error(`ERROR: ${error.message}`);
        process.exit(1);
    }
}
