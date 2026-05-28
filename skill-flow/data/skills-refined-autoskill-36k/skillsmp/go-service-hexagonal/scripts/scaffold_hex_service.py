#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


GO_VERSION = "1.25"


@dataclass
class Options:
    root: Path
    module: str | None
    service: str
    kinds: tuple[str, ...]
    http_framework: str
    http_pprof: bool
    http_trace: bool
    settings_mode: str
    skip_deps: bool


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    _write(path, content)


def _maybe_write_go_mod(root: Path, module: str | None) -> bool:
    if module is None:
        return False
    go_mod = root / "go.mod"
    if go_mod.exists():
        return False
    _write(
        go_mod,
        f"module {module}\n\ngo {GO_VERSION}\n",
    )
    return True


def _install_deps_for_new_project(root: Path) -> None:
    env = os.environ.copy()
    env["GOCACHE"] = str(root / ".gocache")
    env["GOMODCACHE"] = str(root / ".gomodcache")

    try:
        proc = subprocess.run(
            ["go", "mod", "tidy"],
            cwd=root,
            env=env,
            check=False,
        )
    except FileNotFoundError:
        print("⚠️  go not found; skipping dependency install")
        return

    if proc.returncode != 0:
        print("⚠️  go mod tidy failed (likely no network access); run `go mod tidy` later in an online environment.")

def _discover_module_from_go_mod(root: Path) -> str | None:
    go_mod = root / "go.mod"
    if not go_mod.exists():
        return None
    for line in go_mod.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("module "):
            return line.removeprefix("module ").strip()
    return None


def _svc(root: Path) -> Path:
    return root / "internal"


def _base_tree(opt: Options) -> None:
    required = [
        "internal/domain",
        "internal/app",
        "internal/interface",
        "internal/adapter",
        "internal/bootstrap",
    ]
    if opt.settings_mode == "config":
        required.append("internal/interface/options")
    if "grpc" in opt.kinds:
        required.append(f"api/proto/{opt.service}/v1")
    if "http" in opt.kinds:
        required.append("test")

    for rel in required:
        (opt.root / rel).mkdir(parents=True, exist_ok=True)

    _write_project_docs(opt)

    if opt.settings_mode == "config":
        _write_options_package(opt)

    _write_bootstrap_compose(opt)


def _write_options_package(opt: Options) -> None:
    _write(
        _svc(opt.root) / "interface" / "options" / "options.go",
        """package options

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/knadh/koanf/v2"
	"github.com/knadh/koanf/parsers/json"
	"github.com/knadh/koanf/parsers/toml"
	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/file"
)

const (
	envHTTPAddr   = "HTTP_ADDR"
	envPprofAddr  = "PPROF_ADDR"
	envPprofPort  = "PPROF_PORT"
	envLogLevel   = "LOG_LEVEL"
	envConfigPath = "CONFIG_PATH"
)

type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

type Loader interface {
	Load() (Settings, error)
}

type Store interface {
	Get() Settings
	Reload() (Settings, error)
}

type Repository struct {
	loader   Loader
	settings Settings
	lastErr error
}

func NewRepository(loader Loader) *Repository {
	repo := &Repository{loader: loader}
	_, _ = repo.Reload()
	return repo
}

func (r *Repository) Get() Settings {
	return r.settings
}

func (r *Repository) Reload() (Settings, error) {
	if r.loader == nil {
		return r.settings, nil
	}
	settings, err := r.loader.Load()
	r.lastErr = err
	r.settings = settings
	return r.settings, err
}

func (r *Repository) LastError() error {
	return r.lastErr
}

type EnvLoader struct{}

func (EnvLoader) Load() (Settings, error) {
	settings := Settings{
		HTTPAddr:  stringOr(envHTTPAddr, ":8080"),
		PprofAddr: stringOr(envPprofAddr, "127.0.0.1"),
		PprofPort: os.Getenv(envPprofPort),
		LogLevel:  os.Getenv(envLogLevel),
	}
	configPath := os.Getenv(envConfigPath)
	if configPath == "" {
		return settings, nil
	}
	settings, err := applyConfigFile(settings, configPath)
	if err != nil {
		return settings, err
	}
	return applyEnvOverrides(settings), nil
}

func applyConfigFile(base Settings, path string) (Settings, error) {
	k := koanf.New(".")
	parser, err := parserForPath(path)
	if err != nil {
		return base, err
	}
	if err := k.Load(file.Provider(path), parser); err != nil {
		return base, err
	}
	return mergeConfig(base, k), nil
}

func parserForPath(path string) (koanf.Parser, error) {
	switch strings.ToLower(filepath.Ext(path)) {
	case "":
		return toml.Parser(), nil
	case ".json":
		return json.Parser(), nil
	case ".yaml", ".yml":
		return yaml.Parser(), nil
	case ".toml":
		return toml.Parser(), nil
	default:
		return nil, fmt.Errorf("unsupported config extension: %s", filepath.Ext(path))
	}
}

func applyEnvOverrides(base Settings) Settings {
	if v := os.Getenv(envHTTPAddr); v != "" {
		base.HTTPAddr = v
	}
	if v := os.Getenv(envPprofAddr); v != "" {
		base.PprofAddr = v
	}
	if v := os.Getenv(envPprofPort); v != "" {
		base.PprofPort = v
	}
	if v := os.Getenv(envLogLevel); v != "" {
		base.LogLevel = v
	}
	return base
}

func mergeConfig(base Settings, k *koanf.Koanf) Settings {
	if k.Exists("http_addr") {
		base.HTTPAddr = k.String("http_addr")
	}
	if k.Exists("pprof_addr") {
		base.PprofAddr = k.String("pprof_addr")
	}
	if k.Exists("pprof_port") {
		base.PprofPort = k.String("pprof_port")
	}
	if k.Exists("log_level") {
		base.LogLevel = k.String("log_level")
	}
	return base
}

func stringOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
""",
    )


def _write_project_docs(opt: Options) -> None:
    binaries = []
    for kind in opt.kinds:
        if kind == "http":
            binaries.append(f"- `cmd/{opt.service}-api`: HTTP server (Echo default)")
        elif kind == "grpc":
            binaries.append(f"- `cmd/{opt.service}-grpc`: gRPC server")
        elif kind == "worker":
            binaries.append(f"- `cmd/{opt.service}-worker`: background worker")
        elif kind == "cli":
            binaries.append(f"- `cmd/{opt.service}-cli`: CLI")

    binaries_block = "\n".join(binaries) if binaries else "- (none scaffolded)"
    debug_section = ""
    env_pprof: list[str] = []
    if "http" in opt.kinds and (opt.http_pprof or opt.http_trace):
        debug_section = """
## Debug endpoints (optional)

When scaffolded with `--http-pprof` and/or `--http-trace`, these are served by a separate debug HTTP server when `PPROF_PORT` is set:

- `GET http://$PPROF_ADDR:$PPROF_PORT/debug/pprof/` (pprof index)
- `GET http://$PPROF_ADDR:$PPROF_PORT/debug/pprof/trace` (execution trace)
"""
        env_pprof = [
            "- `PPROF_ADDR` (optional; default `127.0.0.1`)",
            "- `PPROF_PORT` (optional; enables debug server on `$PPROF_ADDR:<port>`)",
        ]

    env_lines: list[str] = []
    if opt.settings_mode == "none":
        env_lines = ["- (none; defaults are compiled into bootstrap)"]
    else:
        env_lines = [
            "- `HTTP_ADDR` (default `:8080`)",
            "- `LOG_LEVEL` (e.g. `info`, `debug`)",
        ]
        if opt.settings_mode == "config":
            env_lines.append(
                "- `CONFIG_PATH` (optional; config file path; formats: json/yaml/toml; default `toml` when no extension; keys: `http_addr`, `pprof_addr`, `pprof_port`, `log_level`)"
            )
        if env_pprof:
            env_lines.extend(env_pprof)
    env_block = "\n".join(env_lines)
    config_note = ""
    if opt.settings_mode == "config":
        config_note = "\nEnvironment values override config values when `CONFIG_PATH` is set."

    _write_if_missing(
        opt.root / "README.md",
        f"""# {opt.service}

Go service scaffold using hexagonal (ports-and-adapters) architecture.

## Binaries

{binaries_block}

## Health endpoints (HTTP)

- `GET /health/live`
- `GET /health/ready`
{debug_section}

## Local run (HTTP)

```bash
go run ./cmd/{opt.service}-api
```

Environment:

{env_block}
{config_note}
""",
    )

    compose_call = "bootstrap.Compose(settingsStore)" if opt.settings_mode == "config" else "bootstrap.Compose(settings)"
    compose_entrypoint = (
        " (or build a settings store via `internal/interface/options` and call `bootstrap.Compose(settingsStore)`)"
        if opt.settings_mode == "config"
        else ""
    )
    options_tree_line = (
        "│   │   └── options/                 # Env/config settings loading\n"
        if opt.settings_mode == "config"
        else ""
    )
    if opt.settings_mode == "config":
        compose_guidance = (
            "- Load settings via `internal/interface/options` (env + optional config file via Koanf), store them in a settings store, and pass it into "
            "`bootstrap.Compose(settingsStore)` (or use `bootstrap.ComposeFromEnv()`).\n"
            "- `bootstrap.Compose(settingsStore)` returns a `Root` struct that holds initialized dependencies (logger, servers, clients, repos)."
        )
    elif opt.settings_mode == "env":
        compose_guidance = (
            "- Load settings via `bootstrap.ComposeFromEnv()` and override with `bootstrap.Compose(settings)` when needed.\n"
            "- `bootstrap.Compose(settings)` returns a `Root` struct that holds initialized dependencies (logger, servers, clients, repos)."
        )
    else:
        compose_guidance = (
            "- Use `bootstrap.ComposeFromEnv()` for defaults (no env/config), or call `bootstrap.Compose(settings)` when you need overrides.\n"
            "- `bootstrap.Compose(settings)` returns a `Root` struct that holds initialized dependencies (logger, servers, clients, repos)."
        )

    _write_if_missing(
        opt.root / "AGENTS.md",
        f"""# Agent Instructions

This repository follows Go best practices and hexagonal (ports-and-adapters / “jexagonal”) architecture.

## Architecture (hexagonal)

**Dependency rule (must hold):**

- `internal/domain` depends on nothing in the service (only stdlib / pure helpers).
- `internal/app` depends on `domain` and outbound ports in `internal/adapter`.
- Inbound ports in `internal/interface` and outbound ports in `internal/adapter` define interfaces at the boundaries.
- Inbound adapters under `internal/interface/*` depend on inbound ports in `internal/interface` (+ domain types for mapping).
- Outbound adapters under `internal/adapter/*` depend on outbound ports in `internal/adapter` (+ domain types for mapping).
- **All wiring happens only in the composition root**: `internal/bootstrap/compose.go` (`{compose_call}`).
- `cmd/*` is a thin entrypoint: call `bootstrap.ComposeFromEnv()`{compose_entrypoint}, start servers/loops, handle shutdown.

**Design guidance:**

- Keep ports small and use-case focused; avoid “interface soup”.
- Keep transport/ORM/SDK types out of `domain` and `app` (map in adapters).
- Prefer explicit package names over generic `util`/`common`.

## Project structure (all supported shapes)

The scaffolder creates only what you asked for, but these are the standard directories you may add over time:

```text
.
├── AGENTS.md
├── README.md
├── cmd/
│   ├── {opt.service}-api/          # HTTP server (Echo default)
│   ├── {opt.service}-grpc/         # gRPC server (optional)
│   ├── {opt.service}-worker/       # worker/consumer/scheduler (optional)
│   └── {opt.service}-cli/          # CLI tool (optional)
├── internal/
│   ├── domain/                      # Entities/value objects/invariants
│   ├── app/                         # Use-cases (application services)
│   ├── interface/                   # Inbound ports + adapters (http/grpc/cli/worker)
{options_tree_line}│   ├── adapter/                     # Outbound ports + adapters (db/queue/cache/httpclient)
│   └── bootstrap/
│       └── compose.go               # Single DI composition root
├── api/                            # Create only when you have contracts
│   ├── openapi/                    # OpenAPI specs (HTTP)
│   └── proto/                      # Protobuf IDL (gRPC)
├── configs/                        # Default configs / examples (optional)
├── deploy/                         # Docker/K8s/helm/terraform (optional)
├── migrations/                     # DB migrations (optional)
├── scripts/                        # Dev scripts (optional)
├── tools/                          # Codegen/tools helpers (optional)
├── pkg/                            # Public/reusable packages (rare; opt-in)
└── test/                           # Integration tests (package `test`)
```

## Composition root (DI)

- Put **all construction/injection** in `internal/bootstrap/compose.go`.
{compose_guidance}
- Adapters should be constructed with explicit dependencies (interfaces), not by reaching into globals.

## HTTP (when present)

- Always expose health endpoints:
  - `GET /health/live`
  - `GET /health/ready`
- Keep health handlers fast and dependency-light.
- Request logging must be enabled (Logrus-backed).
- Add profiling/debug endpoints only when needed (opt-in) and keep them on a separate debug server (set `PPROF_PORT`, optional `PPROF_ADDR`).

## Logging

- Use Logrus (`github.com/sirupsen/logrus`) for structured logs.
- Prefer fields (`WithField(s)`) over formatted strings.
- Control verbosity with `LOG_LEVEL` (e.g. `info`, `debug`).

## Testing

- Run `go test ./...` before finishing changes.
- Use `test/` (package `test`) for integration-style tests that exercise the composed app via `bootstrap.ComposeFromEnv()`.
- Keep most unit tests next to packages in `internal/...` as `*_test.go`.

## Go hygiene

- Format with `gofmt`.
- Keep imports tidy (`goimports` if available, otherwise `gofmt` + manual cleanup).
- Avoid long-lived contexts without cancellation; respect shutdown signals in `cmd/*`.
""",
    )

    make_run_target = f"{opt.service}-api"
    if "worker" in opt.kinds:
        make_run_target = f"{opt.service}-worker"
    if "http" in opt.kinds:
        make_run_target = f"{opt.service}-api"

    _write_if_missing(
        opt.root / "Makefile",
        f""".PHONY: help tidy fmt test build run

SERVICE ?= {opt.service}
BINARY ?= {make_run_target}

help:
\t@echo \"Targets: tidy fmt test build run\"
\t@echo \"Variables: SERVICE (default $(SERVICE)), BINARY (default $(BINARY))\"

tidy:
\tgo mod tidy

fmt:
\tgofmt -w $$(find . -name '*.go' -not -path './.gomodcache/*' -not -path './.gocache/*')

test:
\tgo test ./...

build:
\tgo build ./...

run:
\tgo run ./cmd/$(BINARY)
""",
    )


def _write_bootstrap_compose(opt: Options) -> None:
    if opt.module is None:
        raise SystemExit("Go module path not set; pass --module or run inside an existing module (go.mod).")

    if "http" in opt.kinds and opt.http_framework == "echo":
        debug_import = ""
        debug_field = ""
        if opt.http_pprof or opt.http_trace:
            debug_import = '\n\tdebughttp "REPLACE_MODULE/internal/interface/debughttp"'
            debug_field = f"\n\t\tDebugHTTPHandler: debughttp.Handler(debughttp.Options{{Pprof: {str(opt.http_pprof).lower()}, Trace: {str(opt.http_trace).lower()}}}),"
        if opt.settings_mode == "config":
            _write(
                _svc(opt.root) / "bootstrap" / "compose.go",
                """package bootstrap

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/sirupsen/logrus"

	options "REPLACE_MODULE/internal/interface/options"
	httpadapter "REPLACE_MODULE/internal/interface/http"
REPLACE_DEBUG_IMPORT
)

// Root is the single composition root for dependency injection.
// Add databases/clients/etc here and wire them into adapters/use-cases.
type Root struct {
	Logger     *logrus.Logger
	Settings   options.Settings
	SettingsStore options.Store
	HTTPServer *echo.Echo
	HTTPHandler http.Handler
	DebugHTTPHandler http.Handler
}

func Compose(settingsStore options.Store) *Root {
	settings := options.Settings{}
	if settingsStore != nil {
		settings = settingsStore.Get()
	}
	logger := newLogger(settings.LogLevel)
	srv := httpadapter.New(logger)
	return &Root{
		Logger:     logger,
		Settings:   settings,
		SettingsStore: settingsStore,
		HTTPServer: srv,
		HTTPHandler: srv,
REPLACE_DEBUG_FIELD
	}
}

func ComposeFromEnv() *Root {
	settingsStore := options.NewRepository(options.EnvLoader{})
	root := Compose(settingsStore)
	if err := settingsStore.LastError(); err != nil {
		root.Logger.WithError(err).Warn("options_load_failed")
	}
	return root
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
"""
                .replace("REPLACE_DEBUG_IMPORT", debug_import)
                .replace("REPLACE_DEBUG_FIELD", debug_field),
            )
        elif opt.settings_mode == "env":
            _write(
                _svc(opt.root) / "bootstrap" / "compose.go",
                """package bootstrap

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/sirupsen/logrus"

	httpadapter "REPLACE_MODULE/internal/interface/http"
REPLACE_DEBUG_IMPORT
)

const (
	envHTTPAddr  = "HTTP_ADDR"
	envPprofAddr = "PPROF_ADDR"
	envPprofPort = "PPROF_PORT"
	envLogLevel  = "LOG_LEVEL"
)

type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

// Root is the single composition root for dependency injection.
// Add databases/clients/etc here and wire them into adapters/use-cases.
type Root struct {
	Logger          *logrus.Logger
	Settings        Settings
	HTTPServer      *echo.Echo
	HTTPHandler     http.Handler
	DebugHTTPHandler http.Handler
}

func Compose(settings Settings) *Root {
	logger := newLogger(settings.LogLevel)
	srv := httpadapter.New(logger)
	return &Root{
		Logger:     logger,
		Settings:   settings,
		HTTPServer: srv,
		HTTPHandler: srv,
REPLACE_DEBUG_FIELD
	}
}

func ComposeFromEnv() *Root {
	return Compose(settingsFromEnv())
}

func settingsFromEnv() Settings {
	return Settings{
		HTTPAddr:  stringOr(envHTTPAddr, ":8080"),
		PprofAddr: stringOr(envPprofAddr, "127.0.0.1"),
		PprofPort: os.Getenv(envPprofPort),
		LogLevel:  os.Getenv(envLogLevel),
	}
}

func stringOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
"""
                .replace("REPLACE_DEBUG_IMPORT", debug_import)
                .replace("REPLACE_DEBUG_FIELD", debug_field),
            )
        else:
            _write(
                _svc(opt.root) / "bootstrap" / "compose.go",
                """package bootstrap

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/sirupsen/logrus"

	httpadapter "REPLACE_MODULE/internal/interface/http"
REPLACE_DEBUG_IMPORT
)

type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

// Root is the single composition root for dependency injection.
// Add databases/clients/etc here and wire them into adapters/use-cases.
type Root struct {
	Logger          *logrus.Logger
	Settings        Settings
	HTTPServer      *echo.Echo
	HTTPHandler     http.Handler
	DebugHTTPHandler http.Handler
}

func Compose(settings Settings) *Root {
	logger := newLogger(settings.LogLevel)
	srv := httpadapter.New(logger)
	return &Root{
		Logger:     logger,
		Settings:   settings,
		HTTPServer: srv,
		HTTPHandler: srv,
REPLACE_DEBUG_FIELD
	}
}

func ComposeFromEnv() *Root {
	return Compose(defaultSettings())
}

func defaultSettings() Settings {
	return Settings{
		HTTPAddr:  ":8080",
		PprofAddr: "127.0.0.1",
	}
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
"""
                .replace("REPLACE_DEBUG_IMPORT", debug_import)
                .replace("REPLACE_DEBUG_FIELD", debug_field),
            )
        return

    if "http" in opt.kinds and opt.http_framework == "nethttp":
        debug_import = ""
        debug_field = ""
        if opt.http_pprof or opt.http_trace:
            debug_import = '\n\tdebughttp "REPLACE_MODULE/internal/interface/debughttp"'
            debug_field = f"\n\t\tDebugHTTPHandler: debughttp.Handler(debughttp.Options{{Pprof: {str(opt.http_pprof).lower()}, Trace: {str(opt.http_trace).lower()}}}),"
        if opt.settings_mode == "config":
            _write(
                _svc(opt.root) / "bootstrap" / "compose.go",
                """package bootstrap

import (
	"net/http"
	"os"

	"github.com/sirupsen/logrus"

	options "REPLACE_MODULE/internal/interface/options"
	httpadapter "REPLACE_MODULE/internal/interface/http"
REPLACE_DEBUG_IMPORT
)

// Root is the single composition root for dependency injection.
// Add databases/clients/etc here and wire them into adapters/use-cases.
type Root struct {
	Logger     *logrus.Logger
	Settings   options.Settings
	SettingsStore options.Store
	HTTPHandler http.Handler
	DebugHTTPHandler http.Handler
}

func Compose(settingsStore options.Store) *Root {
	settings := options.Settings{}
	if settingsStore != nil {
		settings = settingsStore.Get()
	}
	logger := newLogger(settings.LogLevel)
	return &Root{
		Logger:      logger,
		Settings:    settings,
		SettingsStore: settingsStore,
		HTTPHandler: httpadapter.Router{Logger: logger}.Handler(),
REPLACE_DEBUG_FIELD
	}
}

func ComposeFromEnv() *Root {
	settingsStore := options.NewRepository(options.EnvLoader{})
	root := Compose(settingsStore)
	if err := settingsStore.LastError(); err != nil {
		root.Logger.WithError(err).Warn("options_load_failed")
	}
	return root
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
"""
                .replace("REPLACE_DEBUG_IMPORT", debug_import)
                .replace("REPLACE_DEBUG_FIELD", debug_field),
            )
        elif opt.settings_mode == "env":
            _write(
                _svc(opt.root) / "bootstrap" / "compose.go",
                """package bootstrap

import (
	"net/http"
	"os"

	"github.com/sirupsen/logrus"

	httpadapter "REPLACE_MODULE/internal/interface/http"
REPLACE_DEBUG_IMPORT
)

const (
	envHTTPAddr  = "HTTP_ADDR"
	envPprofAddr = "PPROF_ADDR"
	envPprofPort = "PPROF_PORT"
	envLogLevel  = "LOG_LEVEL"
)

type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

// Root is the single composition root for dependency injection.
// Add databases/clients/etc here and wire them into adapters/use-cases.
type Root struct {
	Logger          *logrus.Logger
	Settings        Settings
	HTTPHandler     http.Handler
	DebugHTTPHandler http.Handler
}

func Compose(settings Settings) *Root {
	logger := newLogger(settings.LogLevel)
	return &Root{
		Logger:      logger,
		Settings:    settings,
		HTTPHandler: httpadapter.Router{Logger: logger}.Handler(),
REPLACE_DEBUG_FIELD
	}
}

func ComposeFromEnv() *Root {
	return Compose(settingsFromEnv())
}

func settingsFromEnv() Settings {
	return Settings{
		HTTPAddr:  stringOr(envHTTPAddr, ":8080"),
		PprofAddr: stringOr(envPprofAddr, "127.0.0.1"),
		PprofPort: os.Getenv(envPprofPort),
		LogLevel:  os.Getenv(envLogLevel),
	}
}

func stringOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
"""
                .replace("REPLACE_DEBUG_IMPORT", debug_import)
                .replace("REPLACE_DEBUG_FIELD", debug_field),
            )
        else:
            _write(
                _svc(opt.root) / "bootstrap" / "compose.go",
                """package bootstrap

import (
	"net/http"
	"os"

	"github.com/sirupsen/logrus"

	httpadapter "REPLACE_MODULE/internal/interface/http"
REPLACE_DEBUG_IMPORT
)

type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

// Root is the single composition root for dependency injection.
// Add databases/clients/etc here and wire them into adapters/use-cases.
type Root struct {
	Logger          *logrus.Logger
	Settings        Settings
	HTTPHandler     http.Handler
	DebugHTTPHandler http.Handler
}

func Compose(settings Settings) *Root {
	logger := newLogger(settings.LogLevel)
	return &Root{
		Logger:      logger,
		Settings:    settings,
		HTTPHandler: httpadapter.Router{Logger: logger}.Handler(),
REPLACE_DEBUG_FIELD
	}
}

func ComposeFromEnv() *Root {
	return Compose(defaultSettings())
}

func defaultSettings() Settings {
	return Settings{
		HTTPAddr:  ":8080",
		PprofAddr: "127.0.0.1",
	}
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
"""
                .replace("REPLACE_DEBUG_IMPORT", debug_import)
                .replace("REPLACE_DEBUG_FIELD", debug_field),
            )
        return

    if opt.settings_mode == "config":
        _write(
            _svc(opt.root) / "bootstrap" / "compose.go",
            """package bootstrap

import (
	"os"

	"github.com/sirupsen/logrus"

	options "REPLACE_MODULE/internal/interface/options"
)

// Root is the single composition root for dependency injection.
type Root struct {
	Logger *logrus.Logger
	Settings   options.Settings
	SettingsStore options.Store
}

func Compose(settingsStore options.Store) *Root {
	settings := options.Settings{}
	if settingsStore != nil {
		settings = settingsStore.Get()
	}
	return &Root{
		Logger:       newLogger(settings.LogLevel),
		Settings:     settings,
		SettingsStore: settingsStore,
	}
}

func ComposeFromEnv() *Root {
	settingsStore := options.NewRepository(options.EnvLoader{})
	root := Compose(settingsStore)
	if err := settingsStore.LastError(); err != nil {
		root.Logger.WithError(err).Warn("options_load_failed")
	}
	return root
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
""",
        )
    elif opt.settings_mode == "env":
        _write(
            _svc(opt.root) / "bootstrap" / "compose.go",
            """package bootstrap

import (
	"os"

	"github.com/sirupsen/logrus"
)

const (
	envHTTPAddr  = "HTTP_ADDR"
	envPprofAddr = "PPROF_ADDR"
	envPprofPort = "PPROF_PORT"
	envLogLevel  = "LOG_LEVEL"
)

// Settings holds optional runtime configuration without a settings package.
type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

// Root is the single composition root for dependency injection.
type Root struct {
	Logger   *logrus.Logger
	Settings Settings
}

func Compose(settings Settings) *Root {
	return &Root{
		Logger:   newLogger(settings.LogLevel),
		Settings: settings,
	}
}

func ComposeFromEnv() *Root {
	return Compose(settingsFromEnv())
}

func settingsFromEnv() Settings {
	return Settings{
		HTTPAddr:  stringOr(envHTTPAddr, ":8080"),
		PprofAddr: stringOr(envPprofAddr, "127.0.0.1"),
		PprofPort: os.Getenv(envPprofPort),
		LogLevel:  os.Getenv(envLogLevel),
	}
}

func stringOr(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
""",
        )
    else:
        _write(
            _svc(opt.root) / "bootstrap" / "compose.go",
            """package bootstrap

import (
	"os"

	"github.com/sirupsen/logrus"
)

// Settings holds optional runtime configuration without env/config settings.
type Settings struct {
	HTTPAddr  string
	PprofAddr string
	PprofPort string
	LogLevel  string
}

// Root is the single composition root for dependency injection.
type Root struct {
	Logger   *logrus.Logger
	Settings Settings
}

func Compose(settings Settings) *Root {
	return &Root{
		Logger:   newLogger(settings.LogLevel),
		Settings: settings,
	}
}

func ComposeFromEnv() *Root {
	return Compose(defaultSettings())
}

func defaultSettings() Settings {
	return Settings{
		HTTPAddr:  ":8080",
		PprofAddr: "127.0.0.1",
	}
}

func newLogger(logLevel string) *logrus.Logger {
	l := logrus.New()
	l.SetOutput(os.Stdout)
	l.SetFormatter(&logrus.JSONFormatter{})
	if logLevel != "" {
		if parsed, err := logrus.ParseLevel(logLevel); err == nil {
			l.SetLevel(parsed)
		}
	}
	return l
}
""",
        )


def _write_http_debug_pprof(opt: Options) -> None:
    if opt.module is None:
        return
    _write(
        _svc(opt.root) / "interface" / "debughttp" / "pprof.go",
        """package debughttp

import (
	"net/http"
	"net/http/pprof"
)

type Options struct {
	Pprof bool
	Trace bool
}

func Handler(opt Options) http.Handler {
	mux := http.NewServeMux()
	if opt.Pprof {
		mux.HandleFunc("/debug/pprof/", pprof.Index)
		mux.HandleFunc("/debug/pprof/cmdline", pprof.Cmdline)
		mux.HandleFunc("/debug/pprof/profile", pprof.Profile)
		mux.HandleFunc("/debug/pprof/symbol", pprof.Symbol)
	}
	if opt.Trace {
		mux.HandleFunc("/debug/pprof/trace", pprof.Trace)
	}
	return mux
}
""",
    )


def _scaffold_http_nethttp(opt: Options) -> None:
    if opt.module is None:
        raise SystemExit("--module is required when scaffolding --kinds http (Go imports need a module path).")
    (opt.root / "cmd" / f"{opt.service}-api").mkdir(parents=True, exist_ok=True)
    (_svc(opt.root) / "interface" / "http").mkdir(parents=True, exist_ok=True)
    (_svc(opt.root) / "interface" / "http" / "middleware").mkdir(parents=True, exist_ok=True)
    if opt.http_pprof or opt.http_trace:
        (_svc(opt.root) / "interface" / "debughttp").mkdir(parents=True, exist_ok=True)
        _write_http_debug_pprof(opt)

    _write(
        _svc(opt.root) / "interface" / "http" / "router.go",
        """package http

import (
	"net/http"

	"github.com/sirupsen/logrus"

	"REPLACE_MODULE/internal/interface/http/middleware"
)

type Router struct {
	Logger logrus.FieldLogger
}

func (r Router) Handler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/health/live", func(w http.ResponseWriter, _ *http.Request) { w.WriteHeader(http.StatusOK) })
	mux.HandleFunc("/health/ready", func(w http.ResponseWriter, _ *http.Request) { w.WriteHeader(http.StatusOK) })
	return middleware.RequestLogger(r.Logger, mux)
}
""",
    )
    _write(
        _svc(opt.root) / "interface" / "http" / "middleware" / "logging.go",
        """package middleware

import (
	"net/http"
	"time"

	"github.com/sirupsen/logrus"
)

type statusCapturingResponseWriter struct {
	http.ResponseWriter
	status int
	bytes  int
}

func (w *statusCapturingResponseWriter) WriteHeader(statusCode int) {
	w.status = statusCode
	w.ResponseWriter.WriteHeader(statusCode)
}

func (w *statusCapturingResponseWriter) Write(p []byte) (int, error) {
	if w.status == 0 {
		w.status = http.StatusOK
	}
	n, err := w.ResponseWriter.Write(p)
	w.bytes += n
	return n, err
}

func RequestLogger(logger logrus.FieldLogger, next http.Handler) http.Handler {
	if logger == nil {
		logger = logrus.StandardLogger()
	}
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		cw := &statusCapturingResponseWriter{ResponseWriter: w}
		next.ServeHTTP(cw, r)
		logger.WithFields(logrus.Fields{
			"method":   r.Method,
			"path":     r.URL.Path,
			"status":   cw.status,
			"bytes":    cw.bytes,
			"duration": time.Since(start).String(),
		}).Info("http_request")
	})
}
""",
    )
    main_go = """package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"REPLACE_MODULE/internal/bootstrap"
)

func main() {
	root := bootstrap.ComposeFromEnv()
	logger := root.Logger
	addr := root.Settings.HTTPAddr
	srv := &http.Server{
		Addr:              addr,
		Handler:           root.HTTPHandler,
		ReadHeaderTimeout: 5 * time.Second,
	}

	go func() {
		logger.WithField("addr", addr).Info("http_listen")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Fatal("http_server_error")
		}
	}()

	<-shutdownSignal()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	_ = srv.Shutdown(ctx)
}

func shutdownSignal() <-chan os.Signal {
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	return ch
}
"""

    if opt.http_pprof or opt.http_trace:
        main_go = """package main

import (
	"context"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/sirupsen/logrus"

	"REPLACE_MODULE/internal/bootstrap"
)

func main() {
	root := bootstrap.ComposeFromEnv()
	logger := root.Logger
	addr := root.Settings.HTTPAddr
	srv := &http.Server{
		Addr:              addr,
		Handler:           root.HTTPHandler,
		ReadHeaderTimeout: 5 * time.Second,
	}

	debugSrv := debugServer(logger, root.Settings.PprofAddr, root.Settings.PprofPort, root.DebugHTTPHandler)

	go func() {
		logger.WithField("addr", addr).Info("http_listen")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Fatal("http_server_error")
		}
	}()

	<-shutdownSignal()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if debugSrv != nil {
		_ = debugSrv.Shutdown(ctx)
	}
	_ = srv.Shutdown(ctx)
}

func debugServer(logger *logrus.Logger, host string, port string, handler http.Handler) *http.Server {
	if handler == nil {
		return nil
	}
	if port == "" {
		return nil
	}
	if logger == nil {
		logger = logrus.StandardLogger()
	}
	addr := net.JoinHostPort(host, port)
	srv := &http.Server{
		Addr:              addr,
		Handler:           handler,
		ReadHeaderTimeout: 5 * time.Second,
	}
	go func() {
		logger.WithField("addr", addr).Info("debug_http_listen")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Error("debug_http_server_error")
		}
	}()
	return srv
}

func shutdownSignal() <-chan os.Signal {
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	return ch
}
"""

    _write(
        opt.root / "cmd" / f"{opt.service}-api" / "main.go",
        main_go,
    )
    _write_health_tests(opt)


def _scaffold_http_echo(opt: Options) -> None:
    if opt.module is None:
        raise SystemExit("--module is required when scaffolding --kinds http (Go imports need a module path).")
    (opt.root / "cmd" / f"{opt.service}-api").mkdir(parents=True, exist_ok=True)
    (_svc(opt.root) / "interface" / "http").mkdir(parents=True, exist_ok=True)
    if opt.http_pprof or opt.http_trace:
        (_svc(opt.root) / "interface" / "debughttp").mkdir(parents=True, exist_ok=True)
        _write_http_debug_pprof(opt)

    _write(
        _svc(opt.root) / "interface" / "http" / "server.go",
        """package http

import (
	"net/http"

	"github.com/labstack/echo/v4"
	echomw "github.com/labstack/echo/v4/middleware"
	"github.com/sirupsen/logrus"
)

func New(logger *logrus.Logger) *echo.Echo {
	e := echo.New()
	if logger == nil {
		logger = logrus.New()
	}
	e.HideBanner = true

	e.Use(echomw.RequestLoggerWithConfig(echomw.RequestLoggerConfig{
		LogStatus:   true,
		LogMethod:   true,
		LogURI:      true,
		LogLatency:  true,
		LogError:    true,
		LogValuesFunc: func(c echo.Context, v echomw.RequestLoggerValues) error {
			entry := logger.WithFields(logrus.Fields{
				"method":  v.Method,
				"uri":     v.URI,
				"status":  v.Status,
				"latency": v.Latency.String(),
			})
			if v.Error != nil {
				entry.WithError(v.Error).Error("http_request")
				return nil
			}
			entry.Info("http_request")
			return nil
		},
	}))

	e.GET("/health/live", func(c echo.Context) error {
		return c.NoContent(http.StatusOK)
	})
	e.GET("/health/ready", func(c echo.Context) error {
		return c.NoContent(http.StatusOK)
	})

	return e
}
""",
    )

    main_go = """package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"REPLACE_MODULE/internal/bootstrap"
)

func main() {
	root := bootstrap.ComposeFromEnv()
	logger := root.Logger
	addr := root.Settings.HTTPAddr
	e := root.HTTPServer

	go func() {
		logger.WithField("addr", addr).Info("http_listen")
		if err := e.Start(addr); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Fatal("http_server_error")
		}
	}()

	<-shutdownSignal()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	_ = e.Shutdown(ctx)
}

func shutdownSignal() <-chan os.Signal {
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	return ch
}
"""

    if opt.http_pprof or opt.http_trace:
        main_go = """package main

import (
	"context"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/sirupsen/logrus"

	"REPLACE_MODULE/internal/bootstrap"
)

func main() {
	root := bootstrap.ComposeFromEnv()
	logger := root.Logger
	addr := root.Settings.HTTPAddr
	e := root.HTTPServer

	debugSrv := debugServer(logger, root.Settings.PprofAddr, root.Settings.PprofPort, root.DebugHTTPHandler)

	go func() {
		logger.WithField("addr", addr).Info("http_listen")
		if err := e.Start(addr); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Fatal("http_server_error")
		}
	}()

	<-shutdownSignal()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if debugSrv != nil {
		_ = debugSrv.Shutdown(ctx)
	}
	_ = e.Shutdown(ctx)
}

func debugServer(logger *logrus.Logger, host string, port string, handler http.Handler) *http.Server {
	if handler == nil {
		return nil
	}
	if port == "" {
		return nil
	}
	if logger == nil {
		logger = logrus.StandardLogger()
	}
	addr := net.JoinHostPort(host, port)
	srv := &http.Server{
		Addr:              addr,
		Handler:           handler,
		ReadHeaderTimeout: 5 * time.Second,
	}
	go func() {
		logger.WithField("addr", addr).Info("debug_http_listen")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Error("debug_http_server_error")
		}
	}()
	return srv
}

func shutdownSignal() <-chan os.Signal {
	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGINT, syscall.SIGTERM)
	return ch
}
"""

    _write(
        opt.root / "cmd" / f"{opt.service}-api" / "main.go",
        main_go,
    )
    _write_health_tests(opt)


def _write_health_tests(opt: Options) -> None:
    if opt.module is None:
        return
    _write(
        opt.root / "test" / "health_test.go",
        """package test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"REPLACE_MODULE/internal/bootstrap"
)

func TestHealthLive(t *testing.T) {
	t.Parallel()
	root := bootstrap.ComposeFromEnv()
	if root.HTTPHandler == nil {
		t.Fatal("root.HTTPHandler is nil")
	}

	req := httptest.NewRequest(http.MethodGet, "/health/live", nil)
	rec := httptest.NewRecorder()
	root.HTTPHandler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("expected %d, got %d", http.StatusOK, rec.Code)
	}
}

func TestHealthReady(t *testing.T) {
	t.Parallel()
	root := bootstrap.ComposeFromEnv()
	if root.HTTPHandler == nil {
		t.Fatal("root.HTTPHandler is nil")
	}

	req := httptest.NewRequest(http.MethodGet, "/health/ready", nil)
	rec := httptest.NewRecorder()
	root.HTTPHandler.ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("expected %d, got %d", http.StatusOK, rec.Code)
	}
}
""",
    )


def _scaffold_placeholder(opt: Options, kind: str) -> None:
    (opt.root / "cmd" / f"{opt.service}-{kind}").mkdir(parents=True, exist_ok=True)
    (_svc(opt.root) / "interface" / kind).mkdir(parents=True, exist_ok=True)
    _write(
        opt.root / "cmd" / f"{opt.service}-{kind}" / "main.go",
        f"""package main

import "REPLACE_MODULE/internal/bootstrap"

func main() {{
	logger := bootstrap.ComposeFromEnv().Logger
	logger.WithField("binary", "{opt.service}-{kind}").Info("todo_implement")
}}
""",
    )


def _replace_module_placeholders(root: Path, module: str | None) -> None:
    if module is None:
        return
    for path in root.rglob("*.go"):
        text = path.read_text(encoding="utf-8")
        if "REPLACE_MODULE" not in text:
            continue
        path.write_text(text.replace("REPLACE_MODULE", module), encoding="utf-8")


def parse_args() -> Options:
    parser = argparse.ArgumentParser(description="Scaffold a Go service repo using hexagonal layout.")
    parser.add_argument("--root", required=True, help="Target repo directory (created if missing).")
    parser.add_argument(
        "--module",
        help="Go module path (writes go.mod if missing; replaces imports). If omitted for a new project, defaults to the root folder name.",
    )
    parser.add_argument("--service", required=True, help="Service name (e.g., billing, payments).")
    parser.add_argument(
        "--kinds",
        default="http",
        help="Comma-separated binaries to scaffold: http,grpc,worker,cli (default: http).",
    )
    parser.add_argument(
        "--http-framework",
        default="echo",
        choices=["nethttp", "echo"],
        help="HTTP framework for --kinds http: echo (default) or nethttp.",
    )
    parser.add_argument(
        "--http-pprof",
        action="store_true",
        help="Include HTTP debug handlers for pprof on /debug/pprof/* (opt-in; only for --kinds http).",
    )
    parser.add_argument(
        "--http-trace",
        action="store_true",
        help="Include HTTP debug handler for trace on /debug/pprof/trace (opt-in; only for --kinds http).",
    )
    parser.add_argument(
        "--settings",
        choices=["none", "env", "config"],
        default="env",
        help="Settings mode: none (no env/config), env (env only), config (env + optional config file via Koanf; env overrides config).",
    )
    parser.add_argument(
        "--with-settings",
        action="store_true",
        help="Deprecated: use --settings=config instead.",
    )
    parser.add_argument(
        "--skip-deps",
        action="store_true",
        help="Skip dependency install (do not run `go mod tidy` even if go.mod is created).",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    kinds = tuple(k.strip() for k in args.kinds.split(",") if k.strip())
    settings_mode = args.settings
    if args.with_settings:
        if settings_mode != "env":
            raise SystemExit("Use either --with-settings or --settings; not both.")
        settings_mode = "config"

    return Options(
        root=root,
        module=args.module,
        service=args.service,
        kinds=kinds,
        http_framework=args.http_framework,
        http_pprof=args.http_pprof,
        http_trace=args.http_trace,
        settings_mode=settings_mode,
        skip_deps=args.skip_deps,
    )


def main() -> None:
    opt = parse_args()
    if opt.module is None:
        opt.module = _discover_module_from_go_mod(opt.root)
    if opt.module is None and not (opt.root / "go.mod").exists():
        # Default to local module path based on folder name (avoid assuming github.com-style paths).
        opt.module = opt.root.name

    go_mod_created = _maybe_write_go_mod(opt.root, opt.module)
    _base_tree(opt)

    for kind in opt.kinds:
        if kind == "http":
            if opt.http_framework == "nethttp":
                _scaffold_http_nethttp(opt)
            elif opt.http_framework == "echo":
                _scaffold_http_echo(opt)
            else:
                raise SystemExit(f"Unsupported http framework: {opt.http_framework}")
        elif kind in {"grpc", "worker", "cli"}:
            _scaffold_placeholder(opt, kind)
        else:
            raise SystemExit(f"Unsupported kind: {kind} (supported: http, grpc, worker, cli)")

    _replace_module_placeholders(opt.root, opt.module)
    if go_mod_created and not opt.skip_deps:
        print("📦 Installing dependencies (go mod tidy)...")
        _install_deps_for_new_project(opt.root)


if __name__ == "__main__":
    main()
