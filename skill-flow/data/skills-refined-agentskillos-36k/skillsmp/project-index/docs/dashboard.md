# Dashboard GUI

Web UI 仪表盘，实时追踪项目健康状态。

## 启动

```bash
# 启动 (默认端口 3008)
node scripts/dashboard.js

# 自定义端口
node scripts/dashboard.js --port 8080

# 自动打开浏览器
node scripts/dashboard.js --open
```

## 界面布局

```
┌─────────────────────────────────────────────────────────────────┐
│ 侧边栏     │                    主区域                           │
│ ─────────  │  ┌────────────────────────────────────────────┐    │
│ 🚀 启动器  │  │  任务启动器 / 运维中心 / 项目洞察 / 配置    │    │
│ 🔧 运维    │  └────────────────────────────────────────────┘    │
│ 📊 洞察    │                                                     │
│ ⚙️ 配置    │                                                     │
└─────────────────────────────────────────────────────────────────┘
```

## 功能模块

### 任务启动器

预设任务一键启动：
- **完整索引**: 文档更新 + 代码审计
- **检测过期**: 只检测过期模块
- **测试分析**: 测试覆盖分析
- **生成测试**: 批量生成测试文件

点击工具卡片选中，配置参数（并发数、索引深度等）后点击"开始任务"。
任务启动后会显示 Toast 通知。

### 运维中心

后台任务管理：
- **任务列表**: 显示所有子任务状态
- **筛选功能**: 按状态（运行中/失败/成功）或任务类型筛选
- **分组视图**: 按任务类型分组，可展开/折叠
- **失败重试**: 点击重试按钮只重试失败任务
- **任务详情**: 查看日志、堆栈跟踪、参数
- **ETA 预估**: 基于历史耗时预估剩余时间

### 项目洞察

四大指标卡片：

| 指标 | 说明 |
|------|------|
| **测试覆盖率** | 源文件被测试 import 的比例 |
| **文档覆盖率** | 有 CLAUDE.md 的目录比例 |
| **审计覆盖率** | 有 AUDIT.md 的模块比例 |
| **模块就绪** | 通过审计的模块比例 |

**有效覆盖率**：显示实际覆盖率和有效覆盖率（排除被父目录覆盖的小目录）。

**审计问题分布**：
- 🔴 Critical
- 🟠 High
- 🟡 Medium
- 🟢 Low

**Stale 文档追踪**：
- 已更新 / 待更新数量
- 最近修改的代码文件

**目录覆盖率热图**：按顶级目录显示覆盖百分比。

### 配置面板

在线编辑 `.stale-config.json`：
- 敏感级别切换
- 自动修正开关
- 覆盖率阈值编辑
- JSON 编辑器（带格式校验）

## API 端点

Dashboard 后端提供以下 API：

| 端点 | 说明 |
|------|------|
| `GET /api/projects` | 已注册项目列表 |
| `GET /api/project-data/{path}` | 项目数据（modules, coverage） |
| `GET /api/tasks` | 任务摘要列表 |
| `GET /api/task-details/{name}` | 细粒度子任务 |
| `GET /api/history/{name}` | 任务执行历史 |
| `GET /api/task-types` | 可用任务类型 |
| `GET /api/eta` | 剩余时间预估 |
| `POST /api/tasks/start` | 启动任务 |
| `POST /api/tasks/{name}/retry/{id}` | 重试失败任务 |
| `POST /api/tasks/{name}/cancel/{id}` | 取消运行中任务 |
| `DELETE /api/tasks/{name}/{id}` | 删除任务记录 |
| `DELETE /api/tasks/{name}/completed` | 清理已完成任务 |
| `GET /api/config` | 获取配置 |
| `PUT /api/config` | 保存配置 |
| `GET /api/audit-status` | 审计状态统计 |
| `GET /api/test-status` | 测试覆盖状态 |
| `GET /api/stale-status` | Stale 检测状态 |
| `GET /api/cached-data` | 缓存数据 |
| `POST /api/cached-data` | 更新缓存 |

## 数据文件

Dashboard 读取以下文件：
- `.module-analyzer-tasks.json` - 子任务列表
- `.module-analyzer-history.json` - 执行历史
- `.module-analyzer-progress.json` - 模块进度
- `.stale-config.json` - 项目配置
