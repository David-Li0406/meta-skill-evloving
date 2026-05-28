#!/usr/bin/env python3
"""
Business Day Calculator and Task Timeline Generator
Matches Brendon's Power Automate flow exactly - calculates business days (excluding weekends)
"""

from datetime import datetime, timedelta
import csv
import json
from typing import List, Dict, Tuple

# Exact task template from Power Automate flow
ENGAGEMENT_TASKS = [
    {"title": "Schedule Internal Precall", "offset": 28},
    {"title": "Research customer", "offset": 22},
    {"title": "Execute Internal Precall", "offset": 21},
    {"title": "Draft Agenda", "offset": 20},
    {"title": "Schedule Customer Precall", "offset": 20},
    {"title": "Execute Customer Precall", "offset": 14},
    {"title": "Schedule internal resources", "offset": 14},
    {"title": "Validate Agenda with ATU", "offset": 10},
    {"title": "Validate Agenda with Customer", "offset": 7},
    {"title": "Prep Demos", "offset": 7},
    {"title": "Confirm all Customer pre-work is completed", "offset": 3},
    {"title": "Send Satisfaction Survey to customer", "offset": 0},
    {"title": "Conduct MSFT Debrief", "offset": -2},
    {"title": "Share Engagement Materials with Customer", "offset": -2},
    {"title": "Complete Engagement Close out form", "offset": -3}
]


def calculate_business_days(target_date: datetime, days_offset: int) -> datetime:
    """
    Calculate business day offset from target date (excludes weekends).
    Positive offset = days before engagement (T-minus)
    Negative offset = days after engagement (T-plus)
    
    Args:
        target_date: The engagement date
        days_offset: Number of business days before (positive) or after (negative)
    
    Returns:
        Calculated date
    """
    # Direction: positive offset means go backwards (T-28 is 28 business days BEFORE)
    direction = -1 if days_offset > 0 else 1
    days_to_move = abs(days_offset)
    
    result = target_date
    days_moved = 0
    
    while days_moved < days_to_move:
        result += timedelta(days=direction)
        
        # Only count weekdays (Monday=0, Sunday=6)
        if result.weekday() < 5:  # Monday to Friday
            days_moved += 1
    
    return result


def generate_task_timeline(
    customer_name: str,
    engagement_date: str,  # YYYY-MM-DD format
    assignee: str = "Brendon Colburn"
) -> List[Dict]:
    """
    Generate complete task timeline with business day calculations.
    Returns list of tasks ready for Planner CSV import.
    """
    
    # Parse engagement date
    eng_date = datetime.strptime(engagement_date, "%Y-%m-%d")
    
    # Bucket name matches Power Automate format
    bucket_name = f"{engagement_date} - {customer_name}"
    
    tasks = []
    
    for task_template in ENGAGEMENT_TASKS:
        # Calculate due date using business days
        due_date = calculate_business_days(eng_date, task_template["offset"])
        
        # Task title includes customer name
        task_title = f"{customer_name} - {task_template['title']}"
        
        # Format for Planner CSV import
        task = {
            "Task Name": task_title,
            "Assignment": assignee,
            "Start date": due_date.strftime("%m/%d/%Y"),
            "Due date": due_date.strftime("%m/%d/%Y"),
            "Bucket": bucket_name,
            "Progress": "Not started",
            "Priority": "Medium",
            "Labels": "Add label"
        }
        
        tasks.append(task)
    
    return tasks


def save_tasks_csv(tasks: List[Dict], output_path: str) -> str:
    """Save tasks to CSV format for Microsoft Planner import"""
    if not tasks:
        return None
    
    fieldnames = [
        "Task Name",
        "Assignment",
        "Start date",
        "Due date",
        "Bucket",
        "Progress",
        "Priority",
        "Labels"
    ]
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)
    
    return output_path


def format_task_summary(tasks: List[Dict]) -> str:
    """Format tasks for display in preview"""
    summary = []
    
    summary.append("PRE-ENGAGEMENT TASKS:")
    for task in tasks[:11]:  # First 11 are pre-engagement
        summary.append(f"  {task['Due date']} - {task['Task Name']}")
    
    summary.append("\nPOST-ENGAGEMENT TASKS:")
    for task in tasks[11:]:  # Remaining are post-engagement
        summary.append(f"  {task['Due date']} - {task['Task Name']}")
    
    return "\n".join(summary)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python business_days.py <customer_name> <engagement_date (YYYY-MM-DD)>")
        sys.exit(1)
    
    customer = sys.argv[1]
    date = sys.argv[2]
    
    tasks = generate_task_timeline(customer, date)
    
    print(f"\n{'='*60}")
    print(f"ENGAGEMENT: {customer}")
    print(f"DATE: {date}")
    print(f"{'='*60}\n")
    
    print(format_task_summary(tasks))
    
    # Save CSV
    output_file = f"{customer.replace(' ', '-')}_{date}_tasks.csv"
    save_tasks_csv(tasks, output_file)
    print(f"\n✅ Tasks saved to: {output_file}")
