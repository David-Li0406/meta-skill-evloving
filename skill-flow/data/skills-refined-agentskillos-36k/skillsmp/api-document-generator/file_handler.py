"""
File Handler Module
Handles file operations, directory scanning, and output file management for API documentation generation.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json


class FileHandler:
    """Handles file operations for API documentation generation."""

    def __init__(self, base_output_dir: str = ".claude/api_doc"):
        """
        Initialize file handler.

        Args:
            base_output_dir: Base directory for output files
        """
        self.base_output_dir = Path(base_output_dir)
        self.timestamp_format = "%Y-%m-%d_%H-%M-%S"

    def ensure_output_directory(self) -> Path:
        """
        Ensure the output directory exists.

        Returns:
            Path to the output directory
        """
        self.base_output_dir.mkdir(parents=True, exist_ok=True)
        return self.base_output_dir

    def get_timestamped_filename(self, base_name: str = "api_documentation",
                                extension: str = "md") -> str:
        """
        Generate a timestamped filename.

        Args:
            base_name: Base name for the file
            extension: File extension

        Returns:
            Timestamped filename
        """
        timestamp = datetime.now().strftime(self.timestamp_format)
        return f"{base_name}_{timestamp}.{extension}"

    def save_documentation(self, content: str, filename: Optional[str] = None,
                          subdirectory: Optional[str] = None) -> str:
        """
        Save documentation content to file.

        Args:
            content: Documentation content to save
            filename: Optional filename (generated if not provided)
            subdirectory: Optional subdirectory within output directory

        Returns:
            Path to saved file
        """
        output_dir = self.base_output_dir
        if subdirectory:
            output_dir = output_dir / subdirectory

        output_dir.mkdir(parents=True, exist_ok=True)

        if filename is None:
            filename = self.get_timestamped_filename()

        output_path = output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_path)

    def scan_directory(self, directory_path: str,
                      extensions: Optional[List[str]] = None) -> List[str]:
        """
        Scan directory for files with specific extensions.

        Args:
            directory_path: Path to directory to scan
            extensions: List of file extensions to include (None for all)

        Returns:
            List of file paths
        """
        directory_path = Path(directory_path)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")

        file_paths = []

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = Path(root) / file
                if extensions is None or file_path.suffix.lower() in extensions:
                    file_paths.append(str(file_path))

        return sorted(file_paths)

    def read_file(self, file_path: str) -> str:
        """
        Read file content.

        Args:
            file_path: Path to file

        Returns:
            File content as string
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_json(self, data: Dict[str, Any], file_path: str) -> str:
        """
        Write data as JSON file.

        Args:
            data: Data to write
            file_path: Path to output file

        Returns:
            Path to saved file
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return str(file_path)

    def read_json(self, file_path: str) -> Dict[str, Any]:
        """
        Read JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Parsed JSON data
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def cleanup_old_files(self, max_files: int = 10,
                         pattern: str = "api_documentation_*.md") -> List[str]:
        """
        Clean up old documentation files, keeping only the most recent ones.

        Args:
            max_files: Maximum number of files to keep
            pattern: File pattern to match

        Returns:
            List of deleted file paths
        """
        output_dir = self.ensure_output_directory()
        deleted_files = []

        # Get all matching files
        files = list(output_dir.glob(pattern))
        if len(files) <= max_files:
            return deleted_files

        # Sort by modification time (oldest first)
        files.sort(key=lambda x: x.stat().st_mtime)

        # Delete oldest files
        files_to_delete = files[:len(files) - max_files]
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                deleted_files.append(str(file_path))
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

        return deleted_files

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about a file.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file information
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        stat = file_path.stat()

        return {
            'path': str(file_path),
            'name': file_path.name,
            'extension': file_path.suffix.lower(),
            'size_bytes': stat.st_size,
            'size_human': self._format_size(stat.st_size),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'is_file': file_path.is_file(),
            'is_dir': file_path.is_dir()
        }

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def create_backup(self, file_path: str, backup_suffix: str = ".backup") -> str:
        """
        Create a backup of a file.

        Args:
            file_path: Path to file to backup
            backup_suffix: Suffix for backup file

        Returns:
            Path to backup file
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
        shutil.copy2(file_path, backup_path)

        return str(backup_path)

    def restore_backup(self, backup_path: str, remove_backup: bool = True) -> str:
        """
        Restore a file from backup.

        Args:
            backup_path: Path to backup file
            remove_backup: Whether to remove backup after restoration

        Returns:
            Path to restored file
        """
        backup_path = Path(backup_path)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        # Remove .backup suffix to get original path
        original_path = backup_path.with_suffix('')
        if original_path.suffix.endswith('.backup'):
            original_path = original_path.with_suffix('')

        shutil.copy2(backup_path, original_path)

        if remove_backup:
            backup_path.unlink()

        return str(original_path)

    def get_recent_documentation_files(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get most recent documentation files.

        Args:
            limit: Maximum number of files to return

        Returns:
            List of file information dictionaries
        """
        output_dir = self.ensure_output_directory()
        files = []

        for file_path in output_dir.glob("*.md"):
            file_info = self.get_file_info(str(file_path))
            files.append(file_info)

        # Sort by modification time (newest first)
        files.sort(key=lambda x: x['modified'], reverse=True)

        return files[:limit]

    def validate_output_directory(self) -> Tuple[bool, List[str]]:
        """
        Validate the output directory.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        try:
            output_dir = self.ensure_output_directory()

            # Check if directory is writable
            test_file = output_dir / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except PermissionError:
                issues.append(f"Directory is not writable: {output_dir}")

            # Check disk space (approximate)
            import shutil
            disk_usage = shutil.disk_usage(output_dir)
            if disk_usage.free < 1024 * 1024 * 10:  # Less than 10MB free
                issues.append(f"Low disk space: {disk_usage.free / (1024*1024):.1f}MB free")

        except Exception as e:
            issues.append(f"Error validating directory: {e}")

        return len(issues) == 0, issues