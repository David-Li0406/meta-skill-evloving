#!/usr/bin/env python3
"""
WhatsApp Flows Validator - Validates Flow JSON structure and constraints
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set
from colorama import Fore, Style, init

init(autoreset=True)


class FlowValidator:
    """Validates WhatsApp Flow JSON files"""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, flow_data: Dict) -> bool:
        """Main validation method - returns True if valid"""
        self.errors = []
        self.warnings = []

        # Check required top-level properties
        if "version" not in flow_data:
            self.errors.append("Missing required property: version")
            return False

        if "screens" not in flow_data:
            self.errors.append("Missing required property: screens")
            return False

        screens = flow_data.get("screens", [])
        if not isinstance(screens, list) or len(screens) == 0:
            self.errors.append("screens must be non-empty array")
            return False

        # Validate each screen
        screen_ids: Set[str] = set()
        for i, screen in enumerate(screens):
            if not isinstance(screen, dict):
                self.errors.append(f"Screen {i}: not an object")
                continue

            screen_id = screen.get("id")
            if not screen_id:
                self.errors.append(f"Screen {i}: missing required property 'id'")
                continue

            if screen_id in screen_ids:
                self.errors.append(f"Duplicate screen ID: {screen_id}")
            else:
                screen_ids.add(screen_id)

            # Check layout exists
            if "layout" not in screen:
                self.errors.append(f"Screen '{screen_id}': missing required property 'layout'")
                continue

            layout = screen.get("layout", {})
            if layout.get("type") != "SingleColumnLayout":
                self.errors.append(f"Screen '{screen_id}': only SingleColumnLayout supported")

            # Check terminal requirements
            if screen.get("terminal"):
                children = layout.get("children", [])
                has_footer = any(
                    c.get("type") == "Footer" for c in children if isinstance(c, dict)
                )
                if not has_footer:
                    self.errors.append(
                        f"Terminal screen '{screen_id}': must have Footer component"
                    )

            # Validate data schema
            if "data" in screen:
                data_schema = screen.get("data", {})
                self._check_examples(data_schema, screen_id)

        # Check routing model if present
        if "routing_model" in flow_data:
            self._validate_routing_model(flow_data.get("routing_model"), screen_ids)

        return len(self.errors) == 0

    def _validate_routing_model(self, routing_model: Dict, screen_ids: Set[str]) -> None:
        """Validate routing model consistency"""
        if not isinstance(routing_model, dict):
            self.errors.append("routing_model must be object")
            return

        for source, destinations in routing_model.items():
            if source not in screen_ids:
                self.errors.append(f"routing_model: screen '{source}' not found")

            if not isinstance(destinations, list):
                self.errors.append(f"routing_model '{source}': destinations must be array")
                continue

            if len(destinations) > 10:
                self.errors.append(
                    f"routing_model '{source}': exceeds 10 maximum destinations"
                )

            for dest in destinations:
                if dest not in screen_ids:
                    self.errors.append(
                        f"routing_model: destination screen '{dest}' not found"
                    )

    def _check_examples(self, schema: Dict, screen_id: str) -> None:
        """Check that all dynamic fields have __example__"""
        if not isinstance(schema, dict):
            return

        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            return

        for field_name in properties:
            field_def = properties[field_name]
            if isinstance(field_def, dict) and "__example__" not in field_def:
                self.warnings.append(
                    f"Screen '{screen_id}' data field '{field_name}': missing __example__"
                )

    def print_results(self) -> None:
        """Print validation results"""
        if self.errors:
            print(f"\n{Fore.RED}❌ Validation Failed{Style.RESET_ALL}\n")
            print(f"{Fore.RED}Errors ({len(self.errors)}):{Style.RESET_ALL}")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n{Fore.YELLOW}⚠ Warnings ({len(self.warnings)}):{Style.RESET_ALL}")
            for warning in self.warnings:
                print(f"  • {warning}")

        if not self.errors:
            if not self.warnings:
                print(f"\n{Fore.GREEN}✅ Flow is valid!{Style.RESET_ALL}\n")
            else:
                print(f"\n{Fore.GREEN}✅ Flow is valid (with warnings){Style.RESET_ALL}\n")


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate_flow.py <flow.json>")
        sys.exit(1)

    flow_path = Path(sys.argv[1])

    if not flow_path.exists():
        print(f"{Fore.RED}Error: File not found: {flow_path}{Style.RESET_ALL}")
        sys.exit(1)

    try:
        with open(flow_path, "r") as f:
            flow_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Invalid JSON - {e}{Style.RESET_ALL}")
        sys.exit(1)

    validator = FlowValidator()
    is_valid = validator.validate(flow_data)
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
