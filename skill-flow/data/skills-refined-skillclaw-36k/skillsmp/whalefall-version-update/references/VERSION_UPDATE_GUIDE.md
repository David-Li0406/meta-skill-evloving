# 版本更新操作指南

> 适用范围：当需要发布全局版本（如 `v1.2.x`）时，使用本指南同步核心版本号、校验脚本与可见页面。该流程力求**聚焦必要文件**，避免在重构文档、分析白皮书等大体量文件上反复改动。

## 1. 操作前准备

1. 确认即将发布的版本号（语义化：`MAJOR.MINOR.PATCH`）。
2. 确认此次发版的主题（例如“注释补齐”“安全补丁”等），以便 CHANGELOG 与 About 页面简述。
3. 切换到干净分支，确保本地 `rg`/`python3` 可运行。

## 2. 必须更新的文件清单

此列表为**版本号强一致**的最小集，更新顺序随意，但务必全部覆盖。

> **强约束**：每次版本更新必须先修改 `app/settings.py` 中的 `APP_VERSION`，该值作为运行时版本号来源（日志、监控、对外返回等以此为准）。

| 更新项 | 文件/位置 | 说明 |
| --- | --- | --- |
| 运行时版本 | `app/settings.py` (`APP_VERSION`) | 运行时版本号唯一来源，用于日志、健康检查与可见页面渲染。 |
| 项目配置 | `pyproject.toml` (`[project].version`) | 供构建工具与 `uv` 使用，需与 `app/settings.py` 保持一致。 |
| 运行环境 | `env.example` (`APP_VERSION`) | 提供健康检查及 `.env` 示例基线，需与 `app/settings.py` 保持一致。 |
| 依赖锁 | `uv.lock` 中 `name = "whalefalling"` 节点 | 搜索 `[[package]] name = "whalefalling"`，更新 `version` 字段。 |
| 部署脚本 | `scripts/deploy/deploy-prod-all.sh` | 更新脚本头部注释、欢迎横幅和日志输出中的版本号。 |
| API 元数据 | `app/routes/main.py` (`app_version`) | `/` 健康检查返回值。 |
| 页脚展示 | `app/templates/base.html` 页脚文本 | 网站所有页面的版本展示。 |
| Nginx 错误页 | `nginx/error_pages/404.html` 与 `50x.html` | 访客可见的离线提示页面。 |
| README 徽章与页脚 | `README.md` 顶部徽章 & 底部“最后更新/版本” | 方便外部访客识别最新版本。 |
| CHANGELOG | `CHANGELOG.md` 顶部新增条目 | 采用倒序记录：日期、主题、修复项。 |
| About 页面 | `app/templates/about.html` 时间轴 | 不需要调整历史条目。 |

> **说明**：如无特殊需求，不要改动重构文档（例如 `docs/Obsidian/architecture/spec.md`、`docs/Obsidian/architecture/project-structure.md`）或分析报告（例如 `docs/reports/clean-code-analysis.md`）。这些文档仅在内容真正变更时更新，避免纯版本跳动带来的审核负担。

## 3. 可选更新项

- 部署/运维文档示例：若文档明确引用 `APP_VERSION` 示例值，可在同一次 PR 中顺手替换，但不是硬性要求。
- 模板或脚本中以“最近版本”做展示的非核心页面，可视需要更新。

## 4. 操作步骤建议

1. **批量搜索**：更新前运行 `rg -n "1\.2\.x"` 定位当前版本号出现位置，逐一甄别属于“必需列表”还是“可忽略项/依赖版本”。
2. **逐项替换**：按照上表替换版本号，并在 CHANGELOG/About 中写入简短中文描述。
3. **自检脚本**：
   - `python3 scripts/check_missing_docs_smart.py`（确保注释规范仍通过）。
   - 如有数据库变更或部署脚本修改，可额外运行针对性的单元/集成测试。
4. **验证差异**：`git status` 应只包含指南列出的文件（以及与本次功能直接相关的内容）。若出现 `docs/Obsidian/architecture/*`、`docs/reports/*` 等大文档，请确认是否确有内容更新，避免仅为版本号而修改。
5. **提交信息**：建议使用 `chore: bump version to x.y.z` 或 `chore: release vX.Y.Z`，并在 PR 描述中列出验证步骤（脚本、手测等）。

## 5. FAQ

- **Q: 版本更新时是否需要重新生成分析报告?**  
  A: 否。除非分析内容有实质变更，否则不要为了版本号刷新而重跑报告。

- **Q: 依赖文件中出现 `1.2.2`，需要改吗?**  
  A: 若是第三方包（如 `flask-wtf==1.2.2`），保持不变；只处理与本项目自身版本直接相关的字符串。

- **Q: 需要同步更新 Git Tag/Release 吗?**  
  A: 视团队流程而定，通常在 PR 合并后由发布者打 Tag 并生成 Release 说明。

## 6. v1.3.2（UI 统一）发布参考

> 主题：统一实例/凭据/标签等 CRUD 模态的布局与启用开关体验，清理历史遗留字段。

### 6.1 版本范围
- **UI**：实例、凭据、标签新增/编辑模态统一为 `modal-lg`，描述字段移到“基础信息”区，启用开关与按钮同排。
- **标签**：移除颜色/排序字段，新增父分类(`infra_domain`、`org_domain`、`external_domain`)及其校验逻辑。
- **说明文档**：`docs/changes/refactor/ui/tag-management-cleanup.md`、`docs/changes/refactor/ui/crud-modal-refactor.md` 等需补充最新 UI 规范截图。

### 6.2 操作清单
1. **版本号替换**：以 `1.3.1 -> 1.3.2` 为例，按照第 2 节表格更新所有必需文件，并在 `CHANGELOG.md` 写入“UI 统一”条目。
2. **功能验证**：
   - 新建/编辑实例、凭据、标签模态截图留档，确保宽度、描述位置、启用开关位置一致。
   - 标签分类管理页面可选择父类，删除颜色/排序后无残留输入。
   - 前端筛选器、标签选择器不再使用颜色信息。
3. **脚本/测试**：
   - `make quality`、`pytest -k tags` 或关联用例通过。
   - 若执行标签数据迁移（删除列/新增父类），附上 Alembic/SQL 执行记录。
4. **验收记录**：在 PR 模板“版本同步”小节中粘贴 `git status`、`CHANGELOG` 片段与关键页面截图链接。

完成以上动作即可宣告 `v1.3.2` 发布，后续版本可参照该结构补充专项说明。

---

按照以上流程执行，可在最短时间内完成一次标准化的版本同步，同时避免维护噪音。
