// ClickUp API Types

export interface ClickUpConfig {
  apiToken: string;
  workspaceId: string;
  teamId?: string;
  userId?: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  color?: string;
  profilePicture?: string | null;
  initials?: string;
}

export interface Status {
  id?: string;
  status: string;
  color: string;
  orderindex?: number;
  type?: string;
}

export interface Priority {
  id?: string;
  priority: string;
  color: string;
  orderindex?: string;
}

export interface Task {
  id: string;
  custom_id?: string;
  name: string;
  description?: string;
  text_content?: string;
  status: Status;
  priority?: Priority | null;
  creator: User;
  assignees: User[];
  due_date?: string | null;
  start_date?: string | null;
  time_estimate?: number | null;
  time_spent?: number;
  date_created: string;
  date_updated: string;
  date_closed?: string | null;
  parent?: string | null;
  url: string;
  list?: {
    id: string;
    name: string;
  };
  folder?: {
    id: string;
    name: string;
  };
  space?: {
    id: string;
  };
  subtasks?: Task[];
  tags?: Tag[];
  custom_fields?: CustomField[];
  attachments?: Attachment[];
}

export interface Tag {
  name: string;
  tag_fg: string;
  tag_bg: string;
}

export interface CustomField {
  id: string;
  name: string;
  type: string;
  value?: unknown;
}

export interface Attachment {
  id: string;
  title: string;
  url: string;
  mimetype: string;
  date: string;
}

export interface Comment {
  id: string;
  comment_text: string;
  user: User;
  date: string;
  resolved?: boolean;
}

export interface TimeEntry {
  id: string;
  task?: {
    id: string;
    name: string;
    status?: Status;
    custom_id?: string;
  };
  user: User;
  start: string;
  end?: string;
  duration: string;
  duration_ms?: string;
  description?: string;
  billable: boolean;
  tags?: Tag[];
}

export interface TimeEntryCreate {
  tid?: string;
  description?: string;
  start: number;
  end?: number;
  duration?: number;
  billable?: boolean;
  assignee?: number;
  tags?: string[];
}

export interface TimeEntryUpdate {
  description?: string;
  start?: number;
  end?: number;
  duration?: number;
  billable?: boolean;
  tags?: string[];
}

export interface Space {
  id: string;
  name: string;
  private: boolean;
  statuses: Status[];
  features?: Record<string, unknown>;
}

export interface Folder {
  id: string;
  name: string;
  hidden: boolean;
  space: { id: string };
  lists?: List[];
}

export interface List {
  id: string;
  name: string;
  folder?: { id: string; name: string };
  space?: { id: string };
  status?: Status;
}

export interface Workspace {
  id: string;
  name: string;
  color: string;
  avatar?: string;
  members: WorkspaceMember[];
}

export interface WorkspaceMember {
  user: User;
  role: number;
}

// API Response types
export interface TasksResponse {
  tasks: Task[];
}

export interface TimeEntriesResponse {
  data: TimeEntry[];
}

export interface CommentsResponse {
  comments: Comment[];
}

export interface SpacesResponse {
  spaces: Space[];
}

export interface FoldersResponse {
  folders: Folder[];
}

export interface ListsResponse {
  lists: List[];
}

export interface WorkspacesResponse {
  teams: Workspace[];
}

export interface MembersResponse {
  members: WorkspaceMember[];
}

// Search/Filter types
export interface TaskSearchOptions {
  query?: string;
  statuses?: string[];
  assignees?: string[];
  listId?: string;
  spaceId?: string;
  includeSubtasks?: boolean;
  includeClosed?: boolean;
  page?: number;
}

export interface TimeEntryListOptions {
  taskId?: string;
  startDate?: Date;
  endDate?: Date;
  assignee?: string;
}

// CLI Output types
export interface TaskSummary {
  id: string;
  customId?: string;
  name: string;
  status: string;
  priority?: string;
  assignee?: string;
  dueDate?: string;
  timeTracked?: string;
  timeEstimate?: string;
  url: string;
}

export interface TimeEntrySummary {
  id: string;
  taskId?: string;
  taskName?: string;
  date: string;
  startTime: string;
  endTime?: string;
  duration: string;
  description?: string;
}

export interface WeeklyReportEntry {
  date: string;
  dayOfWeek: string;
  totalHours: number;
  entries: TimeEntrySummary[];
}

export interface WeeklyReport {
  weekStart: string;
  weekEnd: string;
  totalHours: number;
  dailyBreakdown: WeeklyReportEntry[];
  taskBreakdown: {
    taskId: string;
    taskName: string;
    totalHours: number;
  }[];
}
