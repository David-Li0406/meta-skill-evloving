
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { CannMenusService, SearchParams } from '@/server/services/cannmenus';

// --- Tool 1: Search Products ---
const searchProductsDef: ToolDefinition = {
    name: 'cannmenus.searchProducts',
    description: 'Searches for cannabis products across dispensary menus.',
    inputSchema: {
        type: 'object',
        properties: {
            query: { type: 'string', description: 'Product name or keyword' },
            category: { type: 'string', description: 'Flower, Edible, Vape, etc.' },
            price_min: { type: 'number' },
            price_max: { type: 'number' },
            near: { type: 'string', description: 'City, State or Zip to search near' },
            limit: { type: 'number', default: 10 }
        }
    },
    category: 'read',
    requiredPermission: 'read:products'
};

const searchProductsImpl = async (ctx: any, inputs: any) => {
    const service = new CannMenusService();
    const params: SearchParams = {
        search: inputs.query,
        category: inputs.category,
        price_min: inputs.price_min,
        price_max: inputs.price_max,
        near: inputs.near,
        limit: inputs.limit || 10
    };
    return await service.searchProducts(params);
};

export const searchProductsTool: SkillTool = {
    definition: searchProductsDef,
    implementation: searchProductsImpl
};

// --- Tool 2: Find Retailers ---
const findRetailersDef: ToolDefinition = {
    name: 'cannmenus.findRetailers',
    description: 'Finds dispensaries/retailers in a specific area.',
    inputSchema: {
        type: 'object',
        properties: {
            lat: { type: 'number', description: 'Latitude' },
            lng: { type: 'number', description: 'Longitude' },
            limit: { type: 'number', default: 5 }
        },
        required: ['lat', 'lng']
    },
    category: 'read',
    requiredPermission: 'read:analytics'
};

const findRetailersImpl = async (ctx: any, inputs: any) => {
    const service = new CannMenusService();
    return await service.findRetailers({
        lat: inputs.lat,
        lng: inputs.lng,
        limit: inputs.limit
    });
};

export const findRetailersTool: SkillTool = {
    definition: findRetailersDef,
    implementation: findRetailersImpl
};

const manifest: SkillManifest = {
    tools: [searchProductsTool, findRetailersTool]
};

export default manifest;
export const tools = [searchProductsTool, findRetailersTool];
