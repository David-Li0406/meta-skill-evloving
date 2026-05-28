#!/usr/bin/env python3
"""
ARC Campaign Tracker
Track advance review copy readers and review submissions.

Usage:
    python arc_tracker.py create --book "Book Title" --launch "2026-02-01"
    python arc_tracker.py add --name "John Doe" --email "john@email.com"
    python arc_tracker.py update --email "john@email.com" --status downloaded
    python arc_tracker.py report
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

def create_campaign(book_title: str, launch_date: str) -> str:
    """Create new ARC campaign tracker."""
    
    campaign = {
        "book_title": book_title,
        "launch_date": launch_date,
        "created_at": datetime.now().isoformat(),
        "targets": {
            "signups": 100,
            "downloads": 75,
            "reviews": 25
        },
        "readers": []
    }
    
    filename = f"arc_campaign_{launch_date}.json"
    with open(filename, 'w') as f:
        json.dump(campaign, f, indent=2)
    
    print(f"✅ Created ARC campaign: {filename}")
    return filename

def add_reader(filename: str, name: str, email: str, source: str = "email"):
    """Add a new ARC reader to the campaign."""
    
    with open(filename, 'r') as f:
        campaign = json.load(f)
    
    # Check for duplicate
    if any(r['email'].lower() == email.lower() for r in campaign['readers']):
        print(f"⚠️ Reader already exists: {email}")
        return
    
    reader = {
        "name": name,
        "email": email,
        "source": source,
        "signed_up": datetime.now().isoformat(),
        "downloaded": None,
        "read": False,
        "review_posted": None,
        "review_rating": None,
        "notes": ""
    }
    
    campaign['readers'].append(reader)
    
    with open(filename, 'w') as f:
        json.dump(campaign, f, indent=2)
    
    print(f"✅ Added reader: {name} ({email})")

def update_reader(filename: str, email: str, status: str, value: str = None):
    """Update reader status."""
    
    with open(filename, 'r') as f:
        campaign = json.load(f)
    
    for reader in campaign['readers']:
        if reader['email'].lower() == email.lower():
            if status == 'downloaded':
                reader['downloaded'] = datetime.now().isoformat()
            elif status == 'read':
                reader['read'] = True
            elif status == 'reviewed':
                reader['review_posted'] = datetime.now().isoformat()
                if value:
                    reader['review_rating'] = int(value)
            elif status == 'notes':
                reader['notes'] = value
            
            with open(filename, 'w') as f:
                json.dump(campaign, f, indent=2)
            
            print(f"✅ Updated {email}: {status}")
            return
    
    print(f"❌ Reader not found: {email}")

def generate_report(filename: str):
    """Generate ARC campaign progress report."""
    
    with open(filename, 'r') as f:
        campaign = json.load(f)
    
    readers = campaign['readers']
    targets = campaign['targets']
    launch = datetime.fromisoformat(campaign['launch_date'])
    days_to_launch = (launch - datetime.now()).days
    
    # Calculate metrics
    total = len(readers)
    downloaded = sum(1 for r in readers if r['downloaded'])
    read = sum(1 for r in readers if r['read'])
    reviewed = sum(1 for r in readers if r['review_posted'])
    
    # Calculate averages
    ratings = [r['review_rating'] for r in readers if r['review_rating']]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    # Conversion rates
    download_rate = (downloaded / total * 100) if total > 0 else 0
    read_rate = (read / downloaded * 100) if downloaded > 0 else 0
    review_rate = (reviewed / read * 100) if read > 0 else 0
    
    # Progress vs targets
    signup_progress = (total / targets['signups'] * 100)
    download_progress = (downloaded / targets['downloads'] * 100)
    review_progress = (reviewed / targets['reviews'] * 100)
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║                 ARC CAMPAIGN REPORT                          ║
╠══════════════════════════════════════════════════════════════╣
║ Book: {campaign['book_title'][:50]:<50} ║
║ Launch Date: {campaign['launch_date']:<47} ║
║ Days to Launch: {days_to_launch:<44} ║
╠══════════════════════════════════════════════════════════════╣
║                     FUNNEL METRICS                           ║
╠══════════════════════════════════════════════════════════════╣
║ Signups:    {total:>5} / {targets['signups']:<5} ({signup_progress:>5.1f}%) {'✅' if signup_progress >= 100 else '⏳':<16} ║
║ Downloads:  {downloaded:>5} / {targets['downloads']:<5} ({download_progress:>5.1f}%) {'✅' if download_progress >= 100 else '⏳':<16} ║
║ Reviews:    {reviewed:>5} / {targets['reviews']:<5} ({review_progress:>5.1f}%) {'✅' if review_progress >= 100 else '⏳':<16} ║
╠══════════════════════════════════════════════════════════════╣
║                  CONVERSION RATES                            ║
╠══════════════════════════════════════════════════════════════╣
║ Signup → Download: {download_rate:>5.1f}% (target: 75%)  {'✅' if download_rate >= 75 else '⚠️':<16} ║
║ Download → Read:   {read_rate:>5.1f}% (target: 67%)  {'✅' if read_rate >= 67 else '⚠️':<16} ║
║ Read → Review:     {review_rate:>5.1f}% (target: 50%)  {'✅' if review_rate >= 50 else '⚠️':<16} ║
╠══════════════════════════════════════════════════════════════╣
║ Average Rating: {'⭐' * int(avg_rating):<5} ({avg_rating:.1f}/5.0){' ' * 27}║
╚══════════════════════════════════════════════════════════════╝"""
    
    print(report)
    
    # Action items
    print("\n📋 ACTION ITEMS:")
    if signup_progress < 100 and days_to_launch > 30:
        needed = targets['signups'] - total
        print(f"  • Need {needed} more signups")
    if download_rate < 60:
        not_downloaded = [r for r in readers if not r['downloaded']]
        print(f"  • {len(not_downloaded)} readers haven't downloaded - send reminder")
    if days_to_launch < 7 and reviewed < 10:
        print(f"  • Launch in {days_to_launch} days with only {reviewed} reviews - urgent action needed!")
    
    # Source breakdown
    sources = {}
    for r in readers:
        src = r.get('source', 'unknown')
        if src not in sources:
            sources[src] = {'total': 0, 'reviewed': 0}
        sources[src]['total'] += 1
        if r['review_posted']:
            sources[src]['reviewed'] += 1
    
    print("\n📊 BY SOURCE:")
    for src, data in sorted(sources.items(), key=lambda x: x[1]['total'], reverse=True):
        rate = (data['reviewed'] / data['total'] * 100) if data['total'] > 0 else 0
        print(f"  • {src}: {data['total']} signups, {data['reviewed']} reviews ({rate:.0f}%)")

def main():
    parser = argparse.ArgumentParser(description='ARC Campaign Tracker')
    subparsers = parser.add_subparsers(dest='command')
    
    # Create command
    create_parser = subparsers.add_parser('create')
    create_parser.add_argument('--book', required=True)
    create_parser.add_argument('--launch', required=True, help='YYYY-MM-DD')
    
    # Add command
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--file', required=True)
    add_parser.add_argument('--name', required=True)
    add_parser.add_argument('--email', required=True)
    add_parser.add_argument('--source', default='email')
    
    # Update command
    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('--file', required=True)
    update_parser.add_argument('--email', required=True)
    update_parser.add_argument('--status', required=True,
                              choices=['downloaded', 'read', 'reviewed', 'notes'])
    update_parser.add_argument('--value', default=None)
    
    # Report command
    report_parser = subparsers.add_parser('report')
    report_parser.add_argument('--file', required=True)
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_campaign(args.book, args.launch)
    elif args.command == 'add':
        add_reader(args.file, args.name, args.email, args.source)
    elif args.command == 'update':
        update_reader(args.file, args.email, args.status, args.value)
    elif args.command == 'report':
        generate_report(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
