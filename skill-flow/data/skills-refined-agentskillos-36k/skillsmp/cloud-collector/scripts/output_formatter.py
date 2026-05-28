"""
Evidence Output Formatter

Formats collected evidence into structured JSON and Markdown packages.
"""

import json
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any
from pathlib import Path


@dataclass
class EvidenceItem:
    """Single piece of compliance evidence."""
    
    id: str
    category: str  # iam, logging, storage, security, encryption, network
    title: str
    data: dict[str, Any]
    description: str = ""
    controls: list[str] = field(default_factory=list)


@dataclass
class ControlMapping:
    """Maps evidence to compliance controls."""
    
    framework: str  # soc2, iso27001, nist800-53, cis
    control_id: str
    control_name: str
    evidence_ids: list[str]
    status: str = "collected"  # collected, partial, missing


@dataclass
class EvidencePackage:
    """Complete evidence package for a cloud provider."""
    
    cloud_provider: str
    account_id: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    control_mappings: list[ControlMapping] = field(default_factory=list)
    region: str | None = None
    collector_version: str = "1.0.0"
    collection_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    
    def add_evidence(self, item: EvidenceItem) -> None:
        """Add an evidence item to the package."""
        self.evidence.append(item)
    
    def add_control_mapping(self, mapping: ControlMapping) -> None:
        """Add a control mapping."""
        self.control_mappings.append(mapping)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert package to dictionary."""
        return {
            "metadata": {
                "collection_timestamp": self.collection_timestamp,
                "cloud_provider": self.cloud_provider,
                "collector_version": self.collector_version,
                "account_id": self.account_id,
                "region": self.region,
            },
            "evidence": [asdict(e) for e in self.evidence],
            "control_mappings": [asdict(m) for m in self.control_mappings],
        }


class EvidenceFormatter:
    """Formats evidence packages for output."""
    
    @staticmethod
    def to_json(package: EvidencePackage, pretty: bool = True) -> str:
        """Format evidence package as JSON."""
        indent = 2 if pretty else None
        return json.dumps(package.to_dict(), indent=indent, default=str)
    
    @staticmethod
    def to_markdown(package: EvidencePackage) -> str:
        """Format evidence package as Markdown report."""
        lines = [
            f"# Compliance Evidence Report",
            f"",
            f"## Metadata",
            f"",
            f"| Field | Value |",
            f"|-------|-------|",
            f"| Cloud Provider | {package.cloud_provider.upper()} |",
            f"| Account/Project | {package.account_id} |",
            f"| Collection Time | {package.collection_timestamp} |",
            f"| Collector Version | {package.collector_version} |",
        ]
        
        if package.region:
            lines.append(f"| Region | {package.region} |")
        
        lines.extend(["", "---", "", "## Evidence Items", ""])
        
        # Group evidence by category
        by_category: dict[str, list[EvidenceItem]] = {}
        for item in package.evidence:
            by_category.setdefault(item.category, []).append(item)
        
        for category, items in sorted(by_category.items()):
            lines.append(f"### {category.upper()}")
            lines.append("")
            
            for item in items:
                lines.append(f"#### {item.title}")
                lines.append("")
                if item.description:
                    lines.append(f"{item.description}")
                    lines.append("")
                if item.controls:
                    lines.append(f"**Controls:** {', '.join(item.controls)}")
                    lines.append("")
                lines.append("```json")
                lines.append(json.dumps(item.data, indent=2, default=str))
                lines.append("```")
                lines.append("")
        
        # Control mappings summary
        if package.control_mappings:
            lines.extend(["---", "", "## Control Mappings", ""])
            
            # Group by framework
            by_framework: dict[str, list[ControlMapping]] = {}
            for mapping in package.control_mappings:
                by_framework.setdefault(mapping.framework, []).append(mapping)
            
            for framework, mappings in sorted(by_framework.items()):
                lines.append(f"### {framework.upper()}")
                lines.append("")
                lines.append("| Control ID | Control Name | Status | Evidence |")
                lines.append("|------------|--------------|--------|----------|")
                
                for m in sorted(mappings, key=lambda x: x.control_id):
                    evidence_list = ", ".join(m.evidence_ids) if m.evidence_ids else "None"
                    status_emoji = {"collected": "✅", "partial": "⚠️", "missing": "❌"}.get(m.status, "")
                    lines.append(f"| {m.control_id} | {m.control_name} | {status_emoji} {m.status} | {evidence_list} |")
                
                lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def save(package: EvidencePackage, output_dir: str | Path, formats: list[str] | None = None) -> dict[str, Path]:
        """Save evidence package to files.
        
        Args:
            package: Evidence package to save
            output_dir: Directory to save files
            formats: List of formats to save (json, markdown). Defaults to both.
            
        Returns:
            Dictionary mapping format to saved file path
        """
        if formats is None:
            formats = ["json", "markdown"]
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"evidence_{package.cloud_provider}_{timestamp}"
        
        saved: dict[str, Path] = {}
        
        if "json" in formats:
            json_path = output_path / f"{base_name}.json"
            json_path.write_text(EvidenceFormatter.to_json(package))
            saved["json"] = json_path
        
        if "markdown" in formats:
            md_path = output_path / f"{base_name}.md"
            md_path.write_text(EvidenceFormatter.to_markdown(package))
            saved["markdown"] = md_path
        
        return saved
