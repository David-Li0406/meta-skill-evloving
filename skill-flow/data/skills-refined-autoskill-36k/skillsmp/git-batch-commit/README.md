# Git Batch Commit Optimizer

**Version:** 1.0.0
**License:** MIT
**Category:** Version Control / Git Workflow Optimization

---

## Overview

The Git Batch Commit skill intelligently detects when too many files are staged for commit and automatically organizes them into logical, feature-based batches with Conventional Commit messages. It supports multilingual commit messages and smart threshold-based analysis.

---

## Key Features

✅ **Smart Threshold Detection** - Automatically detects when staging area has too many files
✅ **Intelligent Grouping** - Groups files by feature/functionality, not just directory structure
✅ **Conventional Commits** - Generates standardized commit messages (feat/fix/docs/refactor/chore/style/test/perf)
✅ **Multilingual Support** - Commit messages in English, Chinese, Spanish, Japanese, French, German
✅ **Change Analysis** - Analyzes git diff to understand file modifications
✅ **Dry-run Mode** - Preview batches before committing
✅ **Safety Features** - Validation, conflict detection, rollback support

---

## Installation

### Claude Code (Recommended)

**Project-level installation:**
```bash
# Copy skill folder to project
cp -r git-batch-commit /path/to/your/project/.claude/skills/

# Or clone from repository
git clone https://github.com/your-repo/git-batch-commit .claude/skills/git-batch-commit
```

**User-level installation:**
```bash
# Install globally for all projects
cp -r git-batch-commit ~/.claude/skills/

# Or create symlink
ln -s /path/to/git-batch-commit ~/.claude/skills/git-batch-commit
```

### Claude Apps

1. Import the skill folder or ZIP file
2. Claude will automatically detect and load the skill
3. Use the skill by mentioning git batch commits in your request

### API Integration

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# Load skill
with open(".claude/skills/git-batch-commit/SKILL.md") as f:
    skill_content = f.read()

# Use in message
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Analyze my git repo and create batch commits"}
    ],
    system=skill_content
)
```

---

## Quick Start

### Basic Usage

```bash
# 1. Stage your files
git add .

# 2. Ask Claude to batch commit
"Hey Claude, analyze my git staging area and create appropriate batch commits"
```

### With Language Preference

```bash
"Create batch commits in Chinese for all staged files"
# Output: feat(auth): 新增OAuth2认证功能
```

### With Custom Threshold

```bash
"Use a threshold of 15 files and batch my commits"
```

### Dry-run Preview

```bash
"Preview batch commits without executing"
```

---

## File Structure

```
git-batch-commit/
├── SKILL.md                    # Main skill definition with YAML frontmatter
├── README.md                   # This file
├── HOW_TO_USE.md              # Detailed usage examples
├── git_analyzer.py            # Git status/diff analysis module
├── batch_committer.py         # Batch commit generation and execution
├── commit_language.py         # Multilingual message generation
├── sample_input.json          # Example input data
├── expected_output.json       # Example output structure
└── git_batch_config.json      # Optional configuration file
```

---

## Python Modules

### 1. git_analyzer.py

**Purpose:** Analyzes git repository state and categorizes file changes

**Key Classes:**
- `GitAnalyzer` - Main analyzer class

**Key Methods:**
- `get_git_status()` - Get staged/modified/untracked files
- `analyze_file_changes(filepath)` - Analyze changes in specific file
- `group_files_by_feature(files)` - Group files by functionality
- `should_batch(file_count)` - Determine if batching is needed
- `analyze_repository()` - Complete repository analysis

**Usage:**
```python
from git_analyzer import GitAnalyzer

analyzer = GitAnalyzer(threshold=10)
result = analyzer.analyze_repository()
print(f"Total files: {result['batch_analysis']['total_files']}")
print(f"Batching needed: {result['batch_analysis']['requires_batching']}")
```

---

### 2. batch_committer.py

**Purpose:** Generates Conventional Commit messages and executes batch commits

**Key Classes:**
- `BatchCommitter` - Main committer class

**Key Methods:**
- `generate_commit_message(type, scope, files, lang)` - Generate commit message
- `create_batch_plan(analysis)` - Create execution plan
- `stage_files(files)` - Stage specific files
- `commit(message)` - Create commit
- `execute_batch_commits(plans)` - Execute all batches
- `preview_batch_commits(plans)` - Preview without executing

**Usage:**
```python
from batch_committer import BatchCommitter
from git_analyzer import GitAnalyzer

analyzer = GitAnalyzer()
analysis = analyzer.analyze_repository()

committer = BatchCommitter(language='en', dry_run=True)
plans = committer.create_batch_plan(analysis)
print(committer.preview_batch_commits(plans))
```

---

### 3. commit_language.py

**Purpose:** Handles multilingual commit message generation

**Key Classes:**
- `CommitLanguageHandler` - Language management

**Supported Languages:**
- English (en)
- Chinese (zh)
- Spanish (es)
- Japanese (ja)
- French (fr)
- German (de)
- Korean (ko)
- Russian (ru)
- Portuguese (pt)

**Key Methods:**
- `detect_language_preference(text)` - Auto-detect language
- `get_commit_type_name(type, lang)` - Localized commit type names
- `get_action_verb(type, lang)` - Action verbs by language
- `format_commit_message(...)` - Complete message formatting
- `get_language_examples(lang)` - Example messages

**Usage:**
```python
from commit_language import CommitLanguageHandler

handler = CommitLanguageHandler(default_language='zh')

message = handler.format_commit_message(
    commit_type='feat',
    scope='auth',
    description='新增OAuth2登录支持',
    language='zh'
)
print(message)  # feat(auth): 新增OAuth2登录支持
```

---

## Configuration

### Optional Configuration File

Create `git_batch_config.json` in your repository root:

```json
{
  "threshold": 10,
  "default_language": "en",
  "preferred_scopes": ["auth", "api", "ui", "database", "core"],
  "commit_types": ["feat", "fix", "docs", "refactor", "chore", "style", "test", "perf"],
  "auto_execute": false
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `threshold` | integer | 10 | Max files before batching recommended |
| `default_language` | string | "en" | Default commit message language |
| `preferred_scopes` | array | [] | Project-specific scopes |
| `commit_types` | array | all | Allowed commit types |
| `auto_execute` | boolean | false | Auto-commit without preview ⚠️ |

---

## Conventional Commit Types

| Type | Purpose | Example |
|------|---------|---------|
| **feat** | New feature | `feat(auth): add OAuth2 login support` |
| **fix** | Bug fix | `fix(api): resolve null pointer in endpoint` |
| **docs** | Documentation | `docs(readme): update installation guide` |
| **refactor** | Code restructuring | `refactor(db): optimize query performance` |
| **chore** | Maintenance | `chore(deps): update dependencies` |
| **style** | Formatting | `style(ui): format component styles` |
| **test** | Tests | `test(auth): add OAuth unit tests` |
| **perf** | Performance | `perf(api): optimize response caching` |

---

## Scope Detection

The skill automatically detects scopes based on file paths:

| File Path | Detected Scope | Example |
|-----------|----------------|---------|
| `src/auth/*` | auth | `feat(auth): ...` |
| `src/api/*` | api | `feat(api): ...` |
| `src/ui/*` or `frontend/*` | ui | `feat(ui): ...` |
| `src/database/*` or `models/*` | database | `feat(database): ...` |
| `tests/*` | tests | `test(tests): ...` |
| `docs/*` | docs | `docs(docs): ...` |
| `config/*` | config | `chore(config): ...` |

---

## Language-Specific Examples

### English
```
feat(auth): add OAuth2 authentication functionality
fix(api): resolve null pointer exception in user endpoint
docs(readme): update installation instructions
refactor(database): optimize query performance
```

### Chinese (中文)
```
feat(auth): 新增OAuth2认证功能
fix(api): 修复用户接口空指针异常
docs(readme): 更新安装说明
refactor(database): 优化查询性能
```

### Japanese (日本語)
```
feat(auth): OAuth2認証機能を追加
fix(api): ユーザーエンドポイントのnullポインタ例外を修正
docs(readme): インストール手順を更新
refactor(database): クエリパフォーマンスを最適化
```

---

## Best Practices

### 1. Threshold Tuning

**Small Projects (< 100 files):** Use threshold of 5-8
```json
{"threshold": 6}
```

**Medium Projects (100-1000 files):** Use threshold of 10-15
```json
{"threshold": 12}
```

**Large Projects (> 1000 files):** Use threshold of 15-20
```json
{"threshold": 18}
```

### 2. Scope Consistency

Define project-specific scopes upfront:
```json
{
  "preferred_scopes": ["auth", "api", "frontend", "backend", "database", "tests"]
}
```

### 3. Language Consistency

**Team Projects:** Use English for global collaboration
**Personal Projects:** Use your native language
**Open Source:** Stick to English

### 4. Atomic Commits

Each batch should represent one cohesive change:
- ✅ All authentication changes together
- ✅ All documentation updates together
- ❌ Random mix of unrelated files

### 5. Always Review First

Use dry-run mode before executing:
```
"Preview batch commits without executing"
```

---

## Troubleshooting

### Issue: "git: command not found"

**Solution:** Ensure git is installed and in PATH
```bash
# Check git installation
git --version

# Install git if needed (Ubuntu/Debian)
sudo apt-get install git

# Install git (macOS)
brew install git
```

---

### Issue: "No files to commit"

**Solution:** Stage files first
```bash
git add .
# or
git add <specific-files>
```

---

### Issue: Files grouped incorrectly

**Solution:** Override scope detection
```
"Group authentication files separately from API files"
```

Or specify scopes:
```json
{
  "preferred_scopes": ["auth", "user-api", "admin-api"]
}
```

---

### Issue: Commit messages too generic

**Solution:** Provide context
```
"These changes add OAuth2 support with Google and GitHub providers"
```

---

### Issue: Wrong commit type detected

**Solution:** Override commit type
```
"Use 'refactor' type for database optimization changes"
```

---

## Safety & Security

### Safety Features

✅ **Dry-run Mode** - Preview before committing
✅ **Rollback Support** - Can amend or reset commits
✅ **Validation** - Checks for unstaged critical files
✅ **Conflict Detection** - Warns about dependencies across batches
✅ **No Auto-Execute** - Requires explicit confirmation

### Security Considerations

⚠️ **Code Execution** - This skill executes git commands
⚠️ **File Access** - Reads git status and file diffs
⚠️ **Repository Modification** - Creates commits (with permission)

**Recommendation:** Only use in trusted environments. Review all batch plans before execution.

---

## Requirements

- **Git:** Version 2.0 or higher
- **Python:** 3.7+ (for standalone script execution)
- **Claude:** Any Claude product (Apps, Code, API)
- **Operating System:** Windows, macOS, Linux

---

## Examples

### Example 1: Large Refactoring

**Scenario:** 25 files changed across auth, API, and database modules

**Command:**
```
"Analyze my 25 staged files and create batch commits"
```

**Result:**
```
✓ Batch 1: feat(auth) - 8 files
✓ Batch 2: feat(api) - 6 files
✓ Batch 3: refactor(database) - 7 files
✓ Batch 4: docs(readme) - 4 files

Created 4 commits in logical groups
```

---

### Example 2: Multilingual Team

**Scenario:** Chinese developer working on international project

**Command:**
```
"Create batch commits in Chinese with English fallback for documentation"
```

**Result:**
```
✓ feat(auth): 新增OAuth2认证支持
✓ fix(api): 修复用户接口错误
✓ docs(readme): update installation guide (English)
```

---

### Example 3: Custom Grouping

**Scenario:** Want all frontend changes in one commit

**Command:**
```
"Group all UI and component files together, separate from backend"
```

**Result:**
```
✓ Batch 1: feat(ui) - 12 files (all frontend)
✓ Batch 2: feat(api) - 8 files (all backend)
```

---

## Version History

### Version 1.0.0 (2025-01-06)
- ✅ Initial release
- ✅ Smart threshold detection (default: 10 files)
- ✅ Intelligent file grouping by feature
- ✅ Conventional Commits support (feat/fix/docs/refactor/chore/style/test/perf)
- ✅ Multilingual commit messages (9 languages)
- ✅ Dry-run preview mode
- ✅ Scope auto-detection
- ✅ Git diff analysis
- ✅ Safety features (validation, rollback)
- ✅ Configuration file support

---

## Contributing

Contributions welcome! Areas for improvement:
- Additional language support
- Custom scope detection rules
- Integration with git hooks
- GitHub/GitLab template support
- Emoji commit support
- Semantic versioning integration

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Issues:** Report bugs or request features via GitHub Issues
- **Documentation:** See HOW_TO_USE.md for detailed examples
- **Questions:** Ask Claude directly about batch commits

---

## Credits

**Created by:** Claude Code Skills Factory
**Inspired by:** Conventional Commits specification (conventionalcommits.org)
**Built with:** Python 3, Git, Claude AI

---

**Happy Batch Committing! 🚀**
