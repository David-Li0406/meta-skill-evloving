# 竞品分析工作流

## 概述
本工作流定义了如何在对操作系统类需求分析、可行性评估及规范设计过程中引入业界标杆系统（Android/iOS/Windows）的技术参考，提升技术选型和 API 设计质量。

## 适用场景
- 涉及新子系统设计
- 涉及 API 设计（尤其是开发者直接使用的接口）
- 涉及性能优化、安全机制、架构设计
- 用户明确要求参考竞品
- Dispatcher 在需求分类时标记 `needs_competitive_analysis: true`

## 工作流程

### 步骤1：识别需求类型
分析用户需求，识别需要参考的技术领域：

| 需求类型 | 参考领域 | 优先级平台 |
|---------|---------|-----------|
| API 设计 | api-design.md | Android >= iOS/macOS > Windows |
| 性能优化 | performance.md | Android > iOS/macOS |
| 安全机制 | security.md | iOS/macOS > Android > Windows |
| 架构设计 | architecture.md | Android > Windows |
| 企业特性 | enterprise.md | Windows |
| 开发者体验 | developer-experience.md | iOS/macOS > Windows |

### 步骤2：查询本地知识库
优先从本地知识库获取信息：

```bash
# 知识库路径
KNOWLEDGE_BASE=".claude/ohspec/knowledge-base"

# 根据需求类型查询对应文档
# 例如：API 设计需求
- ${KNOWLEDGE_BASE}/android/api-design.md
- ${KNOWLEDGE_BASE}/ios-macos/api-design.md
- ${KNOWLEDGE_BASE}/windows/architecture.md（如涉及架构）
```

### 步骤3：调用外部工具（按需）
如果本地知识库不足，按以下优先级使用外部工具：

#### 3.1 使用 context7 查询官方文档
**优先级：最高**

```python
# 查询 Android 官方文档
context7.resolve_library_id(
    query="Android API 设计最佳实践",
    libraryName="android"
)
library_id = "/android/docs"  # 获取到的库 ID

context7.query_docs(
    libraryId=library_id,
    query="API naming conventions and best practices"
)
```

**适用场景**：
- 需要最新的官方文档和最佳实践
- 查询具体 API 使用方法
- 了解框架设计理念

#### 3.2 使用 github.search_code 搜索开源实现
**优先级：中**

```python
# 搜索 Android 开源实现
github.search_code(
    query="AudioManager 3D sound implementation",
    language="java",
    repo="aosp-mirror/*"
)
```

**适用场景**：
- 需要参考实际代码实现
- 学习设计模式和架构
- 了解性能优化技巧

#### 3.3 使用 firecrawl 搜索技术博客和文章
**优先级：低（作为补充）**

```python
# 搜索技术文章
firecrawl.search(
    query="Android 3D audio best practices 2025",
    scrapeOptions={
        "formats": ["markdown"],
        "onlyMainContent": True
    }
)
```

**适用场景**：
- 需要社区最佳实践
- 了解常见问题和解决方案
- 获取最新技术趋势

### 步骤4：多源降级策略
处理工具调用失败或限流情况：

```python
def fetch_competitive_analysis(query, platform):
    """多源降级策略"""
    results = []

    # 优先级 1：本地知识库（必定成功）
    local_docs = load_knowledge_base(platform, query_type)
    results.append(local_docs)

    # 优先级 2：context7（官方文档）
    try:
        context7_results = query_context7(platform, query)
        results.append(context7_results)
    except RateLimitError:
        log_warning("context7 限流，跳过")

    # 优先级 3：github.search_code（开源实现）
    try:
        github_results = search_github_code(query, platform)
        results.append(github_results)
    except RateLimitError:
        log_warning("GitHub API 限流，跳过")

    # 优先级 4：firecrawl（技术博客）
    try:
        firecrawl_results = search_firecrawl(query)
        results.append(firecrawl_results)
    except Exception:
        log_warning("firecrawl 失败，跳过")

    return merge_results(results)
```

### 步骤5：合并和输出结果
将多个来源的信息整合，输出到 `findings.json`：

```markdown
## 竞品分析

### Android
**来源**：本地知识库 + Android 官方文档

#### API 设计原则
1. **一致性**：动词开头表示动作（如 enable、disable）
   - 参考：AudioManager.setStreamVolume()
   - 文件：knowledge-base/android/api-design.md

2. **易用性**：Builder 模式简化复杂对象构建
   - 示例：NotificationCompat.Builder
   - 参考：https://developer.android.com/reference/...

#### 性能最佳实践
1. **避免阻塞主线程**：使用异步 API
   - 参考：AudioTrack 异步模式
   - 代码示例：[GitHub AOSP 链接]

### iOS/macOS
**来源**：本地知识库 + Apple 开发者文档

#### API 设计原则
1. **清晰性**：方法名描述其作用和效果
   - 示例：insert(_:at:) vs remove(_:)
   - 参考：Swift API Design Guidelines

2. **类型安全**：利用 Swift 类型系统
   - 示例：使用 Optional 表达"可能没有值"

### 关键发现总结
1. **跨平台共识**：
   - 所有平台都强调 API 命名的清晰性和一致性
   - 异步操作是处理耗时任务的标准做法

2. **差异化特性**：
   - Android：Builder 模式广泛应用
   - iOS/macOS：类型安全和 Swift 语言特性
   - Windows：企业级特性和兼容性

3. **对 OpenHarmony 的建议**：
   - 采用清晰的命名约定（动词+名词）
   - 提供异步 API 和回调机制
   - 学习 Builder 模式简化复杂配置
```

## 质量标准
- ✅ 至少参考 2 个竞品平台
- ✅ 包含具体代码示例或 API 引用
- ✅ 说明设计理由（为什么这样设计）
- ✅ 总结跨平台共识和差异
- ✅ 提供对 OpenHarmony 的具体建议

## 注意事项
1. **避免照搬**：理解设计理念，而非简单复制 API
2. **结合实际**：考虑 OpenHarmony 的技术栈和生态
3. **保持中立**：客观分析优劣，不盲目推崇某个平台
4. **控制范围**：聚焦当前需求，避免发散到无关领域
5. **尊重限流**：遇到 API 限流时使用降级策略，不重复请求

## 配置参数
参考 `config.yaml` 中的 `competitive_analysis` 配置：

```yaml
competitive_analysis:
  enabled: true
  target_platforms: [Android, iOS/macOS, Windows]
  query_strategy:
    max_results_per_platform: 3  # 每个平台最多返回 3 个结果
    timeout: 60                   # 查询超时 60 秒
    cache_ttl: 86400             # 缓存 24 小时
    fallback_on_error: true      # 失败时回退到本地知识库
```

## 输出物
- 更新 `findings.json` 的"竞品分析"章节
- 包含来源标注（本地知识库、context7、GitHub、firecrawl）
- 包含具体引用和链接（可追溯）
