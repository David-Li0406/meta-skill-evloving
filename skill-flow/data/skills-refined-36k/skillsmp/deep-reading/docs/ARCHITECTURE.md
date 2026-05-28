# Deep Reading v2 代码架构说明

## 项目结构

```
deep-reading/
├── SKILL.md                  # Skill 入口文档
├── pyproject.toml            # Python 项目配置
├── tests/                    # 测试套件 (137 个测试)
│   ├── test_mpv_controller.py
│   ├── test_player_cli.py
│   ├── test_processor_cli.py
│   ├── test_pdf_fetcher.py
│   └── test_youtube.py
│
├── src/                      # 源代码 (~1223 行)
│   ├── models.py             (82 行)   数据模型
│   ├── db.py                 (94 行)   数据库层
│   │
│   ├── fetcher/              # 内容获取模块
│   │   ├── cli.py           (123 行)  统一入口
│   │   ├── youtube.py       (195 行)  YouTube 下载
│   │   └── pdf.py           (169 行)  PDF 解析
│   │
│   ├── player/               # 播放器模块
│   │   ├── cli.py           (132 行)  播放 CLI
│   │   └── mpv_controller.py (235 行) mpv IPC 控制
│   │
│   ├── processor/            # 内容处理模块
│   │   ├── cli.py           (73 行)   处理 CLI
│   │   └── inspectional.py  (120 行)  检视阅读报告
│   │
│   └── notes/                # 笔记模块 (待开发)
│
└── ~/.deep-reading/          # 运行时数据
    ├── config.py             # 配置文件
    ├── cache/
    │   ├── youtube/{id}/     # YouTube 缓存
    │   └── pdf/{id}/         # PDF 缓存
    └── db/deep_reading.db    # SQLite 数据库
```

---

## 模块详解

### 1. 核心层 (`models.py` + `db.py`)

**models.py (82 行)** - 数据模型定义
```python
@dataclass
class Source:
    id: str
    type: SourceType (YOUTUBE, PDF, PODCAST, WEB)
    title: str
    author: str
    duration: int
    cache_path: str
    processing_state: ProcessingState

class Note:
    id: Optional[int]
    source_id: Optional[str]
    type: NoteType (SOURCE, CARD)
    title: str
    content: Optional[str]
    obsidian_path: Optional[str]
    status: NoteStatus
```

**db.py (94 行)** - 数据库操作
- 初始化 SQLite 数据库
- FTS5 全文搜索支持
- 五张表：sources, chapters, marks, notes, links

---

### 2. Fetcher 模块 (`fetcher/`)

**统一入口：cli.py**
```python
def fetch(path_or_url: str):
    source_type = detect_source_type(path_or_url)
    if source_type == "youtube":
        result = fetch_youtube(path_or_url)
    elif source_type == "pdf":
        result = fetch_pdf(path_or_url)
    # 保存到数据库
```

**youtube.py (195 行)** - YouTube 下载
- 使用 yt-dlp 下载音频和字幕
- 清理 VTT 字幕为纯文本
- 提取元数据（标题、作者、时长）

**pdf.py (169 行)** - PDF 解析
- 使用 PyMuPDF 提取文本
- 提取 PDF 元数据
- 生成唯一 ID（MD5 hash）

---

### 3. Player 模块 (`player/`)

**mpv_controller.py (235 行)** - mpv IPC 控制
```python
class MpvController:
    def start(audio_path)      # 启动 mpv 进程
    def play() / pause()       # 播放控制
    def seek(seconds)          # 跳转
    def seek_to(position)      # 跳转到位置
    def speed_up() / down()    # 变速
    def get_position()         # 获取进度
    def stop()                 # 停止并清理
```

**cli.py (132 行)** - 交互式播放器
- 终端键盘控制（空格、j/k、J/K、+/-、q）
- 实时进度显示
- 自动检测播放结束

---

### 4. Processor 模块 (`processor/`)

**inspectional.py (120 行)** - 检视阅读报告生成
```python
def generate_inspectional_report(
    source_id, title, author, url, duration,
    transcript, source_type="youtube"
) -> str:
    # 生成 Markdown 格式报告
    # 包含：元信息、摘要、核心观点、关键概念、思考问题
```

**cli.py (73 行)** - 处理入口
```python
def process_source(source_id: str):
    # 从数据库读取源信息
    # 读取 transcript.txt 或 content.txt
    # 生成报告
    # 保存到 Obsidian
```

---

## 数据流

```
┌─────────────────┐
│   用户输入       │
│ (URL 或 PDF 路径)│
└────────┬─────────┘
         │
         ▼
┌─────────────────────────────┐
│   fetcher/cli.py            │
│   detect_source_type()      │
└────────┬────────────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────┐  ┌──────┐
│youtube│  │ pdf  │
│.py   │  │.py   │
└──┬───┘  └──┬───┘
   │         │
   └────┬────┘
        ▼
┌─────────────────┐
│   SQLite DB     │
│  (sources 表)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│   processor/cli.py          │
│   process_source()          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Obsidian Vault              │
│ ~/smart notes/DeepReading/  │
└─────────────────────────────┘
```

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Python 3.11+ |
| 数据库 | SQLite + FTS5 |
| YouTube 下载 | yt-dlp |
| PDF 解析 | PyMuPDF (fitz) |
| 音频播放 | mpv + IPC socket |
| 笔记格式 | Markdown (Obsidian) |
| 测试 | pytest + coverage (98%) |

---

## 扩展点

**计划中但尚未实现的功能**：

```
fetcher/
├── podcast.py      # M5: 播客支持
└── web.py          # M6: 网页支持

processor/
├── analytical.py   # 分析阅读报告
├── comparative.py  # 对比阅读报告
└── chapter_split.py # M3: AI 章节分割

notes/
├── cli.py          # 笔记管理 CLI
└── card_generator.py # M3: 概念卡片生成
```

---

## 设计理念

当前架构的核心设计理念是**模块化**和**可扩展性**：

1. **独立的 Fetcher** - 每种内容源（YouTube、PDF）都有独立的 fetcher 模块
2. **独立的 Processor** - 每种处理级别（检视、分析、对比）都有独立的 processor
3. **统一的 CLI 入口** - 通过 `cli.py` 统一调度各模块
4. **集中的数据模型** - 通过 SQLite 数据库和 `models.py` 连接各模块
5. **外部配置** - 运行时配置存放在 `~/.deep-reading/config.py`

---

## 文件统计

| 模块 | 文件数 | 代码行数 |
|------|--------|----------|
| 核心 (models, db) | 2 | 176 |
| fetcher | 3 | 487 |
| player | 2 | 367 |
| processor | 2 | 193 |
| **总计** | **9** | **~1223** |

测试覆盖率：**98%** (137 个测试用例)
