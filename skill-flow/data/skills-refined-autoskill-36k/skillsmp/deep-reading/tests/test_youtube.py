"""Tests for fetcher/youtube.py"""
import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestExtractVideoId:
    """Tests for extract_video_id function"""

    def test_extract_from_standard_url(self, monkeypatch, temp_dir):
        """Test extracting ID from standard YouTube URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import extract_video_id

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_from_short_url(self, monkeypatch, temp_dir):
        """Test extracting ID from youtu.be URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import extract_video_id

        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_from_shorts_url(self, monkeypatch, temp_dir):
        """Test extracting ID from YouTube Shorts URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import extract_video_id

        url = "https://www.youtube.com/shorts/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_from_embed_url(self, monkeypatch, temp_dir):
        """Test extracting ID from embed URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import extract_video_id

        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_with_extra_params(self, monkeypatch, temp_dir):
        """Test extracting ID from URL with extra parameters"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import extract_video_id

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLtest&index=1"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_extract_invalid_url(self, monkeypatch, temp_dir):
        """Test extracting ID from invalid URL returns None"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import extract_video_id

        url = "https://example.com/video"
        assert extract_video_id(url) is None


class TestGetCacheDir:
    """Tests for get_cache_dir function"""

    def test_get_cache_dir_creates_directory(self, monkeypatch, temp_dir):
        """Test that get_cache_dir creates the directory"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import get_cache_dir

        cache_dir = get_cache_dir("test123")
        assert cache_dir.exists()
        assert cache_dir == temp_dir / "cache" / "youtube" / "test123"


class TestFetchMetadata:
    """Tests for fetch_metadata function"""

    def test_fetch_metadata_success(self, monkeypatch, temp_dir):
        """Test successful metadata fetch"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_metadata

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "title": "Test Video",
            "channel": "Test Channel",
            "duration": 300,
            "description": "Test description",
            "upload_date": "20260121"
        })

        with patch('subprocess.run', return_value=mock_result):
            metadata = fetch_metadata("https://youtube.com/watch?v=test", "test123")

        assert metadata["title"] == "Test Video"
        assert metadata["author"] == "Test Channel"
        assert metadata["duration"] == 300

        # Check that metadata was saved
        metadata_file = temp_dir / "cache" / "youtube" / "test123" / "metadata.json"
        assert metadata_file.exists()

    def test_fetch_metadata_uses_uploader_fallback(self, monkeypatch, temp_dir):
        """Test that uploader is used when channel is not available"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_metadata

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "title": "Test Video",
            "uploader": "Test Uploader",
            "duration": 300
        })

        with patch('subprocess.run', return_value=mock_result):
            metadata = fetch_metadata("https://youtube.com/watch?v=test", "test123")

        assert metadata["author"] == "Test Uploader"

    def test_fetch_metadata_failure(self, monkeypatch, temp_dir):
        """Test metadata fetch failure raises exception"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_metadata

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error fetching metadata"

        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(Exception, match="Failed to fetch metadata"):
                fetch_metadata("https://youtube.com/watch?v=test", "test123")


class TestFetchAudio:
    """Tests for fetch_audio function"""

    def test_fetch_audio_cached(self, monkeypatch, temp_dir, capsys):
        """Test that cached audio is returned without re-downloading"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_audio, get_cache_dir

        # Create cache dir and audio file
        cache_dir = get_cache_dir("test123")
        audio_file = cache_dir / "audio.mp3"
        audio_file.write_text("fake audio content")

        result = fetch_audio("https://youtube.com/watch?v=test", "test123")
        assert result == audio_file

        captured = capsys.readouterr()
        assert "already cached" in captured.out

    def test_fetch_audio_download(self, monkeypatch, temp_dir):
        """Test audio download when not cached"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_audio, get_cache_dir

        cache_dir = get_cache_dir("test123")

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_audio_file(*args, **kwargs):
            # Simulate yt-dlp creating the file
            (cache_dir / "audio.mp3").write_text("audio content")
            return mock_result

        with patch('subprocess.run', side_effect=create_audio_file):
            result = fetch_audio("https://youtube.com/watch?v=test", "test123")

        assert result.exists()

    def test_fetch_audio_rename_different_extension(self, monkeypatch, temp_dir):
        """Test audio file rename when yt-dlp uses different extension"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_audio, get_cache_dir

        cache_dir = get_cache_dir("test123")

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_audio_with_different_ext(*args, **kwargs):
            # Simulate yt-dlp creating file with .m4a extension
            (cache_dir / "audio.m4a").write_text("audio content")
            return mock_result

        with patch('subprocess.run', side_effect=create_audio_with_different_ext):
            result = fetch_audio("https://youtube.com/watch?v=test", "test123")

        assert result == cache_dir / "audio.mp3"
        assert result.exists()

    def test_fetch_audio_failure(self, monkeypatch, temp_dir):
        """Test audio download failure raises exception"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_audio

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Download failed"

        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(Exception, match="Failed to download audio"):
                fetch_audio("https://youtube.com/watch?v=test", "test123")


class TestFetchTranscript:
    """Tests for fetch_transcript function"""

    def test_fetch_transcript_cached(self, monkeypatch, temp_dir, capsys):
        """Test that cached transcript is returned without re-downloading"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_transcript, get_cache_dir

        cache_dir = get_cache_dir("test123")
        (cache_dir / "transcript.txt").write_text("cached transcript")
        (cache_dir / "transcript.vtt").write_text("WEBVTT\n")

        vtt_path, txt_path = fetch_transcript("https://youtube.com/watch?v=test", "test123")
        assert txt_path.exists()

        captured = capsys.readouterr()
        assert "already cached" in captured.out

    def test_fetch_transcript_auto_subs(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test fetching auto-generated subtitles"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_transcript, get_cache_dir

        cache_dir = get_cache_dir("test123")

        mock_result = MagicMock()
        mock_result.returncode = 0

        def create_vtt_file(*args, **kwargs):
            (cache_dir / "transcript.en.vtt").write_text(sample_vtt_content)
            return mock_result

        with patch('subprocess.run', side_effect=create_vtt_file):
            vtt_path, txt_path = fetch_transcript("https://youtube.com/watch?v=test", "test123")

        assert vtt_path.exists()
        assert txt_path.exists()

    def test_fetch_transcript_fallback_to_manual_subs(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test fallback to manual subtitles when auto-subs not available"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_transcript, get_cache_dir

        cache_dir = get_cache_dir("test123")

        mock_result = MagicMock()
        mock_result.returncode = 0

        call_count = [0]

        def create_vtt_on_second_call(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 2:  # Manual subs call
                (cache_dir / "transcript.en.vtt").write_text(sample_vtt_content)
            return mock_result

        with patch('subprocess.run', side_effect=create_vtt_on_second_call):
            vtt_path, txt_path = fetch_transcript("https://youtube.com/watch?v=test", "test123")

        assert vtt_path.exists()
        assert txt_path.exists()

    def test_fetch_transcript_no_subs_available(self, monkeypatch, temp_dir):
        """Test exception when no subtitles available"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_transcript

        mock_result = MagicMock()
        mock_result.returncode = 0

        with patch('subprocess.run', return_value=mock_result):
            with pytest.raises(Exception, match="No subtitles available"):
                fetch_transcript("https://youtube.com/watch?v=test", "test123")


class TestCleanTranscript:
    """Tests for clean_transcript function"""

    def test_clean_transcript_removes_headers(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test that VTT headers are removed"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import clean_transcript

        vtt_path = temp_dir / "test.vtt"
        txt_path = temp_dir / "test.txt"
        vtt_path.write_text(sample_vtt_content)

        clean_transcript(vtt_path, txt_path)

        content = txt_path.read_text()
        assert "WEBVTT" not in content
        assert "Kind:" not in content
        assert "Language:" not in content

    def test_clean_transcript_removes_timestamps(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test that timestamps are removed"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import clean_transcript

        vtt_path = temp_dir / "test.vtt"
        txt_path = temp_dir / "test.txt"
        vtt_path.write_text(sample_vtt_content)

        clean_transcript(vtt_path, txt_path)

        content = txt_path.read_text()
        assert "00:00:00" not in content
        assert "-->" not in content

    def test_clean_transcript_deduplicates(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test that duplicate lines are removed"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import clean_transcript

        vtt_path = temp_dir / "test.vtt"
        txt_path = temp_dir / "test.txt"
        vtt_path.write_text(sample_vtt_content)

        clean_transcript(vtt_path, txt_path)

        content = txt_path.read_text()
        # "Hello world" appears twice in sample but should only be in output once
        assert content.count("Hello world") == 1

    def test_clean_transcript_removes_html_tags(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test that HTML tags are removed"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import clean_transcript

        vtt_path = temp_dir / "test.vtt"
        txt_path = temp_dir / "test.txt"
        vtt_path.write_text(sample_vtt_content)

        clean_transcript(vtt_path, txt_path)

        content = txt_path.read_text()
        assert "<c>" not in content
        assert "</c>" not in content
        assert "Formatted text here" in content


class TestFetchYoutube:
    """Tests for fetch_youtube main function"""

    def test_fetch_youtube_invalid_url(self, monkeypatch, temp_dir):
        """Test that invalid URL raises ValueError"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_youtube

        with pytest.raises(ValueError, match="Could not extract video ID"):
            fetch_youtube("https://example.com/not-youtube")

    def test_fetch_youtube_success(self, monkeypatch, temp_dir, sample_vtt_content):
        """Test successful YouTube fetch"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.youtube' in sys.modules:
            del sys.modules['fetcher.youtube']
        from fetcher.youtube import fetch_youtube, get_cache_dir

        # Pre-create cache dir
        cache_dir = get_cache_dir("dQw4w9WgXcQ")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "title": "Test Video",
            "channel": "Test Channel",
            "duration": 300
        })

        call_count = [0]

        def mock_subprocess(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:  # metadata
                return mock_result
            elif call_count[0] == 2:  # audio
                (cache_dir / "audio.mp3").write_text("audio")
                return mock_result
            else:  # transcript
                (cache_dir / "transcript.en.vtt").write_text(sample_vtt_content)
                return mock_result

        with patch('subprocess.run', side_effect=mock_subprocess):
            result = fetch_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        assert result["id"] == "youtube_dQw4w9WgXcQ"
        assert result["type"] == "youtube"
        assert result["video_id"] == "dQw4w9WgXcQ"
        assert result["metadata"]["title"] == "Test Video"
