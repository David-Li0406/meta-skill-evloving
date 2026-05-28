"""
Safe, atomic file operations with backup support.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional


class SafeFileOperations:
    """Provides safe file operations with atomic writes and backups."""

    @staticmethod
    def read_file(path: Path) -> str:
        """
        Read file contents.

        Args:
            path: Path to file

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file isn't valid UTF-8
        """
        return path.read_text(encoding='utf-8')

    @staticmethod
    def write_file(path: Path, content: str, backup: bool = True) -> None:
        """
        Write content to file atomically with optional backup.

        Args:
            path: Path to file
            content: Content to write
            backup: Whether to create backup (default: True)

        Raises:
            IOError: If write fails
        """
        path = Path(path)

        # Create backup if file exists and backup requested
        if backup and path.exists():
            SafeFileOperations.backup_file(path)

        # Atomic write: write to temp file, then rename
        SafeFileOperations.atomic_write(path, content)

    @staticmethod
    def backup_file(path: Path) -> Path:
        """
        Create backup of file with .backup extension.

        Args:
            path: Path to file to backup

        Returns:
            Path to backup file

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Cannot backup non-existent file: {path}")

        backup_path = path.with_suffix(path.suffix + '.backup')
        shutil.copy2(path, backup_path)
        return backup_path

    @staticmethod
    def restore_backup(backup_path: Path) -> None:
        """
        Restore file from backup.

        Args:
            backup_path: Path to backup file

        Raises:
            FileNotFoundError: If backup doesn't exist
        """
        backup_path = Path(backup_path)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")

        # Remove .backup extension to get original path
        if backup_path.suffix == '.backup':
            original_path = backup_path.with_suffix('')
        else:
            original_path = backup_path.parent / backup_path.stem

        shutil.copy2(backup_path, original_path)

    @staticmethod
    def atomic_write(path: Path, content: str) -> None:
        """
        Write file atomically using temp file and rename.

        Args:
            path: Path to target file
            content: Content to write

        Raises:
            IOError: If write or rename fails
        """
        path = Path(path)

        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file in same directory (for atomic rename)
        fd, temp_path = tempfile.mkstemp(
            dir=path.parent,
            prefix=f'.tmp.{path.name}.',
            text=True
        )

        try:
            # Write content
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(content)

            # Preserve permissions if file exists
            if path.exists():
                shutil.copystat(path, temp_path)

            # Atomic rename
            shutil.move(temp_path, path)

        except Exception as e:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except:
                pass
            raise IOError(f"Failed to write {path}: {e}")
