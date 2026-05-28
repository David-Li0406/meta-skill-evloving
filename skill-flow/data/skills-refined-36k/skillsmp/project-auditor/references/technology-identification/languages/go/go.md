# Go

**Category**: languages
**Description**: Go (Golang) programming language - fast, statically typed, compiled language designed at Google
**Homepage**: https://go.dev

## Package Detection

### GO
- `golang.org/x/*`
- `github.com/golang/*`

## Configuration Files

- `go.mod`
- `go.sum`
- `go.work`
- `go.work.sum`
- `.go-version`
- `Gopkg.toml` (legacy dep)
- `Gopkg.lock` (legacy dep)

## File Extensions

- `.go`

## Import Detection

### Go
**Pattern**: `^package\s+\w+`
- Package declaration
- Example: `package main`

**Pattern**: `import\s+\(`
- Multi-line import
- Example: `import ( "fmt" "os" )`

**Pattern**: `import\s+"[^"]+"`
- Single import
- Example: `import "fmt"`

**Pattern**: `func\s+\w+\(`
- Function declaration
- Example: `func main() {}`

**Pattern**: `func\s+\(\w+\s+\*?\w+\)\s+\w+\(`
- Method declaration
- Example: `func (s *Server) Start() error {}`

## Environment Variables

- `GOPATH`
- `GOROOT`
- `GOPROXY`
- `GOPRIVATE`
- `GOMODCACHE`
- `GO111MODULE`
- `GOOS`
- `GOARCH`

## Version Indicators

- Go 1.22 (current)
- Go 1.21 (supported)
- Go 1.20 (supported)

## Detection Notes

- Look for `.go` files in repository
- go.mod is the primary indicator (Go modules)
- Check for `package main` for executables
- `go.sum` contains dependency checksums
- Standard library has no external dependencies

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **go.mod Detection**: 95% (HIGH)
- **Package Declaration Detection**: 90% (HIGH)
