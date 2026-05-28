# Best Practices and Common Mistakes

## Common Mistakes

### Mistake 1: Skip Code Scanning and Ask Directly

❌ **Wrong Approach**: Directly ask user "How do you want to implement?"

✅ **Correct Approach**: First use Grep/Glob to scan codebase, provide option-based questions based on existing implementations

**Why**: Based on code facts rather than guesses, reduces user burden

### Mistake 2: Vague DFX Descriptions

❌ **Wrong Approach**:
- "Requires permission"
- "Data encryption"
- "Good performance"

✅ **Correct Approach**: Quantify specific requirements
- Permission: `ohos.permission.MANAGE_AUDIO`, validated via `PermissionManager.check()`
- Encryption: AES-256, keys stored in KeyStore
- Performance: p99 latency < 10ms, supports 8 concurrent streams

**Why**: Vague descriptions cannot be verified or implemented

### Mistake 3: Incomplete Scenario Coverage

❌ **Wrong Approach**: Only write normal scenarios

✅ **Correct Approach**: Must include normal/exception/boundary/unsupported scenarios, use Gherkin format

**Example**:
```markdown
#### Normal Scenario
#### Scenario: Enable 3D sound effect
- **GIVEN** User has MANAGE_AUDIO permission
- **WHEN** Call enable3DSound()
- **THEN** 3D sound effect enabled, return success

#### Exception Scenario
#### Scenario: Insufficient permission
- **GIVEN** User lacks MANAGE_AUDIO permission
- **WHEN** Call enable3DSound()
- **THEN** Return PERMISSION_DENIED error

#### Boundary Scenario
#### Scenario: Concurrent switching
- **GIVEN** 3D sound effect already enabled
- **WHEN** Multiple threads call enable3DSound() simultaneously
- **THEN** Only one call succeeds, others return ALREADY_ENABLED

#### Unsupported Scenario
#### Scenario: Device not supported
- **GIVEN** Device doesn't support 3D sound effect
- **WHEN** Call enable3DSound()
- **THEN** Return NOT_SUPPORTED error
- **REASON** Hardware limitation
```

### Mistake 4: Non-Intuitive API Design

❌ **Wrong Approach**:
```typescript
setMode(3);  // What does 3 mean?
process(data, true, false, 100);  // What are the boolean parameters?
```

✅ **Correct Approach**:
```typescript
enable3DSound();  // Self-explanatory
process(data, { mode: 'async', retry: true, timeout: 100 });  // Object parameters
```

**Why**: Intuitive APIs reduce errors and improve developer experience

### Mistake 5: Ignoring Context Budget

❌ **Wrong Approach**: Load all expert Personas in main context

✅ **Correct Approach**: Use Task tool to launch independent subagents, each expert in isolated context

**Why**: Avoid context overflow, improve performance

### Mistake 6: Orchestrator Executes Work Instead of Delegating

❌ **Wrong Approach**: Orchestrator 直接使用 Grep/Glob/Read 扫描代码库（默认路径）
```python
# Scan directly in main thread
grep_result = Grep(pattern="keyword", output_mode="files_with_matches")
files = Glob(pattern="**/*.ts")
content = Read(file_path="src/example.ts")

# Orchestrator analyzes and generates result itself
analysis = analyze_code(grep_result, files, content)
```

✅ **Correct Approach**: Use Task tool to launch dispatcher subagent to execute scanning
```python
# Launch dispatcher subagent
dispatcher_result = Task(
    subagent_type="Explore",
    description="Dispatcher analyzes requirements",
    model="haiku",
    prompt=f"""
You are now the **Dispatcher** of the OHSpec expert team.

## Your Tasks
1. Use Grep/Glob to scan codebase
2. Assess complexity level
3. Select expert combination
4. Generate analysis result summary (JSON format)

## Output Requirements
Only return JSON format summary information (~2k tokens)
"""
)

# Orchestrator only parses result and presents
analysis = json.loads(dispatcher_result)
```

**Why**:
- Avoid main thread context consumption (save 19k-59k tokens)
- Code scanning executes in independent 200k token context
- Orchestrator only handles key summary information, keeps main context clean
- Aligns with core principle "orchestrator coordinates, subagent executes"

**Exception (Codex compatibility)**:
- When Task is unavailable, orchestrator may run **minimal fallback scan**:
  - Use rg/ag/grep to collect candidate key files with roles (entry/config/dependency/test/observability)
  - Present candidates for quick confirmation (keep/remove) before proceeding
  - Record fallback in progress.json.audit_log/tooling
  - Do **not** invent settings keys or APIs without evidence

### Mistake 7: 设计阶段包含实现代码

❌ **错误做法**：在 RFC 设计阶段编写完整实现
```cpp
// 在 RFC §5 中写了完整实现
int32_t AudioEffect::Enable() {
    std::lock_guard<std::mutex> lock(mutex_);
    if (state_ == State::ENABLED) {
        return ERR_ALREADY_ENABLED;
    }
    state_ = State::ENABLED;
    NotifyListeners();
    return SUCCESS;
}
```

✅ **正确做法**：用契约表/数据字典表达接口，必要时提供极少量调用示意（≤2 行）

**示例（表格替代代码）**：
| 接口 | 参数 | 返回/错误码 | 说明 |
|------|------|------------|------|
| Enable() | 无 | SUCCESS / ERR_ALREADY_ENABLED | 开启 3D 音效 |
| IsEnabled() | 无 | true / false | 查询状态 |

**原因**：
- 设计阶段聚焦"做什么"，实现阶段聚焦"怎么做"
- 过早固化实现细节会限制后续优化空间
- 接口签名是契约，实现代码是细节

**设计阶段允许的内容**：
- 规则清单/契约表/矩阵（优先）
- 接口签名/数据结构（尽量表格化）
- 调用示意（最多 1-2 行，非完整代码）
- 开发者心智模型描述
- 图示（COMPLEX 必须，MEDIUM 建议，SIMPLE 可选）

**设计阶段禁止的内容**：
- 完整函数实现
- 业务逻辑代码
- 内部算法实现
- 私有方法实现

## Advanced Usage

### Custom Expert Combination

Add new experts or adjust trigger conditions by modifying `config.yaml`:

```yaml
experts:
  extension:
    - name: "New Expert"
      trigger: "Trigger condition"
      role: "Role description"
```

### Extend DFX Dimensions

Add new inspection dimensions and rules in `personas/core/auditor-core.md`（必要时同步到 `personas/full/auditor.md`）:

```markdown
### 9. New Dimension
| Check Item | Level | Review Points |
|-----------|-------|--------------|
| Check Item 1 | ❌ error | Review points |
```

### Integrate External Tools

Reference external validation tools or test frameworks in `workflows/`:

```markdown
## Step X: Run External Tool
Use Bash tool to execute:
```bash
./external-tool --config config.yaml
```
```
