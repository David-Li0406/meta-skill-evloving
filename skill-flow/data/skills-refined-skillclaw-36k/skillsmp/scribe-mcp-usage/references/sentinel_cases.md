# Sentinel Cases (Repo-wide)

These tools are sentinel-only. Do not call `set_project()` in the session.

Create cases:
```python
open_bug(title="<short title>", symptoms="<symptoms + repro + expected vs actual>", affected_paths=["path/one", "path/two"])
open_security(title="<short title>", symptoms="<threat model + impact + repro>", affected_paths=["path/one", "path/two"])
```

Link fix artifacts:
```python
link_fix(case_id="BUG-YYYYMMDD-XXX", execution_id="<run id / CI id>", artifact_ref="<commit/PR/url>", landing_status="merged|shipped|staged|reverted|wip")
```
