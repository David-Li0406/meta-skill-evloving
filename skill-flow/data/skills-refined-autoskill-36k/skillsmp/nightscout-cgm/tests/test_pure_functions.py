"""
Tests for pure functions that don't require I/O.
These are the easiest to test and most critical for correctness.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock


class TestConvertGlucose:
    """Tests for convert_glucose function."""
    
    def test_mg_dl_mode_returns_unchanged(self, cgm_module):
        """In mg/dL mode, values should be returned unchanged."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            assert cgm_module.convert_glucose(100) == 100
            assert cgm_module.convert_glucose(180) == 180
            assert cgm_module.convert_glucose(55) == 55
    
    def test_mmol_mode_converts_correctly(self, cgm_module):
        """In mmol/L mode, values should be converted from mg/dL."""
        with patch.object(cgm_module, "use_mmol", return_value=True):
            # 180 mg/dL ≈ 10.0 mmol/L
            assert cgm_module.convert_glucose(180) == pytest.approx(10.0, rel=0.1)
            # 100 mg/dL ≈ 5.6 mmol/L
            assert cgm_module.convert_glucose(100) == pytest.approx(5.6, rel=0.1)
            # 70 mg/dL ≈ 3.9 mmol/L
            assert cgm_module.convert_glucose(70) == pytest.approx(3.9, rel=0.1)
    
    def test_zero_value(self, cgm_module):
        """Zero should return zero in both modes."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            assert cgm_module.convert_glucose(0) == 0
        with patch.object(cgm_module, "use_mmol", return_value=True):
            assert cgm_module.convert_glucose(0) == 0.0
    
    def test_extreme_values(self, cgm_module):
        """Test with extreme glucose values."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            assert cgm_module.convert_glucose(40) == 40
            assert cgm_module.convert_glucose(400) == 400
        with patch.object(cgm_module, "use_mmol", return_value=True):
            # 40 mg/dL ≈ 2.2 mmol/L
            assert cgm_module.convert_glucose(40) == pytest.approx(2.2, rel=0.1)
            # 400 mg/dL ≈ 22.2 mmol/L
            assert cgm_module.convert_glucose(400) == pytest.approx(22.2, rel=0.1)


class TestGetStats:
    """Tests for get_stats function."""
    
    def test_basic_statistics(self, cgm_module):
        """Test basic statistical calculations."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            with patch.object(cgm_module, "get_unit_label", return_value="mg/dL"):
                values = [100, 120, 140, 160, 180]
                stats = cgm_module.get_stats(values)
                
                assert stats["count"] == 5
                assert stats["mean"] == 140.0
                assert stats["min"] == 100
                assert stats["max"] == 180
                assert stats["median"] == 140
                assert stats["unit"] == "mg/dL"
    
    def test_empty_values(self, cgm_module):
        """Empty list should return empty dict."""
        assert cgm_module.get_stats([]) == {}
    
    def test_single_value(self, cgm_module):
        """Single value should work correctly."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            with patch.object(cgm_module, "get_unit_label", return_value="mg/dL"):
                stats = cgm_module.get_stats([150])
                
                assert stats["count"] == 1
                assert stats["mean"] == 150.0
                assert stats["min"] == 150
                assert stats["max"] == 150
                assert stats["median"] == 150
                assert stats["std"] == 0.0
    
    def test_standard_deviation(self, cgm_module):
        """Test standard deviation calculation."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            with patch.object(cgm_module, "get_unit_label", return_value="mg/dL"):
                # Values with known std dev
                values = [100, 100, 100, 100, 100]  # std = 0
                stats = cgm_module.get_stats(values)
                assert stats["std"] == 0.0
                
                # More varied values
                values = [80, 100, 120, 140, 160]
                stats = cgm_module.get_stats(values)
                assert stats["std"] > 0
    
    def test_unsorted_input(self, cgm_module):
        """Function should handle unsorted input."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            with patch.object(cgm_module, "get_unit_label", return_value="mg/dL"):
                values = [180, 100, 160, 120, 140]
                stats = cgm_module.get_stats(values)
                
                assert stats["min"] == 100
                assert stats["max"] == 180


class TestGetTimeInRange:
    """Tests for get_time_in_range function."""
    
    def test_all_in_range(self, cgm_module):
        """Test with all values in target range."""
        with patch.object(cgm_module, "get_thresholds", return_value={
            "urgent_low": 55, "target_low": 70, "target_high": 180, "urgent_high": 250
        }):
            values = [100, 120, 140, 160, 170]
            tir = cgm_module.get_time_in_range(values)
            
            assert tir["in_range_pct"] == 100.0
            assert tir["very_low_pct"] == 0.0
            assert tir["low_pct"] == 0.0
            assert tir["high_pct"] == 0.0
            assert tir["very_high_pct"] == 0.0
    
    def test_all_very_low(self, cgm_module):
        """Test with all values very low."""
        with patch.object(cgm_module, "get_thresholds", return_value={
            "urgent_low": 55, "target_low": 70, "target_high": 180, "urgent_high": 250
        }):
            values = [40, 45, 50, 52, 54]
            tir = cgm_module.get_time_in_range(values)
            
            assert tir["very_low_pct"] == 100.0
            assert tir["in_range_pct"] == 0.0
    
    def test_all_very_high(self, cgm_module):
        """Test with all values very high."""
        with patch.object(cgm_module, "get_thresholds", return_value={
            "urgent_low": 55, "target_low": 70, "target_high": 180, "urgent_high": 250
        }):
            values = [260, 280, 300, 350, 400]
            tir = cgm_module.get_time_in_range(values)
            
            assert tir["very_high_pct"] == 100.0
            assert tir["in_range_pct"] == 0.0
    
    def test_mixed_ranges(self, cgm_module, sample_glucose_values):
        """Test with values across all ranges."""
        with patch.object(cgm_module, "get_thresholds", return_value={
            "urgent_low": 55, "target_low": 70, "target_high": 180, "urgent_high": 250
        }):
            tir = cgm_module.get_time_in_range(sample_glucose_values)
            
            # Verify all percentages sum to 100
            total = (tir["very_low_pct"] + tir["low_pct"] + tir["in_range_pct"] + 
                     tir["high_pct"] + tir["very_high_pct"])
            assert total == pytest.approx(100.0, rel=0.01)
            
            # Verify each category has some readings
            assert tir["very_low_pct"] > 0
            assert tir["low_pct"] > 0
            assert tir["in_range_pct"] > 0
            assert tir["high_pct"] > 0
            assert tir["very_high_pct"] > 0
    
    def test_empty_values(self, cgm_module):
        """Empty list should return empty dict."""
        assert cgm_module.get_time_in_range([]) == {}
    
    def test_boundary_values(self, cgm_module):
        """Test values exactly on boundaries."""
        with patch.object(cgm_module, "get_thresholds", return_value={
            "urgent_low": 55, "target_low": 70, "target_high": 180, "urgent_high": 250
        }):
            # Test exact boundary values
            values = [55, 70, 180, 250]
            tir = cgm_module.get_time_in_range(values)
            
            # 55 is at urgent_low boundary - should be in "low" range (>= urgent_low, < target_low)
            # 70 is at target_low boundary - should be "in_range"
            # 180 is at target_high boundary - should be "in_range"
            # 250 is at urgent_high boundary - should be "high" range
            assert tir["in_range_pct"] == 50.0  # 70 and 180


class TestMakeSparkline:
    """Tests for make_sparkline function."""
    
    def test_basic_sparkline(self, cgm_module):
        """Test basic sparkline generation."""
        values = [100, 150, 200, 250, 300]
        sparkline = cgm_module.make_sparkline(values)
        
        assert isinstance(sparkline, str)
        assert len(sparkline) == len(values)
        # Should use Unicode block characters
        assert all(c in " ▁▂▃▄▅▆▇█" for c in sparkline)
    
    def test_constant_values(self, cgm_module):
        """Constant values should produce uniform sparkline."""
        values = [150, 150, 150, 150, 150]
        sparkline = cgm_module.make_sparkline(values)
        
        # All characters should be the same
        assert len(set(sparkline)) == 1
    
    def test_increasing_values(self, cgm_module):
        """Increasing values should produce ascending sparkline."""
        values = [40, 100, 200, 300, 400]
        sparkline = cgm_module.make_sparkline(values)
        
        # First char should be lowest, last should be highest
        blocks = " ▁▂▃▄▅▆▇█"
        first_idx = blocks.index(sparkline[0])
        last_idx = blocks.index(sparkline[-1])
        assert first_idx < last_idx
    
    def test_custom_range(self, cgm_module):
        """Test with custom min/max range."""
        values = [50, 100, 150]
        sparkline = cgm_module.make_sparkline(values, min_val=0, max_val=200)
        
        assert isinstance(sparkline, str)
        assert len(sparkline) == 3
    
    def test_empty_values(self, cgm_module):
        """Empty list should return empty string."""
        sparkline = cgm_module.make_sparkline([])
        assert sparkline == ""
    
    def test_single_value(self, cgm_module):
        """Single value should return single character."""
        sparkline = cgm_module.make_sparkline([150])
        assert len(sparkline) == 1


class TestParseDateArg:
    """Tests for parse_date_arg function."""
    
    def test_today(self, cgm_module):
        """'today' should return today's date."""
        result = cgm_module.parse_date_arg("today")
        assert result == datetime.now().date()
    
    def test_yesterday(self, cgm_module):
        """'yesterday' should return yesterday's date."""
        result = cgm_module.parse_date_arg("yesterday")
        expected = (datetime.now() - timedelta(days=1)).date()
        assert result == expected
    
    def test_iso_format(self, cgm_module):
        """ISO format dates should parse correctly."""
        result = cgm_module.parse_date_arg("2026-01-15")
        assert result.year == 2026
        assert result.month == 1
        assert result.day == 15
    
    def test_short_month_format(self, cgm_module):
        """Short month format should parse correctly."""
        result = cgm_module.parse_date_arg("Jan 15")
        assert result.month == 1
        assert result.day == 15
    
    def test_full_month_format(self, cgm_module):
        """Full month format should parse correctly."""
        result = cgm_module.parse_date_arg("January 15")
        assert result.month == 1
        assert result.day == 15
    
    def test_case_insensitive(self, cgm_module):
        """Date parsing should be case insensitive."""
        result1 = cgm_module.parse_date_arg("TODAY")
        result2 = cgm_module.parse_date_arg("Today")
        result3 = cgm_module.parse_date_arg("today")
        
        assert result1 == result2 == result3
    
    def test_invalid_date_raises(self, cgm_module):
        """Invalid date should raise ValueError."""
        with pytest.raises(ValueError):
            cgm_module.parse_date_arg("not-a-date")
        
        with pytest.raises(ValueError):
            cgm_module.parse_date_arg("32/13/2026")
    
    def test_slash_format(self, cgm_module):
        """Slash format should work."""
        result = cgm_module.parse_date_arg("01/15")
        assert result.month == 1
        assert result.day == 15


class TestGetThresholds:
    """Tests for get_thresholds function."""
    
    def test_default_thresholds(self, cgm_module):
        """Test default thresholds when Nightscout returns empty."""
        with patch.object(cgm_module, "get_nightscout_settings", return_value={}):
            thresholds = cgm_module.get_thresholds()
            
            assert thresholds["urgent_low"] == 55
            assert thresholds["target_low"] == 70
            assert thresholds["target_high"] == 180
            assert thresholds["urgent_high"] == 250
    
    def test_custom_thresholds(self, cgm_module):
        """Test custom thresholds from Nightscout."""
        with patch.object(cgm_module, "get_nightscout_settings", return_value={
            "thresholds": {
                "bgLow": 50,
                "bgTargetBottom": 80,
                "bgTargetTop": 160,
                "bgHigh": 220
            }
        }):
            thresholds = cgm_module.get_thresholds()
            
            assert thresholds["urgent_low"] == 50
            assert thresholds["target_low"] == 80
            assert thresholds["target_high"] == 160
            assert thresholds["urgent_high"] == 220


class TestUseMmol:
    """Tests for use_mmol function."""
    
    def test_mg_dl_setting(self, cgm_module):
        """mg/dL setting should return False."""
        with patch.object(cgm_module, "get_nightscout_settings", return_value={"units": "mg/dl"}):
            assert cgm_module.use_mmol() is False
    
    def test_mmol_setting(self, cgm_module):
        """mmol setting should return True."""
        with patch.object(cgm_module, "get_nightscout_settings", return_value={"units": "mmol"}):
            assert cgm_module.use_mmol() is True
    
    def test_mmol_l_setting(self, cgm_module):
        """mmol/L setting should return True."""
        with patch.object(cgm_module, "get_nightscout_settings", return_value={"units": "mmol/L"}):
            assert cgm_module.use_mmol() is True
    
    def test_default_is_mg_dl(self, cgm_module):
        """Default (no setting) should be mg/dL."""
        with patch.object(cgm_module, "get_nightscout_settings", return_value={}):
            assert cgm_module.use_mmol() is False


class TestGetUnitLabel:
    """Tests for get_unit_label function."""
    
    def test_mg_dl_label(self, cgm_module):
        """mg/dL mode should return 'mg/dL'."""
        with patch.object(cgm_module, "use_mmol", return_value=False):
            assert cgm_module.get_unit_label() == "mg/dL"
    
    def test_mmol_label(self, cgm_module):
        """mmol mode should return 'mmol/L'."""
        with patch.object(cgm_module, "use_mmol", return_value=True):
            assert cgm_module.get_unit_label() == "mmol/L"
