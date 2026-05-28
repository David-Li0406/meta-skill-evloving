import { describe, it, expect, jest, beforeEach } from '@jest/globals';

// Create the mock for AppleScript execution
const mockExecuteAppleScriptFile = jest.fn<(scriptName: string, args?: string[]) => Promise<string>>();

// Mock the applescript module (this is what json-builder actually uses)
jest.unstable_mockModule('../../src/lib/applescript.js', () => ({
  executeAppleScriptFile: mockExecuteAppleScriptFile
}));

// Dynamic imports after mocking
const { ThingsJSONBuilder } = await import('../../src/lib/json-builder.js');

describe('ThingsJSONBuilder', () => {
  let builder: ThingsJSONBuilder;

  beforeEach(() => {
    builder = new ThingsJSONBuilder();
    jest.clearAllMocks();
    // Default mock return value (project ID for create-project)
    mockExecuteAppleScriptFile.mockResolvedValue('mock-project-id');
  });

  describe('createTodo', () => {
    it('should create a simple to-do', async () => {
      const params = { title: 'Test Todo' };

      const result = await builder.createTodo(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('create-todo', [
        'Test Todo', // title
        '',          // notes
        '',          // when
        '',          // deadline
        '',          // tags
        '',          // list
        '',          // listId
        '',          // heading
        'false',     // completed
        'false',     // canceled
        ''           // checklistItems
      ]);
      expect(result).toBe('Created to-do: "Test Todo"');
    });

    it('should create a to-do with all parameters', async () => {
      const params = {
        title: 'Complex Todo',
        notes: 'Some notes',
        when: 'today' as const,
        deadline: '2025-01-15',
        tags: ['work', 'urgent'],
        checklist_items: ['Step 1', 'Step 2'],
        list: 'inbox',
        completed: false
      };

      const result = await builder.createTodo(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('create-todo', [
        'Complex Todo',     // title
        'Some notes',       // notes
        'today',            // when
        '2025-01-15',       // deadline
        'work,urgent',      // tags (comma-separated)
        'inbox',            // list
        '',                 // listId
        '',                 // heading
        'false',            // completed
        'false',            // canceled
        'Step 1\nStep 2'    // checklistItems (newline-separated)
      ]);
      expect(result).toBe('Created to-do: "Complex Todo"');
    });
  });

  describe('createProject', () => {
    it('should create a simple project', async () => {
      const params = { title: 'Test Project' };

      const result = await builder.createProject(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('create-project', [
        'Test Project', // title
        '',             // notes
        '',             // when
        '',             // deadline
        '',             // tags
        '',             // areaId
        '',             // area
        'false',        // completed
        'false'         // canceled
      ]);
      const parsed = JSON.parse(result);
      expect(parsed.success).toBe(true);
      expect(parsed.project.title).toBe('Test Project');
      expect(parsed.project.id).toBe('mock-project-id');
    });

    it('should create a project with items (todos)', async () => {
      const params = {
        title: 'Project with Todos',
        items: [
          { type: 'todo' as const, title: 'Task 1' },
          { type: 'todo' as const, title: 'Task 2' },
          { type: 'todo' as const, title: 'Task 3' }
        ]
      };

      const result = await builder.createProject(params);

      // First call creates the project
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(1, 'create-project', [
        'Project with Todos',
        '', '', '', '', '', '', 'false', 'false'
      ]);

      // Then 3 calls to create todos
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(2, 'create-todo', [
        'Task 1', '', '', '', '', '', 'mock-project-id', '', 'false', 'false', ''
      ]);
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(3, 'create-todo', [
        'Task 2', '', '', '', '', '', 'mock-project-id', '', 'false', 'false', ''
      ]);
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(4, 'create-todo', [
        'Task 3', '', '', '', '', '', 'mock-project-id', '', 'false', 'false', ''
      ]);

      const parsed = JSON.parse(result);
      expect(parsed.success).toBe(true);
      expect(parsed.project.title).toBe('Project with Todos');
      expect(parsed.items.succeeded).toBe(3);
      expect(parsed.created).toEqual(['Task 1', 'Task 2', 'Task 3']);
    });

    it('should create a project with mixed items (headings are skipped)', async () => {
      const params = {
        title: 'Complex Project',
        items: [
          { type: 'heading' as const, title: 'Phase 1' },
          { type: 'todo' as const, title: 'Task A' },
          { type: 'todo' as const, title: 'Task B' }
        ],
        area: 'Work',
        tags: ['important', 'q1']
      };

      const result = await builder.createProject(params);

      // First call creates the project
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(1, 'create-project', [
        'Complex Project',
        '',                 // notes
        '',                 // when
        '',                 // deadline
        'important,q1',     // tags
        '',                 // areaId
        'Work',             // area
        'false',
        'false'
      ]);

      // Only 2 calls for todos (heading is skipped)
      expect(mockExecuteAppleScriptFile).toHaveBeenCalledTimes(3); // 1 project + 2 todos

      const parsed = JSON.parse(result);
      expect(parsed.success).toBe(true);
      expect(parsed.project.title).toBe('Complex Project');
      expect(parsed.items.succeeded).toBe(2);
      expect(parsed.items.skipped).toBe(1);
      expect(parsed.skipped[0].title).toBe('Phase 1');
    });
  });

  describe('parameter conversion', () => {
    it('should omit undefined parameters by using empty strings', async () => {
      const params = {
        title: 'Test',
        notes: undefined,
        when: undefined,
        tags: []
      };

      await builder.createTodo(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('create-todo', [
        'Test',
        '',       // notes -> empty string
        '',       // when -> empty string
        '',       // deadline
        '',       // tags (empty array -> empty string)
        '',       // list
        '',       // listId
        '',       // heading
        'false',
        'false',
        ''
      ]);
    });

    it('should convert tags array to comma-separated string', async () => {
      const params = {
        title: 'Test',
        tags: ['tag1', 'tag2', 'tag3']
      };

      await builder.createProject(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('create-project', [
        'Test',
        '',
        '',
        '',
        'tag1,tag2,tag3', // comma-separated tags
        '',
        '',
        'false',
        'false'
      ]);
    });
  });

  describe('updateTodo', () => {
    it('should update a to-do with title and notes', async () => {
      const params = {
        id: 'todo-123',
        title: 'Updated Todo',
        notes: 'Updated notes'
      };

      const result = await builder.updateTodo(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('update-todo', [
        'todo-123',       // id
        'Updated Todo',   // title
        'Updated notes',  // notes
        '',               // when
        '',               // deadline
        '',               // tags
        '',               // list
        '',               // listId
        '',               // completed (not set, empty)
        ''                // canceled (not set, empty)
      ]);
      expect(result).toBe('Updated to-do: "Updated Todo"');
    });

    it('should update a to-do with completed status', async () => {
      const params = {
        id: 'todo-123',
        completed: true
      };

      const result = await builder.updateTodo(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('update-todo', [
        'todo-123',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        'true',   // completed
        ''        // canceled
      ]);
      expect(result).toBe('Updated to-do: "todo-123"');
    });
  });

  describe('updateProject', () => {
    it('should update a project', async () => {
      const params = {
        id: 'project-456',
        title: 'Updated Project',
        area: 'New Area'
      };

      const result = await builder.updateProject(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('update-project', [
        'project-456',     // id
        'Updated Project', // title
        '',                // notes
        '',                // when
        '',                // deadline
        '',                // tags
        '',                // areaId
        'New Area',        // area
        '',                // completed
        ''                 // canceled
      ]);
      expect(result).toBe('Updated project: "Updated Project"');
    });
  });

  describe('addItemsToProject', () => {
    it('should add todos to an existing project (headings skipped)', async () => {
      const params = {
        id: 'project-789',
        items: [
          { type: 'heading' as const, title: 'New Phase' },
          { type: 'todo' as const, title: 'New Task' }
        ]
      };

      const result = await builder.addItemsToProject(params);

      // Only one call for the todo (heading is skipped)
      expect(mockExecuteAppleScriptFile).toHaveBeenCalledTimes(1);
      expect(mockExecuteAppleScriptFile).toHaveBeenCalledWith('create-todo', [
        'New Task',
        '',
        '',
        '',
        '',
        '',
        'project-789',  // list_id is set to project id
        '',
        'false',
        'false',
        ''
      ]);
      const parsed = JSON.parse(result);
      expect(parsed.summary.succeeded).toBe(1);
      expect(parsed.summary.skipped).toBe(1);
      expect(parsed.success).toEqual(['New Task']);
      expect(parsed.skipped[0].title).toBe('New Phase');
    });

    it('should add multiple todos with proper attributes', async () => {
      const params = {
        id: 'aBc123dEf456gHi789JkL',
        items: [
          { type: 'heading' as const, title: 'Day 1' },
          { type: 'todo' as const, title: 'Morning activity', notes: 'Early start' },
          { type: 'todo' as const, title: 'Lunch at cafe' },
          { type: 'heading' as const, title: 'Day 2' },
          { type: 'todo' as const, title: 'Museum visit', when: 'tomorrow' as const }
        ]
      };

      const result = await builder.addItemsToProject(params);

      // Should be called 3 times (once for each todo, headings are skipped)
      expect(mockExecuteAppleScriptFile).toHaveBeenCalledTimes(3);

      // First todo
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(1, 'create-todo', [
        'Morning activity',
        'Early start',
        '',
        '',
        '',
        '',
        'aBc123dEf456gHi789JkL',
        '',
        'false',
        'false',
        ''
      ]);

      // Second todo
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(2, 'create-todo', [
        'Lunch at cafe',
        '',
        '',
        '',
        '',
        '',
        'aBc123dEf456gHi789JkL',
        '',
        'false',
        'false',
        ''
      ]);

      // Third todo
      expect(mockExecuteAppleScriptFile).toHaveBeenNthCalledWith(3, 'create-todo', [
        'Museum visit',
        '',
        'tomorrow',
        '',
        '',
        '',
        'aBc123dEf456gHi789JkL',
        '',
        'false',
        'false',
        ''
      ]);

      const parsed = JSON.parse(result);
      expect(parsed.summary.succeeded).toBe(3);
      expect(parsed.summary.skipped).toBe(2);
      expect(parsed.success).toEqual(['Morning activity', 'Lunch at cafe', 'Museum visit']);
    });

    it('should handle only headings', async () => {
      const params = {
        id: 'project-789',
        items: [
          { type: 'heading' as const, title: 'Phase 1' },
          { type: 'heading' as const, title: 'Phase 2' }
        ]
      };

      const result = await builder.addItemsToProject(params);

      expect(mockExecuteAppleScriptFile).not.toHaveBeenCalled();
      const parsed = JSON.parse(result);
      expect(parsed.summary.succeeded).toBe(0);
      expect(parsed.summary.skipped).toBe(2);
      expect(parsed.skipped).toHaveLength(2);
      expect(parsed.skipped[0].title).toBe('Phase 1');
      expect(parsed.skipped[1].title).toBe('Phase 2');
    });

    it('should handle errors gracefully', async () => {
      mockExecuteAppleScriptFile
        .mockRejectedValueOnce(new Error('API Error'))
        .mockResolvedValueOnce('');

      const params = {
        id: 'project-789',
        items: [
          { type: 'todo' as const, title: 'Task 1' },
          { type: 'todo' as const, title: 'Task 2' }
        ]
      };

      const result = await builder.addItemsToProject(params);

      expect(mockExecuteAppleScriptFile).toHaveBeenCalledTimes(2);
      const parsed = JSON.parse(result);
      expect(parsed.summary.succeeded).toBe(1);
      expect(parsed.summary.failed).toBe(1);
      expect(parsed.success).toEqual(['Task 2']);
      expect(parsed.failed).toHaveLength(1);
      expect(parsed.failed[0].title).toBe('Task 1');
      expect(parsed.failed[0].reason).toBe('API Error');
    });
  });
});
