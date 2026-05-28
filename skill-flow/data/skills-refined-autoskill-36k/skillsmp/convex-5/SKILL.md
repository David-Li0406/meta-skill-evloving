---
name: convex
description: Use when working with Convex - the reactive backend database platform. This skill covers TypeScript-based database queries, mutations, actions, authentication, file storage, real-time subscriptions, and React/Next.js integration.
---

# Convex - 响应式后端数据库平台

Convex 是一个开源的响应式数据库平台，查询即 TypeScript 代码，直接在数据库中运行。就像 React 组件响应状态变化一样，Convex 查询响应数据库变化。

## 核心特性

- **TypeScript 查询**：数据库查询就是 TypeScript 函数，无需 SQL
- **自动响应式**：数据变化自动更新客户端订阅
- **文档-关系型数据库**：存储 JSON 文档，支持表关系
- **端到端类型安全**：从数据库到客户端的完整类型推断
- **事务保证**：ACID 兼容，可序列化隔离
- **实时更新**：WebSocket 连接自动同步数据
- **服务器函数**：Query、Mutation、Action 三种函数类型
- **内置认证**：支持多种认证提供商
- **文件存储**：内置文件上传和存储
- **全文搜索**：原生支持搜索功能
- **定时任务**：支持 Scheduler 和 Cron Jobs

## 系统要求

- Node.js 18.x 或更高版本
- npm、yarn 或 pnpm
- TypeScript 支持

---

## 项目初始化

### 创建新项目

```bash
# 使用 npm
npm create convex@latest

# 使用 pnpm
pnpm create convex@latest

# 使用 yarn
yarn create convex
```

### 添加到现有项目

```bash
# 安装 Convex
npm install convex

# 初始化 Convex
npx convex dev
```

### 项目结构

```
.
├── convex/
│   ├── _generated/          # 自动生成的类型定义
│   │   ├── api.d.ts
│   │   ├── api.js
│   │   ├── dataModel.d.ts
│   │   └── server.d.ts
│   ├── schema.ts            # 数据库 Schema 定义
│   ├── tasks.ts             # 示例：任务相关函数
│   ├── users.ts             # 示例：用户相关函数
│   └── http.ts              # HTTP Actions
├── src/
│   └── main.tsx             # 客户端代码
├── convex.json              # Convex 配置
└── package.json
```

---

## 开发工作流

### 启动开发服务器

```bash
npx convex dev
```

开发服务器功能：

- 监听 `convex/` 目录文件变化
- 自动推送代码到云端
- 生成类型定义到 `_generated/`
- 提供实时同步

### 部署到生产环境

```bash
# 部署到生产环境
npx convex deploy

# 查看部署状态
npx convex status

# 查看日志
npx convex logs
```

---

## 数据库基础

### 表（Tables）

表在插入第一个文档时自动创建，无需预先定义：

```typescript
// friends 表不存在
await ctx.db.insert("friends", { name: "Jamie" });
// 现在表存在了，包含一个文档
```

### 文档（Documents）

文档类似 JavaScript 对象，可以嵌套数组和对象：

```typescript
// 有效的文档示例
{}
{ "name": "Jamie" }
{
  "name": { "first": "Ari", "last": "Cole" },
  "age": 60
}
```

### Schema 定义

在 `convex/schema.ts` 中定义数据结构：

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    completed: v.boolean(),
    userId: v.id("users"),
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_completed", ["completed"]),

  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatar: v.optional(v.string()),
  }).index("by_email", ["email"]),
});
```

### 数据类型

Convex 支持的值类型：

```typescript
import { v } from "convex/values";

// 基础类型
v.null();
v.boolean();
v.number(); // 包括 NaN, Infinity
v.bigint(); // BigInt
v.string();
v.bytes(); // ArrayBuffer

// 特殊类型
v.id("tableName"); // 文档 ID 引用

// 复合类型
v.array(v.string());
v.object({
  name: v.string(),
  age: v.number(),
});

// 可选类型
v.optional(v.string());

// 联合类型
v.union(
  v.object({ type: v.literal("text"), content: v.string() }),
  v.object({ type: v.literal("image"), url: v.string() }),
);

// 任意类型（不推荐）
v.any();
```

---

## 函数类型

Convex 提供三种服务器函数类型：

| 类型     | 数据库访问 | 事务性 | 缓存 | 实时更新 | 外部 API 调用 |
| -------- | ---------- | ------ | ---- | -------- | ------------- |
| Query    | 只读       | 是     | 是   | 是       | 否            |
| Mutation | 读写       | 是     | 否   | 否       | 否            |
| Action   | 通过调用   | 否     | 否   | 否       | 是            |

### Query Functions（查询函数）

只读函数，自动缓存和订阅：

```typescript
// convex/tasks.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getAllTasks = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect();
  },
});

export const getTasksByUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .collect();
  },
});

export const getCompletedTasks = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_completed", (q) => q.eq("completed", true))
      .order("desc")
      .collect();
  },
});
```

### Mutation Functions（变更函数）

读写事务函数：

```typescript
// convex/tasks.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
    userId: v.id("users"),
  },
  handler: async (ctx, args) => {
    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description,
      completed: false,
      userId: args.userId,
      createdAt: Date.now(),
    });
    return taskId;
  },
});

export const updateTask = mutation({
  args: {
    taskId: v.id("tasks"),
    title: v.optional(v.string()),
    completed: v.optional(v.boolean()),
  },
  handler: async (ctx, args) => {
    const { taskId, ...updates } = args;
    await ctx.db.patch(taskId, updates);
  },
});

export const deleteTask = mutation({
  args: { taskId: v.id("tasks") },
  handler: async (ctx, args) => {
    await ctx.db.delete(args.taskId);
  },
});
```

### Action Functions（行动函数）

可以调用外部 API 的函数：

```typescript
// convex/actions.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { api } from "./_generated/api";

export const sendEmail = action({
  args: {
    to: v.string(),
    subject: v.string(),
    body: v.string(),
  },
  handler: async (ctx, args) => {
    // 调用外部邮件服务
    await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.SENDGRID_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: args.to }] }],
        from: { email: "noreply@example.com" },
        subject: args.subject,
        content: [{ type: "text/plain", value: args.body }],
      }),
    });
  },
});

export const generateAIResponse = action({
  args: { prompt: v.string() },
  handler: async (ctx, args) => {
    // 调用 OpenAI API
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: [{ role: "user", content: args.prompt }],
      }),
    });

    const data = await response.json();

    // 在 Action 中调用 Mutation 保存结果
    await ctx.runMutation(api.messages.create, {
      content: data.choices[0].message.content,
    });

    return data.choices[0].message.content;
  },
});
```

---

## 数据库操作

### 读取数据

```typescript
// 获取所有文档
const allTasks = await ctx.db.query("tasks").collect();

// 使用索引查询
const userTasks = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .collect();

// 范围查询
const recentTasks = await ctx.db
  .query("tasks")
  .withIndex("by_createdAt", (q) =>
    q.gt("createdAt", Date.now() - 24 * 60 * 60 * 1000),
  )
  .collect();

// 排序
const sortedTasks = await ctx.db.query("tasks").order("desc").collect();

// 限制结果数量
const firstTen = await ctx.db.query("tasks").take(10);

// 获取第一个结果
const firstTask = await ctx.db.query("tasks").first();

// 获取唯一结果
const uniqueTask = await ctx.db
  .query("tasks")
  .withIndex("by_email", (q) => q.eq("email", "user@example.com"))
  .unique();

// 通过 ID 获取
const task = await ctx.db.get(taskId);
```

### 写入数据

```typescript
// 插入文档
const taskId = await ctx.db.insert("tasks", {
  title: "New Task",
  completed: false,
  userId: userId,
  createdAt: Date.now(),
});

// 更新文档（部分更新）
await ctx.db.patch(taskId, {
  completed: true,
});

// 替换文档（完整替换）
await ctx.db.replace(taskId, {
  title: "Updated Task",
  completed: true,
  userId: userId,
  createdAt: Date.now(),
});

// 删除文档
await ctx.db.delete(taskId);
```

### 分页查询

```typescript
import { paginationOptsValidator } from "convex/server";

export const listTasks = query({
  args: { paginationOpts: paginationOptsValidator },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

### 索引

在 Schema 中定义索引：

```typescript
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    userId: v.id("users"),
    completed: v.boolean(),
    createdAt: v.number(),
  })
    // 单字段索引
    .index("by_user", ["userId"])
    .index("by_completed", ["completed"])

    // 复合索引
    .index("by_user_completed", ["userId", "completed"])
    .index("by_user_created", ["userId", "createdAt"]),
});
```

使用索引查询：

```typescript
// 使用复合索引
const completedUserTasks = await ctx.db
  .query("tasks")
  .withIndex("by_user_completed", (q) =>
    q.eq("userId", userId).eq("completed", true),
  )
  .collect();
```

---

## React 客户端集成

### 设置 Convex Provider

```tsx
// src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import App from "./App";

const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ConvexProvider client={convex}>
      <App />
    </ConvexProvider>
  </React.StrictMode>,
);
```

### 使用 Hooks

```tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function TaskList() {
  // 查询数据（自动订阅）
  const tasks = useQuery(api.tasks.getAllTasks);

  // 变更函数
  const createTask = useMutation(api.tasks.createTask);
  const updateTask = useMutation(api.tasks.updateTask);
  const deleteTask = useMutation(api.tasks.deleteTask);

  if (tasks === undefined) {
    return <div>Loading...</div>;
  }

  const handleCreate = async () => {
    await createTask({
      title: "New Task",
      userId: currentUserId,
    });
  };

  const handleToggle = async (taskId: Id<"tasks">) => {
    const task = tasks.find((t) => t._id === taskId);
    await updateTask({
      taskId,
      completed: !task.completed,
    });
  };

  return (
    <div>
      <button onClick={handleCreate}>Add Task</button>
      <ul>
        {tasks.map((task) => (
          <li key={task._id}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => handleToggle(task._id)}
            />
            {task.title}
            <button onClick={() => deleteTask({ taskId: task._id })}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 带参数的查询

```tsx
function UserTasks({ userId }: { userId: Id<"users"> }) {
  const tasks = useQuery(api.tasks.getTasksByUser, { userId });

  // 条件查询（userId 为 null 时不查询）
  const conditionalTasks = useQuery(
    api.tasks.getTasksByUser,
    userId ? { userId } : "skip",
  );

  return <div>{/* ... */}</div>;
}
```

### 分页查询

```tsx
import { usePaginatedQuery } from "convex/react";

function PaginatedTaskList() {
  const { results, status, loadMore } = usePaginatedQuery(
    api.tasks.listTasks,
    {},
    { initialNumItems: 10 },
  );

  return (
    <div>
      {results.map((task) => (
        <div key={task._id}>{task.title}</div>
      ))}
      <button onClick={() => loadMore(10)} disabled={status !== "CanLoadMore"}>
        Load More
      </button>
    </div>
  );
}
```

### 使用 Action

```tsx
import { useAction } from "convex/react";

function AIChat() {
  const generateResponse = useAction(api.actions.generateAIResponse);
  const [response, setResponse] = useState("");

  const handleSubmit = async (prompt: string) => {
    const result = await generateResponse({ prompt });
    setResponse(result);
  };

  return <div>{/* ... */}</div>;
}
```

---

## Next.js 集成

### App Router (推荐)

```tsx
// app/providers.tsx
"use client";

import { ConvexProvider, ConvexReactClient } from "convex/react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function ConvexClientProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

```tsx
// app/layout.tsx
import { ConvexClientProvider } from "./providers";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ConvexClientProvider>{children}</ConvexClientProvider>
      </body>
    </html>
  );
}
```

### Server Components

```tsx
// app/tasks/page.tsx
import { fetchQuery } from "convex/nextjs";
import { api } from "../../convex/_generated/api";

export default async function TasksPage() {
  const tasks = await fetchQuery(api.tasks.getAllTasks);

  return (
    <div>
      {tasks.map((task) => (
        <div key={task._id}>{task.title}</div>
      ))}
    </div>
  );
}
```

### Server Actions

```tsx
// app/tasks/actions.ts
"use server";

import { fetchMutation } from "convex/nextjs";
import { api } from "../../convex/_generated/api";

export async function createTask(formData: FormData) {
  const title = formData.get("title") as string;

  await fetchMutation(api.tasks.createTask, {
    title,
    userId: getCurrentUserId(),
  });
}
```

---

## 认证（Authentication）

### 使用 Clerk

```bash
npm install @clerk/nextjs
```

```tsx
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";
import { ConvexProviderWithClerk } from "convex/react-clerk";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider
      publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY!}
    >
      <ConvexProviderWithClerk client={convex}>
        {children}
      </ConvexProviderWithClerk>
    </ClerkProvider>
  );
}
```

在函数中获取认证信息：

```typescript
// convex/tasks.ts
export const createTask = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();

    if (!identity) {
      throw new Error("Unauthenticated");
    }

    const userId = identity.subject;

    await ctx.db.insert("tasks", {
      title: args.title,
      userId,
      completed: false,
      createdAt: Date.now(),
    });
  },
});
```

### 使用 Auth0

```bash
npm install @auth0/nextjs-auth0
```

配置类似 Clerk，使用 `ConvexProviderWithAuth0`。

---

## 文件存储

### 上传文件

```typescript
// convex/files.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const generateUploadUrl = mutation({
  args: {},
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});

export const saveFile = mutation({
  args: {
    storageId: v.string(),
    fileName: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.insert("files", {
      storageId: args.storageId,
      fileName: args.fileName,
      uploadedAt: Date.now(),
    });
  },
});
```

客户端上传：

```tsx
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

function FileUpload() {
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);
  const saveFile = useMutation(api.files.saveFile);

  const handleUpload = async (file: File) => {
    // 1. 获取上传 URL
    const uploadUrl = await generateUploadUrl();

    // 2. 上传文件
    const result = await fetch(uploadUrl, {
      method: "POST",
      headers: { "Content-Type": file.type },
      body: file,
    });

    const { storageId } = await result.json();

    // 3. 保存文件信息
    await saveFile({
      storageId,
      fileName: file.name,
    });
  };

  return (
    <input
      type="file"
      onChange={(e) => {
        const file = e.target.files?.[0];
        if (file) handleUpload(file);
      }}
    />
  );
}
```

### 获取文件 URL

```typescript
export const getFileUrl = query({
  args: { storageId: v.string() },
  handler: async (ctx, args) => {
    return await ctx.storage.getUrl(args.storageId);
  },
});
```

---

## 搜索功能

### 定义搜索索引

```typescript
// convex/schema.ts
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    description: v.string(),
    userId: v.id("users"),
  })
    .searchIndex("search_title", {
      searchField: "title",
      filterFields: ["userId"],
    })
    .searchIndex("search_description", {
      searchField: "description",
    }),
});
```

### 执行搜索

```typescript
export const searchTasks = query({
  args: {
    query: v.string(),
    userId: v.optional(v.id("users")),
  },
  handler: async (ctx, args) => {
    const results = await ctx.db
      .query("tasks")
      .withSearchIndex("search_title", (q) => {
        let search = q.search("title", args.query);
        if (args.userId) {
          search = search.eq("userId", args.userId);
        }
        return search;
      })
      .collect();

    return results;
  },
});
```

---

## 定时任务

### Scheduler（一次性定时任务）

```typescript
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const scheduleTask = mutation({
  args: {
    taskId: v.id("tasks"),
    delayMs: v.number(),
  },
  handler: async (ctx, args) => {
    await ctx.scheduler.runAfter(args.delayMs, api.tasks.deleteTask, {
      taskId: args.taskId,
    });
  },
});

// 在特定时间执行
export const scheduleTaskAt = mutation({
  args: {
    taskId: v.id("tasks"),
    runAt: v.number(), // timestamp
  },
  handler: async (ctx, args) => {
    await ctx.scheduler.runAt(args.runAt, api.tasks.deleteTask, {
      taskId: args.taskId,
    });
  },
});
```

### Cron Jobs（定期任务）

```typescript
// convex/crons.ts
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();

crons.interval(
  "清理过期任务",
  { minutes: 60 }, // 每小时执行一次
  internal.tasks.cleanupExpiredTasks,
);

crons.daily(
  "每日报告",
  { hourUTC: 9, minuteUTC: 0 }, // 每天 9:00 UTC
  internal.reports.generateDailyReport,
);

crons.weekly(
  "周报",
  { hourUTC: 9, minuteUTC: 0, dayOfWeek: "monday" },
  internal.reports.generateWeeklyReport,
);

crons.monthly(
  "月报",
  { hourUTC: 9, minuteUTC: 0, day: 1 },
  internal.reports.generateMonthlyReport,
);

export default crons;
```

---

## HTTP Actions

### 定义 HTTP Endpoint

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { api } from "./_generated/api";

const http = httpRouter();

http.route({
  path: "/webhook",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const body = await request.json();

    // 处理 webhook
    await ctx.runMutation(api.webhooks.processWebhook, {
      data: body,
    });

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }),
});

http.route({
  path: "/api/tasks",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    const tasks = await ctx.runQuery(api.tasks.getAllTasks);

    return new Response(JSON.stringify(tasks), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }),
});

export default http;
```

访问：`https://your-deployment.convex.site/webhook`

---

## 内部函数（Internal Functions）

内部函数只能从其他 Convex 函数调用，不能从客户端调用：

```typescript
// convex/internal.ts
import { internalMutation, internalQuery } from "./_generated/server";
import { v } from "convex/values";

export const cleanupExpiredTasks = internalMutation({
  args: {},
  handler: async (ctx) => {
    const expiredTasks = await ctx.db
      .query("tasks")
      .filter((q) => q.lt(q.field("expiresAt"), Date.now()))
      .collect();

    for (const task of expiredTasks) {
      await ctx.db.delete(task._id);
    }
  },
});

export const getInternalStats = internalQuery({
  args: {},
  handler: async (ctx) => {
    const taskCount = await ctx.db
      .query("tasks")
      .collect()
      .then((t) => t.length);
    const userCount = await ctx.db
      .query("users")
      .collect()
      .then((u) => u.length);

    return { taskCount, userCount };
  },
});
```

从其他函数调用：

```typescript
import { internal } from "./_generated/api";

export const triggerCleanup = mutation({
  args: {},
  handler: async (ctx) => {
    await ctx.runMutation(internal.internal.cleanupExpiredTasks, {});
  },
});
```

---

## 错误处理

### 抛出错误

```typescript
export const createTask = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();

    if (!identity) {
      throw new Error("未认证");
    }

    if (args.title.length === 0) {
      throw new Error("标题不能为空");
    }

    if (args.title.length > 100) {
      throw new Error("标题过长");
    }

    // ...
  },
});
```

### 客户端错误处理

```tsx
function TaskForm() {
  const createTask = useMutation(api.tasks.createTask);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (title: string) => {
    try {
      setError(null);
      await createTask({ title });
    } catch (err) {
      setError(err instanceof Error ? err.message : "未知错误");
    }
  };

  return (
    <div>
      {error && <div className="error">{error}</div>}
      {/* form */}
    </div>
  );
}
```

---

## 环境变量

### 设置环境变量

```bash
# 开发环境
npx convex env set OPENAI_API_KEY sk-...

# 生产环境
npx convex env set OPENAI_API_KEY sk-... --prod

# 查看环境变量
npx convex env list
```

### 使用环境变量

```typescript
export const generateAIResponse = action({
  args: { prompt: v.string() },
  handler: async (ctx, args) => {
    const apiKey = process.env.OPENAI_API_KEY;

    if (!apiKey) {
      throw new Error("OPENAI_API_KEY 未设置");
    }

    // 使用 API key...
  },
});
```

---

## 测试

### 单元测试

```typescript
// convex/tasks.test.ts
import { convexTest } from "convex-test";
import { expect, test } from "vitest";
import schema from "./schema";
import { api } from "./_generated/api";

test("创建任务", async () => {
  const t = convexTest(schema);

  // 创建用户
  const userId = await t.run(async (ctx) => {
    return await ctx.db.insert("users", {
      name: "Test User",
      email: "test@example.com",
    });
  });

  // 创建任务
  const taskId = await t.mutation(api.tasks.createTask, {
    title: "Test Task",
    userId,
  });

  // 验证
  const task = await t.run(async (ctx) => {
    return await ctx.db.get(taskId);
  });

  expect(task?.title).toBe("Test Task");
  expect(task?.completed).toBe(false);
});

test("查询用户任务", async () => {
  const t = convexTest(schema);

  const userId = await t.run(async (ctx) => {
    return await ctx.db.insert("users", {
      name: "Test User",
      email: "test@example.com",
    });
  });

  // 创建多个任务
  await t.mutation(api.tasks.createTask, { title: "Task 1", userId });
  await t.mutation(api.tasks.createTask, { title: "Task 2", userId });

  // 查询
  const tasks = await t.query(api.tasks.getTasksByUser, { userId });

  expect(tasks).toHaveLength(2);
});
```

---

## 最佳实践

### 1. Schema 优先

总是定义 Schema，即使是原型项目：

```typescript
// ✅ 推荐
export default defineSchema({
  tasks: defineTable({
    title: v.string(),
    completed: v.boolean(),
  }),
});

// ❌ 避免
// 没有 schema
```

### 2. 使用索引优化查询

```typescript
// ✅ 使用索引
const tasks = await ctx.db
  .query("tasks")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .collect();

// ❌ 全表扫描
const tasks = await ctx.db
  .query("tasks")
  .filter((q) => q.eq(q.field("userId"), userId))
  .collect();
```

### 3. 适当使用函数类型

- Query：只读操作，需要实时更新
- Mutation：写入操作，需要事务保证
- Action：调用外部 API

```typescript
// ✅ 正确
export const getTasks = query({
  /* ... */
});
export const createTask = mutation({
  /* ... */
});
export const sendEmail = action({
  /* ... */
});

// ❌ 错误
export const getTasks = mutation({
  /* ... */
}); // 只读应该用 query
```

### 4. 避免在 Query/Mutation 中调用外部 API

```typescript
// ❌ 错误 - 在 query 中调用外部 API
export const getBadData = query({
  handler: async (ctx) => {
    const response = await fetch("..."); // 不允许
    return response.json();
  },
});

// ✅ 正确 - 使用 action
export const getGoodData = action({
  handler: async (ctx) => {
    const response = await fetch("...");
    const data = await response.json();

    // 在 action 中调用 mutation 保存数据
    await ctx.runMutation(api.data.saveData, { data });

    return data;
  },
});
```

### 5. 使用类型安全

```typescript
// ✅ 使用生成的类型
import { Id } from "./_generated/dataModel";

export const getTask = query({
  args: { taskId: v.id("tasks") },
  handler: async (ctx, args): Promise<Task | null> => {
    return await ctx.db.get(args.taskId);
  },
});

// 在客户端
const task = useQuery(api.tasks.getTask, { taskId });
// task 的类型是 Task | null | undefined
```

### 6. 合理使用分页

```typescript
// ✅ 对大数据集使用分页
export const listTasks = query({
  args: { paginationOpts: paginationOptsValidator },
  handler: async (ctx, args) => {
    return await ctx.db.query("tasks").paginate(args.paginationOpts);
  },
});

// ❌ 避免返回大量数据
export const getAllTasks = query({
  handler: async (ctx) => {
    return await ctx.db.query("tasks").collect(); // 可能返回数千条
  },
});
```

### 7. 使用 Internal Functions 保护敏感逻辑

```typescript
// ✅ 敏感操作使用 internal
export const deleteAllUserData = internalMutation({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    // 只能从服务端调用，不能从客户端调用
  },
});

// ❌ 避免暴露敏感操作
export const deleteAllUserData = mutation({
  // 客户端可以直接调用
});
```

---

## 常见使用场景

### 1. 聊天应用

```typescript
// convex/messages.ts
export const sendMessage = mutation({
  args: {
    conversationId: v.id("conversations"),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("未认证");

    await ctx.db.insert("messages", {
      conversationId: args.conversationId,
      authorId: identity.subject,
      content: args.content,
      createdAt: Date.now(),
    });
  },
});

export const getMessages = query({
  args: { conversationId: v.id("conversations") },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId),
      )
      .order("desc")
      .take(100);
  },
});
```

### 2. 实时协作

```typescript
// convex/documents.ts
export const updateDocument = mutation({
  args: {
    documentId: v.id("documents"),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.documentId, {
      content: args.content,
      updatedAt: Date.now(),
    });
  },
});

export const subscribeToDocument = query({
  args: { documentId: v.id("documents") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.documentId);
  },
});
```

### 3. AI 应用

```typescript
// convex/ai.ts
export const chat = action({
  args: {
    conversationId: v.id("conversations"),
    message: v.string(),
  },
  handler: async (ctx, args) => {
    // 1. 保存用户消息
    await ctx.runMutation(api.messages.sendMessage, {
      conversationId: args.conversationId,
      content: args.message,
      role: "user",
    });

    // 2. 获取对话历史
    const history = await ctx.runQuery(api.messages.getMessages, {
      conversationId: args.conversationId,
    });

    // 3. 调用 OpenAI
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: history.map((m) => ({
          role: m.role,
          content: m.content,
        })),
      }),
    });

    const data = await response.json();
    const aiMessage = data.choices[0].message.content;

    // 4. 保存 AI 回复
    await ctx.runMutation(api.messages.sendMessage, {
      conversationId: args.conversationId,
      content: aiMessage,
      role: "assistant",
    });

    return aiMessage;
  },
});
```

---

## 调试

### 查看日志

```bash
# 实时查看日志
npx convex logs

# 查看特定函数的日志
npx convex logs --name tasks:createTask
```

### 在函数中打印日志

```typescript
export const createTask = mutation({
  args: { title: v.string() },
  handler: async (ctx, args) => {
    console.log("创建任务:", args.title);

    const taskId = await ctx.db.insert("tasks", {
      title: args.title,
      completed: false,
    });

    console.log("任务已创建:", taskId);

    return taskId;
  },
});
```

### 使用 Dashboard

访问 https://dashboard.convex.dev 查看：

- 函数执行历史
- 数据库内容
- 日志
- 性能指标

---

## 资源

- 官方文档：https://docs.convex.dev
- GitHub：https://github.com/get-convex/convex-backend
- Discord 社区：https://convex.dev/community
- Stack 博客：https://stack.convex.dev
- 示例项目：https://github.com/get-convex/convex-demos

---

## 相关技能

- TypeScript：Convex 函数使用 TypeScript 编写
- React：使用 React Hooks 集成
- Next.js：服务端渲染和 Server Actions
- 认证：Clerk、Auth0 等认证提供商
- AI：OpenAI、Anthropic 等 LLM 集成
