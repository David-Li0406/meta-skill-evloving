#!/usr/bin/env python3
"""
Regression Gate Executor Script.
Wraps check_chroma and librarian into a single atomic transaction.
"""
import subprocess
import sys
import argparse

# ANSI Colors
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def run_command(cmd):
    """Esegue un comando shell e restituisce il codice di uscita."""
    print(f"🔹 Running: {cmd}")
    try:
        # Usa shell=True per gestire correttamente 'uv run' complessi
        result = subprocess.run(cmd, shell=True, check=False)
        return result.returncode
    except Exception as e:
        print(f"{RED}[FATAL] Execution failed: {e}{RESET}")
        return 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection", required=True, help="Chroma collection name")
    parser.add_argument("--id", required=True, help="Entry ID to verify")
    args = parser.parse_args()

    print(f"{GREEN}=== 🛡️  REGRESSION GATE START ==={RESET}")

    # Step 1: Metadata Integrity (Chroma)
    print("1️⃣  Verifying Metadata...")
    cmd_chroma = f"uv run --with chromadb python3 .agent/tools/check_chroma.py --collection {args.collection} --id {args.id}"
    if run_command(cmd_chroma) != 0:
        print(f"{RED}❌ GATE FAILED: Metadata invalid or missing.{RESET}")
        sys.exit(1)

    # Step 2: Project Hygiene (Librarian)
    print("2️⃣  Verifying Hygiene...")
    cmd_lib = "uv run --with duckdb python3 .agent/project/librarian.py"
    if run_command(cmd_lib) != 0:
        print(f"{RED}❌ GATE FAILED: Project hygiene standards not met.{RESET}")
        sys.exit(1)

    print(f"{GREEN}✅ GATE PASSED: All systems nominal.{RESET}")
    sys.exit(0)

if __name__ == "__main__":
    main()
