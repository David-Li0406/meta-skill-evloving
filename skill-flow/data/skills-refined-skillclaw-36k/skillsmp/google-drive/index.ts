
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { uploadFile } from '@/server/integrations/drive/service';
import { requireUser } from '@/server/auth/auth';

// --- Tool 1: Upload File ---
const uploadFileDef: ToolDefinition = {
    name: 'drive.upload_file',
    description: 'Upload (create) a file in Google Drive.',
    inputSchema: {
        type: 'object',
        properties: {
            filename: { type: 'string', description: 'Name of the file (e.g. report.txt)' },
            content: { type: 'string', description: 'Text content of the file' }
        },
        required: ['filename', 'content']
    },
    category: 'write',
    requiredPermission: 'admin:all'
};

const uploadFileImpl = async (ctx: any, inputs: any) => {
    const user = await requireUser();
    const result = await uploadFile(user.uid, inputs.filename, inputs.content);
    return { status: 'success', ...result };
};

export const uploadFileTool: SkillTool = {
    definition: uploadFileDef,
    implementation: uploadFileImpl
};

const manifest: SkillManifest = {
    tools: [uploadFileTool]
};

export default manifest;
export const tools = [uploadFileTool];
