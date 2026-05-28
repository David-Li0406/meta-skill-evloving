"""
GCP Evidence Collector

Collects compliance evidence from Google Cloud Platform.
"""

import logging
from typing import Any

from google.cloud import storage
from google.cloud import kms_v1
from google.cloud import compute_v1
from google.cloud import securitycenter_v1
from google.cloud.logging_v2 import Client as LoggingClient
from google.cloud import resourcemanager_v3
from google.api_core.exceptions import GoogleAPIError, PermissionDenied, NotFound
from google.auth import default as get_default_credentials
from google.auth.exceptions import DefaultCredentialsError

from .output_formatter import EvidencePackage, EvidenceItem, ControlMapping

logger = logging.getLogger(__name__)


class GCPEvidenceCollector:
    """Collects compliance evidence from GCP."""
    
    # Control mappings for GCP evidence
    CONTROL_MAPPINGS = {
        "iam": {
            "soc2": ["CC6.1", "CC6.2", "CC6.3"],
            "iso27001": ["A.9.2.1", "A.9.2.2", "A.9.2.3"],
            "nist800-53": ["AC-2", "AC-3", "AC-6"],
            "cis": ["1.1", "1.2", "1.3"],
        },
        "logging": {
            "soc2": ["CC7.2", "CC7.3"],
            "iso27001": ["A.12.4.1", "A.12.4.2", "A.12.4.3"],
            "nist800-53": ["AU-2", "AU-3", "AU-6", "AU-12"],
            "cis": ["2.1", "2.2", "2.3"],
        },
        "storage": {
            "soc2": ["CC6.1", "CC6.7"],
            "iso27001": ["A.8.2.3", "A.13.2.1"],
            "nist800-53": ["AC-3", "SC-28"],
            "cis": ["5.1", "5.2"],
        },
        "security": {
            "soc2": ["CC7.1", "CC7.2"],
            "iso27001": ["A.12.6.1", "A.18.2.3"],
            "nist800-53": ["SI-4", "RA-5"],
            "cis": ["7.1", "7.2"],
        },
        "encryption": {
            "soc2": ["CC6.1", "CC6.7"],
            "iso27001": ["A.10.1.1", "A.10.1.2"],
            "nist800-53": ["SC-12", "SC-13"],
            "cis": ["1.9", "1.10"],
        },
        "network": {
            "soc2": ["CC6.6", "CC6.7"],
            "iso27001": ["A.13.1.1", "A.13.1.3"],
            "nist800-53": ["SC-7", "AC-4"],
            "cis": ["3.1", "3.2", "3.3"],
        },
    }
    
    def __init__(self, project_id: str | None = None):
        """Initialize GCP collector.
        
        Args:
            project_id: GCP project ID. Will attempt to detect from credentials if not provided.
        """
        self.project_id = project_id
        
        if not self.project_id:
            try:
                _, self.project_id = get_default_credentials()
            except DefaultCredentialsError:
                pass
        
        if not self.project_id:
            raise ValueError("project_id must be provided or available from default credentials")
    
    def _create_package(self) -> EvidencePackage:
        """Create a new evidence package."""
        return EvidencePackage(
            cloud_provider="gcp",
            account_id=self.project_id,
        )
    
    def collect_all(self) -> EvidencePackage:
        """Collect all evidence categories."""
        package = self._create_package()
        
        collectors = [
            ("iam", self.collect_iam),
            ("logging", self.collect_audit_logs),
            ("storage", self.collect_gcs),
            ("security", self.collect_security_center),
            ("encryption", self.collect_kms),
            ("network", self.collect_vpc),
        ]
        
        for category, collector in collectors:
            try:
                evidence_items = collector()
                for item in evidence_items:
                    package.add_evidence(item)
                logger.info(f"Collected {len(evidence_items)} {category} evidence items")
            except Exception as e:
                logger.warning(f"Failed to collect {category} evidence: {e}")
                package.add_evidence(EvidenceItem(
                    id=f"gcp-{category}-error",
                    category=category,
                    title=f"{category.upper()} Collection Error",
                    description=f"Failed to collect {category} evidence",
                    data={"error": str(e)},
                ))
        
        # Add control mappings
        self._add_control_mappings(package)
        
        return package
    
    def _add_control_mappings(self, package: EvidencePackage) -> None:
        """Add control mappings based on collected evidence."""
        evidence_by_category: dict[str, list[str]] = {}
        for item in package.evidence:
            evidence_by_category.setdefault(item.category, []).append(item.id)
        
        for category, evidence_ids in evidence_by_category.items():
            if category not in self.CONTROL_MAPPINGS:
                continue
                
            for framework, controls in self.CONTROL_MAPPINGS[category].items():
                for control_id in controls:
                    package.add_control_mapping(ControlMapping(
                        framework=framework,
                        control_id=control_id,
                        control_name=f"{framework.upper()} {control_id}",
                        evidence_ids=evidence_ids,
                        status="collected" if evidence_ids else "missing",
                    ))
    
    def collect_iam(self) -> list[EvidenceItem]:
        """Collect IAM evidence."""
        evidence: list[EvidenceItem] = []
        
        # Get project IAM policy
        try:
            client = resourcemanager_v3.ProjectsClient()
            project_name = f"projects/{self.project_id}"
            
            policy = client.get_iam_policy(resource=project_name)
            
            bindings_data = []
            for binding in policy.bindings:
                bindings_data.append({
                    "role": binding.role,
                    "members": list(binding.members),
                    "condition": {
                        "expression": binding.condition.expression,
                        "title": binding.condition.title,
                    } if binding.condition.expression else None,
                })
            
            evidence.append(EvidenceItem(
                id="gcp-iam-project-policy",
                category="iam",
                title="Project IAM Policy",
                description=f"IAM policy with {len(bindings_data)} role bindings",
                data={"bindings": bindings_data, "total_bindings": len(bindings_data)},
                controls=["CC6.1", "CC6.2", "A.9.2.1", "AC-2"],
            ))
            
            # Analyze for risky bindings
            risky_bindings = []
            for binding in bindings_data:
                for member in binding.get("members", []):
                    if member == "allUsers" or member == "allAuthenticatedUsers":
                        risky_bindings.append({
                            "role": binding["role"],
                            "member": member,
                        })
            
            if risky_bindings:
                evidence.append(EvidenceItem(
                    id="gcp-iam-risky-bindings",
                    category="iam",
                    title="Risky IAM Bindings",
                    description=f"Found {len(risky_bindings)} public or all-authenticated-users bindings",
                    data={"risky_bindings": risky_bindings},
                    controls=["CC6.1", "A.9.2.3", "AC-3"],
                ))
                
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to get project IAM policy: {e}")
        
        return evidence
    
    def collect_audit_logs(self) -> list[EvidenceItem]:
        """Collect audit log configuration evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            client = LoggingClient(project=self.project_id)
            
            # List log sinks
            sinks_data = []
            for sink in client.list_sinks():
                sinks_data.append({
                    "name": sink.name,
                    "destination": sink.destination,
                    "filter": sink.filter_,
                    "disabled": sink.disabled if hasattr(sink, 'disabled') else False,
                })
            
            evidence.append(EvidenceItem(
                id="gcp-logging-sinks",
                category="logging",
                title="Log Sinks Configuration",
                description=f"Configuration of {len(sinks_data)} log sinks",
                data={"sinks": sinks_data, "total_count": len(sinks_data)},
                controls=["CC7.2", "A.12.4.1", "AU-6"],
            ))
            
            # List log metrics (for alerting)
            metrics_data = []
            for metric in client.list_metrics():
                metrics_data.append({
                    "name": metric.name,
                    "filter": metric.filter_,
                    "description": metric.description,
                })
            
            evidence.append(EvidenceItem(
                id="gcp-logging-metrics",
                category="logging",
                title="Log-Based Metrics",
                description=f"Configuration of {len(metrics_data)} log-based metrics",
                data={"metrics": metrics_data, "total_count": len(metrics_data)},
                controls=["CC7.2", "CC7.3", "A.12.4.3", "AU-12"],
            ))
            
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to collect audit log evidence: {e}")
        
        return evidence
    
    def collect_gcs(self) -> list[EvidenceItem]:
        """Collect GCS bucket evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            client = storage.Client(project=self.project_id)
            
            buckets_data = []
            for bucket in client.list_buckets():
                bucket_detail = {
                    "name": bucket.name,
                    "location": bucket.location,
                    "storage_class": bucket.storage_class,
                    "versioning_enabled": bucket.versioning_enabled,
                    "uniform_bucket_level_access": bucket.iam_configuration.uniform_bucket_level_access_enabled,
                    "public_access_prevention": bucket.iam_configuration.public_access_prevention,
                    "default_kms_key": bucket.default_kms_key_name,
                    "retention_policy": {
                        "retention_period": bucket.retention_period,
                        "is_locked": bucket.retention_policy_locked,
                    } if bucket.retention_period else None,
                    "logging": {
                        "log_bucket": bucket.logging.bucket,
                        "log_prefix": bucket.logging.prefix,
                    } if bucket.logging else None,
                }
                
                # Check IAM policy for public access
                try:
                    policy = bucket.get_iam_policy()
                    public_access = False
                    for binding in policy.bindings:
                        if "allUsers" in binding["members"] or "allAuthenticatedUsers" in binding["members"]:
                            public_access = True
                            break
                    bucket_detail["has_public_iam"] = public_access
                except (GoogleAPIError, PermissionDenied):
                    bucket_detail["has_public_iam"] = "access_denied"
                
                buckets_data.append(bucket_detail)
            
            evidence.append(EvidenceItem(
                id="gcp-gcs-buckets",
                category="storage",
                title="GCS Bucket Configuration",
                description=f"Security configuration of {len(buckets_data)} GCS buckets",
                data={"buckets": buckets_data, "total_count": len(buckets_data)},
                controls=["CC6.1", "CC6.7", "A.8.2.3", "SC-28"],
            ))
            
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to collect GCS evidence: {e}")
        
        return evidence
    
    def collect_security_center(self) -> list[EvidenceItem]:
        """Collect Security Command Center evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            client = securitycenter_v1.SecurityCenterClient()
            
            # List sources
            org_name = f"projects/{self.project_id}"
            
            # Get findings summary
            findings_data = []
            try:
                request = securitycenter_v1.ListFindingsRequest(
                    parent=f"{org_name}/sources/-",
                    filter='state="ACTIVE" AND (severity="HIGH" OR severity="CRITICAL")',
                    page_size=100,
                )
                
                findings_count = {"CRITICAL": 0, "HIGH": 0}
                for finding_result in client.list_findings(request=request):
                    severity = securitycenter_v1.Finding.Severity(finding_result.finding.severity).name
                    if severity in findings_count:
                        findings_count[severity] += 1
                    
                    if len(findings_data) < 20:  # Sample findings
                        findings_data.append({
                            "name": finding_result.finding.name,
                            "category": finding_result.finding.category,
                            "severity": severity,
                            "state": securitycenter_v1.Finding.State(finding_result.finding.state).name,
                            "resource": finding_result.finding.resource_name,
                        })
                
                evidence.append(EvidenceItem(
                    id="gcp-scc-findings",
                    category="security",
                    title="Security Command Center Findings",
                    description=f"High/Critical findings: {findings_count['CRITICAL']} critical, {findings_count['HIGH']} high",
                    data={
                        "summary": findings_count,
                        "sample_findings": findings_data,
                    },
                    controls=["CC7.1", "A.12.6.1", "SI-4", "RA-5"],
                ))
                
            except (GoogleAPIError, PermissionDenied, NotFound) as e:
                evidence.append(EvidenceItem(
                    id="gcp-scc-status",
                    category="security",
                    title="Security Command Center Status",
                    description="Security Command Center findings not accessible",
                    data={"accessible": False, "error": str(e)},
                    controls=["CC7.1", "A.12.6.1", "SI-4"],
                ))
                
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to collect SCC evidence: {e}")
        
        return evidence
    
    def collect_kms(self) -> list[EvidenceItem]:
        """Collect Cloud KMS evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            client = kms_v1.KeyManagementServiceClient()
            
            # List key rings and keys
            parent = f"projects/{self.project_id}/locations/global"
            
            keyrings_data = []
            try:
                for keyring in client.list_key_rings(parent=parent):
                    keyring_detail = {
                        "name": keyring.name,
                        "keys": [],
                    }
                    
                    # List keys in keyring
                    for key in client.list_crypto_keys(parent=keyring.name):
                        key_detail = {
                            "name": key.name,
                            "purpose": kms_v1.CryptoKey.CryptoKeyPurpose(key.purpose).name,
                            "create_time": key.create_time.isoformat() if key.create_time else None,
                            "rotation_period": str(key.rotation_period) if key.rotation_period else None,
                            "next_rotation_time": key.next_rotation_time.isoformat() if key.next_rotation_time else None,
                            "primary_state": kms_v1.CryptoKeyVersion.CryptoKeyVersionState(key.primary.state).name if key.primary else None,
                        }
                        keyring_detail["keys"].append(key_detail)
                    
                    keyrings_data.append(keyring_detail)
                    
            except (GoogleAPIError, PermissionDenied):
                pass
            
            # Also check other common locations
            for location in ["us", "us-east1", "us-west1", "europe-west1"]:
                try:
                    loc_parent = f"projects/{self.project_id}/locations/{location}"
                    for keyring in client.list_key_rings(parent=loc_parent):
                        keyring_detail = {
                            "name": keyring.name,
                            "location": location,
                            "keys": [],
                        }
                        
                        for key in client.list_crypto_keys(parent=keyring.name):
                            key_detail = {
                                "name": key.name,
                                "purpose": kms_v1.CryptoKey.CryptoKeyPurpose(key.purpose).name,
                                "rotation_period": str(key.rotation_period) if key.rotation_period else None,
                            }
                            keyring_detail["keys"].append(key_detail)
                        
                        keyrings_data.append(keyring_detail)
                except (GoogleAPIError, PermissionDenied):
                    continue
            
            total_keys = sum(len(kr["keys"]) for kr in keyrings_data)
            evidence.append(EvidenceItem(
                id="gcp-kms-keys",
                category="encryption",
                title="Cloud KMS Configuration",
                description=f"Configuration of {len(keyrings_data)} key rings with {total_keys} keys",
                data={"keyrings": keyrings_data, "total_keyrings": len(keyrings_data), "total_keys": total_keys},
                controls=["CC6.1", "A.10.1.2", "SC-12", "SC-13"],
            ))
            
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to collect KMS evidence: {e}")
        
        return evidence
    
    def collect_vpc(self) -> list[EvidenceItem]:
        """Collect VPC and network evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            # VPC Networks
            networks_client = compute_v1.NetworksClient()
            networks_data = []
            
            for network in networks_client.list(project=self.project_id):
                networks_data.append({
                    "name": network.name,
                    "auto_create_subnetworks": network.auto_create_subnetworks,
                    "routing_mode": network.routing_config.routing_mode if network.routing_config else None,
                    "mtu": network.mtu,
                    "subnetworks": list(network.subnetworks) if network.subnetworks else [],
                })
            
            evidence.append(EvidenceItem(
                id="gcp-vpc-networks",
                category="network",
                title="VPC Networks",
                description=f"Configuration of {len(networks_data)} VPC networks",
                data={"networks": networks_data, "total_count": len(networks_data)},
                controls=["CC6.6", "A.13.1.1", "SC-7"],
            ))
            
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to collect VPC networks: {e}")
        
        try:
            # Firewall rules
            firewalls_client = compute_v1.FirewallsClient()
            firewalls_data = []
            
            for fw in firewalls_client.list(project=self.project_id):
                # Check for overly permissive rules
                is_risky = False
                if fw.source_ranges and "0.0.0.0/0" in fw.source_ranges:
                    is_risky = True
                
                firewalls_data.append({
                    "name": fw.name,
                    "network": fw.network,
                    "direction": fw.direction,
                    "priority": fw.priority,
                    "source_ranges": list(fw.source_ranges) if fw.source_ranges else [],
                    "destination_ranges": list(fw.destination_ranges) if fw.destination_ranges else [],
                    "allowed": [
                        {"protocol": a.I_p_protocol, "ports": list(a.ports) if a.ports else []}
                        for a in fw.allowed
                    ] if fw.allowed else [],
                    "denied": [
                        {"protocol": d.I_p_protocol, "ports": list(d.ports) if d.ports else []}
                        for d in fw.denied
                    ] if fw.denied else [],
                    "disabled": fw.disabled,
                    "is_risky": is_risky,
                })
            
            risky_count = sum(1 for f in firewalls_data if f["is_risky"])
            evidence.append(EvidenceItem(
                id="gcp-vpc-firewalls",
                category="network",
                title="Firewall Rules",
                description=f"Configuration of {len(firewalls_data)} firewall rules ({risky_count} potentially risky)",
                data={"firewalls": firewalls_data, "total_count": len(firewalls_data), "risky_count": risky_count},
                controls=["CC6.6", "A.13.1.1", "SC-7", "AC-4"],
            ))
            
        except (GoogleAPIError, PermissionDenied) as e:
            logger.warning(f"Failed to collect firewall rules: {e}")
        
        return evidence
