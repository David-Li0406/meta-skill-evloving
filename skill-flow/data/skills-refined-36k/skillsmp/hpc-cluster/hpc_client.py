#!/usr/bin/env python3
"""
HPC Client for CURC (CU Boulder Alpine)

A lightweight client that handles SSH connection management and common HPC operations
while preserving full agent autonomy. Uses SSH ControlMaster for efficient connection
multiplexing.

Design Philosophy:
- Handles tedious plumbing (connections, paths, polling)
- Never limits what the agent can do
- Agent can always drop to raw SSH via run_command()
- All operations are transparent and debuggable

Usage:
    from hpc_client import HPCClient

    hpc = HPCClient()
    hpc.connect()

    # Run any command
    output = hpc.run("squeue -u $USER")

    # Create workspace for a new run
    run_dir = hpc.create_run("argon-diffusion")

    # Upload input files
    hpc.upload("local_input.lmp", f"{run_dir}/input.lmp")

    # Submit and monitor job
    job_id = hpc.submit(f"{run_dir}/job.slurm")
    status = hpc.wait_for_job(job_id, timeout=3600)

    # Download results
    hpc.download(f"{run_dir}/output.dat", "./results/")

    hpc.disconnect()
"""

import os
import subprocess
import time
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from datetime import datetime


@dataclass
class JobStatus:
    """Status of a SLURM job."""
    job_id: str
    state: str  # PENDING, RUNNING, COMPLETED, FAILED, TIMEOUT, CANCELLED
    exit_code: Optional[int] = None
    runtime: Optional[str] = None
    reason: Optional[str] = None

    @property
    def is_finished(self) -> bool:
        return self.state in ('COMPLETED', 'FAILED', 'TIMEOUT', 'CANCELLED', 'OUT_OF_MEMORY')

    @property
    def is_success(self) -> bool:
        return self.state == 'COMPLETED' and self.exit_code == 0


class HPCClient:
    """
    Client for interacting with CURC HPC cluster.

    Handles SSH connection management with ControlMaster multiplexing
    for efficient, persistent connections.
    """

    def __init__(
        self,
        user: Optional[str] = None,
        host: str = "login.rc.colorado.edu",
        ssh_alias: str = "cu_alpine",
        workspace_base: Optional[str] = None
    ):
        """
        Initialize HPC client.

        Args:
            user: CURC username (defaults to CURC_USER env var)
            host: Login node hostname
            ssh_alias: SSH config host alias (uses ~/.ssh/config settings)
            workspace_base: Base path for agent workspaces (defaults to /scratch/alpine/$USER/agent-workspace)
        """
        self.user = user or os.environ.get('CURC_USER')
        if not self.user:
            raise ValueError("CURC_USER environment variable not set and no user provided")

        self.host = host
        self.ssh_alias = ssh_alias  # Uses ~/.ssh/config for ControlMaster settings
        self.workspace_base = workspace_base or f"/scratch/alpine/{self.user}/Agent_Runs"

        self._connected = False

    @property
    def ssh_target(self) -> str:
        """SSH target string - uses alias if configured, else user@host."""
        return self.ssh_alias

    @property
    def scp_target(self) -> str:
        """SCP target string - needs user@host format."""
        return f"{self.user}@{self.host}"

    def _ssh_base_args(self) -> List[str]:
        """Base SSH arguments - leverages ~/.ssh/config for ControlMaster."""
        return [
            "ssh",
            "-o", "BatchMode=yes",       # Don't prompt for passwords
        ]

    def connect(self) -> bool:
        """
        Establish SSH connection with ControlMaster.

        Uses ~/.ssh/config settings for the cu_alpine host alias,
        which already has ControlMaster configured.

        Returns:
            True if connection successful
        """
        if self._connected:
            return True

        # Test connection - SSH config handles ControlMaster
        result = subprocess.run(
            self._ssh_base_args() + [self.ssh_target, "echo", "connected"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and "connected" in result.stdout:
            self._connected = True
            print(f"Connected to {self.ssh_target} ({self.user}@{self.host})")
            return True
        else:
            print(f"Connection failed: {result.stderr}")
            return False

    def disconnect(self):
        """Close SSH ControlMaster connection."""
        # ControlMaster is managed by ~/.ssh/config with ControlPersist
        # No need to explicitly close - it will timeout after 600s of inactivity
        self._connected = False
        print(f"Disconnected from {self.ssh_target}")

    def run(self, command: str, timeout: int = 120) -> Tuple[int, str, str]:
        """
        Run a command on HPC.

        This is the most flexible method - agent can run ANY command.

        Args:
            command: Shell command to run on HPC
            timeout: Command timeout in seconds

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        if not self._connected:
            self.connect()

        result = subprocess.run(
            self._ssh_base_args() + [self.ssh_target, command],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return result.returncode, result.stdout, result.stderr

    def run_check(self, command: str, timeout: int = 120) -> str:
        """
        Run command and raise exception on failure.

        Args:
            command: Shell command to run
            timeout: Command timeout

        Returns:
            stdout on success

        Raises:
            RuntimeError on non-zero exit code
        """
        code, stdout, stderr = self.run(command, timeout)
        if code != 0:
            raise RuntimeError(f"Command failed (exit {code}): {stderr}")
        return stdout

    # =========================================================================
    # Workspace Management
    # =========================================================================

    def init_workspace(self) -> str:
        """
        Initialize the agent workspace structure on HPC.

        Returns:
            Path to workspace base directory
        """
        self.run_check(f"mkdir -p {self.workspace_base}/runs")
        self.run_check(f"mkdir -p {self.workspace_base}/shared/potentials")
        self.run_check(f"mkdir -p {self.workspace_base}/shared/pseudopotentials")
        self.run_check(f"mkdir -p {self.workspace_base}/shared/scripts")

        print(f"Workspace initialized at {self.workspace_base}")
        return self.workspace_base

    def create_run(self, name: str, subdirs: List[str] = None) -> str:
        """
        Create a new run directory with timestamp.

        Args:
            name: Descriptive name for the run
            subdirs: Subdirectories to create (default: inputs, outputs)

        Returns:
            Full path to run directory on HPC
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_name = f"{name}-{timestamp}"
        run_dir = f"{self.workspace_base}/runs/{run_name}"

        subdirs = subdirs or ["inputs", "outputs"]
        subdir_str = " ".join(f"{run_dir}/{s}" for s in subdirs)

        self.run_check(f"mkdir -p {subdir_str}")

        print(f"Created run directory: {run_dir}")
        return run_dir

    def list_runs(self) -> List[str]:
        """List all run directories."""
        code, stdout, _ = self.run(f"ls -1 {self.workspace_base}/runs/ 2>/dev/null")
        if code != 0:
            return []
        return [r.strip() for r in stdout.strip().split('\n') if r.strip()]

    # =========================================================================
    # File Transfer
    # =========================================================================

    def upload(self, local_path: str, remote_path: str) -> bool:
        """
        Upload file or directory to HPC.

        Args:
            local_path: Local file/directory path
            remote_path: Destination path on HPC

        Returns:
            True on success
        """
        local = Path(local_path)

        # Use scp with the SSH alias to leverage ControlMaster from config
        scp_args = ["scp", "-o", "BatchMode=yes"]

        if local.is_dir():
            scp_args.append("-r")

        # Use scp_target (user@host) for file transfer
        scp_args.extend([str(local), f"{self.scp_target}:{remote_path}"])

        result = subprocess.run(scp_args, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            print(f"Upload failed: {result.stderr}")
            return False

        print(f"Uploaded {local_path} -> {remote_path}")
        return True

    def download(self, remote_path: str, local_path: str) -> bool:
        """
        Download file or directory from HPC.

        Args:
            remote_path: Path on HPC
            local_path: Local destination path

        Returns:
            True on success
        """
        # Ensure local directory exists
        local = Path(local_path)
        if local_path.endswith('/'):
            local.mkdir(parents=True, exist_ok=True)
        else:
            local.parent.mkdir(parents=True, exist_ok=True)

        scp_args = [
            "scp", "-o", "BatchMode=yes",
            "-r",  # Always use -r for safety
            f"{self.scp_target}:{remote_path}",
            str(local)
        ]

        result = subprocess.run(scp_args, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            print(f"Download failed: {result.stderr}")
            return False

        print(f"Downloaded {remote_path} -> {local_path}")
        return True

    def sync_to_hpc(self, local_dir: str, remote_dir: str) -> bool:
        """
        Sync local directory to HPC using rsync.

        Args:
            local_dir: Local directory
            remote_dir: Remote directory on HPC

        Returns:
            True on success
        """
        rsync_args = [
            "rsync", "-avz", "--progress",
            "-e", "ssh",  # Uses ~/.ssh/config settings
            f"{local_dir}/",
            f"{self.scp_target}:{remote_dir}/"
        ]

        result = subprocess.run(rsync_args, capture_output=True, text=True, timeout=600)
        return result.returncode == 0

    # =========================================================================
    # Job Management
    # =========================================================================

    def submit(self, script_path: str) -> str:
        """
        Submit a SLURM job script.

        Args:
            script_path: Path to job script on HPC

        Returns:
            Job ID as string
        """
        # Get directory of script for submission
        script_dir = str(Path(script_path).parent)
        script_name = Path(script_path).name

        stdout = self.run_check(f"cd {script_dir} && sbatch {script_name}")

        # Parse job ID from "Submitted batch job 12345"
        parts = stdout.strip().split()
        job_id = parts[-1]

        print(f"Submitted job {job_id}")
        return job_id

    def get_job_status(self, job_id: str) -> JobStatus:
        """
        Get status of a SLURM job.

        Args:
            job_id: SLURM job ID

        Returns:
            JobStatus object
        """
        # Use sacct for completed jobs, squeue for running
        code, stdout, _ = self.run(
            f"sacct -j {job_id} --format=JobID,State,ExitCode,Elapsed --noheader --parsable2 | head -1"
        )

        if code != 0 or not stdout.strip():
            # Job might be pending/running, try squeue
            code, stdout, _ = self.run(f"squeue -j {job_id} --format=%i|%T|%r --noheader")
            if code != 0 or not stdout.strip():
                return JobStatus(job_id=job_id, state="UNKNOWN")

            parts = stdout.strip().split('|')
            return JobStatus(
                job_id=parts[0],
                state=parts[1] if len(parts) > 1 else "UNKNOWN",
                reason=parts[2] if len(parts) > 2 else None
            )

        # Parse sacct output
        parts = stdout.strip().split('|')
        exit_code = None
        if len(parts) > 2 and ':' in parts[2]:
            exit_code = int(parts[2].split(':')[0])

        return JobStatus(
            job_id=parts[0],
            state=parts[1] if len(parts) > 1 else "UNKNOWN",
            exit_code=exit_code,
            runtime=parts[3] if len(parts) > 3 else None
        )

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a SLURM job."""
        code, _, _ = self.run(f"scancel {job_id}")
        return code == 0

    def wait_for_job(
        self,
        job_id: str,
        timeout: int = 86400,  # 24 hours default
        poll_interval: int = 30
    ) -> JobStatus:
        """
        Wait for a job to complete.

        Args:
            job_id: SLURM job ID
            timeout: Maximum wait time in seconds
            poll_interval: Seconds between status checks

        Returns:
            Final JobStatus
        """
        start_time = time.time()
        last_state = None

        while (time.time() - start_time) < timeout:
            status = self.get_job_status(job_id)

            if status.state != last_state:
                print(f"Job {job_id}: {status.state}")
                last_state = status.state

            if status.is_finished:
                return status

            time.sleep(poll_interval)

        # Timeout reached
        return JobStatus(job_id=job_id, state="TIMEOUT", reason="Client-side timeout")

    def list_jobs(self, all_users: bool = False) -> List[Dict]:
        """
        List SLURM jobs.

        Args:
            all_users: If True, list all users' jobs

        Returns:
            List of job dictionaries
        """
        user_flag = "" if all_users else f"-u {self.user}"
        code, stdout, _ = self.run(
            f"squeue {user_flag} --format='%i|%j|%T|%M|%P|%l|%S' --noheader"
        )

        if code != 0:
            return []

        jobs = []
        for line in stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split('|')
            if len(parts) >= 6:
                jobs.append({
                    'job_id': parts[0],
                    'name': parts[1],
                    'state': parts[2],
                    'time': parts[3],
                    'partition': parts[4],
                    'time_limit': parts[5],
                    'start_time': parts[6] if len(parts) > 6 else 'N/A'
                })

        return jobs

    # =========================================================================
    # Queue Analysis (for smart partition selection)
    # =========================================================================

    def get_queue_status(self, partition: str = None) -> Dict:
        """
        Get queue status for a partition to estimate wait times.

        Args:
            partition: Partition name (default: all partitions)

        Returns:
            Dict with queue statistics
        """
        part_flag = f"-p {partition}" if partition else ""

        # Get pending jobs with start time estimates
        code, stdout, _ = self.run(
            f"squeue {part_flag} --state=PENDING --format='%i|%S|%l|%D' --noheader"
        )

        pending_jobs = []
        if code == 0 and stdout.strip():
            for line in stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('|')
                    pending_jobs.append({
                        'job_id': parts[0],
                        'est_start': parts[1] if len(parts) > 1 else 'N/A',
                        'time_limit': parts[2] if len(parts) > 2 else 'N/A',
                        'nodes': parts[3] if len(parts) > 3 else '1'
                    })

        # Get running jobs
        code, stdout, _ = self.run(
            f"squeue {part_flag} --state=RUNNING --format='%i' --noheader | wc -l"
        )
        running_count = int(stdout.strip()) if code == 0 and stdout.strip() else 0

        # Get node availability
        code, stdout, _ = self.run(
            f"sinfo {part_flag} --format='%D|%a' --noheader 2>/dev/null"
        )
        total_nodes = 0
        avail_nodes = 0
        if code == 0 and stdout.strip():
            for line in stdout.strip().split('\n'):
                parts = line.split('|')
                if len(parts) >= 2:
                    total_nodes += int(parts[0])
                    if 'up' in parts[1]:
                        avail_nodes += int(parts[0])

        return {
            'partition': partition or 'all',
            'pending_jobs': len(pending_jobs),
            'running_jobs': running_count,
            'total_nodes': total_nodes,
            'jobs_with_start_estimate': [j for j in pending_jobs if j['est_start'] != 'N/A'][:5],
            'estimated_wait': self._estimate_wait(pending_jobs)
        }

    def _estimate_wait(self, pending_jobs: List[Dict]) -> str:
        """Estimate wait time based on pending jobs with start times."""
        from datetime import datetime

        jobs_with_times = [j for j in pending_jobs if j['est_start'] != 'N/A']
        if not jobs_with_times:
            return "unknown (no estimates available)"

        # Find the latest estimated start time
        latest = None
        for job in jobs_with_times:
            try:
                start = datetime.strptime(job['est_start'], '%Y-%m-%dT%H:%M:%S')
                if latest is None or start > latest:
                    latest = start
            except ValueError:
                continue

        if latest:
            now = datetime.now()
            if latest > now:
                delta = latest - now
                days = delta.days
                hours = delta.seconds // 3600
                if days > 0:
                    return f"~{days}d {hours}h (based on queue)"
                else:
                    return f"~{hours}h (based on queue)"

        return "unknown"

    def compare_partitions(self, partitions: List[str] = None) -> List[Dict]:
        """
        Compare queue status across partitions to help choose.

        Args:
            partitions: List of partitions to compare (default: common ones)

        Returns:
            List of partition status dicts, sorted by estimated wait
        """
        partitions = partitions or ['atesting', 'amilan', 'amilan128c', 'aa100']

        results = []
        for part in partitions:
            status = self.get_queue_status(part)
            results.append(status)

        return results

    # =========================================================================
    # Async Job Management (for long-running jobs)
    # =========================================================================

    def submit_async(self, script_path: str, run_dir: str = None) -> Dict:
        """
        Submit a job and return immediately with tracking info.

        For jobs with long queue times, use this instead of submit + wait.
        Saves job info to a tracking file for later status checks.

        Args:
            script_path: Path to job script on HPC
            run_dir: Directory to save tracking file (default: script directory)

        Returns:
            Dict with job_id, tracking_file path, and submission info
        """
        import json
        from datetime import datetime

        job_id = self.submit(script_path)

        # Get initial status with start time estimate
        status = self.get_job_status(job_id)
        _, start_est, _ = self.run(f"squeue -j {job_id} --format='%S' --noheader")

        # Save tracking info
        run_dir = run_dir or str(Path(script_path).parent)
        tracking_file = f"{run_dir}/job_{job_id}_tracking.json"

        tracking_info = {
            'job_id': job_id,
            'script': script_path,
            'submitted_at': datetime.now().isoformat(),
            'status': status.state,
            'estimated_start': start_est.strip() if start_est else 'N/A',
            'tracking_file': tracking_file
        }

        self.write_file(tracking_file, json.dumps(tracking_info, indent=2))

        print(f"Job {job_id} submitted (async)")
        print(f"Estimated start: {tracking_info['estimated_start']}")
        print(f"Tracking file: {tracking_file}")

        return tracking_info

    def check_async_jobs(self, run_dir: str = None) -> List[Dict]:
        """
        Check status of all async-submitted jobs.

        Args:
            run_dir: Directory to search for tracking files (default: workspace)

        Returns:
            List of job status dicts
        """
        import json

        run_dir = run_dir or self.workspace_base

        # Find all tracking files
        code, stdout, _ = self.run(f"find {run_dir} -name 'job_*_tracking.json' 2>/dev/null")

        if code != 0 or not stdout.strip():
            return []

        results = []
        for tracking_file in stdout.strip().split('\n'):
            if not tracking_file.strip():
                continue

            try:
                content = self.read_file(tracking_file)
                info = json.loads(content)
                job_id = info['job_id']

                # Get current status
                status = self.get_job_status(job_id)
                info['current_status'] = status.state
                info['is_finished'] = status.is_finished
                info['is_success'] = status.is_success

                results.append(info)
            except Exception as e:
                print(f"Error reading {tracking_file}: {e}")

        return results

    # =========================================================================
    # Module Management
    # =========================================================================

    def list_modules(self, pattern: str = "") -> str:
        """
        List available modules.

        Args:
            pattern: Optional filter pattern

        Returns:
            Module listing output
        """
        if pattern:
            code, stdout, stderr = self.run(f"module spider {pattern} 2>&1")
        else:
            code, stdout, stderr = self.run("module avail 2>&1")

        return stdout + stderr

    def get_module_info(self, module_name: str) -> str:
        """Get detailed info about a module."""
        _, output, _ = self.run(f"module spider {module_name} 2>&1")
        return output

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def read_file(self, remote_path: str, max_lines: int = None) -> str:
        """
        Read a file on HPC.

        Args:
            remote_path: Path to file on HPC
            max_lines: Optional limit on lines to read

        Returns:
            File contents
        """
        if max_lines:
            cmd = f"head -n {max_lines} {remote_path}"
        else:
            cmd = f"cat {remote_path}"

        code, stdout, stderr = self.run(cmd)
        if code != 0:
            raise FileNotFoundError(f"Cannot read {remote_path}: {stderr}")
        return stdout

    def write_file(self, remote_path: str, content: str):
        """
        Write content to a file on HPC.

        Args:
            remote_path: Destination path on HPC
            content: File content
        """
        # Write locally then upload (safer than heredoc over SSH)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tmp', delete=False) as f:
            f.write(content)
            local_tmp = f.name

        try:
            self.upload(local_tmp, remote_path)
        finally:
            os.unlink(local_tmp)

    def file_exists(self, remote_path: str) -> bool:
        """Check if a file exists on HPC."""
        code, _, _ = self.run(f"test -e {remote_path}")
        return code == 0

    def list_dir(self, remote_path: str) -> List[str]:
        """List directory contents on HPC."""
        code, stdout, _ = self.run(f"ls -1 {remote_path}")
        if code != 0:
            return []
        return [f.strip() for f in stdout.split('\n') if f.strip()]


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI for testing HPC client."""
    import argparse

    parser = argparse.ArgumentParser(description="CURC HPC Client")
    parser.add_argument("command", choices=["connect", "run", "submit", "status", "jobs", "modules"])
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--user", help="CURC username")

    args = parser.parse_args()

    hpc = HPCClient(user=args.user)

    try:
        if args.command == "connect":
            hpc.connect()
            print("Connection test successful")

        elif args.command == "run":
            cmd = " ".join(args.args)
            code, stdout, stderr = hpc.run(cmd)
            print(stdout)
            if stderr:
                print(f"STDERR: {stderr}")
            exit(code)

        elif args.command == "submit":
            if not args.args:
                print("Usage: hpc_client.py submit <script_path>")
                exit(1)
            job_id = hpc.submit(args.args[0])
            print(f"Job ID: {job_id}")

        elif args.command == "status":
            if not args.args:
                print("Usage: hpc_client.py status <job_id>")
                exit(1)
            status = hpc.get_job_status(args.args[0])
            print(f"Job {status.job_id}: {status.state}")
            if status.exit_code is not None:
                print(f"Exit code: {status.exit_code}")

        elif args.command == "jobs":
            jobs = hpc.list_jobs()
            for job in jobs:
                print(f"{job['job_id']}: {job['name']} ({job['state']})")

        elif args.command == "modules":
            pattern = args.args[0] if args.args else ""
            print(hpc.list_modules(pattern))

    finally:
        hpc.disconnect()


if __name__ == "__main__":
    main()
