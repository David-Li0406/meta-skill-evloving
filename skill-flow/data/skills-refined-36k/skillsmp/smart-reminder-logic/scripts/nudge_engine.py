import sys
import json
from datetime import datetime, timedelta

def create_nudge_schedule(start_time_str):
    try:
        # Normalize input - ensure HH:MM format
        fmt = "%H:%M"
        # validation of input
        start = datetime.strptime(start_time_str, fmt)
        
        nudge1 = (start + timedelta(minutes=5)).strftime(fmt)
        nudge2 = (start + timedelta(minutes=15)).strftime(fmt)
        critical = (start + timedelta(minutes=30)).strftime(fmt)
        
        # Improvement: Returning Structured JSON for easier integration
        return json.dumps({
            "original_time": start_time_str,
            "schedule": [
                {
                    "type": "soft_nudge",
                    "time": nudge1,
                    "delay_minutes": 5,
                    "message": f"Soft Nudge: Did you take your supplement?",
                    "priority": "low"
                },
                {
                    "type": "medium_nudge",
                    "time": nudge2, 
                    "delay_minutes": 15,
                    "message": f"Reminder: It's been 15 minutes.",
                    "priority": "default"
                },
                {
                    "type": "critical_alert",
                    "time": critical,
                    "delay_minutes": 30,
                    "message": f"CRITICAL: 30 minutes past due! (Sound On)",
                    "priority": "max" 
                }
            ]
        }, indent=2)
        
    except ValueError:
        return json.dumps({
            "error": "Invalid time format. Please use HH:MM (24-hour format).",
            "example": "09:00"
        })

if __name__ == "__main__":
    time_input = sys.argv[1] if len(sys.argv) > 1 else "09:00"
    print(create_nudge_schedule(time_input))
