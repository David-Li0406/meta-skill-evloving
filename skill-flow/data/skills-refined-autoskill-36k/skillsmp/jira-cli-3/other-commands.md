# Other Commands Reference

## `jira open` (aliases: `browse`, `navigate`)

Open issue or project in browser.

```bash
jira open ISSUE-KEY
jira open              # Opens project page
```

| Flag | Description |
|------|-------------|
| `-n, --no-browser` | Print URL without opening browser |

**Examples:**
```bash
jira open MDBIM-123           # Open issue in browser
jira open                     # Open project page
jira open MDBIM-123 -n        # Just print the URL
```

---

## `jira board list` (aliases: `ls`, `lists`)

List boards in a project.

```bash
jira board list
```

---

## `jira project list` (aliases: `ls`, `lists`)

List all accessible Jira projects.

```bash
jira project list
```

---

## `jira release list` (aliases: `ls`, `lists`)

List project versions/releases.

```bash
jira release list
```

---

## `jira me`

Display configured Jira user.

```bash
jira me
```

Useful for scripting:
```bash
jira issue assign MDBIM-123 $(jira me)
jira issue list -a$(jira me) --plain
```

---

## `jira serverinfo` (alias: `systeminfo`)

Display Jira instance information.

```bash
jira serverinfo
```

---

## `jira init` (aliases: `initialize`, `configure`, `config`, `setup`)

Initialize or reconfigure jira-cli.

```bash
jira init
```

| Flag | Description |
|------|-------------|
| `--installation` | `cloud` or `local` |
| `--server` | Jira server URL |
| `--login` | Username or email |
| `--auth-type` | `basic`, `bearer`, or `mtls` |
| `--project` | Default project key |
| `--board` | Default board name |
| `--force` | Override existing config |
| `--insecure` | Skip TLS verification (self-signed certs) |

**Example:**
```bash
jira init --installation cloud --server https://company.atlassian.net --project MDBIM
```

---

## `jira version`

Print version information.

```bash
jira version
```

---

## `jira completion`

Generate shell completion scripts.

### Bash
```bash
# Add to .bashrc
source <(jira completion bash)

# Or install permanently
jira completion bash > /usr/local/etc/bash_completion.d/jira
```

### Zsh
```bash
# Enable completion (add to .zshrc)
echo "autoload -U compinit; compinit" >> ~/.zshrc

# Install completion
jira completion zsh > "${fpath[1]}/_jira"
```

### Fish
```bash
jira completion fish > ~/.config/fish/completions/_jira.fish
```

### PowerShell
```powershell
jira completion powershell | Out-String | Invoke-Expression
```

---

## `jira man`

Generate man pages.

```bash
jira man --generate
jira man --generate --output /path/to/man-pages
```

| Flag | Description |
|------|-------------|
| `-g, --generate` | Generate man pages |
| `-o, --output` | Output directory (default: `/tmp/man-jira-cli`) |

---

## `jira help`

Get help for any command.

```bash
jira help
jira help issue
jira help issue list
jira issue list --help
```
