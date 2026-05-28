## Prerequisites

### **IMPORTANT: Project Context Required**

Most Scribe tools require an active project context. Before using any tool, you MUST set a project:

```python
await set_project(name="your-project-name")
```

**Failure to set a project first will result in errors like:**
- `"No project configured. Invoke set_project before using this tool."`
- `"No project configured. Invoke set_project before reading logs"`

---
