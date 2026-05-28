/**
 * Task CRUD operations
 */

const { loadTasks, saveTasks, archiveTask } = require('./storage.cjs');
const { generateId, now, isValidStatus, isValidPriority, isValidEffort, parseTags } = require('./utils.cjs');

/**
 * Add a new task
 * @param {string} title - Task title
 * @param {object} options - Optional fields
 * @returns {object} Created task
 */
function addTask(title, options = {}) {
  const data = loadTasks();
  data._counter = (data._counter || 0) + 1;

  const task = {
    id: generateId(data._counter),
    title,
    status: 'pending',
    created: now(),
    updated: now()
  };

  // Add optional fields if provided
  if (options.description) task.description = options.description;
  if (options.priority && isValidPriority(options.priority)) task.priority = options.priority;
  if (options.effort && isValidEffort(options.effort)) task.effort = options.effort;
  if (options.tags) task.tags = parseTags(options.tags);
  if (options.assignee) task.assignee = options.assignee;
  if (options.due_date) task.due_date = options.due_date;

  data.tasks.push(task);
  saveTasks(data);
  return task;
}

/**
 * List tasks with optional filters
 * @param {object} filters - Filter options
 * @returns {object[]} Filtered tasks
 */
function listTasks(filters = {}) {
  const data = loadTasks();
  let tasks = data.tasks;

  if (filters.status) {
    tasks = tasks.filter(t => t.status === filters.status);
  }
  if (filters.tag) {
    tasks = tasks.filter(t => t.tags && t.tags.includes(filters.tag));
  }
  if (filters.assignee) {
    tasks = tasks.filter(t => t.assignee === filters.assignee);
  }
  if (filters.priority) {
    tasks = tasks.filter(t => t.priority === filters.priority);
  }

  return tasks;
}

/**
 * Get a single task by ID
 * @param {string} id - Task ID
 * @returns {object|null} Task or null
 */
function getTask(id) {
  const data = loadTasks();
  return data.tasks.find(t => t.id === id) || null;
}

/**
 * Update a task
 * @param {string} id - Task ID
 * @param {object} updates - Fields to update
 * @returns {object|null} Updated task or null
 */
function updateTask(id, updates) {
  const data = loadTasks();
  const idx = data.tasks.findIndex(t => t.id === id);

  if (idx === -1) return null;

  const task = data.tasks[idx];

  // Apply updates
  if (updates.title) task.title = updates.title;
  if (updates.description !== undefined) task.description = updates.description;
  if (updates.status && isValidStatus(updates.status)) task.status = updates.status;
  if (updates.priority && isValidPriority(updates.priority)) task.priority = updates.priority;
  if (updates.effort && isValidEffort(updates.effort)) task.effort = updates.effort;
  if (updates.tags) task.tags = parseTags(updates.tags);
  if (updates.assignee !== undefined) task.assignee = updates.assignee;
  if (updates.due_date !== undefined) task.due_date = updates.due_date;
  if (updates.notes) {
    task.progress = task.progress || {};
    task.progress.notes = updates.notes;
  }

  task.updated = now();
  data.tasks[idx] = task;
  saveTasks(data);
  return task;
}

/**
 * Complete a task (marks complete + auto-archives)
 * @param {string} id - Task ID
 * @param {string} notes - Completion notes
 * @returns {object|null} Completed task or null
 */
function completeTask(id, notes = null) {
  const data = loadTasks();
  const idx = data.tasks.findIndex(t => t.id === id);

  if (idx === -1) return null;

  const task = data.tasks[idx];
  task.status = 'completed';
  task.updated = now();
  task.completed_at = now();

  if (notes) {
    task.progress = task.progress || {};
    task.progress.notes = notes;
  }

  // Archive and remove from active tasks
  archiveTask(task);
  data.tasks.splice(idx, 1);
  saveTasks(data);

  return task;
}

/**
 * Delete a task
 * @param {string} id - Task ID
 * @returns {boolean} Success
 */
function deleteTask(id) {
  const data = loadTasks();
  const idx = data.tasks.findIndex(t => t.id === id);

  if (idx === -1) return false;

  data.tasks.splice(idx, 1);
  saveTasks(data);
  return true;
}

/**
 * Set task to in_progress and return context
 * @param {string} id - Task ID
 * @returns {object|null} Task with context or null
 */
function workOnTask(id) {
  const task = updateTask(id, { status: 'in_progress' });
  return task;
}

/**
 * Add blocking relationship
 * @param {string} id - Task ID
 * @param {string} blockedById - Blocking task ID
 * @returns {object|null} Updated task or null
 */
function blockTask(id, blockedById) {
  const data = loadTasks();
  const idx = data.tasks.findIndex(t => t.id === id);
  const blockerIdx = data.tasks.findIndex(t => t.id === blockedById);

  if (idx === -1 || blockerIdx === -1) return null;

  // Update blocked task
  const task = data.tasks[idx];
  task.blocked_by = task.blocked_by || [];
  if (!task.blocked_by.includes(blockedById)) {
    task.blocked_by.push(blockedById);
  }
  task.status = 'blocked';
  task.updated = now();

  // Update blocker task
  const blocker = data.tasks[blockerIdx];
  blocker.blocks = blocker.blocks || [];
  if (!blocker.blocks.includes(id)) {
    blocker.blocks.push(id);
  }

  saveTasks(data);
  return task;
}

module.exports = {
  addTask,
  listTasks,
  getTask,
  updateTask,
  completeTask,
  deleteTask,
  workOnTask,
  blockTask
};
