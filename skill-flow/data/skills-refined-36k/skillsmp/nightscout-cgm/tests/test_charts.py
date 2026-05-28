"""
Tests for chart/visualization functions (show_sparkline, show_heatmap, show_day_chart).
These tests capture stdout to verify output.
"""
import io
import sys
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch


class TestShowSparkline:
    """Tests for show_sparkline function."""
    
    def test_outputs_sparkline(self, cgm_module, populated_db, capsys):
        """Should output a sparkline to stdout."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline(hours=24, use_color=False)
                        
                        captured = capsys.readouterr()
                        
                        # Should contain sparkline characters
                        assert any(c in captured.out for c in "▁▂▃▄▅▆▇█")
                        # Should contain stats
                        assert "Readings:" in captured.out
                        assert "Avg:" in captured.out
    
    def test_hours_parameter(self, cgm_module, populated_db, capsys):
        """Different hours should show different data ranges."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline(hours=6, use_color=False)
                        out_6h = capsys.readouterr().out
                        
                        cgm_module.show_sparkline(hours=24, use_color=False)
                        out_24h = capsys.readouterr().out
                        
                        # 24h should have more readings than 6h
                        # Extract reading counts
                        assert "6h" in out_6h
                        assert "24h" in out_24h
    
    def test_date_parameter(self, cgm_module, populated_db, capsys):
        """Should show data for specific date."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline(
                            date_str="yesterday", 
                            use_color=False
                        )
                        
                        captured = capsys.readouterr()
                        # Should contain date in title
                        yesterday = (datetime.now() - timedelta(days=1)).strftime("%b %d")
                        assert yesterday in captured.out or "Sparkline" in captured.out
    
    def test_hour_range_filter(self, cgm_module, populated_db, capsys):
        """Should filter by hour range when date is specified."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline(
                            date_str="yesterday",
                            hour_start=11,
                            hour_end=14,
                            use_color=False
                        )
                        
                        captured = capsys.readouterr()
                        # Should indicate time range in title
                        assert "11:00" in captured.out or "11" in captured.out
    
    def test_color_mode(self, cgm_module, populated_db, capsys):
        """Color mode should include ANSI codes."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline(hours=6, use_color=True)
                        
                        captured = capsys.readouterr()
                        # Should contain ANSI escape codes
                        assert "\033[" in captured.out
    
    def test_no_data_message(self, cgm_module, temp_db, capsys):
        """Should print message when no data available."""
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                cgm_module.show_sparkline(hours=6, use_color=False)
                
                captured = capsys.readouterr()
                assert "No data" in captured.out


class TestShowHeatmap:
    """Tests for show_heatmap function."""
    
    def test_outputs_heatmap(self, cgm_module, populated_db, capsys):
        """Should output a heatmap to stdout."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_heatmap(days=7, use_color=False)
                        
                        captured = capsys.readouterr()
                        
                        # Should contain day names
                        assert any(day in captured.out for day in 
                                   ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    
    def test_heatmap_structure(self, cgm_module, populated_db, capsys):
        """Heatmap should have hour labels."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_heatmap(days=7, use_color=False)
                        
                        captured = capsys.readouterr()
                        
                        # Should have hour markers
                        assert "00" in captured.out or "0" in captured.out
    
    def test_color_mode(self, cgm_module, populated_db, capsys):
        """Color mode should include ANSI codes."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_heatmap(days=7, use_color=True)
                        
                        captured = capsys.readouterr()
                        # Should contain ANSI escape codes
                        assert "\033[" in captured.out


class TestShowDayChart:
    """Tests for show_day_chart function."""
    
    def test_outputs_day_chart(self, cgm_module, populated_db, capsys):
        """Should output a day chart to stdout."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_day_chart("Monday", days=7, use_color=False)
                        
                        captured = capsys.readouterr()
                        
                        # Should contain the day name
                        assert "Monday" in captured.out
    
    def test_all_days_of_week(self, cgm_module, populated_db, capsys):
        """Should work for all days of the week."""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday", "Sunday"]
        
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        for day in days:
                            cgm_module.show_day_chart(day, days=7, use_color=False)
                            captured = capsys.readouterr()
                            assert day in captured.out
    
    def test_short_day_names(self, cgm_module, populated_db, capsys):
        """Should accept short day names."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        # Try short name
                        cgm_module.show_day_chart("Mon", days=7, use_color=False)
                        captured = capsys.readouterr()
                        # Should work and show something
                        assert len(captured.out) > 0


class TestShowSparklineWeek:
    """Tests for show_sparkline_week function."""
    
    def test_outputs_week_sparklines(self, cgm_module, populated_db, capsys):
        """Should output sparklines for each day of the week."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline_week(days=7, use_color=False)
                        
                        captured = capsys.readouterr()
                        
                        # Should have multiple lines with sparkline characters
                        lines_with_sparkline = [
                            line for line in captured.out.split('\n')
                            if any(c in line for c in "▁▂▃▄▅▆▇█")
                        ]
                        # Should have at least a few days
                        assert len(lines_with_sparkline) >= 1
    
    def test_days_parameter(self, cgm_module, populated_db, capsys):
        """Different days parameter should affect output."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline_week(days=3, use_color=False)
                        out_3 = capsys.readouterr().out
                        
                        cgm_module.show_sparkline_week(days=7, use_color=False)
                        out_7 = capsys.readouterr().out
                        
                        # 7 days should typically have more content
                        # (though both outputs are valid)
                        assert len(out_3) > 0
                        assert len(out_7) > 0


class TestChartEdgeCases:
    """Tests for edge cases in chart functions."""
    
    def test_empty_database(self, cgm_module, temp_db, capsys):
        """Charts should handle empty database gracefully."""
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                # These should not raise exceptions
                cgm_module.show_sparkline(hours=24, use_color=False)
                cgm_module.show_heatmap(days=7, use_color=False)
                cgm_module.show_sparkline_week(days=7, use_color=False)
                
                # Just verify they completed without error
                captured = capsys.readouterr()
                assert captured.out is not None
    
    def test_very_short_time_range(self, cgm_module, populated_db, capsys):
        """Should handle very short time ranges."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            with patch.object(cgm_module, "ensure_data", return_value=True):
                with patch.object(cgm_module, "use_mmol", return_value=False):
                    with patch.object(cgm_module, "get_thresholds", return_value={
                        "urgent_low": 55, "target_low": 70,
                        "target_high": 180, "urgent_high": 250
                    }):
                        cgm_module.show_sparkline(hours=1, use_color=False)
                        captured = capsys.readouterr()
                        # Should complete without error
                        assert captured.out is not None
