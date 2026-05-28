import fs from 'fs/promises';
import { resolve } from 'path';
import fetch from 'node-fetch';
import dotenv from 'dotenv';

dotenv.config();

export class WeeekClient {
    constructor(token = process.env.WEEEK_API_KEY, apiUrl = 'https://api.weeek.net/public/v1') {
        if (!token) {
            throw new Error('WEEEK_API_KEY is required');
        }
        this.token = token;
        this.apiUrl = apiUrl;
    }

    async request(method, path, body = null, params = null) {
        const normalizedPath = path.startsWith('/') ? path : `/${path}`;
        let url = `${this.apiUrl}${normalizedPath}`;

        if (params) {
            const validParams = {};
            Object.keys(params).forEach(key => {
                if (params[key] !== null && params[key] !== undefined) {
                    validParams[key] = params[key];
                }
            });
            const query = new URLSearchParams(validParams).toString();
            if (query) url += `?${query}`;
        }

        const fetchOptions = {
            method: method.toUpperCase(),
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };

        if (body) {
            fetchOptions.body = JSON.stringify(body);
        }

        const response = await fetch(url, fetchOptions);

        if (!response.ok) {
            const text = await response.text();
            throw new Error(`${response.status} ${response.statusText}: ${text}`);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        return await response.text();
    }

    // --- Projects & Boards ---

    async getProjects() {
        const data = await this.request('GET', 'tm/projects');
        return data.projects || [];
    }

    async getBoards(projectId = null) {
        if (projectId) {
            const data = await this.request('GET', 'tm/boards', null, { projectId });
            return data.boards || [];
        }

        // If no projectId, fetch all boards from all projects (heavy operation)
        const projects = await this.getProjects();
        const promises = projects.map(async p => {
            try {
                const boards = await this.getBoards(p.id);
                return boards.map(b => ({ ...b, projectName: p.name }));
            } catch {
                return [];
            }
        });
        const results = await Promise.all(promises);
        return results.flat();
    }

    async findBoard(query) {
        const boards = await this.getBoards();
        const queryLower = query.toLowerCase();
        const exact = boards.find(b => b.name.toLowerCase() === queryLower);
        if (exact) return [exact];
        return boards.filter(b => b.name.toLowerCase().includes(queryLower));
    }

    async findColumn(boardId, query) {
        const columns = await this.getColumns(boardId);
        const queryLower = query.toLowerCase();
        return columns.find(c => c.name.toLowerCase().includes(queryLower));
    }

    async getColumns(boardId) {
        const data = await this.request('GET', 'tm/board-columns', null, { boardId });
        return data.boardColumns || [];
    }

    async getBoardWithContext(boardName) {
        const matches = await this.findBoard(boardName);
        if (matches.length === 0) throw new Error(`Board "${boardName}" not found.`);
        if (matches.length > 1) {
            const names = matches.map(m => `"${m.name}" (ID: ${m.id})`).join(', ');
            throw new Error(`Multiple boards found: ${names}. Please be more specific.`);
        }

        const board = matches[0];
        const [columns, tasks] = await Promise.all([
            this.getColumns(board.id),
            this.getTasks({ boardId: board.id })
        ]);

        return {
            ...board,
            columns,
            tasks
        };
    }

    // --- Tasks ---

    async getTasks(params = {}) {
        const data = await this.request('GET', 'tm/tasks', null, params);
        return data.tasks || [];
    }

    async getTask(taskId) {
        const res = await this.request('GET', `tm/tasks/${taskId}`);
        return res.task || res;
    }

    async createTaskDetailed({ title, boardName, columnName, assigneeName, priority, description, subtasks = [] }) {
        let boardId, boardColumnId, assigneeId, projectId;

        if (boardName) {
            const board = await this.getBoardWithContext(boardName);
            boardId = board.id;
            projectId = board.projectId;

            if (columnName) {
                const col = board.columns.find(c => c.name.toLowerCase().includes(columnName.toLowerCase()));
                if (!col) throw new Error(`Column "${columnName}" not found on board "${boardName}".`);
                boardColumnId = col.id;
            } else if (board.columns.length > 0) {
                boardColumnId = board.columns[0].id;
            }
        }

        if (assigneeName) {
            const user = await this.findUser(assigneeName);
            if (!user) throw new Error(`User "${assigneeName}" not found.`);
            assigneeId = user.id;
        }

        const mainTask = await this.createTask({
            title,
            description: description || '',
            priority: priority !== undefined ? parseInt(priority) : 0,
            projectId,
            boardId,
            boardColumnId,
            assignees: assigneeId ? [assigneeId] : []
        });

        if (subtasks && subtasks.length > 0) {
            for (const stTitle of subtasks) {
                await this.createTask({
                    title: stTitle,
                    parentId: mainTask.id,
                    projectId,
                    boardId,
                    boardColumnId,
                    assignees: assigneeId ? [assigneeId] : []
                });
            }
        }

        return mainTask;
    }

    async createTask(data) {
        // data: { title, description, priority, boardId, boardColumnId, assignees, type, parentId }
        const payload = {
            type: 'action',
            ...data
        };

        // Handle locations format if boardId is provided
        if (data.boardId) {
            payload.locations = [{
                projectId: data.projectId || 0, // We might need to resolve projectId too if not provided
                boardId: data.boardId,
                boardColumnId: data.boardColumnId
            }];
            // The API might expect specific format for locations vs top-level IDs
        }

        const res = await this.request('POST', 'tm/tasks', payload);
        return res.task || res;
    }

    async updateTask(taskId, data) {
        const res = await this.request('PUT', `tm/tasks/${taskId}`, data);
        return res.task || res;
    }

    async moveTaskToColumn(taskId, columnName) {
        const task = await this.getTask(taskId);
        if (!task) throw new Error('Task not found');
        if (!task.boardId) throw new Error('Task is not assigned to a board');

        const col = await this.findColumn(task.boardId, columnName);
        if (!col) throw new Error(`Column "${columnName}" not found on board.`);

        return await this.moveTask(taskId, col.id);
    }

    async moveTask(taskId, boardColumnId) {
        return await this.request('POST', `tm/tasks/${taskId}/board-column`, { boardColumnId });
    }

    // --- Users ---

    async getUsers() {
        const data = await this.request('GET', 'ws/members');
        return (data.members || []).map(u => ({
            id: u.id,
            name: [u.firstName, u.lastName].filter(Boolean).join(' ') || u.email,
            email: u.email,
            raw: u
        }));
    }

    async findUser(query) {
        const users = await this.getUsers();
        const queryLower = query.toLowerCase();
        return users.find(u =>
            u.name.toLowerCase().includes(queryLower) ||
            u.email.toLowerCase().includes(queryLower)
        );
    }

    // --- Timer ---

    async startTimer(taskId) {
        return await this.request('POST', `tm/tasks/${taskId}/start-timer`);
    }

    async stopTimer(taskId) {
        return await this.request('POST', `tm/tasks/${taskId}/stop-timer`);
    }

    async getHelp() {
        try {
            // Correct way to get directory name in ESM on Node.js
            const __dirname = new URL('.', import.meta.url).pathname;
            const skillPath = resolve(__dirname, 'SKILL.md');

            // Fix for Windows paths starting with /C:/...
            const fixedPath = (process.platform === 'win32' && skillPath.startsWith('/'))
                ? skillPath.substring(1)
                : skillPath;

            return await fs.readFile(fixedPath, 'utf8');
        } catch (err) {
            // Fallback for CLI and other environments
            try {
                return await fs.readFile(resolve(process.cwd(), 'SKILL.md'), 'utf8');
            } catch (err2) {
                return "Help documentation (SKILL.md) not found.";
            }
        }
    }

    static stripHtml(html) {
        if (!html) return '';
        return html
            .replace(/<[^>]*>?/gm, '')
            .replace(/&nbsp;/g, ' ')
            .replace(/&quot;/g, '"')
            .trim();
    }
}
