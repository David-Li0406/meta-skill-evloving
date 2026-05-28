# Quotefix - Examples

Practical patterns for cross-shell quoting and escaping.

---

## Quick Reference

### Decision Tree

```
Is the command nested?
├─ No → Use normal quoting rules
└─ Yes → How many levels?
    ├─ 1 level → Use opposite quotes (outer single, inner double or vice versa)
    ├─ 2 levels → Alternate quotes + escape inner
    └─ 3+ levels → Use heredoc/here-string or intermediate script
```

### Golden Rules

| # | Rule | Example |
|---|------|---------|
| 1 | Alternate quote types at each level | `bash -c 'echo "Hello"'` |
| 2 | Use heredoc/here-string for 3+ lines or 2+ nesting | See below |
| 3 | Test each nesting level separately | Build from innermost out |
| 4 | Use intermediate scripts for complex cases | `scp script.sh host:; ssh host 'bash script.sh'` |
| 5 | In PowerShell, use `--%` for external programs | `git --% commit -m "msg"` |
| 6 | Escape `$` in Bash when calling PowerShell | `powershell.exe -Command '...$_...'` |

### Escape Characters

| Shell | Escape | Example |
|-------|--------|---------|
| Bash/Zsh | `\` | `echo "Price: \$100"` |
| PowerShell | `` ` `` | ``Write-Host "Price: `$100"`` |
| CMD | `^` | `echo Price: ^$100` |

### Quoting Rules

| Shell | Literal (no expansion) | Expandable |
|-------|------------------------|------------|
| Bash | `'$var'` → `$var` | `"$var"` → `value` |
| PowerShell | `'$var'` → `$var` | `"$var"` → `value` |
| CMD | N/A | `%var%` |

---

## 1. Here-Strings & Heredocs

**The #1 tool for avoiding quoting hell.**

### PowerShell Here-Strings

```powershell
# Literal (single quotes) - NO expansion
$literal = @'
$variables and "quotes" stay literal
Special chars: \ $ @ " ' `
'@

# Expandable (double quotes) - WITH expansion
$name = "John"
$expandable = @"
Hello $name
Date: $(Get-Date -Format 'yyyy-MM-dd')
Literal dollar: `$100
"@
```

### Bash Heredocs

```bash
# Literal (quoted EOF) - NO expansion
cat << 'EOF'
$variables and "quotes" stay literal
EOF

# Expandable (unquoted EOF) - WITH expansion
name="John"
cat << EOF
Hello $name
Date: $(date +%Y-%m-%d)
Literal dollar: \$100
EOF

# Store in variable
content=$(cat << 'EOF'
Multi-line content here
EOF
)
```

### Use Cases

**JSON:**
```powershell
$json = @'
{"user": {"name": "O'Brien", "path": "C:\\Files"}}
'@
```

```bash
json=$(cat << 'EOF'
{"user": {"name": "O'Brien", "path": "/home/user"}}
EOF
)
```

**SQL:**
```powershell
$sql = @"
SELECT * FROM Users WHERE Name = 'O''Brien'
"@
```

**Git commits:**
```bash
git commit -m "$(cat << 'EOF'
Fix user's "profile" bug

- Resolved O'Brien's account issue
- Updated "Edit Profile" functionality
EOF
)"
```

```powershell
$msg = @"
Fix user's "profile" bug

- Resolved O'Brien's account issue
"@
git commit -m $msg
```

---

## 2. PowerShell-Specific Patterns

### Stop-Parsing Token (--%)

Tells PowerShell to pass everything literally to external programs.

```powershell
# Without --% (PowerShell mangles quotes)
git commit -m "Fix user's "profile" bug"  # BROKEN

# With --% (passed literally)
git --% commit -m "Fix user's "profile" bug"  # WORKS

# More examples
cmd --% /c dir "C:\Program Files" /s
icacls --% "C:\Files\test.txt" /grant:r "User:(RX)"
```

**Limitation:** Variables don't expand after `--%`
```powershell
# $file won't expand - use alternative approaches
$file = "C:\test.txt"
icacls --% $file /grant:r "User:(RX)"  # WRONG

# Workaround: use cmd /c
cmd /c "icacls `"$file`" /grant:r `"User:(RX)`""
```

### Comparison Operators

PowerShell uses `-eq`, `-ne`, `-gt`, etc. (not `==`, `!=`, `>`)

```powershell
# String comparison
if ($name -eq "John") { ... }
if ($name -ne "Jane") { ... }
if ($name -like "*oh*") { ... }    # Wildcard
if ($name -match "^J") { ... }     # Regex

# Numeric comparison
if ($count -gt 5) { ... }
if ($count -le 20) { ... }

# In pipelines
Get-Process | Where-Object { $_.CPU -gt 100 }
Get-Service | Where-Object { $_.Status -eq "Running" }

# Multiple conditions
Get-Process | Where-Object { $_.Name -eq "chrome" -and $_.CPU -gt 50 }
```

**Bash equivalent:**
```bash
# String: =, !=, or == in [[ ]]
[ "$name" = "John" ]
[[ "$name" == *oh* ]]    # Wildcard
[[ "$name" =~ ^J ]]      # Regex

# Numeric: -eq, -ne, -gt, -lt (same names, different context)
[ $count -gt 5 ]
```

### Calling External Programs

```powershell
# Path with spaces - use call operator &
& "C:\Program Files\App\app.exe" --arg value

# Arguments with quotes - escape with backtick
git commit -m "`"Fix bug`""

# Or use here-string
$msg = @'
Fix user's "profile" bug
'@
git commit -m $msg

# Complex arguments - use Start-Process
Start-Process "C:\Program Files\App\app.exe" -ArgumentList @(
    '--config', 'C:\My Files\config.txt',
    '--output', 'C:\Output'
) -NoNewWindow -Wait
```

---

## 3. Cross-Shell Calls

### PowerShell from Bash

```bash
# WRONG - Bash expands $_
powershell.exe -Command "Get-Process | Where-Object {$_.Name -eq 'chrome'}"

# CORRECT - Single quotes protect from Bash
powershell.exe -Command 'Get-Process | Where-Object {$_.Name -eq "chrome"}'

# CORRECT - Escape the dollar sign
powershell.exe -Command "Get-Process | Where-Object {\$_.Name -eq 'chrome'}"

# Complex with paths
powershell.exe -Command 'Get-Content "C:\Program Files\App\config.txt" | Select-String "pattern"'
```

### Bash from PowerShell

```powershell
# CORRECT - Single quotes in PowerShell
bash -c 'echo "Hello World"'

# CORRECT - Backtick escaping
bash -c "echo \`"Hello World\`""

# Complex with grep/awk (note doubled single quotes)
bash -c 'grep "error" /var/log/app.log | awk ''{print $1}'''

# BEST - Use here-string
$cmd = @'
grep "error" /var/log/app.log | awk '{print $1}' | sort | uniq
'@
bash -c $cmd
```

### CMD from PowerShell

```powershell
# Use --% stop-parsing token
cmd --% /c dir "C:\Program Files"

# Or backtick escaping
cmd /c dir `"C:\Program Files`"

# Complex CMD command
cmd --% /c for /f "tokens=*" %i in ('dir /b *.txt') do echo %i
```

### PowerShell from CMD

```cmd
REM Use single quotes for PowerShell command
powershell.exe -Command 'Get-Process | Where-Object {$_.Name -eq "chrome"}'

REM Or use -File with script
echo Get-Process ^| Where-Object {$_.Name -eq "chrome"} > temp.ps1
powershell.exe -File temp.ps1
del temp.ps1
```

---

## 4. Nested Commands

### Docker Exec

```bash
# 1 level - alternate quotes
docker exec container bash -c 'echo "Hello"'

# With SQL
docker exec container bash -c 'mysql -e "SELECT * FROM users"'

# Complex - use heredoc
docker exec container bash -c "$(cat << 'EOF'
mysql -e "SELECT * FROM users WHERE name='O\"Brien'"
grep "error" "/app/log files/app.log"
EOF
)"
```

```powershell
# From PowerShell
docker exec container bash -c 'mysql -e "SELECT * FROM users"'

# Complex - use here-string
$cmd = @'
mysql -e "SELECT * FROM users WHERE name='admin'"
grep "error" /var/log/app.log
'@
docker exec container bash -c $cmd
```

### SSH

```bash
# 1 level
ssh user@host 'grep "error" /var/log/syslog'

# 2 levels (SSH -> Docker)
ssh user@host 'docker exec container bash -c "grep \"error\" /var/log/app.log"'

# 3+ levels - use intermediate script
cat > /tmp/remote.sh << 'EOF'
docker exec mysql bash -c 'mysql -e "CREATE DATABASE app"'
EOF
scp /tmp/remote.sh user@host:/tmp/
ssh user@host 'bash /tmp/remote.sh'
```

### Multi-Level Example

**Scenario:** Local -> SSH -> Docker -> MySQL

```bash
# WRONG - Quote chaos
ssh host "docker exec db bash -c "mysql -e "SELECT 1"""

# HARD TO READ but works
ssh host 'docker exec db bash -c "mysql -e \"SELECT 1\""'

# BEST - Use intermediate script
cat > /tmp/deploy.sh << 'EOF'
#!/bin/bash
docker exec db bash -c 'mysql -e "CREATE DATABASE app"'
docker exec db bash -c 'mysql -e "INSERT INTO t VALUES (1, \"O'"'"'Brien\")"'
EOF
scp /tmp/deploy.sh host:/tmp/
ssh host 'bash /tmp/deploy.sh'
```

---

## 5. Common Scenarios

### Paths with Spaces

```bash
# Always quote
cd "/c/Program Files/My App"
"/c/Program Files/My App/app.exe" --arg value

# In PowerShell call
powershell.exe -Command '& "C:\Program Files\App\app.exe" --config "C:\My Files\cfg.txt"'
```

```powershell
# Use call operator
& "C:\Program Files\App\app.exe"

# With arguments
& "C:\Program Files\App\app.exe" --config "C:\My Files\config.txt"

# Start-Process for complex cases
Start-Process "C:\Program Files\App\app.exe" -ArgumentList @(
    '--config', 'C:\My Files\config.txt'
) -NoNewWindow -Wait
```

### JSON in API Calls

```bash
# Simple - single quotes
curl -X POST -H "Content-Type: application/json" \
  -d '{"name": "John"}' http://api.example.com

# Complex - heredoc
json=$(cat << 'EOF'
{"user": {"name": "O'Brien", "role": "admin"}}
EOF
)
curl -X POST -H "Content-Type: application/json" -d "$json" http://api.example.com
```

```powershell
# Here-string
$json = @'
{"user": {"name": "O'Brien", "role": "admin"}}
'@
Invoke-RestMethod -Method Post -Uri 'http://api.example.com' -Body $json -ContentType 'application/json'

# Or use PowerShell objects (best)
$data = @{ user = @{ name = "O'Brien"; role = "admin" } }
$json = $data | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method Post -Uri 'http://api.example.com' -Body $json -ContentType 'application/json'
```

### Azure CLI

```powershell
# JSON tags - use here-string
$tags = @'
{"Environment":"Production","Owner":"John"}
'@
az vm create --name "MyVM" --resource-group "MyRG" --tags $tags

# JMESPath queries - use here-string
$query = @'
[?location=='eastus'].{Name:name,RG:resourceGroup}
'@
az vm list --query $query --output table
```

```bash
# Single quotes protect everything
az vm create --name "MyVM" --resource-group "MyRG" \
  --tags '{"Environment":"Production"}'

az vm list --query '[?location==`eastus`]' --output table
```

---

## 6. Anti-Patterns

```bash
# Same quotes at multiple levels
powershell.exe -Command "Get-Content "file.txt""  # BROKEN

# Forgetting to escape $ in Bash
powershell.exe -Command "Where {$_.Name}"  # $_ expands to nothing

# Complex inline JSON
curl -d "{\"user\":{\"name\":\"O'Brien\"}}" api  # NIGHTMARE

# Not testing each level
ssh host "docker exec c bash -c "mysql -e "SELECT 1"""  # IMPOSSIBLE TO DEBUG

# Using --% with variables
icacls --% $file /grant:r "User:(RX)"  # $file won't expand

# Wrong comparison operators
powershell.exe -Command "if ($x == 10) {...}"  # Use -eq, not ==
```

---

## Summary Table

| Scenario | Bash | PowerShell |
|----------|------|------------|
| Literal string | `'text'` | `'text'` |
| Variable expansion | `"$var"` | `"$var"` |
| Escape char | `\` | `` ` `` |
| Multi-line literal | `<< 'EOF'` | `@' '@` |
| Multi-line expandable | `<< EOF` | `@" "@` |
| Call program with spaces | `"/path/app"` | `& "C:\path\app"` |
| External program args | N/A | `--% args` |
| JSON | `'{...}'` | `@'{...}'@` or `ConvertTo-Json` |
