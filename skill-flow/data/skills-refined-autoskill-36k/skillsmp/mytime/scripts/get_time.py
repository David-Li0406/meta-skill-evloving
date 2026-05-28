#!/usr/bin/env python3
import json
import platform
from datetime import datetime
import sys

try:
    import pytz
except ImportError:
    pytz = None

def get_system_language():
    """Get system language setting."""
    try:
        import locale
        lang = locale.getlocale()[0]
        return lang if lang else "unknown"
    except:
        return "unknown"

def get_timezone_info():
    """Get timezone information."""
    try:
        if pytz:
            import tzlocal
            local_tz = tzlocal.get_localzone()
            return str(local_tz)
        else:
            import time
            return time.tzname[0] or "UTC"
    except:
        return "UTC"

def get_utc_offset():
    """Get UTC offset in +HH:MM format."""
    try:
        import time
        # Use time.timezone to get offset (note: negative because time.timezone is opposite sign)
        offset_seconds = -time.timezone if time.daylight == 0 else -time.altzone
        hours = offset_seconds // 3600
        minutes = (abs(offset_seconds) % 3600) // 60
        sign = '+' if hours >= 0 else '-'
        return f"{sign}{abs(hours):02d}:{minutes:02d}"
    except:
        return "+00:00"

def get_os_info():
    """Get operating system name and architecture."""
    system = platform.system()
    machine = platform.machine()
    
    # Normalize OS names
    os_names = {
        'Windows': 'Windows',
        'Darwin': 'macOS',
        'Linux': 'Linux'
    }
    os_name = os_names.get(system, system)
    
    return {
        'name': os_name,
        'architecture': machine
    }

def main():
    """Main function to get time information."""
    # Get current times
    now_local = datetime.now()
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        now_utc = datetime.utcnow()
    
    # Get timezone info
    timezone = get_timezone_info()
    utc_offset = get_utc_offset()
    
    # Format times
    local_time = now_local.strftime('%Y-%m-%d %H:%M:%S')
    utc_time = now_utc.strftime('%Y-%m-%d %H:%M:%S')
    
    # Get system info
    system_language = get_system_language()
    os_info = get_os_info()
    
    # Build output
    result = {
        'timezone': timezone,
        'utc_offset': utc_offset,
        'local_time': local_time,
        'utc_time': utc_time,
        'system_language': system_language,
        'os_name': os_info['name'],
        'os_architecture': os_info['architecture']
    }
    
    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
