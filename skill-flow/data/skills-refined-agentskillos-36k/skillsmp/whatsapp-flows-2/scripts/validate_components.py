#!/usr/bin/env python3
"""
Component-specific validator for WhatsApp Flows
"""

import json
import sys
from pathlib import Path
from typing import Dict
from colorama import Fore, Style, init

init(autoreset=True)


class ComponentValidator:
    """Validates individual components and their constraints"""

    COMPONENTS = {
        "TextHeading": {"max_text": 80},
        "TextSubheading": {"max_text": 80},
        "TextBody": {"max_text": 4096},
        "TextCaption": {"max_text": 409},
        "RichText": {"max_text": 4096, "version": "5.1+"},
        "TextInput": {"max_length": 80, "requires": ["name"]},
        "TextArea": {"max_length": 600, "requires": ["name"]},
        "CheckboxGroup": {"max_options": 20, "requires": ["name"]},
        "RadioButtonsGroup": {"max_options": 20, "requires": ["name"]},
        "Dropdown": {"requires": ["name"]},
        "OptIn": {"max_label": 80, "requires": ["name", "label"]},
        "DatePicker": {"requires": ["name"]},
        "CalendarPicker": {"version": "6.1+", "requires": ["name"]},
        "PhotoPicker": {"version": "5.0+", "requires": ["name"]},
        "DocumentPicker": {"version": "5.0+", "requires": ["name"]},
        "Image": {"requires": ["src"]},
        "ImageCarousel": {"version": "7.1+", "requires": ["images"]},
        "NavigationList": {"version": "6.2+", "requires": ["name"]},
        "ChipsSelector": {"version": "6.3+", "requires": ["name"]},
        "EmbeddedLink": {"max_text": 25, "requires": ["text"]},
        "Footer": {"max_label": 30, "requires": ["label"]},
        "If": {"requires": ["condition", "then"]},
        "Switch": {"requires": ["value", "cases"]},
    }

    def __init__(self):
        self.errors = 0
        self.warnings = 0

    def validate_component(self, component: Dict, screen_id: str, index: int) -> None:
        """Validate a single component"""
        comp_type = component.get("type")
        if not comp_type:
            print(f"{Fore.RED}❌ Screen '{screen_id}' component {index}: missing type{Style.RESET_ALL}")
            self.errors += 1
            return

        if comp_type not in self.COMPONENTS:
            print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type} {index}: unknown type{Style.RESET_ALL}")
            self.errors += 1
            return

        spec = self.COMPONENTS[comp_type]

        # Check required properties
        for required in spec.get("requires", []):
            if required not in component:
                print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type}: missing '{required}'{Style.RESET_ALL}")
                self.errors += 1

        # Check markdown property rules
        has_markdown = "markdown" in component
        if has_markdown:
            # Only TextBody and TextCaption support markdown
            if comp_type not in ["TextBody", "TextCaption"]:
                print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type}: Property 'markdown' is not allowed in '{comp_type}' component{Style.RESET_ALL}")
                self.errors += 1
            else:
                # Warn if markdown is enabled
                if component.get("markdown") is True:
                    print(f"{Fore.CYAN}✓ Screen '{screen_id}' {comp_type}: markdown enabled{Style.RESET_ALL}")

        # Check text limits
        if "max_text" in spec:
            text = component.get("text", "")
            if len(text) > spec["max_text"]:
                print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type}: text exceeds {spec['max_text']} chars{Style.RESET_ALL}")
                self.errors += 1

        # Check label limits
        if "max_label" in spec:
            label = component.get("label", "")
            if len(label) > spec["max_label"]:
                print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type}: label exceeds {spec['max_label']} chars{Style.RESET_ALL}")
                self.errors += 1

        # Check image URL
        if comp_type == "Image":
            src = component.get("src", "")
            if src and not src.startswith("https://"):
                print(f"{Fore.RED}❌ Screen '{screen_id}' Image: must use HTTPS{Style.RESET_ALL}")
                self.errors += 1

        # Check data-source options
        if "data-source" in component:
            data_source = component.get("data-source", {})
            if isinstance(data_source, dict):
                values = data_source.get("values", [])
                if isinstance(values, list) and len(values) == 0:
                    print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type}: no options{Style.RESET_ALL}")
                    self.errors += 1

                if "max_options" in spec and isinstance(values, list):
                    if len(values) > spec["max_options"]:
                        print(f"{Fore.RED}❌ Screen '{screen_id}' {comp_type}: exceeds {spec['max_options']} options{Style.RESET_ALL}")
                        self.errors += 1

    def validate_all(self, flow_data: Dict) -> None:
        """Validate all components in flow"""
        screens = flow_data.get("screens", [])
        for screen in screens:
            if not isinstance(screen, dict):
                continue

            screen_id = screen.get("id", "unknown")
            layout = screen.get("layout", {})
            children = layout.get("children", [])

            for i, component in enumerate(children):
                if isinstance(component, dict):
                    self.validate_component(component, screen_id, i)


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate_components.py <flow.json>")
        sys.exit(1)

    flow_path = Path(sys.argv[1])

    if not flow_path.exists():
        print(f"{Fore.RED}Error: File not found{Style.RESET_ALL}")
        sys.exit(1)

    try:
        with open(flow_path, "r") as f:
            flow_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Invalid JSON{Style.RESET_ALL}")
        sys.exit(1)

    validator = ComponentValidator()
    validator.validate_all(flow_data)

    print(f"\n{Fore.CYAN}Component Validation:{Style.RESET_ALL}")
    if validator.errors == 0:
        print(f"{Fore.GREEN}✅ All components valid{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}{validator.errors} error(s){Style.RESET_ALL}\n")

    sys.exit(0 if validator.errors == 0 else 1)


if __name__ == "__main__":
    main()
