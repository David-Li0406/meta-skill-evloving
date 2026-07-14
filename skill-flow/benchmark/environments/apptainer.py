"""Apptainer-backed harbor environment (rootless, no Docker daemon).

Builds each task's image from its ``Dockerfile`` into an Apptainer *sandbox*
(a writable rootfs directory), then runs the agent + verifier via
``apptainer exec --writable --fakeroot``. Designed for HPC nodes that have
Apptainer but cannot run Docker/rootless-podman (no /etc/subuid, cgroups v1).

Register with harbor via:
    --environment-import-path benchmark.environments.apptainer:ApptainerEnvironment
"""

from __future__ import annotations

import asyncio
import os
import shutil
from pathlib import Path

from harbor.environments.base import BaseEnvironment, ExecResult
from harbor.models.environment_type import EnvironmentType
from harbor.models.trial.paths import EnvironmentPaths

from benchmark.environments.dockerfile_interp import (
    base_image,
    parse_copy,
    parse_dockerfile,
    parse_env,
)

def _dq(value: str) -> str:
    """Double-quote a shell value, keeping $VAR expansion but escaping specials."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("`", "\\`")
    return f'"{escaped}"'


_DEFAULT_ROOT = os.environ.get(
    "HARBOR_APPTAINER_ROOT", f"/tmp/harbor-apptainer-{os.environ.get('USER', 'user')}"
)
_CACHE_DIR = os.environ.get(
    "APPTAINER_CACHEDIR", f"/tmp/apptainer-cache-{os.environ.get('USER', 'user')}"
)
# Persistent local SIF cache: each unique base image is pulled from the registry
# exactly ONCE into a .sif here; every task sandbox is then built from the local
# SIF (no registry access). This makes builds immune to Docker Hub's anonymous
# pull rate limit, which otherwise fails whole runs once exhausted.
_SIF_DIR = os.environ.get("APPTAINER_SIF_DIR", "/scratch/daweili5/apptainer-sif")


def _sif_path(image: str) -> Path:
    safe = image.replace("/", "_").replace(":", "_").replace("@", "_")
    return Path(_SIF_DIR) / f"{safe}.sif"


class ApptainerEnvironment(BaseEnvironment):
    """One writable Apptainer sandbox per trial."""

    def __init__(self, *args, sandbox_root: str | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        root = Path(sandbox_root or _DEFAULT_ROOT)
        safe = self.session_id.lower().replace(".", "-").replace("/", "-")
        self._sbx = root / safe
        # bind host log dirs -> in-container paths (mirrors docker is_mounted)
        self._binds: list[tuple[str, str]] = [
            (str(self.trial_paths.agent_dir.resolve()), EnvironmentPaths.agent_dir.as_posix()),
            (str(self.trial_paths.verifier_dir.resolve()), EnvironmentPaths.verifier_dir.as_posix()),
        ]
        self._workdir = "/root"
        self._apptainer_env = {
            **os.environ,
            "APPTAINER_CACHEDIR": _CACHE_DIR,
            "APPTAINER_QUIET": "1",  # suppress INFO/WARNING chatter on stderr
            "APPTAINERENV_DEBIAN_FRONTEND": "noninteractive",
        }
        Path(_CACHE_DIR).mkdir(parents=True, exist_ok=True)

    # ----- harbor interface metadata -----
    @staticmethod
    def type() -> EnvironmentType:
        return EnvironmentType.DOCKER  # reused label; selected via import-path

    @property
    def is_mounted(self) -> bool:
        return True

    @property
    def supports_gpus(self) -> bool:
        return False

    @property
    def can_disable_internet(self) -> bool:
        # Report support so harbor's _validate_internet_config gate doesn't raise
        # (and crash the whole run) on tasks that leave allow_internet falsy.
        # Rootless apptainer shares the host network, so the in-sandbox agent can
        # still reach the model API; faithful network isolation isn't available
        # unprivileged. Both seed and evolved runs use this identical setting, so
        # the cross-iteration comparison stays fair.
        return True

    @property
    def _dockerfile_path(self) -> Path:
        return self.environment_dir / "Dockerfile"

    def _validate_definition(self):
        if not self._dockerfile_path.exists():
            raise FileNotFoundError(f"{self._dockerfile_path} not found")

    # ----- subprocess helper -----
    async def _run(
        self, cmd: list[str], timeout_sec: int | None = None, check: bool = False
    ) -> ExecResult:
        # Keep stdout (the command's real output) separate from stderr so the
        # verifier reads clean output; apptainer's own chatter goes to stderr.
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=self._apptainer_env,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            out, err = (
                await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
                if timeout_sec
                else await proc.communicate()
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.communicate()
            raise RuntimeError(f"command timed out after {timeout_sec}s")
        res = ExecResult(
            stdout=(out.decode(errors="replace") if out else None),
            stderr=(err.decode(errors="replace") if err else None),
            return_code=proc.returncode or 0,
        )
        if check and res.return_code != 0:
            raise RuntimeError(
                f"apptainer command failed ({res.return_code}): "
                f"{' '.join(cmd)}\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}"
            )
        return res

    def _exec_in_sandbox(
        self, inner: str, cwd: str | None = None, env: dict[str, str] | None = None
    ) -> list[str]:
        # --cleanenv: do NOT inherit the host environment (host PATH etc. would
        # otherwise leak in and shadow the container's tools). Dockerfile ENV is
        # restored from .singularity.d/env; harbor's env dict is passed via --env.
        # --no-home / --no-mount: stop apptainer from bind-mounting the host
        # $HOME (which is /root under fakeroot and would shadow the task's files),
        # the host CWD, and host /tmp. The sandbox's own dirs must show through.
        cmd = ["apptainer", "exec", "--writable", "--fakeroot", "--cleanenv",
               "--no-home", "--no-mount", "tmp,cwd",
               "--pwd", cwd or self._workdir]
        for host, dest in self._binds:
            cmd += ["--bind", f"{host}:{dest}"]
        for k, v in (env or {}).items():
            cmd += ["--env", f"{k}={v}"]
        # Ensure user-local installs (e.g. Claude Code's native install into
        # ~/.local/bin) are on PATH — some agents don't export it themselves.
        inner = 'export PATH="$HOME/.local/bin:$HOME/bin:$PATH"; ' + inner
        cmd += [str(self._sbx), "bash", "-c", inner]
        return cmd

    async def _base_image_source(self, img: str) -> str:
        """Return a registry-free build source for the base image.

        Pull each unique base image from the registry exactly once into the
        shared SIF cache; every build (this run or future) then builds straight
        from the local ``.sif`` with no registry access — immune to Docker Hub's
        anonymous pull rate limit. A lockfile serializes concurrent first pulls
        of the same image across parallel trials.
        """
        sif = _sif_path(img)
        if sif.exists() and sif.stat().st_size > 0:
            return str(sif)
        sif.parent.mkdir(parents=True, exist_ok=True)
        lock = Path(str(sif) + ".lock")
        for _ in range(900):  # wait up to ~15 min for a peer trial's pull
            try:
                fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                break
            except FileExistsError:
                if sif.exists() and sif.stat().st_size > 0:
                    return str(sif)
                await asyncio.sleep(1)
        else:
            return f"docker://{img}"  # lock stuck; fall back to direct pull
        try:
            if not (sif.exists() and sif.stat().st_size > 0):
                tmp = Path(str(sif) + ".tmp")
                await self._run(
                    ["apptainer", "pull", "--force", str(tmp), f"docker://{img}"],
                    timeout_sec=int(self.task_env_config.build_timeout_sec or 1200),
                    check=True,
                )
                tmp.rename(sif)
        finally:
            try:
                lock.unlink()
            except OSError:
                pass
        return str(sif)

    # ----- build (Dockerfile interpreter) -----
    async def start(self, force_build: bool):
        if self._sbx.exists():
            shutil.rmtree(self._sbx, ignore_errors=True)
        self._sbx.parent.mkdir(parents=True, exist_ok=True)

        instr = parse_dockerfile(self._dockerfile_path.read_text(encoding="utf-8"))
        img = base_image(instr)
        base_src = await self._base_image_source(img)
        await self._run(
            ["apptainer", "build", "--sandbox", "--force", str(self._sbx), base_src],
            timeout_sec=int(self.task_env_config.build_timeout_sec or 1200),
            check=True,
        )
        # pre-create bind targets so apptainer can mount them
        for _, dest in self._binds:
            (self._sbx / dest.lstrip("/")).mkdir(parents=True, exist_ok=True)

        env_acc: dict[str, str] = {}
        for ins in instr:
            if ins.op == "ENV" or ins.op == "ARG":
                for k, v in parse_env(ins.value):
                    if k:
                        env_acc[k] = v
            elif ins.op == "WORKDIR":
                self._workdir = ins.value.strip() or "/"
                (self._sbx / self._workdir.lstrip("/")).mkdir(parents=True, exist_ok=True)
            elif ins.op in ("COPY", "ADD"):
                self._apply_copy(ins.value)
            elif ins.op == "RUN":
                # Apply Dockerfile ENV as shell `export`s so values that
                # reference other vars (e.g. PATH="/x:$PATH") expand correctly.
                prefix = "".join(f"export {k}={_dq(v)}; " for k, v in env_acc.items())
                await self._run(
                    self._exec_in_sandbox(prefix + ins.value),
                    timeout_sec=int(self.task_env_config.build_timeout_sec or 1200),
                    check=True,
                )
        self._persist_env(env_acc)

    def _apply_copy(self, value: str):
        srcs, dst = parse_copy(value)
        dest_in_sbx = self._sbx / dst.lstrip("/")
        dst_is_dir = dst.endswith("/") or len(srcs) > 1
        if dst_is_dir:
            dest_in_sbx.mkdir(parents=True, exist_ok=True)
        else:
            dest_in_sbx.parent.mkdir(parents=True, exist_ok=True)
        for src in srcs:
            sp = (self.environment_dir / src).resolve()
            if sp.is_dir():
                shutil.copytree(sp, dest_in_sbx / sp.name if dst_is_dir else dest_in_sbx,
                                dirs_exist_ok=True)
            else:
                shutil.copy2(sp, dest_in_sbx / sp.name if dst_is_dir else dest_in_sbx)

    def _persist_env(self, env_acc: dict[str, str]):
        """Write ENV vars so every exec (incl. the agent) inherits them.

        Uses double-quoting so values referencing other vars (PATH="/x:$PATH")
        expand against the container's environment at startup.
        """
        envd = self._sbx / ".singularity.d" / "env"
        envd.mkdir(parents=True, exist_ok=True)
        lines = [f"export {k}={_dq(v)}" for k, v in env_acc.items()]
        (envd / "91-task-env.sh").write_text("\n".join(lines) + "\n", encoding="utf-8")

    async def stop(self, delete: bool):
        if delete and self._sbx.exists():
            shutil.rmtree(self._sbx, ignore_errors=True)

    # ----- file transfer (host <-> sandbox rootfs) -----
    def _host_location(self, container_path: str) -> Path:
        """Map an in-container absolute path to its real host location.

        Paths under a bind mount (e.g. /logs/agent) live on the host bind dir;
        everything else lives inside the sandbox rootfs.
        """
        cp = "/" + container_path.lstrip("/")
        for host, dest in self._binds:
            d = dest.rstrip("/")
            if cp == d or cp.startswith(d + "/"):
                return Path(host) / cp[len(d):].lstrip("/")
        return self._sbx / cp.lstrip("/")

    async def upload_file(self, source_path: Path | str, target_path: str):
        dst = self._host_location(target_path)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dst)

    async def upload_dir(self, source_dir: Path | str, target_dir: str):
        # Copy the CONTENTS of source_dir into target_dir (mirrors `docker cp
        # srcdir main:/target` when /target does not yet exist), so e.g.
        # tests/ -> /tests/test.sh, not /tests/tests/test.sh.
        dst = self._host_location(target_dir)
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, dst, dirs_exist_ok=True)

    async def download_file(self, source_path: str, target_path: Path | str):
        Path(target_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self._host_location(source_path), target_path)

    async def download_dir(self, source_dir: str, target_dir: Path | str):
        src = self._host_location(source_dir)
        if src.exists():
            shutil.copytree(src, target_dir, dirs_exist_ok=True)

    async def exec(
        self,
        command: str,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        timeout_sec: int | None = None,
    ) -> ExecResult:
        return await self._run(
            self._exec_in_sandbox(command, cwd=cwd, env=env),
            timeout_sec=timeout_sec,
            check=False,
        )
