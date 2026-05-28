"""Tests for fetcher/pdf.py"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import sys
import hashlib

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestGeneratePdfId:
    """Tests for generate_pdf_id function"""

    def test_generates_consistent_id(self, monkeypatch, temp_dir):
        """Test that same path generates same ID"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import generate_pdf_id

        pdf_path = Path("/tmp/test.pdf")
        id1 = generate_pdf_id(pdf_path)
        id2 = generate_pdf_id(pdf_path)

        assert id1 == id2
        assert len(id1) == 12  # MD5 truncated to 12 chars

    def test_different_paths_different_ids(self, monkeypatch, temp_dir):
        """Test that different paths generate different IDs"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import generate_pdf_id

        id1 = generate_pdf_id(Path("/tmp/test1.pdf"))
        id2 = generate_pdf_id(Path("/tmp/test2.pdf"))

        assert id1 != id2


class TestGetCacheDir:
    """Tests for get_cache_dir function"""

    def test_creates_cache_directory(self, monkeypatch, temp_dir):
        """Test that cache directory is created"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import get_cache_dir

        cache_dir = get_cache_dir("test123")

        assert cache_dir.exists()
        assert cache_dir == temp_dir / "cache" / "pdf" / "test123"


class TestExtractTextWithPymupdf:
    """Tests for extract_text_with_pymupdf function"""

    def test_extracts_text_from_pdf(self, monkeypatch, temp_dir):
        """Test text extraction from PDF"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        # Mock fitz module
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Page content here"

        mock_doc = MagicMock()
        mock_doc.__len__ = lambda self: 2
        mock_doc.__iter__ = lambda self: iter([mock_page, mock_page])
        mock_doc.__getitem__ = lambda self, idx: mock_page

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import extract_text_with_pymupdf

        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()
        txt_path = temp_dir / "output.txt"

        text = extract_text_with_pymupdf(pdf_path, txt_path)

        assert "Page content here" in text
        assert txt_path.exists()
        mock_doc.close.assert_called_once()

    def test_raises_when_fitz_not_installed(self, monkeypatch, temp_dir):
        """Test that ImportError is raised when PyMuPDF not installed"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        # Remove fitz from modules if present
        if 'fitz' in sys.modules:
            del sys.modules['fitz']
        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        # Make fitz import fail
        import builtins
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == 'fitz':
                raise ImportError("No module named 'fitz'")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, '__import__', mock_import)

        from fetcher.pdf import extract_text_with_pymupdf

        with pytest.raises(ImportError, match="PyMuPDF not installed"):
            extract_text_with_pymupdf(Path("/tmp/test.pdf"), Path("/tmp/out.txt"))


class TestExtractMetadataWithPymupdf:
    """Tests for extract_metadata_with_pymupdf function"""

    def test_extracts_metadata(self, monkeypatch, temp_dir):
        """Test metadata extraction"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        mock_doc = MagicMock()
        mock_doc.metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "subject": "Test Subject",
            "creator": "Test Creator",
            "producer": "Test Producer",
        }
        mock_doc.__len__ = lambda self: 100

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import extract_metadata_with_pymupdf

        metadata = extract_metadata_with_pymupdf(Path("/tmp/test.pdf"))

        assert metadata["title"] == "Test Book"
        assert metadata["author"] == "Test Author"
        assert metadata["page_count"] == 100
        mock_doc.close.assert_called_once()

    def test_handles_empty_metadata(self, monkeypatch, temp_dir):
        """Test handling of empty metadata"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        mock_doc = MagicMock()
        mock_doc.metadata = None
        mock_doc.__len__ = lambda self: 50

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import extract_metadata_with_pymupdf

        metadata = extract_metadata_with_pymupdf(Path("/tmp/test.pdf"))

        assert metadata["title"] == ""
        assert metadata["author"] == ""
        assert metadata["page_count"] == 50


class TestFetchMetadata:
    """Tests for fetch_metadata function"""

    def test_saves_metadata_to_cache(self, monkeypatch, temp_dir):
        """Test that metadata is saved to cache"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        mock_doc = MagicMock()
        mock_doc.metadata = {"title": "Test", "author": "Author"}
        mock_doc.__len__ = lambda self: 10

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import fetch_metadata

        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()

        metadata = fetch_metadata(pdf_path, "testid")

        # Check cache file exists
        cache_file = temp_dir / "cache" / "pdf" / "testid" / "metadata.json"
        assert cache_file.exists()

    def test_cleans_zlibrary_title(self, monkeypatch, temp_dir):
        """Test that Z-Library suffix is removed from title"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        mock_doc = MagicMock()
        mock_doc.metadata = {"title": "", "author": ""}
        mock_doc.__len__ = lambda self: 10

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import fetch_metadata

        pdf_path = temp_dir / "Test Book (Author Name) (Z-Library).pdf"
        pdf_path.touch()

        metadata = fetch_metadata(pdf_path, "testid")

        assert "(Z-Library)" not in metadata["title"]
        assert metadata["author"] == "Author Name"


class TestFetchText:
    """Tests for fetch_text function"""

    def test_uses_cached_text(self, monkeypatch, temp_dir, capsys):
        """Test that cached text is used if available"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import fetch_text, get_cache_dir

        # Create cached text
        cache_dir = get_cache_dir("testid")
        (cache_dir / "content.txt").write_text("Cached content")

        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()

        result = fetch_text(pdf_path, "testid")

        captured = capsys.readouterr()
        assert "already cached" in captured.out
        assert result == cache_dir / "content.txt"

    def test_extracts_text_when_not_cached(self, monkeypatch, temp_dir, capsys):
        """Test text extraction when not cached"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        mock_page = MagicMock()
        mock_page.get_text.return_value = "Extracted text"

        mock_doc = MagicMock()
        mock_doc.__len__ = lambda self: 1
        mock_doc.__getitem__ = lambda self, idx: mock_page

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import fetch_text

        pdf_path = temp_dir / "test.pdf"
        pdf_path.touch()

        result = fetch_text(pdf_path, "newid")

        captured = capsys.readouterr()
        assert "Extracting text" in captured.out
        assert result.exists()


class TestCopyPdfToCache:
    """Tests for copy_pdf_to_cache function"""

    def test_copies_pdf(self, monkeypatch, temp_dir):
        """Test PDF is copied to cache"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import copy_pdf_to_cache

        pdf_path = temp_dir / "original.pdf"
        pdf_path.write_text("PDF content")

        result = copy_pdf_to_cache(pdf_path, "testid")

        assert result.exists()
        assert result.read_text() == "PDF content"

    def test_skips_if_already_cached(self, monkeypatch, temp_dir):
        """Test that copy is skipped if already cached"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import copy_pdf_to_cache, get_cache_dir

        # Create cached PDF
        cache_dir = get_cache_dir("testid")
        (cache_dir / "source.pdf").write_text("Cached PDF")

        pdf_path = temp_dir / "original.pdf"
        pdf_path.write_text("New PDF content")

        result = copy_pdf_to_cache(pdf_path, "testid")

        # Should still have old content
        assert result.read_text() == "Cached PDF"


class TestFetchPdf:
    """Tests for fetch_pdf main function"""

    def test_fetch_pdf_not_found(self, monkeypatch, temp_dir):
        """Test error when PDF not found"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import fetch_pdf

        with pytest.raises(FileNotFoundError):
            fetch_pdf("/nonexistent/file.pdf")

    def test_fetch_pdf_not_pdf(self, monkeypatch, temp_dir):
        """Test error when file is not PDF"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']
        from fetcher.pdf import fetch_pdf

        txt_file = temp_dir / "test.txt"
        txt_file.touch()

        with pytest.raises(ValueError, match="Not a PDF"):
            fetch_pdf(str(txt_file))

    def test_fetch_pdf_success(self, monkeypatch, temp_dir, capsys):
        """Test successful PDF fetch"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'fetcher.pdf' in sys.modules:
            del sys.modules['fetcher.pdf']

        mock_page = MagicMock()
        mock_page.get_text.return_value = "Page text"

        mock_doc = MagicMock()
        mock_doc.metadata = {"title": "Test Book", "author": "Test Author"}
        mock_doc.__len__ = lambda self: 5
        mock_doc.__getitem__ = lambda self, idx: mock_page

        mock_fitz = MagicMock()
        mock_fitz.open.return_value = mock_doc

        monkeypatch.setitem(sys.modules, 'fitz', mock_fitz)

        from fetcher.pdf import fetch_pdf

        pdf_path = temp_dir / "test.pdf"
        pdf_path.write_bytes(b"PDF content")

        result = fetch_pdf(str(pdf_path))

        assert result["type"] == "pdf"
        assert result["id"].startswith("pdf_")
        assert "metadata" in result
        assert "cache_dir" in result
        assert "txt_path" in result

        captured = capsys.readouterr()
        assert "Processing PDF" in captured.out
