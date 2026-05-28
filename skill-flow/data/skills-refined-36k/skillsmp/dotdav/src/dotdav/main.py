
import argparse
from .operations import (
    cmd_init, cmd_add, cmd_remove, cmd_profile, cmd_deploy, 
    cmd_sync, cmd_autosync, cmd_service
)

def main():
    parser = argparse.ArgumentParser(description="Dotfile synchronization tool (dotdav)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Init
    p_init = subparsers.add_parser("init", help="Initialize repository")
    p_init.add_argument("--remote", help="rclone remote name")
    p_init.add_argument("--path", help="path on remote")
    
    # Add
    p_add = subparsers.add_parser("add", help="Add file to management")
    p_add.add_argument("file", help="File to add")
    p_add.add_argument("--profile", help="Specific profile", default=None)
    
    # Remove
    p_remove = subparsers.add_parser("remove", help="Remove file from management")
    p_remove.add_argument("file", help="File to remove")
    p_remove.add_argument("--profile", help="Specific profile", default=None)

    
    # Profile
    p_profile = subparsers.add_parser("profile", help="Get or set current profile")
    p_profile.add_argument("name", nargs="?", help="Profile name")
    
    # Deploy
    p_deploy = subparsers.add_parser("deploy", help="Deploy symlinks")
    p_deploy.add_argument("--force", action="store_true", help="Overwrite existing files")
    
    # Sync
    p_sync = subparsers.add_parser("sync", help="Manual sync")
    p_sync.add_argument("action", choices=["push", "pull"], help="Action to perform")

    # Autosync
    p_autosync = subparsers.add_parser("autosync", help="Run auto-sync daemon")
    
    # Service
    p_service = subparsers.add_parser("service", help="Manage systemd service")
    p_service.add_argument("action", choices=["install", "uninstall"], help="Action")

    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "profile":
        cmd_profile(args)
    elif args.command == "deploy":
        cmd_deploy(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "autosync":
        cmd_autosync(args)
    elif args.command == "service":
        cmd_service(args)

if __name__ == "__main__":
    main()
