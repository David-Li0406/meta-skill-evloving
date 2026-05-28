#!/usr/bin/env python3
"""
Jellyfin Library Scan Monitor

Monitors Jellyfin library scan progress in real-time.

Usage:
    python3 monitor_scan.py                    # Monitor until complete
    python3 monitor_scan.py --trigger          # Trigger scan then monitor
    python3 monitor_scan.py --library TV       # Monitor specific library

Requirements:
    - requests library
    - Jellyfin API token in environment or script
"""

import requests
import sys
import time
import os
from datetime import datetime

# Configuration
JELLYFIN_URL = os.getenv("JELLYFIN_URL", "http://localhost:8096")
API_TOKEN = os.getenv("JELLYFIN_API_TOKEN", "9af5f56a66e44ee68ddeec7bd07c9db8")
HEADERS = {"X-Emby-Token": API_TOKEN}

def trigger_scan(library_id=None):
    """Trigger a library scan"""
    if library_id:
        url = f"{JELLYFIN_URL}/Items/{library_id}/Refresh?Recursive=true"
    else:
        url = f"{JELLYFIN_URL}/Library/Refresh"

    response = requests.post(url, headers=HEADERS)

    if response.status_code in [200, 204]:
        print("✓ Library scan triggered")
        return True
    else:
        print(f"✗ Failed to trigger scan (HTTP {response.status_code})")
        return False

def get_scheduled_tasks():
    """Get all scheduled tasks"""
    url = f"{JELLYFIN_URL}/ScheduledTasks"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    return []

def find_scan_task(tasks):
    """Find the library scan task"""
    for task in tasks:
        if "Scan" in task.get("Name", "") or "Library" in task.get("Name", ""):
            return task
    return None

def get_library_counts():
    """Get library item counts"""
    url = f"{JELLYFIN_URL}/Items/Counts"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    return {}

def monitor_scan():
    """Monitor scan progress"""
    print("📊 Monitoring scan progress...")
    print("Press Ctrl+C to stop monitoring\n")

    last_state = None
    start_time = time.time()

    try:
        while True:
            tasks = get_scheduled_tasks()
            scan_task = find_scan_task(tasks)

            if scan_task:
                state = scan_task.get("State", "Unknown")
                current_progress = scan_task.get("CurrentProgressPercentage", 0)

                if state != last_state:
                    elapsed = int(time.time() - start_time)
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    if state == "Running":
                        print(f"[{timestamp}] 🔄 Scan running... ({current_progress}%) - {elapsed}s elapsed")
                    elif state == "Idle":
                        if last_state == "Running":
                            print(f"[{timestamp}] ✓ Scan completed! - Total time: {elapsed}s")

                            # Show final counts
                            counts = get_library_counts()
                            if counts:
                                print("\n--- Library Statistics ---")
                                print(f"  Series: {counts.get('SeriesCount', 0)}")
                                print(f"  Episodes: {counts.get('EpisodeCount', 0)}")
                                print(f"  Movies: {counts.get('MovieCount', 0)}")
                            break
                        else:
                            print(f"[{timestamp}] ⏸️  No scan running")

                    last_state = state

            time.sleep(5)  # Check every 5 seconds

    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")

def main():
    trigger = "--trigger" in sys.argv
    library_name = None

    if "--library" in sys.argv:
        idx = sys.argv.index("--library")
        if idx + 1 < len(sys.argv):
            library_name = sys.argv[idx + 1]

    if trigger:
        print("🔄 Triggering library scan...")
        if not trigger_scan():
            sys.exit(1)
        print("Waiting 5 seconds for scan to start...\n")
        time.sleep(5)

    monitor_scan()

if __name__ == "__main__":
    main()
