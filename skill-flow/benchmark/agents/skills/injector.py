"""
Skill injection logic for uploading skills to evaluation containers.
"""

import logging
import shutil
import tempfile
from pathlib import Path, PurePosixPath

from harbor.environments.base import BaseEnvironment


class TarGzSkillInjector:
    """
    Injects skills into containers using tar.gz archive upload.

    Uses tar instead of zip because tar is universally available on Linux
    containers while unzip may not be installed.

    ``container_skills_dir`` is where the agent's runtime expects skills.
    Codex auto-discovers ``$CODEX_HOME/skills`` (= ``/logs/agent/skills``);
    Claude Code reads ``$CLAUDE_CONFIG_DIR/skills`` (= ``/logs/agent/sessions/skills``).
    The archive's top-level folder is always ``skills``, so the extract target
    is the parent of ``container_skills_dir``.
    """

    CONTAINER_TMP_ARCHIVE = "/tmp/skills.tar.gz"  # nosec B108

    def __init__(
        self,
        logger: logging.Logger | None = None,
        container_skills_dir: str = "/logs/agent/skills",
    ) -> None:
        """
        Initialize skill injector.

        Args:
            logger: Optional logger instance.
            container_skills_dir: In-container path the agent reads skills from.
        """
        self._logger = logger or logging.getLogger(__name__)
        if PurePosixPath(container_skills_dir).name != "skills":
            msg = "container_skills_dir must end in 'skills'"
            raise ValueError(msg)
        self._container_skills_dir = container_skills_dir
        self._extract_dir = str(PurePosixPath(container_skills_dir).parent)

    async def inject(
        self,
        environment: BaseEnvironment,
        skill_folders: list[Path],
        logs_dir: Path,
    ) -> int:
        """
        Upload skills to container via tar.gz archive.

        Args:
            environment: The execution environment.
            skill_folders: List of skill folder paths to upload.
            logs_dir: Local logs directory for copying skills.

        Returns:
            Number of skills injected.
        """
        if not skill_folders:
            return 0

        self._logger.debug(f"Injecting {len(skill_folders)} skills")

        # Create skills directory in container
        await environment.exec(command=f"mkdir -p {self._container_skills_dir}")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            skills_staging = temp_path / "skills"
            skills_staging.mkdir()

            # Clean up existing local skills directory
            self._cleanup_local_skills(logs_dir)

            # Stage skills for archive
            for folder in skill_folders:
                self._stage_skill(folder, skills_staging, logs_dir)

            # Create and upload archive
            await self._upload_archive(environment, temp_path)

        # Verify upload
        result = await environment.exec(
            command=f"ls -la {self._container_skills_dir}/"
        )
        self._logger.debug(f"Skills directory contents:\n{result.stdout}")

        return len(skill_folders)

    def _cleanup_local_skills(self, logs_dir: Path) -> None:
        """Remove existing skills directory in logs."""
        local_skills_dir = logs_dir / "skills"
        if local_skills_dir.exists():
            try:
                shutil.rmtree(local_skills_dir)
            except PermissionError:
                self._logger.warning(
                    f"Could not remove existing skills dir: {local_skills_dir}"
                )

    def _stage_skill(
        self, skill_folder: Path, staging_dir: Path, logs_dir: Path
    ) -> None:
        """
        Stage a skill for archive creation.

        Args:
            skill_folder: Source skill folder.
            staging_dir: Temporary staging directory.
            logs_dir: Local logs directory for copying.
        """
        base_name = skill_folder.name
        skill_name = base_name
        counter = 2
        while (staging_dir / skill_name).exists():
            skill_name = f"{base_name}-{counter}"
            counter += 1
        self._logger.debug(f"Staging skill: {skill_name}")

        shutil.copytree(skill_folder, staging_dir / skill_name)

        skills_log_dir = logs_dir / "skills" / skill_name
        try:
            skills_log_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(skill_folder, skills_log_dir, dirs_exist_ok=True)
        except (PermissionError, FileExistsError):
            self._logger.warning(f"Could not copy skill to logs dir: {skill_name}")

    async def _upload_archive(
        self, environment: BaseEnvironment, temp_path: Path
    ) -> None:
        """
        Create tar.gz archive and upload to container.

        Args:
            environment: The execution environment.
            temp_path: Temporary directory containing staged skills.
        """
        tar_path = temp_path / "skills.tar.gz"
        shutil.make_archive(
            str(tar_path.with_suffix("").with_suffix("")),
            "gztar",
            root_dir=temp_path,
            base_dir="skills",
        )

        self._logger.debug(
            f"Created skills archive: {tar_path} "
            f"({tar_path.stat().st_size / 1024:.1f} KB)"
        )

        # Upload archive
        await environment.upload_file(
            source_path=tar_path,
            target_path=self.CONTAINER_TMP_ARCHIVE,
        )

        # Extract and cleanup in container. The archive's top-level folder is
        # "skills", so extracting into the parent dir yields container_skills_dir.
        # --no-same-owner: the archive carries the host uid/gid; the sandbox
        # cannot chown to them, which otherwise makes tar exit non-zero.
        extract_cmd = (
            f"mkdir -p {self._extract_dir} && "
            f"tar --no-same-owner -xzf {self.CONTAINER_TMP_ARCHIVE} "
            f"-C {self._extract_dir} && "
            f"rm {self.CONTAINER_TMP_ARCHIVE}"
        )
        result = await environment.exec(command=extract_cmd)
        if result.return_code != 0:
            self._logger.error(f"Failed to extract skills: {result.stderr}")
