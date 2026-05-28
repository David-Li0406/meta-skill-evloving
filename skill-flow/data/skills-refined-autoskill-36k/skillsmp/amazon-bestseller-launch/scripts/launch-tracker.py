#!/usr/bin/env python3
"""
Amazon Book Launch Tracker
Track BSR, reviews, and sales metrics throughout launch day.

Usage:
    python launch-tracker.py --asin B0XXXXXXXX --title "Your Book Title"
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

def create_launch_tracker(asin: str, title: str, launch_date: str = None):
    """Create a new launch tracking file."""
    
    if launch_date is None:
        launch_date = datetime.now().strftime("%Y-%m-%d")
    
    tracker = {
        "book": {
            "asin": asin,
            "title": title,
            "launch_date": launch_date
        },
        "targets": {
            "day1_sales": 50,
            "day1_reviews": 10,
            "target_bsr": 5000,
            "target_category_rank": 1
        },
        "hourly_metrics": [],
        "daily_summary": []
    }
    
    # Create tracking file
    filename = f"launch_tracker_{asin}_{launch_date}.json"
    with open(filename, 'w') as f:
        json.dump(tracker, f, indent=2)
    
    print(f"✅ Created launch tracker: {filename}")
    return filename

def log_metrics(filename: str, bsr: int, category_rank: int, reviews: int, 
                review_avg: float, notes: str = ""):
    """Log hourly metrics to tracker."""
    
    with open(filename, 'r') as f:
        tracker = json.load(f)
    
    metric = {
        "timestamp": datetime.now().isoformat(),
        "bsr": bsr,
        "category_rank": category_rank,
        "reviews": reviews,
        "review_avg": review_avg,
        "notes": notes
    }
    
    tracker["hourly_metrics"].append(metric)
    
    with open(filename, 'w') as f:
        json.dump(tracker, f, indent=2)
    
    # Status check
    targets = tracker["targets"]
    status = "🟢" if bsr <= targets["target_bsr"] else "🟡" if bsr <= targets["target_bsr"] * 2 else "🔴"
    
    print(f"""
{status} Metrics Logged @ {datetime.now().strftime('%H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BSR: {bsr:,} (target: {targets['target_bsr']:,})
Category Rank: #{category_rank} (target: #{targets['target_category_rank']})
Reviews: {reviews} (target: {targets['day1_reviews']})
Average Rating: {review_avg}⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def generate_report(filename: str):
    """Generate launch day summary report."""
    
    with open(filename, 'r') as f:
        tracker = json.load(f)
    
    metrics = tracker["hourly_metrics"]
    if not metrics:
        print("No metrics logged yet.")
        return
    
    book = tracker["book"]
    targets = tracker["targets"]
    
    # Calculate stats
    best_bsr = min(m["bsr"] for m in metrics)
    best_rank = min(m["category_rank"] for m in metrics)
    final_reviews = metrics[-1]["reviews"]
    first_bsr = metrics[0]["bsr"]
    
    bsr_improvement = ((first_bsr - best_bsr) / first_bsr * 100) if first_bsr > 0 else 0
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║                   LAUNCH DAY REPORT                          ║
╠══════════════════════════════════════════════════════════════╣
║ Book: {book['title'][:50]:<50} ║
║ ASIN: {book['asin']:<54} ║
║ Launch Date: {book['launch_date']:<47} ║
╠══════════════════════════════════════════════════════════════╣
║                      PERFORMANCE                             ║
╠══════════════════════════════════════════════════════════════╣
║ Best BSR: {best_bsr:>10,} (Target: {targets['target_bsr']:>10,}) {'✅' if best_bsr <= targets['target_bsr'] else '❌':<8} ║
║ Best Category Rank: #{best_rank:<5} (Target: #{targets['target_category_rank']:<5}) {'✅' if best_rank <= targets['target_category_rank'] else '❌':<8} ║
║ Reviews: {final_reviews:>10} (Target: {targets['day1_reviews']:>10}) {'✅' if final_reviews >= targets['day1_reviews'] else '❌':<8} ║
║ BSR Improvement: {bsr_improvement:>38.1f}% ║
╠══════════════════════════════════════════════════════════════╣
║                    HOURLY PROGRESSION                        ║
╠══════════════════════════════════════════════════════════════╣"""
    
    for m in metrics:
        timestamp = datetime.fromisoformat(m["timestamp"]).strftime("%H:%M")
        report += f"\n║ {timestamp}: BSR {m['bsr']:>8,} | Rank #{m['category_rank']:<3} | {m['reviews']} reviews{' '*15}║"
    
    report += """
╚══════════════════════════════════════════════════════════════╝"""
    
    print(report)
    
    # Save report
    report_file = filename.replace('.json', '_report.txt')
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\n📄 Report saved: {report_file}")

def main():
    parser = argparse.ArgumentParser(description='Amazon Book Launch Tracker')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new tracker')
    create_parser.add_argument('--asin', required=True, help='Amazon ASIN')
    create_parser.add_argument('--title', required=True, help='Book title')
    create_parser.add_argument('--date', help='Launch date (YYYY-MM-DD)')
    
    # Log command
    log_parser = subparsers.add_parser('log', help='Log metrics')
    log_parser.add_argument('--file', required=True, help='Tracker file')
    log_parser.add_argument('--bsr', type=int, required=True, help='Best Seller Rank')
    log_parser.add_argument('--rank', type=int, required=True, help='Category rank')
    log_parser.add_argument('--reviews', type=int, required=True, help='Review count')
    log_parser.add_argument('--rating', type=float, default=0.0, help='Average rating')
    log_parser.add_argument('--notes', default='', help='Notes')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate report')
    report_parser.add_argument('--file', required=True, help='Tracker file')
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_launch_tracker(args.asin, args.title, args.date)
    elif args.command == 'log':
        log_metrics(args.file, args.bsr, args.rank, args.reviews, 
                   args.rating, args.notes)
    elif args.command == 'report':
        generate_report(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
