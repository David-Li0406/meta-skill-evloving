param(
  [switch]$Quiet
)

$ErrorActionPreference = "Stop"

function Fail([string]$Message, [int]$Code = 1) {
  if (-not $Quiet) {
    Write-Error $Message
  }
  exit $Code
}

function Ok([string]$Message) {
  if (-not $Quiet) {
    Write-Host $Message
  }
}

try {
  $null = Get-Command git -ErrorAction Stop
} catch {
  Fail "Missing prerequisite: git is not available on PATH."
}

try {
  $null = Get-Command gh -ErrorAction Stop
} catch {
  Fail "Missing prerequisite: gh (GitHub CLI) is not available on PATH. Install from https://cli.github.com/."
}

try {
  git rev-parse --is-inside-work-tree *> $null
} catch {
  Fail "Not in a git repository. Run this from within the repo root (or any subdirectory)."
}

try {
  $origin = git remote get-url origin 2>$null
  if (-not $origin) {
    Fail "Missing remote: origin. This skill expects an 'origin' remote."
  }
} catch {
  Fail "Missing remote: origin. This skill expects an 'origin' remote."
}

try {
  gh auth status *> $null
} catch {
  Fail "GitHub CLI is not authenticated. Run: gh auth login"
}

Ok "OK: prerequisites satisfied (git, gh, authenticated, origin remote present)."
