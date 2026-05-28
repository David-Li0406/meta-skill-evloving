
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { leaflinkAction } from '@/server/tools/leaflink';

// --- Tool 1: List Orders ---
const listOrdersDef: ToolDefinition = {
    name: 'leaflink.list_orders',
    description: 'List incoming wholesale orders.',
    inputSchema: {
        type: 'object',
        properties: {
            status: { type: 'string', description: 'Filter status (e.g. Accepted)' },
            limit: { type: 'number' }
        }
    },
    category: 'read',
    requiredPermission: 'read:orders'
};

const listOrdersImpl = async (ctx: any, inputs: any) => {
    return await leaflinkAction({ 
        action: 'list_orders', 
        status: inputs.status, 
        limit: inputs.limit 
    });
};

export const listOrdersTool: SkillTool = {
    definition: listOrdersDef,
    implementation: listOrdersImpl
};

// --- Tool 2: List Products ---
const listProductsDef: ToolDefinition = {
    name: 'leaflink.list_products',
    description: 'List products in the wholesale catalog.',
    inputSchema: {
        type: 'object',
        properties: {
            limit: { type: 'number' }
        }
    },
    category: 'read',
    requiredPermission: 'read:products'
};

const listProductsImpl = async (ctx: any, inputs: any) => {
    return await leaflinkAction({ 
        action: 'list_products', 
        limit: inputs.limit 
    });
};

export const listProductsTool: SkillTool = {
    definition: listProductsDef,
    implementation: listProductsImpl
};

// --- Tool 3: Update Inventory ---
const updateInventoryDef: ToolDefinition = {
    name: 'leaflink.update_inventory',
    description: 'Update inventory quantity for a specific product.',
    inputSchema: {
        type: 'object',
        properties: {
            productId: { type: 'string', description: 'LeafLink Product ID' },
            quantity: { type: 'number', description: 'New quantity available' }
        },
        required: ['productId', 'quantity']
    },
    category: 'write',
    requiredPermission: 'write:products'
};

const updateInventoryImpl = async (ctx: any, inputs: any) => {
    return await leaflinkAction({ 
        action: 'update_inventory', 
        productId: inputs.productId, 
        quantity: inputs.quantity 
    });
};

export const updateInventoryTool: SkillTool = {
    definition: updateInventoryDef,
    implementation: updateInventoryImpl
};

const manifest: SkillManifest = {
    tools: [listOrdersTool, listProductsTool, updateInventoryTool]
};

export default manifest;
export const tools = [listOrdersTool, listProductsTool, updateInventoryTool];
