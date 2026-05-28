"""ModalJob - A decorator for submitting Python functions to Modal with job tracking.

Single-file version for easy copy-paste. Usage:

    @ModalJob(image=my_image, gpu="A10G", secrets=["wandb"])
    def train(config):
        with open("/outputs/metrics.json", "w") as f:
            json.dump({"loss": 0.5}, f)
        return {"done": True}

    # Submit job
    handle = train.submit(config={"lr": 1e-4})
    print(f"Job ID: {handle.job_id}")

    # Resume later
    handle = JobHandle.from_id("a1b2c3d4")
    print(handle.status())  # "running" | "completed" | "failed"
    result = handle.result(timeout=3600)
    handle.download("./outputs/")
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Sequence, Any, Literal, Tuple
import uuid

import modal

__all__ = ["ModalJob", "JobHandle"]

# =============================================================================
# Types and Data Classes
# =============================================================================

JobStatus = Literal["pending", "running", "completed", "failed"]


@dataclass
class JobMetadata:
    """Persistent metadata for tracking a job."""

    job_id: str
    function_call_id: str
    volume_name: str
    status: JobStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class ModalJobConfig:
    """Configuration for a Modal job."""

    image: Optional[modal.Image] = None
    gpu: Optional[str] = None  # "T4", "A10G", "A100-40GB"
    secrets: Sequence[str] = field(default_factory=list)
    timeout: int = 3600
    cpu: Optional[float] = None
    memory: Optional[int] = None


# =============================================================================
# Persistence (Modal Dict)
# =============================================================================

JOBS_DICT_NAME = "modaljob-registry"


def _get_jobs_dict() -> modal.Dict:
    """Get or create the shared jobs registry Dict."""
    return modal.Dict.from_name(JOBS_DICT_NAME, create_if_missing=True)


def _save_job_metadata(meta: JobMetadata) -> None:
    """Persist job metadata to Modal Dict."""
    jobs = _get_jobs_dict()
    jobs[meta.job_id] = {
        "job_id": meta.job_id,
        "function_call_id": meta.function_call_id,
        "volume_name": meta.volume_name,
        "status": meta.status,
        "created_at": meta.created_at.isoformat(),
        "completed_at": meta.completed_at.isoformat() if meta.completed_at else None,
        "error": meta.error,
    }


def _load_job_metadata(job_id: str) -> JobMetadata:
    """Load job metadata from Modal Dict."""
    jobs = _get_jobs_dict()
    data = jobs[job_id]
    return JobMetadata(
        job_id=data["job_id"],
        function_call_id=data["function_call_id"],
        volume_name=data["volume_name"],
        status=data["status"],
        created_at=datetime.fromisoformat(data["created_at"]),
        completed_at=(
            datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None
        ),
        error=data.get("error"),
    )


def _update_job_status(
    job_id: str,
    status: JobStatus,
    completed_at: Optional[datetime] = None,
    error: Optional[str] = None,
) -> None:
    """Update job status in Modal Dict."""
    jobs = _get_jobs_dict()
    data = dict(jobs[job_id])
    data["status"] = status
    if completed_at:
        data["completed_at"] = completed_at.isoformat()
    if error:
        data["error"] = error
    jobs[job_id] = data


def list_jobs(limit: int = 50) -> list[JobMetadata]:
    """List recent jobs."""
    jobs = _get_jobs_dict()
    result = []
    for job_id in list(jobs.keys())[-limit:]:
        try:
            result.append(_load_job_metadata(job_id))
        except Exception:
            pass
    return result


# =============================================================================
# JobHandle
# =============================================================================


class JobHandle:
    """Handle for tracking and retrieving results from a Modal job."""

    def __init__(self, job_id: str, function_call_id: str, volume_name: str):
        self.job_id = job_id
        self._function_call_id = function_call_id
        self._volume_name = volume_name
        self._result_cache: Optional[Any] = None

    def __repr__(self) -> str:
        return f"JobHandle(job_id={self.job_id!r})"

    @classmethod
    def from_id(cls, job_id: str) -> "JobHandle":
        """Reconstruct a JobHandle from a persisted job_id."""
        meta = _load_job_metadata(job_id)
        return cls(meta.job_id, meta.function_call_id, meta.volume_name)

    def status(self) -> JobStatus:
        """Poll current job status (non-blocking)."""
        from modal.functions import FunctionCall

        try:
            fc = FunctionCall.from_id(self._function_call_id)
            try:
                fc.get(timeout=0)
                return "completed"
            except TimeoutError:
                return "running"
        except Exception as e:
            if "not found" in str(e).lower():
                return "failed"
            return "running"

    def result(self, timeout: Optional[float] = None) -> Any:
        """Block until job completes and return result."""
        if self._result_cache is not None:
            return self._result_cache

        from modal.functions import FunctionCall

        fc = FunctionCall.from_id(self._function_call_id)
        self._result_cache = fc.get(timeout=timeout)
        return self._result_cache

    def download(self, local_path: str | Path = ".") -> Path:
        """Download artifacts from job's volume to local path."""
        local_path = Path(local_path)
        local_path.mkdir(parents=True, exist_ok=True)

        vol = modal.Volume.from_name(self._volume_name)

        # Files written to /outputs appear at volume root
        for entry in vol.listdir("/"):
            if entry.type.name == "FILE":
                content = b"".join(vol.read_file(entry.path))
                dest = local_path / Path(entry.path).name
                dest.write_bytes(content)
                print(f"Downloaded: {dest}")

        return local_path


# =============================================================================
# Job Submission
# =============================================================================


def _submit_job(
    fn: Callable,
    config: ModalJobConfig,
    args: Tuple[Any, ...],
    kwargs: dict,
) -> JobHandle:
    """Submit a job to Modal."""
    job_id = uuid.uuid4().hex[:8]
    volume_name = f"modaljob-{job_id}"

    # Create volume for artifacts
    vol = modal.Volume.from_name(volume_name, create_if_missing=True)

    # Build secrets list
    secrets = [modal.Secret.from_name(s) for s in config.secrets]

    # Create dynamic app
    app = modal.App(f"modaljob-{job_id}")

    # Wrapper that ensures /outputs exists and commits volume
    def _wrapper(user_fn: Callable, vol_name: str, *args, **kwargs):
        import os
        import modal

        os.makedirs("/outputs", exist_ok=True)
        result = user_fn(*args, **kwargs)

        # Commit volume to persist artifacts
        vol = modal.Volume.from_name(vol_name)
        vol.commit()

        return result

    # Build function kwargs
    fn_kwargs = {
        "image": config.image,
        "volumes": {"/outputs": vol},
        "timeout": config.timeout,
        "serialized": True,
    }
    if config.gpu:
        fn_kwargs["gpu"] = config.gpu
    if secrets:
        fn_kwargs["secrets"] = secrets
    if config.cpu:
        fn_kwargs["cpu"] = config.cpu
    if config.memory:
        fn_kwargs["memory"] = config.memory

    # Register function with serialized=True for cloudpickle transport
    modal_fn = app.function(**fn_kwargs)(_wrapper)

    # Submit asynchronously
    with app.run(detach=True):
        fc = modal_fn.spawn(fn, volume_name, *args, **kwargs)
        function_call_id = fc.object_id

    # Persist metadata
    meta = JobMetadata(
        job_id=job_id,
        function_call_id=function_call_id,
        volume_name=volume_name,
        status="running",
        created_at=datetime.now(),
    )
    _save_job_metadata(meta)

    return JobHandle(job_id, function_call_id, volume_name)


# =============================================================================
# Decorator
# =============================================================================


class ModalJobCallable:
    """Wrapper around a user function that adds .submit() capability."""

    def __init__(self, fn: Callable, config: ModalJobConfig):
        self._fn = fn
        self._config = config
        self.__name__ = fn.__name__
        self.__doc__ = fn.__doc__

    def __call__(self, *args, **kwargs) -> Any:
        """Direct invocation runs locally (for testing)."""
        return self._fn(*args, **kwargs)

    def submit(self, *args, **kwargs) -> JobHandle:
        """Submit function to Modal for remote execution."""
        return _submit_job(self._fn, self._config, args, kwargs)


class ModalJob:
    """Decorator that wraps Python functions for Modal submission.

    Usage:
        @ModalJob(image=my_image, gpu="A10G", secrets=["wandb"])
        def train(config):
            ...

        handle = train.submit(config={"lr": 1e-4})
        print(handle.status())
        result = handle.result(timeout=3600)
        handle.download("./outputs/")
    """

    def __init__(
        self,
        image: Optional[modal.Image] = None,
        gpu: Optional[str] = None,
        secrets: Sequence[str] = (),
        timeout: int = 3600,
        cpu: Optional[float] = None,
        memory: Optional[int] = None,
    ):
        self.config = ModalJobConfig(
            image=image or self._default_image(),
            gpu=gpu,
            secrets=list(secrets),
            timeout=timeout,
            cpu=cpu,
            memory=memory,
        )

    def __call__(self, fn: Callable) -> ModalJobCallable:
        """Wrap function and return a callable with .submit() method."""
        return ModalJobCallable(fn, self.config)

    @staticmethod
    def _default_image() -> modal.Image:
        return modal.Image.debian_slim(python_version="3.12").pip_install(
            "cloudpickle"
        )
