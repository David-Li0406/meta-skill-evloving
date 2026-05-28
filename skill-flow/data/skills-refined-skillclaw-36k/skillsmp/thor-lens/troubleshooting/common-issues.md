# Common Issues

## Build Issues

### "Command not found: make"

Install build tools:

| OS | Command |
|----|---------|
| macOS | `xcode-select --install` |
| Ubuntu/Debian | `sudo apt install build-essential` |
| Windows | Use Git Bash or install Make via Chocolatey |

### "go: command not found"

Go is not in PATH. Add it:

```bash
export PATH=$PATH:/usr/local/go/bin
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

### "npm: command not found"

Node.js is not installed. Install it:

| OS | Command |
|----|---------|
| macOS | `brew install node` |
| Ubuntu/Debian | `sudo apt install nodejs npm` |
| Windows | `choco install nodejs` |

### Frontend Build Fails

Clear cache and reinstall:

```bash
cd web
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Import Issues

### Import Fails Immediately

**Check input file exists:**
```bash
ls -lh /path/to/audit.jsonl
```

**Check file is not empty:**
```bash
wc -l /path/to/audit.jsonl
# Should show > 0 lines
```

**Check file is valid JSONL:**
```bash
head -1 /path/to/audit.jsonl | jq .
# Should parse without error
```

### Import Takes Forever / Hangs

**Large file on slow storage:**
- Use local SSD instead of network share
- Increase workers: `--workers 8`

**Corrupted file:**
- For gzip: `gzip -t file.jsonl.gz`
- Try decompressing first: `gunzip file.jsonl.gz`

### Case Folder Not Created

Check for error messages during import. Common causes:
- Permission denied (run in writable directory)
- Disk full
- Invalid input file format

## Serve Issues

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8080  # Linux/macOS
netstat -ano | findstr :8080  # Windows

# Use different port
./thorlens serve --case ./cases/mycase --port 9000
```

### "Case not found" Error

Verify case directory exists and has correct structure:

```bash
ls -la ./cases/mycase/
# Should show:
# meta.json
# events/
# annotations.sqlite
```

### Server Starts but UI Shows Error

Check API is responding:

```bash
curl http://127.0.0.1:8080/api/meta | jq .
```

If this fails, check server output for errors.

## General Troubleshooting

### Check THOR Lens Version

```bash
./thorlens --version
```

### Verify Go Installation

```bash
go version
# Should show go1.21 or later
```

### Verify Node.js Installation

```bash
node --version
npm --version
```

### Check Disk Space

```bash
df -h .
```

### Check Memory

```bash
free -h  # Linux
vm_stat  # macOS
```

## Getting Help

When reporting issues, include:

1. Operating system and version
2. THOR Lens version (if known)
3. Exact command that failed
4. Full error message
5. Input file size and format
6. Output of `ls -la ./cases/<name>/` if relevant
