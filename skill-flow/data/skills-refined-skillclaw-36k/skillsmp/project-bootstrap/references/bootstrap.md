# 项目启动落盘（bootstrap）

## 目标

当您说"开始一个项目/我的需求是…"时，先把项目的"规划入口文件"与 Record 目录结构落盘，形成后续循环A/循环B的统一锚点。

## 步骤（必须按顺序）

1) 确认项目根目录
   - 明确告知：默认项目根目录 = 当前工作目录（CWD）
   - 用一句话询问确认：是否把 `Record/` 写入当前目录
   - 若回答"不是"，要求给出正确项目根目录路径后再继续

2) 创建 Record 目录结构（项目内）
   - `Record/plan/`
   - `Record/Memory/`（子代理记忆目录）

3) 生成并落盘"预定清单（草案）"
   - 文件路径固定：`Record/plan/draft-plan.md`
   - 内容必须包含：
     - 详细需求描述：完整记录需求，供 analysis-agent 分析用
     - 待澄清问题：需要进一步确认的点（如技术栈、部署方式等）

4) 初始化项目级状态机文件（可选但推荐）
   - 文件路径固定：`Record/state.json`
   - 在"规划确认通过"之前，`active_plan_version` 必须为空字符串或 null
   - 其余字段按最小结构写入

5) 创建项目记录文件
   - 文件路径固定：`Record/record.md`
   - 写入初始内容（见 templates.md）
   - 追加第一条记录：
     ```markdown
     ## YYYY-MM-DD HH:MM 需求提出
     {需求摘要}
     ```

6) 创建 plan-agent 记忆文件
   - 文件路径固定：`Record/Memory/plan-agent.md`
   - 根据 memory-template.md 创建
   - 填写基本信息：项目名、项目根目录、技术栈、创建时间

7) 输出"下一步指令"
   - 告知：请先审阅 `Record/plan/draft-plan.md`
   - 如需修改则在此对话中提出，plan-agent 更新该文件
   - 确认无误后，请启动 analysis-agent 进行草案分析
