"""
Tests for analysis functions (analyze_cgm, query_patterns, find_patterns, view_day, find_worst_days).
"""
import sqlite3
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock


class TestAnalyzeCgm:
    """Tests for analyze_cgm function."""
    
    def test_basic_analysis(self, cgm_module, populated_db):
        """Should return complete analysis structure."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70, 
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=7)
                        
                        # Check structure
                        assert "date_range" in result
                        assert "readings" in result
                        assert "statistics" in result
                        assert "time_in_range" in result
                        assert "gmi_estimated_a1c" in result
                        assert "cv_variability" in result
                        assert "hourly_averages" in result
    
    def test_returns_error_when_no_data(self, cgm_module, temp_db):
        """Should return error when no data available."""
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=False):
                result = cgm_module.analyze_cgm(days=7)
                assert "error" in result
    
    def test_gmi_calculation(self, cgm_module, populated_db):
        """GMI should be calculated correctly."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=7)
                        
                        # GMI should be reasonable (typically 5.0-10.0)
                        assert 5.0 <= result["gmi_estimated_a1c"] <= 10.0
    
    def test_cv_status(self, cgm_module, populated_db):
        """CV status should be 'stable' or 'high variability'."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=7)
                        
                        assert result["cv_status"] in ["stable", "high variability"]
                        if result["cv_variability"] < 36:
                            assert result["cv_status"] == "stable"
                        else:
                            assert result["cv_status"] == "high variability"
    
    def test_hourly_averages_has_24_hours(self, cgm_module, populated_db):
        """Hourly averages should cover all 24 hours."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.analyze_cgm(days=7)
                        
                        # Should have entries for most hours
                        assert len(result["hourly_averages"]) >= 20
    
    def test_days_parameter(self, cgm_module, populated_db):
        """Different days parameter should affect results."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result_7 = cgm_module.analyze_cgm(days=7)
                        result_1 = cgm_module.analyze_cgm(days=1)
                        
                        # 7 days should have more readings than 1 day
                        assert result_7["readings"] >= result_1["readings"]


class TestQueryPatterns:
    """Tests for query_patterns function."""
    
    def test_basic_query(self, cgm_module, populated_db):
        """Should return query results structure."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.query_patterns(days=7)
                        
                        assert "statistics" in result
                        assert "time_in_range" in result
    
    def test_day_of_week_filter(self, cgm_module, populated_db):
        """Should filter by day of week."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.query_patterns(days=7, day_of_week="Monday")
                        
                        assert "filter" in result
                        assert "Monday" in result["filter"]
    
    def test_hour_range_filter(self, cgm_module, populated_db):
        """Should filter by hour range."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.query_patterns(
                            days=7, hour_start=12, hour_end=14
                        )
                        
                        assert "filter" in result
                        assert "12:00" in result["filter"]
    
    def test_combined_filters(self, cgm_module, populated_db):
        """Should handle combined day and hour filters."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.query_patterns(
                            days=7, 
                            day_of_week="Tuesday",
                            hour_start=11,
                            hour_end=14
                        )
                        
                        assert "filter" in result
                        assert "Tuesday" in result["filter"]
                        assert "11:00" in result["filter"]


class TestFindPatterns:
    """Tests for find_patterns function."""
    
    def test_returns_insights(self, cgm_module, populated_db):
        """Should return pattern insights."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_patterns(days=7)
                        
                        assert "insights" in result
                        insights = result["insights"]
                        
                        assert "best_time_of_day" in insights
                        assert "worst_time_of_day" in insights
                        assert "best_day" in insights
                        assert "worst_day" in insights
    
    def test_best_worst_times(self, cgm_module, populated_db):
        """Best and worst times should have required fields."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_patterns(days=7)
                        
                        best_time = result["insights"]["best_time_of_day"]
                        worst_time = result["insights"]["worst_time_of_day"]
                        
                        assert "hour" in best_time
                        assert "time_in_range" in best_time
                        assert "hour" in worst_time
                        assert "time_in_range" in worst_time
                        
                        # Best should have higher TIR than worst
                        assert best_time["time_in_range"] >= worst_time["time_in_range"]
    
    def test_problem_times(self, cgm_module, populated_db):
        """Should identify problem time combinations."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_patterns(days=7)
                        
                        assert "problem_times" in result["insights"]
                        # Should be a list
                        assert isinstance(result["insights"]["problem_times"], list)


class TestViewDay:
    """Tests for view_day function."""
    
    def test_view_today(self, cgm_module, populated_db):
        """Should return readings for today."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today")
                        
                        assert "date" in result
                        assert "readings" in result
                        assert "statistics" in result
    
    def test_view_yesterday(self, cgm_module, populated_db):
        """Should return readings for yesterday."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("yesterday")
                        
                        expected_date = (datetime.now() - timedelta(days=1)).date().isoformat()
                        assert result["date"] == expected_date
    
    def test_hour_filter(self, cgm_module, populated_db):
        """Should filter by hour range."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today", hour_start=12, hour_end=14)
                        
                        assert result["filter"] == "hours=12:00-14:00"
                        
                        # All readings should be within hour range
                        for reading in result.get("readings", []):
                            hour = int(reading["time"].split(":")[0])
                            assert 12 <= hour <= 14
    
    def test_statistics_included(self, cgm_module, populated_db):
        """Should include statistics for the day."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today")
                        
                        stats = result["statistics"]
                        assert "average" in stats
                        assert "min" in stats
                        assert "max" in stats
                        assert "time_in_range_pct" in stats
                        assert "peak_time" in stats
                        assert "trough_time" in stats
    
    def test_invalid_date(self, cgm_module, populated_db):
        """Should return error for invalid date."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                result = cgm_module.view_day("not-a-date")
                assert "error" in result
    
    def test_readings_have_status(self, cgm_module, populated_db):
        """Each reading should have a status field."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.view_day("today")
                        
                        for reading in result.get("readings", []):
                            assert "status" in reading
                            assert reading["status"] in [
                                "very_low", "low", "in_range", "high", "very_high"
                            ]


class TestFindWorstDays:
    """Tests for find_worst_days function."""
    
    def test_returns_worst_days(self, cgm_module, populated_db):
        """Should return list of worst days."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_worst_days(days=7)
                        
                        assert "worst_days" in result
                        assert isinstance(result["worst_days"], list)
    
    def test_limit_parameter(self, cgm_module, populated_db):
        """Should respect limit parameter."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_worst_days(days=7, limit=3)
                        
                        assert len(result["worst_days"]) <= 3
    
    def test_sorted_by_peak(self, cgm_module, populated_db):
        """Results should be sorted by peak glucose (descending)."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_worst_days(days=7, limit=5)
                        
                        worst_days = result["worst_days"]
                        if len(worst_days) > 1:
                            peaks = [d["peak"] for d in worst_days]
                            assert peaks == sorted(peaks, reverse=True)
    
    def test_hour_filter(self, cgm_module, populated_db):
        """Should filter by hour range."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_worst_days(
                            days=7, hour_start=11, hour_end=14
                        )
                        
                        assert result["filter"] == "hours=11:00-14:00"
    
    def test_worst_day_fields(self, cgm_module, populated_db):
        """Each worst day should have required fields."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        result = cgm_module.find_worst_days(days=7)
                        
                        for day in result["worst_days"]:
                            assert "date" in day
                            assert "peak" in day
                            assert "trough" in day
                            assert "average" in day
                            assert "time_in_range_pct" in day
                            assert "high_readings" in day
                            assert "low_readings" in day
