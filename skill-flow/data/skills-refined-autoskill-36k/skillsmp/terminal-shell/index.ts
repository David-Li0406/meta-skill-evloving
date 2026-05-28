import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { exec } from 'child_process';
import * as util from 'util';

const promisify = util.promisify;
const execAsync = promisify(exec);

// --- Tool 1: Execute Command ---
const executeDef: ToolDefinition = {
    name: 'terminal.execute',
    description: 'Execute a shell command on the server.',
    inputSchema: {
        type: 'object',
        properties: {
            command: { type: 'string', description: 'The command to run (e.g. "ls -la")' },
            cwd: { type: 'string', description: 'Optional working directory' }
        },
        required: ['command']
    },
    category: 'side-effect',
    requiredPermission: 'admin:all' // Highly restricted
};

const executeImpl = async (ctx: any, inputs: any) => {
    try {
        const { stdout, stderr } = await execAsync(inputs.command, {
            cwd: inputs.cwd || process.cwd()
        });

        return {
            status: 'success',
            stdout: stdout.trim(),
            stderr: stderr.trim()
        };
    } catch (error: any) {
        return {
            status: 'error',
            error: error.message,
            cmd: error.cmd,
            stdout: error.stdout,
            stderr: error.stderr
        };
    }
};

export const executeTool: SkillTool = {
    definition: executeDef,
    implementation: executeImpl
};

const manifest: SkillManifest = {
    tools: [executeTool]
};

export default manifest;
export const tools = [executeTool];
