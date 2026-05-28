#!/usr/bin/env python3
"""
FixLog Writer Script.
Standardizes the creation of FixLog entries for ChromaDB.
Integrates with Dual Layer Audit (JSONL + Markdown).
"""
import argparse
import sys
import datetime
import json
import uuid
import os

# Add .agent/tools to python path to import event_logger
# Path: .agent/skills/fixlog_writer/scripts/write_log.py -> .agent/tools/event_logger.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../../tools"))
sys.path.append(TOOLS_DIR)

try:
    import event_logger
except ImportError:
    # Fallback if tools dir mapping fails (e.g. different execution context)
    event_logger = None

# ANSI Colors
GREEN = '\033[92m'
RESET = '\033[0m'
BLUE = '\033[94m'
YELLOW = '\033[93m'

def get_date_slug():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d")

def main():
    parser = argparse.ArgumentParser(description="Generate and save FixLog entry.")
    parser.add_argument("--project", required=True, help="Project Name")
    parser.add_argument("--prefix", default="AG", help="Project Prefix")
    parser.add_argument("--desc", required=True, help="Description of the fix (Document content)")
    parser.add_argument("--files", required=True, help="Comma separated list of modified files")
    parser.add_argument("--test", required=True, help="Test results summary")
    parser.add_argument("--result", required=True, choices=["pass", "fail"], help="Outcome")
    parser.add_argument("--evidence", default="", help="Path or Hash of Walkthrough Evidence")
    parser.add_argument("--notes", default="", help="Additional notes")
    parser.add_argument("--dry-run", action="store_true", help="Print JSON without serving/logging")

    args = parser.parse_args()

    # ID Generation Logic
    # Format: <Prefix>.fix.<YYYYMMDD>.<short_uuid>
    slug = str(uuid.uuid4())[:8]
    date_str = get_date_slug()
    log_id = f"{args.prefix}.fix.{date_str}.{slug}"
    
    # ISO Date for metadata
    iso_date = datetime.date.today().isoformat()

    file_list = [f.strip() for f in args.files.split(",")]

    # Construct Payload
    payload = {
        "id": log_id,
        "document": args.desc,
        "metadatas": {
            "project": args.project,
            "type": "fix_log",
            "date": iso_date,
            "files": file_list,
            "tests": args.test,
            "result": args.result,
            "evidence_path": args.evidence,
            "notes": args.notes
        }
    }

    if args.dry_run:
        print(f"{BLUE}=== DRY RUN: Generated Payload ==={RESET}")
        print(json.dumps(payload, indent=2))
        return

    # 1. Dual Layer Audit Logging (JSONL + MD)
    if event_logger:
        try:
            # Flatten payload for logger
            log_payload = payload["metadatas"].copy()
            log_payload["fixlog_id"] = log_id
            log_payload["description"] = args.desc 
            
            # Use Singleton
            event_logger.logger.set_context(project=args.project)
            event_logger.logger.log(event_logger.EventType.FIX_LOG.value, log_payload)
            print(f"{GREEN}✔ Audit Trail Updated (Event Log + Summary){RESET}")
        except Exception as e:
            print(f"{YELLOW}⚠ Audit Logging Failed: {e}{RESET}")
    else:
        print(f"{YELLOW}⚠ Event Logger module not found, skipping Audit Trail.{RESET}")

    # 2. Filesystem Persistence
    logs_dir = os.path.abspath(os.path.join(CURRENT_DIR, "../../../fix_logs"))
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f"{log_id}.json")
    
    try:
        with open(log_path, 'w') as f:
            json.dump(payload, f, indent=2)
        print(f"{GREEN}✔ FixLog saved to {log_path}{RESET}")
    except Exception as e:
        print(f"{RED}✘ Failed to save FixLog: {e}{RESET}")

    # 3. Chroma Injection Instruction
    print(f"\n{GREEN}=== Generated FixLog Payload ==={RESET}")
    print(json.dumps(payload, indent=2))
    print(f"\n{BLUE}To save to Chroma, use the chroma_add_documents tool with this data.{RESET}")

if __name__ == "__main__":
    main()
