# Error Handling Workflow

Comprehensive error handling and recovery procedures for skillmeat CLI operations.

---

## Error Categories

### 1. Network Errors

#### Rate Limit Exceeded

**Detection**: `403 Forbidden` with `X-RateLimit-Remaining: 0` header

```
[Rate Limited]: GitHub API rate limit exceeded
[Cause]: Too many requests without authentication (60/hour limit)
[Solution]: Set a GitHub personal access token for higher limits (5000/hour)
[Command]: skillmeat config set github-token <your-token>
[Guide]: Visit https://github.com/settings/tokens to create token with 'repo' scope
```

**Recovery Actions**:
1. Check current rate limit: `curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit`
2. Wait for reset time (shown in error message)
3. Set token for future requests

#### Connection Timeout

**Detection**: `requests.exceptions.Timeout` or similar

```
[Connection Timeout]: Failed to reach GitHub API
[Cause]: Network connectivity issue or GitHub API unavailable
[Solution]: Retry with exponential backoff (automatic)
[Manual]: Check network connection, try again in a few seconds
```

**Recovery Actions**:
1. Verify internet connectivity: `ping github.com`
2. Check GitHub status: https://www.githubstatus.com
3. Retry command with `--retry 3` flag (if supported)

#### DNS Resolution Failed

**Detection**: `socket.gaierror` or `requests.exceptions.ConnectionError`

```
[DNS Failed]: Cannot resolve github.com
[Cause]: DNS server unavailable or network disconnected
[Solution]: Check network connectivity
[Commands]:
  - Test DNS: nslookup github.com
  - Test connectivity: ping 8.8.8.8
  - Restart network: (platform-specific)
```

**Recovery Actions**:
1. Check `/etc/resolv.conf` (Unix) or DNS settings (Windows)
2. Try alternate DNS server (8.8.8.8, 1.1.1.1)
3. Restart network interface

---

### 2. Authentication Errors

#### Invalid GitHub Token

**Detection**: `401 Unauthorized` with token present

```
[Auth Failed]: GitHub token is invalid or expired
[Cause]: Token revoked, expired, or incorrectly copied
[Solution]: Generate new token and update configuration
[Commands]:
  1. Remove old token: skillmeat config unset github-token
  2. Create new token: Visit https://github.com/settings/tokens
  3. Set new token: skillmeat config set github-token <new-token>
```

**Recovery Actions**:
1. Verify token format: 40-character hex string (classic) or starts with `ghp_` (fine-grained)
2. Check token hasn't been revoked in GitHub settings
3. Ensure token has required scopes (`repo` for private repos)

#### Permission Denied (Private Repo)

**Detection**: `404 Not Found` (GitHub returns 404 for inaccessible repos)

```
[Permission Denied]: Cannot access private repository
[Cause]: Token missing 'repo' scope or user lacks repository access
[Solution]: Update token scopes or request repository access
[Commands]:
  1. Check token scopes: curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
  2. Update token: Regenerate with 'repo' scope at https://github.com/settings/tokens
  3. Verify access: Visit repository URL in browser while logged in
```

**Recovery Actions**:
1. Confirm repository exists and is private
2. Check token has `repo` scope (not just `public_repo`)
3. Verify user has read access to repository

#### Missing Authentication

**Detection**: Rate limit near exhaustion without token

```
[Warning]: Approaching rate limit without authentication
[Current]: {X-RateLimit-Remaining} requests remaining
[Solution]: Set GitHub token to increase limit from 60/hour to 5000/hour
[Command]: skillmeat config set github-token <your-token>
```

**Recovery Actions**:
1. Set token preemptively before hitting limit
2. Continue without token (accept lower rate limit)

---

### 3. Artifact Errors

#### Artifact Not Found

**Detection**: `404 Not Found` or search returns empty results

```
[Not Found]: Artifact '{name}' not found at '{source}'
[Cause]: Path incorrect, artifact doesn't exist, or private/inaccessible
[Solution]: Search for similar artifacts or verify path
[Commands]:
  - Search by name: skillmeat search {name}
  - List repo contents: skillmeat list {username}/{repo}
  - Verify path: Check repository structure at https://github.com/{username}/{repo}
```

**Recovery Actions**:
1. Check for typos in artifact name/path
2. Search marketplace: `skillmeat search {keyword}`
3. Verify repository exists and is accessible
4. Check if artifact path includes nested directories

#### Ambiguous Artifact Name

**Detection**: Multiple matches found for name

```
[Ambiguous]: Multiple artifacts match '{name}'
[Matches]:
  1. {username}/{repo}/{path1} - {description}
  2. {username}/{repo}/{path2} - {description}
  3. {username}/{repo}/{path3} - {description}
[Solution]: Use full source path to specify exact artifact
[Command]: skillmeat add {username}/{repo}/{path}
```

**Recovery Actions**:
1. Review match descriptions to identify correct artifact
2. Use full source path instead of name
3. Add specific version: `{source}@{version}`

#### Artifact Already Exists

**Detection**: Duplicate entry in manifest or lockfile

```
[Already Exists]: Artifact '{name}' is already in collection
[Source]: {existing_source}
[Version]: {existing_version}
[Solution]: Update existing artifact or use different name
[Commands]:
  - Update: skillmeat update {name}
  - Force reinstall: skillmeat add {source} --force
  - Use alias: skillmeat add {source} --alias {new-name}
```

**Recovery Actions**:
1. Check if update is needed: `skillmeat list`
2. Remove and re-add: `skillmeat remove {name} && skillmeat add {source}`
3. Install with different alias to keep both versions

#### Invalid Artifact Format

**Detection**: Missing SKILL.md, invalid frontmatter, or structural issues

```
[Invalid Format]: Artifact does not meet SkillMeat requirements
[Issues]:
  - Missing SKILL.md (skills)
  - Invalid YAML frontmatter
  - Missing required fields: {field_list}
[Solution]: Contact artifact author or fork and fix
[Validation]: Run local validation before adding
```

**Recovery Actions**:
1. Check artifact structure matches type requirements
2. Validate YAML frontmatter: `yamllint SKILL.md`
3. Report issue to artifact author
4. Fork and fix if open-source

#### Version Conflict

**Detection**: Requested version not found or incompatible

```
[Version Conflict]: Version '{version}' not found for artifact '{name}'
[Available]: {list_of_versions}
[Solution]: Use available version or omit version for latest
[Commands]:
  - Use latest: skillmeat add {source}
  - Use specific: skillmeat add {source}@{available_version}
  - List versions: skillmeat search {source} --versions
```

**Recovery Actions**:
1. List available tags/releases in repository
2. Use `@latest` or omit version specifier
3. Check if version uses tag prefix (v1.0.0 vs 1.0.0)

---

### 4. File System Errors

#### Permission Denied

**Detection**: `PermissionError` or `errno 13`

```
[Permission Denied]: Cannot write to '{path}'
[Cause]: Insufficient permissions for directory
[Solution]: Check directory permissions or run with appropriate privileges
[Commands]:
  - Check permissions: ls -la {path}
  - Fix ownership (Unix): sudo chown -R $USER {path}
  - Fix permissions (Unix): chmod 755 {path}
  - Run as admin (Windows): Right-click > Run as Administrator
```

**Recovery Actions**:
1. Verify user has write access to `~/.skillmeat/` (user scope)
2. Check project directory permissions (local scope)
3. Avoid `sudo` usage (not recommended for SkillMeat)
4. Use `--dangerously-skip-permissions` only if absolutely necessary

#### Disk Full

**Detection**: `OSError: [Errno 28] No space left on device`

```
[Disk Full]: Insufficient disk space to complete operation
[Required]: ~{size_needed} MB
[Available]: {size_available} MB
[Solution]: Free up disk space
[Commands]:
  - Check usage: df -h (Unix) or dir (Windows)
  - Clean cache: skillmeat cache clear
  - Remove unused artifacts: skillmeat remove {unused-artifacts}
  - Clean snapshots: skillmeat snapshot prune --keep 5
```

**Recovery Actions**:
1. Check available space: `df -h ~/.skillmeat`
2. Clear SkillMeat cache: `~/.skillmeat/cache/`
3. Remove old snapshots: `~/.skillmeat/snapshots/`
4. Undeploy unused artifacts: `skillmeat undeploy {name}`

#### Path Too Long (Windows)

**Detection**: `OSError: [Errno 63] File name too long` (Windows)

```
[Path Too Long]: File path exceeds Windows MAX_PATH limit (260 characters)
[Current Path]: {path} ({length} characters)
[Solution]: Use shorter collection path or enable long path support
[Commands]:
  - Enable long paths (Admin): Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1
  - Use shorter path: Set SKILLMEAT_HOME to shorter directory
  - Move collection: skillmeat config set collection-path C:\sm
```

**Recovery Actions**:
1. Enable Windows long path support (requires admin + reboot)
2. Set shorter `SKILLMEAT_HOME` environment variable
3. Move collection to shorter path (C:\sm instead of C:\Users\LongUsername\...)
4. Use subst to map to shorter drive letter: `subst S: C:\Users\Username\.skillmeat`

#### File Locked (Windows)

**Detection**: `PermissionError: [WinError 32]` (file in use)

```
[File Locked]: File is open in another process
[File]: {path}
[Cause]: File open in editor, terminal, or another SkillMeat process
[Solution]: Close file and retry
[Commands]:
  - Find process (Windows): handle.exe {path}
  - Kill process (Windows): taskkill /F /PID {pid}
  - Retry operation: (repeat command)
```

**Recovery Actions**:
1. Close editors, terminals with file open
2. Wait for background processes to complete
3. Restart terminal/IDE if file remains locked
4. Use Windows Resource Monitor to identify process

---

### 5. Parse Errors

#### Invalid JSON Output

**Detection**: `json.JSONDecodeError`

```
[Parse Error]: Command output is not valid JSON
[Cause]: Command doesn't support --json flag or returned error message
[Solution]: Retry with --json flag or check command syntax
[Commands]:
  - Retry: skillmeat {command} --json
  - Check help: skillmeat {command} --help
  - Use non-JSON output: skillmeat {command} (without --json)
```

**Recovery Actions**:
1. Verify command supports `--json` flag
2. Check for error messages in output before JSON
3. Use Rich console output instead of JSON parsing

#### Malformed Manifest

**Detection**: `toml.TOMLDecodeError` or missing required fields

```
[Malformed Manifest]: manifest.toml contains syntax errors
[File]: {path}/manifest.toml
[Error]: {parse_error_details}
[Solution]: Repair manifest manually or reinitialize
[Commands]:
  - Validate TOML: tomli-cli {path}/manifest.toml
  - Backup and repair: cp manifest.toml manifest.toml.bak && vim manifest.toml
  - Reinitialize (DESTRUCTIVE): skillmeat init --force
```

**Recovery Actions**:
1. Open `manifest.toml` in editor with TOML syntax highlighting
2. Check for common errors:
   - Unquoted strings with special characters
   - Missing closing brackets/quotes
   - Invalid dates/times
3. Restore from backup: `~/.skillmeat/snapshots/`
4. Validate after repair: `python -c "import tomllib; tomllib.load(open('manifest.toml', 'rb'))"`

#### Malformed Lockfile

**Detection**: Lock file version mismatch or corrupted entries

```
[Malformed Lockfile]: lockfile.toml is corrupted or incompatible
[File]: {path}/lockfile.toml
[Version]: {lockfile_version} (expected: {expected_version})
[Solution]: Regenerate lockfile from manifest
[Commands]:
  - Backup: cp lockfile.toml lockfile.toml.bak
  - Regenerate: skillmeat sync --regenerate-lock
  - Verify: skillmeat list
```

**Recovery Actions**:
1. Backup lockfile before regeneration
2. Regenerate from manifest: `skillmeat sync --regenerate-lock`
3. If regeneration fails, restore from snapshot
4. Check manifest is valid before regenerating lock

#### Invalid YAML Frontmatter

**Detection**: `yaml.YAMLError` when parsing artifact metadata

```
[Invalid YAML]: Artifact frontmatter contains syntax errors
[File]: {artifact_path}/SKILL.md
[Error]: {yaml_error_details}
[Solution]: Contact artifact author or fix manually
[Commands]:
  - Validate YAML: yamllint {artifact_path}/SKILL.md
  - View raw: cat {artifact_path}/SKILL.md | head -20
  - Report issue: (GitHub issue link if available)
```

**Recovery Actions**:
1. Check YAML syntax in frontmatter (lines between `---`)
2. Common errors:
   - Tabs instead of spaces
   - Incorrect indentation
   - Unquoted strings with colons
3. Fork and fix if open-source
4. Report to artifact author

---

### 6. Database Errors (Web UI)

#### Database Locked

**Detection**: `sqlite3.OperationalError: database is locked`

```
[Database Locked]: SQLite database is locked by another process
[Cause]: Multiple processes accessing database simultaneously
[Solution]: Wait for operation to complete or restart server
[Commands]:
  - Stop server: Ctrl+C or skillmeat web stop
  - Kill processes: pkill -f "skillmeat web"
  - Restart: skillmeat web dev
```

**Recovery Actions**:
1. Close duplicate web servers
2. Wait for long-running operations to complete
3. Check for zombie processes: `ps aux | grep skillmeat`
4. Restart API server

#### Migration Failed

**Detection**: Alembic migration error

```
[Migration Failed]: Database schema migration failed
[Migration]: {migration_version}
[Error]: {migration_error}
[Solution]: Rollback and retry or reset database
[Commands]:
  - Rollback: alembic downgrade -1
  - Retry: alembic upgrade head
  - Reset (DESTRUCTIVE): rm ~/.skillmeat/skillmeat.db && alembic upgrade head
```

**Recovery Actions**:
1. Check Alembic logs for detailed error
2. Rollback to previous version: `alembic downgrade -1`
3. Backup database before reset: `cp ~/.skillmeat/skillmeat.db ~/.skillmeat/skillmeat.db.bak`
4. Reset and re-migrate (loses data)

---

## Error Response Format

All errors follow this structure for consistency:

```
[Error Type]: Brief description
[Cause]: Why this happened
[Solution]: How to fix it
[Command]: Specific fix command (if applicable)
[Additional Context]: (optional)
```

### Example: Full Error Output

```
Error: Failed to add artifact 'canvas-design'

[Rate Limited]: GitHub API rate limit exceeded
[Cause]: Too many requests without authentication (60/hour limit)
[Current]: 0 requests remaining, resets at 2025-12-24 14:30:00 UTC
[Solution]: Set a GitHub personal access token for higher limits (5000/hour)
[Command]: skillmeat config set github-token <your-token>
[Guide]: Visit https://github.com/settings/tokens to create token with 'repo' scope

Alternative: Wait 23 minutes for rate limit reset
```

---

## Recovery Procedures

### General Recovery Steps

1. **Capture Error Output**
   - Copy full error message
   - Note command that failed
   - Check logs: `~/.skillmeat/logs/`

2. **Identify Error Category**
   - Network (timeout, DNS, rate limit)
   - Auth (token, permissions)
   - Artifact (not found, invalid format)
   - File system (permissions, disk space)
   - Parse (JSON, TOML, YAML)
   - Database (locked, migration)

3. **Apply Category-Specific Recovery**
   - Follow procedures from relevant section above
   - Try suggested commands in order
   - Check if issue persists

4. **Escalate If Needed**
   - Search GitHub issues: https://github.com/skillmeat/skillmeat/issues
   - Create new issue with:
     - Full error message
     - Command executed
     - Platform/version info: `skillmeat --version`
     - Relevant logs

### Backup and Restore

**Before Destructive Operations**:
```bash
# Backup collection
cp -r ~/.skillmeat ~/.skillmeat.backup

# Backup specific files
cp ~/.skillmeat/manifest.toml ~/.skillmeat/manifest.toml.bak
cp ~/.skillmeat/lockfile.toml ~/.skillmeat/lockfile.toml.bak
```

**Restore from Backup**:
```bash
# Restore full collection
rm -rf ~/.skillmeat
mv ~/.skillmeat.backup ~/.skillmeat

# Restore specific file
cp ~/.skillmeat/manifest.toml.bak ~/.skillmeat/manifest.toml
```

**Restore from Snapshot**:
```bash
# List snapshots
skillmeat snapshot list

# Restore specific snapshot
skillmeat snapshot restore <snapshot-id>
```

### Safe Mode / Clean Slate

**When All Else Fails**:

1. **Export artifact list**:
   ```bash
   skillmeat list --json > artifacts-backup.json
   ```

2. **Backup custom artifacts**:
   ```bash
   cp -r ~/.skillmeat/artifacts ~/.skillmeat-artifacts-backup
   ```

3. **Reinitialize**:
   ```bash
   mv ~/.skillmeat ~/.skillmeat.broken
   skillmeat init
   ```

4. **Re-add artifacts**:
   ```bash
   # From backup list
   cat artifacts-backup.json | jq -r '.artifacts[].source' | xargs -I {} skillmeat add {}
   ```

---

## Logging and Debugging

### Enable Debug Logging

```bash
# Set environment variable
export SKILLMEAT_LOG_LEVEL=DEBUG

# Run command with verbose output
skillmeat --verbose add anthropics/skills/canvas-design

# Check logs
tail -f ~/.skillmeat/logs/skillmeat.log
```

### Log Locations

- **CLI logs**: `~/.skillmeat/logs/skillmeat.log`
- **Web API logs**: `~/.skillmeat/logs/api.log`
- **Web UI logs**: Browser DevTools console

### Debug Information to Collect

When reporting issues:

```bash
# Version info
skillmeat --version

# System info
uname -a  # Unix
systeminfo | findstr /B /C:"OS"  # Windows

# Configuration
skillmeat config list

# Collection state
skillmeat list --json

# Manifest/lockfile
cat ~/.skillmeat/manifest.toml
cat ~/.skillmeat/lockfile.toml
```

---

## Prevention Best Practices

1. **Set GitHub Token Early**
   - Avoid rate limits before they happen
   - Configure during initial setup

2. **Use Snapshots**
   - Automatic snapshots before major operations
   - Manually snapshot before risky changes: `skillmeat snapshot create`

3. **Validate Before Commit**
   - Check artifact format before adding
   - Verify manifest syntax after manual edits

4. **Regular Sync**
   - Keep collection in sync: `skillmeat sync` weekly
   - Update artifacts: `skillmeat update --all`

5. **Monitor Disk Space**
   - Check periodically: `df -h ~/.skillmeat`
   - Clean cache: `skillmeat cache clear` monthly

6. **Backup Before Major Changes**
   - Before version upgrades
   - Before bulk operations
   - Before manual manifest edits

---

## Quick Reference Table

| Error Pattern | Category | Quick Fix |
|--------------|----------|-----------|
| `403` + rate limit | Network | Set GitHub token |
| `Timeout` | Network | Retry, check connectivity |
| `401` | Auth | Update token |
| `404` | Artifact | Verify path, search alternatives |
| `PermissionError` | File System | Check directory permissions |
| `[Errno 28]` | File System | Free disk space |
| `JSONDecodeError` | Parse | Use `--json` flag or check output |
| `TOMLDecodeError` | Parse | Validate and repair manifest |
| `database locked` | Database | Restart server, close duplicates |

---

## Advanced Recovery: File System Repair

### Manifest Corruption Recovery

```bash
# 1. Attempt automated repair
skillmeat doctor --repair-manifest

# 2. Manual repair from lockfile
python << EOF
import tomllib
import tomli_w

# Read lockfile
with open('lockfile.toml', 'rb') as f:
    lock = tomllib.load(f)

# Reconstruct manifest
manifest = {
    'tool': {
        'skillmeat': {
            'version': '1.0.0'
        }
    },
    'artifacts': [
        {
            'name': entry['name'],
            'type': entry['type'],
            'source': entry['source'],
            'version': entry.get('version_spec', 'latest'),
            'scope': entry.get('scope', 'user'),
        }
        for entry in lock.get('lock', {}).get('entries', {}).values()
    ]
}

# Write repaired manifest
with open('manifest.toml', 'wb') as f:
    tomli_w.dump(manifest, f)
EOF

# 3. Verify repair
skillmeat list
```

### Lockfile Corruption Recovery

```bash
# Regenerate from manifest
skillmeat sync --regenerate-lock --verbose

# If sync fails, rebuild manually
python << EOF
import tomllib
from datetime import datetime
import tomli_w

# Read manifest
with open('manifest.toml', 'rb') as f:
    manifest = tomllib.load(f)

# Create new lockfile structure
lock = {
    'lock': {
        'version': '1.0.0',
        'entries': {}
    }
}

# Populate entries (will need manual resolution of versions)
for artifact in manifest.get('artifacts', []):
    name = artifact['name']
    lock['lock']['entries'][name] = {
        'source': artifact['source'],
        'version_spec': artifact.get('version', 'latest'),
        'resolved_sha': 'unknown',  # Needs manual resolution
        'locked_at': datetime.utcnow().isoformat() + 'Z',
    }

# Write lockfile
with open('lockfile.toml', 'wb') as f:
    tomli_w.dump(lock, f)
EOF

# Sync to resolve versions
skillmeat sync
```

---

## Error Code Reference

SkillMeat uses exit codes for programmatic error detection:

| Exit Code | Category | Description |
|-----------|----------|-------------|
| `0` | Success | Operation completed successfully |
| `1` | General Error | Unspecified error |
| `2` | Usage Error | Invalid command/arguments |
| `3` | Network Error | Connection, timeout, DNS |
| `4` | Auth Error | Invalid token, permissions |
| `5` | Artifact Error | Not found, invalid format |
| `6` | File System Error | Permissions, disk space, path |
| `7` | Parse Error | Invalid JSON, TOML, YAML |
| `8` | Database Error | Lock, migration failure |

**Usage**:
```bash
# Bash script error handling
if ! skillmeat add anthropics/skills/canvas-design; then
    exit_code=$?
    case $exit_code in
        3) echo "Network error: check connectivity" ;;
        4) echo "Auth error: set GitHub token" ;;
        5) echo "Artifact error: verify path" ;;
        *) echo "Unknown error: $exit_code" ;;
    esac
fi
```

---

This error handling workflow provides comprehensive guidance for all failure modes in SkillMeat CLI operations. Each error category includes:

- Clear detection patterns
- Root cause analysis
- Step-by-step recovery procedures
- Specific commands to execute
- Prevention best practices

When encountering an error, start by identifying the category, then follow the category-specific recovery steps. Most errors are recoverable without data loss using the procedures above.
