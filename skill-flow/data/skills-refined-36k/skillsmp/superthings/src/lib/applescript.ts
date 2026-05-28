import { exec } from 'child_process';
import { promisify } from 'util';
import { readFile } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { validateAppleScriptArg } from './validation.js';
import { ThingsScriptError, ThingsTimeoutError } from './errors.js';

const execAsync = promisify(exec);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

export interface ExecuteOptions {
  timeout?: number;  // in milliseconds
  maxResults?: number;
  retries?: number;  // number of retry attempts (default: 2)
  retryDelay?: number; // delay between retries in ms (default: 1000)
}

// Helper to sleep between retries
const sleep = (ms: number): Promise<void> => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Execute AppleScript file with arguments (SECURE VERSION)
 * This is the only method we use - no string interpolation
 */
export async function executeAppleScriptFile(
  scriptName: string,
  args: string[] = [],
  options: ExecuteOptions = {}
): Promise<string> {
  const { timeout = 30000, maxResults, retries = 2, retryDelay = 1000 } = options;
  const scriptPath = path.join(__dirname, '..', 'scripts', `${scriptName}.applescript`);

  // Validate script exists
  try {
    await readFile(scriptPath, 'utf-8');
  } catch {
    throw new ThingsScriptError(scriptName, 'Script file not found');
  }

  // Validate and sanitize all arguments
  const safeArgs = args.map((arg, index) =>
    validateAppleScriptArg(arg, `argument[${index}]`)
  );

  // Add maxResults as last argument if specified
  if (maxResults !== undefined) {
    safeArgs.push(String(maxResults));
  }

  // Build command with proper escaping
  // Using single quotes and escaping any single quotes in arguments
  const quotedArgs = safeArgs.map(arg => `'${arg.replace(/'/g, "'\"'\"'")}'`);
  const command = `osascript "${scriptPath}" ${quotedArgs.join(' ')}`;

  // Execute with retry logic
  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const { stdout, stderr } = await execAsync(command, {
        timeout,
        maxBuffer: 1024 * 1024 * 10 // 10MB buffer for large lists
      });

      if (stderr) {
        console.warn(`AppleScript warning (${scriptName}):`, stderr);
      }

      return stdout.trim();
    } catch (error: unknown) {
      const errorObj = error as { code?: string; stderr?: string; message?: string };

      // Don't retry on timeouts - they're likely to timeout again
      if (errorObj.code === 'ETIMEDOUT') {
        throw new ThingsTimeoutError(scriptName, timeout);
      }

      lastError = new ThingsScriptError(
        scriptName,
        errorObj.stderr || errorObj.message || 'Unknown error'
      );

      // If we have retries left, wait and try again
      if (attempt < retries) {
        console.warn(`AppleScript attempt ${attempt + 1} failed for ${scriptName}, retrying in ${retryDelay}ms...`);
        await sleep(retryDelay);
      }
    }
  }

  // All retries exhausted
  throw lastError;
}

/**
 * Test if Things 3 is installed and accessible
 */
export async function testThingsAvailable(): Promise<boolean> {
  try {
    const { stdout } = await execAsync(
      'osascript -e \'tell application "System Events" to name of application processes\'',
      { timeout: 5000 }
    );
    return stdout.includes('Things3');
  } catch {
    return false;
  }
}