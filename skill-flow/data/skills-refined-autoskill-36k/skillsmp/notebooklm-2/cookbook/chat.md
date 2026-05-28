# Chat Cookbook

---

## List saved chat sessions

**Problem**: See existing chat sessions on disk.

**Solution**:
```bash
nlm chat-list
```

**Tip**: Sessions are stored per notebook ID.

---

## Interactive chat with commands

**Problem**: Use the built-in chat UI and commands.

**Solution**:
```bash
nlm chat <notebook-id>
```

**Tip**: In chat, use `/help`, `/history`, `/reset`, `/save`, `/multiline`, `/exit`.
