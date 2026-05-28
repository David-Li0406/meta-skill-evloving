"""
Tests for database operations.
"""
import sqlite3
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock


class TestCreateDatabase:
    """Tests for create_database function."""
    
    def test_creates_readings_table(self, cgm_module, tmp_path):
        """Database should have readings table with correct schema."""
        db_path = tmp_path / "test_db.db"
        with patch.object(cgm_module, "DB_PATH", db_path):
            conn = cgm_module.create_database()
            
            # Check table exists
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='readings'"
            )
            assert cursor.fetchone() is not None
            
            # Check columns
            cursor = conn.execute("PRAGMA table_info(readings)")
            columns = {row[1]: row[2] for row in cursor.fetchall()}
            
            assert "id" in columns
            assert "sgv" in columns
            assert "date_ms" in columns
            assert "date_string" in columns
            assert "trend" in columns
            assert "direction" in columns
            assert "device" in columns
            
            conn.close()
    
    def test_idempotent(self, cgm_module, tmp_path):
        """Creating database multiple times should be safe."""
        db_path = tmp_path / "test_db.db"
        with patch.object(cgm_module, "DB_PATH", db_path):
            conn1 = cgm_module.create_database()
            conn1.close()
            
            # Create again - should not raise
            conn2 = cgm_module.create_database()
            conn2.close()
            
            # Should still work
            conn3 = sqlite3.connect(db_path)
            cursor = conn3.execute("SELECT COUNT(*) FROM readings")
            assert cursor.fetchone()[0] == 0
            conn3.close()


class TestEnsureData:
    """Tests for ensure_data function."""
    
    def test_returns_true_with_existing_data(self, cgm_module, populated_db):
        """Should return True when data exists."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            result = cgm_module.ensure_data(days=7)
            assert result is True
    
    def test_fetches_when_empty(self, cgm_module, temp_db):
        """Should attempt to fetch when database is empty."""
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "fetch_and_store") as mock_fetch:
                mock_fetch.return_value = {"new_readings": 100, "total_readings": 100}
                
                # First call should trigger fetch
                cgm_module.ensure_data(days=7)
                mock_fetch.assert_called_once()
    
    def test_returns_false_on_fetch_error(self, cgm_module, temp_db):
        """Should return False when fetch fails."""
        with patch.object(cgm_module, "DB_PATH", temp_db):
            with patch.object(cgm_module, "fetch_and_store") as mock_fetch:
                mock_fetch.return_value = {"error": "Connection failed"}
                
                result = cgm_module.ensure_data(days=7)
                assert result is False


class TestFetchAndStore:
    """Tests for fetch_and_store function."""
    
    def test_stores_readings(self, cgm_module, temp_db, mock_requests_get):
        """Should store fetched readings in database."""
        # Mock Nightscout response
        now = datetime.now(timezone.utc)
        mock_entries = [
            {
                "_id": "entry1",
                "sgv": 120,
                "date": int(now.timestamp() * 1000),
                "dateString": now.isoformat(),
                "trend": 5,
                "direction": "Flat",
                "device": "test",
                "type": "sgv"
            },
            {
                "_id": "entry2",
                "sgv": 130,
                "date": int((now - timedelta(minutes=5)).timestamp() * 1000),
                "dateString": (now - timedelta(minutes=5)).isoformat(),
                "trend": 4,
                "direction": "FortyFiveUp",
                "device": "test",
                "type": "sgv"
            }
        ]
        
        mock_requests_get.return_value = MagicMock(
            json=MagicMock(side_effect=[mock_entries, []]),
            raise_for_status=MagicMock()
        )
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            result = cgm_module.fetch_and_store(days=1)
            
            assert "error" not in result
            assert result["new_readings"] == 2
            
            # Verify data in database
            conn = sqlite3.connect(temp_db)
            cursor = conn.execute("SELECT COUNT(*) FROM readings")
            assert cursor.fetchone()[0] == 2
            conn.close()
    
    def test_handles_api_error(self, cgm_module, temp_db, mock_requests_get):
        """Should return error dict on API failure."""
        import requests
        mock_requests_get.side_effect = requests.RequestException("Connection failed")
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            result = cgm_module.fetch_and_store(days=1)
            
            assert "error" in result
    
    def test_skips_non_sgv_entries(self, cgm_module, temp_db, mock_requests_get):
        """Should skip non-SGV entries (like calibrations)."""
        now = datetime.now(timezone.utc)
        mock_entries = [
            {
                "_id": "entry1",
                "sgv": 120,
                "date": int(now.timestamp() * 1000),
                "dateString": now.isoformat(),
                "type": "sgv"  # Valid
            },
            {
                "_id": "cal1",
                "slope": 1000,
                "date": int(now.timestamp() * 1000),
                "type": "cal"  # Calibration - should skip
            }
        ]
        
        mock_requests_get.return_value = MagicMock(
            json=MagicMock(side_effect=[mock_entries, []]),
            raise_for_status=MagicMock()
        )
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            result = cgm_module.fetch_and_store(days=1)
            
            assert result["new_readings"] == 1
    
    def test_deduplicates_readings(self, cgm_module, temp_db, mock_requests_get):
        """Should not duplicate readings on repeated fetch."""
        now = datetime.now(timezone.utc)
        mock_entry = {
            "_id": "entry1",
            "sgv": 120,
            "date": int(now.timestamp() * 1000),
            "dateString": now.isoformat(),
            "type": "sgv"
        }
        
        mock_requests_get.return_value = MagicMock(
            json=MagicMock(side_effect=[[mock_entry], [], [mock_entry], []]),
            raise_for_status=MagicMock()
        )
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            # First fetch
            result1 = cgm_module.fetch_and_store(days=1)
            # Second fetch with same data
            result2 = cgm_module.fetch_and_store(days=1)
            
            # Should only have 1 reading total
            conn = sqlite3.connect(temp_db)
            cursor = conn.execute("SELECT COUNT(*) FROM readings")
            assert cursor.fetchone()[0] == 1
            conn.close()


class TestDatabaseIntegrity:
    """Tests for database integrity and edge cases."""
    
    def test_handles_missing_fields(self, cgm_module, temp_db, mock_requests_get):
        """Should handle entries with missing optional fields."""
        now = datetime.now(timezone.utc)
        mock_entry = {
            "_id": "entry1",
            "sgv": 120,
            "date": int(now.timestamp() * 1000),
            "dateString": now.isoformat(),
            "type": "sgv"
            # Missing: trend, direction, device
        }
        
        mock_requests_get.return_value = MagicMock(
            json=MagicMock(side_effect=[[mock_entry], []]),
            raise_for_status=MagicMock()
        )
        
        with patch.object(cgm_module, "DB_PATH", temp_db):
            result = cgm_module.fetch_and_store(days=1)
            assert "error" not in result
    
    def test_concurrent_access(self, cgm_module, populated_db):
        """Database should handle concurrent read access."""
        with patch.object(cgm_module, "DB_PATH", populated_db):
            # Simulate multiple reads
            results = []
            for _ in range(5):
                conn = sqlite3.connect(populated_db)
                cursor = conn.execute("SELECT COUNT(*) FROM readings")
                results.append(cursor.fetchone()[0])
                conn.close()
            
            # All should return same count
            assert len(set(results)) == 1
