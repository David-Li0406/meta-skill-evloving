
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { searchWeb } from '@/server/tools/web-search';

const webSearchDefinition: ToolDefinition = {
    name: 'web.search',
    description: 'Performs a live web search using Serper (Google).',
    inputSchema: {
        type: 'object',
        properties: {
            query: { type: 'string', description: 'Search query' }
        },
        required: ['query']
    },
    category: 'read',
    requiredPermission: 'read:analytics'
};

const webSearchImplementation = async (ctx: any, inputs: any) => {
    // Implementation uses the existing server tool
    return await searchWeb(inputs.query, 5);
};

export const webSearch: SkillTool = {
    definition: webSearchDefinition,
    implementation: webSearchImplementation
};

const manifest: SkillManifest = {
    tools: [webSearch]
};

export default manifest;
export const tools = [webSearch];
