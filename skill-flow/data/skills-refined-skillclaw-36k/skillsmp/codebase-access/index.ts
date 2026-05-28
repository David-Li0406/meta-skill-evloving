
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { readCodebase } from '@/server/tools/codebase';

// --- Tool 1: Read Codebase ---
const readCodebaseDef: ToolDefinition = {
    name: 'codebase.read',
    description: 'Read a file or directory relative to the project root.',
    inputSchema: {
        type: 'object',
        properties: {
            path: { type: 'string', description: 'Relative path (e.g. "src/config.ts")' }
        },
        required: ['path']
    },
    category: 'read',
    requiredPermission: 'admin:all' // Restricted permission
};

const readCodebaseImpl = async (ctx: any, inputs: any) => {
    return await readCodebase({ path: inputs.path });
};

export const readCodebaseTool: SkillTool = {
    definition: readCodebaseDef,
    implementation: readCodebaseImpl
};

const manifest: SkillManifest = {
    tools: [readCodebaseTool]
};

export default manifest;
export const tools = [readCodebaseTool];
