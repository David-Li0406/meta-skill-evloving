/**
 * Markdown view generation for tasks
 */

const { loadTasks } = require('./storage.cjs');

/**
 * Generate status emoji
 * @param {string} status - Task status
 * @returns {string} Emoji
 */
function statusIcon(status) {
  const icons = {
    pending: '⏳',
    in_progress: '🔄',
    completed: '✅',
    blocked: '🚫'
  };
  return icons[status] || '❓';
}

/**
 * Generate priority badge
 * @param {string} priority - Priority level
 * @returns {string} Badge text
 */
function priorityBadge(priority) {
  const badges = {
    critical: '🔴 CRITICAL',
    high: '🟠 High',
    medium: '🟡 Medium',
    low: '🟢 Low'
  };
  return badges[priority] || '';
}

/**
 * Format a single task as markdown
 * @param {object} task - Task object
 * @returns {string} Markdown string
 */
function formatTask(task) {
  const lines = [];
  const checkbox = task.status === 'completed' ? '[x]' : '[ ]';

  lines.push(`### ${checkbox} ${task.id}: ${task.title}`);
  lines.push('');

  // Status line
  const parts = [`**Status:** ${statusIcon(task.status)} ${task.status}`];
  if (task.priority) parts.push(`| ${priorityBadge(task.priority)}`);
  if (task.effort) parts.push(`| **Effort:** ${task.effort}`);
  lines.push(parts.join(' '));

  // Description
  if (task.description) {
    lines.push('');
    lines.push(task.description);
  }

  // Tags
  if (task.tags && task.tags.length > 0) {
    lines.push('');
    lines.push(`**Tags:** ${task.tags.map(t => '`' + t + '`').join(' ')}`);
  }

  // Metadata
  const meta = [];
  if (task.assignee) meta.push(`Assignee: ${task.assignee}`);
  if (task.due_date) meta.push(`Due: ${task.due_date}`);
  if (meta.length > 0) {
    lines.push('');
    lines.push(`*${meta.join(' | ')}*`);
  }

  // Context
  if (task.context) {
    lines.push('');
    lines.push('**Context:**');
    if (task.context.plan) lines.push(`- Plan: \`${task.context.plan}\``);
    if (task.context.phase) lines.push(`- Phase: ${task.context.phase}`);
    if (task.context.branch) lines.push(`- Branch: \`${task.context.branch}\``);
  }

  // Progress notes
  if (task.progress && task.progress.notes) {
    lines.push('');
    lines.push(`> ${task.progress.notes}`);
  }

  // Dependencies
  if (task.blocked_by && task.blocked_by.length > 0) {
    lines.push('');
    lines.push(`**Blocked by:** ${task.blocked_by.join(', ')}`);
  }

  lines.push('');
  lines.push('---');

  return lines.join('\n');
}

/**
 * Generate full markdown view of all tasks
 * @returns {string} Markdown document
 */
function generateView() {
  const data = loadTasks();
  const lines = [];

  lines.push('# Tasks');
  lines.push('');
  lines.push(`*Updated: ${data.metadata.updated}*`);
  lines.push('');

  // Group by status
  const groups = {
    in_progress: data.tasks.filter(t => t.status === 'in_progress'),
    blocked: data.tasks.filter(t => t.status === 'blocked'),
    pending: data.tasks.filter(t => t.status === 'pending')
  };

  if (groups.in_progress.length > 0) {
    lines.push('## 🔄 In Progress');
    lines.push('');
    groups.in_progress.forEach(t => lines.push(formatTask(t)));
  }

  if (groups.blocked.length > 0) {
    lines.push('## 🚫 Blocked');
    lines.push('');
    groups.blocked.forEach(t => lines.push(formatTask(t)));
  }

  if (groups.pending.length > 0) {
    lines.push('## ⏳ Pending');
    lines.push('');
    groups.pending.forEach(t => lines.push(formatTask(t)));
  }

  // Summary
  lines.push('## Summary');
  lines.push('');
  lines.push(`| Status | Count |`);
  lines.push(`|--------|-------|`);
  lines.push(`| In Progress | ${groups.in_progress.length} |`);
  lines.push(`| Blocked | ${groups.blocked.length} |`);
  lines.push(`| Pending | ${groups.pending.length} |`);
  lines.push(`| **Total** | **${data.tasks.length}** |`);

  return lines.join('\n');
}

module.exports = {
  generateView,
  formatTask,
  statusIcon,
  priorityBadge
};
