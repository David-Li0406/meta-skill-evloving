import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  ClickUpConfig,
  Task,
  TimeEntry,
  TimeEntryCreate,
  TimeEntryUpdate,
  Comment,
  Space,
  Folder,
  List,
  Workspace,
  WorkspaceMember,
  TasksResponse,
  TimeEntriesResponse,
  CommentsResponse,
  SpacesResponse,
  FoldersResponse,
  ListsResponse,
  WorkspacesResponse,
  MembersResponse,
} from '../types/clickup.js';

const API_BASE = 'https://api.clickup.com/api/v2';

export class ClickUpClient {
  private client: AxiosInstance;
  private config: ClickUpConfig;

  constructor(config: ClickUpConfig) {
    this.config = config;
    this.client = axios.create({
      baseURL: API_BASE,
      headers: {
        Authorization: config.apiToken,
        'Content-Type': 'application/json',
      },
    });

    // Add retry logic for rate limiting
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 429) {
          // Rate limited - wait and retry
          const retryAfter = parseInt(
            error.response.headers['retry-after'] || '60',
            10
          );
          console.warn(`Rate limited. Waiting ${retryAfter} seconds...`);
          await this.sleep(retryAfter * 1000);
          return this.client.request(error.config!);
        }
        throw error;
      }
    );
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // ============================================
  // WORKSPACE & TEAM METHODS
  // ============================================

  async getWorkspaces(): Promise<Workspace[]> {
    const response = await this.client.get<WorkspacesResponse>('/team');
    return response.data.teams;
  }

  async getWorkspaceMembers(teamId?: string): Promise<WorkspaceMember[]> {
    const id = teamId || this.config.workspaceId;
    // Members are embedded in the /team response, not a separate endpoint
    const response = await this.client.get<WorkspacesResponse>('/team');
    const workspace = response.data.teams.find((t) => t.id === id);
    return workspace?.members || [];
  }

  // ============================================
  // SPACE METHODS
  // ============================================

  async getSpaces(teamId?: string): Promise<Space[]> {
    const id = teamId || this.config.workspaceId;
    const response = await this.client.get<SpacesResponse>(`/team/${id}/space`);
    return response.data.spaces;
  }

  async getSpace(spaceId: string): Promise<Space> {
    const response = await this.client.get<Space>(`/space/${spaceId}`);
    return response.data;
  }

  // ============================================
  // FOLDER METHODS
  // ============================================

  async getFolders(spaceId: string): Promise<Folder[]> {
    const response = await this.client.get<FoldersResponse>(
      `/space/${spaceId}/folder`
    );
    return response.data.folders;
  }

  // ============================================
  // LIST METHODS
  // ============================================

  async getLists(folderId: string): Promise<List[]> {
    const response = await this.client.get<ListsResponse>(
      `/folder/${folderId}/list`
    );
    return response.data.lists;
  }

  async getFolderlessLists(spaceId: string): Promise<List[]> {
    const response = await this.client.get<ListsResponse>(
      `/space/${spaceId}/list`
    );
    return response.data.lists;
  }

  async getList(listId: string): Promise<List> {
    const response = await this.client.get<List>(`/list/${listId}`);
    return response.data;
  }

  // ============================================
  // TASK METHODS
  // ============================================

  async getTask(taskId: string, includeSubtasks = false): Promise<Task> {
    const params = new URLSearchParams();
    if (includeSubtasks) {
      params.set('include_subtasks', 'true');
    }
    const response = await this.client.get<Task>(
      `/task/${taskId}?${params.toString()}`
    );
    return response.data;
  }

  async getTasks(
    listId: string,
    options: {
      statuses?: string[];
      assignees?: string[];
      includeClosed?: boolean;
      subtasks?: boolean;
      page?: number;
    } = {}
  ): Promise<Task[]> {
    const params = new URLSearchParams();

    if (options.statuses?.length) {
      options.statuses.forEach((s) => params.append('statuses[]', s));
    }
    if (options.assignees?.length) {
      options.assignees.forEach((a) => params.append('assignees[]', a));
    }
    if (options.includeClosed) {
      params.set('include_closed', 'true');
    }
    if (options.subtasks) {
      params.set('subtasks', 'true');
    }
    if (options.page) {
      params.set('page', options.page.toString());
    }

    const response = await this.client.get<TasksResponse>(
      `/list/${listId}/task?${params.toString()}`
    );
    return response.data.tasks;
  }

  async searchTasks(
    teamId: string,
    query: string,
    options: {
      statuses?: string[];
      assignees?: string[];
      listIds?: string[];
      spaceIds?: string[];
      includeClosed?: boolean;
      includeSubtasks?: boolean;
      page?: number;
    } = {}
  ): Promise<Task[]> {
    const params = new URLSearchParams();

    if (query) {
      params.set('query', query);
    }
    if (options.statuses?.length) {
      options.statuses.forEach((s) => params.append('statuses[]', s));
    }
    if (options.assignees?.length) {
      options.assignees.forEach((a) => params.append('assignees[]', a));
    }
    if (options.listIds?.length) {
      options.listIds.forEach((id) => params.append('list_ids[]', id));
    }
    if (options.spaceIds?.length) {
      options.spaceIds.forEach((id) => params.append('space_ids[]', id));
    }
    if (options.includeClosed) {
      params.set('include_closed', 'true');
    }
    if (options.includeSubtasks) {
      params.set('include_subtasks', 'true');
    }
    if (options.page) {
      params.set('page', options.page.toString());
    }

    // Note: ClickUp doesn't have a direct search endpoint for all tasks
    // We'll use the filtered tasks endpoint instead
    const response = await this.client.get<TasksResponse>(
      `/team/${teamId}/task?${params.toString()}`
    );
    return response.data.tasks;
  }

  async createTask(
    listId: string,
    data: {
      name: string;
      description?: string;
      status?: string;
      priority?: number;
      assignees?: number[];
      due_date?: number;
      start_date?: number;
      time_estimate?: number;
      parent?: string;
      tags?: string[];
    }
  ): Promise<Task> {
    const response = await this.client.post<Task>(`/list/${listId}/task`, data);
    return response.data;
  }

  async updateTask(
    taskId: string,
    data: {
      name?: string;
      description?: string;
      status?: string;
      priority?: number | null;
      assignees?: { add?: number[]; rem?: number[] };
      due_date?: number | null;
      start_date?: number | null;
      time_estimate?: number | null;
      parent?: string | null;
    }
  ): Promise<Task> {
    const response = await this.client.put<Task>(`/task/${taskId}`, data);
    return response.data;
  }

  async deleteTask(taskId: string): Promise<void> {
    await this.client.delete(`/task/${taskId}`);
  }

  // ============================================
  // COMMENT METHODS
  // ============================================

  async getTaskComments(taskId: string): Promise<Comment[]> {
    const response = await this.client.get<CommentsResponse>(
      `/task/${taskId}/comment`
    );
    return response.data.comments;
  }

  async createComment(
    taskId: string,
    commentText: string,
    notifyAll = false
  ): Promise<Comment> {
    const response = await this.client.post<Comment>(`/task/${taskId}/comment`, {
      comment_text: commentText,
      notify_all: notifyAll,
    });
    return response.data;
  }

  // ============================================
  // TIME ENTRY METHODS
  // ============================================

  async getTimeEntries(
    teamId: string,
    options: {
      startDate?: number;
      endDate?: number;
      assignee?: string;
    } = {}
  ): Promise<TimeEntry[]> {
    const params = new URLSearchParams();

    if (options.startDate) {
      params.set('start_date', options.startDate.toString());
    }
    if (options.endDate) {
      params.set('end_date', options.endDate.toString());
    }
    if (options.assignee) {
      params.set('assignee', options.assignee);
    }

    const response = await this.client.get<TimeEntriesResponse>(
      `/team/${teamId}/time_entries?${params.toString()}`
    );
    return response.data.data;
  }

  async getTaskTimeEntries(
    taskId: string,
    teamId: string
  ): Promise<TimeEntry[]> {
    // Get time entries and filter by task
    const entries = await this.getTimeEntries(teamId);
    return entries.filter((e) => e.task?.id === taskId);
  }

  async getTimeEntry(
    teamId: string,
    timerId: string
  ): Promise<TimeEntry> {
    const response = await this.client.get<{ data: TimeEntry }>(
      `/team/${teamId}/time_entries/${timerId}`
    );
    return response.data.data;
  }

  async createTimeEntry(
    teamId: string,
    data: TimeEntryCreate
  ): Promise<TimeEntry> {
    const response = await this.client.post<{ data: TimeEntry }>(
      `/team/${teamId}/time_entries`,
      data
    );
    return response.data.data;
  }

  async updateTimeEntry(
    teamId: string,
    timerId: string,
    data: TimeEntryUpdate
  ): Promise<TimeEntry> {
    const response = await this.client.put<{ data: TimeEntry }>(
      `/team/${teamId}/time_entries/${timerId}`,
      data
    );
    return response.data.data;
  }

  async deleteTimeEntry(teamId: string, timerId: string): Promise<void> {
    await this.client.delete(`/team/${teamId}/time_entries/${timerId}`);
  }

  // ============================================
  // RUNNING TIMER METHODS
  // ============================================

  async getCurrentTimer(teamId: string): Promise<TimeEntry | null> {
    const response = await this.client.get<{ data: TimeEntry | null }>(
      `/team/${teamId}/time_entries/current`
    );
    return response.data.data;
  }

  async startTimer(
    teamId: string,
    taskId: string,
    description?: string
  ): Promise<TimeEntry> {
    const response = await this.client.post<{ data: TimeEntry }>(
      `/team/${teamId}/time_entries/start`,
      {
        tid: taskId,
        description,
      }
    );
    return response.data.data;
  }

  async stopTimer(teamId: string): Promise<TimeEntry> {
    const response = await this.client.post<{ data: TimeEntry }>(
      `/team/${teamId}/time_entries/stop`
    );
    return response.data.data;
  }

  // ============================================
  // HELPER METHODS
  // ============================================

  /**
   * Resolve a task ID - handles both regular IDs and custom IDs (like TCG-1234)
   */
  async resolveTaskId(taskIdOrCustomId: string): Promise<string> {
    // If it looks like a custom ID (contains letters and numbers with hyphen)
    if (/^[A-Z]+-\d+$/i.test(taskIdOrCustomId)) {
      // Search for the task by custom ID
      const tasks = await this.searchTasks(
        this.config.workspaceId,
        taskIdOrCustomId,
        { includeClosed: true }
      );

      const task = tasks.find(
        (t) => t.custom_id?.toLowerCase() === taskIdOrCustomId.toLowerCase()
      );

      if (!task) {
        throw new Error(`Task with custom ID "${taskIdOrCustomId}" not found`);
      }
      return task.id;
    }

    // Assume it's a regular task ID
    return taskIdOrCustomId;
  }

  /**
   * Find a list by name
   */
  async findListByName(name: string): Promise<List | null> {
    const spaces = await this.getSpaces();

    for (const space of spaces) {
      // Check folderless lists
      const folderlessLists = await this.getFolderlessLists(space.id);
      const found = folderlessLists.find(
        (l) => l.name.toLowerCase() === name.toLowerCase()
      );
      if (found) return found;

      // Check lists in folders
      const folders = await this.getFolders(space.id);
      for (const folder of folders) {
        const lists = await this.getLists(folder.id);
        const foundInFolder = lists.find(
          (l) => l.name.toLowerCase() === name.toLowerCase()
        );
        if (foundInFolder) return foundInFolder;
      }
    }

    return null;
  }

  /**
   * Find a member by name or email
   */
  async findMember(nameOrEmail: string): Promise<WorkspaceMember | null> {
    const members = await this.getWorkspaceMembers();
    const search = nameOrEmail.toLowerCase();

    return (
      members.find(
        (m) =>
          (m.user.username?.toLowerCase().includes(search) ?? false) ||
          (m.user.email?.toLowerCase().includes(search) ?? false)
      ) || null
    );
  }
}

// Singleton instance
let clientInstance: ClickUpClient | null = null;

export function getClient(config?: ClickUpConfig): ClickUpClient {
  if (!clientInstance && !config) {
    throw new Error('ClickUp client not initialized. Provide config on first call.');
  }
  if (config) {
    clientInstance = new ClickUpClient(config);
  }
  return clientInstance!;
}

export function initClient(config: ClickUpConfig): ClickUpClient {
  clientInstance = new ClickUpClient(config);
  return clientInstance;
}
