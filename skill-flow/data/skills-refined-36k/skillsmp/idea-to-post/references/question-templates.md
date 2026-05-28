# 提问模板库

本文档为 `idea-to-post` skill 提供针对不同思考框架的预设提问模板。

---

## 通用阶段问题

所有框架都会经历的初始提问阶段。

### 推文目标

使用 `AskUserQuestion` 工具提问：

```yaml
question: 这篇推文的主要目标是什么？
header: 推文目标
options:
  - label: 分享经验心得
    description: 记录和分享个人/团队的实践经验、方法、心得
  - label: 表达观点看法
    description: 对某件事、某个现象表达自己的观点和立场
  - label: 解决具体问题
    description: 针对某个问题提供解决方案和建议
  - label: 推广产品/服务
    description: 介绍产品功能，吸引用户使用
multiSelect: false
```

### 目标受众

```yaml
question: 这篇推文的目标受众是谁？
header: 目标受众
options:
  - label: 行业同行/专业人士
    description: 面向同行、同事、专业人士的内容
  - label: 大众/一般读者
    description: 面向广泛大众，通俗易懂的内容
  - label: 特定群体
    description: 如创业者、开发者、学生等特定人群
  - label: 潜在客户/用户
    description: 面向可能购买/使用产品的用户
multiSelect: false
```

### 目标平台

```yaml
question: 你打算在哪个平台发布？
header: 发布平台
options:
  - label: 微信公众号
    description: 深度长文，2000字以上
  - label: 小红书
    description: 实用干货，500-1000字，多用emoji
  - label: 微博/Twitter
    description: 短小精悍，140-280字
  - label: LinkedIn/脉脉
    description: 专业职场，1000-1500字
multiSelect: true
```

---

## 5W1H 提问模板

### What（是什么）

```yaml
question: 你想介绍/讨论的核心主题是什么？
header: 核心主题
options:
  - label: 一个概念/理论
    description: 解释某个专业概念或理论
  - label: 一个产品/工具
    description: 介绍某个产品或工具的使用
  - label: 一个方法/技巧
    description: 分享某种方法或技巧
  - label: 一个问题/现象
    description: 讨论某个问题或社会现象
multiSelect: false
```

### Why（为什么）

```yaml
question: 为什么这个主题重要？你想要传达的核心意义是什么？
header: 核心意义
options:
  - label: 解决痛点
    description: 这个主题能解决什么实际痛点
  - label: 提供新视角
    description: 提供不同的思考角度
  - label: 分享趋势
    description: 分享行业或技术趋势
  - label: 传递价值
    description: 传递某种价值观或理念
multiSelect: true
```

### Who（谁）

```yaml
question: 谁应该关注这个主题？主要涉及哪些角色？
header: 涉及角色
options:
  - label: 个人用户
    description: 普通用户、个人消费者
  - label: 专业人士
    description: 开发者、设计师、从业者
  - label: 企业/团队
    description: 公司团队、组织机构
  - label: 决策者
    description: 管理者、创业者、投资人
multiSelect: true
```

### When（何时）

```yaml
question: 这个主题有什么时间维度需要强调？
header: 时间维度
options:
  - label: 当前热点
    description: 正在发生的、当下的趋势
  - label: 未来趋势
    description: 对未来的预测和展望
  - label: 历史回顾
    description: 从历史演变角度分析
  - label: 时机选择
    description: 强调做某事的最佳时机
multiSelect: false
```

### Where（何地）

```yaml
question: 这个主题在什么场景下最相关？
header: 应用场景
options:
  - label: 工作场景
    description: 职场、工作相关
  - label: 生活场景
    description: 日常生活相关
  - label: 学习场景
    description: 学习、教育相关
  - label: 特定行业
    description: 在特定行业/领域内
multiSelect: true
```

### How（如何）

```yaml
question: 你希望读者了解或采取什么行动？
header: 行动导向
options:
  - label: 了解认知
    description: 主要是让读者了解某个知识
  - label: 学习方法
    description: 教读者具体的方法/技巧
  - label: 改变行为
    description: 促使读者改变某些行为
  - label: 开始行动
    description: 促使读者开始某项行动
multiSelect: false
```

---

## SCQA 提问模板

### Situation（情境）

```yaml
question: 故事的"情境"是什么？即最初的稳定状态是什么？
header: 初始情境
options:
  - label: 理想状态
    description: 一切正常运行的状态
  - label: 常规状态
    description: 按部就班的日常
  - label: 困惑状态
    description: 对现状感到困惑或不满
  - label: 特定背景
    description: 某个特定的时机或背景
multiSelect: false
```

### Complication（冲突）

```yaml
question: 出现了什么"冲突"？打破了原有的平衡？
header: 冲突事件
options:
  - label: 突发问题
    description: 突然出现的问题、故障
  - label: 新的挑战
    description: 新的需求、新的竞争
  - label: 意外发现
    description: 发现了意想不到的事情
  - label: 内部矛盾
    description: 团队内部的分歧或矛盾
multiSelect: false
```

### Question（疑问）

```yaml
question: 面对这个冲突，产生了什么关键疑问？
header: 核心疑问
options:
  - label: 如何解决
    description: 如何解决这个问题？
  - label: 为什么会发生
    description: 为什么会出现这种情况？
  - label: 该怎么办
    description: 我们应该怎么办？
  - label: 是否要改变
    description: 是否需要改变现状？
multiSelect: false
```

### Answer（答案）

```yaml
question: 最终的"答案"是什么？你发现了/做了什么？
header: 解决方案
options:
  - label: 找到根本原因
    description: 发现了问题的根源
  - label: 实施了新方案
    description: 尝试了新的解决方案
  - label: 改变了认知
    description: 对问题有了新的理解
  - label: 取得了成果
    description: 最终达成了什么成果
multiSelect: true
```

---

## 黄金圈 提问模板

### Why（内核）

```yaml
question: 你最想传达的"为什么"是什么？你的信念/初衷是什么？
header: 核心信念
options:
  - label: 改变现状
    description: 相信现状需要改变
  - label: 创造价值
    description: 相信某件事能创造巨大价值
  - label: 传递理念
    description: 相信某种理念值得推广
  - label: 解决痛点
    description: 相信某个痛点必须被解决
multiSelect: false
```

### How（方法）

```yaml
question: 你用什么独特的方法来实现这个信念？
header: 方法论
options:
  - label: 独特流程
    description: 有一套独特的流程/方法
  - label: 创新技术
    description: 使用了创新的技术手段
  - label: 新颖模式
    description: 采用了新颖的商业模式
  - label: 思维方式
    description: 运用了不同的思维方式
multiSelect: true
```

### What（结果）

```yaml
question: 最终呈现的"结果"是什么？
header: 最终成果
options:
  - label: 具体产品
    description: 一个具体的产品或服务
  - label: 服务方案
    description: 一套解决方案或服务
  - label: 内容输出
    description: 一篇文章、课程、内容
  - label: 变化成效
    description: 某种变化或改进的成果
multiSelect: false
```

---

## AIDA 提问模板

### Attention（注意）

```yaml
question: 你打算用什么来"抓住"读者的注意力？
header: 吸引注意
options:
  - label: 震撼数据
    description: 用反常识的数据吸引注意
  - label: 制造悬念
    description: 用悬念引发好奇
  - label: 直击痛点
    description: 直接点出读者痛点
  - label: 反常识观点
    description: 提出与常识相反的观点
multiSelect: false
```

### Interest（兴趣）

```yaml
question: 如何让读者产生"兴趣"？
header: 激发兴趣
options:
  - label: 关联自身
    description: 让读者觉得"这说的就是我"
  - label: 揭示真相
    description: 揭示某些不为人知的真相
  - label: 承诺利益
    description: 承诺阅读后的收获
  - label: 故事引入
    description: 用故事引发兴趣
multiSelect: true
```

### Desire（欲望）

```yaml
question: 如何让读者产生"欲望"，想要你的产品/方案？
header: 激发欲望
options:
  - label: 描绘愿景
    description: 描绘使用后的美好状态
  - label: 社会认同
    description: 展示他人使用的成功案例
  - label: 稀缺性
    description: 强调机会的稀缺
  - label: 痛点加剧
    description: 强调不解决的后果
multiSelect: true
```

### Action（行动）

```yaml
question: 你希望读者采取什么"行动"？
header: 促使行动
options:
  - label: 立即购买
    description: 直接购买产品
  - label: 免费试用
    description: 先试用再决定
  - label: 了解更多
    description: 点击链接了解更多
  - label: 关注账号
    description: 关注获取更多内容
multiSelect: false
```

---

## PREP 提问模板

### Point（观点）

```yaml
question: 你的核心"观点"是什么？请用一句话概括。
header: 核心观点
options:
  - label: 应该做某事
    description: 建议做某件事
  - label: 不应该做某事
    description: 建议不做某件事
  - label: 某事是好/坏的
    description: 对某事的评价
  - label: 某事会发生
    description: 对未来的预测
multiSelect: false
```

### Reason（理由）

```yaml
question: 你为什么持有这个观点？主要理由是什么？
header: 支撑理由
options:
  - label: 个人经验
    description: 基于自己的经验
  - label: 数据支撑
    description: 基于数据和研究
  - label: 逻辑推理
    description: 基于逻辑推导
  - label: 价值判断
    description: 基于价值观或原则
multiSelect: true
```

### Example（例子）

```yaml
question: 你有什么具体的"例子"来支撑这个观点？
header: 具体例子
options:
  - label: 个人经历
    description: 自己的故事
  - label: 案例研究
    description: 他人的案例
  - label: 数据/事实
    description: 具体的数据或事实
  - label: 类比说明
    description: 用类比来解释
multiSelect: true
```

---

## 5-Why 提问模板

### 初始问题

```yaml
question: 你想要深入分析的"问题"是什么？
header: 初始问题
options:
  - label: 用户问题
    description: 用户遇到的问题
  - label: 产品问题
    description: 产品出现的问题
  - label: 工作问题
    description: 工作中的问题
  - label: 个人问题
    description: 个人发展中的问题
multiSelect: false
```

### Why引导

（动态生成，每次追问"为什么？"并提供选项）

---

## 第一性原理 提问模板

### 待质疑的假设

```yaml
question: 你想要质疑的"常识"或"假设"是什么？
header: 质疑对象
options:
  - label: 行业惯例
    description: 大家都这么做的行业做法
  - label: 技术限制
    description: 被认为技术上做不到的事
  - label: 市场认知
    description: 市场普遍认可的认知
  - label: 个人限制
    description: 自己能力上的限制
multiSelect: false
```

### 基本事实

```yaml
question: 拆解到最基本的"事实"是什么？
header: 基本事实
options:
  - label: 物理规律
    description: 自然界的物理规律
  - label: 经济规律
    description: 经济学的基本原理
  - label: 人的需求
    description: 人的本质需求
  - label: 技术本质
    description: 技术的根本原理
multiSelect: true
```

### 重构方案

```yaml
question: 从基本事实出发，如何"重构"解决方案？
header: 重构方向
options:
  - label: 全新方法
    description: 用全新的方法解决
  - label: 简化流程
    description: 大幅简化原有流程
  - label: 成本降低
    description: 大幅降低成本
  - label: 性能突破
    description: 实现性能上的突破
multiSelect: true
```

---

## FBA 提问模板

### Feature（特性）

```yaml
question: 你的产品/服务有什么核心"特性"？
header: 产品特性
options:
  - label: 技术特性
    description: 技术上的特点
  - label: 功能特性
    description: 功能上的特点
  - label: 设计特性
    description: 设计上的特点
  - label: 服务特性
    description: 服务上的特点
multiSelect: true
```

### Benefit（利益）

```yaml
question: 这个特性给用户带来什么"利益"？
header: 用户利益
options:
  - label: 节省时间
    description: 帮用户节省时间
  - label: 节省成本
    description: 帮用户节省金钱
  - label: 提升效率
    description: 提高工作效率
  - label: 更好体验
    description: 提供更好的使用体验
multiSelect: true
```

### Advantage（优势）

```yaml
question: 与其他产品相比，你的"优势"是什么？
header: 差异优势
options:
  - label: 更快
    description: 速度上的优势
  - label: 更便宜
    description: 价格上的优势
  - label: 更好用
    description: 易用性上的优势
  - label: 更专业
    description: 专业性上的优势
multiSelect: true
```

---

## 风格偏好问题

所有框架最后都会询问风格偏好。

```yaml
question: 你希望推文的整体风格是什么？
header: 风格偏好
options:
  - label: 专业严谨
    description: 数据支撑、逻辑严密、专业术语
  - label: 轻松幽默
    description: 语言活泼、幽默风趣、通俗易懂
  - label: 故事化
    description: 用讲故事的方式、情节生动
  - label: 实用干货
    description: 直接给方法、清单式、可操作
multiSelect: false
```

---

## 提问策略

### 渐进式提问

1. **先宽后窄**：先问大方向，再问细节
2. **先易后难**：先问容易回答的，建立回答节奏
3. **提供选项**：每个问题提供3-4个选项
4. **允许自定义**：始终支持"Other"选项让用户自定义输入

### 动态调整

- 根据用户之前的回答动态调整后续问题
- 如果用户选择"Other"自定义输入，分析输入内容确定下一步
- 每个阶段3-5个问题为宜，避免过多造成疲劳

### 提问时机

- **第一阶段**：在框架选择之前（目标、受众、平台）
- **第二阶段**：在框架选择之后（框架特定问题）
- **第三阶段**：在内容生成之前（风格偏好、补充信息）
