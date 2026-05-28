#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import unicodedata
from pathlib import Path

# Paths to macro-agent assets
MACRO_AGENT = Path("~/.copilot/skills/macro-agent/macro_agent.py").expanduser()
SEQUENCES_DIR = MACRO_AGENT.parent / "data" / "sequences"
PREFIX = "whatsapp_send_"


def preprocess_message(message: str) -> str:
    """
    Preprocess the message: convert to lowercase and remove accents.
    """
    # Convert to lowercase
    processed = message.lower()
    
    # Remove accents
    processed = unicodedata.normalize('NFD', processed)
    processed = ''.join(char for char in processed if unicodedata.category(char) != 'Mn')
    
    return processed


def normalize_contact(name: str) -> str:
    return name.strip().lower().replace(" ", "_")


def load_contacts():
    """Return a dict of available whatsapp_send_* sequences keyed by normalized alias."""
    contacts = {}
    if not SEQUENCES_DIR.exists():
        return contacts
    for path in SEQUENCES_DIR.glob(f"{PREFIX}*.json"):
        alias = path.stem.replace(PREFIX, "", 1)
        key = normalize_contact(alias)
        contacts[key] = {
            "alias": alias,
            "sequence": path.stem,
            "path": str(path),
        }
    return contacts


def run_macro_agent(args_list):
    """Execute macro-agent with provided arguments."""
    subprocess.run([sys.executable, str(MACRO_AGENT), *args_list], check=True)


def command_list():
    contacts = load_contacts()
    payload = {
        "success": True,
        "contacts": list(contacts.values()),
        "count": len(contacts),
        "hint": "Add more sequences in macro-agent using pattern whatsapp_send_<alias>.",
    }
    print(json.dumps(payload, ensure_ascii=True))


def command_send(contact: str, message: str):
    contacts = load_contacts()
    key = normalize_contact(contact)
    if key not in contacts:
        payload = {
            "success": False,
            "error": f"Contact '{contact}' not found. Use 'list' to see available contacts.",
            "available": list(contacts.keys()),
        }
        print(json.dumps(payload, ensure_ascii=True))
        sys.exit(1)

    sequence_name = contacts[key]["sequence"]
    
    # Preprocess the message
    processed_message = preprocess_message(message)
    
    try:
        run_macro_agent(["seq-run", sequence_name])
        run_macro_agent(["write", processed_message])
        run_macro_agent(["press", "enter"])
        payload = {
            "success": True,
            "contact": contacts[key]["alias"],
            "sequence": sequence_name,
            "original_message": message,
            "processed_message": processed_message,
        }
        print(json.dumps(payload, ensure_ascii=True))
    except subprocess.CalledProcessError as exc:
        payload = {
            "success": False,
            "error": str(exc),
            "sequence": sequence_name,
        }
        print(json.dumps(payload, ensure_ascii=True))
        sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser(description="WhatsApp messaging wrapper using macro-agent sequences.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List available WhatsApp contacts/groups derived from sequences.")

    send_p = sub.add_parser("send", help="Send message to contact/group.")
    send_p.add_argument("contact", help="Contact/group alias (matches whatsapp_send_<alias>).")
    send_p.add_argument("message", help="Message to send.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        command_list()
    elif args.command == "send":
        command_send(args.contact, args.message)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
