# Setup & Installation

## Installation Options

### Option 1: Global Install (Recommended)

```bash
npm install -g llm-context
```

Use from anywhere:
```bash
cd ~/any-project
llm-context analyze
```

### Option 2: Project-Local Install

```bash
cd ~/my-project
npm install --save-dev llm-context
npx llm-context analyze
```

### Option 3: Direct Use (No Install)

```bash
npx llm-context analyze
```

## Project Initialization

### For New Projects

```bash
cd ~/my-project
llm-context init
```

This will:
1. Create `package.json` if missing
2. Install dependencies (`@babel/parser`, `@babel/traverse`, etc)
3. Run initial analysis
4. Generate `.llm-context/` directory

### For Existing Projects

```bash
cd ~/existing-project
llm-context analyze
```

## Verify Installation

```bash
# Check version
llm-context version

# Check help
llm-context help

# Test analysis (if in a project with .js files)
llm-context analyze
```

## Dependencies

Auto-installed by `llm-context init`:
- `@babel/parser` - JavaScript parsing
- `@babel/traverse` - AST traversal
- `@sourcegraph/scip-typescript` - SCIP indexing
- `protobufjs` - Protocol buffer parsing

## Requirements

- Node.js ≥ 16.0.0
- JavaScript or TypeScript project
- Unix-like system (Linux, macOS) or Windows

## Troubleshooting Installation

**"npm install -g" fails with permissions**
```bash
# Use npm's recommended fix
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Then retry
npm install -g llm-context
```

**"command not found: llm-context" after install**
```bash
# Check npm global bin path
npm bin -g

# Add to PATH in ~/.bashrc or ~/.zshrc
export PATH="$(npm bin -g):$PATH"
```

**Dependencies fail to install**
```bash
# Clear cache and retry
npm cache clean --force
npm install -g llm-context
```
