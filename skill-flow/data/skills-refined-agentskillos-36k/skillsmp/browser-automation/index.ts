
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { browserAction, BrowserStep } from '@/server/tools/browser';

// --- Tool 1: Perform Browser Steps ---
const browserPerformDef: ToolDefinition = {
    name: 'browser.perform',
    description: 'Execute a sequence of browser actions (e.g. goto, click, discover).',
    inputSchema: {
        type: 'object',
        properties: {
            steps: { 
                type: 'array',
                items: {
                    type: 'object',
                    properties: {
                        action: { type: 'string', enum: ['goto', 'type', 'click', 'wait', 'discover', 'screenshot', 'evaluate'] },
                        url: { type: 'string' },
                        selector: { type: 'string' },
                        text: { type: 'string' },
                        timeout: { type: 'number' },
                        script: { type: 'string' }
                    },
                    required: ['action']
                }
            }
        },
        required: ['steps']
    },
    category: 'read',
    requiredPermission: 'read:analytics' // Assuming browser usage falls under research/analytics access
};

const browserPerformImpl = async (ctx: any, inputs: any) => {
    return await browserAction({ steps: inputs.steps });
};

export const browserPerformTool: SkillTool = {
    definition: browserPerformDef,
    implementation: browserPerformImpl
};

// --- Tool 2: Simple Navigate (Convenience) ---
const browserNavigateDef: ToolDefinition = {
    name: 'browser.navigate',
    description: 'Go to a URL and discover the text content.',
    inputSchema: {
        type: 'object',
        properties: {
            url: { type: 'string', description: 'URL to visit' }
        },
        required: ['url']
    },
    category: 'read',
    requiredPermission: 'read:analytics'
};

const browserNavigateImpl = async (ctx: any, inputs: any) => {
    return await browserAction({
        steps: [
            { action: 'goto', url: inputs.url },
            { action: 'discover' }
        ]
    });
};

export const browserNavigateTool: SkillTool = {
    definition: browserNavigateDef,
    implementation: browserNavigateImpl
};

const manifest: SkillManifest = {
    tools: [browserPerformTool, browserNavigateTool]
};

export default manifest;
export const tools = [browserPerformTool, browserNavigateTool];
