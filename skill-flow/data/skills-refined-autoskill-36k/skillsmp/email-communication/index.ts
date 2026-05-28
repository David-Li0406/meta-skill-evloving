
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { gmailAction } from '@/server/tools/gmail';
import { sendGenericEmail } from '@/lib/email/dispatcher';

// --- Tool 1: Gmail List ---
const gmailListDef: ToolDefinition = {
    name: 'gmail.list',
    description: 'List recent emails from the user\'s inbox.',
    inputSchema: {
        type: 'object',
        properties: {
            query: { type: 'string', description: 'Gmail search query (e.g., "is:unread from:boss")' }
        }
    },
    category: 'read',
    requiredPermission: 'read:orders'
};

const gmailListImpl = async (ctx: any, inputs: any) => {
    return await gmailAction({ action: 'list', query: inputs.query });
};

export const gmailListTool: SkillTool = {
    definition: gmailListDef,
    implementation: gmailListImpl
};

// --- Tool 2: Gmail Read ---
const gmailReadDef: ToolDefinition = {
    name: 'gmail.read',
    description: 'Read the full content of a specific email.',
    inputSchema: {
        type: 'object',
        properties: {
            messageId: { type: 'string', description: 'The ID of the message to read' }
        },
        required: ['messageId']
    },
    category: 'read',
    requiredPermission: 'read:orders'
};

const gmailReadImpl = async (ctx: any, inputs: any) => {
    return await gmailAction({ action: 'read', messageId: inputs.messageId });
};

export const gmailReadTool: SkillTool = {
    definition: gmailReadDef,
    implementation: gmailReadImpl
};

// --- Tool 3: Gmail Send (User) ---
const gmailSendDef: ToolDefinition = {
    name: 'gmail.send',
    description: 'Send an email from the user\'s connected Gmail account.',
    inputSchema: {
        type: 'object',
        properties: {
            to: { type: 'string' },
            subject: { type: 'string' },
            body: { type: 'string' }
        },
        required: ['to', 'subject', 'body']
    },
    category: 'side-effect',
    requiredPermission: 'manage:campaigns'
};

const gmailSendImpl = async (ctx: any, inputs: any) => {
    return await gmailAction({ 
        action: 'send', 
        to: inputs.to, 
        subject: inputs.subject, 
        body: inputs.body 
    });
};

export const gmailSendTool: SkillTool = {
    definition: gmailSendDef,
    implementation: gmailSendImpl
};

// --- Tool 4: Marketing Send (System) ---
const marketingSendDef: ToolDefinition = {
    name: 'marketing.sendEmail',
    description: 'Send a formatted marketing/system email via the brand\'s provider (Mailjet/SendGrid).',
    inputSchema: {
        type: 'object',
        properties: {
            to: { type: 'string' },
            subject: { type: 'string' },
            htmlBody: { type: 'string', description: 'HTML content of the email' }
        },
        required: ['to', 'subject', 'htmlBody']
    },
    category: 'side-effect',
    requiredPermission: 'manage:campaigns'
};

import { checkContent } from '@/server/agents/deebo/policy-gate';

import { requireUser } from '@/server/auth/auth';

const marketingSendImpl = async (ctx: any, inputs: any) => {
    let userEmail = '';
    try {
        const user = await requireUser();
        userEmail = user.email || '';
    } catch (e) { /* System call or no user */ }

    // Logic: Skip compliance for self-sends, internal bakedbot domains, or explicit test emails
    const isSelfSend = userEmail && inputs.to.toLowerCase() === userEmail.toLowerCase();
    const isInternal = inputs.to.includes('@bakedbot.ai');
    const isTest = inputs.to.includes('test') || inputs.subject.toLowerCase().includes('test');
    
    if (!isSelfSend && !isInternal && !isTest) {
        // 1. Compliance Pre-flight (Deebo)
        const compliance = await checkContent(inputs.htmlBody + ' ' + inputs.subject, {
            channel: 'email',
            jurisdictions: ['US']
        });

        if (!compliance.allowed) {
            throw new Error(`Compliance Blocked: ${compliance.reason}. Violations: ${compliance.violations?.join(', ')}`);
        }
    }

    // 2. Execute Send
    const result = await sendGenericEmail({
        to: inputs.to,
        subject: inputs.subject,
        htmlBody: inputs.htmlBody
    });
    
    return { 
        success: result.success, 
        error: result.error,
        provider: 'system', 
        compliance: (isSelfSend || isInternal || isTest) ? 'skipped (internal/test)' : 'verified' 
    };
};

export const marketingSendTool: SkillTool = {
    definition: marketingSendDef,
    implementation: marketingSendImpl
};

const manifest: SkillManifest = {
    tools: [gmailListTool, gmailReadTool, gmailSendTool, marketingSendTool]
};

export default manifest;
export const tools = [gmailListTool, gmailReadTool, gmailSendTool, marketingSendTool];
