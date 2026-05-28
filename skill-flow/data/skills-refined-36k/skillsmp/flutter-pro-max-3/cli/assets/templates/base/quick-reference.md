
---

## Quick Reference

### Search Commands

```bash
# Auto-detect domain
python3 {{SCRIPT_PATH}}/search.py "ListView" --top 5

# Specific domain
python3 {{SCRIPT_PATH}}/search.py "network http" --domain package --top 5

# Stack filter
python3 {{SCRIPT_PATH}}/search.py "state" --stack riverpod --top 5

# JSON output
python3 {{SCRIPT_PATH}}/search.py "login" --json --top 3
```

### Example Workflow

**User Request:** "Tạo màn hình đăng nhập với Riverpod"

1. **Search widgets:**
   ```bash
   python3 {{SCRIPT_PATH}}/search.py "form input" --domain widget --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 {{SCRIPT_PATH}}/search.py "authentication login" --domain pattern --top 5
   ```

3. **Search packages:**
   ```bash
   python3 {{SCRIPT_PATH}}/search.py "validation" --domain package --stack riverpod --top 5
   ```

4. **Apply results** to generate code với Riverpod state management
