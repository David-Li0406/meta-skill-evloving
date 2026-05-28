---
name: bash-linux
description: Use this skill when working on macOS or Linux systems to leverage essential Bash terminal commands, scripting techniques, and process management.
---

# Bash Linux Patterns

> Essential patterns for Bash on Linux/macOS.

## 1. Operator Syntax

### Chaining Commands

| Operator | Meaning                   | Example                             |
| -------- | ------------------------- | ----------------------------------- |
| `;`      | Run sequentially          | `cmd1; cmd2`                        |
| `&&`     | Run if previous succeeded | `npm install && npm run dev`        |
| `\|\|`   | Run if previous failed    | `npm test \|\| echo "Tests failed"` |
| `\|`     | Pipe output               | `ls \| grep ".js"`                  |

## 2. File Operations

### Essential Commands

| Task            | Command                              |
| --------------- | ------------------------------------ |
| List all        | `ls -la`                             |
| Find files      | `find . -name "*.js" -type f`        |
| File content    | `cat file.txt`                       |
| First N lines   | `head -n 20 file.txt`                |
| Last N lines    | `tail -n 20 file.txt`                |
| Follow log      | `tail -f log.txt`                    |
| Search in files | `grep -r "pattern" --include="*.js"` |
| File size       | `du -sh *`                           |
| Disk usage      | `df -h`                              |

## 3. Process Management

| Task           | Command                       |
| -------------- | ----------------------------- |
| List processes | `ps aux`                      |
| Find by name   | `ps aux \| grep node`         |
| Kill by PID    | `kill -9 <PID>`               |
| Find port user | `lsof -i :3000`               |
| Kill port      | `kill -9 $(lsof -t -i :3000)` |
| Background     | `npm run dev &`               |
| Jobs           | `jobs -l`                     |
| Bring to front | `fg %1`                       |

## 4. Text Processing

### Core Tools

| Tool   | Purpose         | Example                         |
| ------ | --------------- | ------------------------------- |
| `grep` | Search          | `grep -rn "TODO" src/`          |
| `sed`  | Replace         | `sed -i 's/old/new/g' file.txt` |
| `awk`  | Extract columns | `awk '{print $1}' file.txt`     |
| `cut`  | Cut fields      | `cut -d',' -f1 data.csv`        |
| `sort` | Sort lines      | `sort -u file.txt`              |
| `uniq` | Unique lines    | `sort file.txt \| uniq -c`      |
| `wc`   | Count lines     | `wc -l file.txt`                |

## 5. Environment Variables

| Task | Command |
|------|---------|
| View all | `env` or `printenv` |
| View one | `echo $PATH` |
| Set temporary | `export VAR="value"` |
| Set in script | `VAR="value" command` |
| Add to PATH | `export PATH="$PATH:/new/path"` |

## 6. Network

| Task | Command |
|------|---------|
| Download | `curl -O https://example.com/file` |
| API request | `curl -X GET https://api.example.com` |
| POST JSON | `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL` |
| Check port | `nc -zv localhost 3000` |
| Network info | `ifconfig` or `ip addr` |

## 7. Script Template

```bash
#!/bin/bash
# Your script here
```