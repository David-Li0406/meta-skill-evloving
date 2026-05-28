#!/usr/bin/env npx tsx
/**
 * ClickUp API CLI Tool
 * Standalone wrapper for ClickUp REST API v2
 *
 * Usage:
 *   npx tsx clickup-api.ts <command> [args...]
 *
 * Commands:
 *   validate                       - Verify API token
 *   workspaces                     - List workspaces
 *   spaces <workspaceId>           - List spaces in workspace
 *   folders <spaceId>              - List folders in space
 *   lists <spaceId>                - List all lists in space
 *   tasks <listId> [status]        - List tasks (optionally filter by status)
 *   task <taskId>                  - Get full task context
 *   update-status <taskId> <status> - Update task status
 *   comment <taskId> <message>     - Post comment to task
 *   create-task <listId> <name> [description] - Create task in list
 *   create-subtask <parentTaskId> <name> [description] - Create subtask
 *   sync-from-file <taskFile> <parentTaskId> - Sync task file to ClickUp subtasks
 *   sync-completion <taskFile>     - Sync completed items to ClickUp
 *   set-custom-field <taskId> <fieldId> <value> - Set custom field value
 *   set-pr <taskId> <prUrl>        - Set Github PR custom field on task
 *   download-attachments <taskId> <outputDir> - Download all task attachments
 *
 * Environment:
 *   CLICKUP_API_TOKEN - API token (can also be set in .env file in skill folder)
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { dirname, join, basename } from "path";
import { fileURLToPath } from "url";
// Dynamic import for task-parser since we're a CLI script
async function loadTaskParser() {
  // Get the directory where this script lives using __dirname equivalent
  const currentFileUrl = import.meta.url;
  const currentFilePath = fileURLToPath(currentFileUrl);
  const scriptDir = dirname(currentFilePath);
  const taskParserPath = join(scriptDir, "task-parser.ts");
  const { parseTaskFile, extractTaskId } = await import(`file://${taskParserPath}`);
  return { parseTaskFile, extractTaskId };
}

// Load .env file from skill directory
function loadEnvFile(): void {
  // Get the directory where this script lives
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  // Skill directory is one level up from scripts/
  const skillDir = dirname(scriptDir);
  const envPath = join(skillDir, ".env");

  if (existsSync(envPath)) {
    const content = readFileSync(envPath, "utf-8");
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      // Skip comments and empty lines
      if (!trimmed || trimmed.startsWith("#")) continue;

      const eqIndex = trimmed.indexOf("=");
      if (eqIndex > 0) {
        const key = trimmed.slice(0, eqIndex).trim();
        let value = trimmed.slice(eqIndex + 1).trim();
        // Remove quotes if present
        if ((value.startsWith('"') && value.endsWith('"')) ||
            (value.startsWith("'") && value.endsWith("'"))) {
          value = value.slice(1, -1);
        }
        // Only set if not already in environment (env vars take precedence)
        if (!process.env[key]) {
          process.env[key] = value;
        }
      }
    }
  }
}

// Load env file immediately
loadEnvFile();

const CLICKUP_API_BASE = "https://api.clickup.com/api/v2";

// Types
interface ClickUpUser {
  id: number;
  username: string;
  email: string;
}

interface ClickUpWorkspace {
  id: string;
  name: string;
  color: string;
  avatar: string | null;
  members: Array<{ user: ClickUpUser }>;
}

interface ClickUpSpace {
  id: string;
  name: string;
  private: boolean;
  statuses: Array<{ status: string; color: string }>;
}

interface ClickUpFolder {
  id: string;
  name: string;
  hidden: boolean;
  space: { id: string; name: string };
}

interface ClickUpList {
  id: string;
  name: string;
  folder?: { id: string; name: string };
  space: { id: string; name: string };
  task_count?: number;
}

interface ClickUpTask {
  id: string;
  name: string;
  description: string;
  status: { status: string; color: string };
  priority?: { priority: string; color: string };
  assignees: Array<{ id: number; username: string; email: string }>;
  tags: Array<{ name: string; tag_fg: string; tag_bg: string }>;
  url: string;
  date_created: string;
  date_updated: string;
  custom_fields?: Array<{
    id: string;
    name: string;
    type: string;
    value?: unknown;
  }>;
}

interface ClickUpComment {
  id: string;
  comment_text: string;
  user: { id: number; username: string; email: string };
  date: string;
  comment?: Array<{
    type: string;
    text?: string;
    attributes?: {
      attachment?: { url: string; extension: string };
    };
  }>;
}

interface ClickUpAttachment {
  id: string;
  title: string;
  url: string;
  extension: string;
}

// API Client
class ClickUpAPI {
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${CLICKUP_API_BASE}${endpoint}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        Authorization: this.token,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`ClickUp API error ${response.status}: ${errorText}`);
    }

    return response.json() as Promise<T>;
  }

  async validateToken(): Promise<ClickUpUser> {
    const response = await this.request<{ user: ClickUpUser }>("/user");
    return response.user;
  }

  async getWorkspaces(): Promise<ClickUpWorkspace[]> {
    const response = await this.request<{ teams: ClickUpWorkspace[] }>("/team");
    return response.teams;
  }

  async getSpaces(workspaceId: string): Promise<ClickUpSpace[]> {
    const response = await this.request<{ spaces: ClickUpSpace[] }>(
      `/team/${workspaceId}/space?archived=false`
    );
    return response.spaces;
  }

  async getFolders(spaceId: string): Promise<ClickUpFolder[]> {
    const response = await this.request<{ folders: ClickUpFolder[] }>(
      `/space/${spaceId}/folder?archived=false`
    );
    return response.folders;
  }

  async getListsInSpace(spaceId: string): Promise<ClickUpList[]> {
    const response = await this.request<{ lists: ClickUpList[] }>(
      `/space/${spaceId}/list?archived=false`
    );
    return response.lists;
  }

  async getListsInFolder(folderId: string): Promise<ClickUpList[]> {
    const response = await this.request<{ lists: ClickUpList[] }>(
      `/folder/${folderId}/list?archived=false`
    );
    return response.lists;
  }

  async getAllListsInSpace(spaceId: string): Promise<ClickUpList[]> {
    // Get folderless lists
    const folderlessLists = await this.getListsInSpace(spaceId);

    // Get lists from folders
    const folders = await this.getFolders(spaceId);
    const folderLists: ClickUpList[] = [];

    for (const folder of folders) {
      const lists = await this.getListsInFolder(folder.id);
      folderLists.push(...lists);
    }

    return [...folderlessLists, ...folderLists];
  }

  async getTasksByList(listId: string, status?: string): Promise<ClickUpTask[]> {
    const params = new URLSearchParams();
    params.append("archived", "false");
    params.append("subtasks", "true");
    params.append("include_closed", "false");

    if (status) {
      params.append("statuses[]", status);
    }

    const response = await this.request<{ tasks: ClickUpTask[] }>(
      `/list/${listId}/task?${params.toString()}`
    );
    return response.tasks;
  }

  async getTask(taskId: string): Promise<ClickUpTask> {
    return this.request<ClickUpTask>(`/task/${taskId}?include_subtasks=true`);
  }

  async getTaskComments(taskId: string): Promise<ClickUpComment[]> {
    const response = await this.request<{ comments: ClickUpComment[] }>(
      `/task/${taskId}/comment`
    );
    return response.comments;
  }

  async getTaskAttachments(taskId: string): Promise<ClickUpAttachment[]> {
    const task = await this.getTask(taskId);
    const attachments: ClickUpAttachment[] = [];

    if (task.custom_fields) {
      for (const field of task.custom_fields) {
        if (field.type === "attachment" && field.value) {
          if (Array.isArray(field.value)) {
            attachments.push(...(field.value as ClickUpAttachment[]));
          }
        }
      }
    }

    return attachments;
  }

  async getCommentAttachments(taskId: string): Promise<Array<{
    commentId: string;
    url: string;
    type: string;
  }>> {
    const comments = await this.getTaskComments(taskId);
    const attachments: Array<{ commentId: string; url: string; type: string }> = [];

    for (const comment of comments) {
      if (comment.comment && Array.isArray(comment.comment)) {
        for (const block of comment.comment) {
          if (block.type === "attachment" && block.attributes?.attachment) {
            attachments.push({
              commentId: comment.id,
              url: block.attributes.attachment.url,
              type: block.attributes.attachment.extension || "unknown",
            });
          }
        }
      }
    }

    return attachments;
  }

  async getFullTaskContext(taskId: string): Promise<{
    task: ClickUpTask;
    comments: ClickUpComment[];
    attachments: ClickUpAttachment[];
    commentAttachments: Array<{ commentId: string; url: string; type: string }>;
  }> {
    const [task, comments, attachments, commentAttachments] = await Promise.all([
      this.getTask(taskId),
      this.getTaskComments(taskId),
      this.getTaskAttachments(taskId),
      this.getCommentAttachments(taskId),
    ]);

    return { task, comments, attachments, commentAttachments };
  }

  async updateTaskStatus(taskId: string, status: string): Promise<ClickUpTask> {
    return this.request<ClickUpTask>(`/task/${taskId}`, {
      method: "PUT",
      body: JSON.stringify({ status }),
    });
  }

  async postComment(taskId: string, commentText: string): Promise<{ id: string }> {
    const response = await this.request<{ id: string | number }>(`/task/${taskId}/comment`, {
      method: "POST",
      body: JSON.stringify({
        comment_text: commentText,
        notify_all: false,
      }),
    });
    return { id: String(response.id) };
  }

  async setCustomField(taskId: string, fieldId: string, value: unknown): Promise<void> {
    await this.request(`/task/${taskId}/field/${fieldId}`, {
      method: "POST",
      body: JSON.stringify({ value }),
    });
  }

  async createTask(
    listId: string,
    name: string,
    options?: {
      description?: string;
      parent?: string;
      status?: string;
    }
  ): Promise<ClickUpTask> {
    const body: Record<string, unknown> = { name };
    if (options?.description) body.description = options.description;
    if (options?.parent) body.parent = options.parent;
    if (options?.status) body.status = options.status;

    return this.request<ClickUpTask>(`/list/${listId}/task`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  }

  async createSubtask(
    parentTaskId: string,
    name: string,
    description?: string,
    status?: string
  ): Promise<ClickUpTask> {
    // First get parent task to find its list
    const parentTask = await this.getTask(parentTaskId);
    // The task response includes list info in custom_fields or we need to extract from URL
    // Actually the task response has a list field when fetched with details
    const taskWithList = await this.request<ClickUpTask & { list: { id: string } }>(
      `/task/${parentTaskId}`
    );
    const listId = taskWithList.list.id;

    return this.createTask(listId, name, {
      description,
      parent: parentTaskId,
      status,
    });
  }

  async downloadAttachment(
    url: string,
    outputPath: string
  ): Promise<{ success: boolean; size: number; error?: string }> {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        return { success: false, size: 0, error: `HTTP ${response.status}` };
      }

      const arrayBuffer = await response.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      writeFileSync(outputPath, buffer);

      return { success: true, size: buffer.length };
    } catch (err) {
      return {
        success: false,
        size: 0,
        error: err instanceof Error ? err.message : String(err),
      };
    }
  }

  async downloadAllAttachments(
    taskId: string,
    outputDir: string,
    maxSizeBytes: number = 50 * 1024 * 1024 // 50MB default
  ): Promise<{
    downloaded: Array<{
      title: string;
      localPath: string;
      type: string;
      source: "task" | "comment";
      size: number;
    }>;
    skipped: Array<{
      title: string;
      url: string;
      reason: string;
    }>;
    failed: Array<{
      title: string;
      url: string;
      error: string;
    }>;
    totalSize: number;
  }> {
    // Ensure output directory exists
    if (!existsSync(outputDir)) {
      mkdirSync(outputDir, { recursive: true });
    }

    const context = await this.getFullTaskContext(taskId);
    const downloaded: Array<{
      title: string;
      localPath: string;
      type: string;
      source: "task" | "comment";
      size: number;
    }> = [];
    const skipped: Array<{ title: string; url: string; reason: string }> = [];
    const failed: Array<{ title: string; url: string; error: string }> = [];
    let totalSize = 0;

    // Helper to sanitize filename
    const sanitizeFilename = (name: string): string => {
      return name.replace(/[^a-zA-Z0-9._-]/g, "_").slice(0, 100);
    };

    // Helper to get unique filename
    const usedNames = new Set<string>();
    const getUniqueFilename = (baseName: string): string => {
      let name = baseName;
      let counter = 1;
      while (usedNames.has(name)) {
        const ext = baseName.includes(".") ? baseName.slice(baseName.lastIndexOf(".")) : "";
        const base = baseName.includes(".") ? baseName.slice(0, baseName.lastIndexOf(".")) : baseName;
        name = `${base}_${counter}${ext}`;
        counter++;
      }
      usedNames.add(name);
      return name;
    };

    // Download task attachments
    for (const attachment of context.attachments) {
      const filename = sanitizeFilename(attachment.title || `attachment_${attachment.id}.${attachment.extension}`);
      const uniqueFilename = getUniqueFilename(filename);
      const localPath = join(outputDir, uniqueFilename);

      // Check file size via HEAD request first
      try {
        const headResponse = await fetch(attachment.url, { method: "HEAD" });
        const contentLength = headResponse.headers.get("content-length");
        const fileSize = contentLength ? parseInt(contentLength, 10) : 0;

        if (fileSize > maxSizeBytes) {
          skipped.push({
            title: attachment.title,
            url: attachment.url,
            reason: `File too large (${(fileSize / 1024 / 1024).toFixed(1)}MB > ${maxSizeBytes / 1024 / 1024}MB limit)`,
          });
          continue;
        }
      } catch {
        // If HEAD fails, proceed with download anyway
      }

      const result = await this.downloadAttachment(attachment.url, localPath);
      if (result.success) {
        downloaded.push({
          title: attachment.title,
          localPath: uniqueFilename,
          type: attachment.extension,
          source: "task",
          size: result.size,
        });
        totalSize += result.size;
      } else {
        failed.push({
          title: attachment.title,
          url: attachment.url,
          error: result.error || "Unknown error",
        });
      }

      // Small delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    // Download comment attachments
    for (const attachment of context.commentAttachments) {
      // Generate filename from URL for comment attachments
      const urlFilename = attachment.url.split("/").pop() || `comment_attachment.${attachment.type}`;
      const filename = sanitizeFilename(`comment_${attachment.commentId}_${urlFilename}`);
      const uniqueFilename = getUniqueFilename(filename);
      const localPath = join(outputDir, uniqueFilename);

      // Check file size via HEAD request first
      try {
        const headResponse = await fetch(attachment.url, { method: "HEAD" });
        const contentLength = headResponse.headers.get("content-length");
        const fileSize = contentLength ? parseInt(contentLength, 10) : 0;

        if (fileSize > maxSizeBytes) {
          skipped.push({
            title: urlFilename,
            url: attachment.url,
            reason: `File too large (${(fileSize / 1024 / 1024).toFixed(1)}MB > ${maxSizeBytes / 1024 / 1024}MB limit)`,
          });
          continue;
        }
      } catch {
        // If HEAD fails, proceed with download anyway
      }

      const result = await this.downloadAttachment(attachment.url, localPath);
      if (result.success) {
        downloaded.push({
          title: urlFilename,
          localPath: uniqueFilename,
          type: attachment.type,
          source: "comment",
          size: result.size,
        });
        totalSize += result.size;
      } else {
        failed.push({
          title: urlFilename,
          url: attachment.url,
          error: result.error || "Unknown error",
        });
      }

      // Small delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    return { downloaded, skipped, failed, totalSize };
  }
}

// Output helpers
function output(data: unknown): void {
  console.log(JSON.stringify(data, null, 2));
}

function error(message: string): never {
  console.error(JSON.stringify({ error: message }));
  process.exit(1);
}

// Main CLI
async function main(): Promise<void> {
  // Support both CLICKUP_ACCESS_TOKEN (OAuth) and CLICKUP_API_TOKEN (personal token)
  const token = process.env.CLICKUP_ACCESS_TOKEN || process.env.CLICKUP_API_TOKEN;
  if (!token) {
    error("ClickUp token not set. Options:\n  1. Complete OAuth flow in the UI (http://localhost:3000), then copy token to .env\n  2. Get personal API token from ClickUp Settings > Apps > API Token\n  3. Set in .env file: CLICKUP_ACCESS_TOKEN=<your-token>");
  }

  const api = new ClickUpAPI(token);
  const [, , command, ...args] = process.argv;

  if (!command) {
    error("Usage: clickup-api.ts <command> [args...]\nCommands: validate, workspaces, spaces, folders, lists, tasks, task, update-status, comment, create-task, create-subtask, sync-from-file, sync-completion, set-custom-field, set-pr, download-attachments");
  }

  try {
    switch (command) {
      case "validate": {
        const user = await api.validateToken();
        output({ success: true, user });
        break;
      }

      case "workspaces": {
        const workspaces = await api.getWorkspaces();
        output({
          count: workspaces.length,
          workspaces: workspaces.map(w => ({
            id: w.id,
            name: w.name,
          })),
        });
        break;
      }

      case "spaces": {
        const workspaceId = args[0];
        if (!workspaceId) error("Usage: spaces <workspaceId>");
        const spaces = await api.getSpaces(workspaceId);
        output({
          count: spaces.length,
          spaces: spaces.map(s => ({
            id: s.id,
            name: s.name,
            statuses: s.statuses.map(st => st.status),
          })),
        });
        break;
      }

      case "folders": {
        const spaceId = args[0];
        if (!spaceId) error("Usage: folders <spaceId>");
        const folders = await api.getFolders(spaceId);
        output({
          count: folders.length,
          folders: folders.map(f => ({
            id: f.id,
            name: f.name,
          })),
        });
        break;
      }

      case "lists": {
        const spaceId = args[0];
        if (!spaceId) error("Usage: lists <spaceId>");
        const lists = await api.getAllListsInSpace(spaceId);
        output({
          count: lists.length,
          lists: lists.map(l => ({
            id: l.id,
            name: l.name,
            folder: l.folder?.name || "(folderless)",
            taskCount: l.task_count,
          })),
        });
        break;
      }

      case "tasks": {
        const listId = args[0];
        const status = args[1];
        if (!listId) error("Usage: tasks <listId> [status]");
        const tasks = await api.getTasksByList(listId, status);
        output({
          count: tasks.length,
          tasks: tasks.map(t => ({
            id: t.id,
            name: t.name,
            status: t.status.status,
            priority: t.priority?.priority,
            tags: t.tags.map(tag => tag.name),
            url: t.url,
          })),
        });
        break;
      }

      case "task": {
        const taskId = args[0];
        if (!taskId) error("Usage: task <taskId>");
        const context = await api.getFullTaskContext(taskId);
        output({
          task: {
            id: context.task.id,
            name: context.task.name,
            description: context.task.description,
            status: context.task.status.status,
            priority: context.task.priority?.priority,
            tags: context.task.tags.map(t => t.name),
            assignees: context.task.assignees.map(a => a.username),
            url: context.task.url,
            dateCreated: context.task.date_created,
            dateUpdated: context.task.date_updated,
          },
          comments: context.comments.map(c => ({
            id: c.id,
            user: c.user.username,
            text: c.comment_text,
            date: c.date,
          })),
          attachments: context.attachments.map(a => ({
            id: a.id,
            title: a.title,
            url: a.url,
            type: a.extension,
          })),
          commentAttachments: context.commentAttachments,
        });
        break;
      }

      case "update-status": {
        const taskId = args[0];
        const status = args[1];
        if (!taskId || !status) error("Usage: update-status <taskId> <status>");
        const task = await api.updateTaskStatus(taskId, status);
        output({
          success: true,
          task: {
            id: task.id,
            name: task.name,
            status: task.status.status,
          },
        });
        break;
      }

      case "comment": {
        const taskId = args[0];
        const message = args.slice(1).join(" ");
        if (!taskId || !message) error("Usage: comment <taskId> <message>");
        const result = await api.postComment(taskId, message);
        output({ success: true, commentId: result.id });
        break;
      }

      case "create-task": {
        const listId = args[0];
        const name = args[1];
        // Parse --status flag from remaining args
        const remainingArgs = args.slice(2);
        const statusFlagIndex = remainingArgs.findIndex(a => a.startsWith("--status="));
        let status: string | undefined;
        if (statusFlagIndex !== -1) {
          status = remainingArgs[statusFlagIndex].replace("--status=", "");
          remainingArgs.splice(statusFlagIndex, 1);
        }
        const description = remainingArgs.join(" ") || undefined;
        if (!listId || !name) error("Usage: create-task <listId> <name> [description] [--status=<status>]");
        const task = await api.createTask(listId, name, { description, status });
        output({
          success: true,
          task: {
            id: task.id,
            name: task.name,
            url: task.url,
            status: task.status.status,
          },
        });
        break;
      }

      case "create-subtask": {
        const parentTaskId = args[0];
        const name = args[1];
        // Parse --status flag from remaining args
        const remainingArgs = args.slice(2);
        const statusFlagIndex = remainingArgs.findIndex(a => a.startsWith("--status="));
        let status: string | undefined;
        if (statusFlagIndex !== -1) {
          status = remainingArgs[statusFlagIndex].replace("--status=", "");
          remainingArgs.splice(statusFlagIndex, 1);
        }
        const description = remainingArgs.join(" ") || undefined;
        if (!parentTaskId || !name) error("Usage: create-subtask <parentTaskId> <name> [description] [--status=<status>]");
        const subtask = await api.createSubtask(parentTaskId, name, description, status);
        output({
          success: true,
          subtask: {
            id: subtask.id,
            name: subtask.name,
            url: subtask.url,
            status: subtask.status.status,
            parent: parentTaskId,
          },
        });
        break;
      }

      case "sync-from-file": {
        const taskFilePath = args[0];
        const parentTaskId = args[1];
        if (!taskFilePath || !parentTaskId) {
          error("Usage: sync-from-file <taskFilePath> <parentTaskId>");
        }

        // Parse the task file
        const { parseTaskFile } = await loadTaskParser();
        const parsed = parseTaskFile(taskFilePath);
        if (parsed.phases.length === 0) {
          error("No phases found in task file");
        }

        // Prepare mapping structure
        interface SyncMapping {
          parentTaskId: string;
          taskFile: string;
          syncedAt: string;
          phases: Record<string, {
            clickupId: string;
            items: Record<string, string>;
          }>;
        }

        const mapping: SyncMapping = {
          parentTaskId,
          taskFile: taskFilePath,
          syncedAt: new Date().toISOString(),
          phases: {},
        };

        const results: Array<{ phase: string; phaseId: string; items: Array<{ name: string; id: string }> }> = [];

        // Create subtasks for each phase
        for (const phase of parsed.phases) {
          // Create phase subtask with business-friendly description
          const completedCount = phase.items.filter(i => i.completed).length;
          const phaseDescription = [
            `${phase.items.length} task${phase.items.length === 1 ? '' : 's'} to complete`,
            completedCount > 0 ? `(${completedCount} already done)` : '',
          ].filter(Boolean).join(' ');

          const phaseTask = await api.createSubtask(parentTaskId, phase.name, phaseDescription);

          mapping.phases[phase.name] = {
            clickupId: phaseTask.id,
            items: {},
          };

          const phaseResult = {
            phase: phase.name,
            phaseId: phaseTask.id,
            items: [] as Array<{ name: string; id: string }>,
          };

          // Create item subtasks under the phase with business-friendly descriptions
          for (const item of phase.items) {
            // Build a rich description for business users
            const descriptionParts: string[] = [];

            // Add phase context so the item makes sense standalone
            descriptionParts.push(`**Phase:** ${phase.name}`);

            // Add file location if available
            if (item.file) {
              descriptionParts.push(`**File:** \`${item.file}\``);
            }

            // Add task context from parent
            if (parsed.title) {
              descriptionParts.push(`**Project:** ${parsed.title}`);
            }

            const itemDescription = descriptionParts.join('\n');
            const itemTask = await api.createSubtask(phaseTask.id, item.text, itemDescription || undefined);

            mapping.phases[phase.name].items[item.text] = itemTask.id;
            phaseResult.items.push({
              name: item.text,
              id: itemTask.id,
            });

            // If item is already completed, mark it as closed
            if (item.completed) {
              await api.updateTaskStatus(itemTask.id, "CLOSED");
            }

            // Small delay to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 100));
          }

          results.push(phaseResult);
        }

        // Save mapping file
        const syncDir = join(process.cwd(), ".clickup-sync");
        if (!existsSync(syncDir)) {
          mkdirSync(syncDir, { recursive: true });
        }
        const mappingPath = join(syncDir, `${parentTaskId}.json`);
        writeFileSync(mappingPath, JSON.stringify(mapping, null, 2));

        output({
          success: true,
          mappingFile: mappingPath,
          phases: results,
          totalItems: results.reduce((sum, p) => sum + p.items.length, 0),
        });
        break;
      }

      case "sync-completion": {
        const taskFilePath = args[0];
        if (!taskFilePath) {
          error("Usage: sync-completion <taskFilePath>");
        }

        // Find mapping file
        const { parseTaskFile, extractTaskId } = await loadTaskParser();
        const parsed = parseTaskFile(taskFilePath);
        const clickupUrl = parsed.clickupUrl;
        if (!clickupUrl) {
          error("Task file missing ClickUp URL. Add **ClickUp:** <url> to the file.");
        }

        const taskId = extractTaskId(clickupUrl);
        if (!taskId) {
          error(`Could not extract task ID from URL: ${clickupUrl}`);
        }

        const syncDir = join(process.cwd(), ".clickup-sync");
        const mappingPath = join(syncDir, `${taskId}.json`);

        if (!existsSync(mappingPath)) {
          error(`No mapping file found at ${mappingPath}. Run sync-from-file first.`);
        }

        interface SyncMapping {
          parentTaskId: string;
          taskFile: string;
          syncedAt: string;
          phases: Record<string, {
            clickupId: string;
            items: Record<string, string>;
          }>;
        }

        const mapping: SyncMapping = JSON.parse(readFileSync(mappingPath, "utf-8"));

        const results = {
          synced: 0,
          alreadyComplete: 0,
          notFound: 0,
          errors: [] as string[],
        };

        // Sync completion status for each item
        for (const phase of parsed.phases) {
          const phaseMapping = mapping.phases[phase.name];
          if (!phaseMapping) {
            continue; // Phase not in mapping, skip
          }

          for (const item of phase.items) {
            if (!item.completed) continue; // Only sync completed items

            const clickupTaskId = phaseMapping.items[item.text];
            if (!clickupTaskId) {
              results.notFound++;
              continue;
            }

            try {
              // Check current status first
              const currentTask = await api.getTask(clickupTaskId);
              if (currentTask.status.status.toLowerCase() === "closed") {
                results.alreadyComplete++;
              } else {
                await api.updateTaskStatus(clickupTaskId, "CLOSED");
                results.synced++;
              }
            } catch (err) {
              results.errors.push(`Failed to update ${item.text}: ${err instanceof Error ? err.message : String(err)}`);
            }

            // Small delay to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 100));
          }
        }

        output({
          success: true,
          ...results,
        });
        break;
      }

      case "set-custom-field": {
        const taskId = args[0];
        const fieldId = args[1];
        const value = args.slice(2).join(" ");
        if (!taskId || !fieldId || !value) {
          error("Usage: set-custom-field <taskId> <fieldId> <value>");
        }
        await api.setCustomField(taskId, fieldId, value);
        output({ success: true, taskId, fieldId, value });
        break;
      }

      case "set-pr": {
        const taskId = args[0];
        const prUrl = args[1];
        if (!taskId || !prUrl) {
          error("Usage: set-pr <taskId> <prUrl>");
        }

        // Get task to find Github PR field ID
        const task = await api.getTask(taskId);
        const prField = task.custom_fields?.find(
          (cf) =>
            cf.name.toLowerCase().includes("github") &&
            cf.name.toLowerCase().includes("pr")
        );

        if (!prField) {
          error("Github PR custom field not found on this task");
        }

        await api.setCustomField(taskId, prField.id, prUrl);
        output({
          success: true,
          taskId,
          fieldId: prField.id,
          fieldName: prField.name,
          value: prUrl,
        });
        break;
      }

      case "download-attachments": {
        const taskId = args[0];
        const outputDir = args[1];
        if (!taskId || !outputDir) {
          error("Usage: download-attachments <taskId> <outputDir>");
        }

        const results = await api.downloadAllAttachments(taskId, outputDir);
        output({
          success: true,
          outputDir,
          downloaded: results.downloaded,
          skipped: results.skipped,
          failed: results.failed,
          summary: {
            downloadedCount: results.downloaded.length,
            skippedCount: results.skipped.length,
            failedCount: results.failed.length,
            totalSizeBytes: results.totalSize,
            totalSizeMB: (results.totalSize / 1024 / 1024).toFixed(2),
          },
        });
        break;
      }

      default:
        error(`Unknown command: ${command}\nCommands: validate, workspaces, spaces, folders, lists, tasks, task, update-status, comment, create-task, create-subtask, sync-from-file, sync-completion, set-custom-field, set-pr, download-attachments`);
    }
  } catch (err) {
    error(err instanceof Error ? err.message : String(err));
  }
}

main();
