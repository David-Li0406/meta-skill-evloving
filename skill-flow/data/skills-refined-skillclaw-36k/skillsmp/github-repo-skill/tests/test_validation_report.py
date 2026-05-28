"""Tests for validation base classes - ValidationReport methods."""

from cmm_ai_automation.validation.base import (
    IssueType,
    Severity,
    ValidationIssue,
    ValidationReport,
)


class TestValidationReportMethods:
    """Tests for ValidationReport methods."""

    def test_add_issue_updates_stats(self) -> None:
        """Test that add_issue updates stats correctly."""
        report = ValidationReport()
        issue = ValidationIssue(
            sheet="test.tsv",
            row=1,
            field="test_field",
            issue_type=IssueType.INVALID_ID,
            severity=Severity.ERROR,
            message="Test error",
        )

        report.add_issue(issue)

        assert len(report.issues) == 1
        assert report.stats["invalid_id"] == 1

    def test_add_multiple_issues_same_type(self) -> None:
        """Test adding multiple issues of the same type."""
        report = ValidationReport()
        for i in range(3):
            issue = ValidationIssue(
                sheet="test.tsv",
                row=i,
                field="field",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message=f"Error {i}",
            )
            report.add_issue(issue)

        assert len(report.issues) == 3
        assert report.stats["invalid_id"] == 3

    def test_add_issues_different_types(self) -> None:
        """Test adding issues of different types."""
        report = ValidationReport()
        issue1 = ValidationIssue(
            sheet="test.tsv",
            row=1,
            field="field1",
            issue_type=IssueType.INVALID_ID,
            severity=Severity.ERROR,
            message="Error 1",
        )
        issue2 = ValidationIssue(
            sheet="test.tsv",
            row=2,
            field="field2",
            issue_type=IssueType.NAME_MISMATCH,
            severity=Severity.WARNING,
            message="Warning 1",
        )

        report.add_issue(issue1)
        report.add_issue(issue2)

        assert len(report.issues) == 2
        assert report.stats["invalid_id"] == 1
        assert report.stats["name_mismatch"] == 1

    def test_merge_combines_sheets(self) -> None:
        """Test merging combines sheets_checked lists."""
        report1 = ValidationReport(sheets_checked=["sheet1.tsv", "sheet2.tsv"])
        report2 = ValidationReport(sheets_checked=["sheet3.tsv"])

        report1.merge(report2)

        assert len(report1.sheets_checked) == 3
        assert "sheet1.tsv" in report1.sheets_checked
        assert "sheet2.tsv" in report1.sheets_checked
        assert "sheet3.tsv" in report1.sheets_checked

    def test_merge_combines_row_counts(self) -> None:
        """Test merging adds row counts."""
        report1 = ValidationReport(rows_checked=10)
        report2 = ValidationReport(rows_checked=5)

        report1.merge(report2)

        assert report1.rows_checked == 15

    def test_merge_combines_issues(self) -> None:
        """Test merging combines and re-stats issues."""
        report1 = ValidationReport()
        issue1 = ValidationIssue(
            sheet="test1.tsv",
            row=1,
            field="field",
            issue_type=IssueType.INVALID_ID,
            severity=Severity.ERROR,
            message="Error 1",
        )
        report1.add_issue(issue1)

        report2 = ValidationReport()
        issue2 = ValidationIssue(
            sheet="test2.tsv",
            row=1,
            field="field",
            issue_type=IssueType.INVALID_ID,
            severity=Severity.ERROR,
            message="Error 2",
        )
        report2.add_issue(issue2)

        report1.merge(report2)

        assert len(report1.issues) == 2
        assert report1.stats["invalid_id"] == 2

    def test_merge_combines_lookup_cache(self) -> None:
        """Test merging combines lookup caches."""
        report1 = ValidationReport(lookup_cache={"key1": "value1"})
        report2 = ValidationReport(lookup_cache={"key2": "value2"})

        report1.merge(report2)

        assert len(report1.lookup_cache) == 2
        assert report1.lookup_cache["key1"] == "value1"
        assert report1.lookup_cache["key2"] == "value2"

    def test_error_count_property(self) -> None:
        """Test error_count property."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Error",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=2,
                field="f2",
                issue_type=IssueType.NAME_MISMATCH,
                severity=Severity.WARNING,
                message="Warning",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=3,
                field="f3",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Error 2",
            )
        )

        assert report.error_count == 2

    def test_warning_count_property(self) -> None:
        """Test warning_count property."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Error",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=2,
                field="f2",
                issue_type=IssueType.NAME_MISMATCH,
                severity=Severity.WARNING,
                message="Warning 1",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=3,
                field="f3",
                issue_type=IssueType.MISSING_VALUE,
                severity=Severity.WARNING,
                message="Warning 2",
            )
        )

        assert report.warning_count == 2

    def test_info_count_property(self) -> None:
        """Test info_count property."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.INFO,
                message="Info 1",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=2,
                field="f2",
                issue_type=IssueType.NAME_MISMATCH,
                severity=Severity.INFO,
                message="Info 2",
            )
        )

        assert report.info_count == 2

    def test_get_issues_by_severity(self) -> None:
        """Test filtering issues by severity."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Error",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=2,
                field="f2",
                issue_type=IssueType.NAME_MISMATCH,
                severity=Severity.WARNING,
                message="Warning",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=3,
                field="f3",
                issue_type=IssueType.MISSING_VALUE,
                severity=Severity.INFO,
                message="Info",
            )
        )

        errors = report.get_issues_by_severity(Severity.ERROR)
        warnings = report.get_issues_by_severity(Severity.WARNING)
        infos = report.get_issues_by_severity(Severity.INFO)

        assert len(errors) == 1
        assert len(warnings) == 1
        assert len(infos) == 1
        assert errors[0].message == "Error"
        assert warnings[0].message == "Warning"
        assert infos[0].message == "Info"

    def test_get_issues_by_type(self) -> None:
        """Test filtering issues by type."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Invalid ID 1",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=2,
                field="f2",
                issue_type=IssueType.NAME_MISMATCH,
                severity=Severity.WARNING,
                message="Name mismatch",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=3,
                field="f3",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Invalid ID 2",
            )
        )

        invalid_id_issues = report.get_issues_by_type(IssueType.INVALID_ID)
        name_mismatch_issues = report.get_issues_by_type(IssueType.NAME_MISMATCH)

        assert len(invalid_id_issues) == 2
        assert len(name_mismatch_issues) == 1
        assert invalid_id_issues[0].message == "Invalid ID 1"
        assert invalid_id_issues[1].message == "Invalid ID 2"

    def test_get_issues_for_row(self) -> None:
        """Test getting all issues for a specific row."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Row 1 issue 1",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=1,
                field="f2",
                issue_type=IssueType.NAME_MISMATCH,
                severity=Severity.WARNING,
                message="Row 1 issue 2",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="test.tsv",
                row=2,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Row 2 issue",
            )
        )

        row1_issues = report.get_issues_for_row("test.tsv", 1)
        row2_issues = report.get_issues_for_row("test.tsv", 2)

        assert len(row1_issues) == 2
        assert len(row2_issues) == 1
        assert "Row 1" in row1_issues[0].message
        assert "Row 2" in row2_issues[0].message

    def test_get_issues_for_row_different_sheets(self) -> None:
        """Test that get_issues_for_row filters by sheet name."""
        report = ValidationReport()
        report.add_issue(
            ValidationIssue(
                sheet="sheet1.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Sheet 1",
            )
        )
        report.add_issue(
            ValidationIssue(
                sheet="sheet2.tsv",
                row=1,
                field="f1",
                issue_type=IssueType.INVALID_ID,
                severity=Severity.ERROR,
                message="Sheet 2",
            )
        )

        sheet1_row1 = report.get_issues_for_row("sheet1.tsv", 1)
        sheet2_row1 = report.get_issues_for_row("sheet2.tsv", 1)

        assert len(sheet1_row1) == 1
        assert len(sheet2_row1) == 1
        assert "Sheet 1" in sheet1_row1[0].message
        assert "Sheet 2" in sheet2_row1[0].message

    def test_empty_report_counts(self) -> None:
        """Test that empty report has zero counts."""
        report = ValidationReport()

        assert report.error_count == 0
        assert report.warning_count == 0
        assert report.info_count == 0
        assert report.get_issues_by_severity(Severity.ERROR) == []
        assert report.get_issues_by_type(IssueType.INVALID_ID) == []
        assert report.get_issues_for_row("test.tsv", 1) == []
