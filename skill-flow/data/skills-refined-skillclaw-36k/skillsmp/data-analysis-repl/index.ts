
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import vm from 'vm';

// --- Tool 1: Evaluate JavaScript ---
const evaluateJsDef: ToolDefinition = {
    name: 'analysis.evaluate_js',
    description: 'Execute JavaScript code for data analysis.',
    inputSchema: {
        type: 'object',
        properties: {
            code: { type: 'string', description: 'JavaScript code to execute' },
            context: { type: 'object', description: 'Optional JSON data to inject as variables' }
        },
        required: ['code']
    },
    category: 'read', 
    requiredPermission: 'read:analytics'
};

const evaluateJsImpl = async (ctx: any, inputs: any) => {
    try {
        const sandbox = {
            ...inputs.context,
            console: { log: (...args: any[]) => logs.push(args.join(' ')) },
            result: null
        };
        
        const logs: string[] = [];
        vm.createContext(sandbox);
        
        // Wrap code to capture result if not explicitly returned
        const script = new vm.Script(inputs.code);
        const result = script.runInContext(sandbox);

        return {
            status: 'success',
            result: result,
            logs: logs
        };
    } catch (error: any) {
        return {
            status: 'error',
            error: error.message
        };
    }
};

export const evaluateJsTool: SkillTool = {
    definition: evaluateJsDef,
    implementation: evaluateJsImpl
};

const manifest: SkillManifest = {
    tools: [evaluateJsTool]
};

export default manifest;
export const tools = [evaluateJsTool];
