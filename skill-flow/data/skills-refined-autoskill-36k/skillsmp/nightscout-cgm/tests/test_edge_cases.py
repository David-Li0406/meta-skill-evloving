"""
Tests for edge cases, error handling, and integration scenarios.
"""
import sqlite3
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import requests


class TestNightscoutUrlNormalization:
    """Tests for flexible NIGHTSCOUT_URL handling."""
    
    def test_full_url_unchanged(self, cgm_module):
        """Full URL with /api/v1/entries.json should be unchanged."""
        url = "https://my-ns.herokuapp.com/api/v1/entries.json"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == url
    
    def test_domain_only(self, cgm_module):
        """Just domain should get full path appended."""
        url = "https://my-ns.herokuapp.com"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == "https://my-ns.herokuapp.com/api/v1/entries.json"
    
    def test_domain_with_trailing_slash(self, cgm_module):
        """Domain with trailing slash should work."""
        url = "https://my-ns.herokuapp.com/"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == "https://my-ns.herokuapp.com/api/v1/entries.json"
    
    def test_partial_api_path(self, cgm_module):
        """Partial /api path should be completed."""
        url = "https://my-ns.herokuapp.com/api"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == "https://my-ns.herokuapp.com/api/v1/entries.json"
    
    def test_partial_api_v1_path(self, cgm_module):
        """Partial /api/v1 path should be completed."""
        url = "https://my-ns.herokuapp.com/api/v1"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == "https://my-ns.herokuapp.com/api/v1/entries.json"
    
    def test_entries_without_json(self, cgm_module):
        """/api/v1/entries without .json should add it."""
        url = "https://my-ns.herokuapp.com/api/v1/entries"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == "https://my-ns.herokuapp.com/api/v1/entries.json"
    
    def test_custom_subdomain(self, cgm_module):
        """Works with custom subdomains."""
        url = "https://nightscout.example.org"
        result = cgm_module._normalize_nightscout_url(url)
        assert result == "https://nightscout.example.org/api/v1/entries.json"


class TestErrorHandling:
    """Tests for error handling throughout the module."""
    
    def test_network_error_on_current(self, cgm_module, mock_requests_get):
        """Network errors should return error dict."""
        mock_requests_get.side_effect = requests.RequestException("Connection failed")
        
        result = cgm_module.get_current_glucose()
        assert "error" in result
    
    def test_invalid_json_response(self, cgm_module, mock_requests_get):
        """Invalid JSON should be handled gracefully."""
        # Note: Currently the code doesn't catch json decode errors.
        # This test documents that ValueError will be raised.
        # Consider adding try/except for json.JSONDecodeError in get_current_glucose
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(ValueError):
            cgm_module.get_current_glucose()
    
    def test_empty_api_response(self, cgm_module, mock_requests_get):
        """Empty API response should be handled."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response
        
        result = cgm_module.get_current_glucose()
        assert "error" in result
    
    def test_missing_sgv_in_response(self, cgm_module, mock_requests_get):
        """Response without sgv field should be handled."""
        mock_response = MagicMock()
        mock_response.json.return_value = [{"date": 123456, "direction": "Flat"}]
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response
        
        result = cgm_module.get_current_glucose()
        # Should handle missing sgv gracefully
        assert result is not None


class TestBoundaryConditions:
    """Tests for boundary conditions."""
    
    def test_zero_days_analysis(self, cgm_module, populated_db):
        """Zero days should return empty/error."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                result = cgm_module.analyze_cgm(days=0)
                # Should either error or return empty results
                assert result is not None
    
    def test_very_large_days_value(self, cgm_module, populated_db):
        """Very large days value should work."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=3650)  # 10 years
                        assert result is not None
    
    def test_extreme_glucose_values(self, cgm_module):
        """Extreme glucose values should be handled."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            with patch.object(cgm_module, "get_unit_label", return_value="mg/dL"):
                # Very low
                stats = cgm_module.get_stats([20, 25, 30])
                assert stats["min"] == 20
                
                # Very high
                stats = cgm_module.get_stats([500, 550, 600])
                assert stats["max"] == 600
    
    def test_single_reading_analysis(self, cgm_module, temp_db):
        """Single reading should be handled."""
        # Insert single reading
        conn = sqlite3.connect(temp_db)
        now = datetime.now(timezone.utc)
        conn.execute(
            "INSERT INTO readings (id, sgv, date_ms, date_string, direction) VALUES (?, ?, ?, ?, ?)",
            ("single", 120, int(now.timestamp() * 1000), now.isoformat(), "Flat")
        )
        conn.commit()
        conn.close()
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=1)
                        assert result["readings"] == 1


class TestDateParsing:
    """Tests for date parsing edge cases."""
    
    def test_future_date(self, cgm_module, populated_db):
        """Future dates should work but return no data."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("2030-01-01")
                        # Should return error or empty readings
                        assert "error" in result or len(result.get("readings", [])) == 0
    
    def test_very_old_date(self, cgm_module, populated_db):
        """Very old dates should work but return no data."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("2000-01-01")
                        # Should return error or empty readings
                        assert "error" in result or len(result.get("readings", [])) == 0
    
    def test_whitespace_in_date(self, cgm_module):
        """Dates with leading/trailing whitespace should work."""
        result = cgm_module.parse_date_arg("  today  ")
        assert result == datetime.now().date()
    
    def test_mixed_case_month(self, cgm_module):
        """Month names with mixed case should work."""
        result = cgm_module.parse_date_arg("JaNuArY 15")
        assert result.month == 1
        assert result.day == 15


class TestTimeRanges:
    """Tests for time range handling."""
    
    def test_inverted_hour_range(self, cgm_module, populated_db):
        """Inverted hour range (end < start) behavior."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        # Start > End (e.g., overnight: 22 to 6)
                        result = cgm_module.view_day("today", hour_start=22, hour_end=6)
                        # Should still work (might return no data for simple BETWEEN)
                        assert result is not None
    
    def test_same_start_end_hour(self, cgm_module, populated_db):
        """Same start and end hour should return that hour."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today", hour_start=12, hour_end=12)
                        # Should return readings for hour 12 only
                        for reading in result.get("readings", []):
                            hour = int(reading["time"].split(":")[0])
                            assert hour == 12


class TestGlucoseStatus:
    """Tests for glucose status categorization."""
    
    def test_all_status_categories(self, cgm_module, temp_db):
        """All status categories should be assigned correctly."""
        conn = sqlite3.connect(temp_db)
        now = datetime.now(timezone.utc)
        
        test_values = [
            (40, "very_low"),    # < 55
            (60, "low"),         # 55-69
            (100, "in_range"),   # 70-180
            (200, "high"),       # 181-250
            (300, "very_high"),  # > 250
        ]
        
        for i, (sgv, expected_status) in enumerate(test_values):
            dt = now - timedelta(minutes=i*5)
            conn.execute(
                "INSERT INTO readings (id, sgv, date_ms, date_string, direction) VALUES (?, ?, ?, ?, ?)",
                (f"test_{i}", sgv, int(dt.timestamp() * 1000), dt.isoformat(), "Flat")
            )
        conn.commit()
        conn.close()
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today")
                        
                        statuses = {r["glucose"]: r["status"] for r in result.get("readings", [])}
                        
                        for sgv, expected in test_values:
                            if sgv in statuses:
                                assert statuses[sgv] == expected


class TestMmolConversion:
    """Tests for mmol/L conversion in various scenarios."""
    
    def test_analysis_output_in_mmol(self, cgm_module, populated_db):
        """Analysis should output values in mmol/L when configured."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=True):
                    with patch.object(cgm_module, "get_unit_label", return_value="mmol/L"):
                        with patch.object(cgm_module, "get_thresholds", return_value={
                            "urgent_low": 55, "target_low": 70,
                            "target_high": 180, "urgent_high": 250
                        }):
                            result = cgm_module.analyze_cgm(days=7)
                            
                            assert result["unit"] == "mmol/L"
                            # Values should be in mmol range (typically 2-25)
                            assert result["statistics"]["mean"] < 30
    
    def test_view_day_in_mmol(self, cgm_module, populated_db):
        """Day view should show values in mmol/L when configured."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=True):
                    with patch.object(cgm_module, "get_unit_label", return_value="mmol/L"):
                        with patch.object(cgm_module, "get_thresholds", return_value={
                            "urgent_low": 55, "target_low": 70,
                            "target_high": 180, "urgent_high": 250
                        }):
                            result = cgm_module.view_day("today")
                            
                            assert result["unit"] == "mmol/L"
                            for reading in result.get("readings", []):
                                # Values should be in mmol range
                                assert reading["glucose"] < 30


class TestDataIntegrity:
    """Tests for data integrity checks."""
    
    def test_handles_null_values(self, cgm_module, temp_db):
        """Should handle NULL values in database."""
        conn = sqlite3.connect(temp_db)
        now = datetime.now(timezone.utc)
        
        # Insert reading with NULL direction
        conn.execute(
            "INSERT INTO readings (id, sgv, date_ms, date_string, direction) VALUES (?, ?, ?, ?, ?)",
            ("null_test", 120, int(now.timestamp() * 1000), now.isoformat(), None)
        )
        conn.commit()
        conn.close()
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today")
                        # Should not crash
                        assert result is not None
    
    def test_handles_invalid_date_string(self, cgm_module, temp_db):
        """Should handle invalid date strings in database."""
        conn = sqlite3.connect(temp_db)
        now = datetime.now(timezone.utc)
        
        # Insert reading with invalid date string
        conn.execute(
            "INSERT INTO readings (id, sgv, date_ms, date_string, direction) VALUES (?, ?, ?, ?, ?)",
            ("bad_date", 120, int(now.timestamp() * 1000), "not-a-date", "Flat")
        )
        conn.commit()
        conn.close()
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=1)
                        # Should not crash
                        assert result is not None
    
    def test_handles_zero_sgv(self, cgm_module, temp_db):
        """Should filter out zero SGV values."""
        conn = sqlite3.connect(temp_db)
        now = datetime.now(timezone.utc)
        
        # Insert readings including zero
        for i, sgv in enumerate([0, 120, 0, 140, 0]):
            dt = now - timedelta(minutes=i*5)
            conn.execute(
                "INSERT INTO readings (id, sgv, date_ms, date_string, direction) VALUES (?, ?, ?, ?, ?)",
                (f"zero_test_{i}", sgv, int(dt.timestamp() * 1000), dt.isoformat(), "Flat")
            )
        conn.commit()
        conn.close()
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=1)
                        # Should only count non-zero readings
                        assert result["readings"] == 2  # 120 and 140
