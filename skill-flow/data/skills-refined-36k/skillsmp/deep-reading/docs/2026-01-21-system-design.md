# Deep Reading System 设计方案

> 日期：2026-01-21
> 状态：草案
> 作者：Claude + liweixin

---

## 1. 项目概述

### 1.1 目标用户
- 个人学习者：阅读/听播客，做笔记，建立知识库
- 研究工作者：文献综述、论文对比分析
- 程序员摸鱼：高效消化内容，隐蔽性强

### 1.2 设计原则
- **隐蔽性**：终端界面，老板看到就是代码
- **高效率**：AI 全自动处理，用户只需审核
- **可中断**：随时暂停/继续，状态持久化
- **双链优先**：链接即组织，拒绝文件夹分类

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                │
├─────────────────────────────────────────────────────────────────┤
│  Claude Code CLI          TUI Player           Obsidian         │
│  (主控制台)               (播放+实时交互)       (笔记审核/浏览)   │
└───────┬───────────────────────┬─────────────────────┬───────────┘
        │                       │                     │
        ▼                       ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        核心服务层                                │
├─────────────────────────────────────────────────────────────────┤
│  Content        Audio         AI            Note                │
│  Fetcher        Engine        Processor     Manager             │
│  (内容获取)     (播放引擎)    (Claude API)  (笔记管理)           │
└───────┬───────────────────────┬─────────────────────┬───────────┘
        │                       │                     │
        ▼                       ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        存储层                                    │
├─────────────────────────────────────────────────────────────────┤
│  ~/.deep-reading/cache/           Obsidian Vault                │
│  (音视频缓存、转录文本、           /Users/liweixin/smart notes/  │
│   处理状态、用户标记)              DeepReading/                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 技术栈选型

| 组件 | 技术选择 | 理由 |
|------|----------|------|
| CLI 框架 | Bash + Python | Claude Code 原生支持 |
| 音频播放 | mpv (IPC 模式) | 功能强大，支持后台控制 |
| TUI 界面 | Python Textual 或 Rich | 现代终端 UI，美观易用 |
| 内容下载 | yt-dlp, wget, curl | 成熟稳定 |
| AI 处理 | Claude API (via Claude Code) | 原生集成 |
| 笔记存储 | Obsidian Vault (Markdown) | 双链生态成熟 |
| 数据库 | SQLite | 轻量，本地优先 |

---

## 3. 核心模块设计

### 3.1 Content Fetcher (内容获取模块)

#### 3.1.1 支持的内容源 (按优先级)

| 优先级 | 来源 | 获取方式 | 输出 |
|--------|------|----------|------|
| P0 | YouTube 视频 | yt-dlp | 音频 + 字幕 + 元数据 |
| P0 | 播客 (Podcast) | RSS 解析 + wget | 音频 + show notes |
| P0 | 博客/网页 | readability + wget | 清洁文本 + 元数据 |
| P1 | arXiv 论文 | arxiv API | PDF + 元数据 |
| P1 | 本地 PDF | 直接读取 | 文本提取 |
| P2 | Anna's Archive | 搜索 API | 电子书下载 |

#### 3.1.2 内容获取流程

```
URL/来源输入
    ↓
┌─────────────────┐
│  来源识别器     │ → 判断类型 (YouTube/Podcast/Blog/...)
└────────┬────────┘
         ↓
┌─────────────────┐
│  专用下载器     │ → 调用对应工具下载
└────────┬────────┘
         ↓
┌─────────────────┐
│  内容标准化     │ → 统一格式: 音频(mp3) + 文本(txt) + 元数据(json)
└────────┬────────┘
         ↓
    存入缓存 + 触发 AI 处理
```

#### 3.1.3 缓存结构

```
~/.deep-reading/cache/
├── youtube/
│   └── {video_id}/
│       ├── audio.mp3
│       ├── transcript.txt
│       ├── transcript.vtt      # 带时间戳
│       ├── metadata.json
│       └── processing_state.json
├── podcast/
│   └── {podcast_id}_{episode_id}/
│       └── ...
└── web/
    └── {url_hash}/
        └── ...
```

### 3.2 Audio Engine (音频引擎)

#### 3.2.1 架构

```
┌──────────────────────────────────────────────────────────┐
│                      TUI Player                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  ▶ Elon Musk on AGI                                │  │
│  │  ━━━━━━━━━━●━━━━━━━━━━━  45:23 / 2:52:10  1.5x    │  │
│  ├────────────────────────────────────────────────────┤  │
│  │  [00:45:20] We're in the singularity.              │  │
│  │  [00:45:23] It's like the top of the roller    ◀── │  │
│  │  [00:45:28] And it's going to be a lot of G's      │  │
│  ├────────────────────────────────────────────────────┤  │
│  │  章节: [3/12] AGI Timeline                         │  │
│  │  标记: 2 个重点 | 1 条语音笔记                      │  │
│  ├────────────────────────────────────────────────────┤  │
│  │  [j]下句 [k]上句 [space]暂停 [n]下章 [p]上章       │  │
│  │  [m]标记重点 [v]语音笔记 [?]提问 [q]退出           │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
          │
          ▼ (IPC Socket)
┌──────────────────────────────────────────────────────────┐
│                    mpv (后台进程)                         │
│  --input-ipc-server=/tmp/deep-reading-mpv.sock           │
└──────────────────────────────────────────────────────────┘
```

#### 3.2.2 核心功能

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 播放/暂停 | `Space` | 切换播放状态 |
| 跳转下一句 | `j` | 基于字幕时间戳 |
| 跳转上一句 | `k` | 基于字幕时间戳 |
| 下一章节 | `n` | 语义分割的章节 |
| 上一章节 | `p` | 语义分割的章节 |
| 调整倍速 | `[` / `]` | 0.5x - 3.0x |
| 标记重点 | `m` | 记录当前时间点 |
| 语音笔记 | `v` | 录音 + 转文字 |
| 提问 | `?` | 基于上下文向 AI 提问 |
| 跳到干货 | `h` | 跳转到下一个高亮片段 |

#### 3.2.3 语义章节跳转

AI 预处理时自动识别章节：

```json
{
  "chapters": [
    {"start": 0, "end": 180, "title": "开场介绍", "type": "intro"},
    {"start": 180, "end": 1200, "title": "AGI 时间线预测", "type": "core"},
    {"start": 1200, "end": 1800, "title": "广告/闲聊", "type": "skip"},
    {"start": 1800, "end": 3600, "title": "中国 vs 美国", "type": "core"}
  ]
}
```

"只听干货"模式自动跳过 `type: skip` 的章节。

### 3.3 AI Processor (AI 处理模块)

#### 3.3.1 处理流程

```
内容获取完成
    ↓
┌─────────────────────────────────────────┐
│  Stage 1: 快速预处理 (立即完成)          │
│  - 语义章节分割                          │
│  - 关键时间点识别 (高亮片段)              │
│  - 基础元数据提取                        │
└────────────────┬────────────────────────┘
                 ↓
         用户可以开始播放
                 ↓
┌─────────────────────────────────────────┐
│  Stage 2: 深度分析 (后台进行)            │
│  - 检视阅读报告生成                      │
│  - 概念卡片拆分                          │
│  - 双链关系识别                          │
│  - 与已有笔记关联                        │
└────────────────┬────────────────────────┘
                 ↓
         播放结束时呈现完整分析
                 ↓
┌─────────────────────────────────────────┐
│  Stage 3: 用户审核 (交互)                │
│  - 展示 AI 生成的卡片和链接              │
│  - 合并用户的标记和语音笔记              │
│  - 确认/修改后写入 Obsidian              │
└─────────────────────────────────────────┘
```

#### 3.3.2 AI 任务清单

| 任务 | 触发时机 | 输出 |
|------|----------|------|
| 语义分割 | 下载完成后立即 | chapters.json |
| 干货识别 | 下载完成后立即 | highlights.json |
| 检视阅读 | 后台/播放中 | 主笔记草稿 |
| 概念提取 | 后台/播放中 | 概念卡片草稿 |
| 双链匹配 | 笔记生成后 | 链接建议 |
| Q&A 响应 | 用户按 `?` 时 | 实时回答 |

#### 3.3.3 上下文感知 Q&A

用户播放时按 `?` 提问，AI 能访问：

```python
context = {
    "current_position": "00:45:23",
    "recent_transcript": "最近 2 分钟的文字",
    "full_transcript": "完整转录文本",
    "user_marks": ["00:30:00 - 重要", "00:42:15 - 有疑问"],
    "existing_notes": ["[[AGI]]", "[[Elon Musk]]"],  # vault 中相关笔记
}
```

### 3.4 Note Manager (笔记管理模块)

#### 3.4.1 Obsidian Vault 结构

```
/Users/liweixin/smart notes/DeepReading/
│
├── Sources/                           # 主笔记 (来源概览)
│   ├── Elon Musk AGI 访谈.md
│   ├── Lex Fridman - Sam Altman.md
│   └── ...
│
├── Cards/                             # 概念卡片 (原子化知识)
│   ├── AGI 时间线.md
│   ├── 三重指数增长.md
│   ├── Kardashev 文明等级.md
│   └── ...
│
└── _meta/                             # 元数据 (可选，隐藏)
    ├── processing_queue.md            # 待处理队列
    └── link_suggestions.md            # 待确认的链接建议
```

#### 3.4.2 主笔记模板 (Sources/)

```markdown
---
source_type: youtube
source_url: https://youtube.com/watch?v=RSNuB9pj9P8
title: Elon Musk on AGI Timeline
author: Peter Diamandis
duration: "2:52:10"
date_consumed: 2026-01-21
tags: [AI, AGI, Elon-Musk, podcast]
status: reviewed
---

# Elon Musk on AGI Timeline

## 元信息
- **来源**: [YouTube](https://youtube.com/watch?v=RSNuB9pj9P8)
- **时长**: 2:52:10
- **消费日期**: 2026-01-21

## 核心观点
1. AGI 将在 2026 年实现 → [[AGI 时间线]]
2. 三重指数增长驱动机器人发展 → [[三重指数增长]]
3. 中国将在 AI 算力上超越美国 → [[中美 AI 竞争]]

## 我的标记
- [00:45:23] ⭐ "We're in the singularity" - 这个判断很大胆
- [01:23:45] ❓ 关于 UHI 的说法需要更多证据

## 我的笔记
> 听完后的感想：Elon 的乐观主义有其逻辑基础...

## 相关卡片
- [[AGI 时间线]]
- [[三重指数增长]]
- [[Optimus 机器人]]
- [[太阳能 vs 核聚变]]

## 相关来源
- [[Sam Altman 谈 AGI]] - 对比观点
- [[Geoffrey Hinton 的担忧]] - 反方观点
```

#### 3.4.3 概念卡片模板 (Cards/)

```markdown
---
type: concept
created: 2026-01-21
sources:
  - "[[Elon Musk AGI 访谈]]"
  - "[[Sam Altman 谈 AGI]]"
tags: [AI, prediction, timeline]
---

# AGI 时间线

## 定义
AGI (Artificial General Intelligence) 指能够执行任何人类智力任务的 AI 系统。

## 各方预测

| 人物 | 预测时间 | 来源 |
|------|----------|------|
| Elon Musk | 2026 | [[Elon Musk AGI 访谈]] |
| Sam Altman | 2027-2028 | [[Sam Altman 谈 AGI]] |
| Demis Hassabis | 2030 | [[DeepMind 访谈]] |

## 关键论据
- Musk: 算法效率每年提升 10x
- Altman: 需要新的架构突破

## 我的思考
> ...

## 相关概念
- [[ASI]] - 超级人工智能
- [[技术奇点]]
- [[AI 安全]]
```

#### 3.4.4 自动双链策略

AI 自动创建链接的规则：

```python
linking_rules = {
    # 1. 概念匹配：卡片标题出现在文本中
    "concept_match": {
        "text": "Elon 预测 AGI 将在 2026 年实现",
        "cards": ["AGI", "AGI 时间线"],
        "action": "link_first_match"  # → [[AGI 时间线]]
    },

    # 2. 语义相似：embedding 相似度 > 0.85
    "semantic_match": {
        "new_card": "三重指数增长",
        "similar_cards": ["复合增长", "指数思维"],
        "action": "suggest_link"  # 建议链接，用户确认
    },

    # 3. 共同来源：多个卡片引用同一来源
    "co_reference": {
        "source": "Elon Musk AGI 访谈",
        "cards": ["AGI", "Optimus", "UHI"],
        "action": "create_see_also"  # 在各卡片添加 See Also
    }
}
```

---

## 4. 用户工作流

### 4.1 完整使用流程

```
                    ┌─────────────────────────┐
                    │  1. 输入内容来源         │
                    │  dr https://youtube...  │
                    └───────────┬─────────────┘
                                ↓
                    ┌─────────────────────────┐
                    │  2. 自动下载 + 预处理    │
                    │  (进度条显示)            │
                    └───────────┬─────────────┘
                                ↓
          ┌─────────────────────┴─────────────────────┐
          ↓                                           ↓
┌─────────────────────┐                   ┌─────────────────────┐
│  3a. 开始播放       │                   │  3b. 后台深度分析    │
│  (TUI Player)       │                   │  (AI 处理)          │
│                     │                   │                     │
│  - 边听边标记       │      并行进行      │  - 生成检视报告     │
│  - 语音笔记         │  ←───────────→    │  - 拆分概念卡片     │
│  - 随时提问         │                   │  - 识别双链关系     │
└─────────┬───────────┘                   └──────────┬──────────┘
          │                                          │
          └─────────────────┬────────────────────────┘
                            ↓
                ┌─────────────────────────┐
                │  4. 播放结束/手动触发    │
                │  呈现完整分析结果        │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │  5. 用户审核界面         │
                │                         │
                │  [✓] 概念卡片 1          │
                │  [✓] 概念卡片 2          │
                │  [ ] 概念卡片 3 (删除)   │
                │  [~] 修改链接建议        │
                │                         │
                │  [确认] [编辑] [稍后]    │
                └───────────┬─────────────┘
                            ↓
                ┌─────────────────────────┐
                │  6. 写入 Obsidian Vault │
                │  → 主笔记 + 概念卡片     │
                │  → 自动创建双链          │
                └─────────────────────────┘
```

### 4.2 命令接口设计

```bash
# 主命令
dr <url>                    # 下载并进入播放模式
dr play <source_id>         # 播放已缓存内容
dr status                   # 查看处理状态
dr review                   # 进入审核界面
dr search <keyword>         # 搜索已有笔记

# 播放控制 (TUI 内)
# 见 3.2.2 快捷键表

# 管理命令
dr cache list               # 列出缓存内容
dr cache clean              # 清理过期缓存
dr config                   # 配置设置
```

---

## 5. 数据模型

### 5.1 SQLite 数据库

```sql
-- 内容来源
CREATE TABLE sources (
    id TEXT PRIMARY KEY,              -- youtube_RSNuB9pj9P8
    type TEXT NOT NULL,               -- youtube, podcast, web
    url TEXT,
    title TEXT,
    author TEXT,
    duration INTEGER,                 -- 秒
    cache_path TEXT,                  -- ~/.deep-reading/cache/...
    processing_state TEXT,            -- pending, processing, ready, reviewed
    created_at DATETIME,
    updated_at DATETIME
);

-- 章节信息
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY,
    source_id TEXT,
    start_time INTEGER,               -- 秒
    end_time INTEGER,
    title TEXT,
    type TEXT,                        -- intro, core, skip, outro
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- 用户标记
CREATE TABLE marks (
    id INTEGER PRIMARY KEY,
    source_id TEXT,
    timestamp INTEGER,                -- 秒
    type TEXT,                        -- highlight, question, note
    content TEXT,                     -- 语音笔记转文字等
    created_at DATETIME,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- 生成的笔记
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    source_id TEXT,
    type TEXT,                        -- source, card
    title TEXT,
    content TEXT,
    obsidian_path TEXT,               -- vault 中的路径
    status TEXT,                      -- draft, reviewed, synced
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- 链接关系
CREATE TABLE links (
    id INTEGER PRIMARY KEY,
    from_note_id INTEGER,
    to_note_id INTEGER,
    type TEXT,                        -- auto, manual, suggested
    status TEXT,                      -- pending, confirmed, rejected
    FOREIGN KEY (from_note_id) REFERENCES notes(id),
    FOREIGN KEY (to_note_id) REFERENCES notes(id)
);
```

### 5.2 处理状态机

```
┌─────────┐     下载完成      ┌────────────┐
│ pending │ ───────────────→ │ processing │
└─────────┘                   └─────┬──────┘
                                    │
                              预处理完成
                                    ↓
                              ┌──────────┐
                              │  ready   │ ← 可以播放
                              └────┬─────┘
                                   │
                              用户审核完成
                                   ↓
                              ┌──────────┐
                              │ reviewed │ ← 已写入 Obsidian
                              └──────────┘
```

---

## 6. 开发计划

### 6.1 里程碑

| 阶段 | 内容 | 预计时间 |
|------|------|----------|
| **M1: 基础可用** | YouTube 下载 + 简单播放 + 检视阅读 | 1 周 |
| **M2: 播放体验** | TUI Player + 字幕同步 + 快捷键 | 1 周 |
| **M3: AI 集成** | 自动章节分割 + 概念卡片生成 | 1 周 |
| **M4: Obsidian** | 笔记写入 + 双链生成 + 审核界面 | 1 周 |
| **M5: 播客支持** | RSS 解析 + 播客特有功能 | 3 天 |
| **M6: 网页支持** | 网页内容提取 + 阅读模式 | 3 天 |

### 6.2 M1 详细任务

```
□ 重构 fetch-youtube-transcript.sh
  □ 下载音频 (mp3)
  □ 下载字幕 (vtt + txt)
  □ 提取元数据 (json)
  □ 统一缓存结构

□ 基础播放功能
  □ mpv IPC 控制脚本
  □ 播放/暂停/跳转
  □ 显示当前进度

□ 检视阅读集成
  □ 触发 AI 分析
  □ 生成 Markdown 报告
  □ 保存到 Obsidian vault
```

---

## 7. 配置项

```bash
# ~/.deep-reading/config.sh

# Obsidian Vault 路径
OBSIDIAN_VAULT="/Users/liweixin/smart notes"
DEEP_READING_DIR="DeepReading"

# 笔记子目录
SOURCES_DIR="Sources"    # 主笔记 (来源概览)
CARDS_DIR="Cards"        # 概念卡片 (原子化知识)

# 缓存设置
CACHE_DIR="$HOME/.deep-reading/cache"
CACHE_MAX_SIZE="10G"
CACHE_EXPIRE_DAYS=30

# 播放设置
DEFAULT_SPEED=1.0
SUBTITLE_OFFSET=0

# AI 设置
AUTO_PROCESS=true
CARD_MIN_IMPORTANCE=0.7  # 只生成重要度 > 0.7 的卡片

# 语音笔记
VOICE_BACKEND="macos"    # macos | whisper
WHISPER_MODEL="base"     # tiny | base | small | medium

# TUI 设置
THEME="dark"
SHOW_TIMESTAMPS=true
```

---

## 8. 已确认决策

| 问题 | 决策 | 说明 |
|------|------|------|
| **语音笔记** | macOS 原生 + Whisper 可选 | 默认用系统语音识别，需要高准确率时切换 Whisper |
| **跨语言翻译** | P2 可选 | 用户英文能力足够，暂不需要 |
| **AI 配音** | P2 可选 | 后期有空再做 |
| **移动端同步** | 不处理 | 用户已用 GitHub 同步 Obsidian vault |
| **多人协作** | 不需要 | 纯个人工具 |

---

## 9. 附录

### 9.1 相关工具

| 工具 | 用途 | 安装 |
|------|------|------|
| yt-dlp | YouTube 下载 | `brew install yt-dlp` |
| mpv | 音频播放 | `brew install mpv` |
| ffmpeg | 音频处理 | `brew install ffmpeg` |
| jq | JSON 处理 | `brew install jq` |

### 9.2 参考项目

- [spotify-tui](https://github.com/Rigellute/spotify-tui) - TUI 设计参考
- [Obsidian](https://obsidian.md) - 笔记管理
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) - 本地语音转文字
