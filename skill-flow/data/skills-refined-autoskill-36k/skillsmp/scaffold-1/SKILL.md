---
name: scaffold
description: Scaffold a new project in a subdirectory
user-invocable: true
argument-hint: <language> <project-name>
allowed-tools: Bash, Write, Read
---

# Scaffold New Project

Create a new project in a subdirectory.

## Usage

`/scaffold <language> <project-name>`

## Supported Languages

### Python
```bash
mkdir -p <project-name> && cd <project-name>
uv init
uv add --dev pytest ruff
```

### Rust
```bash
cargo new <project-name>
cd <project-name>
```

### Go
```bash
mkdir -p <project-name> && cd <project-name>
go mod init github.com/orangekame3/vibebox/<project-name>
```

### Node.js / TypeScript
```bash
mkdir -p <project-name> && cd <project-name>
npm init -y
# For TypeScript:
npm install -D typescript @types/node
npx tsc --init
```

## Arguments

Parse $ARGUMENTS as:
- First word: language (python, rust, go, node, ts)
- Second word: project name

If project name is omitted, ask for it.
