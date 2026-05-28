
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { postMessage } from '@/server/integrations/slack/service';
import { requireUser } from '@/server/auth/auth';

// --- Tool 1: Post Message ---
const postMessageDef: ToolDefinition = {
    name: 'slack.post_message',
    description: 'Post a message to a Slack channel.',
    inputSchema: {
        type: 'object',
        properties: {
            channel: { type: 'string', description: 'Channel name (e.g. #general) or ID' },
            text: { type: 'string', description: 'Message content' }
        },
        required: ['channel', 'text']
    },
    category: 'side-effect',
    requiredPermission: 'manage:campaigns'
};

const postMessageImpl = async (ctx: any, inputs: any) => {
    const user = await requireUser();
    const result = await postMessage(user.uid, inputs.channel, inputs.text);
    return { status: 'success', ...result };
};

export const postMessageTool: SkillTool = {
    definition: postMessageDef,
    implementation: postMessageImpl
};

const manifest: SkillManifest = {
    tools: [postMessageTool]
};

export default manifest;
export const tools = [postMessageTool];
