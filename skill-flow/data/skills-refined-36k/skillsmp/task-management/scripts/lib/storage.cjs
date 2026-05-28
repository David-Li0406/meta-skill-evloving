/**
 * YAML storage operations for tasks
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { dateStamp } = require('./utils.cjs');

const DEFAULT_STORAGE_PATH = '.claude/tasks';
const TASKS_FILE = 'tasks.yaml';

/**
 * Get storage path from env or default
 * @returns {string} Storage directory path
 */
function getStoragePath() {
  return process.env.TASK_STORAGE_PATH || DEFAULT_STORAGE_PATH;
}

/**
 * Get full path to tasks file
 * @returns {string} Full path
 */
function getTasksFilePath() {
  return path.join(process.cwd(), getStoragePath(), TASKS_FILE);
}

/**
 * Get archive directory path
 * @returns {string} Archive path
 */
function getArchivePath() {
  return path.join(process.cwd(), getStoragePath(), 'archive');
}

/**
 * Ensure storage directory exists
 */
function ensureStorageDir() {
  const storagePath = path.join(process.cwd(), getStoragePath());
  const archivePath = getArchivePath();

  if (!fs.existsSync(storagePath)) {
    fs.mkdirSync(storagePath, { recursive: true });
  }
  if (!fs.existsSync(archivePath)) {
    fs.mkdirSync(archivePath, { recursive: true });
  }
}

/**
 * Create initial tasks file structure
 * @returns {object} Empty tasks structure
 */
function createEmptyTasksFile() {
  return {
    version: '1.0',
    metadata: {
      project: path.basename(process.cwd()),
      created: new Date().toISOString().split('T')[0],
      updated: new Date().toISOString()
    },
    tasks: [],
    _counter: 0
  };
}

/**
 * Load tasks from YAML file
 * @returns {object} Tasks data
 */
function loadTasks() {
  ensureStorageDir();
  const filePath = getTasksFilePath();

  if (!fs.existsSync(filePath)) {
    const empty = createEmptyTasksFile();
    saveTasks(empty);
    return empty;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  return yaml.load(content) || createEmptyTasksFile();
}

/**
 * Save tasks to YAML file
 * @param {object} data - Tasks data
 */
function saveTasks(data) {
  ensureStorageDir();
  const filePath = getTasksFilePath();

  data.metadata.updated = new Date().toISOString();
  const content = yaml.dump(data, {
    indent: 2,
    lineWidth: 120,
    noRefs: true
  });

  fs.writeFileSync(filePath, content, 'utf8');
}

/**
 * Archive completed task
 * @param {object} task - Task to archive
 */
function archiveTask(task) {
  const archivePath = getArchivePath();
  const archiveFile = path.join(archivePath, `${dateStamp()}-batch.yaml`);

  let archive = { archived: [] };
  if (fs.existsSync(archiveFile)) {
    archive = yaml.load(fs.readFileSync(archiveFile, 'utf8')) || { archived: [] };
  }

  task.archived_at = new Date().toISOString();
  archive.archived.push(task);

  fs.writeFileSync(archiveFile, yaml.dump(archive, { indent: 2 }), 'utf8');
}

module.exports = {
  getStoragePath,
  getTasksFilePath,
  getArchivePath,
  ensureStorageDir,
  loadTasks,
  saveTasks,
  archiveTask
};
