# User Research Examples

User research examples including persona creation, journey mapping, competitive analysis, and survey design using Gemini.

---

## Example 1: User Persona Creation

Create detailed user personas based on research data.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: personas
backend: gemini
workdir: /path/to/research
---CONTENT---
基于以下用户访谈摘要，创建3个主要用户画像：

访谈摘要：
- 10名受访者，年龄25-45岁
- 职业：产品经理、设计师、开发者
- 痛点：现有项目管理工具过于复杂，学习成本高
- 需求：简单直观的任务管理，团队协作，进度可视化

请为每个画像包含：
1. 基本信息（姓名、年龄、职业、技术熟练度）
2. 目标和动机
3. 痛点和挑战
4. 使用场景
5. 引用（代表性语录）
---END---
EOF
```

### Expected Output

```
▶ personas (gemini)

# 用户画像

## Persona 1: 效率型产品经理 - 李明

### 基本信息
- **年龄:** 32岁
- **职业:** 产品经理，5年经验
- **技术熟练度:** 中等（熟悉常见工具，不写代码）
- **工作环境:** 创业公司，团队15人

### 目标和动机
- 快速跟踪多个项目进度
- 与设计师、开发者高效协作
- 减少会议时间，提高透明度
- 需要清晰的优先级管理

### 痛点和挑战
- 现有工具（Jira）功能过多，界面复杂
- 每次创建任务需要填写10+字段
- 团队成员抱怨难以上手
- 切换视图（看板、列表、甘特图）操作繁琐

### 使用场景
- **每天早晨:** 查看团队今日任务和优先级
- **每周例会:** 展示项目进度给管理层
- **随时:** 快速分配新任务给团队成员

### 引用
> "我不需要那么多功能，我只想快速看到谁在做什么，哪些任务逾期了。"

---

## Persona 2: 协作型设计师 - 王小美

### 基本信息
- **年龄:** 28岁
- **职业:** UI/UX设计师，3年经验
- **技术熟练度:** 中高（熟练使用设计工具，略懂前端）
- **工作环境:** 互联网公司，设计团队8人

### 目标和动机
- 与产品、开发无缝协作
- 设计任务与开发进度同步
- 方便附加设计稿和反馈
- 希望工具美观易用

### 痛点和挑战
- 工具界面不够直观美观
- 上传设计稿流程繁琐
- 与Figma等设计工具集成差
- 难以跟踪设计实现状态

### 使用场景
- **设计评审后:** 创建设计任务，附加Figma链接
- **开发提问时:** 快速查看设计规范和批注
- **每周:** 检查有多少设计已完成开发

### 引用
> "为什么项目管理工具都这么丑？我们是设计师，也需要美的体验。"

---

## Persona 3: 自主型开发者 - 张伟

### 基本信息
- **年龄:** 30岁
- **职业:** 全栈开发工程师，7年经验
- **技术熟练度:** 高（熟练使用Git、CLI、API）
- **工作环境:** 远程办公，开源项目贡献者

### 目标和动机
- 专注编码，减少工具切换
- 通过键盘快捷键操作
- 与Git/GitHub集成
- 自动化工作流

### 痛点和挑战
- 需要离开IDE去更新任务状态
- 缺少CLI工具和API
- 强制使用鼠标点击
- 邮件通知过多干扰工作

### 使用场景
- **提交代码后:** 自动关联相关任务
- **每日站会前:** 快速用CLI查看今日任务
- **完成功能后:** 快速标记为Done（快捷键）

### 引用
> "我喜欢在终端里工作，最好能用命令行直接操作任务。"

---

» 写入 personas.md
✓ personas 8.5s
```

### Usage Tips

- Include quantitative data (interview count, demographics)
- Add behavioral patterns and quotes for authenticity
- Create 2-4 primary personas (not more)
- Focus on goals and pain points, not just demographics

---

## Example 2: User Journey Map

Map the current user experience to identify pain points and opportunities.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: journey-map
backend: gemini
workdir: /path/to/research
---CONTENT---
为在线课程平台创建学生用户的学习旅程地图：

用户目标：完成一门编程课程并获得证书

阶段：
1. 发现课程（搜索、推荐）
2. 注册报名
3. 观看视频学习
4. 完成作业和测验
5. 获得证书

对每个阶段，描述：
- 用户行为（具体做什么）
- 想法和感受（情绪曲线）
- 痛点（遇到的问题）
- 机会点（可以改进的地方）
- 接触点（使用的渠道：网页、App、邮件等）

使用Markdown表格格式输出。
---END---
EOF
```

### Expected Output

```markdown
# 学生学习旅程地图

| 阶段 | 用户行为 | 想法和感受 | 痛点 | 机会点 | 接触点 |
|------|----------|------------|------|--------|--------|
| **发现课程** | 搜索"Python入门"<br>浏览课程列表<br>查看课程详情 | 😐 中立<br>"有这么多课程，哪个适合我？" | - 搜索结果太多，难以筛选<br>- 不知道哪个课程质量好<br>- 缺少难度标识 | - 智能推荐（基于水平）<br>- 添加用户评分筛选<br>- 明确标注"零基础"/"进阶" | 网页搜索<br>首页推荐 |
| **注册报名** | 点击"立即报名"<br>填写表单<br>选择支付方式 | 🙂 略积极<br>"看起来不错，试试看" | - 表单字段过多（12个）<br>- 不清楚是否可退款<br>- 支付流程需要跳转 | - 简化表单（3-5个必填）<br>- 突出显示退款政策<br>- 支付页内嵌 | 网页注册<br>支付页面 |
| **观看学习** | 播放视频<br>做笔记<br>暂停回看 | 😊 积极<br>"讲得很清楚！" | - 视频无法调速<br>- 笔记功能不明显<br>- 移动端体验差 | - 添加1.5x、2x倍速<br>- 时间戳笔记<br>- 优化移动端播放器 | 网页/App视频<br>笔记功能 |
| **完成作业** | 阅读题目<br>编写代码<br>提交 | 😟 焦虑<br>"这道题太难了..." | - 题目说明不清晰<br>- 没有代码提示<br>- 提交后无即时反馈 | - 添加示例和提示<br>- 集成代码补全<br>- 提交后立即显示结果 | 网页作业系统<br>代码编辑器 |
| **获得证书** | 完成测验<br>查看成绩<br>下载证书 | 😄 喜悦<br>"终于完成了！" | - 证书生成慢（需24小时）<br>- 证书PDF格式不美观<br>- 分享到LinkedIn流程复杂 | - 即时生成证书<br>- 提供高清证书模板<br>- 一键分享社交媒体 | 网页成绩页<br>证书下载 |

## 情绪曲线

```
情绪
 😄 |                                              ●
 😊 |                    ●                        /
 🙂 |           ●       /                        /
 😐 |    ●     /                                /
 😟 |                              ●
    |________________________________________________
     发现   注册   学习   作业   证书
```

## 关键洞察

1. **最大痛点:** 作业阶段（情绪低谷）
   - 建议：增加辅助学习资源和即时反馈

2. **高兴奋点:** 学习视频阶段
   - 保持：优质内容制作

3. **流失风险点:** 注册阶段表单过长
   - 优先优化：简化注册流程

4. **增长机会:** 证书分享
   - 病毒式传播潜力，需优化分享体验
```

---

## Example 3: Competitive Analysis

Analyze competitor products to identify best practices and gaps.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: competitive-analysis
backend: gemini
workdir: /path/to/research
---CONTENT---
对比分析3个待办事项App（Todoist、Things、Microsoft To Do）：

分析维度：
1. 核心功能对比（任务创建、分类、提醒、协作）
2. 用户体验（易用性、学习曲线）
3. 视觉设计（界面美观度、一致性）
4. 定价策略
5. 独特功能（差异化特色）
6. 用户评价（App Store评分和主要反馈）

输出格式：
- 使用Markdown表格对比
- 总结各产品的优势和劣势
- 提出我们的产品机会点
---END---
EOF
```

### Expected Output

```markdown
# 待办事项App竞品分析

## 功能对比表

| 功能 | Todoist | Things | Microsoft To Do |
|------|---------|--------|-----------------|
| **任务创建** | ⭐⭐⭐⭐⭐<br>自然语言解析 | ⭐⭐⭐⭐<br>快速添加 | ⭐⭐⭐<br>基础输入 |
| **优先级** | ✅ 4级优先级 | ✅ 3级（Today/Upcoming/Someday） | ✅ 标星标记 |
| **标签/分类** | ✅ 标签+项目 | ✅ 区域+项目 | ✅ 列表分组 |
| **提醒** | ✅ 时间+地点 | ✅ 时间提醒 | ✅ 时间提醒 |
| **重复任务** | ✅ 灵活规则 | ✅ 预设规则 | ✅ 基础重复 |
| **协作** | ✅ 共享项目 | ❌ 仅个人 | ✅ 共享列表 |
| **跨平台** | ✅ 全平台 | ⚠️ 仅Apple生态 | ✅ 全平台 |

[...其他对比维度表格...]

## 差异化分析

### Todoist 优势
- 自然语言输入（"明天下午3点提醒我开会"自动解析）
- 生产力可视化（完成任务Karma积分）
- 强大的过滤器和视图

### Things 优势
- 极简优雅设计（Apple Design Award获奖）
- Today视图设计（每日计划体验最佳）
- 无缝Apple生态集成（Siri、Widget）

### Microsoft To Do 优势
- 免费无限制
- 与Outlook任务同步
- 企业用户基础大

## 我们的产品机会

1. **AI智能助手**
   - 竞品均无：基于历史行为推荐任务优先级
   - 差异化点：自动识别拖延任务并提醒

2. **团队协作增强**
   - Todoist协作功能简单
   - 机会：任务分配、进度跟踪、团队看板

3. **跨工作流集成**
   - 竞品孤立使用
   - 机会：与Slack、Notion、GitHub深度集成

4. **定价策略**
   - Todoist高级版$4/月（功能锁定多）
   - Things买断制$50（仅Apple）
   - 机会：Freemium模式，基础功能永久免费
```

---

## Example 4: Survey Design

Design user research surveys with clear questions and structure.

### Command

```bash
memex-cli run --backend gemini --stdin <<'EOF'
---TASK---
id: survey-design
backend: gemini
workdir: /path/to/research
---CONTENT---
为健身App设计用户调研问卷：

目标：了解用户健身习惯、痛点和对App功能的期望

要求：
1. 包含3个部分：基本信息、使用习惯、功能需求
2. 每部分5-8个问题
3. 混合使用单选、多选、量表、开放问题
4. 问题清晰无歧义
5. 预计填写时间：5-7分钟

输出Markdown格式问卷。
---END---
EOF
```

### Expected Output

```markdown
# 健身App用户调研问卷

**预计时间:** 5-7分钟
**目的:** 帮助我们设计更符合您需求的健身App

---

## 第一部分：基本信息

1. **您的年龄段？** （单选）
   - [ ] 18-24岁
   - [ ] 25-34岁
   - [ ] 35-44岁
   - [ ] 45岁以上

2. **您的健身经验？** （单选）
   - [ ] 新手（少于6个月）
   - [ ] 初级（6个月-2年）
   - [ ] 中级（2-5年）
   - [ ] 高级（5年以上）

3. **您主要的健身场所？** （可多选）
   - [ ] 健身房
   - [ ] 家中
   - [ ] 户外（公园、跑步道）
   - [ ] 其他：_______

---

## 第二部分：健身习惯

4. **您每周健身几次？** （单选）
   - [ ] 0次（不健身）
   - [ ] 1-2次
   - [ ] 3-4次
   - [ ] 5次以上

5. **您健身的主要目标是什么？** （最多选3项）
   - [ ] 减重/减脂
   - [ ] 增肌
   - [ ] 提高体能
   - [ ] 保持健康
   - [ ] 减压放松
   - [ ] 其他：_______

6. **您在坚持健身时遇到的最大困难是？** （可多选）
   - [ ] 缺乏动力/容易放弃
   - [ ] 不知道如何训练
   - [ ] 时间不够
   - [ ] 进步缓慢，看不到效果
   - [ ] 容易受伤
   - [ ] 其他：_______

7. **您目前是否使用健身App？** （单选）
   - [ ] 是（请填写App名称：_______）
   - [ ] 否

8. **如果使用，您对现有健身App的满意度？** （1-5分）
   - 1分（非常不满意） - 2分 - 3分 - 4分 - 5分（非常满意）

---

## 第三部分：功能需求

9. **以下功能对您有多重要？** （量表：1=不重要，5=非常重要）

   | 功能 | 1 | 2 | 3 | 4 | 5 |
   |------|---|---|---|---|---|
   | 个性化训练计划 | ○ | ○ | ○ | ○ | ○ |
   | 视频教学 | ○ | ○ | ○ | ○ | ○ |
   | 进度追踪和数据分析 | ○ | ○ | ○ | ○ | ○ |
   | 社交和挑战（与好友PK） | ○ | ○ | ○ | ○ | ○ |
   | 饮食记录和营养建议 | ○ | ○ | ○ | ○ | ○ |
   | 真人教练在线指导 | ○ | ○ | ○ | ○ | ○ |

10. **您希望App提供哪种训练内容？** （可多选）
    - [ ] 力量训练
    - [ ] 有氧运动
    - [ ] 瑜伽/拉伸
    - [ ] HIIT
    - [ ] 普拉提
    - [ ] 其他：_______

11. **您愿意为健身App付费吗？** （单选）
    - [ ] 愿意订阅（月费/年费）
    - [ ] 愿意一次性买断
    - [ ] 只使用免费版
    - [ ] 看具体功能和价格

12. **如果付费，您认为合理的价格是？** （单选）
    - [ ] ￥19/月
    - [ ] ￥29/月
    - [ ] ￥49/月
    - [ ] ￥99/月以上

13. **您最希望健身App解决您的什么问题？** （开放问题）

    _请简述：_____________________

14. **您还有什么建议或期望？** （开放问题，选填）

    _请简述：_____________________

---

**感谢您的参与！**
```

---

## Tips for User Research

1. **Persona Creation**
   - Base on real research data, not assumptions
   - Include quotes from actual users
   - Create 2-4 primary personas (avoid "everyone")
   - Update personas as you learn more

2. **Journey Mapping**
   - Focus on one specific user goal per map
   - Include emotional states (not just actions)
   - Identify pain points AND opportunities
   - Involve stakeholders in the mapping process

3. **Competitive Analysis**
   - Analyze 3-5 direct competitors
   - Include screenshots for reference (use Gemini multimodal!)
   - Focus on differentiators, not just features
   - Update quarterly as competitors evolve

4. **Survey Design**
   - Keep surveys under 10 minutes
   - Start with easy questions (demographics)
   - Mix question types for engagement
   - Avoid leading questions ("Don't you think...")
   - Pilot test with 5 people before launch

---

## Related Resources

- [references/design-principles.md](../references/design-principles.md) - UX methodologies
- [references/design-workflow.md](../references/design-workflow.md) - Research stage details
- [examples/information-architecture.md](./information-architecture.md) - IA design
- [SKILL.md](../SKILL.md) - Gemini basic usage
