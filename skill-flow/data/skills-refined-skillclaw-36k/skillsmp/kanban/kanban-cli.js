#!/usr/bin/env node
/**
 * Code Kanban CLI - 任务管理命令行工具
 *
 * Usage:
 *   node kanban-cli.js [command] [options]
 *
 * Commands:
 *   (none)           显示当前项目状态
 *   list             列出所有任务
 *   add <title>      创建新任务
 *   edit <id>        编辑任务 (更新任务内容)
 *   done <id>        标记任务完成
 *   start <id>       开始任务 (in_progress)
 *   move <id>        移动任务 (改状态/优先级/worktree)
 *   delete <id>      删除任务
 *   show <id>        显示任务详情
 *   projects         列出所有项目
 *   worktree <id>    为任务创建 worktree
 *   import <file>    从 JSON 文件批量导入任务
 *   export           导出 AI 友好的任务上下文
 *
 * Options (add/edit):
 *   --priority=<n>       优先级 (0=P0紧急, 1=P1高, 2=P2中, 3=P3低)
 *   --description=<text> 任务描述 (支持 \n 换行)
 *   --tags=<t1,t2>       标签 (逗号分隔)
 *   --due=<date>         截止日期 (ISO 8601, 如 2025-01-20)
 *
 * Options (move):
 *   --status=<s>         状态 (todo/in_progress/done/blocked)
 *   --priority=<n>       优先级
 *   --worktree=<id>      绑定 Worktree ID (空字符串解绑)
 *   --order=<n>          排序索引
 *
 * Options (list):
 *   --status=<s>     过滤状态
 *   --priority=<n>   过滤优先级
 *
 * Global Options:
 *   --project=<id>   指定项目 ID
 *   --json           JSON 输出
 *   --verbose, -v    显示完整详情
 *   --base-url=<url> API 基础 URL
 */

const BASE_URL = process.env.KANBAN_URL || "http://127.0.0.1:3007";
const API = `${BASE_URL}/api/v1`;

// ============================================================
// HTTP 客户端
// ============================================================

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

async function postJson(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }
  return response.json();
}

async function putJson(url, data) {
  const response = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`HTTP ${response.status}: ${text}`);
  }
  return response.json();
}

async function deleteRequest(url) {
  const response = await fetch(url, { method: "DELETE" });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// ============================================================
// 项目操作
// ============================================================

async function detectProject() {
  const cwd = process.cwd();
  const data = await fetchJson(`${API}/projects`);

  for (const project of data.items || []) {
    if (project.path === cwd || cwd.startsWith(project.path + "/")) {
      return project;
    }
  }

  return null;
}

async function listProjects() {
  const data = await fetchJson(`${API}/projects`);
  return data.items || [];
}

// ============================================================
// 任务操作
// ============================================================

async function listTasks(projectId, options = {}) {
  const data = await fetchJson(`${API}/projects/${projectId}/tasks`);
  let tasks = data.items || [];

  if (options.status) {
    tasks = tasks.filter((t) => t.status === options.status);
  }

  if (options.priority !== undefined) {
    tasks = tasks.filter((t) => t.priority === options.priority);
  }

  return tasks.sort((a, b) => a.priority - b.priority);
}

async function createTask(projectId, title, options = {}) {
  return postJson(`${API}/projects/${projectId}/tasks/create`, {
    title,
    description: options.description || "",
    status: "todo",
    priority: options.priority ?? 2,
    tags: options.tags || [],
    dueDate: options.dueDate || null,
    worktreeId: options.worktreeId || null,
  });
}

async function updateTask(taskId, updates) {
  return postJson(`${API}/tasks/${taskId}/update`, updates);
}

async function moveTask(taskId, moveData) {
  return postJson(`${API}/tasks/${taskId}/move`, moveData);
}

async function deleteTask(taskId) {
  return postJson(`${API}/tasks/${taskId}/delete`, {});
}

async function resolveTaskId(shortId, projectId) {
  // 如果已经是完整 ID (16位)，直接返回
  if (shortId.length >= 16) return shortId;

  // 否则从项目任务列表中前缀匹配
  const data = await fetchJson(`${API}/projects/${projectId}/tasks`);
  const tasks = data.items || [];
  const matches = tasks.filter(t => t.id.startsWith(shortId));

  if (matches.length === 0) {
    throw new Error(`No task found with ID prefix: ${shortId}`);
  }
  if (matches.length > 1) {
    throw new Error(`Ambiguous ID prefix: ${shortId} (${matches.length} matches)`);
  }
  return matches[0].id;
}

async function getTask(taskId) {
  const data = await fetchJson(`${API}/tasks/${taskId}`);
  return data.item || data;
}

// ============================================================
// Worktree 操作
// ============================================================

async function createWorktree(projectId, branchName) {
  return postJson(`${API}/projects/${projectId}/worktrees/create`, {
    branchName,
  });
}

async function bindWorktree(taskId, worktreeId) {
  return putJson(`${API}/tasks/${taskId}/bind-worktree`, {
    worktreeId,
  });
}

// ============================================================
// 显示格式化
// ============================================================

const PRIORITY_LABELS = ["P0", "P1", "P2", "P3"];
const STATUS_ICONS = {
  todo: "○",
  in_progress: "◐",
  done: "●",
};

function formatTask(task, verbose = false) {
  const icon = STATUS_ICONS[task.status] || "?";
  const priority = PRIORITY_LABELS[task.priority] || `P${task.priority}`;
  const line = `${icon} [${priority}] ${task.title}`;

  if (verbose) {
    const parts = [line, `   ID: ${task.id}`, `   Status: ${task.status}`];
    if (task.description) {
      parts.push(`   Description:\n${task.description.split('\n').map(l => '     ' + l).join('\n')}`);
    }
    if (task.tags?.length > 0) {
      parts.push(`   Tags: ${task.tags.join(', ')}`);
    }
    return parts.join('\n');
  }

  return `${line} (${task.id.slice(0, 8)})`;
}

function formatProjectStatus(project, tasks) {
  const todo = tasks.filter((t) => t.status === "todo").length;
  const inProgress = tasks.filter((t) => t.status === "in_progress").length;
  const done = tasks.filter((t) => t.status === "done").length;

  const lines = [];
  lines.push(`\n📁 ${project.name}`);
  lines.push(`   Path: ${project.path}`);
  lines.push(`   Branch: ${project.defaultBranch}`);
  lines.push(`\n📊 Tasks: ${todo} todo, ${inProgress} in progress, ${done} done`);

  if (inProgress > 0) {
    lines.push("\n🔄 In Progress:");
    tasks
      .filter((t) => t.status === "in_progress")
      .forEach((t) => lines.push(`   ${formatTask(t)}`));
  }

  const p0Tasks = tasks.filter((t) => t.status === "todo" && t.priority === 0);
  if (p0Tasks.length > 0) {
    lines.push("\n🔴 P0 Tasks:");
    p0Tasks.forEach((t) => lines.push(`   ${formatTask(t)}`));
  }

  return lines.join("\n");
}

// ============================================================
// 命令处理
// ============================================================

async function cmdStatus(options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }

  const tasks = await listTasks(project.id);

  if (options.json) {
    console.log(JSON.stringify({ project, tasks }, null, 2));
  } else {
    console.log(formatProjectStatus(project, tasks));
  }
}

async function cmdList(options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found");
    process.exit(1);
  }

  const tasks = await listTasks(project.id, options);

  if (options.json) {
    console.log(JSON.stringify(tasks, null, 2));
  } else {
    if (tasks.length === 0) {
      console.log("No tasks found");
      return;
    }

    const grouped = {
      todo: tasks.filter((t) => t.status === "todo"),
      in_progress: tasks.filter((t) => t.status === "in_progress"),
      done: tasks.filter((t) => t.status === "done"),
    };

    if (grouped.in_progress.length > 0) {
      console.log("\n◐ In Progress:");
      grouped.in_progress.forEach((t) => console.log(`  ${formatTask(t, options.verbose)}`));
    }

    if (grouped.todo.length > 0) {
      console.log("\n○ Todo:");
      grouped.todo.forEach((t) => console.log(`  ${formatTask(t, options.verbose)}`));
    }

    if (grouped.done.length > 0) {
      console.log("\n● Done:");
      grouped.done.forEach((t) => console.log(`  ${formatTask(t, options.verbose)}`));
    }
  }
}

async function cmdAdd(title, options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found");
    process.exit(1);
  }

  const result = await createTask(project.id, title, options);
  const taskId = result.item?.id || result.id;
  console.log(`Created: ${taskId}`);

  // 显示创建的任务详情
  const details = [];
  if (options.priority !== undefined) details.push(`P${options.priority}`);
  if (options.tags?.length > 0) details.push(`tags: ${options.tags.join(', ')}`);
  if (options.description) details.push(`desc: ${options.description.slice(0, 50)}${options.description.length > 50 ? '...' : ''}`);
  if (details.length > 0) {
    console.log(`  ${details.join(' | ')}`);
  }
}

async function cmdDone(shortId) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }
  const taskId = await resolveTaskId(shortId, project.id);
  await moveTask(taskId, { status: "done" });
  console.log(`Marked as done: ${taskId}`);
}

async function cmdStart(shortId) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }
  const taskId = await resolveTaskId(shortId, project.id);
  await moveTask(taskId, { status: "in_progress" });
  console.log(`Started: ${taskId}`);
}

async function cmdMove(shortId, options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }
  const taskId = await resolveTaskId(shortId, project.id);

  // moveTask 使用 /move API: status, orderIndex, worktreeId
  const moveData = {};
  if (options.status) moveData.status = options.status;
  if (options.orderIndex !== undefined) moveData.orderIndex = options.orderIndex;
  if (options.worktreeId !== undefined) moveData.worktreeId = options.worktreeId;

  // priority 需要用 /update API
  if (options.priority !== undefined) {
    await updateTask(taskId, { priority: options.priority });
  }

  if (Object.keys(moveData).length === 0 && options.priority === undefined) {
    console.error("Usage: kanban move <id> --status=<s> or --priority=<n> or --worktree=<id>");
    process.exit(1);
  }

  if (Object.keys(moveData).length > 0) {
    await moveTask(taskId, moveData);
  }

  const parts = [];
  if (moveData.status) parts.push(`status → ${moveData.status}`);
  if (options.priority !== undefined) parts.push(`priority → P${options.priority}`);
  if (moveData.worktreeId !== undefined) parts.push(`worktree → ${moveData.worktreeId || "(unbound)"}`);
  if (moveData.orderIndex !== undefined) parts.push(`order → ${moveData.orderIndex}`);
  console.log(`Moved ${taskId}: ${parts.join(", ")}`);
}

async function cmdEdit(shortId, options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }
  const taskId = await resolveTaskId(shortId, project.id);

  const updates = {};
  if (options.args.length > 0) updates.title = options.args.join(" ");
  if (options.description !== undefined) updates.description = options.description;
  if (options.priority !== undefined) updates.priority = options.priority;
  if (options.tags !== undefined) updates.tags = options.tags;
  if (options.dueDate !== undefined) updates.dueDate = options.dueDate || null;

  if (Object.keys(updates).length === 0) {
    console.error("Usage: kanban edit <id> [new title] --description=<text> --priority=<n> --tags=<t1,t2> --due=<date>");
    process.exit(1);
  }

  await updateTask(taskId, updates);
  const parts = Object.keys(updates).map(k => k);
  console.log(`Updated ${taskId}: ${parts.join(", ")}`);
}

async function cmdDelete(shortId) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }
  const taskId = await resolveTaskId(shortId, project.id);
  await deleteTask(taskId);
  console.log(`Deleted: ${taskId}`);
}

async function cmdShow(shortId, options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found for current directory");
    process.exit(1);
  }
  const taskId = await resolveTaskId(shortId, project.id);
  const task = await getTask(taskId);

  if (options.json) {
    console.log(JSON.stringify(task, null, 2));
  } else {
    console.log(`\nTask: ${task.title}`);
    console.log(`ID: ${task.id}`);
    console.log(`Status: ${task.status}`);
    console.log(`Priority: P${task.priority}`);
    if (task.description) {
      console.log(`\nDescription:\n${task.description}`);
    }
    if (task.tags?.length > 0) {
      console.log(`\nTags: ${task.tags.join(", ")}`);
    }
  }
}

async function cmdProjects(options) {
  const projects = await listProjects();

  if (options.json) {
    console.log(JSON.stringify(projects, null, 2));
  } else {
    console.log("\nProjects:\n");
    for (const p of projects) {
      console.log(`  ${p.id}: ${p.name}`);
      console.log(`     ${p.path}\n`);
    }
  }
}

async function cmdWorktree(taskId) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found");
    process.exit(1);
  }

  const task = await getTask(taskId);
  const branchName = `task/${taskId.slice(0, 8)}`;

  console.log(`Creating worktree: ${branchName}`);
  const worktree = await createWorktree(project.id, branchName);
  const worktreeId = worktree.item?.id || worktree.id;

  console.log(`Binding to task: ${task.title}`);
  await bindWorktree(taskId, worktreeId);

  console.log(`Marking as in_progress`);
  await updateTask(taskId, { status: "in_progress" });

  console.log(`\nWorktree created and bound!`);
  console.log(`Branch: ${branchName}`);
}

async function cmdImport(filePath) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found");
    process.exit(1);
  }

  const fs = await import("fs");
  const content = fs.readFileSync(filePath, "utf-8");
  const tasks = JSON.parse(content);

  console.log(`Importing ${tasks.length} tasks...`);

  for (const task of tasks) {
    const result = await createTask(project.id, task.title, {
      priority: task.priority ?? 2,
      description: task.description || "",
      tags: task.tags || [],
    });
    console.log(`  Created: ${task.title}`);
  }

  console.log(`\nDone! Imported ${tasks.length} tasks.`);
}

async function cmdExport(options) {
  const project = await detectProject();
  if (!project) {
    console.error("No project found");
    process.exit(1);
  }

  const tasks = await listTasks(project.id);
  const format = options.format || "context";

  if (format === "json") {
    console.log(JSON.stringify({ project, tasks }, null, 2));
    return;
  }

  // AI-friendly context format
  const lines = [];
  lines.push(`# ${project.name} - 任务上下文`);
  lines.push(`\n> 路径: ${project.path}`);
  lines.push(`> 分支: ${project.defaultBranch}`);
  lines.push(`> 生成时间: ${new Date().toISOString()}`);

  // Summary
  const todo = tasks.filter(t => t.status === "todo");
  const inProgress = tasks.filter(t => t.status === "in_progress");
  const done = tasks.filter(t => t.status === "done");

  lines.push(`\n## 概览`);
  lines.push(`- 待办: ${todo.length}`);
  lines.push(`- 进行中: ${inProgress.length}`);
  lines.push(`- 已完成: ${done.length}`);

  // In Progress (highest priority for AI)
  if (inProgress.length > 0) {
    lines.push(`\n## 🔄 进行中 (优先处理)`);
    for (const t of inProgress) {
      lines.push(`\n### ${t.title}`);
      lines.push(`- ID: \`${t.id}\``);
      lines.push(`- 优先级: P${t.priority}`);
      if (t.dueDate) lines.push(`- 截止: ${t.dueDate.split("T")[0]}`);
      if (t.description) {
        lines.push(`\n${t.description}`);
      }
    }
  }

  // P0 Todo
  const p0 = todo.filter(t => t.priority === 0);
  if (p0.length > 0) {
    lines.push(`\n## 🔴 P0 待办 (紧急)`);
    for (const t of p0) {
      lines.push(`\n### ${t.title}`);
      lines.push(`- ID: \`${t.id}\``);
      if (t.dueDate) lines.push(`- 截止: ${t.dueDate.split("T")[0]}`);
      if (t.description) {
        lines.push(`\n${t.description}`);
      }
    }
  }

  // P1 Todo
  const p1 = todo.filter(t => t.priority === 1);
  if (p1.length > 0) {
    lines.push(`\n## 🟠 P1 待办 (高优先级)`);
    for (const t of p1) {
      lines.push(`\n### ${t.title}`);
      lines.push(`- ID: \`${t.id}\``);
      if (t.dueDate) lines.push(`- 截止: ${t.dueDate.split("T")[0]}`);
      if (t.description) {
        // Truncate long descriptions for context
        const desc = t.description.length > 500
          ? t.description.slice(0, 500) + "\n...(truncated)"
          : t.description;
        lines.push(`\n${desc}`);
      }
    }
  }

  // P2+ Todo (brief)
  const pLow = todo.filter(t => t.priority >= 2);
  if (pLow.length > 0) {
    lines.push(`\n## 🟡 P2+ 待办 (可延后)`);
    for (const t of pLow) {
      lines.push(`- [P${t.priority}] ${t.title} (\`${t.id.slice(0,8)}\`)`);
    }
  }

  // Recent Done (for context)
  if (done.length > 0) {
    lines.push(`\n## ✅ 最近完成 (参考)`);
    const recentDone = done.slice(0, 3);
    for (const t of recentDone) {
      lines.push(`\n### ${t.title}`);
      if (t.description) {
        // Only show summary for done tasks
        const summary = t.description.split("\n").slice(0, 10).join("\n");
        lines.push(`\n${summary}`);
        if (t.description.split("\n").length > 10) {
          lines.push("...(truncated)");
        }
      }
    }
  }

  // Instructions for AI
  lines.push(`\n---`);
  lines.push(`\n## AI 工作指南`);
  lines.push(`1. 优先处理"进行中"任务`);
  lines.push(`2. P0 任务必须尽快完成`);
  lines.push(`3. 每个任务包含验收标准，完成后逐项确认`);
  lines.push(`4. 完成任务后执行: \`/kanban done <task-id>\``);
  lines.push(`5. 开始新任务前执行: \`/kanban start <task-id>\``);

  console.log(lines.join("\n"));
}

async function cmdBatchUpdate(filePath) {
  const fs = await import("fs");
  const content = fs.readFileSync(filePath, "utf-8");
  const tasks = JSON.parse(content);

  console.log(`Updating ${tasks.length} tasks...`);

  let updated = 0;
  let skipped = 0;

  for (const task of tasks) {
    if (!task.id) {
      console.log(`  Skipped (no id): ${task.title}`);
      skipped++;
      continue;
    }

    try {
      const updates = {};
      if (task.title) updates.title = task.title;
      if (task.description !== undefined) updates.description = task.description;
      if (task.priority !== undefined) updates.priority = task.priority;
      if (task.tags) updates.tags = task.tags;
      if (task.dueDate !== undefined) updates.dueDate = task.dueDate;
      // Note: branchName is set via worktree binding, not direct update
      // Note: status uses move API, not update API

      await updateTask(task.id, updates);
      console.log(`  Updated: ${task.title || task.id}`);
      updated++;
    } catch (err) {
      console.log(`  Failed: ${task.title} - ${err.message}`);
      skipped++;
    }
  }

  console.log(`\nDone! Updated: ${updated}, Skipped: ${skipped}`);
}

// ============================================================
// Main
// ============================================================

function parseArgs(args) {
  const options = {
    command: null,
    args: [],
    // add/edit options
    priority: undefined,
    description: undefined,
    tags: undefined,
    dueDate: undefined,
    // move options
    status: undefined,
    worktreeId: undefined,
    orderIndex: undefined,
    // global options
    projectId: null,
    json: false,
    verbose: false,
    format: "context",
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg.startsWith("--priority=")) {
      options.priority = parseInt(arg.slice(11), 10);
    } else if (arg.startsWith("--status=")) {
      options.status = arg.slice(9);
    } else if (arg.startsWith("--description=")) {
      // 支持 \n 换行符
      options.description = arg.slice(14).replace(/\\n/g, "\n");
    } else if (arg.startsWith("--tags=")) {
      options.tags = arg.slice(7).split(",").map(t => t.trim()).filter(Boolean);
    } else if (arg.startsWith("--due=")) {
      options.dueDate = arg.slice(6);
    } else if (arg.startsWith("--worktree=")) {
      options.worktreeId = arg.slice(11);
    } else if (arg.startsWith("--order=")) {
      options.orderIndex = parseInt(arg.slice(8), 10);
    } else if (arg.startsWith("--project=")) {
      options.projectId = arg.slice(10);
    } else if (arg.startsWith("--format=")) {
      options.format = arg.slice(9);
    } else if (arg === "--json") {
      options.json = true;
      options.format = "json";
    } else if (arg === "--verbose" || arg === "-v") {
      options.verbose = true;
    } else if (!arg.startsWith("-")) {
      if (!options.command) {
        options.command = arg;
      } else {
        options.args.push(arg);
      }
    }
  }

  return options;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));

  try {
    switch (options.command) {
      case null:
      case "status":
        await cmdStatus(options);
        break;

      case "list":
      case "ls":
        await cmdList(options);
        break;

      case "add":
      case "create":
        if (options.args.length === 0) {
          console.error("Usage: kanban add <title>");
          process.exit(1);
        }
        await cmdAdd(options.args.join(" "), options);
        break;

      case "done":
      case "complete":
        if (options.args.length === 0) {
          console.error("Usage: kanban done <task-id>");
          process.exit(1);
        }
        await cmdDone(options.args[0]);
        break;

      case "start":
        if (options.args.length === 0) {
          console.error("Usage: kanban start <task-id>");
          process.exit(1);
        }
        await cmdStart(options.args[0]);
        break;

      case "move":
        if (options.args.length === 0) {
          console.error("Usage: kanban move <task-id> --status=<s> or --priority=<n> or --worktree=<id>");
          process.exit(1);
        }
        await cmdMove(options.args[0], options);
        break;

      case "edit":
        if (options.args.length === 0) {
          console.error("Usage: kanban edit <task-id> [new title] --description=<text> --priority=<n> --tags=<t1,t2> --due=<date>");
          process.exit(1);
        }
        await cmdEdit(options.args[0], { ...options, args: options.args.slice(1) });
        break;

      case "delete":
      case "rm":
        if (options.args.length === 0) {
          console.error("Usage: kanban delete <task-id>");
          process.exit(1);
        }
        await cmdDelete(options.args[0]);
        break;

      case "show":
        if (options.args.length === 0) {
          console.error("Usage: kanban show <task-id>");
          process.exit(1);
        }
        await cmdShow(options.args[0], options);
        break;

      case "projects":
        await cmdProjects(options);
        break;

      case "worktree":
      case "wt":
        if (options.args.length === 0) {
          console.error("Usage: kanban worktree <task-id>");
          process.exit(1);
        }
        await cmdWorktree(options.args[0]);
        break;

      case "import":
        if (options.args.length === 0) {
          console.error("Usage: kanban import <file.json>");
          process.exit(1);
        }
        await cmdImport(options.args[0]);
        break;

      case "update":
      case "batch-update":
        if (options.args.length === 0) {
          console.error("Usage: kanban update <file.json>");
          process.exit(1);
        }
        await cmdBatchUpdate(options.args[0]);
        break;

      case "export":
      case "context":
        await cmdExport(options);
        break;

      default:
        console.error(`Unknown command: ${options.command}`);
        console.error("\nCommands: list, add, done, start, delete, show, projects, worktree, import, update, export");
        process.exit(1);
    }
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  }
}

main();
