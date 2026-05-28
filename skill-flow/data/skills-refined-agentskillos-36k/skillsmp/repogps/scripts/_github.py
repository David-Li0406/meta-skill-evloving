#!/usr/bin/env python3
"""
Shared utilities for RepoGPS scripts.

- Supports GitHub repos (public without auth, private with GITHUB_TOKEN)
- Supports local directories
- Provides shared file selection heuristics.
- Includes logging and progress reporting.
"""

from __future__ import annotations

import os
import re
import sys
import time
import json
import pathlib
import logging
import shutil
import concurrent.futures
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any, Union

import requests

GITHUB_API = "https://api.github.com"

# File extensions to treat as text (for local scanning)
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".rs", ".go", ".java", ".kt", ".scala",
    ".c", ".cpp", ".h", ".hpp", ".cs", ".rb", ".php", ".swift", ".m", ".mm",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd",
    ".json", ".yaml", ".yml", ".toml", ".xml", ".ini", ".cfg", ".conf",
    ".md", ".rst", ".txt", ".html", ".css", ".scss", ".less",
    ".sql", ".graphql", ".proto", ".thrift",
    ".dockerfile", ".gitignore", ".env", ".editorconfig",
    "Makefile", "Dockerfile", "Gemfile", "Rakefile", "Procfile",
}

# Directories to skip when scanning locally
SKIP_DIRS = {
    ".git", ".svn", ".hg", ".bzr",
    "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache",
    "venv", ".venv", "env", ".env", "virtualenv",
    ".tox", ".nox", ".eggs", "*.egg-info",
    "dist", "build", "target", "out", "bin", "obj",
    ".idea", ".vscode", ".vs",
    "coverage", ".coverage", "htmlcov",
    ".next", ".nuxt", ".output",
}

# Configure logging
logger = logging.getLogger("repogps")


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    )
    logger.setLevel(level)
    logger.handlers = [handler]


@dataclass
class RepoRef:
    """Reference to a GitHub repository."""
    owner: str
    repo: str


@dataclass
class LocalRef:
    """Reference to a local directory."""
    path: pathlib.Path
    name: str  # Directory name, used for cache naming


@dataclass
class DownloadResult:
    """Result of a file download attempt."""

    path: str
    success: bool
    saved_as: Optional[str] = None
    error: Optional[str] = None


class ProgressReporter:
    """Simple progress reporter for long-running operations."""

    def __init__(self, total: int, prefix: str = ""):
        self.total = total
        self.current = 0
        self.prefix = prefix
        self.start_time = time.time()

    def update(self, increment: int = 1, message: str = "") -> None:
        self.current += increment
        elapsed = time.time() - self.start_time
        pct = (self.current / self.total * 100) if self.total > 0 else 100

        if message:
            print(f"  [{self.current}/{self.total}] {message}")
        else:
            print(
                f"  {self.prefix} {self.current}/{self.total} ({pct:.0f}%) - {elapsed:.1f}s",
                end="\r",
            )

    def finish(self) -> None:
        elapsed = time.time() - self.start_time
        print(
            f"  {self.prefix} {self.current}/{self.total} completed in {elapsed:.1f}s"
        )


def parse_github_url(repo_url: str) -> RepoRef:
    """
    Accepts:
      - https://github.com/<owner>/<repo>
      - https://github.com/<owner>/<repo>/
      - git@github.com:<owner>/<repo>.git
      - https://github.com/<owner>/<repo>.git
    """
    repo_url = repo_url.strip()

    # SSH
    m = re.match(r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$", repo_url)
    if m:
        return RepoRef(owner=m.group(1), repo=m.group(2))

    # HTTPS
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", repo_url)
    if m:
        return RepoRef(owner=m.group(1), repo=m.group(2))

    raise ValueError(f"Unrecognized GitHub repo URL: {repo_url}")


# =============================================================================
# LOCAL DIRECTORY SUPPORT
# =============================================================================


def is_local_path(input_str: str) -> bool:
    """Check if input is a local path (vs a GitHub URL)."""
    input_str = input_str.strip()

    # Obvious URL patterns
    if input_str.startswith(("http://", "https://", "git@")):
        return False

    # Check if it looks like a path
    p = pathlib.Path(input_str).expanduser()
    return p.exists() and p.is_dir()


def parse_local_path(input_str: str) -> LocalRef:
    """Parse a local directory path into a LocalRef."""
    p = pathlib.Path(input_str).expanduser().resolve()

    if not p.exists():
        raise ValueError(f"Directory does not exist: {p}")
    if not p.is_dir():
        raise ValueError(f"Path is not a directory: {p}")

    return LocalRef(path=p, name=p.name)


def get_local_tree(local_ref: LocalRef) -> Tuple[List[str], bool]:
    """
    Get list of file paths from a local directory.
    Returns tuple of (list of relative paths, truncated flag).
    """
    paths = []
    root = local_ref.path

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip ignored directories (modify in place to prevent descent)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]

        for filename in filenames:
            # Skip hidden files
            if filename.startswith(".") and filename not in {".env.example", ".gitignore", ".editorconfig"}:
                continue

            full_path = pathlib.Path(dirpath) / filename
            rel_path = full_path.relative_to(root)
            paths.append(str(rel_path))

    # Sort for consistency
    paths.sort()

    # Truncate if too large (same limit as GitHub API)
    truncated = len(paths) > 100_000
    if truncated:
        paths = paths[:100_000]
        logger.warning("Directory has >100k files. Tree is truncated.")

    return paths, truncated


def read_local_file(local_ref: LocalRef, rel_path: str, max_chars: int = 120_000) -> str:
    """
    Read a text file from the local directory.
    Truncates to max_chars for safety.
    """
    full_path = local_ref.path / rel_path

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {rel_path}")
    if not full_path.is_file():
        raise ValueError(f"Path is not a file: {rel_path}")

    # Check if file is likely text
    ext = full_path.suffix.lower()
    basename = full_path.name

    is_text = (
        ext in TEXT_EXTENSIONS or
        basename in TEXT_EXTENSIONS or
        ext in {".lock"} or  # Lock files are often text
        basename.startswith(".")  # Dotfiles
    )

    if not is_text:
        # Try to detect binary
        try:
            with open(full_path, "rb") as f:
                chunk = f.read(1024)
                if b"\x00" in chunk:
                    raise ValueError(f"Skipping binary file: {rel_path}")
        except Exception:
            pass

    try:
        text = full_path.read_text(encoding="utf-8", errors="ignore")
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n<<TRUNCATED>>\n"
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to read {rel_path}: {e}")


def copy_local_files(
    local_ref: LocalRef,
    paths: List[str],
    output_dir: pathlib.Path,
    max_chars: int = 120_000,
    show_progress: bool = True,
) -> List[DownloadResult]:
    """
    Copy/read files from local directory to cache.
    Returns list of DownloadResult objects.
    """
    results: List[DownloadResult] = []

    for path in paths:
        try:
            text = read_local_file(local_ref, path, max_chars=max_chars)
            out_path = output_dir / f"{slugify_path(path)}.txt"
            safe_write_text(out_path, text)
            results.append(DownloadResult(path=path, success=True, saved_as=str(out_path.name)))
            print(f"  ✓ {path}")
        except Exception as e:
            results.append(DownloadResult(path=path, success=False, error=str(e)))
            print(f"  ✗ {path} ({e})")

    return results


def github_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "RepoGPS/1.0",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _request_with_backoff(
    url: str, params: Optional[dict] = None, timeout: int = 30
) -> requests.Response:
    """
    Handles GitHub rate limits and transient errors with basic backoff.
    """
    for attempt in range(6):
        try:
            r = requests.get(
                url, headers=github_headers(), params=params, timeout=timeout
            )
        except requests.exceptions.RequestException as e:
            logger.debug(f"Request failed (attempt {attempt+1}): {e}")
            if attempt < 5:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise

        # Rate limit handling
        if r.status_code == 403:
            remaining = r.headers.get("X-RateLimit-Remaining")
            reset = r.headers.get("X-RateLimit-Reset")
            if remaining == "0" and reset:
                wait_s = max(0, int(reset) - int(time.time()) + 1)
                wait_s = min(wait_s, 60)
                logger.warning(f"Rate limited. Waiting {wait_s}s...")
                time.sleep(wait_s)
                continue
            # Check if it's a permission error
            if "rate limit" not in r.text.lower():
                raise RuntimeError(
                    f"Permission denied (403). Is this a private repo? Set GITHUB_TOKEN env var."
                )

        # Retry transient errors
        if r.status_code in (429, 500, 502, 503, 504):
            logger.debug(f"Transient error {r.status_code}, retrying...")
            time.sleep(1.5 * (attempt + 1))
            continue

        return r

    return r


def get_default_branch(ref: RepoRef) -> str:
    url = f"{GITHUB_API}/repos/{ref.owner}/{ref.repo}"
    r = _request_with_backoff(url)
    r.raise_for_status()
    return r.json().get("default_branch", "main")


def get_branch_head_sha(ref: RepoRef, branch: str) -> str:
    url = f"{GITHUB_API}/repos/{ref.owner}/{ref.repo}/branches/{branch}"
    r = _request_with_backoff(url)
    r.raise_for_status()
    return r.json()["commit"]["sha"]


def get_repo_tree(ref: RepoRef, branch: str) -> Tuple[List[str], bool]:
    """
    Returns tuple of (list of blob paths, truncated flag).
    GitHub API truncates at ~100k items.
    """
    sha = get_branch_head_sha(ref, branch)
    url = f"{GITHUB_API}/repos/{ref.owner}/{ref.repo}/git/trees/{sha}"
    r = _request_with_backoff(url, params={"recursive": "1"})
    r.raise_for_status()

    data = r.json()
    tree = data.get("tree", [])
    truncated = data.get("truncated", False)

    if truncated:
        logger.warning("Repository has >100k files. Tree is truncated.")

    paths = [x["path"] for x in tree if x.get("type") == "blob"]
    return paths, truncated


def raw_file_url(ref: RepoRef, branch: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{ref.owner}/{ref.repo}/{branch}/{path}"


def fetch_text_file(
    ref: RepoRef, branch: str, path: str, max_chars: int = 120_000
) -> str:
    """
    Fetch a text file from GitHub raw content.
    Truncates to max_chars for safety.
    """
    url = raw_file_url(ref, branch, path)
    r = requests.get(url, headers={"User-Agent": "RepoGPS/1.0"}, timeout=30)
    if r.status_code == 404:
        raise FileNotFoundError(f"File not found: {path}")
    if r.status_code != 200:
        raise RuntimeError(f"Failed to fetch {path} (HTTP {r.status_code})")

    text = r.text
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n<<TRUNCATED>>\n"
    return text


def fetch_files_parallel(
    ref: RepoRef,
    branch: str,
    paths: List[str],
    output_dir: pathlib.Path,
    max_chars: int = 120_000,
    max_workers: int = 8,
    show_progress: bool = True,
) -> List[DownloadResult]:
    """
    Download multiple files in parallel.
    Returns list of DownloadResult objects.
    """
    results: List[DownloadResult] = []

    def download_one(path: str) -> DownloadResult:
        try:
            text = fetch_text_file(ref, branch, path, max_chars=max_chars)
            out_path = output_dir / f"{slugify_path(path)}.txt"
            safe_write_text(out_path, text)
            return DownloadResult(path=path, success=True, saved_as=str(out_path.name))
        except Exception as e:
            return DownloadResult(path=path, success=False, error=str(e))

    progress = ProgressReporter(len(paths), "Downloading") if show_progress else None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_one, p): p for p in paths}

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)

            if result.success:
                print(f"  ✓ {result.path}")
            else:
                print(f"  ✗ {result.path} ({result.error})")

    return results


def safe_write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", errors="ignore")


def safe_write_json(path: pathlib.Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def slugify_path(p: str) -> str:
    """For saving files under a flat folder."""
    return p.replace("/", "__")


# =============================================================================
# SHARED FILE SELECTION HEURISTICS
# =============================================================================


def pick_key_files(paths: List[str]) -> Dict[str, List[str]]:
    """
    Heuristic selection of key files that matter for onboarding.
    Returns groups -> list(paths)

    Supports: Python, JavaScript/TypeScript, Rust, Go, Java, C#, Ruby, PHP
    """
    paths_set = set(paths)

    def exists(p: str) -> bool:
        return p in paths_set

    # README / docs
    docs = []
    for cand in [
        "README.md",
        "README",
        "README.rst",
        "docs/README.md",
        "docs/index.md",
        "doc/README.md",
    ]:
        if exists(cand):
            docs.append(cand)

    # Build manifests - check root level first
    manifests = []
    root_manifest_names = [
        # Python
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        # JavaScript/TypeScript
        "package.json",
        "tsconfig.json",
        # Rust
        "Cargo.toml",
        # Go
        "go.mod",
        # Java/Kotlin
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "settings.gradle",
        # C#/.NET
        "*.csproj",
        "*.sln",
        "Directory.Build.props",
        # Ruby
        "Gemfile",
        "*.gemspec",
        # PHP
        "composer.json",
        # General
        "Makefile",
        "CMakeLists.txt",
        "docker-compose.yml",
        "Dockerfile",
        ".env.example",
    ]

    for cand in root_manifest_names:
        if "*" in cand:
            # Pattern match
            pattern = cand.replace("*", "")
            for p in paths:
                if "/" not in p and p.endswith(pattern):
                    manifests.append(p)
        elif exists(cand):
            manifests.append(cand)

    # Also find manifests in subdirectories (for monorepos)
    manifest_basenames = {
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "Pipfile",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Makefile",
        "Gemfile",
        "composer.json",
    }
    for p in paths:
        basename = p.split("/")[-1]
        if basename in manifest_basenames and p not in manifests:
            # Prioritize shallow paths (depth <= 2)
            if p.count("/") <= 2:
                manifests.append(p)

    # CI / workflows - support multiple platforms
    ci = []
    for p in paths:
        # GitHub Actions
        if p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml")):
            ci.append(p)
        # GitLab CI
        if p == ".gitlab-ci.yml" or p.endswith("/.gitlab-ci.yml"):
            ci.append(p)
        # CircleCI
        if p == ".circleci/config.yml" or p.endswith("/.circleci/config.yml"):
            ci.append(p)
        # Travis CI
        if p == ".travis.yml":
            ci.append(p)
        # Azure Pipelines
        if p == "azure-pipelines.yml" or p.startswith(".azure-pipelines/"):
            ci.append(p)
        # Jenkins
        if p == "Jenkinsfile" or p.endswith("/Jenkinsfile"):
            ci.append(p)

    # Common entrypoints - check exact paths first
    entrypoints = []
    entrypoint_exact = {
        # Python
        "main.py",
        "__main__.py",
        "app.py",
        "server.py",
        "manage.py",
        "wsgi.py",
        "asgi.py",
        "src/main.py",
        "src/__main__.py",
        "src/app.py",
        "src/server.py",
        # JavaScript/TypeScript
        "src/index.ts",
        "src/main.ts",
        "src/server.ts",
        "src/app.ts",
        "index.ts",
        "index.js",
        "main.ts",
        "main.js",
        "server.ts",
        "server.js",
        "src/index.js",
        "src/main.js",
        "src/server.js",
        "src/app.js",
        # Rust
        "src/main.rs",
        "src/lib.rs",
        # Go
        "main.go",
        "cmd/main.go",
        # Java
        "src/main/java/Main.java",
        "src/Main.java",
        # C#
        "Program.cs",
        "Startup.cs",
        "src/Program.cs",
        # Ruby
        "config.ru",
        "app.rb",
        "main.rb",
        "Rakefile",
        # PHP
        "index.php",
        "artisan",
        "public/index.php",
    }
    for p in paths:
        if p in entrypoint_exact:
            entrypoints.append(p)

    # Also find entrypoints by basename pattern in subdirectories
    entrypoint_basenames = {
        # Python
        "main.py",
        "__main__.py",
        "app.py",
        "server.py",
        "wsgi.py",
        "asgi.py",
        # Rust
        "main.rs",
        "lib.rs",
        # Go
        "main.go",
        # JavaScript/TypeScript
        "index.ts",
        "index.js",
        "main.ts",
        "main.js",
        "server.ts",
        "server.js",
        # Java
        "Main.java",
        "Application.java",
        "App.java",
        # C#
        "Program.cs",
        "Startup.cs",
        # Ruby
        "config.ru",
        "application.rb",
        # PHP
        "index.php",
    }
    for p in paths:
        basename = p.split("/")[-1]
        if basename in entrypoint_basenames and p not in entrypoints:
            entrypoints.append(p)

    # Tests
    tests = []
    for p in paths:
        lower_p = p.lower()
        if (
            p.startswith("tests/")
            or "/tests/" in p
            or p.startswith("__tests__/")
            or p.startswith("test/")
            or "/test/" in p
            or p.startswith("spec/")
            or "/spec/" in p
            or "_test.go" in p
            or "_test.rs" in p
            or "test_" in basename
            or "_test." in basename
            or ".test." in basename
            or ".spec." in basename
        ):
            tests.append(p)
    tests = sorted(tests)[:15]

    # Config candidates (but not manifests we already captured)
    config = []
    for p in paths:
        if p in manifests:
            continue
        lower_p = p.lower()
        if (
            p.startswith("config/")
            or p.startswith("configs/")
            or p.startswith(".config/")
            or p.startswith("settings/")
            or p.endswith((".yaml", ".yml", ".ini", ".cfg", ".conf"))
        ):
            if any(p.endswith(suf) for suf in [".lock", "-lock.json", "-lock.yaml"]):
                continue
            if len(config) < 10:
                config.append(p)

    return {
        "docs": sorted(set(docs)),
        "manifests": sorted(set(manifests))[:15],
        "ci": sorted(set(ci))[:10],
        "entrypoints": sorted(set(entrypoints))[:20],
        "tests_sample": tests,
        "config_sample": sorted(set(config))[:10],
    }


# =============================================================================
# ENTRYPOINT SCORING PATTERNS
# =============================================================================

ENTRYPOINT_PATTERNS: List[Tuple[str, float]] = [
    # Python - higher score for root/src, still match anywhere
    (r"^main\.py$", 0.92),
    (r"^src/main\.py$", 0.90),
    (r"(^|/)main\.py$", 0.82),
    (r"(^|/)__main__\.py$", 0.85),
    (r"(^|/)(app|server|wsgi|asgi)\.py$", 0.75),
    (r"(^|/)manage\.py$", 0.70),  # Django
    # TypeScript/JavaScript
    (r"^src/(main|index|server|app)\.(ts|js)$", 0.88),
    (r"(^|/)(main|index|server|app)\.(ts|js)$", 0.78),
    (r"(^|/)index\.(ts|js)$", 0.72),
    # Rust - match main.rs anywhere
    (r"^src/main\.rs$", 0.92),
    (r"(^|/)main\.rs$", 0.85),
    (r"(^|/)lib\.rs$", 0.70),
    # Go
    (r"^main\.go$", 0.92),
    (r"^cmd/[^/]+/main\.go$", 0.88),
    (r"(^|/)main\.go$", 0.82),
    # Java
    (r"(^|/)Main\.java$", 0.85),
    (r"(^|/)Application\.java$", 0.82),
    (r"(^|/)App\.java$", 0.78),
    # C# / .NET
    (r"(^|/)Program\.cs$", 0.88),
    (r"(^|/)Startup\.cs$", 0.82),
    # Ruby
    (r"^config\.ru$", 0.85),
    (r"(^|/)application\.rb$", 0.78),
    (r"(^|/)app\.rb$", 0.75),
    # PHP
    (r"^public/index\.php$", 0.85),
    (r"^index\.php$", 0.82),
    (r"(^|/)artisan$", 0.80),  # Laravel
]

CONTENT_HINTS: List[Tuple[str, float]] = [
    # Python
    (r'if __name__ == [\'"]__main__[\'"]', 0.15),
    (r"FastAPI\(", 0.12),
    (r"Flask\(__name__\)", 0.12),
    (r"Django", 0.08),
    (r"uvicorn\.run", 0.12),
    (r"argparse|click\.command|typer\.Typer", 0.08),
    # Node.js
    (r"app\.listen\(", 0.12),
    (r"express\(\)", 0.12),
    (r"createServer\(", 0.10),
    (r"Fastify\(", 0.10),
    # Rust
    (r"fn main\(\)", 0.18),
    (r"#\[tokio::main\]", 0.15),
    (r"actix_web::", 0.10),
    # Go
    (r"func main\(\)", 0.18),
    (r"gin\.Default\(\)", 0.10),
    (r"http\.ListenAndServe", 0.12),
    # Java
    (r"public static void main\(", 0.18),
    (r"@SpringBootApplication", 0.15),
    # C#
    (r"static void Main\(", 0.18),
    (r"WebApplication\.CreateBuilder", 0.15),
    (r"\[ApiController\]", 0.10),
    # Ruby
    (r"Rails\.application", 0.12),
    (r"Sinatra::", 0.10),
    # PHP
    (r"Illuminate\\", 0.10),  # Laravel
    (r"Symfony\\", 0.10),
    # General
    (r"grpc\.", 0.08),
    (r"\.serve\(", 0.08),
]


def score_entrypoint_path(path: str) -> float:
    """Score a file path as a potential entrypoint."""
    best = 0.0
    for pat, base in ENTRYPOINT_PATTERNS:
        if re.search(pat, path):
            best = max(best, base)
    return best


def score_entrypoint_content(text: str) -> float:
    """Score file content for entrypoint hints."""
    bonus = 0.0
    for pat, b in CONTENT_HINTS:
        if re.search(pat, text):
            bonus += b
    return min(bonus, 0.35)


# =============================================================================
# CI PLATFORM DETECTION
# =============================================================================


def extract_ci_commands(text: str, filename: str) -> Tuple[List[str], List[str]]:
    """
    Extract run and test commands from CI configuration files.
    Supports: GitHub Actions, GitLab CI, CircleCI, Travis CI

    Returns: (run_commands, test_commands)
    """
    run_cmds: List[str] = []
    test_cmds: List[str] = []

    # Keywords for classification
    test_keywords = [
        "pytest",
        "cargo test",
        "go test",
        "npm test",
        "pnpm test",
        "yarn test",
        "jest",
        "vitest",
        "rspec",
        "phpunit",
        "dotnet test",
        "mvn test",
        "gradle test",
        "make test",
        "make check",
    ]
    run_keywords = [
        "cargo run",
        "npm run",
        "pnpm run",
        "yarn run",
        "python ",
        "go run",
        "dotnet run",
        "node ",
        "ruby ",
        "php ",
    ]

    def classify_command(cmd: str) -> None:
        cmd = cmd.strip().strip('"').strip("'")
        if not cmd or cmd.startswith("#"):
            return

        lower_cmd = cmd.lower()
        if any(k in lower_cmd for k in test_keywords):
            test_cmds.append(cmd)
        elif any(k in lower_cmd for k in run_keywords):
            run_cmds.append(cmd)

    if "workflows" in filename or filename.endswith((".yml", ".yaml")):
        # GitHub Actions: "- run: command" or "run: command"
        for m in re.finditer(r"^\s*-?\s*run:\s*[|>]?\s*(.+?)$", text, re.MULTILINE):
            classify_command(m.group(1))

        # Multi-line run blocks
        for m in re.finditer(r"-?\s*run:\s*\|\s*\n((?:\s+.+\n)+)", text):
            for line in m.group(1).strip().split("\n"):
                classify_command(line.strip())

    if ".gitlab-ci" in filename:
        # GitLab CI: "script:" sections
        for m in re.finditer(r"script:\s*\n((?:\s+-\s*.+\n)+)", text):
            for line in m.group(1).strip().split("\n"):
                line = line.strip().lstrip("-").strip()
                classify_command(line)

    if "circleci" in filename or ".circleci" in filename:
        # CircleCI: "command:" or "run:" sections
        for m in re.finditer(r"(?:command|run):\s*(.+?)$", text, re.MULTILINE):
            classify_command(m.group(1))

    if ".travis" in filename:
        # Travis CI: "script:" array
        for m in re.finditer(r"script:\s*\n((?:\s+-\s*.+\n)+)", text):
            for line in m.group(1).strip().split("\n"):
                line = line.strip().lstrip("-").strip()
                classify_command(line)

    return run_cmds, test_cmds


# =============================================================================
# COMMAND EXTRACTION UTILITIES (shared by repogps.py and extract_runbook.py)
# =============================================================================


def load_downloaded_text(cache_dir: pathlib.Path, original_path: str) -> Optional[str]:
    """Load downloaded file content by original path."""
    slug = original_path.replace("/", "__") + ".txt"
    p = cache_dir / "downloaded" / slug
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8", errors="ignore")


def load_key_files(cache_dir: pathlib.Path) -> Dict[str, List[str]]:
    """Load key_files.json from cache directory."""
    p = cache_dir / "key_files.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def dedupe(xs: List[str]) -> List[str]:
    """Remove duplicates while preserving order."""
    out = []
    seen = set()
    for x in xs:
        x = x.strip()
        if not x or x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def extract_commands_from_readme(text: str) -> Tuple[List[str], List[str]]:
    """Extract run and test commands from README content."""
    run_cmds: List[str] = []
    test_cmds: List[str] = []

    test_keywords = [
        "pytest",
        "npm test",
        "pnpm test",
        "yarn test",
        "cargo test",
        "go test",
        "make test",
        "make check",
        "dotnet test",
        "mvn test",
        "gradle test",
        "rspec",
        "phpunit",
        "bundle exec",
    ]
    run_keywords = [
        "run",
        "start",
        "dev",
        "serve",
        "uvicorn",
        "python ",
        "npm ",
        "pnpm ",
        "yarn ",
        "cargo run",
        "go run",
        "node ",
        "dotnet run",
        "ruby ",
        "php ",
        "rails s",
        "bundle exec",
    ]

    # Pull fenced code blocks
    blocks = re.findall(
        r"```(?:bash|sh|shell|zsh|console|)\s*([\s\S]*?)```", text, flags=re.IGNORECASE
    )
    for b in blocks:
        lines = [
            ln.strip().lstrip("$").strip()
            for ln in b.splitlines()
            if ln.strip() and not ln.strip().startswith("#")
        ]
        for ln in lines:
            if any(k in ln.lower() for k in test_keywords):
                test_cmds.append(ln)
            elif any(k in ln.lower() for k in run_keywords):
                run_cmds.append(ln)

    return dedupe(run_cmds), dedupe(test_cmds)


def extract_from_package_json(text: str) -> Tuple[List[str], List[str]]:
    """Extract npm scripts from package.json."""
    run_cmds: List[str] = []
    test_cmds: List[str] = []

    try:
        obj = json.loads(text)
    except Exception:
        return [], []

    scripts = obj.get("scripts", {}) or {}
    for name, cmd in scripts.items():
        if not isinstance(cmd, str):
            continue
        full = f"npm run {name}"
        lower_name = name.lower()

        # Test scripts
        if any(k in lower_name for k in ["test", "spec", "e2e", "unit", "integration"]):
            test_cmds.append(full)
        elif any(k in cmd.lower() for k in ["jest", "vitest", "mocha", "ava"]):
            test_cmds.append(full)

        # Run scripts
        if name in ("start", "dev", "serve", "build", "preview"):
            run_cmds.append(full)
        elif "node " in cmd or "ts-node" in cmd:
            run_cmds.append(full)

    return dedupe(run_cmds), dedupe(test_cmds)


def extract_from_makefile(text: str) -> Tuple[List[str], List[str]]:
    """Extract make targets from Makefile."""
    run_cmds: List[str] = []
    test_cmds: List[str] = []

    targets = re.findall(r"^([a-zA-Z0-9_.-]+)\s*:\s*(?:.*)$", text, flags=re.MULTILINE)
    for t in targets:
        lower_t = t.lower()
        if t in ("run", "start", "dev", "serve", "build", "all", "default"):
            run_cmds.append(f"make {t}")
        if "test" in lower_t or t in ("check", "ci", "lint", "verify"):
            test_cmds.append(f"make {t}")

    return dedupe(run_cmds), dedupe(test_cmds)


def detect_languages(manifests: set, entrypoints: set) -> set:
    """Detect programming languages from manifests and entrypoints."""
    langs = set()

    # From manifests
    manifest_patterns = {
        "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
        "javascript": ["package.json"],
        "typescript": ["tsconfig.json"],
        "rust": ["Cargo.toml"],
        "go": ["go.mod"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "csharp": [".csproj", ".sln"],
        "ruby": ["Gemfile", ".gemspec"],
        "php": ["composer.json"],
    }

    for lang, patterns in manifest_patterns.items():
        for m in manifests:
            if any(m.endswith(p) for p in patterns):
                langs.add(lang)

    # From entrypoints
    ext_patterns = {
        ".py": "python",
        ".rs": "rust",
        ".go": "go",
        ".ts": "typescript",
        ".js": "javascript",
        ".java": "java",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
    }

    for e in entrypoints:
        for ext, lang in ext_patterns.items():
            if e.endswith(ext):
                langs.add(lang)

    return langs
