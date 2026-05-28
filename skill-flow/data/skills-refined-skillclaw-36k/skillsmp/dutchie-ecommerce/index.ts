
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { dutchieAction } from '@/server/tools/dutchie';

// --- Tool 1: List Menu ---
const listMenuDef: ToolDefinition = {
    name: 'dutchie.list_menu',
    description: 'List products from the connected Dutchie menu.',
    inputSchema: {
        type: 'object',
        properties: {
            limit: { type: 'number', description: 'Max results (default 5)' },
            search: { type: 'string', description: 'Filter by product name' }
        }
    },
    category: 'read',
    requiredPermission: 'read:products'
};

const listMenuImpl = async (ctx: any, inputs: any) => {
    return await dutchieAction({ 
        action: 'list_menu', 
        limit: inputs.limit, 
        search: inputs.search 
    });
};

export const listMenuTool: SkillTool = {
    definition: listMenuDef,
    implementation: listMenuImpl
};

// --- Tool 2: List Orders ---
const listOrdersDef: ToolDefinition = {
    name: 'dutchie.list_orders',
    description: 'List recent retail orders from Dutchie.',
    inputSchema: {
        type: 'object',
        properties: {
            limit: { type: 'number', description: 'Max results (default 5)' }
        }
    },
    category: 'read',
    requiredPermission: 'read:orders'
};

const listOrdersImpl = async (ctx: any, inputs: any) => {
    return await dutchieAction({ 
        action: 'list_orders', 
        limit: inputs.limit 
    });
};

export const listOrdersTool: SkillTool = {
    definition: listOrdersDef,
    implementation: listOrdersImpl
};

const manifest: SkillManifest = {
    tools: [listMenuTool, listOrdersTool]
};

export default manifest;
export const tools = [listMenuTool, listOrdersTool];
