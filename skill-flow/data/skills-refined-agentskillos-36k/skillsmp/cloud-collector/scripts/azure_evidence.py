"""
Azure Evidence Collector

Collects compliance evidence from Microsoft Azure.
"""

import logging
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.security import SecurityCenter
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError, HttpResponseError

from .output_formatter import EvidencePackage, EvidenceItem, ControlMapping

logger = logging.getLogger(__name__)


class AzureEvidenceCollector:
    """Collects compliance evidence from Azure."""
    
    # Control mappings for Azure evidence
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
            "cis": ["5.1", "5.2", "5.3"],
        },
        "storage": {
            "soc2": ["CC6.1", "CC6.7"],
            "iso27001": ["A.8.2.3", "A.13.2.1"],
            "nist800-53": ["AC-3", "SC-28"],
            "cis": ["3.1", "3.2", "3.3"],
        },
        "security": {
            "soc2": ["CC7.1", "CC7.2"],
            "iso27001": ["A.12.6.1", "A.18.2.3"],
            "nist800-53": ["SI-4", "RA-5"],
            "cis": ["2.1", "2.2"],
        },
        "encryption": {
            "soc2": ["CC6.1", "CC6.7"],
            "iso27001": ["A.10.1.1", "A.10.1.2"],
            "nist800-53": ["SC-12", "SC-13"],
            "cis": ["8.1", "8.2"],
        },
        "network": {
            "soc2": ["CC6.6", "CC6.7"],
            "iso27001": ["A.13.1.1", "A.13.1.3"],
            "nist800-53": ["SC-7", "AC-4"],
            "cis": ["6.1", "6.2", "6.3"],
        },
    }
    
    def __init__(self, subscription_id: str, credential: Any = None):
        """Initialize Azure collector.
        
        Args:
            subscription_id: Azure subscription ID.
            credential: Azure credential. Defaults to DefaultAzureCredential.
        """
        self.subscription_id = subscription_id
        self.credential = credential or DefaultAzureCredential()
    
    def _create_package(self) -> EvidencePackage:
        """Create a new evidence package."""
        return EvidencePackage(
            cloud_provider="azure",
            account_id=self.subscription_id,
        )
    
    def collect_all(self) -> EvidencePackage:
        """Collect all evidence categories."""
        package = self._create_package()
        
        collectors = [
            ("iam", self.collect_rbac),
            ("logging", self.collect_activity_logs),
            ("storage", self.collect_storage),
            ("security", self.collect_defender),
            ("encryption", self.collect_keyvault),
            ("network", self.collect_network),
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
                    id=f"azure-{category}-error",
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
    
    def collect_rbac(self) -> list[EvidenceItem]:
        """Collect RBAC evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            auth_client = AuthorizationManagementClient(
                self.credential, self.subscription_id
            )
            
            # Role assignments
            assignments_data = []
            for assignment in auth_client.role_assignments.list_for_subscription():
                assignments_data.append({
                    "id": assignment.id,
                    "name": assignment.name,
                    "principal_id": assignment.principal_id,
                    "principal_type": assignment.principal_type,
                    "role_definition_id": assignment.role_definition_id,
                    "scope": assignment.scope,
                    "created_on": assignment.created_on.isoformat() if assignment.created_on else None,
                })
            
            evidence.append(EvidenceItem(
                id="azure-rbac-assignments",
                category="iam",
                title="Role Assignments",
                description=f"List of {len(assignments_data)} role assignments",
                data={"assignments": assignments_data, "total_count": len(assignments_data)},
                controls=["CC6.1", "CC6.2", "A.9.2.1", "AC-2"],
            ))
            
            # Role definitions (custom roles)
            custom_roles_data = []
            for role in auth_client.role_definitions.list(scope=f"/subscriptions/{self.subscription_id}"):
                if role.role_type == "CustomRole":
                    custom_roles_data.append({
                        "id": role.id,
                        "name": role.role_name,
                        "description": role.description,
                        "permissions": [
                            {
                                "actions": list(p.actions) if p.actions else [],
                                "not_actions": list(p.not_actions) if p.not_actions else [],
                                "data_actions": list(p.data_actions) if p.data_actions else [],
                                "not_data_actions": list(p.not_data_actions) if p.not_data_actions else [],
                            }
                            for p in role.permissions
                        ] if role.permissions else [],
                        "assignable_scopes": list(role.assignable_scopes) if role.assignable_scopes else [],
                    })
            
            evidence.append(EvidenceItem(
                id="azure-rbac-custom-roles",
                category="iam",
                title="Custom Role Definitions",
                description=f"List of {len(custom_roles_data)} custom roles",
                data={"custom_roles": custom_roles_data, "total_count": len(custom_roles_data)},
                controls=["CC6.1", "CC6.3", "A.9.2.3", "AC-3"],
            ))
            
            # Check for risky assignments (Owner/Contributor at subscription level)
            risky_assignments = []
            for assignment in assignments_data:
                role_name = assignment["role_definition_id"].split("/")[-1].lower()
                if assignment["scope"] == f"/subscriptions/{self.subscription_id}":
                    if "owner" in role_name or "contributor" in role_name:
                        risky_assignments.append(assignment)
            
            if risky_assignments:
                evidence.append(EvidenceItem(
                    id="azure-rbac-risky-assignments",
                    category="iam",
                    title="High-Privilege Role Assignments",
                    description=f"Found {len(risky_assignments)} Owner/Contributor assignments at subscription scope",
                    data={"risky_assignments": risky_assignments},
                    controls=["CC6.1", "A.9.2.3", "AC-6"],
                ))
                
        except (AzureError, HttpResponseError) as e:
            logger.warning(f"Failed to collect RBAC evidence: {e}")
        
        return evidence
    
    def collect_activity_logs(self) -> list[EvidenceItem]:
        """Collect Activity Log configuration evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            monitor_client = MonitorManagementClient(
                self.credential, self.subscription_id
            )
            
            # Diagnostic settings for subscription
            diagnostic_settings_data = []
            try:
                for setting in monitor_client.subscription_diagnostic_settings.list(
                    subscription_id=self.subscription_id
                ):
                    diagnostic_settings_data.append({
                        "name": setting.name,
                        "storage_account_id": setting.storage_account_id,
                        "event_hub_authorization_rule_id": setting.event_hub_authorization_rule_id,
                        "workspace_id": setting.workspace_id,
                        "logs": [
                            {
                                "category": log.category,
                                "enabled": log.enabled,
                                "retention_days": log.retention_policy.days if log.retention_policy else None,
                            }
                            for log in setting.logs
                        ] if setting.logs else [],
                    })
            except HttpResponseError:
                pass
            
            evidence.append(EvidenceItem(
                id="azure-logging-diagnostic-settings",
                category="logging",
                title="Activity Log Diagnostic Settings",
                description=f"Configuration of {len(diagnostic_settings_data)} diagnostic settings",
                data={"diagnostic_settings": diagnostic_settings_data, "total_count": len(diagnostic_settings_data)},
                controls=["CC7.2", "A.12.4.1", "AU-6", "AU-12"],
            ))
            
            # Log profiles (classic activity log export)
            log_profiles_data = []
            try:
                for profile in monitor_client.log_profiles.list():
                    log_profiles_data.append({
                        "name": profile.name,
                        "storage_account_id": profile.storage_account_id,
                        "service_bus_rule_id": profile.service_bus_rule_id,
                        "locations": list(profile.locations) if profile.locations else [],
                        "categories": list(profile.categories) if profile.categories else [],
                        "retention_days": profile.retention_policy.days if profile.retention_policy else None,
                        "retention_enabled": profile.retention_policy.enabled if profile.retention_policy else False,
                    })
            except HttpResponseError:
                pass
            
            evidence.append(EvidenceItem(
                id="azure-logging-profiles",
                category="logging",
                title="Activity Log Profiles",
                description=f"Configuration of {len(log_profiles_data)} log profiles",
                data={"log_profiles": log_profiles_data, "total_count": len(log_profiles_data)},
                controls=["CC7.2", "A.12.4.2", "AU-2"],
            ))
            
        except (AzureError, HttpResponseError) as e:
            logger.warning(f"Failed to collect activity log evidence: {e}")
        
        return evidence
    
    def collect_storage(self) -> list[EvidenceItem]:
        """Collect Storage Account evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            storage_client = StorageManagementClient(
                self.credential, self.subscription_id
            )
            
            accounts_data = []
            for account in storage_client.storage_accounts.list():
                account_detail = {
                    "name": account.name,
                    "id": account.id,
                    "location": account.location,
                    "sku": account.sku.name if account.sku else None,
                    "kind": account.kind,
                    "creation_time": account.creation_time.isoformat() if account.creation_time else None,
                    "https_only": account.enable_https_traffic_only,
                    "minimum_tls_version": account.minimum_tls_version,
                    "allow_blob_public_access": account.allow_blob_public_access,
                    "network_rule_set": {
                        "default_action": account.network_rule_set.default_action if account.network_rule_set else None,
                        "bypass": account.network_rule_set.bypass if account.network_rule_set else None,
                        "ip_rules_count": len(account.network_rule_set.ip_rules) if account.network_rule_set and account.network_rule_set.ip_rules else 0,
                        "virtual_network_rules_count": len(account.network_rule_set.virtual_network_rules) if account.network_rule_set and account.network_rule_set.virtual_network_rules else 0,
                    } if account.network_rule_set else None,
                    "encryption": {
                        "key_source": account.encryption.key_source if account.encryption else None,
                        "services": {
                            "blob": account.encryption.services.blob.enabled if account.encryption and account.encryption.services and account.encryption.services.blob else None,
                            "file": account.encryption.services.file.enabled if account.encryption and account.encryption.services and account.encryption.services.file else None,
                        } if account.encryption and account.encryption.services else None,
                    } if account.encryption else None,
                }
                accounts_data.append(account_detail)
            
            # Check for risky configurations
            risky_accounts = [
                a for a in accounts_data 
                if a.get("allow_blob_public_access") or not a.get("https_only")
            ]
            
            evidence.append(EvidenceItem(
                id="azure-storage-accounts",
                category="storage",
                title="Storage Account Configuration",
                description=f"Security configuration of {len(accounts_data)} storage accounts ({len(risky_accounts)} with potential issues)",
                data={
                    "accounts": accounts_data,
                    "total_count": len(accounts_data),
                    "risky_count": len(risky_accounts),
                },
                controls=["CC6.1", "CC6.7", "A.8.2.3", "SC-28"],
            ))
            
        except (AzureError, HttpResponseError) as e:
            logger.warning(f"Failed to collect storage evidence: {e}")
        
        return evidence
    
    def collect_defender(self) -> list[EvidenceItem]:
        """Collect Microsoft Defender for Cloud evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            security_client = SecurityCenter(
                self.credential, self.subscription_id, ""
            )
            
            # Security contacts
            contacts_data = []
            try:
                for contact in security_client.security_contacts.list():
                    contacts_data.append({
                        "name": contact.name,
                        "email": contact.email,
                        "phone": contact.phone,
                        "alert_notifications": contact.alert_notifications,
                        "alerts_to_admins": contact.alerts_to_admins,
                    })
            except HttpResponseError:
                pass
            
            evidence.append(EvidenceItem(
                id="azure-defender-contacts",
                category="security",
                title="Security Contacts",
                description=f"Configuration of {len(contacts_data)} security contacts",
                data={"contacts": contacts_data, "total_count": len(contacts_data)},
                controls=["CC7.2", "A.16.1.1", "IR-6"],
            ))
            
            # Secure score
            try:
                secure_scores = list(security_client.secure_scores.list())
                if secure_scores:
                    score = secure_scores[0]
                    evidence.append(EvidenceItem(
                        id="azure-defender-secure-score",
                        category="security",
                        title="Secure Score",
                        description=f"Current secure score: {score.current if hasattr(score, 'current') else 'N/A'}",
                        data={
                            "current": score.current if hasattr(score, 'current') else None,
                            "max": score.max if hasattr(score, 'max') else None,
                            "percentage": score.percentage if hasattr(score, 'percentage') else None,
                        },
                        controls=["CC7.1", "A.18.2.3", "RA-5"],
                    ))
            except HttpResponseError:
                pass
            
            # Pricing (which Defender plans are enabled)
            pricing_data = []
            try:
                for pricing in security_client.pricings.list().value:
                    pricing_data.append({
                        "name": pricing.name,
                        "pricing_tier": pricing.pricing_tier,
                        "free_trial_remaining_time": str(pricing.free_trial_remaining_time) if hasattr(pricing, 'free_trial_remaining_time') and pricing.free_trial_remaining_time else None,
                    })
            except HttpResponseError:
                pass
            
            evidence.append(EvidenceItem(
                id="azure-defender-pricing",
                category="security",
                title="Defender Plans",
                description=f"Configuration of {len(pricing_data)} Defender plans",
                data={"plans": pricing_data, "total_count": len(pricing_data)},
                controls=["CC7.1", "A.12.6.1", "SI-4"],
            ))
            
            # Alerts summary
            alerts_summary = {"high": 0, "medium": 0, "low": 0}
            try:
                for alert in security_client.alerts.list():
                    severity = alert.severity.lower() if alert.severity else "low"
                    if severity in alerts_summary:
                        alerts_summary[severity] += 1
            except HttpResponseError:
                pass
            
            evidence.append(EvidenceItem(
                id="azure-defender-alerts",
                category="security",
                title="Security Alerts Summary",
                description=f"Active alerts: {alerts_summary['high']} high, {alerts_summary['medium']} medium, {alerts_summary['low']} low",
                data=alerts_summary,
                controls=["CC7.1", "CC7.2", "A.12.6.1", "SI-4"],
            ))
            
        except (AzureError, HttpResponseError) as e:
            logger.warning(f"Failed to collect Defender evidence: {e}")
        
        return evidence
    
    def collect_keyvault(self) -> list[EvidenceItem]:
        """Collect Key Vault evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            kv_client = KeyVaultManagementClient(
                self.credential, self.subscription_id
            )
            
            vaults_data = []
            for vault in kv_client.vaults.list():
                # Get full vault details
                try:
                    rg_name = vault.id.split("/")[4]  # Extract resource group from ID
                    vault_detail = kv_client.vaults.get(rg_name, vault.name)
                    
                    vaults_data.append({
                        "name": vault.name,
                        "id": vault.id,
                        "location": vault.location,
                        "sku": vault_detail.properties.sku.name if vault_detail.properties.sku else None,
                        "tenant_id": str(vault_detail.properties.tenant_id) if vault_detail.properties.tenant_id else None,
                        "enabled_for_deployment": vault_detail.properties.enabled_for_deployment,
                        "enabled_for_disk_encryption": vault_detail.properties.enabled_for_disk_encryption,
                        "enabled_for_template_deployment": vault_detail.properties.enabled_for_template_deployment,
                        "enable_soft_delete": vault_detail.properties.enable_soft_delete,
                        "soft_delete_retention_days": vault_detail.properties.soft_delete_retention_in_days,
                        "enable_purge_protection": vault_detail.properties.enable_purge_protection,
                        "enable_rbac_authorization": vault_detail.properties.enable_rbac_authorization,
                        "network_acls": {
                            "default_action": vault_detail.properties.network_acls.default_action if vault_detail.properties.network_acls else None,
                            "bypass": vault_detail.properties.network_acls.bypass if vault_detail.properties.network_acls else None,
                        } if vault_detail.properties.network_acls else None,
                        "access_policies_count": len(vault_detail.properties.access_policies) if vault_detail.properties.access_policies else 0,
                    })
                except HttpResponseError:
                    vaults_data.append({
                        "name": vault.name,
                        "id": vault.id,
                        "location": vault.location,
                    })
            
            # Check for missing protection
            unprotected_vaults = [
                v for v in vaults_data 
                if not v.get("enable_purge_protection") or not v.get("enable_soft_delete")
            ]
            
            evidence.append(EvidenceItem(
                id="azure-keyvault-vaults",
                category="encryption",
                title="Key Vault Configuration",
                description=f"Configuration of {len(vaults_data)} Key Vaults ({len(unprotected_vaults)} without full protection)",
                data={
                    "vaults": vaults_data,
                    "total_count": len(vaults_data),
                    "unprotected_count": len(unprotected_vaults),
                },
                controls=["CC6.1", "A.10.1.2", "SC-12", "SC-13"],
            ))
            
        except (AzureError, HttpResponseError) as e:
            logger.warning(f"Failed to collect Key Vault evidence: {e}")
        
        return evidence
    
    def collect_network(self) -> list[EvidenceItem]:
        """Collect network security evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            network_client = NetworkManagementClient(
                self.credential, self.subscription_id
            )
            
            # Virtual Networks
            vnets_data = []
            for vnet in network_client.virtual_networks.list_all():
                vnets_data.append({
                    "name": vnet.name,
                    "id": vnet.id,
                    "location": vnet.location,
                    "address_space": list(vnet.address_space.address_prefixes) if vnet.address_space and vnet.address_space.address_prefixes else [],
                    "subnets_count": len(vnet.subnets) if vnet.subnets else 0,
                    "enable_ddos_protection": vnet.enable_ddos_protection,
                    "enable_vm_protection": vnet.enable_vm_protection,
                })
            
            evidence.append(EvidenceItem(
                id="azure-network-vnets",
                category="network",
                title="Virtual Networks",
                description=f"Configuration of {len(vnets_data)} Virtual Networks",
                data={"vnets": vnets_data, "total_count": len(vnets_data)},
                controls=["CC6.6", "A.13.1.1", "SC-7"],
            ))
            
            # Network Security Groups
            nsgs_data = []
            for nsg in network_client.network_security_groups.list_all():
                # Analyze rules for risky configurations
                risky_rules = []
                if nsg.security_rules:
                    for rule in nsg.security_rules:
                        if rule.access == "Allow" and rule.direction == "Inbound":
                            if rule.source_address_prefix in ["*", "0.0.0.0/0", "Internet"]:
                                risky_rules.append({
                                    "name": rule.name,
                                    "destination_port_range": rule.destination_port_range,
                                    "protocol": rule.protocol,
                                    "source": rule.source_address_prefix,
                                })
                
                nsgs_data.append({
                    "name": nsg.name,
                    "id": nsg.id,
                    "location": nsg.location,
                    "security_rules_count": len(nsg.security_rules) if nsg.security_rules else 0,
                    "default_rules_count": len(nsg.default_security_rules) if nsg.default_security_rules else 0,
                    "subnets_count": len(nsg.subnets) if nsg.subnets else 0,
                    "network_interfaces_count": len(nsg.network_interfaces) if nsg.network_interfaces else 0,
                    "risky_rules": risky_rules,
                })
            
            risky_nsg_count = sum(1 for n in nsgs_data if n["risky_rules"])
            evidence.append(EvidenceItem(
                id="azure-network-nsgs",
                category="network",
                title="Network Security Groups",
                description=f"Configuration of {len(nsgs_data)} NSGs ({risky_nsg_count} with potentially risky rules)",
                data={
                    "nsgs": nsgs_data,
                    "total_count": len(nsgs_data),
                    "risky_count": risky_nsg_count,
                },
                controls=["CC6.6", "A.13.1.1", "SC-7", "AC-4"],
            ))
            
            # Application Security Groups
            asgs_data = []
            for asg in network_client.application_security_groups.list_all():
                asgs_data.append({
                    "name": asg.name,
                    "id": asg.id,
                    "location": asg.location,
                })
            
            evidence.append(EvidenceItem(
                id="azure-network-asgs",
                category="network",
                title="Application Security Groups",
                description=f"List of {len(asgs_data)} Application Security Groups",
                data={"asgs": asgs_data, "total_count": len(asgs_data)},
                controls=["CC6.6", "A.13.1.3", "SC-7"],
            ))
            
            # Network Watchers (for flow logs)
            watchers_data = []
            for watcher in network_client.network_watchers.list_all():
                watchers_data.append({
                    "name": watcher.name,
                    "id": watcher.id,
                    "location": watcher.location,
                    "provisioning_state": watcher.provisioning_state,
                })
            
            evidence.append(EvidenceItem(
                id="azure-network-watchers",
                category="network",
                title="Network Watchers",
                description=f"Configuration of {len(watchers_data)} Network Watchers",
                data={"watchers": watchers_data, "total_count": len(watchers_data)},
                controls=["CC7.2", "A.12.4.1", "AU-12"],
            ))
            
        except (AzureError, HttpResponseError) as e:
            logger.warning(f"Failed to collect network evidence: {e}")
        
        return evidence
