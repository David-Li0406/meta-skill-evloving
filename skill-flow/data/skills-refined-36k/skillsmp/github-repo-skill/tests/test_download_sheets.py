"""Tests for download_sheets.py script."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from click.testing import CliRunner

from cmm_ai_automation.scripts.download_sheets import main


class TestDownloadSheetsMain:
    """Tests for download_sheets main function."""

    @pytest.fixture
    def mock_gsheets(self) -> tuple[MagicMock, MagicMock]:
        """Create mocks for gsheets functions."""
        mock_list = MagicMock(return_value=["tab1", "tab2", "tab3"])
        mock_get = MagicMock(return_value=pd.DataFrame({"col1": ["a", "b", "c"], "col2": [1, 2, 3]}))
        return mock_list, mock_get

    def test_cli_help(self) -> None:
        """Test CLI --help works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Download Google Sheet tabs" in result.output

    def test_download_all_tabs(self, mock_gsheets: tuple[MagicMock, MagicMock]) -> None:
        """Test downloading all tabs from a spreadsheet."""
        mock_list, mock_get = mock_gsheets

        with (
            patch("cmm_ai_automation.scripts.download_sheets.list_worksheets", mock_list),
            patch("cmm_ai_automation.scripts.download_sheets.get_sheet_data", mock_get),
        ):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    ["--output-dir", ".", "--spreadsheet", "Test Sheet"],
                )

                assert result.exit_code == 0
                assert "tab1" in result.output
                assert "tab2" in result.output
                assert "tab3" in result.output
                assert Path("tab1.tsv").exists()
                assert Path("tab2.tsv").exists()
                assert Path("tab3.tsv").exists()

    def test_download_specific_tabs(self, mock_gsheets: tuple[MagicMock, MagicMock]) -> None:
        """Test downloading specific tabs."""
        mock_list, mock_get = mock_gsheets

        with (
            patch("cmm_ai_automation.scripts.download_sheets.list_worksheets", mock_list),
            patch("cmm_ai_automation.scripts.download_sheets.get_sheet_data", mock_get),
        ):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    [
                        "--output-dir",
                        ".",
                        "--spreadsheet",
                        "Test Sheet",
                        "--tabs",
                        "tab1",
                        "--tabs",
                        "tab2",
                    ],
                )

                assert result.exit_code == 0
                assert Path("tab1.tsv").exists()
                assert Path("tab2.tsv").exists()
                # tab3 should NOT exist since we only requested tab1 and tab2
                assert not Path("tab3.tsv").exists()

    def test_skip_nonexistent_tab(self, mock_gsheets: tuple[MagicMock, MagicMock]) -> None:
        """Test that nonexistent tabs are skipped."""
        mock_list, mock_get = mock_gsheets

        with (
            patch("cmm_ai_automation.scripts.download_sheets.list_worksheets", mock_list),
            patch("cmm_ai_automation.scripts.download_sheets.get_sheet_data", mock_get),
        ):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    [
                        "--output-dir",
                        ".",
                        "--spreadsheet",
                        "Test Sheet",
                        "--tabs",
                        "nonexistent",
                    ],
                )

                assert result.exit_code == 0
                assert "SKIP: nonexistent (not found)" in result.output

    def test_error_handling(self, mock_gsheets: tuple[MagicMock, MagicMock]) -> None:
        """Test error handling when get_sheet_data fails."""
        mock_list, _ = mock_gsheets
        mock_get_error = MagicMock(side_effect=Exception("API Error"))

        with (
            patch("cmm_ai_automation.scripts.download_sheets.list_worksheets", mock_list),
            patch("cmm_ai_automation.scripts.download_sheets.get_sheet_data", mock_get_error),
        ):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    [
                        "--output-dir",
                        ".",
                        "--spreadsheet",
                        "Test Sheet",
                        "--tabs",
                        "tab1",
                    ],
                )

                assert result.exit_code == 0
                assert "ERROR: tab1" in result.output
                assert "API Error" in result.output

    def test_creates_output_dir(self, mock_gsheets: tuple[MagicMock, MagicMock]) -> None:
        """Test that output directory is created if needed."""
        mock_list, mock_get = mock_gsheets

        with (
            patch("cmm_ai_automation.scripts.download_sheets.list_worksheets", mock_list),
            patch("cmm_ai_automation.scripts.download_sheets.get_sheet_data", mock_get),
        ):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    [
                        "--output-dir",
                        "nested/output/dir",
                        "--spreadsheet",
                        "Test Sheet",
                        "--tabs",
                        "tab1",
                    ],
                )

                assert result.exit_code == 0
                assert Path("nested/output/dir/tab1.tsv").exists()

    def test_tsv_content(self, mock_gsheets: tuple[MagicMock, MagicMock]) -> None:
        """Test that TSV files have correct content."""
        mock_list, mock_get = mock_gsheets

        with (
            patch("cmm_ai_automation.scripts.download_sheets.list_worksheets", mock_list),
            patch("cmm_ai_automation.scripts.download_sheets.get_sheet_data", mock_get),
        ):
            runner = CliRunner()
            with runner.isolated_filesystem():
                result = runner.invoke(
                    main,
                    [
                        "--output-dir",
                        ".",
                        "--spreadsheet",
                        "Test Sheet",
                        "--tabs",
                        "tab1",
                    ],
                )

                assert result.exit_code == 0

                # Read the TSV file and verify content
                content = Path("tab1.tsv").read_text()
                assert "col1\tcol2" in content
                assert "a\t1" in content
