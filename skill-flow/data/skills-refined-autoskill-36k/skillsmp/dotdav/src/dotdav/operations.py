
import os
import sys
import shutil
import time
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .config import Config, Mappings, REPO_DIR
from .utils import run_rclone
import fnmatch

def get_ignore_patterns(config):
    return config.get("ignores") or []

def make_rclone_excludes(patterns):
    args = []
    for p in patterns:
        args.extend(["--exclude", p])
    return args


def cmd_remove(args):
    # Don't resolve immediately to preserve symlink nature for checking
    # But expanduser is needed
    raw_path = Path(args.file).expanduser()
    target_path = raw_path.resolve()
    
    # Check if target is mapped
    config = Config()
    mappings = Mappings()
    profile = args.profile or config.get("current_profile")
    
    # Try to find mapping key using the raw path relative to home if possible
    try:
        rel_path = raw_path.relative_to(Path.home())
        mapping_key = str(rel_path)
    except ValueError:
        # If raw path fails (e.g. absolute not in home), try absolute
        try:
            rel_path = target_path.relative_to(Path.home())
            mapping_key = str(rel_path)
        except ValueError:
            mapping_key = str(target_path)

    if mapping_key not in mappings.data["files"]:
        # Try to find by checking if the input file is a symlink pointing to a repo file
        found = False
        # Check raw_path for symlink
        if raw_path.is_symlink():
            target_resolve = raw_path.resolve()
            for k, profiles in mappings.data["files"].items():
                repo_f = profiles.get(profile) or profiles.get("default")
                if repo_f and (REPO_DIR / repo_f).resolve() == target_resolve:
                    mapping_key = k
                    found = True
                    break
        if not found:
            print(f"Error: {raw_path} is not tracked by dotdav.")
            return

    repo_filename = mappings.get_repo_file(mapping_key, profile)
    if not repo_filename:
        print(f"Error: No version of {mapping_key} found for profile {profile}.")
        return

    repo_path = REPO_DIR / repo_filename
    
    # Restore file to the original location (raw_path)
    # raw_path is the user's file (e.g. ~/.bashrc), which should be a symlink or file
    print(f"Restoring {raw_path} from {repo_path}...")
    
    if raw_path.exists() or raw_path.is_symlink():
        if raw_path.is_dir() and not raw_path.is_symlink():
            shutil.rmtree(raw_path)
        else:
            raw_path.unlink()
    
    if repo_path.is_dir():
        shutil.copytree(repo_path, raw_path)
    else:
        shutil.copy2(repo_path, raw_path)
        
    # Remove from updates
    if profile in mappings.data["files"][mapping_key]:
        del mappings.data["files"][mapping_key][profile]
    
    if not mappings.data["files"][mapping_key]:
        del mappings.data["files"][mapping_key]
    mappings.save()
    
    # Remove from repo
    if repo_path.exists():
        if repo_path.is_dir():
            shutil.rmtree(repo_path)
        else:
            repo_path.unlink()
        # Clean up empty parent dir if needed (profile dir)
        if repo_path.parent != REPO_DIR and repo_path.parent.is_dir() and not any(repo_path.parent.iterdir()):
             repo_path.parent.rmdir()
             
    print(f"Removed {target_path} from dotdav management.")


def cmd_init(args):
    if not REPO_DIR.exists():
        REPO_DIR.mkdir()
    
    config = Config()
    if args.remote:
        config.set("rclone_remote", args.remote)
    if args.path:
        config.set("rclone_path", args.path)
    
    # Initialize mappings if not exists
    Mappings()
    
    print(f"Initialized dotdav in {os.getcwd()}")
    print("Project structure created.")

def cmd_add(args):
    target_path = Path(args.file).expanduser().resolve()
    if not target_path.exists():
        print(f"Error: File {target_path} not found.")
        return

    config = Config()
    mappings = Mappings()
    profile = args.profile or config.get("current_profile")
    
    # Define repo path: repo/profile/filename
    repo_subdir = REPO_DIR / profile
    if not repo_subdir.exists():
        repo_subdir.mkdir(parents=True)
        
    repo_filename = f"{profile}/{target_path.name}"
    dest_path = REPO_DIR / repo_filename
    
    
    # Copy file
    if target_path.is_dir():
        if dest_path.exists(): 
            shutil.rmtree(dest_path)
        
        # Prepare ignore patterns for copytree
        ignore_patterns = get_ignore_patterns(config)
        shutil.copytree(target_path, dest_path, ignore=shutil.ignore_patterns(*ignore_patterns))
    else:
        # For single files, we check if it matches ignore patterns? 
        # Usually checking single file add against ignores is good practice but user might force it.
        # skipping explicit check for now as user explicitly added it.
        shutil.copy2(target_path, dest_path)
        
    # Relative path from HOME for mapping key
    try:
        rel_path = target_path.relative_to(Path.home())
        mapping_key = str(rel_path)
    except ValueError:
        # Not under HOME, use absolute path key (less portable)
        mapping_key = str(target_path)
        print(f"Warning: File {target_path} is not under {Path.home()}. using absolute path as key.")

    mappings.add_file(mapping_key, profile, repo_filename)
    print(f"Added {target_path} as {repo_filename} (profile: {profile})")

def cmd_profile(args):
    config = Config()
    if args.name:
        config.set("current_profile", args.name)
        print(f"Switched to profile: {args.name}")
    else:
        print(f"Current profile: {config.get('current_profile')}")

def cmd_deploy(args):
    config = Config()
    mappings = Mappings()
    current_profile = config.get("current_profile")
    
    for user_file, profiles in mappings.data["files"].items():
        # Determine source in repo
        repo_file = profiles.get(current_profile) or profiles.get("default")
        if not repo_file:
            print(f"Skipping {user_file}: No version for {current_profile} or default.")
            continue
            
        repo_path = REPO_DIR / repo_file
        if not repo_path.exists():
            print(f"Warning: Repository file {repo_file} missing for {user_file}")
            continue
            
        # Determine dest in HOME
        if user_file.startswith("/"):
            dest_path = Path(user_file)
        else:
            dest_path = Path.home() / user_file
            
        # Create parent dirs
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True)
            
        # Symlink
        if dest_path.is_symlink() or dest_path.exists():
            if args.force:
                if dest_path.is_dir() and not dest_path.is_symlink():
                     shutil.rmtree(dest_path)
                else:
                     dest_path.unlink()
            else:
                # Check if it already points to correctly
                if dest_path.is_symlink() and dest_path.resolve() == repo_path.resolve():
                    print(f"uptodate: {user_file}")
                    continue
                print(f"Conflict: {dest_path} exists. Use --force to overwrite.")
                continue
        
        try:
            dest_path.symlink_to(repo_path.resolve())
            print(f"Linked {user_file} -> {repo_file}")
        except Exception as e:
            print(f"Error linking {user_file}: {e}")
            
    # Auto-install completions
    # Assumes completions.fish is in project root, 2 dirs up from src/dotdav
    project_root = Path(__file__).parent.parent.parent
    source_completion = project_root / "completions.fish"
    
    if source_completion.exists():
        fish_completions_dir = Path.home() / ".config/fish/completions"
        if not fish_completions_dir.exists():
            try:
                fish_completions_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass # Can't create, skip
        
        if fish_completions_dir.exists():
            dest_completion = fish_completions_dir / "dotdav.fish"
            # Remove existing if needed
            if dest_completion.is_symlink() or dest_completion.exists():
                if dest_completion.resolve() == source_completion.resolve():
                    print("Completions already installed.")
                else:
                    try:
                        if dest_completion.is_dir():
                            shutil.rmtree(dest_completion)
                        else:
                            dest_completion.unlink()
                        dest_completion.symlink_to(source_completion)
                        print(f"Installed completions to {dest_completion}")
                    except Exception as e:
                        print(f"Failed to update completions: {e}")
            else:
                 try:
                    dest_completion.symlink_to(source_completion)
                    print(f"Installed completions to {dest_completion}")
                 except Exception as e:
                    print(f"Failed to install completions: {e}")
    else:
        # Fallback: try to find it if we are installed solely as package? 
        # For now, simplistic approach for this dev environment is sufficient.
        pass


def cmd_sync(args):
    config = Config()
    remote = config.get("rclone_remote")
    path = config.get("rclone_path")
    
    if not remote:
        print("Error: rclone_remote not configured. Run 'dotdav init --remote <name>'")
        return

    remote_url = f"{remote}:{path}"
    ignores = get_ignore_patterns(config)
    rclone_flags = make_rclone_excludes(ignores)
    
    if args.action == "push":
        print(f"Pushing to {remote_url}...")
        run_rclone(["sync", str(REPO_DIR), remote_url, "--progress"] + rclone_flags)
    elif args.action == "pull":
        print(f"Pulling from {remote_url}...")
        run_rclone(["sync", remote_url, str(REPO_DIR), "--progress"] + rclone_flags)

class AutoSyncHandler(FileSystemEventHandler):
    def __init__(self, callback, debounce=2.0, ignores=None):
        self.callback = callback
        self.debounce = debounce
        self.timer = None
        self.ignores = ignores or []
    
    def on_any_event(self, event):
        if event.is_directory:
            return
            
        # Check ignores
        filename = os.path.basename(event.src_path)
        for pattern in self.ignores:
            if fnmatch.fnmatch(filename, pattern):
                return
                
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.debounce, self.callback)
        self.timer.start()

def cmd_autosync(args):
    config = Config()
    remote = config.get("rclone_remote")
    
    if not remote:
        print("Error: rclone_remote not configured.")
        return

    print("Starting AutoSync Daemon...")
    
    sync_lock = threading.Lock()
    ignores = get_ignore_patterns(config)
    rclone_flags = make_rclone_excludes(ignores)
    
    # 1. Periodic Pull
    interval = config.get("sync_interval_minutes") * 60
    
    def periodic_pull():
        while True:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Auto-Pull started...")
            remote_url = f"{remote}:{config.get('rclone_path')}"
            with sync_lock:
                run_rclone(["sync", remote_url, str(REPO_DIR)] + rclone_flags)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Auto-Pull finished.")
            time.sleep(interval)
            
    pull_thread = threading.Thread(target=periodic_pull, daemon=True)
    pull_thread.start()
    
    # 2. Watch for changes (Push)
    def push_callback():
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Detected changes. Pushing...")
        remote_url = f"{remote}:{config.get('rclone_path')}"
        with sync_lock:
            run_rclone(["sync", str(REPO_DIR), remote_url] + rclone_flags)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Push finished.")

    observer = Observer()
    handler = AutoSyncHandler(push_callback, debounce=config.get("debounce_seconds"), ignores=ignores)
    observer.schedule(handler, str(REPO_DIR), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def cmd_service(args):
    service_dir = Path.home() / ".config/systemd/user"
    service_file = service_dir / "dotdav.service"
    
    if args.action == "install":
        if not service_dir.exists():
            service_dir.mkdir(parents=True)
            
        python_exec = sys.executable
        # NOTE: When refactored, we need to point to the installed executable or proper module
        # For now, we assume 'dotdav' is available in path if installed via pip/uv
        # But to be safe in dev, we might point to main.py
        # Ideally, we use `-m dotdav.main` if running via python
        
        # NOTE: Adjusted logic to use '-m dotdav.main'
        script_args = "-m dotdav.main"
        
        content = f"""[Unit]
Description=Dotfile AutoSync Service
After=network.target

[Service]
ExecStart={python_exec} {script_args} autosync
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
"""
        with open(service_file, "w") as f:
            f.write(content)
            
        print(f"Service file created at {service_file}")
        print("Enabling service...")
        subprocess.run(["systemctl", "--user", "daemon-reload"])
        subprocess.run(["systemctl", "--user", "enable", "--now", "dotdav.service"])
        print("Service installed and started.")
        
    elif args.action == "uninstall":
        if service_file.exists():
            subprocess.run(["systemctl", "--user", "stop", "dotdav.service"])
            subprocess.run(["systemctl", "--user", "disable", "dotdav.service"])
            service_file.unlink()
            print("Service uninstalled.")
        else:
            print("Service file not found.")
