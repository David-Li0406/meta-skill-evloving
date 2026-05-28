#!/usr/bin/env python3
"""
Report Compilation Script

Compiles project planning outputs into a professional report with optional
IEEE citations, table of contents, and cover page.

Supports PDF (via Pandoc/LaTeX), DOCX, and Markdown output.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Default section ordering
DEFAULT_SECTION_ORDER = [
    ("SUMMARY.md", "Executive Summary"),
    ("research", "Market Research"),
    ("specifications", "Technical Specifications"),
    ("diagrams", "Architecture Diagrams"),
    ("components", "Building Blocks"),
    ("planning", "Implementation Plan"),
    ("analysis", "Analysis"),
    ("marketing", "Go-to-Market Strategy"),
]

# File ordering within sections
SECTION_FILE_ORDER = {
    "research": [
        "market_research.md",
        "market_overview.md",
        "competitive_analysis.md",
        "technology_research.md",
    ],
    "specifications": [
        "project_spec.md",
        "technical_spec.md",
        "api_spec.md",
    ],
    "planning": [
        "sprint_plan.md",
        "timeline.md",
        "milestones.md",
    ],
    "analysis": [
        "feasibility.md",
        "feasibility_analysis.md",
        "cost_analysis.md",
        "service_cost_analysis.md",
        "risk_assessment.md",
        "roi_projections.md",
    ],
    "marketing": [
        "campaign_brief.md",
        "marketing_campaign.md",
        "content_calendar.md",
        "influencer_strategy.md",
    ],
    "components": [
        "building_blocks.md",
        "building_blocks.yaml",
    ],
}


class ReportCompiler:
    """Compiles markdown files into a unified report."""

    def __init__(
        self,
        input_dir: str,
        output_file: str,
        output_format: str = "pdf",
        sections: Optional[list[str]] = None,
        citations: bool = False,
        toc: bool = True,
        cover_title: Optional[str] = None,
        template: Optional[str] = None,
        excluded_files: Optional[list[str]] = None,
        additional_files: Optional[list[str]] = None,
    ):
        self.input_dir = Path(input_dir)
        self.output_file = Path(output_file)
        self.output_format = output_format.lower()
        self.sections = sections or ["research", "specifications", "components", "planning", "analysis"]
        self.citations = citations
        self.toc = toc
        self.cover_title = cover_title or self._extract_project_name()
        self.template = template
        self.excluded_files = excluded_files or []
        self.additional_files = additional_files or []

        # Citation tracking
        self.citation_data: list[dict] = []
        self.citation_map: dict[str, int] = {}  # url -> citation number
        self.next_citation_num = 1

    def _extract_project_name(self) -> str:
        """Extract project name from folder name."""
        folder_name = self.input_dir.name
        # Format: YYYYMMDD_HHMMSS_project_name
        parts = folder_name.split("_", 2)
        if len(parts) >= 3:
            return parts[2].replace("_", " ").title()
        return folder_name.replace("_", " ").title()

    def compile(self) -> bool:
        """Main compilation method."""
        print(f"Compiling report from: {self.input_dir}")
        print(f"Output: {self.output_file} ({self.output_format})")

        # Load citations if enabled
        if self.citations:
            self._load_citations()

        # Build combined markdown
        combined_md = self._build_combined_markdown()

        # Write intermediate markdown
        temp_md = self.output_file.with_suffix(".compiled.md")
        temp_md.write_text(combined_md, encoding="utf-8")
        print(f"Intermediate markdown: {temp_md}")

        # Convert to output format
        if self.output_format == "md":
            # Just rename the temp file
            temp_md.rename(self.output_file)
            print(f"Markdown report: {self.output_file}")
            return True

        success = self._convert_with_pandoc(temp_md)

        # Clean up temp file on success
        if success and temp_md.exists():
            temp_md.unlink()

        return success

    def _load_citations(self) -> None:
        """Load all citation JSON files."""
        citation_files = list(self.input_dir.rglob("*.citations.json"))
        print(f"Found {len(citation_files)} citation files")

        for cf in citation_files:
            try:
                data = json.loads(cf.read_text(encoding="utf-8"))
                citations = data.get("citations", [])
                for cite in citations:
                    url = cite.get("url", "")
                    if url and url not in self.citation_map:
                        self.citation_map[url] = self.next_citation_num
                        cite["number"] = self.next_citation_num
                        self.citation_data.append(cite)
                        self.next_citation_num += 1
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load {cf}: {e}")

        print(f"Loaded {len(self.citation_data)} unique citations")

    def _build_combined_markdown(self) -> str:
        """Build the combined markdown content."""
        parts = []

        # Cover page
        parts.append(self._generate_cover_page())
        parts.append("\n\\newpage\n")

        # Table of contents placeholder (Pandoc handles actual TOC)
        if self.toc:
            parts.append("# Table of Contents\n")
            parts.append("\\tableofcontents\n")
            parts.append("\\newpage\n")

        # Process sections in order
        for section_key, section_title in DEFAULT_SECTION_ORDER:
            if section_key == "SUMMARY.md":
                # Handle executive summary specially
                summary_file = self.input_dir / "SUMMARY.md"
                if summary_file.exists():
                    content = self._process_markdown_file(summary_file)
                    parts.append(f"\n# Executive Summary\n\n{content}\n")
                    parts.append("\\newpage\n")
                continue

            if section_key not in self.sections:
                continue

            section_dir = self.input_dir / section_key
            if not section_dir.exists():
                continue

            # Get files in this section
            section_content = self._process_section(section_dir, section_key, section_title)
            if section_content:
                parts.append(section_content)

        # Add any additional files
        for add_file in self.additional_files:
            add_path = Path(add_file)
            if add_path.exists():
                content = self._process_markdown_file(add_path)
                parts.append(f"\n# {add_path.stem.replace('_', ' ').title()}\n\n{content}\n")

        # Add references section if citations enabled
        if self.citations and self.citation_data:
            parts.append("\n\\newpage\n")
            parts.append(self._generate_references_section())

        return "\n".join(parts)

    def _generate_cover_page(self) -> str:
        """Generate the cover page markdown."""
        date_str = datetime.now().strftime("%B %d, %Y")

        return f"""---
title: "{self.cover_title}"
subtitle: "Project Planning Report"
date: "{date_str}"
---

\\begin{{center}}

\\vspace*{{2cm}}

{{\\Huge \\textbf{{{self.cover_title}}}}}

\\vspace{{1cm}}

{{\\Large Project Planning Report}}

\\vspace{{2cm}}

{{\\large {date_str}}}

\\vspace{{3cm}}

{{\\small Generated by Claude Project Planner}}

\\end{{center}}

\\newpage
"""

    def _process_section(self, section_dir: Path, section_key: str, section_title: str) -> str:
        """Process all files in a section."""
        parts = [f"\n# {section_title}\n"]

        # Get ordered file list
        file_order = SECTION_FILE_ORDER.get(section_key, [])
        processed_files = set()

        # Process files in preferred order first
        for filename in file_order:
            filepath = section_dir / filename
            if filepath.exists() and str(filepath) not in self.excluded_files:
                content = self._process_markdown_file(filepath)
                if content.strip():
                    # Demote headings by one level
                    content = self._demote_headings(content)
                    parts.append(content)
                    parts.append("\n")
                processed_files.add(filepath.name)

        # Process remaining files
        for filepath in sorted(section_dir.glob("*.md")):
            if filepath.name not in processed_files and str(filepath) not in self.excluded_files:
                content = self._process_markdown_file(filepath)
                if content.strip():
                    content = self._demote_headings(content)
                    parts.append(content)
                    parts.append("\n")

        # Handle YAML files (building blocks)
        for filepath in sorted(section_dir.glob("*.yaml")):
            if str(filepath) not in self.excluded_files:
                content = self._yaml_to_markdown(filepath)
                if content.strip():
                    parts.append(content)
                    parts.append("\n")

        if len(parts) == 1:
            return ""  # No content in section

        parts.append("\\newpage\n")
        return "\n".join(parts)

    def _process_markdown_file(self, filepath: Path) -> str:
        """Process a single markdown file, handling citations if enabled."""
        content = filepath.read_text(encoding="utf-8")

        # Remove YAML frontmatter if present
        if content.startswith("---"):
            end_idx = content.find("---", 3)
            if end_idx > 0:
                content = content[end_idx + 3:].strip()

        # Process citations if enabled
        if self.citations:
            content = self._process_inline_citations(content, filepath)

        return content

    def _process_inline_citations(self, content: str, source_file: Path) -> str:
        """Replace citation markers with IEEE-style numbers."""
        # Look for associated citations file
        citation_file = source_file.with_suffix(".citations.json")
        if not citation_file.exists():
            citation_file = source_file.parent / f"{source_file.stem}.citations.json"

        if citation_file.exists():
            try:
                data = json.loads(citation_file.read_text(encoding="utf-8"))
                inline_refs = data.get("inline_refs", [])

                for ref in inline_refs:
                    cite_id = ref.get("cite_id", "")
                    url = ref.get("url", "")

                    if url in self.citation_map:
                        num = self.citation_map[url]
                        # Replace various citation marker formats
                        content = re.sub(
                            rf"\[{re.escape(cite_id)}\]",
                            f"[{num}]",
                            content
                        )
            except (json.JSONDecodeError, IOError):
                pass

        return content

    def _demote_headings(self, content: str) -> str:
        """Demote all headings by one level (# -> ##)."""
        lines = content.split("\n")
        result = []
        for line in lines:
            if line.startswith("#"):
                # Add one # to demote
                result.append("#" + line)
            else:
                result.append(line)
        return "\n".join(result)

    def _yaml_to_markdown(self, filepath: Path) -> str:
        """Convert YAML building blocks to markdown."""
        try:
            import yaml
            data = yaml.safe_load(filepath.read_text(encoding="utf-8"))
        except ImportError:
            # Fallback: just include as code block
            content = filepath.read_text(encoding="utf-8")
            return f"## Building Blocks\n\n```yaml\n{content}\n```\n"
        except Exception:
            return ""

        if not data:
            return ""

        blocks = data.get("building_blocks", data.get("blocks", []))
        if not blocks:
            return ""

        parts = ["## Building Blocks\n"]

        for block in blocks:
            name = block.get("name", "Unnamed Block")
            block_id = block.get("id", "")
            desc = block.get("description", "")
            complexity = block.get("complexity", "")

            parts.append(f"### {name}")
            if block_id:
                parts.append(f"**ID:** {block_id}")
            if desc:
                parts.append(f"\n{desc}\n")
            if complexity:
                parts.append(f"**Complexity:** {complexity}")

            # Responsibilities
            responsibilities = block.get("responsibilities", [])
            if responsibilities:
                parts.append("\n**Responsibilities:**")
                for resp in responsibilities:
                    parts.append(f"- {resp}")

            # Test criteria
            test_criteria = block.get("test_criteria", [])
            if test_criteria:
                parts.append("\n**Acceptance Criteria:**")
                for tc in test_criteria:
                    parts.append(f"- {tc}")

            parts.append("")

        return "\n".join(parts)

    def _generate_references_section(self) -> str:
        """Generate IEEE-formatted references section."""
        parts = ["# References\n"]

        for cite in sorted(self.citation_data, key=lambda x: x.get("number", 0)):
            num = cite.get("number", 0)
            title = cite.get("title", "Untitled")
            author = cite.get("author", "")
            url = cite.get("url", "")
            date = cite.get("date", "")
            accessed = cite.get("accessed", datetime.now().strftime("%d-%b.-%Y"))

            # Format author
            if not author:
                # Try to extract from URL domain
                if url:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc.replace("www.", "")
                    author = domain.split(".")[0].title()

            # Format date
            if date:
                try:
                    dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
                    date_str = dt.strftime("%d-%b.-%Y")
                except ValueError:
                    date_str = date
            else:
                date_str = "n.d."

            # IEEE format for web source
            ref_line = f"[{num}] "
            if author:
                ref_line += f"{author}, "
            ref_line += f'"{title}," '
            ref_line += f"{date_str}. "
            if url:
                ref_line += f"[Online]. Available: {url}"

            parts.append(ref_line)
            parts.append("")

        return "\n".join(parts)

    def _convert_with_pandoc(self, input_file: Path) -> bool:
        """Convert markdown to output format using Pandoc."""
        cmd = [
            "pandoc",
            str(input_file),
            "-o", str(self.output_file),
            "--standalone",
            "-V", "geometry:margin=1in",
            "-V", "fontsize=11pt",
            "-V", "colorlinks=true",
            "-V", "linkcolor=blue",
            "-V", "urlcolor=blue",
        ]

        if self.output_format == "pdf":
            cmd.extend(["--pdf-engine=xelatex"])

        if self.toc:
            cmd.extend(["--toc", "--toc-depth=3"])

        if self.template and Path(self.template).exists():
            cmd.extend(["--template", self.template])

        print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Report generated: {self.output_file}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Pandoc error: {e.stderr}")
            return False
        except FileNotFoundError:
            print("Error: Pandoc not found. Install with: brew install pandoc")
            return False


def check_dependencies() -> dict[str, bool]:
    """Check if required dependencies are installed."""
    deps = {}

    # Check Pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        deps["pandoc"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        deps["pandoc"] = False

    # Check xelatex (for PDF)
    try:
        subprocess.run(["xelatex", "--version"], capture_output=True, check=True)
        deps["xelatex"] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        deps["xelatex"] = False

    return deps


def main():
    parser = argparse.ArgumentParser(
        description="Compile project planning outputs into a professional report"
    )
    parser.add_argument(
        "--input-dir", "-i",
        required=True,
        help="Planning outputs folder path"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: <input-dir>/REPORT.<format>)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["pdf", "docx", "md"],
        default="pdf",
        help="Output format (default: pdf)"
    )
    parser.add_argument(
        "--sections", "-s",
        help="Comma-separated sections to include (default: all)"
    )
    parser.add_argument(
        "--citations",
        action="store_true",
        help="Enable IEEE citation processing"
    )
    parser.add_argument(
        "--no-toc",
        action="store_true",
        help="Disable table of contents"
    )
    parser.add_argument(
        "--cover-title",
        help="Custom cover page title"
    )
    parser.add_argument(
        "--template",
        help="Custom Pandoc template file"
    )
    parser.add_argument(
        "--exclude",
        help="Comma-separated files to exclude"
    )
    parser.add_argument(
        "--include",
        help="Comma-separated additional files to include"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check if dependencies are installed"
    )

    args = parser.parse_args()

    if args.check_deps:
        deps = check_dependencies()
        print("Dependency check:")
        for name, installed in deps.items():
            status = "✓ installed" if installed else "✗ NOT installed"
            print(f"  {name}: {status}")

        if not deps.get("pandoc"):
            print("\nInstall Pandoc: brew install pandoc")
        if not deps.get("xelatex"):
            print("Install LaTeX: brew install --cask mactex")

        sys.exit(0 if all(deps.values()) else 1)

    # Set default output path
    input_dir = Path(args.input_dir)
    if args.output:
        output_file = str(args.output)
    else:
        output_file = str(input_dir / f"REPORT.{args.format}")

    # Parse sections
    sections = None
    if args.sections:
        sections = [s.strip() for s in args.sections.split(",")]

    # Parse exclusions/inclusions
    excluded = []
    if args.exclude:
        excluded = [f.strip() for f in args.exclude.split(",")]

    additional = []
    if args.include:
        additional = [f.strip() for f in args.include.split(",")]

    # Check dependencies for PDF
    if args.format == "pdf":
        deps = check_dependencies()
        if not deps.get("pandoc"):
            print("Error: Pandoc required for PDF. Install: brew install pandoc")
            sys.exit(1)
        if not deps.get("xelatex"):
            print("Warning: xelatex not found. PDF may fail. Install: brew install --cask mactex")

    # Compile report
    compiler = ReportCompiler(
        input_dir=args.input_dir,
        output_file=output_file,
        output_format=args.format,
        sections=sections,
        citations=args.citations,
        toc=not args.no_toc,
        cover_title=args.cover_title,
        template=args.template,
        excluded_files=excluded,
        additional_files=additional,
    )

    success = compiler.compile()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
