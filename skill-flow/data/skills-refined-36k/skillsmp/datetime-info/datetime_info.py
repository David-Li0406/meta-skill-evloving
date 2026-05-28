#!/usr/bin/env python3
"""Datetime Info - Muestra fecha y hora actual en varios formatos"""

import json
from datetime import datetime
import calendar

def main():
    now = datetime.now()
    
    info = {
        "iso": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_name": calendar.day_name[now.weekday()],
        "month_name": calendar.month_name[now.month],
        "week_number": now.isocalendar()[1],
        "timestamp": int(now.timestamp())
    }
    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()
