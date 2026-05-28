
import subprocess
import sys

def run_rclone(args, capture_output=False):
    try:
        cmd = ["rclone"] + args
        result = subprocess.run(cmd, check=True, capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running rclone: {e}")
        if capture_output:
            print(e.stderr)
        return None
    except FileNotFoundError:
        print("Error: rclone not found. Please install rclone.")
        sys.exit(1)
