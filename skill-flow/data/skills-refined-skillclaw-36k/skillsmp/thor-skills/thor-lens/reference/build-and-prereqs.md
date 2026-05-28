# Build & Prerequisites

## System Requirements

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| **Go** | 1.21+ | `go version` |
| **Node.js** | 18+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **Make** | any | `make --version` |

## Installing Prerequisites

### macOS (with Homebrew)

```bash
brew install go node
```

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install golang-go nodejs npm build-essential
```

### Windows (with Chocolatey)

```powershell
choco install golang nodejs
```

## Building THOR Lens

### Clone Repository

```bash
git clone https://github.com/NextronSystems/thor-lens.git
cd thor-lens
```

### Full Build

```bash
make build
```

This performs:
1. `npm install` - Install frontend dependencies
2. `npm run build` - Build React frontend to `web/dist/`
3. `go build` - Compile Go backend to `./thorlens`

### Available Make Targets

| Target | Description |
|--------|-------------|
| `make` | Full build (frontend + backend) |
| `make rebuild` | Quick rebuild after code changes |
| `make dev` | Start backend server on :8080 |
| `make dev-frontend` | Start Vite dev server with hot reload on :5173 |
| `make test` | Run Go tests |
| `make clean` | Remove build artifacts |
| `make help` | Show all available targets |

## Build Verification

```bash
# Check binary was created
ls -la ./thorlens

# Check version (if implemented)
./thorlens --version

# Quick import test
./thorlens import --help
```

## Development Mode

For active development with hot reload:

**Terminal 1 - Go backend:**
```bash
./thorlens serve --case ./cases/demo --port 8080
```

**Terminal 2 - Vite dev server:**
```bash
cd web
npm run dev
```

Open **http://localhost:5173** - the Vite dev server proxies API requests to the Go backend.

## Build Troubleshooting

### "Command not found: make"

Install build tools:
- macOS: `xcode-select --install`
- Ubuntu: `sudo apt install build-essential`
- Windows: Use Git Bash or install Make via Chocolatey

### "go: command not found"

Ensure Go is in PATH:
```bash
export PATH=$PATH:/usr/local/go/bin
# Add to ~/.bashrc or ~/.zshrc for persistence
```

### "npm: command not found"

Install Node.js which includes npm:
- macOS: `brew install node`
- Ubuntu: `sudo apt install nodejs npm`

### npm permission errors

Don't use sudo with npm. Fix permissions:
```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

### Frontend build fails

```bash
# Clear npm cache and reinstall
cd web
rm -rf node_modules package-lock.json
npm install
npm run build
```
