---
name: github-actions-debugging
description: Use this skill when debugging GitHub Actions workflows, CI/CD issues, or deployment failures.
---

# GitHub Actions Debugging Skill

This skill provides a comprehensive approach to diagnosing and fixing issues with GitHub Actions workflows, CI/CD pipeline failures, and deployment problems.

## When to Use

- GitHub Actions workflow failures
- CI build errors that don't occur locally
- Test failures only in CI environment
- Artifact upload/download issues
- Secret/credential problems
- Cache-related failures
- Timeout issues
- Deployment failures
- Terraform state lock errors
- Authentication or authorization failures
- Azure resource issues during deployment

## Debugging Process

### Step 1: Check Recent Workflow Runs

```bash
gh run list --limit 10
```

### Step 2: View Failed Logs

```bash
gh run view <run-id> --log-failed
```

### Step 3: Identify the Issue

#### Common Failure Patterns

- **Terraform State Lock**
  - **Pattern:** `Error acquiring the state lock`
  - **Fix:** Extract Lock ID and run:
    ```bash
    cd infra && terraform force-unlock -force <lock-id>
    ```

- **Authentication Failures**
  - **Pattern:** `AuthorizationFailed`, `AADSTS`
  - **Fix:** Validate `AZURE_CREDENTIALS` secret.

- **Resource Not Found**
  - **Pattern:** `ResourceNotFound`
  - **Fix:** Run `terraform refresh` or re-import.

- **Gradle Build Failures**
  - **Pattern:** Gradle daemon issues
  - **Fix:** Check `android/gradle-ci.properties` settings.

- **Test Failures**
  - **Pattern:** `FAILED`, `pytest`
  - **Fix:** Run tests locally:
    ```bash
    cd api && pytest tests/ -v
    ```

- **Cache Issues**
  - **Pattern:** Cache not working
  - **Fix:** Verify cache key and paths.

- **Artifact Upload Issues**
  - **Pattern:** Artifacts not found
  - **Fix:** Ensure build step completed successfully.

### Step 4: Fix and Re-run

After addressing the identified issues, re-run the workflow:

```bash
gh run rerun <run-id>
```

### Quick Commands Reference

| Command | Description |
|---------|-------------|
| `gh run list` | Show recent workflow runs |
| `gh run view <run-id>` | View specific run's failed logs |
| `gh run rerun <run-id>` | Re-run most recent failed workflow |
| `gh run watch <run-id>` | Watch running workflow |

## Best Practices

1. **Test Locally First**: Always run the same commands as in CI locally.
2. **Use Verbose Logging**: Add `--verbose` to debug commands.
3. **Check All Secrets**: Ensure secrets exist and are correct.
4. **Monitor Cache Usage**: Clear cache if builds become inconsistent.
5. **Document Workflow Changes**: Add comments explaining modifications.

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Terraform Documentation](https://www.terraform.io/docs/index.html)
- [Flutter CI/CD Guide](https://docs.flutter.dev/deployment/cd)