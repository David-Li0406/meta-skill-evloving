#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path
from typing import Dict


def main():
    if len(sys.argv) < 3:
        print("Usage: python update_flake.py <flake.nix> <versions.json>", file=sys.stderr)
        sys.exit(1)
    
    flake_path = Path(sys.argv[1])
    versions_path = Path(sys.argv[2])
    
    if not flake_path.exists():
        print(f"Error: {flake_path} does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not versions_path.exists():
        print(f"Error: {versions_path} does not exist", file=sys.stderr)
        sys.exit(1)
    
    with open(versions_path) as f:
        versions = json.load(f)
    
    flake_content = flake_path.read_text()
    
    for package_name, info in versions.items():
        version = info["tag"].lstrip("v")
        tag = info["tag"]
        sha256 = info["sha256"]
        print(f"Updating {package_name} to {version}...", file=sys.stderr)
        
        pattern = rf'({package_name} = self\.trivialBuild {{\s+pname = "{package_name}";\s+version = )"[^"]+"(;\s+src = final\.fetchFromGitHub {{\s+owner = "xenodium";\s+repo = "[^"]+";\s+rev = )"[^"]+"(;\s+sha256 = )"[^"]+"(;)'
        replacement = rf'\g<1>"{version}"\g<2>"{tag}"\g<3>"{sha256}"\g<4>'
        
        flake_content = re.sub(pattern, replacement, flake_content, flags=re.MULTILINE)
        
        if re.search(pattern, flake_content) is None:
            print(
                f"Warning: Pattern may not have matched for {package_name}",
                file=sys.stderr,
            )
    
    flake_path.write_text(flake_content)
    print(f"Successfully updated {flake_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
