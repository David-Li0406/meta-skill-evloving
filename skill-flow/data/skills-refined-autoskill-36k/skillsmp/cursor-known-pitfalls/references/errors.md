# Error Handling Reference

| Error | Cause | Solution |
|-------|-------|----------|
| AI output incorrect | Context pollution or vague prompts | Start new chat, be more specific |
| Tab completion wrong | Outdated patterns or wrong framework | Update .cursorrules, verify language mode |
| Performance degraded | Too many extensions or large context | Audit extensions, add to .cursorignore |
| Secrets exposed | Sensitive files not excluded | Update .cursorignore, enable Privacy Mode |