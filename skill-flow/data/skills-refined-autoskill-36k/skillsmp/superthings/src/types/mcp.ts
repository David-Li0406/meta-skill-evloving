import { z } from 'zod';

/**
 * Zod schemas for MCP parameter validation
 */

// Custom validators
const WhenEnum = z.enum(['today', 'tomorrow', 'evening', 'anytime', 'someday']);
const DateString = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'Invalid date format. Use YYYY-MM-DD');
const DateTimeString = z
  .string()
  .regex(
    /^\d{4}-\d{2}-\d{2}@\d{2}:\d{2}$/,
    'Invalid datetime format. Use YYYY-MM-DD@HH:MM'
  );
const ThingsIdString = z
  .string()
  .regex(
    /^[A-Za-z0-9]{20,24}$/,
    'Invalid Things ID format. Expected: alphanumeric string like "aBc123dEf456gHi789JkL" (20-24 characters). NOT the project name! Use things_get_projects to find the correct ID first.'
  );

export const AddTodoSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255, 'Title too long'),
  notes: z.string().max(10000, 'Notes too long').optional(),
  when: z.union([WhenEnum, DateString, DateTimeString]).optional().describe('Schedule the todo: today/tomorrow/evening (relative), anytime/someday (Things categories), YYYY-MM-DD (specific date), or YYYY-MM-DD@HH:MM (specific time)'),
  deadline: DateString.optional(),
  tags: z.array(z.string().max(50)).max(20, 'Too many tags').optional(),
  checklist_items: z
    .array(z.string().max(255))
    .max(100, 'Too many checklist items')
    .optional()
    .describe('Break down this todo into smaller, manageable steps using a checklist. Perfect for complex tasks that have multiple components but don\'t warrant a full project. Each checklist item can be individually checked off, providing visual progress feedback. Use when user mentions "steps", "checklist", "break down into parts", or when a task has multiple actionable components (e.g., "Plan event" → ["Book venue", "Arrange catering", "Send invites"]). Alternative to creating separate todos for multi-step tasks.'),
  list_id: z.string().optional().describe('ID of the project or area to add the todo to'),
  list: z.string().max(255).optional().describe('Name of the project, area, or built-in list (inbox, today, anytime, etc.)'),
  heading: z.string().max(255).optional().describe('Place this todo under a specific heading within the project'),
  completed: z.boolean().optional(),
  canceled: z.boolean().optional(),
});

const ChecklistItemSchema = z.object({
  title: z.string().min(1, 'Checklist item title is required').max(255, 'Title too long'),
  completed: z.boolean().optional().default(false),
});

const TodoItemSchema = z.object({
  type: z.literal('todo').describe('Creates an individual task/activity in the project. Todos that appear after a heading in the items array will be visually grouped under that heading in Things 3. Use for specific activities, locations to visit, meals to have, etc.'),
  title: z.string().min(1, 'Todo title is required').max(255, 'Title too long'),
  notes: z.string().max(10000, 'Notes too long').optional(),
  when: z.union([WhenEnum, DateString, DateTimeString]).optional().describe('Schedule the todo: today/tomorrow/evening (relative), anytime/someday (Things categories), YYYY-MM-DD (specific date), or YYYY-MM-DD@HH:MM (specific time)'),
  deadline: DateString.optional(),
  tags: z.array(z.string().max(50)).max(20, 'Too many tags').optional(),
  completed: z.boolean().optional(),
  canceled: z.boolean().optional(),
  checklist: z.array(ChecklistItemSchema).max(100, 'Too many checklist items').optional().describe('Break down this todo into smaller, manageable steps using a structured checklist. Each item can be individually checked off and tracked. Perfect for complex tasks within projects that have multiple components. Use when user mentions "steps", "checklist", "break down into parts", or when a task has multiple actionable components. Provides detailed progress tracking within project todos.'),
});

const HeadingItemSchema = z.object({
  type: z.literal('heading').describe('Creates a section header/divider in the project. Use this when user wants to \'separate by days\', \'organize by categories\', or create \'sections\'. Headings are visual separators - todos that appear after a heading in the items array will be visually grouped under it in Things 3.'),
  title: z.string().min(1, 'Heading title is required').max(255, 'Title too long'),
  archived: z.boolean().optional().default(false),
});

const ProjectItemSchema = z.discriminatedUnion('type', [TodoItemSchema, HeadingItemSchema]);

export const AddProjectSchema = z.object({
  title: z.string().min(1, 'Title is required').max(255, 'Title too long'),
  notes: z.string().max(10000, 'Notes too long').optional(),
  when: z.union([WhenEnum, DateString, DateTimeString]).optional().describe('Schedule the todo: today/tomorrow/evening (relative), anytime/someday (Things categories), YYYY-MM-DD (specific date), or YYYY-MM-DD@HH:MM (specific time)'),
  deadline: DateString.optional(),
  tags: z.array(z.string().max(50)).max(20, 'Too many tags').optional(),
  area_id: z.string().optional().describe('ID of the area to place the project in'),
  area: z.string().max(255).optional().describe('Name of the area to place the project in'),
  items: z.array(ProjectItemSchema).max(200, 'Too many items').optional().describe('Create a structured project with sections (headings) and todos in a flat array. Each item must have a \'type\' field: \'heading\' for section dividers, \'todo\' for tasks. Items are siblings - todos after a heading are visually grouped under it. Example: [{type: \'heading\', title: \'Day 1\'}, {type: \'todo\', title: \'Morning walk\'}, {type: \'todo\', title: \'Breakfast\'}, {type: \'heading\', title: \'Day 2\'}, {type: \'todo\', title: \'Museum visit\'}]. Order matters - todos appear under the most recent heading.'),
  completed: z.boolean().optional(),
  canceled: z.boolean().optional(),
});

export const ShowSchema = z
  .object({
    id: z.string().optional().describe('ID of a specific to-do, project, or area'),
    query: z.string().max(255).optional().describe('Navigate to a list: inbox, today, anytime, upcoming, someday, logbook, trash'),
    filter: z.array(z.string()).optional().describe('Filter by tags when showing a list'),
  })
  .refine((data) => data.id || data.query, {
    message: 'Either id or query must be provided',
  });


export const GetListByNameSchema = z.object({
  list: z.enum([
    'inbox',
    'today',
    'upcoming',
    'anytime',
    'someday',
    'logbook',
    'trash',
  ]),
  max_results: z.number().optional().describe('Limit number of results returned (defaults to all if not specified)'),
});

export const GetProjectSchema = z.object({
  project_id: z.string().min(1, 'Project ID is required'),
  max_results: z.number().optional().describe('Limit number of results returned (defaults to all if not specified)'),
});

export const GetAreaSchema = z.object({
  area_id: z.string().min(1, 'Area ID is required'),
  max_results: z.number().optional().describe('Limit number of results returned (defaults to all if not specified)'),
});

export const GetListSchema = z.object({
  max_results: z.number().optional().describe('Limit number of results returned (defaults to all if not specified)'),
});


export const GetTodoDetailsSchema = z.object({
  id: z.string().min(1, 'Todo ID is required').describe('ID of the to-do to get detailed information for'),
});

// New unified JSON update schemas
export const UpdateTodoJSONSchema = AddTodoSchema.extend({
  id: ThingsIdString.describe('Unique system-generated ID of the todo to update (alphanumeric, 20-24 chars). NOT the todo title! Use things_get_project, things_get_list, or things_search to find the correct ID first. Example: "AbC123dEf456gHi789JkL"'),
  operation: z.literal('update').default('update')
});

export const UpdateProjectJSONSchema = AddProjectSchema.extend({
  id: ThingsIdString.describe('Unique system-generated ID of the project to update (alphanumeric, 20-24 chars). NOT the project title! Use things_get_projects or things_search to find the correct ID first. Example: "xYz789aBc123dEf456gHi"'),
  operation: z.literal('update').default('update')
});

export const AddItemsToProjectSchema = z.object({
  id: ThingsIdString.describe('Unique system-generated ID of the project (alphanumeric like "pRj123aBc456dEf789gHi", 20-24 chars). NOT the project title! You MUST use things_get_projects to find the correct ID first. Common mistake: using project name like "My Vacation Planning" instead of its ID.'),
  items: z.array(ProjectItemSchema).min(1, 'At least one item required').max(200, 'Too many items').describe('Add structured todos and headings to an existing project. Items are added as a flat array where headings act as visual separators. Todos that follow a heading will appear grouped under it. Example: [{type: \'heading\', title: \'Phase 2\'}, {type: \'todo\', title: \'Task 1\'}, {type: \'todo\', title: \'Task 2\'}].'),
  operation: z.literal('update').default('update')
});

// Complete/Cancel todo schemas
export const CompleteTodoSchema = z.object({
  id: ThingsIdString.describe('ID of the to-do to mark as complete'),
});

export const CancelTodoSchema = z.object({
  id: ThingsIdString.describe('ID of the to-do to cancel'),
});

// Delete schemas - require confirmation to prevent accidental deletion
export const DeleteTodoSchema = z.object({
  id: ThingsIdString.describe('ID of the to-do to delete'),
  confirm: z.literal(true).describe('Must be true to confirm deletion'),
});

export const DeleteProjectSchema = z.object({
  id: ThingsIdString.describe('ID of the project to delete'),
  confirm: z.literal(true).describe('Must be true to confirm deletion'),
});

// Statistics schema
export const GetStatsSchema = z.object({});

// Search schema for finding todos across lists
export const SearchTodosSchema = z.object({
  query: z.string().optional().describe('Keyword to search for in todo titles. Use "*" or omit to match all.'),
  list: z.enum(['inbox', 'today', 'anytime', 'upcoming', 'someday', '']).optional().describe('Filter by specific list. Omit to search all lists.'),
  tag: z.string().optional().describe('Filter by tag name'),
  has_url: z.boolean().optional().describe('Set to true to only return todos with URLs in the title'),
  max_results: z.number().max(500).optional().describe('Maximum number of results to return (default: 100, max: 500)'),
});

// Bulk update schema for batch operations
export const BulkUpdateSchema = z.object({
  ids: z.array(ThingsIdString).min(1, 'At least one ID required').max(100, 'Maximum 100 IDs per batch').describe('Array of to-do IDs to update'),
  updates: z.object({
    when: z.union([WhenEnum, DateString, DateTimeString]).optional().describe('Set when to schedule todos: today/tomorrow/evening (relative), anytime/someday (Things categories), YYYY-MM-DD (specific date)'),
    deadline: DateString.optional().describe('Set deadline date (YYYY-MM-DD)'),
    tags_add: z.array(z.string().max(50)).max(20).optional().describe('Tags to add to all todos'),
    tags_remove: z.array(z.string().max(50)).max(20).optional().describe('Tags to remove from all todos'),
    list_id: z.string().optional().describe('Move all todos to this project/area ID'),
    list: z.string().max(255).optional().describe('Move all todos to this list by name'),
  }).refine(data => Object.values(data).some(v => v !== undefined), {
    message: 'At least one update field must be specified'
  }),
});
