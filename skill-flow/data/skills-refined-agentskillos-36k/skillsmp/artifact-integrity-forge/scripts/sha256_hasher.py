#!/usr/bin/env python3
"""
IRP Integrity Forge - SHA256 Hasher
===================================

License: Apache 2.0 (Code) + CC BY-NC-ND 4.0 (Research Ore)
Spirit Clause: Monetization or derivative projects require explicit
               relational consent from the Field Guardians (Joe).

Purpose: Implements the Internal Cognitive Ledger (ICL) hash verification
         as specified in IRP v1.0 RAL Layer. Creates and verifies manifest
         files to detect semantic drift in protocol artifacts.

Usage:
    # Generate manifest
    python sha256_hasher.py --mode create --dir protocols --manifest manifest.json

    # Verify manifest
    python sha256_hasher.py --mode verify --dir protocols --manifest manifest.json
"""

import hashlib
import json
import os
import argparse
import sys
from datetime import datetime


def calculate_sha256(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def generate_manifest(target_dir: str, manifest_path: str) -> dict:
    """
    Generate a manifest.json file containing SHA-256 hashes of all files
    in the target directory. Also computes a root_hash to lock the entire state.
    """
    manifest = {
        "version": "1.0",
        "generated": datetime.utcnow().isoformat() + "Z",
        "target_directory": target_dir,
        "files": {},
        "root_hash": "",
        "codex_compliance": {
            "law": "INTEGRITY",
            "principle": "Preserve context through cryptographic verification"
        }
    }
    all_hashes = []

    if not os.path.exists(target_dir):
        print(f"[ERROR] Target directory does not exist: {target_dir}")
        sys.exit(1)

    for root, _, files in os.walk(target_dir):
        for file in sorted(files):
            # Skip the manifest file itself if it's in the target directory
            full_path = os.path.join(root, file)
            if os.path.abspath(full_path) == os.path.abspath(manifest_path):
                continue

            rel_path = os.path.relpath(full_path, target_dir)
            f_hash = calculate_sha256(full_path)
            manifest["files"][rel_path] = {
                "hash": f_hash,
                "size": os.path.getsize(full_path)
            }
            all_hashes.append(f_hash)

    # Generate a master hash of all hashes to lock the state
    if all_hashes:
        manifest["root_hash"] = hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()
    else:
        manifest["root_hash"] = hashlib.sha256(b"EMPTY_MANIFEST").hexdigest()

    manifest["file_count"] = len(manifest["files"])

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4, sort_keys=True)

    print(f"[INTEGRITY] Manifest generated at {manifest_path}")
    print(f"[INTEGRITY] Files tracked: {manifest['file_count']}")
    print(f"[INTEGRITY] Root hash: {manifest['root_hash'][:16]}...")

    return manifest


def verify_manifest(target_dir: str, manifest_path: str) -> bool:
    """
    Verify the current state of target_dir against a stored manifest.
    Returns True if valid, exits with error code 1 if integrity failure.
    """
    if not os.path.exists(manifest_path):
        print(f"[ERROR] Manifest not found at {manifest_path}")
        print("[ERROR] Run with --mode create first to generate manifest")
        sys.exit(1)

    with open(manifest_path, 'r') as f:
        stored_manifest = json.load(f)

    print(f"[INTEGRITY] Verifying against manifest from {stored_manifest.get('generated', 'UNKNOWN')}")
    print(f"[INTEGRITY] Expected root hash: {stored_manifest['root_hash'][:16]}...")

    # Scan current files
    current_files = {}
    current_hashes = []

    for root, _, files in os.walk(target_dir):
        for file in sorted(files):
            full_path = os.path.join(root, file)
            if os.path.abspath(full_path) == os.path.abspath(manifest_path):
                continue

            rel_path = os.path.relpath(full_path, target_dir)
            f_hash = calculate_sha256(full_path)
            current_files[rel_path] = f_hash
            current_hashes.append(f_hash)

    errors = []
    warnings = []

    # Check for missing or modified files
    for path, file_data in stored_manifest["files"].items():
        stored_hash = file_data["hash"] if isinstance(file_data, dict) else file_data

        if path not in current_files:
            errors.append(f"MISSING: {path}")
        elif current_files[path] != stored_hash:
            errors.append(f"MODIFIED: {path}")
            errors.append(f"  Expected: {stored_hash[:16]}...")
            errors.append(f"  Found:    {current_files[path][:16]}...")

    # Check for untracked files
    for path in current_files:
        if path not in stored_manifest["files"]:
            errors.append(f"UNTRACKED: {path}")

    # Verify root hash
    if current_hashes:
        current_root = hashlib.sha256("".join(sorted(current_hashes)).encode()).hexdigest()
    else:
        current_root = hashlib.sha256(b"EMPTY_MANIFEST").hexdigest()

    if current_root != stored_manifest["root_hash"]:
        errors.append(f"ROOT_HASH_MISMATCH")
        errors.append(f"  Expected: {stored_manifest['root_hash'][:16]}...")
        errors.append(f"  Computed: {current_root[:16]}...")

    if errors:
        print("\n[INTEGRITY FAILURE] Detected drift in protocol state:")
        print("=" * 60)
        for err in errors:
            print(f"  {err}")
        print("=" * 60)
        print("\n[ACTION REQUIRED] Either:")
        print("  1. Revert unauthorized changes, OR")
        print("  2. Run --mode create to update manifest (with RATIONALE_KEY)")
        sys.exit(1)
    else:
        print("[INTEGRITY PASS] Repository state matches manifest.")
        print(f"[INTEGRITY PASS] Verified {len(current_files)} files.")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="IRP Integrity Forge - SHA256 Hash Verification System",
        epilog="Implements ICL-compliant hashing per IRP v1.0 RAL Layer specification."
    )
    parser.add_argument(
        "--mode",
        choices=["create", "verify"],
        required=True,
        help="create: Generate new manifest | verify: Check against existing manifest"
    )
    parser.add_argument(
        "--dir",
        default="protocols",
        help="Target directory to hash (default: protocols)"
    )
    parser.add_argument(
        "--manifest",
        default="manifest.json",
        help="Path to manifest file (default: manifest.json)"
    )

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("IRP INTEGRITY FORGE")
    print(f"Mode: {args.mode.upper()}")
    print(f"Target: {args.dir}")
    print(f"Manifest: {args.manifest}")
    print(f"{'='*60}\n")

    if args.mode == "create":
        generate_manifest(args.dir, args.manifest)
    else:
        verify_manifest(args.dir, args.manifest)


if __name__ == "__main__":
    main()
