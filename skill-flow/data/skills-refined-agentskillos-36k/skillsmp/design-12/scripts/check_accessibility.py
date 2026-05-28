#!/usr/bin/env python3
"""
Accessibility Checker

Performs basic static analysis for common accessibility issues in HTML files.
Not a replacement for proper accessibility testing, but catches obvious mistakes.

Usage:
    python check_accessibility.py <path> [--format text|json]
    python check_accessibility.py src/templates/ --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple
from html.parser import HTMLParser


class Issue(NamedTuple):
    file: str
    line: int
    element: str
    issue: str
    fix: str
    severity: str  # "error", "warning", "info"


# Void elements (no closing tag)
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}

# Elements that need accessible names
NEEDS_ACCESSIBLE_NAME = {"img", "button", "a", "input", "textarea", "select"}

# Form input types that need labels
LABELABLE_INPUTS = {
    "text", "password", "email", "tel", "url", "number", "search",
    "date", "time", "datetime-local", "month", "week", "color",
    "file", "checkbox", "radio", "range"
}


class AccessibilityParser(HTMLParser):
    """HTML parser that checks for accessibility issues."""

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.issues: list[Issue] = []
        self.heading_level = 0
        self.in_label = False
        self.label_for = None
        self.form_inputs: dict[str, int] = {}  # id -> line number
        self.labeled_inputs: set[str] = set()
        self.current_line = 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        attrs_dict = {k: v for k, v in attrs}
        line = self.getpos()[0]

        # Check specific elements
        if tag == "img":
            self._check_img(attrs_dict, line)
        elif tag == "a":
            self._check_link(attrs_dict, line)
        elif tag == "button":
            self._check_button(attrs_dict, line)
        elif tag == "input":
            self._check_input(attrs_dict, line)
        elif tag == "label":
            self.in_label = True
            self.label_for = attrs_dict.get("for")
            if self.label_for:
                self.labeled_inputs.add(self.label_for)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._check_heading(tag, line)
        elif tag == "html":
            self._check_html_lang(attrs_dict, line)
        elif tag == "iframe":
            self._check_iframe(attrs_dict, line)
        elif tag == "form":
            self._check_form(attrs_dict, line)
        elif tag == "table":
            self._check_table(attrs_dict, line)

    def handle_endtag(self, tag: str):
        if tag == "label":
            self.in_label = False
            self.label_for = None

    def _check_img(self, attrs: dict, line: int):
        """Check image accessibility."""
        alt = attrs.get("alt")
        role = attrs.get("role")

        # Missing alt attribute entirely
        if alt is None and role != "presentation":
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element="img",
                issue="Image missing alt attribute",
                fix='Add alt="" for decorative images or descriptive alt text for informative images',
                severity="error"
            ))
        # Empty alt on potentially informative image
        elif alt == "" and "src" in attrs:
            src = attrs["src"]
            # Skip common decorative patterns
            if not any(p in src.lower() for p in ["icon", "decoration", "background", "spacer"]):
                self.issues.append(Issue(
                    file=self.file_path,
                    line=line,
                    element="img",
                    issue="Image has empty alt - verify it's decorative",
                    fix="If image conveys information, add descriptive alt text",
                    severity="warning"
                ))

    def _check_link(self, attrs: dict, line: int):
        """Check link accessibility."""
        href = attrs.get("href")
        aria_label = attrs.get("aria-label")
        aria_labelledby = attrs.get("aria-labelledby")
        title = attrs.get("title")

        # Link with no href
        if href is None:
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element="a",
                issue="Link missing href attribute",
                fix="Add href attribute or use button element for actions",
                severity="warning"
            ))

        # Empty link (no content and no aria-label)
        # Note: Can't fully check this without parsing content
        if not aria_label and not aria_labelledby and not title:
            # This is just a flag - content check would need more context
            pass

    def _check_button(self, attrs: dict, line: int):
        """Check button accessibility."""
        btn_type = attrs.get("type")
        aria_label = attrs.get("aria-label")
        aria_labelledby = attrs.get("aria-labelledby")

        # Button without type (defaults to submit)
        if btn_type is None:
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element="button",
                issue="Button missing type attribute",
                fix='Add type="button" for non-submit buttons or type="submit" for forms',
                severity="warning"
            ))

    def _check_input(self, attrs: dict, line: int):
        """Check input accessibility."""
        input_type = attrs.get("type", "text")
        input_id = attrs.get("id")
        aria_label = attrs.get("aria-label")
        aria_labelledby = attrs.get("aria-labelledby")
        placeholder = attrs.get("placeholder")

        # Track input for label checking
        if input_id and input_type in LABELABLE_INPUTS:
            self.form_inputs[input_id] = line

        # Input without id (can't be associated with label)
        if input_type in LABELABLE_INPUTS:
            if not input_id and not aria_label and not aria_labelledby:
                self.issues.append(Issue(
                    file=self.file_path,
                    line=line,
                    element="input",
                    issue=f"Input type={input_type} has no accessible label",
                    fix="Add id and associated <label>, or use aria-label",
                    severity="error"
                ))

            # Placeholder as only label
            if placeholder and not aria_label and not aria_labelledby:
                if not input_id or input_id not in self.labeled_inputs:
                    self.issues.append(Issue(
                        file=self.file_path,
                        line=line,
                        element="input",
                        issue="Placeholder used as only label",
                        fix="Placeholders disappear when typing. Add a visible <label>",
                        severity="warning"
                    ))

    def _check_heading(self, tag: str, line: int):
        """Check heading hierarchy."""
        level = int(tag[1])

        # First heading should be h1
        if self.heading_level == 0 and level != 1:
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element=tag,
                issue=f"First heading is {tag}, not h1",
                fix="Start with h1, then use h2, h3, etc. in order",
                severity="warning"
            ))
        # Skipped heading level
        elif level > self.heading_level + 1 and self.heading_level > 0:
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element=tag,
                issue=f"Heading level skipped: h{self.heading_level} to {tag}",
                fix=f"Use h{self.heading_level + 1} instead of {tag}",
                severity="warning"
            ))

        self.heading_level = level

    def _check_html_lang(self, attrs: dict, line: int):
        """Check html element has lang attribute."""
        if "lang" not in attrs:
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element="html",
                issue="HTML element missing lang attribute",
                fix='Add lang="en" (or appropriate language code)',
                severity="error"
            ))

    def _check_iframe(self, attrs: dict, line: int):
        """Check iframe accessibility."""
        title = attrs.get("title")
        aria_label = attrs.get("aria-label")

        if not title and not aria_label:
            self.issues.append(Issue(
                file=self.file_path,
                line=line,
                element="iframe",
                issue="Iframe missing title attribute",
                fix="Add title attribute describing iframe content",
                severity="error"
            ))

    def _check_form(self, attrs: dict, line: int):
        """Check form accessibility."""
        # Reset input tracking for this form
        pass

    def _check_table(self, attrs: dict, line: int):
        """Flag tables for manual review."""
        self.issues.append(Issue(
            file=self.file_path,
            line=line,
            element="table",
            issue="Table found - verify it has proper headers",
            fix="Ensure <th> elements with scope attribute for data tables",
            severity="info"
        ))

    def finalize(self) -> list[Issue]:
        """Run final checks after parsing."""
        # Check for inputs without labels
        for input_id, line in self.form_inputs.items():
            if input_id not in self.labeled_inputs:
                self.issues.append(Issue(
                    file=self.file_path,
                    line=line,
                    element="input",
                    issue=f'Input id="{input_id}" has no associated label',
                    fix=f'Add <label for="{input_id}">',
                    severity="error"
                ))

        return self.issues


def check_css_accessibility(file_path: Path) -> list[Issue]:
    """Check CSS for common accessibility issues."""
    issues = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    lines = content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        # Check for outline: none without alternative
        if re.search(r"outline:\s*none", line) and ":focus" in line:
            # Look for alternative focus styles in nearby lines
            context = "\n".join(lines[max(0, line_num-3):min(len(lines), line_num+3)])
            if not re.search(r"(box-shadow|border|background)", context):
                issues.append(Issue(
                    file=str(file_path),
                    line=line_num,
                    element=":focus",
                    issue="outline: none removes focus indicator",
                    fix="Add alternative focus indicator (box-shadow, border, etc.)",
                    severity="error"
                ))

        # Check for small font sizes
        size_match = re.search(r"font-size:\s*(\d+)(px|pt)", line)
        if size_match:
            size = int(size_match.group(1))
            unit = size_match.group(2)
            if (unit == "px" and size < 12) or (unit == "pt" and size < 9):
                issues.append(Issue(
                    file=str(file_path),
                    line=line_num,
                    element="font-size",
                    issue=f"Font size {size}{unit} may be too small",
                    fix="Minimum recommended size is 12px/9pt for readability",
                    severity="warning"
                ))

        # Check for !important on display (might hide skip links incorrectly)
        if re.search(r"display:\s*none\s*!important", line):
            issues.append(Issue(
                file=str(file_path),
                line=line_num,
                element="display",
                issue="display: none !important may hide important content",
                fix="Verify this doesn't hide skip links or other accessible content",
                severity="info"
            ))

    return issues


def find_files(path: Path, extensions: set[str]) -> list[Path]:
    """Find all files with given extensions."""
    if path.is_file():
        return [path] if path.suffix in extensions else []

    files = []
    for ext in extensions:
        files.extend(path.rglob(f"*{ext}"))

    # Skip common directories
    skip_patterns = {"node_modules", "vendor", ".git", "dist", "build"}
    return sorted(
        f for f in files
        if not any(p in f.parts for p in skip_patterns)
    )


def format_text_output(issues: list[Issue]) -> str:
    """Format issues as human-readable text."""
    if not issues:
        return "✅ No accessibility issues found in static analysis."

    output = []
    output.append(f"Found {len(issues)} accessibility issue(s):\n")

    # Group by file
    by_file: dict[str, list[Issue]] = {}
    for issue in issues:
        by_file.setdefault(issue.file, []).append(issue)

    for file_path, file_issues in by_file.items():
        output.append(f"📄 {file_path}")
        for i in file_issues:
            if i.severity == "error":
                icon = "❌"
            elif i.severity == "warning":
                icon = "⚠️"
            else:
                icon = "ℹ️"

            output.append(f"  {icon} Line {i.line}: <{i.element}> {i.issue}")
            output.append(f"     └─ Fix: {i.fix}")
        output.append("")

    # Summary
    errors = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")
    info = sum(1 for i in issues if i.severity == "info")

    output.append("─" * 50)
    output.append(f"Summary: {errors} error(s), {warnings} warning(s), {info} info")

    if errors > 0:
        output.append("\n❌ Accessibility check FAILED")
        output.append("\nNote: This is basic static analysis. Always test with:")
        output.append("  - Screen readers (NVDA, VoiceOver)")
        output.append("  - Keyboard navigation")
        output.append("  - axe DevTools / Lighthouse")
    else:
        output.append("\n⚠️ Passed with findings. Review warnings and run full a11y audit.")

    return "\n".join(output)


def format_json_output(issues: list[Issue]) -> str:
    """Format issues as JSON."""
    return json.dumps({
        "total": len(issues),
        "errors": sum(1 for i in issues if i.severity == "error"),
        "warnings": sum(1 for i in issues if i.severity == "warning"),
        "info": sum(1 for i in issues if i.severity == "info"),
        "issues": [i._asdict() for i in issues],
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Check HTML/CSS for basic accessibility issues"
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    all_issues = []

    # Check HTML files
    html_files = find_files(path, {".html", ".htm"})
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8")
            parser = AccessibilityParser(str(html_file))
            parser.feed(content)
            all_issues.extend(parser.finalize())
        except Exception as e:
            print(f"Warning: Could not parse {html_file}: {e}", file=sys.stderr)

    # Check CSS files
    css_files = find_files(path, {".css"})
    for css_file in css_files:
        all_issues.extend(check_css_accessibility(css_file))

    if not html_files and not css_files:
        print(f"No HTML or CSS files found in {path}", file=sys.stderr)
        sys.exit(0)

    # Output
    if args.format == "json":
        print(format_json_output(all_issues))
    else:
        print(format_text_output(all_issues))

    # Exit code based on errors
    errors = sum(1 for i in all_issues if i.severity == "error")
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
