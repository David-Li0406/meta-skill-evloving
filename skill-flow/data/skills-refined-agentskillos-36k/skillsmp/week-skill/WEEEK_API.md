# Weeek API Documentation

This document provides a concise overview of the Weeek API endpoints for Tags, Projects, Boards, Board Columns, Tasks, and Attachments, extracted from the OpenAPI specification.

## Authentication
Authentication is handled via Bearer Token in the `Authorization` header.
- **Base URL:** `https://api.weeek.net/public/v1`

---

## 1. Tags API
Manage workspace tags used for categorizing tasks and other resources.

- **GET `/ws/tags`**: List all tags in the workspace.
- **POST `/ws/tags`**: Create a new tag.
    - *Body*: `{"title": "Tag Name"}`
- **GET `/ws/tags/{id}`**: Get details of a specific tag.
- **PUT `/ws/tags/{id}`**: Update an existing tag's title or color.
- **DELETE `/ws/tags/{id}`**: Permanently delete a tag.

**Tag Object Snippet:**
```json
{
  "id": 1,
  "title": "Backend",
  "color": "#aaaaaa"
}
```

---

## 2. Project API
Manage projects within a workspace.

- **GET `/tm/projects`**: List all projects.
- **POST `/tm/projects`**: Create a new project.
    - *Body*: `{"name": "Project Name", "isPrivate": false, "description": "...", "portfolioId": 1}`
- **GET `/tm/projects/{id}`**: Get project details.
- **PUT `/tm/projects/{id}`**: Update project information (name, logo, description, color, etc.).
- **DELETE `/tm/projects/{id}`**: Delete a project.
- **POST `/tm/projects/{id}/archive`**: Archive a project.
- **POST `/tm/projects/{id}/un-archive`**: Restore an archived project.

---

## 3. Board API
Manage boards within projects.

- **GET `/tm/boards`**: List boards. Use query parameter `projectId` to filter.
- **POST `/tm/boards`**: Create a new board in a project.
    - *Body*: `{"name": "Board Name", "projectId": 1, "isPrivate": false}`
- **GET `/tm/boards/{id}`**: Get board details.
- **PUT `/tm/boards/{id}`**: Update board name or privacy status.
- **DELETE `/tm/boards/{id}`**: Delete a board.
- **POST `/tm/boards/{id}/archive`**: Archive a board.
- **POST `/tm/boards/{id}/un-archive`**: Restore an archived board.

---

## 4. Board Column API
Manage columns (statuses) within a board.

- **GET `/tm/board-columns`**: List columns for a board. Use `boardId` query param.
- **POST `/tm/board-columns`**: Create a new column on a board.
    - *Body*: `{"name": "Status Name", "boardId": 1}`
- **GET `/tm/board-columns/{id}`**: Get column details.
- **PUT `/tm/board-columns/{id}`**: Update column name.
- **DELETE `/tm/board-columns/{id}`**: Delete a column.
- **POST `/tm/board-columns/{id}/move`**: Change the position of a column.

---

## 5. Task API
The core of task management in Weeek.

- **GET `/tm/tasks`**: List tasks with extensive filtering (project, board, status, assignee, tags, etc.).
- **POST `/tm/tasks`**: Create a new task.
- **GET `/tm/tasks/{id}`**: Get full task details, including custom fields and attachments.
- **PUT `/tm/tasks/{id}`**: Update task properties (title, description, dates, priority, etc.).
- **DELETE `/tm/tasks/{id}`**: Delete a task.
- **POST `/tm/tasks/{id}/complete`**: Mark task as completed.
- **POST `/tm/tasks/{id}/un-complete`**: Reopen a completed task.
- **POST `/tm/tasks/{id}/board`**: Move task to a different board.
- **POST `/tm/tasks/{id}/board-column`**: Move task to a different column (status).
- **POST `/tm/tasks/{id}/start-timer`**: Start the time tracker for this task.
- **POST `/tm/tasks/{id}/stop-timer`**: Stop the time tracker.

---

## 6. Attachments
Attachments are specifically associated with Tasks. There are no standalone attachment endpoints; they are managed through task-specific paths.

### Endpoints
- **POST `/tm/tasks/{task_id}/attachments`**: Upload one or more files to a task.
    - **Request Format:** `multipart/form-data`
    - **Header:** `Content-Type: multipart/form-data`
    - **Field:** `files[]` (The binary file data)
    - **Constraints:** Max file size is 100MB.

### Attachment Data Model
When retrieving a task via `GET /tm/tasks/{id}`, attachments are returned in an array with the following structure:

| Property | Type | Description |
| :--- | :--- | :--- |
| `id` | `uuid` | Unique identifier for the attachment. |
| `creatorId` | `uuid` | ID of the user who uploaded the attachment. |
| `service` | `enum` | The storage service (`weeek`, `google_drive`, `dropbox`, `one_drive`, `box`). |
| `name` | `string` | The original name of the file. |
| `url` | `uri` | URL to access the file. Weeek-hosted files URLs are valid for 1 hour. |
| `size` | `integer` | File size in bytes (only provided for `weeek` service). |
| `createdAt` | `datetime` | ISO 8601 timestamp of when the file was attached. |

---
