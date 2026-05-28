# -*- coding: utf-8 -*-
"""セキュリティスキャンスキル - Security Scanner.

コードベースのセキュリティ脆弱性を検出するスキル。

使用例:
    >>> scanner = SecurityScanner()
    >>> report = await scanner.scan(
    ...     repo_info=repo,
    ...     scan_types=["sast", "dependency"],
    ... )
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from agentflow.core.agent_block import AgentBlock


logger = logging.getLogger(__name__)


class VulnerabilitySeverity(str, Enum):
    """脆弱性の重要度."""

    CRITICAL = "critical"  # CVSS 9.0-10.0
    HIGH = "high"  # CVSS 7.0-8.9
    MEDIUM = "medium"  # CVSS 4.0-6.9
    LOW = "low"  # CVSS 0.1-3.9
    INFO = "info"


class VulnerabilityType(str, Enum):
    """脆弱性のタイプ."""

    INJECTION = "injection"  # SQLインジェクション等
    XSS = "xss"  # クロスサイトスクリプティング
    AUTHENTICATION = "authentication"  # 認証関連
    EXPOSURE = "exposure"  # 情報漏洩
    CRYPTO = "crypto"  # 暗号化関連
    DEPENDENCY = "dependency"  # 依存関係の脆弱性
    CONFIGURATION = "configuration"  # 設定ミス


@dataclass
class Vulnerability:
    """検出された脆弱性."""

    vuln_id: str
    cve_id: str | None = None
    cwes: list[str] = field(default_factory=list)
    severity: VulnerabilitySeverity = VulnerabilitySeverity.MEDIUM
    vuln_type: VulnerabilityType = VulnerabilityType.INJECTION
    title: str = ""
    description: str = ""
    file_path: str | None = None
    line_number: int | None = None
    affected_component: str = ""
    remediation: str = ""
    cvss_score: float | None = None
    references: list[str] = field(default_factory=list)


@dataclass
class ScanSummary:
    """スキャンサマリー."""

    total_vulnerabilities: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    fixed_count: int  # 修正済み
    risk_score: float  # 0-100


@dataclass
class SecurityReport:
    """セキュリティレポート."""

    report_id: str
    summary: ScanSummary
    vulnerabilities: list[Vulnerability]
    scan_types: list[str]
    compliance_status: dict[str, bool]  # OWASP, PCI-DSS等
    recommendations: list[str]
    scanned_at: datetime = field(default_factory=datetime.now)


class SecurityScanner(AgentBlock):
    """セキュリティスキャンスキル.

    SAST、依存関係チェック、設定監査を実行し、
    セキュリティ脆弱性を検出します。
    """

    def __init__(
        self,
        severity_threshold: VulnerabilitySeverity = VulnerabilitySeverity.LOW,
        include_info: bool = False,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            severity_threshold: 報告する最低重要度
            include_info: 情報レベルを含めるか
            llm_client: LLMクライアント
        """
        super().__init__()
        self._severity_threshold = severity_threshold
        self._include_info = include_info
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - repo_info: リポジトリ情報
                - scan_types: スキャンタイプ

        Returns:
            セキュリティレポート
        """
        scan_types = input_data.get("scan_types", ["sast", "dependency"])

        report = await self.scan(scan_types=scan_types)

        return {
            "report_id": report.report_id,
            "summary": {
                "total_vulnerabilities": report.summary.total_vulnerabilities,
                "critical_count": report.summary.critical_count,
                "high_count": report.summary.high_count,
                "medium_count": report.summary.medium_count,
                "low_count": report.summary.low_count,
                "risk_score": report.summary.risk_score,
            },
            "vulnerabilities": [
                self._vuln_to_dict(v) for v in report.vulnerabilities[:50]
            ],
            "scan_types": report.scan_types,
            "compliance_status": report.compliance_status,
            "recommendations": report.recommendations,
            "scanned_at": report.scanned_at.isoformat(),
        }

    async def scan(
        self,
        scan_types: list[str] | None = None,
    ) -> SecurityReport:
        """セキュリティスキャンを実行.

        Args:
            scan_types: スキャンタイプ

        Returns:
            セキュリティレポート
        """
        import uuid

        scan_types = scan_types or ["sast", "dependency"]
        report_id = f"sec-{uuid.uuid4().hex[:8]}"

        logger.info("セキュリティスキャン開始: types=%s", scan_types)

        vulnerabilities: list[Vulnerability] = []

        # SAST スキャン
        if "sast" in scan_types:
            vulnerabilities.extend(await self._run_sast_scan())

        # 依存関係スキャン
        if "dependency" in scan_types:
            vulnerabilities.extend(await self._run_dependency_scan())

        # サマリー作成
        summary = self._create_summary(vulnerabilities)

        # コンプライアンスチェック
        compliance = self._check_compliance(vulnerabilities)

        # 推奨事項生成
        recommendations = self._generate_recommendations(vulnerabilities)

        return SecurityReport(
            report_id=report_id,
            summary=summary,
            vulnerabilities=vulnerabilities,
            scan_types=scan_types,
            compliance_status=compliance,
            recommendations=recommendations,
        )

    async def _run_sast_scan(self) -> list[Vulnerability]:
        """SAST スキャンを実行（デモ用）."""
        return [
            Vulnerability(
                vuln_id="vuln-001",
                severity=VulnerabilitySeverity.HIGH,
                vuln_type=VulnerabilityType.INJECTION,
                cwes=["CWE-89"],
                title="SQLインジェクションの可能性",
                description="ユーザー入力が直接SQLクエリに使用されています",
                file_path="src/db/queries.py",
                line_number=45,
                remediation="パラメータ化クエリを使用してください",
            ),
            Vulnerability(
                vuln_id="vuln-002",
                severity=VulnerabilitySeverity.MEDIUM,
                vuln_type=VulnerabilityType.EXPOSURE,
                cwes=["CWE-200"],
                title="機密情報の露出",
                description="APIキーがソースコードにハードコードされています",
                file_path="src/config.py",
                line_number=12,
                remediation="環境変数を使用してください",
            ),
        ]

    async def _run_dependency_scan(self) -> list[Vulnerability]:
        """依存関係スキャンを実行（デモ用）."""
        return [
            Vulnerability(
                vuln_id="vuln-003",
                cve_id="CVE-2024-1234",
                severity=VulnerabilitySeverity.CRITICAL,
                vuln_type=VulnerabilityType.DEPENDENCY,
                title="既知の脆弱性を持つライブラリ",
                description="requests 2.25.0 にCVE-2024-1234の脆弱性があります",
                affected_component="requests==2.25.0",
                cvss_score=9.8,
                remediation="requests>=2.31.0 にアップグレードしてください",
                references=["https://nvd.nist.gov/vuln/detail/CVE-2024-1234"],
            ),
        ]

    def _create_summary(
        self, vulnerabilities: list[Vulnerability]
    ) -> ScanSummary:
        """サマリーを作成."""
        severity_counts = {s: 0 for s in VulnerabilitySeverity}
        for v in vulnerabilities:
            severity_counts[v.severity] += 1

        # リスクスコア計算
        weights = {
            VulnerabilitySeverity.CRITICAL: 40,
            VulnerabilitySeverity.HIGH: 20,
            VulnerabilitySeverity.MEDIUM: 10,
            VulnerabilitySeverity.LOW: 5,
            VulnerabilitySeverity.INFO: 1,
        }
        risk_score = min(100, sum(
            severity_counts[s] * w for s, w in weights.items()
        ))

        return ScanSummary(
            total_vulnerabilities=len(vulnerabilities),
            critical_count=severity_counts[VulnerabilitySeverity.CRITICAL],
            high_count=severity_counts[VulnerabilitySeverity.HIGH],
            medium_count=severity_counts[VulnerabilitySeverity.MEDIUM],
            low_count=severity_counts[VulnerabilitySeverity.LOW],
            fixed_count=0,
            risk_score=risk_score,
        )

    def _check_compliance(
        self, vulnerabilities: list[Vulnerability]
    ) -> dict[str, bool]:
        """コンプライアンスをチェック."""
        critical_high = sum(
            1 for v in vulnerabilities
            if v.severity in [
                VulnerabilitySeverity.CRITICAL,
                VulnerabilitySeverity.HIGH,
            ]
        )

        return {
            "OWASP_Top10": critical_high == 0,
            "PCI_DSS": critical_high == 0,
            "SOC2": critical_high <= 2,
        }

    def _generate_recommendations(
        self, vulnerabilities: list[Vulnerability]
    ) -> list[str]:
        """推奨事項を生成."""
        recommendations = []

        critical = [
            v for v in vulnerabilities
            if v.severity == VulnerabilitySeverity.CRITICAL
        ]
        if critical:
            recommendations.append(
                f"[緊急] {len(critical)}件のCritical脆弱性を即座に修正してください"
            )

        dep_vulns = [
            v for v in vulnerabilities
            if v.vuln_type == VulnerabilityType.DEPENDENCY
        ]
        if dep_vulns:
            recommendations.append(
                f"[高優先] {len(dep_vulns)}件の依存関係をアップデートしてください"
            )

        if not recommendations:
            recommendations.append("セキュリティ状態は良好です")

        return recommendations

    def _vuln_to_dict(self, vuln: Vulnerability) -> dict[str, Any]:
        """脆弱性をdict形式に変換."""
        return {
            "vuln_id": vuln.vuln_id,
            "cve_id": vuln.cve_id,
            "cwes": vuln.cwes,
            "severity": vuln.severity.value,
            "type": vuln.vuln_type.value,
            "title": vuln.title,
            "description": vuln.description,
            "file_path": vuln.file_path,
            "line_number": vuln.line_number,
            "affected_component": vuln.affected_component,
            "remediation": vuln.remediation,
            "cvss_score": vuln.cvss_score,
        }
