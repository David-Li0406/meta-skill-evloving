#!/usr/bin/env python3
"""
Citation Formatter for IEEE Style

Processes citation JSON files and formats them according to IEEE standards.
Generates a references markdown file and provides utilities for inline citation
replacement.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


class IEEECitationFormatter:
    """Formats citations according to IEEE style guidelines."""

    def __init__(self):
        self.citations: list[dict] = []
        self.citation_map: dict[str, int] = {}  # url/id -> number
        self.next_number = 1

    def load_citations_from_directory(self, directory: str) -> int:
        """
        Load all citation JSON files from a directory.

        Returns the number of citations loaded.
        """
        dir_path = Path(directory)
        citation_files = list(dir_path.rglob("*.citations.json"))

        for cf in citation_files:
            self._load_citation_file(cf)

        return len(self.citations)

    def load_citations_from_file(self, filepath: str) -> int:
        """Load citations from a single JSON file."""
        self._load_citation_file(Path(filepath))
        return len(self.citations)

    def _load_citation_file(self, filepath: Path) -> None:
        """Load and process a single citation file."""
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            citations = data.get("citations", [])

            for cite in citations:
                # Use URL as unique identifier
                url = cite.get("url", "")
                cite_id = cite.get("id", url)

                if cite_id and cite_id not in self.citation_map:
                    self.citation_map[cite_id] = self.next_number
                    cite["number"] = self.next_number
                    cite["source_file"] = str(filepath)
                    self.citations.append(cite)
                    self.next_number += 1

        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)

    def format_citation_ieee(self, citation: dict) -> str:
        """
        Format a single citation in IEEE style.

        IEEE Web Source Format:
        [N] Author, "Title," Source, Date. [Online]. Available: URL

        IEEE Journal Format:
        [N] Author, "Title," Journal, vol. X, no. Y, pp. Z, Date.
        """
        num = citation.get("number", 0)
        title = citation.get("title", "Untitled")
        author = citation.get("author", "")
        url = citation.get("url", "")
        date = citation.get("date", "")
        source = citation.get("source", "")
        doi = citation.get("doi", "")

        # Clean up title
        title = title.strip().rstrip(".")

        # Format author (IEEE uses first initial, last name)
        if not author and url:
            # Extract domain as fallback author
            domain = urlparse(url).netloc.replace("www.", "")
            author = domain.split(".")[0].title()

        author = self._format_author_ieee(author)

        # Format date (IEEE uses DD-Mon.-YYYY)
        date_str = self._format_date_ieee(date)

        # Determine source name
        if not source and url:
            source = self._extract_source_name(url)

        # Build IEEE reference
        parts = [f"[{num}]"]

        if author:
            parts.append(f"{author},")

        parts.append(f'"{title},"')

        if source:
            parts.append(f"{source},")

        if date_str:
            parts.append(f"{date_str}.")

        # Add online availability
        if url:
            parts.append("[Online]. Available:")
            parts.append(url)
        elif doi:
            parts.append(f"doi: {doi}")

        return " ".join(parts)

    def _format_author_ieee(self, author: str) -> str:
        """Format author name(s) in IEEE style (F. Lastname)."""
        if not author:
            return ""

        # Handle "et al." cases
        if "et al" in author.lower():
            return author

        # Handle multiple authors separated by comma or "and"
        authors = re.split(r",\s*|\s+and\s+", author)
        formatted = []

        for a in authors:
            a = a.strip()
            if not a:
                continue

            parts = a.split()
            if len(parts) >= 2:
                # First initial(s), Last name
                initials = ". ".join([p[0].upper() for p in parts[:-1]]) + "."
                lastname = parts[-1]
                formatted.append(f"{initials} {lastname}")
            else:
                formatted.append(a)

        if len(formatted) > 3:
            return f"{formatted[0]} et al."
        elif len(formatted) == 2:
            return f"{formatted[0]} and {formatted[1]}"
        elif len(formatted) > 2:
            return ", ".join(formatted[:-1]) + f", and {formatted[-1]}"
        elif formatted:
            return formatted[0]
        return author

    def _format_date_ieee(self, date: str) -> str:
        """Format date in IEEE style (DD-Mon.-YYYY or Mon. YYYY)."""
        if not date:
            return ""

        try:
            # Try ISO format
            dt = datetime.fromisoformat(date.replace("Z", "+00:00"))
            return dt.strftime("%d-%b.-%Y")
        except ValueError:
            pass

        try:
            # Try common formats
            for fmt in ["%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%Y/%m/%d"]:
                try:
                    dt = datetime.strptime(date, fmt)
                    return dt.strftime("%d-%b.-%Y")
                except ValueError:
                    continue
        except Exception:
            pass

        # Return as-is if parsing fails
        return date

    def _extract_source_name(self, url: str) -> str:
        """Extract a readable source name from URL."""
        domain = urlparse(url).netloc.replace("www.", "")

        # Known source mappings
        source_map = {
            "nature.com": "Nature",
            "science.org": "Science",
            "ieee.org": "IEEE",
            "acm.org": "ACM",
            "arxiv.org": "arXiv",
            "github.com": "GitHub",
            "medium.com": "Medium",
            "aws.amazon.com": "AWS",
            "cloud.google.com": "Google Cloud",
            "azure.microsoft.com": "Microsoft Azure",
            "docs.microsoft.com": "Microsoft Docs",
            "developer.mozilla.org": "MDN Web Docs",
            "stackoverflow.com": "Stack Overflow",
            "wikipedia.org": "Wikipedia",
        }

        for pattern, name in source_map.items():
            if pattern in domain:
                return name

        # Fallback: capitalize domain
        return domain.split(".")[0].title()

    def generate_references_markdown(self) -> str:
        """Generate the references section in markdown format."""
        if not self.citations:
            return ""

        lines = ["# References\n"]

        for cite in sorted(self.citations, key=lambda x: x.get("number", 0)):
            formatted = self.format_citation_ieee(cite)
            lines.append(formatted)
            lines.append("")

        return "\n".join(lines)

    def generate_bibtex(self) -> str:
        """Generate BibTeX format for use with Pandoc citeproc."""
        entries = []

        for cite in self.citations:
            num = cite.get("number", 0)
            title = cite.get("title", "Untitled")
            author = cite.get("author", "Unknown")
            url = cite.get("url", "")
            date = cite.get("date", "")
            doi = cite.get("doi", "")

            # Extract year
            year = ""
            if date:
                match = re.search(r"(\d{4})", date)
                if match:
                    year = match.group(1)

            entry_id = f"ref{num}"

            entry = f"""@misc{{{entry_id},
  author = {{{author}}},
  title = {{{title}}},
  year = {{{year}}},
  url = {{{url}}},
  note = {{Accessed: {datetime.now().strftime("%Y-%m-%d")}}}"""

            if doi:
                entry += f""",
  doi = {{{doi}}}"""

            entry += "\n}"
            entries.append(entry)

        return "\n\n".join(entries)

    def replace_inline_citations(
        self,
        content: str,
        citation_file: Optional[str] = None
    ) -> str:
        """
        Replace citation markers in text with IEEE-style numbers.

        Handles formats like:
        - [cite-1] -> [1]
        - [ref-url] -> [N]
        - Markdown links that are citations
        """
        if citation_file:
            # Load inline reference mappings
            try:
                data = json.loads(Path(citation_file).read_text(encoding="utf-8"))
                inline_refs = data.get("inline_refs", [])

                for ref in inline_refs:
                    cite_id = ref.get("cite_id", ref.get("id", ""))
                    url = ref.get("url", "")

                    # Find the citation number
                    num = self.citation_map.get(cite_id) or self.citation_map.get(url)

                    if num:
                        # Replace various marker formats
                        patterns = [
                            rf"\[{re.escape(cite_id)}\]",
                            rf"\[cite:{re.escape(cite_id)}\]",
                        ]
                        for pattern in patterns:
                            content = re.sub(pattern, f"[{num}]", content)

            except (json.JSONDecodeError, IOError, FileNotFoundError):
                pass

        return content

    def get_citation_stats(self) -> dict:
        """Return statistics about loaded citations."""
        return {
            "total": len(self.citations),
            "with_author": sum(1 for c in self.citations if c.get("author")),
            "with_doi": sum(1 for c in self.citations if c.get("doi")),
            "with_date": sum(1 for c in self.citations if c.get("date")),
            "sources": list(set(
                self._extract_source_name(c.get("url", ""))
                for c in self.citations if c.get("url")
            )),
        }


def main():
    parser = argparse.ArgumentParser(
        description="Format citations in IEEE style"
    )
    parser.add_argument(
        "--input-dir", "-i",
        help="Directory containing .citations.json files"
    )
    parser.add_argument(
        "--input-file", "-f",
        help="Single citation JSON file to process"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "bibtex", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show citation statistics"
    )

    args = parser.parse_args()

    if not args.input_dir and not args.input_file:
        parser.error("Either --input-dir or --input-file is required")

    formatter = IEEECitationFormatter()

    # Load citations
    if args.input_dir:
        count = formatter.load_citations_from_directory(args.input_dir)
        print(f"Loaded {count} citations from {args.input_dir}", file=sys.stderr)
    else:
        count = formatter.load_citations_from_file(args.input_file)
        print(f"Loaded {count} citations from {args.input_file}", file=sys.stderr)

    if args.stats:
        stats = formatter.get_citation_stats()
        print(f"\nCitation Statistics:", file=sys.stderr)
        print(f"  Total: {stats['total']}", file=sys.stderr)
        print(f"  With author: {stats['with_author']}", file=sys.stderr)
        print(f"  With DOI: {stats['with_doi']}", file=sys.stderr)
        print(f"  With date: {stats['with_date']}", file=sys.stderr)
        print(f"  Sources: {', '.join(stats['sources'][:10])}", file=sys.stderr)

    # Generate output
    if args.format == "markdown":
        output = formatter.generate_references_markdown()
    elif args.format == "bibtex":
        output = formatter.generate_bibtex()
    else:
        output = json.dumps(formatter.citations, indent=2, ensure_ascii=False)

    # Write output
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
