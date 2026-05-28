---
name: release-new-version
description: Use this skill to release a new version of the project, ensuring proper versioning and documentation.
---

# Release New Version

This skill guides you through the process of releasing a new version of the project, following Semantic Versioning (SemVer) and updating the changelog.

## Usage

```
/release [version]
```

If the version is not provided, you will be prompted for it.

## Steps

1. **Validate Version**: Ensure the version follows SemVer (X.Y.Z) and is greater than the current version.
2. **Check Current Version**: Find the latest tag using `git describe --tags --abbrev=0`.
3. **Analyze Changes**: Review commits since the last tag with `git log <last_tag>..HEAD --oneline` and verify file modifications using `git diff <last_tag>..HEAD --stat` and `git diff <last_tag>..HEAD`.
4. **Determine Increment**:
   - **Major**: For breaking changes.
   - **Minor**: For new features (backward compatible).
   - **Patch**: For bug fixes.
5. **Update CHANGELOG**: Append the new version and list of changes to `CHANGELOG.md`.
6. **Commit Changes**: Commit the updated `CHANGELOG.md`.
7. **Create Release Tag**: Tag the release (e.g., `git tag v1.2.3`).
8. **Push Changes**: Push the commit and the tag using `git push origin main --tags`.

## Notes

- Ensure you are on the `main` branch with a clean working directory.
- Requires cargo credentials (`cargo login` or `CARGO_REGISTRY_TOKEN`).
- If any step fails, stop and report the error.
- The git tag triggers GitHub Actions to build Docker images and create the GitHub release.

## Output

- **CHANGELOG.md**: Updated with the new version entry.
- **Git Tag**: A new tag created in the repository.