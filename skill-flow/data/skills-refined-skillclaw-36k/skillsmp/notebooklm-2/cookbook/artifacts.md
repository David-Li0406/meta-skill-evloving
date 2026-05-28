# Artifacts Cookbook

---

## List artifacts

**Problem**: See artifacts for a notebook.

**Solution**:
```bash
nlm artifacts <notebook-id>
```

**Tip**: `nlm list-artifacts <notebook-id>` is an alias.

---

## Create an artifact

**Problem**: Create a note, audio, report, or app artifact.

**Solution**:
```bash
nlm create-artifact <notebook-id> note
```

**Tip**: Valid types: `note`, `audio`, `report`, `app`.

---

## Delete an artifact (destructive)

**Problem**: Remove an artifact.

**Solution**:
```bash
nlm delete-artifact <artifact-id>
```

**Tip**: Always confirm with the user first.
