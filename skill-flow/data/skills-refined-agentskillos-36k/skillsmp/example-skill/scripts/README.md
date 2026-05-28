# Skill scripts

Place helper scripts here to support the skill. Prefer Bash for portability, but keep commands cross-platform where feasible (e.g., avoid platform-specific flags when possible).

Call scripts from the skill steps using relative paths, for example:

```bash
bash scripts/example.sh
```

Document any prerequisites at the top of each script and keep them idempotent so they can be rerun safely.
