
import { SkillManifest, SkillTool } from '../../types';
import { ToolDefinition } from '@/types/agent-toolkit';
import { calendarAction } from '@/server/tools/calendar';
import { sheetsAction } from '@/server/tools/sheets';
import { scheduleTask } from '@/server/tools/scheduler';

// --- Tool 1: Calendar List ---
const calendarListDef: ToolDefinition = {
    name: 'productivity.calendar_list',
    description: 'List upcoming calendar events.',
    inputSchema: {
        type: 'object',
        properties: {
            timeMin: { type: 'string', description: 'ISO start time (default now)' },
            maxResults: { type: 'number', description: 'Max events (default 10)' }
        }
    },
    category: 'read',
    requiredPermission: 'admin:all'
};

const calendarListImpl = async (ctx: any, inputs: any) => {
    return await calendarAction({ 
        action: 'list', 
        timeMin: inputs.timeMin, 
        maxResults: inputs.maxResults 
    });
};

export const calendarListTool: SkillTool = {
    definition: calendarListDef,
    implementation: calendarListImpl
};

// --- Tool 2: Calendar Create ---
const calendarCreateDef: ToolDefinition = {
    name: 'productivity.calendar_create',
    description: 'Create a new calendar event.',
    inputSchema: {
        type: 'object',
        properties: {
            summary: { type: 'string', description: 'Event title' },
            startTime: { type: 'string', description: 'ISO start time' },
            endTime: { type: 'string', description: 'ISO end time' },
            description: { type: 'string', description: 'Event description' }
        },
        required: ['summary', 'startTime', 'endTime']
    },
    category: 'write',
    requiredPermission: 'admin:all'
};

const calendarCreateImpl = async (ctx: any, inputs: any) => {
    return await calendarAction({ 
        action: 'create', 
        summary: inputs.summary, 
        startTime: inputs.startTime, 
        endTime: inputs.endTime,
        description: inputs.description
    });
};

export const calendarCreateTool: SkillTool = {
    definition: calendarCreateDef,
    implementation: calendarCreateImpl
};

// --- Tool 3: Sheets Read ---
const sheetsReadDef: ToolDefinition = {
    name: 'productivity.sheets_read',
    description: 'Read values from a Google Sheet.',
    inputSchema: {
        type: 'object',
        properties: {
            spreadsheetId: { type: 'string', description: 'The Google Sheet ID' },
            range: { type: 'string', description: 'Range (e.g. "Sheet1!A1:B10")' }
        },
        required: ['spreadsheetId', 'range']
    },
    category: 'read',
    requiredPermission: 'admin:all'
};

const sheetsReadImpl = async (ctx: any, inputs: any) => {
    return await sheetsAction({ 
        action: 'read', 
        spreadsheetId: inputs.spreadsheetId, 
        range: inputs.range 
    });
};

export const sheetsReadTool: SkillTool = {
    definition: sheetsReadDef,
    implementation: sheetsReadImpl
};

// --- Tool 4: Sheets Append ---
const sheetsAppendDef: ToolDefinition = {
    name: 'productivity.sheets_append',
    description: 'Append rows to a Google Sheet.',
    inputSchema: {
        type: 'object',
        properties: {
            spreadsheetId: { type: 'string' },
            range: { type: 'string' },
            values: { 
                type: 'array', 
                items: { type: 'array', items: { type: 'string' } },
                description: '2D array of strings'
            }
        },
        required: ['spreadsheetId', 'range', 'values']
    },
    category: 'write',
    requiredPermission: 'admin:all'
};

const sheetsAppendImpl = async (ctx: any, inputs: any) => {
    return await sheetsAction({ 
        action: 'append', 
        spreadsheetId: inputs.spreadsheetId, 
        range: inputs.range, 
        values: inputs.values 
    });
};

export const sheetsAppendTool: SkillTool = {
    definition: sheetsAppendDef,
    implementation: sheetsAppendImpl
};


// --- Tool 5: Sheets Create ---
const sheetsCreateDef: ToolDefinition = {
    name: 'productivity.sheets_create',
    description: 'Create a new Google Sheet.',
    inputSchema: {
        type: 'object',
        properties: {
            title: { type: 'string', description: 'Spreadsheet title' }
        }
    },
    category: 'write',
    requiredPermission: 'admin:all'
};

const sheetsCreateImpl = async (ctx: any, inputs: any) => {
    return await sheetsAction({ 
        action: 'create', 
        title: inputs.title 
    });
};

export const sheetsCreateTool: SkillTool = {
    definition: sheetsCreateDef,
    implementation: sheetsCreateImpl
};

// --- Tool 6: Schedule Task ---
const scheduleTaskDef: ToolDefinition = {
    name: 'productivity.schedule_task',
    description: 'Schedule a recurring task for the agent.',
    inputSchema: {
        type: 'object',
        properties: {
            task: { type: 'string', description: 'Description of task to perform' },
            cron: { type: 'string', description: 'Cron expression (e.g. "0 9 * * *")' }
        },
        required: ['task', 'cron']
    },
    category: 'side-effect',
    requiredPermission: 'admin:all'
};

const scheduleTaskImpl = async (ctx: any, inputs: any) => {
    return await scheduleTask({ 
        action: 'create', 
        task: inputs.task, 
        cron: inputs.cron 
    });
};

export const scheduleTaskTool: SkillTool = {
    definition: scheduleTaskDef,
    implementation: scheduleTaskImpl
};

const manifest: SkillManifest = {
    tools: [
        calendarListTool, calendarCreateTool, 
        sheetsReadTool, sheetsAppendTool, sheetsCreateTool,
        scheduleTaskTool
    ]
};

export default manifest;
export const tools = [
    calendarListTool, calendarCreateTool, 
    sheetsReadTool, sheetsAppendTool, sheetsCreateTool,
    scheduleTaskTool
];
