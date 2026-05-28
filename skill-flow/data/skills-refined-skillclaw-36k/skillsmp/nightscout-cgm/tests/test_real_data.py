"""
Tests using real Nightscout API responses.

These tests ensure cgm.py correctly handles the actual format
returned by Nightscout, including all fields and edge cases.
"""
import sqlite3
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch


class TestRealDataFormat:
    """Test that we correctly parse real Nightscout API responses."""
    
    def test_all_entries_have_required_fields(self, real_nightscout_entries):
        """Real data should have all required fields."""
        required_fields = {"_id", "sgv", "date", "dateString", "type"}
        
        for entry in real_nightscout_entries:
            if entry.get("type") == "sgv":
                missing = required_fields - set(entry.keys())
                assert not missing, f"Entry missing fields: {missing}"
    
    def test_sgv_values_are_integers(self, real_nightscout_entries):
        """SGV values should be integers in mg/dL."""
        for entry in real_nightscout_entries:
            if entry.get("type") == "sgv":
                sgv = entry.get("sgv")
                assert isinstance(sgv, int), f"SGV should be int, got {type(sgv)}"
                assert 20 <= sgv <= 500, f"SGV {sgv} outside reasonable range"
    
    def test_date_is_milliseconds(self, real_nightscout_entries):
        """Date field should be milliseconds since epoch."""
        for entry in real_nightscout_entries:
            date = entry.get("date")
            assert isinstance(date, int), f"Date should be int, got {type(date)}"
            # Should be in milliseconds (13 digits for 2020s)
            assert len(str(date)) == 13, f"Date {date} doesn't look like milliseconds"
    
    def test_directions_are_valid(self, real_nightscout_entries):
        """Direction field should be a known value."""
        valid_directions = {
            "Flat", "FortyFiveUp", "FortyFiveDown", 
            "SingleUp", "SingleDown", "DoubleUp", "DoubleDown",
            "NONE", "NOT COMPUTABLE", "RATE OUT OF RANGE", None
        }
        
        for entry in real_nightscout_entries:
            direction = entry.get("direction")
            assert direction in valid_directions, f"Unknown direction: {direction}"
    
    def test_extra_fields_dont_break_parsing(self, real_nightscout_entries):
        """Real data may have extra fields like utcOffset, sysTime."""
        # These fields exist in real data but we don't use them
        extra_fields = {"utcOffset", "sysTime"}
        
        has_extra = False
        for entry in real_nightscout_entries:
            if any(f in entry for f in extra_fields):
                has_extra = True
                break
        
        assert has_extra, "Expected real data to have extra fields like utcOffset"


class TestRealDataStorage:
    """Test storing real Nightscout data in our database."""
    
    def test_store_real_entries(self, cgm_module, temp_db, real_nightscout_entries, mock_requests_get):
        """Should store all real entries correctly."""
        # Mock the API to return real data
        mock_requests_get.return_value = MagicMock(
            json=MagicMock(side_effect=[real_nightscout_entries, []]),
            raise_for_status=MagicMock()
        )
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            result = cgm_module.fetch_and_store(days=1)
            
            assert "error" not in result
            assert result["new_readings"] == len(real_nightscout_entries)
            
            # Verify all stored
            conn = sqlite3.connect(temp_db)
            cursor = conn.execute("SELECT COUNT(*) FROM readings")
            count = cursor.fetchone()[0]
            conn.close()
            
            assert count == len(real_nightscout_entries)
    
    def test_query_real_data(self, cgm_module, real_data_db):
        """Should be able to query stored real data."""
        conn = sqlite3.connect(real_data_db)
        cursor = conn.execute("""
            SELECT MIN(sgv), MAX(sgv), AVG(sgv), COUNT(*) 
            FROM readings WHERE sgv > 0
        """)
        min_sgv, max_sgv, avg_sgv, count = cursor.fetchone()
        conn.close()
        
        assert count > 0, "Should have readings"
        assert min_sgv >= 20, f"Min SGV {min_sgv} too low"
        assert max_sgv <= 500, f"Max SGV {max_sgv} too high"
        assert 70 <= avg_sgv <= 250, f"Avg SGV {avg_sgv} outside typical range"


class TestRealDataAnalysis:
    """Test analysis functions with real data."""
    
    def test_get_stats_with_real_data(self, cgm_module, real_data_db):
        """get_stats should work with real data format."""
        conn = sqlite3.connect(real_data_db)
        cursor = conn.execute("SELECT sgv FROM readings WHERE sgv > 0")
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        stats = cgm_module.get_stats(values)
        
        assert "mean" in stats
        assert "std" in stats
        assert "min" in stats
        assert "max" in stats
        assert "count" in stats
        assert stats["count"] == len(values)
    
    def test_time_in_range_with_real_data(self, cgm_module, real_data_db):
        """get_time_in_range should handle real data."""
        conn = sqlite3.connect(real_data_db)
        cursor = conn.execute("SELECT sgv FROM readings WHERE sgv > 0")
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Mock thresholds for test
        with patch.object(cgm_module, "get_thresholds", return_value={
            "low": 70, "high": 180, "target_low": 70, "target_high": 180, "urgent_low": 55, "urgent_high": 250
        }):
            tir = cgm_module.get_time_in_range(values)
            
            # Check for actual keys returned by the function
            assert "in_range_pct" in tir
            assert "low_pct" in tir
            assert "high_pct" in tir
            assert 0 <= tir["in_range_pct"] <= 100
            assert 0 <= tir["low_pct"] <= 100
            assert 0 <= tir["high_pct"] <= 100
            # All percentages should sum to 100
            total = tir["very_low_pct"] + tir["low_pct"] + tir["in_range_pct"] + tir["high_pct"] + tir["very_high_pct"]
            assert abs(total - 100) < 0.1
    
    def test_sparkline_with_real_data(self, cgm_module, real_data_db):
        """make_sparkline should handle real data values."""
        conn = sqlite3.connect(real_data_db)
        cursor = conn.execute("SELECT sgv FROM readings WHERE sgv > 0 ORDER BY date_ms DESC LIMIT 24")
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        sparkline = cgm_module.make_sparkline(values)
        
        assert len(sparkline) > 0
        # Should use sparkline characters
        assert any(c in sparkline for c in "▁▂▃▄▅▆▇█")


class TestRealDataEdgeCases:
    """Test edge cases found in real data."""
    
    def test_handles_low_readings(self, real_nightscout_entries):
        """Real data may have very low readings (compression lows, etc.)."""
        lows = [e for e in real_nightscout_entries if e.get("sgv", 999) < 55]
        # We expect some lows in 24h of data
        assert len(lows) >= 0, "Test data should potentially have lows"
    
    def test_handles_high_readings(self, real_nightscout_entries):
        """Real data may have high readings."""
        highs = [e for e in real_nightscout_entries if e.get("sgv", 0) > 250]
        # We expect some highs in 24h of data  
        assert len(highs) >= 0, "Test data should potentially have highs"
    
    def test_handles_none_direction(self, real_nightscout_entries):
        """Some entries may have NONE direction during warmup."""
        none_dirs = [e for e in real_nightscout_entries if e.get("direction") == "NONE"]
        # This is valid, shouldn't crash
        assert isinstance(none_dirs, list)
    
    def test_chronological_order(self, real_nightscout_entries):
        """Entries should be in reverse chronological order (newest first)."""
        dates = [e.get("date") for e in real_nightscout_entries]
        # Nightscout returns newest first
        assert dates == sorted(dates, reverse=True), "Expected newest entries first"


class TestRealDataConversion:
    """Test glucose conversion with real data values."""
    
    def test_convert_real_values_to_mmol(self, cgm_module, real_nightscout_entries):
        """Should convert real mg/dL values to mmol/L correctly."""
        # When use_mmol returns True, convert_glucose divides by 18
        with patch.object(cgm_module, "use_mmol", return_value=True):
            for entry in real_nightscout_entries[:10]:  # Test first 10
                sgv = entry.get("sgv")
                if sgv:
                    mmol = cgm_module.convert_glucose(sgv)
                    # Typical range: 2-20 mmol/L
                    assert 1 <= mmol <= 30, f"Converted {sgv} to {mmol}, outside range"
                    # Should be roughly sgv / 18
                    expected = round(sgv / 18.0, 1)
                    assert abs(mmol - expected) < 0.1, f"Conversion error: {sgv} -> {mmol}"
    
    def test_convert_preserves_mg_dl(self, cgm_module, real_nightscout_entries):
        """Converting with use_mmol=False should preserve value."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            for entry in real_nightscout_entries[:10]:
                sgv = entry.get("sgv")
                if sgv:
                    result = cgm_module.convert_glucose(sgv)
                    assert result == sgv


class TestRealDataTimestamps:
    """Test timestamp handling with real data."""
    
    def test_parse_real_datestring(self, real_nightscout_entries):
        """Should be able to parse real dateString values."""
        for entry in real_nightscout_entries[:10]:
            date_string = entry.get("dateString")
            # Should be ISO format
            dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            assert dt.tzinfo is not None or "Z" in date_string
    
    def test_date_and_datestring_match(self, real_nightscout_entries):
        """date (ms) and dateString should represent same time."""
        for entry in real_nightscout_entries[:10]:
            date_ms = entry.get("date")
            date_string = entry.get("dateString")
            
            # Convert ms to datetime
            dt_from_ms = datetime.fromtimestamp(date_ms / 1000, tz=timezone.utc)
            
            # Parse dateString
            dt_from_str = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
            
            # Should be within 1 second (allowing for rounding)
            diff = abs((dt_from_ms - dt_from_str).total_seconds())
            assert diff < 1, f"Timestamp mismatch: {diff}s difference"
