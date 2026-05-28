#!/usr/bin/env python3
"""
Real-Debrid Torrent Cleanup Script

Identifies and removes dead, unavailable, or error torrents from Real-Debrid account.

Usage:
    python3 cleanup_realdebrid.py              # Interactive mode
    python3 cleanup_realdebrid.py --dry-run    # Show what would be deleted

Requirements:
    - requests library (pip install requests)
    - Real-Debrid API key in SECRETS.md or environment variable RD_API_KEY
"""

import requests
import sys
import time
import os

# Get API key from environment or use default (update in SECRETS.md)
API_KEY = os.getenv("RD_API_KEY", "HZLVDRPVBT7RPTNFQ6V2MEF2Z74UKJWCMJC")
BASE_URL = "https://api.real-debrid.com/rest/1.0"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Statuses that indicate dead/unusable torrents
DEAD_STATUSES = ["magnet_error", "dead", "virus", "error", "timeout"]

# Whitelist - torrents to NEVER delete (customize this list)
WHITELIST = [
    "Naruto",
    "4QMHWXG66PW64"
]

def get_all_torrents():
    """Fetch all torrents from Real-Debrid (handles pagination)"""
    all_torrents = []
    page = 1

    while True:
        url = f"{BASE_URL}/torrents?limit=100&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            break

        torrents = response.json()
        if not torrents:
            break

        all_torrents.extend(torrents)
        page += 1
        time.sleep(0.5)  # Rate limit protection

    return all_torrents

def is_whitelisted(torrent):
    """Check if torrent is in whitelist"""
    for item in WHITELIST:
        if item in torrent["filename"] or item == torrent["id"]:
            return True
    return False

def identify_dead_torrents(torrents):
    """Filter dead torrents that can be deleted"""
    dead = []

    for torrent in torrents:
        status = torrent.get("status", "")

        # Skip active/healthy torrents
        if status not in DEAD_STATUSES:
            continue

        # Skip whitelisted
        if is_whitelisted(torrent):
            print(f"⚠️  Skipping (whitelisted): {torrent['filename']}")
            continue

        dead.append(torrent)

    return dead

def delete_torrent(torrent_id):
    """Delete a torrent by ID"""
    url = f"{BASE_URL}/torrents/delete/{torrent_id}"
    response = requests.delete(url, headers=HEADERS)

    return response.status_code == 204

def main():
    dry_run = "--dry-run" in sys.argv

    print("📊 Fetching Real-Debrid torrents...")
    all_torrents = get_all_torrents()

    print(f"Total torrents: {len(all_torrents)}")

    # Categorize by status
    status_counts = {}
    total_size = 0

    for torrent in all_torrents:
        status = torrent.get("status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
        total_size += torrent.get("bytes", 0)

    print(f"Total size: {total_size / 1024**3:.2f} GB")
    print("\n--- Status Breakdown ---")
    for status, count in sorted(status_counts.items()):
        emoji = "🟢" if status == "downloaded" else ("🔴" if status in DEAD_STATUSES else "🟡")
        print(f"{emoji} {status}: {count}")

    # Identify dead torrents
    dead_torrents = identify_dead_torrents(all_torrents)

    if not dead_torrents:
        print("\n✅ No dead torrents found!")
        return

    print(f"\n🔴 Found {len(dead_torrents)} dead torrents")

    # Calculate space to free
    dead_size = sum(t.get("bytes", 0) for t in dead_torrents)
    print(f"Reclaimable: {dead_size / 1024**3:.2f} GB")

    # Show list
    print("\n--- Dead Torrents ---")
    for i, torrent in enumerate(dead_torrents[:20], 1):
        status = torrent.get("status", "unknown")
        name = torrent.get("filename", "Unknown")
        print(f"{i}. [{status.upper()}] {name}")

    if len(dead_torrents) > 20:
        print(f"... and {len(dead_torrents) - 20} more")

    if dry_run:
        print("\n🔍 DRY-RUN MODE - No torrents will be deleted")
        return

    # Confirmation
    print(f"\n⚠️  About to delete {len(dead_torrents)} torrents")
    confirm = input("Type 'DELETE' to confirm: ")

    if confirm != "DELETE":
        print("❌ Cancelled")
        return

    # Delete torrents
    print("\n🗑️  Deleting torrents...")
    deleted = 0
    failed = 0

    for torrent in dead_torrents:
        torrent_id = torrent["id"]
        name = torrent["filename"]

        if delete_torrent(torrent_id):
            print(f"✓ Deleted: {name}")
            deleted += 1
        else:
            print(f"✗ Failed: {name}")
            failed += 1

        time.sleep(0.5)  # Rate limit protection

    print(f"\n✅ Cleanup completed")
    print(f"Deleted: {deleted}")
    print(f"Failed: {failed}")
    print(f"Freed: {dead_size / 1024**3:.2f} GB")

if __name__ == "__main__":
    main()
