#!/usr/bin/env python3
"""
Expiry Checker Module

Checks trademark validity periods and generates expiry alerts.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum


class ExpiryStatus(Enum):
    """Expiry status enumeration"""
    EXPIRED = "expired"
    CRITICAL = "critical"      # < 90 days
    WARNING = "warning"        # < 180 days
    ATTENTION = "attention"    # < 365 days
    VALID = "valid"
    UNKNOWN = "unknown"


class ExpiryChecker:
    """
    Checks trademark validity periods and generates renewal reminders
    """

    # Alert thresholds in days
    THRESHOLD_CRITICAL = 90
    THRESHOLD_WARNING = 180
    THRESHOLD_ATTENTION = 365

    def __init__(self, reference_date: Optional[datetime] = None):
        """
        Initialize expiry checker

        Args:
            reference_date: Reference date for calculations (defaults to today)
        """
        self.reference_date = reference_date or datetime.now()

    def parse_validity_period(self, date_str: str) -> Optional[datetime]:
        """
        Parse validity period string to datetime

        Args:
            date_str: Date string in various formats

        Returns:
            datetime object or None if parsing fails
        """
        if not date_str or not isinstance(date_str, str):
            return None

        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d/%m/%Y',
            '%Y年%m月%d日',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%Y.%m.%d',
            '%Y%m%d',
        ]

        # Clean up the string
        cleaned = date_str.strip().replace('日', '')

        for fmt in date_formats:
            try:
                return datetime.strptime(cleaned, fmt)
            except (ValueError, TypeError):
                continue

        return None

    def check_expiry(self, validity_period: str) -> Tuple[ExpiryStatus, int, str]:
        """
        Check expiry status of a trademark

        Args:
            validity_period: Validity period string

        Returns:
            Tuple of (status, days_remaining, message)
        """
        expiry_date = self.parse_validity_period(validity_period)

        if not expiry_date:
            return (ExpiryStatus.UNKNOWN, 0, "无法解析有效期")

        # Calculate days remaining
        days_remaining = (expiry_date - self.reference_date).days

        # Determine status
        if days_remaining < 0:
            status = ExpiryStatus.EXPIRED
            message = f"已过期 {abs(days_remaining)} 天"
        elif days_remaining < self.THRESHOLD_CRITICAL:
            status = ExpiryStatus.CRITICAL
            message = f"⚠️ 紧急：还有 {days_remaining} 天到期"
        elif days_remaining < self.THRESHOLD_WARNING:
            status = ExpiryStatus.WARNING
            message = f"⚠️ 警告：还有 {days_remaining} 天到期"
        elif days_remaining < self.THRESHOLD_ATTENTION:
            status = ExpiryStatus.ATTENTION
            message = f"注意：还有 {days_remaining} 天到期"
        else:
            status = ExpiryStatus.VALID
            message = f"有效（还有 {days_remaining} 天）"

        return (status, days_remaining, message)

    def add_expiry_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add expiry information to trademark data

        Args:
            data: Trademark data dictionary

        Returns:
            Enhanced data with expiry information
        """
        enhanced_data = data.copy()
        validity_period = data.get('有效期限', '')

        status, days_remaining, message = self.check_expiry(validity_period)

        enhanced_data['expiry_status'] = status.value
        enhanced_data['days_until_expiry'] = days_remaining
        enhanced_data['expiry_message'] = message
        enhanced_data['requires_renewal'] = status in [ExpiryStatus.CRITICAL, ExpiryStatus.WARNING]

        # Add renewal deadline (typically 6 months before expiry)
        expiry_date = self.parse_validity_period(validity_period)
        if expiry_date:
            renewal_deadline = expiry_date - timedelta(days=180)
            enhanced_data['renewal_deadline'] = renewal_deadline.strftime('%Y-%m-%d')
            enhanced_data['expiry_date_parsed'] = expiry_date.strftime('%Y-%m-%d')

        return enhanced_data

    def generate_renewal_list(self, trademarks: List[Dict[str, Any]],
                             threshold_days: int = THRESHOLD_WARNING) -> List[Dict[str, Any]]:
        """
        Generate renewal to-do list for trademarks expiring soon

        Args:
            trademarks: List of trademark data dictionaries
            threshold_days: Only include trademarks expiring within this many days

        Returns:
            List of trademarks requiring renewal, sorted by expiry date
        """
        renewal_list = []

        for trademark in trademarks:
            validity_period = trademark.get('有效期限', '')
            status, days_remaining, message = self.check_expiry(validity_period)

            if 0 <= days_remaining <= threshold_days:
                renewal_item = trademark.copy()
                renewal_item['expiry_status'] = status.value
                renewal_item['days_until_expiry'] = days_remaining
                renewal_item['expiry_message'] = message
                renewal_item['priority'] = self._calculate_priority(days_remaining)
                renewal_list.append(renewal_item)

        # Sort by days remaining (most urgent first)
        renewal_list.sort(key=lambda x: x['days_until_expiry'])

        return renewal_list

    def _calculate_priority(self, days_remaining: int) -> str:
        """Calculate renewal priority based on days remaining"""
        if days_remaining < self.THRESHOLD_CRITICAL:
            return "🔴 紧急"
        elif days_remaining < self.THRESHOLD_WARNING:
            return "🟡 高"
        else:
            return "🟢 中"

    def generate_renewal_report(self, trademarks: List[Dict[str, Any]]) -> str:
        """
        Generate renewal reminder report

        Args:
            trademarks: List of trademark data

        Returns:
            Formatted renewal report
        """
        # Add expiry info to all trademarks
        enhanced_trademarks = [self.add_expiry_info(tm) for tm in trademarks]

        # Get renewal list
        renewal_list = self.generate_renewal_list(enhanced_trademarks)

        # Generate report
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("商标续展提醒报告")
        report_lines.append("=" * 80)
        report_lines.append(f"生成日期: {self.reference_date.strftime('%Y年%m月%d日')}")
        report_lines.append("")

        # Statistics
        expired_count = sum(1 for tm in enhanced_trademarks if tm.get('expiry_status') == ExpiryStatus.EXPIRED.value)
        critical_count = sum(1 for tm in enhanced_trademarks if tm.get('expiry_status') == ExpiryStatus.CRITICAL.value)
        warning_count = sum(1 for tm in enhanced_trademarks if tm.get('expiry_status') == ExpiryStatus.WARNING.value)

        report_lines.append("📊 统计概览")
        report_lines.append("-" * 80)
        report_lines.append(f"总商标数: {len(enhanced_trademarks)}")
        report_lines.append(f"已过期: {expired_count}")
        report_lines.append(f"90天内到期: {critical_count}")
        report_lines.append(f"180天内到期: {warning_count}")
        report_lines.append(f"需要续展: {len(renewal_list)}")
        report_lines.append("")

        # Renewal list
        if renewal_list:
            report_lines.append("🔔 续展待办清单")
            report_lines.append("-" * 80)
            report_lines.append(f"{'优先级':<10} {'注册人':<25} {'注册号':<15} {'到期日期':<15} {'剩余天数':<10}")
            report_lines.append("-" * 80)

            for tm in renewal_list:
                priority = tm.get('priority', '')
                registrant = tm.get('注册人', '')[:23]
                reg_number = tm.get('注册号', '')
                expiry_date = tm.get('expiry_date_parsed', tm.get('有效期限', ''))
                days = tm.get('days_until_expiry', 0)

                report_lines.append(f"{priority:<12} {registrant:<25} {reg_number:<15} {expiry_date:<15} {days:<10}")

            report_lines.append("")
        else:
            report_lines.append("✅ 暂无需要续展的商标")
            report_lines.append("")

        # Expired trademarks
        expired_trademarks = [tm for tm in enhanced_trademarks if tm.get('expiry_status') == ExpiryStatus.EXPIRED.value]
        if expired_trademarks:
            report_lines.append("❌ 已过期商标")
            report_lines.append("-" * 80)
            for tm in expired_trademarks:
                registrant = tm.get('注册人', '')
                reg_number = tm.get('注册号', '')
                expiry_date = tm.get('有效期限', '')
                report_lines.append(f"• {registrant} - {reg_number} (到期日: {expiry_date})")
            report_lines.append("")

        report_lines.append("=" * 80)
        report_lines.append("提示: 商标续展应在到期前6-12个月内办理")
        report_lines.append("=" * 80)

        return "\n".join(report_lines)


if __name__ == "__main__":
    # Test expiry checker
    checker = ExpiryChecker()

    test_trademarks = [
        {
            '注册人': '阿里巴巴集团控股有限公司',
            '注册号': '12345678',
            '有效期限': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
        },
        {
            '注册人': '腾讯科技（深圳）有限公司',
            '注册号': '87654321',
            '有效期限': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d'),
        },
        {
            '注册人': '百度在线网络技术有限公司',
            '注册号': '11111111',
            '有效期限': (datetime.now() + timedelta(days=500)).strftime('%Y-%m-%d'),
        },
    ]

    print(checker.generate_renewal_report(test_trademarks))
