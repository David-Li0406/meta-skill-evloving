#!/usr/bin/env node
/**
 * Kanban 批量处理 - 依赖分析和执行计划生成
 *
 * Usage:
 *   node kanban-planner.js [options]
 *
 * Options:
 *   --project=<id>    指定项目 ID
 *   --priority=<n>    只处理特定优先级 (0-3)
 *   --dry-run         只生成计划，不输出执行命令
 *   --max=<n>         最大并行数 (默认 3)
 *   --json            输出 JSON 格式
 *   --detect          检测当前目录对应的项目
 *   --base-url=<url>  API 基础 URL (默认 http://127.0.0.1:3007)
 */

// ============================================================
// 配置
// ============================================================

const DEFAULT_MAX_PARALLEL = 3;
const DEFAULT_BASE_URL = "http://127.0.0.1:3007";

// 依赖解析正则
const DEP_PATTERNS = [
  /blocked\s+by[:\s]+\[([a-zA-Z0-9]+)\]/gi,
  /depends\s+on[:\s]+\[([a-zA-Z0-9]+)\]/gi,
  /after[:\s]+\[([a-zA-Z0-9]+)\]/gi,
  /requires[:\s]+\[([a-zA-Z0-9]+)\]/gi,
];

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

// ============================================================
// 项目检测
// ============================================================

async function detectProject(baseUrl) {
  const cwd = process.cwd();
  const projects = await fetchJson(`${baseUrl}/api/v1/projects`);

  for (const project of projects.items || []) {
    if (project.path === cwd || cwd.startsWith(project.path + "/")) {
      return project;
    }
  }

  return null;
}

async function getProjectById(baseUrl, projectId) {
  const data = await fetchJson(`${baseUrl}/api/v1/projects/${projectId}`);
  return data.item || data;
}

// ============================================================
// 任务获取
// ============================================================

async function fetchTasks(baseUrl, projectId, priorityFilter) {
  const data = await fetchJson(`${baseUrl}/api/v1/projects/${projectId}/tasks`);
  let tasks = data.items || [];

  // 只获取 todo 状态的任务
  tasks = tasks.filter((t) => t.status === "todo");

  // 优先级过滤
  if (priorityFilter !== null && priorityFilter !== undefined) {
    tasks = tasks.filter((t) => t.priority === priorityFilter);
  }

  return tasks;
}

// ============================================================
// 依赖解析
// ============================================================

function parseDependencies(taskDescription) {
  if (!taskDescription) return [];

  const deps = new Set();

  for (const pattern of DEP_PATTERNS) {
    let match;
    pattern.lastIndex = 0;
    while ((match = pattern.exec(taskDescription)) !== null) {
      deps.add(match[1]);
    }
  }

  return Array.from(deps);
}

// ============================================================
// 依赖图构建
// ============================================================

function buildDependencyGraph(tasks) {
  const graph = new Map();
  const taskIds = new Set(tasks.map((t) => t.id));

  for (const task of tasks) {
    const deps = parseDependencies(task.description).filter((d) => taskIds.has(d));

    graph.set(task.id, {
      task,
      deps,
      priority: task.priority,
      dependents: [],
    });
  }

  // 填充 dependents
  for (const [id, node] of graph) {
    for (const dep of node.deps) {
      const depNode = graph.get(dep);
      if (depNode) {
        depNode.dependents.push(id);
      }
    }
  }

  return graph;
}

// ============================================================
// 拓扑排序 + 分层
// ============================================================

function topologicalSort(graph) {
  const waves = [];
  const completed = new Set();
  const remaining = new Set(graph.keys());

  while (remaining.size > 0) {
    const ready = [];
    for (const id of remaining) {
      const node = graph.get(id);
      const allDepsCompleted = node.deps.every((d) => completed.has(d));
      if (allDepsCompleted) {
        ready.push(id);
      }
    }

    if (ready.length === 0) {
      console.error("Circular dependency detected! Remaining tasks:", Array.from(remaining));
      break;
    }

    // 按优先级排序
    ready.sort((a, b) => {
      const pa = graph.get(a).priority;
      const pb = graph.get(b).priority;
      return pa - pb;
    });

    waves.push(ready);

    for (const id of ready) {
      completed.add(id);
      remaining.delete(id);
    }
  }

  return waves;
}

// ============================================================
// 执行计划生成
// ============================================================

function generatePlan(project, graph, waves, maxParallel) {
  const plan = {
    project: {
      id: project.id,
      name: project.name,
      path: project.path,
    },
    summary: {
      totalTasks: graph.size,
      totalWaves: waves.length,
      maxParallel,
    },
    waves: [],
  };

  for (let i = 0; i < waves.length; i++) {
    const taskIds = waves[i];
    const waveTasks = taskIds.map((id) => {
      const node = graph.get(id);
      return {
        id,
        title: node.task.title,
        priority: node.priority,
        deps: node.deps,
        description: node.task.description,
      };
    });

    plan.waves.push({
      level: i,
      tasks: waveTasks,
      parallel: taskIds.length > 1,
      maxParallel: Math.min(taskIds.length, maxParallel),
    });
  }

  return plan;
}

// ============================================================
// 输出格式化
// ============================================================

function formatPlanAsMarkdown(plan) {
  const lines = [];

  lines.push("# Kanban 批量执行计划\n");
  lines.push(`**项目**: ${plan.project.name}`);
  lines.push(`**路径**: ${plan.project.path}\n`);
  lines.push(`- 总任务: ${plan.summary.totalTasks}`);
  lines.push(`- 执行波次: ${plan.summary.totalWaves}`);
  lines.push(`- 最大并行: ${plan.summary.maxParallel}\n`);

  for (const wave of plan.waves) {
    const parallelNote = wave.parallel ? `(并行, 最多 ${wave.maxParallel} 个)` : "(顺序)";
    lines.push(`## Wave ${wave.level} ${parallelNote}\n`);

    for (const task of wave.tasks) {
      const depsNote = task.deps.length > 0 ? ` [deps: ${task.deps.join(", ")}]` : "";
      const priorityNote = `(P${task.priority})`;
      lines.push(`- [ ] **${task.title}** ${priorityNote}${depsNote}`);
      lines.push(`  - ID: \`${task.id}\``);
    }

    lines.push("");
  }

  return lines.join("\n");
}

function formatExecutionCommands(plan, baseUrl) {
  const lines = [];

  lines.push("# 执行命令\n");

  for (const wave of plan.waves) {
    lines.push(`## Wave ${wave.level}\n`);

    if (wave.parallel && wave.tasks.length > 1) {
      lines.push("```");
      lines.push("# 使用 Claude Task 工具并行执行以下任务:");
      for (const task of wave.tasks) {
        lines.push(`# - ${task.title} (${task.id})`);
      }
      lines.push("```\n");
    } else {
      for (const task of wave.tasks) {
        lines.push(`### ${task.title}\n`);
        lines.push("```");
        lines.push(`# Task ID: ${task.id}`);
        lines.push(`# Priority: P${task.priority}`);
        if (task.description) {
          lines.push(`# Description: ${task.description.slice(0, 100)}...`);
        }
        lines.push("```\n");
      }
    }
  }

  lines.push("## 状态更新命令\n");
  lines.push("```bash");
  lines.push("# 标记任务为完成");
  lines.push(`curl -X PUT ${baseUrl}/api/v1/tasks/{TASK_ID}/update \\`);
  lines.push('  -H "Content-Type: application/json" \\');
  lines.push("  -d '{\"status\": \"done\"}'");
  lines.push("```");

  return lines.join("\n");
}

// ============================================================
// Main
// ============================================================

function parseArgs(args) {
  const options = {
    projectId: null,
    priority: null,
    dryRun: false,
    maxParallel: DEFAULT_MAX_PARALLEL,
    json: false,
    detect: false,
    baseUrl: DEFAULT_BASE_URL,
  };

  for (const arg of args) {
    if (arg.startsWith("--project=")) {
      options.projectId = arg.slice(10);
    } else if (arg.startsWith("--priority=")) {
      options.priority = parseInt(arg.slice(11), 10);
    } else if (arg === "--dry-run") {
      options.dryRun = true;
    } else if (arg.startsWith("--max=")) {
      options.maxParallel = parseInt(arg.slice(6), 10) || DEFAULT_MAX_PARALLEL;
    } else if (arg === "--json") {
      options.json = true;
    } else if (arg === "--detect") {
      options.detect = true;
    } else if (arg.startsWith("--base-url=")) {
      options.baseUrl = arg.slice(11);
    }
  }

  return options;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));

  // 检测项目
  let project;
  if (options.projectId) {
    project = await getProjectById(options.baseUrl, options.projectId);
  } else {
    console.error("Detecting project from current directory...");
    project = await detectProject(options.baseUrl);
  }

  if (!project) {
    console.error("No project found. Use --project=<id> to specify.");
    console.error("\nAvailable projects:");
    const projects = await fetchJson(`${options.baseUrl}/api/v1/projects`);
    for (const p of projects.items || []) {
      console.error(`  ${p.id}: ${p.name} (${p.path})`);
    }
    process.exit(1);
  }

  if (options.detect) {
    console.log(JSON.stringify(project, null, 2));
    return;
  }

  console.error(`Project: ${project.name} (${project.id})`);
  console.error(`Fetching tasks${options.priority !== null ? ` with priority: P${options.priority}` : ""}...`);

  const tasks = await fetchTasks(options.baseUrl, project.id, options.priority);

  if (tasks.length === 0) {
    console.error("No todo tasks found.");
    process.exit(0);
  }

  console.error(`Found ${tasks.length} todo tasks.`);

  const graph = buildDependencyGraph(tasks);
  const waves = topologicalSort(graph);
  const plan = generatePlan(project, graph, waves, options.maxParallel);

  if (options.json) {
    console.log(JSON.stringify(plan, null, 2));
  } else {
    console.log(formatPlanAsMarkdown(plan));
    if (!options.dryRun) {
      console.log("\n---\n");
      console.log(formatExecutionCommands(plan, options.baseUrl));
    }
  }
}

main().catch((err) => {
  console.error("Error:", err.message);
  process.exit(1);
});
