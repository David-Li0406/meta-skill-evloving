/**
 * Utility functions for task management
 */

/**
 * Generate a task ID with format t-XXX
 * @param {number} counter - Current counter value
 * @returns {string} Task ID
 */
function generateId(counter) {
  return `t-${String(counter).padStart(3, '0')}`;
}

/**
 * Get current ISO timestamp
 * @returns {string} ISO 8601 timestamp
 */
function now() {
  return new Date().toISOString();
}

/**
 * Get current date in YYMMDD format
 * @returns {string} Date string
 */
function dateStamp() {
  const d = new Date();
  const yy = String(d.getFullYear()).slice(-2);
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yy}${mm}${dd}`;
}

/**
 * Parse comma-separated tags into array
 * @param {string} tagString - Comma-separated tags
 * @returns {string[]} Array of tags
 */
function parseTags(tagString) {
  if (!tagString) return [];
  return tagString.split(',').map(t => t.trim()).filter(Boolean);
}

/**
 * Validate task status
 * @param {string} status - Status to validate
 * @returns {boolean} Is valid
 */
function isValidStatus(status) {
  return ['pending', 'in_progress', 'completed', 'blocked'].includes(status);
}

/**
 * Validate priority
 * @param {string} priority - Priority to validate
 * @returns {boolean} Is valid
 */
function isValidPriority(priority) {
  return ['low', 'medium', 'high', 'critical'].includes(priority);
}

/**
 * Validate effort estimate
 * @param {string} effort - Effort to validate
 * @returns {boolean} Is valid
 */
function isValidEffort(effort) {
  return ['S', 'M', 'L', 'XL'].includes(effort);
}

module.exports = {
  generateId,
  now,
  dateStamp,
  parseTags,
  isValidStatus,
  isValidPriority,
  isValidEffort
};
