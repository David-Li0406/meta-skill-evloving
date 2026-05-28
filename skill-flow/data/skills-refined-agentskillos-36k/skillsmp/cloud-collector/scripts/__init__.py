"""
Evidence Collector Scripts

Multi-cloud compliance evidence collection for SOC 2, ISO 27001, NIST, and CIS.
"""

from .aws_evidence import AWSEvidenceCollector
from .gcp_evidence import GCPEvidenceCollector
from .azure_evidence import AzureEvidenceCollector
from .output_formatter import EvidenceFormatter, EvidencePackage

__all__ = [
    "AWSEvidenceCollector",
    "GCPEvidenceCollector", 
    "AzureEvidenceCollector",
    "EvidenceFormatter",
    "EvidencePackage",
]
