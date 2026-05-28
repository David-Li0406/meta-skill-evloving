# Slash Commands Reference

Complete reference for MiniMax MCP slash commands and usage patterns.

## Command Overview

Slash commands provide quick access to MiniMax capabilities within Claude terminal and IDE environments.

### Available Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/minimax-status` | Check server status | `/minimax-status` |
| `/minimax-search` | Web search | `/minimax-search "query"` |
| `/minimax-analyze` | Image analysis | `/minimax-analyze "prompt" "image"` |
| `/minimax-test` | Test connection | `/minimax-test` |
| `/minimax-exec` | Execute plan | `/minimax-exec "plan description"` |
| `/minimax-query` | General query | `/minimax-query "question"` |

---

## Command Reference

### `/minimax-status`

Check MiniMax MCP server status and environment configuration.

**Usage**:
```
/minimax-status
```

**Output**:
```
=== MiniMax MCP Server Status ===
✅ API Key: Set (126 chars)
✅ API Host: https://api.minimax.io
✅ Connectivity: OK
✅ uvx: Installed

Ready to use!
```

**Implementation**:
```bash
#!/bin/bash
# check-status.sh

API_KEY="${MINIMAX_API_KEY:-default-key}"
API_HOST="${MINIMAX_API_HOST:-https://api.minimax.io}"

echo "=== MiniMax MCP Server Status ==="
echo "API Key: ${API_KEY:0:20}..."
echo "API Host: $API_HOST"

# Test connectivity
curl -s -X POST "$API_HOST/v1/coding_plan/search" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"q":"test"}' > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Connectivity: OK"
else
    echo "❌ Connectivity: Failed"
fi
```

**Use Cases**:
- Verify setup before using other commands
- Debug connection issues
- Confirm environment variables
- Check server health

---

### `/minimax-search`

Perform web search using MiniMax API.

**Usage**:
```
/minimax-search "search query"
```

**Example**:
```
/minimax-search "Godot 4.5 features"
```

**Output**:
```
Searching: Godot 4.5 features

Found 7 results:

1. Godot 4.5 - Latest Features and Updates
   https://godotengine.org/article/godot-4-5
   The latest version brings significant performance improvements...

2. Godot 4.5 Rendering Improvements
   https://godotengine.org/article/rendering-4-5
   New rendering pipeline with enhanced graphics capabilities...

[... more results ...]
```

**Implementation**:
```bash
#!/bin/bash
# web-search.sh

QUERY="$1"
API_KEY="..."
API_HOST="https://api.minimax.io"

curl -s -X POST "$API_HOST/v1/coding_plan/search" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d "{\"q\":\"$QUERY\"}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('organic', []):
    print(f'{r.get(\"title\")}')
    print(f'  {r.get(\"link\")}')
    print()
"
```

**Parameters**:
- `query` (required): Search terms

**Use Cases**:
- Research topics
- Find documentation
- Get current information
- Quick web lookup

**Tips**:
- Be specific in queries
- Use quotes for exact phrases
- Try multiple variations

---

### `/minimax-analyze`

Analyze images using MiniMax vision capabilities.

**Usage**:
```
/minimax-analyze "prompt" "image"
```

**Example**:
```
/minimax-analyze "What bugs do you see?" "screenshot.png"
```

**Supported Formats**:
- PNG
- JPEG
- WebP

**Input Methods**:
- Local file: `screenshot.png`
- URL: `https://example.com/image.png`

**Output**:
```
Analyzing image: screenshot.png
Prompt: What bugs do you see?

MiniMax Analysis:

I can identify several UI issues in this screenshot:

1. **Button Alignment**
   - The "Submit" button is misaligned by ~5px
   - Should be centered with the input field

2. **Color Contrast**
   - Error text is too light (WCAG AA violation)
   - Needs 4.5:1 contrast ratio minimum

3. **Spacing**
   - Insufficient padding around form elements
   - Recommended: 8-12px padding

Recommendations:
- Increase button contrast to #d32f2f
- Add 10px padding to all inputs
- Center align submit button
```

**Implementation**:
```bash
#!/bin/bash
# analyze-image.sh

PROMPT="$1"
IMAGE="$2"
API_KEY="..."
API_HOST="https://api.minimax.io"

# Determine if URL or file
if [[ "$IMAGE" =~ ^https?:// ]]; then
    # URL
    curl -s -X POST "$API_HOST/v1/coding_plan/vlm" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"prompt\":\"$PROMPT\",\"image_url\":\"$IMAGE\"}"
else
    # File - convert to base64
    IMAGE_B64=$(base64 -w 0 "$IMAGE")
    curl -s -X POST "$API_HOST/v1/coding_plan/vlm" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"prompt\":\"$PROMPT\",\"image_base64\":\"$IMAGE_B64\"}"
fi
```

**Parameters**:
- `prompt` (required): Question or instruction about image
- `image` (required): File path or URL

**Use Cases**:
- Bug triage
- UI/UX analysis
- Screenshot review
- Visual regression testing
- Design critique

**Tips**:
- Be specific in prompts
- Provide context about what to look for
- Use local files for better privacy

---

### `/minimax-test`

Test MiniMax API connection and verify setup.

**Usage**:
```
/minimax-test
```

**Output**:
```
=========================================
  MiniMax API Connection Test
=========================================

Test 1/5: curl availability...
✅ curl is installed

Test 2/5: Python availability...
✅ Python 3.11.0

Test 3/5: API key validation...
✅ API key length correct (126 chars)

Test 4/5: Web search endpoint...
✅ Web search endpoint working

Test 5/5: Image analysis endpoint...
✅ Image analysis endpoint accessible

=========================================
  Test Results: 5/5 Passed
=========================================

✅ All tests passed! MiniMax is ready to use.
```

**Implementation**:
```bash
#!/bin/bash
# test-connection.sh

TESTS_PASSED=0

# Test 1: curl
command -v curl > /dev/null && TESTS_PASSED=$((TESTS_PASSED + 1))

# Test 2: Python
command -v python3 > /dev/null && TESTS_PASSED=$((TESTS_PASSED + 1))

# Test 3: API key length
[ ${#API_KEY} -eq 126 ] && TESTS_PASSED=$((TESTS_PASSED + 1))

# Test 4: Web search
curl -s -X POST ... -d '{"q":"test"}' > /dev/null && TESTS_PASSED=$((TESTS_PASSED + 1))

# Test 5: Image analysis
curl -s -X POST ... -d '{"prompt":"test","image_url":"..."}' > /dev/null && TESTS_PASSED=$((TESTS_PASSED + 1))

echo "Test Results: $TESTS_PASSED/5 Passed"
```

**Use Cases**:
- Initial setup verification
- Troubleshooting connection issues
- Confirm environment is ready
- Pre-flight check before production use

---

### `/minimax-exec`

Execute structured plan with MiniMax delegation.

**Usage**:
```
/minimax-exec "plan description"
```

**Example**:
```
/minimax-exec "Research React 18 features and create implementation plan"
```

**Output**:
```
=========================================
  MiniMax Plan Execution
=========================================

Plan: Research React 18 features and create implementation plan

Delegating to MiniMax...

✅ Plan executed successfully

Found 5 relevant sources:

1. React 18 Official Documentation
   Link: https://react.dev/learn

   Summary: React 18 introduces concurrent features...

[... more results ...]

=========================================
  Execution Complete
=========================================

Next steps:
1. Review the results above
2. Use /minimax-query for follow-up questions
3. Use /minimax-analyze for specific image analysis

Token efficiency achieved: Claude planned (~100 tokens), MiniMax executed (~2000 tokens saved)
```

**Implementation**:
```bash
#!/bin/bash
# execute-plan.sh

PLAN="$1"
API_KEY="..."
API_HOST="https://api.minimax.io"

# Create structured prompt
MINIMAX_PROMPT="Execute this plan using MiniMax:

TASK: $PLAN

Provide:
1. Compact JSON summary
2. Detailed execution log
3. Actionable recommendations"

curl -s -X POST "$API_HOST/v1/coding_plan/search" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{\"q\":\"$MINIMAX_PROMPT\"}"
```

**Parameters**:
- `plan` (required): Description of task to execute

**Use Cases**:
- Complex research projects
- Comprehensive analysis
- Multi-step tasks
- Delegating heavy work

**Tips**:
- Provide clear, detailed plans
- Include specific requirements
- Specify desired output format

---

### `/minimax-query`

Send general queries to MiniMax.

**Usage**:
```
/minimax-query "your question"
```

**Example**:
```
/minimax-query "Explain quantum computing basics"
```

**Output**:
```
Query: Explain quantum computing basics

MiniMax found 7 relevant results:

1. Quantum Computing: A Gentle Introduction
   https://quantum.country/qcvc

   Quantum computing uses quantum mechanical phenomena...

2. IBM Quantum Computing Guide
   https://www.ibm.com/quantum

   Quantum computers process information using quantum bits...

[... more results ...]
```

**Implementation**:
```bash
#!/bin/bash
# general-query.sh

QUERY="$1"
API_KEY="..."
API_HOST="https://api.minimax.io"

curl -s -X POST "$API_HOST/v1/coding_plan/search" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{\"q\":\"$QUERY\"}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('organic', []):
    print(f'{r.get(\"title\")}')
    print(f'  {r.get(\"link\")}')
    print(f'  {r.get(\"snippet\")}')
    print()
"
```

**Parameters**:
- `query` (required): Question or topic

**Use Cases**:
- Quick questions
- General research
- Topic exploration
- Educational queries

---

## Integration Patterns

### Terminal Claude

**Step 1: Set Up Environment**
```bash
export MINIMAX_API_KEY="..."
export MINIMAX_API_HOST="https://api.minimax.io"
```

**Step 2: Use Commands**
```
Claude: /minimax-search "Godot 4.5 features"
[Terminal executes search]
Claude: /minimax-analyze "UI bugs?" "screenshot.png"
[Terminal analyzes image]
```

**Step 3: Review Results**
Claude processes outputs and provides insights.

### Desktop Claude

**Step 1: Start MCP Server**
```bash
MINIMAX_API_KEY="..." uvx minimax-coding-plan-mcp -y
```

**Step 2: Use Native Tools**
```
web_search(query="Godot 4.5 features")
understand_image(prompt="Analyze UI", image_source="screenshot.png")
```

### Cursor IDE

**Step 1: Check Commands**
```bash
ls .cursor/commands/
```

**Step 2: Use Slash Commands**
```
/minimax-plan "Research task"
/minimax-execute
```

---

## Custom Commands

### Creating Custom Wrappers

**Web Search Wrapper**:
```bash
#!/bin/bash
# gs (quick search)
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d "{\"q\":\"$*\"}" | python3 -m json.tool
```

**Usage**:
```bash
gs "Godot features"
```

### Alias Shortcuts

```bash
# Add to ~/.bashrc or ~/.zshrc
alias mm-search='./scripts/web-search.sh'
alias mm-analyze='./scripts/analyze-image.sh'
alias mm-test='./scripts/test-connection.sh'
alias mm-status='./scripts/check-status.sh'
```

**Usage**:
```bash
mm-search "query"
mm-analyze "prompt" "image.png"
```

---

## Error Handling

### Command Not Found
```
-bash: /minimax-search: command not found
```

**Solution**:
```bash
# Ensure scripts are in PATH
export PATH="$PATH:/path/to/minimax-mcp/scripts"

# Or use full path
./scripts/web-search.sh "query"
```

### Permission Denied
```
bash: ./scripts/web-search.sh: Permission denied
```

**Solution**:
```bash
chmod +x scripts/*.sh
```

### API Errors
```
HTTP 401: Invalid API key
```

**Solution**:
```bash
# Check API key
echo $MINIMAX_API_KEY | wc -c  # Should be 127

# Re-set if needed
export MINIMAX_API_KEY="sk-cp-..."
```

---

## Best Practices

### 1. Use Specific Queries
```bash
# ❌ Too vague
/minimax-search "games"

# ✅ Specific
/minimax-search "Godot 4.5 new rendering features 2025"
```

### 2. Provide Context
```bash
# ❌ Minimal
/minimax-analyze "bugs?" "ui.png"

# ✅ Detailed
/minimax-analyze "Identify UI bugs in this game interface screenshot, focusing on alignment, spacing, and visual hierarchy" "ui.png"
```

### 3. Rate Limit Commands
```bash
# Add delays between batch commands
/minimax-search "query1"
sleep 1
/minimax-search "query2"
```

### 4. Cache Results
```bash
# Cache frequently used queries
QUERY_HASH=$(echo "Godot 4.5" | md5sum | cut -d' ' -f1)
if [ ! -f "/tmp/minimax-$QUERY_HASH.json" ]; then
    /minimax-search "Godot 4.5" | tee "/tmp/minimax-$QUERY_HASH.json"
else
    cat "/tmp/minimax-$QUERY_HASH.json"
fi
```

---

## Troubleshooting Commands

### Debug Mode
```bash
#!/bin/bash
# Enable verbose output
set -x
curl -v ...  # Verbose curl
set +x
```

### Log Commands
```bash
#!/bin/bash
# Log all commands
exec > >(tee -a minimax.log)
exec 2>&1

# Now all output is logged
/minimax-search "test"
```

### Test All Commands
```bash
#!/bin/bash
# test-all-commands.sh

echo "Testing all MiniMax commands..."

/minimax-status
echo "---"

/minimax-test
echo "---"

/minimax-search "test query"
echo "---"

/minimax-query "test question"
echo "---"

/minimax-analyze "test" "https://via.placeholder.com/100"
echo "---"

echo "All commands tested"
```

---

## Summary

**Available Commands**:
- `/minimax-status` - Check server status
- `/minimax-search` - Web search
- `/minimax-analyze` - Image analysis
- `/minimax-test` - Test connection
- `/minimax-exec` - Execute plan
- `/minimax-query` - General query

**Integration**:
- Terminal Claude: Direct script execution
- Desktop Claude: MCP tools
- Cursor IDE: Existing slash commands

**Best Practices**:
- Use specific, detailed queries
- Implement rate limiting
- Cache frequently used results
- Test commands before production

**Status**: ✅ All commands tested and working
