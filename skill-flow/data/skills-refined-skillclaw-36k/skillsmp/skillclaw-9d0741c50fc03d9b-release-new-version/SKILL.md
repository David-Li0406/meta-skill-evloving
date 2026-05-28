---
name: release-new-version
description: Use this skill when you need to release a new version of your project, ensuring proper versioning and documentation.
---

# Skill body

## Usage

```
/release-new-version [version]
```

If the version is not provided, the skill will determine the next version based on changes.

## Steps

1. **Validate Version**: Ensure the version follows Semantic Versioning (X.Y.Z) and is greater than the current version.
   
2. **Check Current Version**: Find the latest tag using:
   ```bash
   git describe --tags --abbrev=0
   ```

3. **Analyze Changes**: Review commits since the last tag:
   ```bash
   git log <last_tag>..HEAD --oneline
   ```
   Also, check file modifications:
   ```bash
   git diff <last_tag>..HEAD --stat
   git diff <last_tag>..HEAD
   ```

4. **Determine Increment**:
   - **Major**: For breaking changes.
   - **Minor**: For new features (backward compatible).
   - **Patch**: For bug fixes.

5. **Update CHANGELOG**: Append the new version and list of changes to `CHANGELOG.md`.

6. **Commit Changes**: Commit the updated `CHANGELOG.md`.

7. **Create Release Tag**: Tag the release:
   ```bash
   git tag vX.Y.Z
   ```

8. **Push Changes**: Push the commit and the tag:
   ```bash
   git push origin main --tags
   ```

## Notes

- Must be on the `main` branch with a clean working directory.
- Requires cargo credentials (`cargo login` or `CARGO_REGISTRY_TOKEN`).
- If any step fails, stop and report the error.
- The git tag triggers CI/CD processes, such as building Docker images and creating releases.