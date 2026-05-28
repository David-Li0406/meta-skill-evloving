"""
AWS Evidence Collector

Collects compliance evidence from AWS using boto3.
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from .output_formatter import EvidencePackage, EvidenceItem, ControlMapping

logger = logging.getLogger(__name__)


class AWSEvidenceCollector:
    """Collects compliance evidence from AWS."""
    
    # Control mappings for AWS evidence
    CONTROL_MAPPINGS = {
        "iam": {
            "soc2": ["CC6.1", "CC6.2", "CC6.3"],
            "iso27001": ["A.9.2.1", "A.9.2.2", "A.9.2.3"],
            "nist800-53": ["AC-2", "AC-3", "AC-6"],
            "cis": ["1.1", "1.2", "1.3", "1.4"],
        },
        "logging": {
            "soc2": ["CC7.2", "CC7.3"],
            "iso27001": ["A.12.4.1", "A.12.4.2", "A.12.4.3"],
            "nist800-53": ["AU-2", "AU-3", "AU-6", "AU-12"],
            "cis": ["3.1", "3.2", "3.3"],
        },
        "storage": {
            "soc2": ["CC6.1", "CC6.7"],
            "iso27001": ["A.8.2.3", "A.13.2.1"],
            "nist800-53": ["AC-3", "SC-28"],
            "cis": ["2.1.1", "2.1.2"],
        },
        "security": {
            "soc2": ["CC7.1", "CC7.2"],
            "iso27001": ["A.12.6.1", "A.18.2.3"],
            "nist800-53": ["SI-4", "RA-5"],
            "cis": ["4.1", "4.2"],
        },
        "encryption": {
            "soc2": ["CC6.1", "CC6.7"],
            "iso27001": ["A.10.1.1", "A.10.1.2"],
            "nist800-53": ["SC-12", "SC-13"],
            "cis": ["2.8", "2.9"],
        },
        "network": {
            "soc2": ["CC6.6", "CC6.7"],
            "iso27001": ["A.13.1.1", "A.13.1.3"],
            "nist800-53": ["SC-7", "AC-4"],
            "cis": ["5.1", "5.2", "5.3"],
        },
    }
    
    def __init__(self, region: str | None = None, profile: str | None = None):
        """Initialize AWS collector.
        
        Args:
            region: AWS region. Defaults to session default.
            profile: AWS profile name. Defaults to default profile.
        """
        session_kwargs: dict[str, Any] = {}
        if profile:
            session_kwargs["profile_name"] = profile
        if region:
            session_kwargs["region_name"] = region
            
        self.session = boto3.Session(**session_kwargs)
        self.region = region or self.session.region_name or "us-east-1"
        self._account_id: str | None = None
    
    @property
    def account_id(self) -> str:
        """Get AWS account ID."""
        if self._account_id is None:
            try:
                sts = self.session.client("sts")
                self._account_id = sts.get_caller_identity()["Account"]
            except (ClientError, NoCredentialsError) as e:
                logger.error(f"Failed to get account ID: {e}")
                self._account_id = "unknown"
        return self._account_id
    
    def _create_package(self) -> EvidencePackage:
        """Create a new evidence package."""
        return EvidencePackage(
            cloud_provider="aws",
            account_id=self.account_id,
            region=self.region,
        )
    
    def collect_all(self) -> EvidencePackage:
        """Collect all evidence categories."""
        package = self._create_package()
        
        collectors = [
            ("iam", self.collect_iam),
            ("logging", self.collect_cloudtrail),
            ("storage", self.collect_s3),
            ("security", self.collect_securityhub),
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
                    id=f"aws-{category}-error",
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
        iam = self.session.client("iam")
        
        # Password policy
        try:
            policy = iam.get_account_password_policy()["PasswordPolicy"]
            evidence.append(EvidenceItem(
                id="aws-iam-password-policy",
                category="iam",
                title="IAM Password Policy",
                description="Account-level password policy configuration",
                data=policy,
                controls=["CC6.1", "A.9.4.3", "IA-5"],
            ))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchEntity":
                evidence.append(EvidenceItem(
                    id="aws-iam-password-policy",
                    category="iam",
                    title="IAM Password Policy",
                    description="No password policy configured",
                    data={"configured": False},
                    controls=["CC6.1", "A.9.4.3", "IA-5"],
                ))
            else:
                raise
        
        # IAM users
        users_response = iam.list_users()
        users_data = []
        for user in users_response.get("Users", []):
            user_detail = {
                "UserName": user["UserName"],
                "UserId": user["UserId"],
                "CreateDate": user["CreateDate"].isoformat(),
                "PasswordLastUsed": user.get("PasswordLastUsed", "Never").isoformat() if isinstance(user.get("PasswordLastUsed"), datetime) else user.get("PasswordLastUsed", "Never"),
            }
            
            # Get MFA devices
            try:
                mfa_response = iam.list_mfa_devices(UserName=user["UserName"])
                user_detail["MFAEnabled"] = len(mfa_response.get("MFADevices", [])) > 0
            except ClientError:
                user_detail["MFAEnabled"] = "unknown"
            
            # Get access keys
            try:
                keys_response = iam.list_access_keys(UserName=user["UserName"])
                user_detail["AccessKeys"] = [
                    {
                        "AccessKeyId": k["AccessKeyId"],
                        "Status": k["Status"],
                        "CreateDate": k["CreateDate"].isoformat(),
                    }
                    for k in keys_response.get("AccessKeyMetadata", [])
                ]
            except ClientError:
                user_detail["AccessKeys"] = []
            
            users_data.append(user_detail)
        
        evidence.append(EvidenceItem(
            id="aws-iam-users",
            category="iam",
            title="IAM Users",
            description=f"List of {len(users_data)} IAM users with MFA and access key status",
            data={"users": users_data, "total_count": len(users_data)},
            controls=["CC6.1", "CC6.2", "A.9.2.1", "AC-2"],
        ))
        
        # IAM roles
        roles_response = iam.list_roles()
        roles_data = [
            {
                "RoleName": r["RoleName"],
                "RoleId": r["RoleId"],
                "CreateDate": r["CreateDate"].isoformat(),
                "AssumeRolePolicyDocument": r.get("AssumeRolePolicyDocument"),
            }
            for r in roles_response.get("Roles", [])
        ]
        
        evidence.append(EvidenceItem(
            id="aws-iam-roles",
            category="iam",
            title="IAM Roles",
            description=f"List of {len(roles_data)} IAM roles with trust policies",
            data={"roles": roles_data, "total_count": len(roles_data)},
            controls=["CC6.1", "CC6.3", "A.9.2.3", "AC-3"],
        ))
        
        # Account summary
        summary = iam.get_account_summary()["SummaryMap"]
        evidence.append(EvidenceItem(
            id="aws-iam-summary",
            category="iam",
            title="IAM Account Summary",
            description="High-level IAM statistics for the account",
            data=summary,
            controls=["CC6.1", "A.9.2.1", "AC-2"],
        ))
        
        return evidence
    
    def collect_cloudtrail(self) -> list[EvidenceItem]:
        """Collect CloudTrail evidence."""
        evidence: list[EvidenceItem] = []
        cloudtrail = self.session.client("cloudtrail")
        
        # List trails
        trails_response = cloudtrail.describe_trails()
        trails_data = []
        
        for trail in trails_response.get("trailList", []):
            trail_detail = {
                "Name": trail["Name"],
                "S3BucketName": trail.get("S3BucketName"),
                "IsMultiRegionTrail": trail.get("IsMultiRegionTrail", False),
                "IsOrganizationTrail": trail.get("IsOrganizationTrail", False),
                "IncludeGlobalServiceEvents": trail.get("IncludeGlobalServiceEvents", False),
                "LogFileValidationEnabled": trail.get("LogFileValidationEnabled", False),
                "KMSKeyId": trail.get("KMSKeyId"),
                "CloudWatchLogsLogGroupArn": trail.get("CloudWatchLogsLogGroupArn"),
            }
            
            # Get trail status
            try:
                status = cloudtrail.get_trail_status(Name=trail["Name"])
                trail_detail["IsLogging"] = status.get("IsLogging", False)
                trail_detail["LatestDeliveryTime"] = status.get("LatestDeliveryTime", "").isoformat() if status.get("LatestDeliveryTime") else None
            except ClientError:
                trail_detail["IsLogging"] = "unknown"
            
            trails_data.append(trail_detail)
        
        evidence.append(EvidenceItem(
            id="aws-cloudtrail-trails",
            category="logging",
            title="CloudTrail Configuration",
            description=f"Configuration of {len(trails_data)} CloudTrail trails",
            data={"trails": trails_data, "total_count": len(trails_data)},
            controls=["CC7.2", "A.12.4.1", "AU-2", "AU-12"],
        ))
        
        return evidence
    
    def collect_s3(self) -> list[EvidenceItem]:
        """Collect S3 evidence."""
        evidence: list[EvidenceItem] = []
        s3 = self.session.client("s3")
        
        # List buckets
        buckets_response = s3.list_buckets()
        buckets_data = []
        
        for bucket in buckets_response.get("Buckets", []):
            bucket_name = bucket["Name"]
            bucket_detail = {
                "Name": bucket_name,
                "CreationDate": bucket["CreationDate"].isoformat(),
            }
            
            # Get bucket encryption
            try:
                encryption = s3.get_bucket_encryption(Bucket=bucket_name)
                bucket_detail["Encryption"] = encryption.get("ServerSideEncryptionConfiguration", {})
            except ClientError as e:
                if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                    bucket_detail["Encryption"] = None
                else:
                    bucket_detail["Encryption"] = "access_denied"
            
            # Get bucket versioning
            try:
                versioning = s3.get_bucket_versioning(Bucket=bucket_name)
                bucket_detail["Versioning"] = versioning.get("Status", "Disabled")
            except ClientError:
                bucket_detail["Versioning"] = "access_denied"
            
            # Get public access block
            try:
                public_access = s3.get_public_access_block(Bucket=bucket_name)
                bucket_detail["PublicAccessBlock"] = public_access.get("PublicAccessBlockConfiguration", {})
            except ClientError as e:
                if e.response["Error"]["Code"] == "NoSuchPublicAccessBlockConfiguration":
                    bucket_detail["PublicAccessBlock"] = None
                else:
                    bucket_detail["PublicAccessBlock"] = "access_denied"
            
            # Get bucket logging
            try:
                logging_config = s3.get_bucket_logging(Bucket=bucket_name)
                bucket_detail["Logging"] = logging_config.get("LoggingEnabled")
            except ClientError:
                bucket_detail["Logging"] = "access_denied"
            
            buckets_data.append(bucket_detail)
        
        evidence.append(EvidenceItem(
            id="aws-s3-buckets",
            category="storage",
            title="S3 Bucket Configuration",
            description=f"Security configuration of {len(buckets_data)} S3 buckets",
            data={"buckets": buckets_data, "total_count": len(buckets_data)},
            controls=["CC6.1", "CC6.7", "A.8.2.3", "SC-28"],
        ))
        
        # Account-level public access block
        try:
            s3control = self.session.client("s3control")
            account_public_access = s3control.get_public_access_block(AccountId=self.account_id)
            evidence.append(EvidenceItem(
                id="aws-s3-account-public-access",
                category="storage",
                title="S3 Account Public Access Block",
                description="Account-level S3 public access block configuration",
                data=account_public_access.get("PublicAccessBlockConfiguration", {}),
                controls=["CC6.1", "A.13.2.1", "AC-3"],
            ))
        except ClientError:
            pass
        
        return evidence
    
    def collect_securityhub(self) -> list[EvidenceItem]:
        """Collect Security Hub evidence."""
        evidence: list[EvidenceItem] = []
        
        try:
            securityhub = self.session.client("securityhub")
            
            # Get enabled standards
            standards_response = securityhub.get_enabled_standards()
            standards_data = [
                {
                    "StandardsArn": s["StandardsArn"],
                    "StandardsSubscriptionArn": s["StandardsSubscriptionArn"],
                    "StandardsStatus": s["StandardsStatus"],
                }
                for s in standards_response.get("StandardsSubscriptions", [])
            ]
            
            evidence.append(EvidenceItem(
                id="aws-securityhub-standards",
                category="security",
                title="Security Hub Enabled Standards",
                description=f"List of {len(standards_data)} enabled security standards",
                data={"standards": standards_data, "total_count": len(standards_data)},
                controls=["CC7.1", "A.18.2.3", "RA-5"],
            ))
            
            # Get findings summary (high and critical)
            findings_response = securityhub.get_findings(
                Filters={
                    "SeverityLabel": [
                        {"Value": "CRITICAL", "Comparison": "EQUALS"},
                        {"Value": "HIGH", "Comparison": "EQUALS"},
                    ],
                    "WorkflowStatus": [
                        {"Value": "NEW", "Comparison": "EQUALS"},
                        {"Value": "NOTIFIED", "Comparison": "EQUALS"},
                    ],
                },
                MaxResults=100,
            )
            
            findings_summary = {
                "total_high_critical": len(findings_response.get("Findings", [])),
                "by_type": {},
            }
            
            for finding in findings_response.get("Findings", []):
                finding_type = finding.get("Type", ["Unknown"])[0] if finding.get("Type") else "Unknown"
                findings_summary["by_type"][finding_type] = findings_summary["by_type"].get(finding_type, 0) + 1
            
            evidence.append(EvidenceItem(
                id="aws-securityhub-findings",
                category="security",
                title="Security Hub Findings Summary",
                description="Summary of high and critical security findings",
                data=findings_summary,
                controls=["CC7.1", "CC7.2", "A.12.6.1", "SI-4"],
            ))
            
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidAccessException":
                evidence.append(EvidenceItem(
                    id="aws-securityhub-disabled",
                    category="security",
                    title="Security Hub Status",
                    description="Security Hub is not enabled",
                    data={"enabled": False},
                    controls=["CC7.1", "A.12.6.1", "SI-4"],
                ))
            else:
                raise
        
        return evidence
    
    def collect_kms(self) -> list[EvidenceItem]:
        """Collect KMS evidence."""
        evidence: list[EvidenceItem] = []
        kms = self.session.client("kms")
        
        # List keys
        keys_response = kms.list_keys()
        keys_data = []
        
        for key in keys_response.get("Keys", []):
            key_id = key["KeyId"]
            
            try:
                key_detail = kms.describe_key(KeyId=key_id)["KeyMetadata"]
                key_data = {
                    "KeyId": key_id,
                    "KeyArn": key_detail.get("Arn"),
                    "KeyState": key_detail.get("KeyState"),
                    "KeyUsage": key_detail.get("KeyUsage"),
                    "KeyManager": key_detail.get("KeyManager"),
                    "CreationDate": key_detail.get("CreationDate", "").isoformat() if key_detail.get("CreationDate") else None,
                    "Description": key_detail.get("Description"),
                    "Enabled": key_detail.get("Enabled"),
                }
                
                # Get key rotation status (only for customer-managed keys)
                if key_detail.get("KeyManager") == "CUSTOMER":
                    try:
                        rotation = kms.get_key_rotation_status(KeyId=key_id)
                        key_data["KeyRotationEnabled"] = rotation.get("KeyRotationEnabled", False)
                    except ClientError:
                        key_data["KeyRotationEnabled"] = "access_denied"
                
                keys_data.append(key_data)
            except ClientError:
                continue
        
        evidence.append(EvidenceItem(
            id="aws-kms-keys",
            category="encryption",
            title="KMS Key Configuration",
            description=f"Configuration of {len(keys_data)} KMS keys",
            data={"keys": keys_data, "total_count": len(keys_data)},
            controls=["CC6.1", "A.10.1.2", "SC-12", "SC-13"],
        ))
        
        return evidence
    
    def collect_vpc(self) -> list[EvidenceItem]:
        """Collect VPC and network evidence."""
        evidence: list[EvidenceItem] = []
        ec2 = self.session.client("ec2")
        
        # VPCs
        vpcs_response = ec2.describe_vpcs()
        vpcs_data = [
            {
                "VpcId": vpc["VpcId"],
                "CidrBlock": vpc["CidrBlock"],
                "IsDefault": vpc.get("IsDefault", False),
                "State": vpc["State"],
                "Tags": {t["Key"]: t["Value"] for t in vpc.get("Tags", [])},
            }
            for vpc in vpcs_response.get("Vpcs", [])
        ]
        
        evidence.append(EvidenceItem(
            id="aws-vpc-vpcs",
            category="network",
            title="VPC Configuration",
            description=f"Configuration of {len(vpcs_data)} VPCs",
            data={"vpcs": vpcs_data, "total_count": len(vpcs_data)},
            controls=["CC6.6", "A.13.1.1", "SC-7"],
        ))
        
        # Security Groups
        sgs_response = ec2.describe_security_groups()
        sgs_data = []
        
        for sg in sgs_response.get("SecurityGroups", []):
            # Flag overly permissive rules
            risky_ingress = []
            for rule in sg.get("IpPermissions", []):
                for ip_range in rule.get("IpRanges", []):
                    if ip_range.get("CidrIp") == "0.0.0.0/0":
                        risky_ingress.append({
                            "Protocol": rule.get("IpProtocol"),
                            "FromPort": rule.get("FromPort"),
                            "ToPort": rule.get("ToPort"),
                            "CidrIp": "0.0.0.0/0",
                        })
            
            sgs_data.append({
                "GroupId": sg["GroupId"],
                "GroupName": sg["GroupName"],
                "VpcId": sg.get("VpcId"),
                "Description": sg.get("Description"),
                "IngressRuleCount": len(sg.get("IpPermissions", [])),
                "EgressRuleCount": len(sg.get("IpPermissionsEgress", [])),
                "RiskyIngressRules": risky_ingress,
            })
        
        evidence.append(EvidenceItem(
            id="aws-vpc-security-groups",
            category="network",
            title="Security Groups",
            description=f"Configuration of {len(sgs_data)} security groups with risk assessment",
            data={"security_groups": sgs_data, "total_count": len(sgs_data)},
            controls=["CC6.6", "A.13.1.1", "SC-7", "AC-4"],
        ))
        
        # Network ACLs
        nacls_response = ec2.describe_network_acls()
        nacls_data = [
            {
                "NetworkAclId": nacl["NetworkAclId"],
                "VpcId": nacl["VpcId"],
                "IsDefault": nacl.get("IsDefault", False),
                "EntryCount": len(nacl.get("Entries", [])),
                "AssociationCount": len(nacl.get("Associations", [])),
            }
            for nacl in nacls_response.get("NetworkAcls", [])
        ]
        
        evidence.append(EvidenceItem(
            id="aws-vpc-nacls",
            category="network",
            title="Network ACLs",
            description=f"Configuration of {len(nacls_data)} Network ACLs",
            data={"network_acls": nacls_data, "total_count": len(nacls_data)},
            controls=["CC6.6", "A.13.1.3", "SC-7"],
        ))
        
        # Flow Logs
        flow_logs_response = ec2.describe_flow_logs()
        flow_logs_data = [
            {
                "FlowLogId": fl["FlowLogId"],
                "ResourceId": fl.get("ResourceId"),
                "ResourceType": fl.get("ResourceType"),
                "TrafficType": fl.get("TrafficType"),
                "LogDestinationType": fl.get("LogDestinationType"),
                "FlowLogStatus": fl.get("FlowLogStatus"),
            }
            for fl in flow_logs_response.get("FlowLogs", [])
        ]
        
        evidence.append(EvidenceItem(
            id="aws-vpc-flow-logs",
            category="network",
            title="VPC Flow Logs",
            description=f"Configuration of {len(flow_logs_data)} VPC flow logs",
            data={"flow_logs": flow_logs_data, "total_count": len(flow_logs_data)},
            controls=["CC7.2", "A.12.4.1", "AU-12"],
        ))
        
        return evidence
