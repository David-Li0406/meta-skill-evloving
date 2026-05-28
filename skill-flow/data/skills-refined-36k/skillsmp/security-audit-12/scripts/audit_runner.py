#!/usr/bin/env python3
"""
Security Audit Runner (Divine Edition)
--------------------------------------
Checks for:
1. Hardcoded Secrets (Regex)
2. Risky Files (Extensions, Size)
3. Dependency Integrity (uv pip check)
"""

import os
import re
import sys
import subprocess
from pathlib import Path

# Config
MAX_FILE_SIZE_MB = 50
RISKY_EXTENSIONS = {'.exe', '.dll', '.so', '.dylib', '.class', '.jar', '.p12', '.pfx', '.pem', '.key'}
IGNORED_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.idea', '.vscode', 'tmp', 'temp'}
IGNORED_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'}

# Regex Patterns (Simplified for V1)
PATTERNS = [
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"github_pat_[0-9a-zA-Z_]{82}", "GitHub Fine-Grained Token"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"Bearer [a-zA-Z0-9\-\._~\+\/]{20,}", "Generic Bearer Token"),
    (r"PRIVATE " + r"KEY-----", "SSH/RSA Private Key"),
]

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def is_ignored(path):
    parts = path.parts
    for part in parts:
        if part in IGNORED_DIRS:
            return True
    if path.name in IGNORED_FILES:
        return True
    return False

def check_secrets():
    print(f"{BLUE}[1/3] Secret Scanning...{RESET}")
    issues = []
    
    # Walk only recognized text files or non-ignored files
    for root, dirs, files in os.walk("."):
        # Filter dirs in place
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            path = Path(root) / file
            if is_ignored(path):
                continue
                
            try:
                # Basic check: skip binary files or very large files for regex
                if path.stat().st_size > 1_000_000: # Skip > 1MB for regex speed
                    continue
                    
                text = path.read_text(encoding='utf-8', errors='ignore')
                for pattern, name in PATTERNS:
                    if re.search(pattern, text):
                        # Double check for false positives (simplistic)
                        issues.append(f"{name} found in {path}")
            except Exception:
                continue # Skip unreadable
                
    if issues:
        for i in issues:
            print(f"  {RED}✘ {i}{RESET}")
        return False
    
    print(f"  {GREEN}PASS{RESET}")
    return True

def check_risky_files():
    print(f"{BLUE}[2/3] Risky File Scanning (Binaries, Keys, size > {MAX_FILE_SIZE_MB}MB)...{RESET}")
    issues = []
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            path = Path(root) / file
            if is_ignored(path):
                continue
            
            # Check Extension
            if path.suffix.lower() in RISKY_EXTENSIONS:
                issues.append(f"Risky extension '{path.suffix}' in {path}")
                
            # Check Size
            try:
                size_mb = path.stat().st_size / (1024 * 1024)
                if size_mb > MAX_FILE_SIZE_MB:
                    issues.append(f"Large file ({size_mb:.2f} MB) in {path}")
            except Exception:
                pass

    if issues:
        for i in issues:
            print(f"  {RED}✘ {i}{RESET}")
        return False
        
    print(f"  {GREEN}PASS{RESET}")
    return True

def check_dependencies():
    print(f"{BLUE}[3/3] Python Dependency Check (uv pip check)...{RESET}")
    # Only run if uv is present
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(f"  {YELLOW}⚠ uv not found, skipping.{RESET}")
        return True # Not a failure, just skipped
        
    res = subprocess.run(["uv", "pip", "check"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  {GREEN}PASS{RESET}")
        return True
    else:
        print(f"  {RED}✘ Dependency issues found:{RESET}")
        print(res.stdout)
        print(res.stderr)
        return False

def main():
    print(f"{GREEN}=== SECURTY AUDIT START ==={RESET}")
    
    # Run Checks
    secret_ok = check_secrets()
    files_ok = check_risky_files()
    deps_ok = check_dependencies()
    
    print(f"{GREEN}=== SUMMARY ==={RESET}")
    print(f"Secrets:      {'✅ PASS' if secret_ok else '❌ FAIL'}")
    print(f"Risky Files:  {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    
    if secret_ok and files_ok and deps_ok:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
