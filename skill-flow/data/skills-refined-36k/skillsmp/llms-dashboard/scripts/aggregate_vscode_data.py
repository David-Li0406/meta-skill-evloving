import os
import json
import glob
from datetime import datetime, timezone
from pathlib import Path

# Constants
VSCODE_EXT_DIR = Path.home() / ".vscode" / "extensions"
VSCODE_INSIDERS_EXT_DIR = Path.home() / ".vscode-insiders" / "extensions"
VSCODE_LOGS_DIR = Path.home() / "Library" / "Application Support" / "Code" / "logs"
VSCODE_INSIDERS_LOGS_DIR = Path.home() / "Library" / "Application Support" / "Code - Insiders" / "logs"
VSCODE_HISTORY_DIR = Path.home() / "Library" / "Application Support" / "Code" / "User" / "History"
VSCODE_INSIDERS_HISTORY_DIR = Path.home() / "Library" / "Application Support" / "Code - Insiders" / "User" / "History"
VSCODE_STORAGE_FILE = Path.home() / "Library" / "Application Support" / "Code" / "User" / "globalStorage" / "storage.json"

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "vscode_data.json"

def scan_projects(storage_file):
    projects = []
    if not storage_file.exists():
        return projects
        
    try:
        with open(storage_file, 'r') as f:
            data = json.load(f)
            
        workspaces = data.get('profileAssociations', {}).get('workspaces', {})
        for uri, profile in workspaces.items():
            # URI is like file:///Users/you/Documents/Github/my-project
            if uri.startswith('file://'):
                path = uri.replace('file://', '')
                # Decode URL encoding (e.g. %20 -> space)
                from urllib.parse import unquote
                path = unquote(path)
                
                name = os.path.basename(path)
                parent = os.path.dirname(path)
                
                projects.append({
                    "name": name,
                    "path": path,
                    "parent": parent,
                    "profile": profile
                })
    except Exception as e:
        print(f"Error reading storage file: {e}")
        
    return projects

def scan_extensions(directory, type_label):
    extensions = []
    if not directory.exists():
        return extensions
        
    for ext_path in directory.iterdir():
        if not ext_path.is_dir():
            continue
            
        # Try to read package.json
        pkg_file = ext_path / "package.json"
        if pkg_file.exists():
            try:
                with open(pkg_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    extensions.append({
                        "id": f"{data.get('publisher')}.{data.get('name')}",
                        "name": data.get('displayName', data.get('name')),
                        "version": data.get('version'),
                        "description": data.get('description'),
                        "publisher": data.get('publisher'),
                        "installPath": str(ext_path),
                        "source": type_label
                    })
            except Exception as e:
                # print(f"Error reading {pkg_file}: {e}")
                pass
    return extensions

def scan_logs(directory, type_label):
    sessions = []
    if not directory.exists():
        return sessions
        
    # Log folders are named like 20251225T180729
    for log_folder in directory.iterdir():
        if not log_folder.is_dir():
            continue
            
        name = log_folder.name
        # Basic validation of timestamp format
        if len(name) < 15 or 'T' not in name:
            continue
            
        try:
            # Parse start time from folder name
            # Format: YYYYMMDDTHHMMSS
            # Sometimes it has suffixes, so take first 15 chars
            ts_str = name[:15]
            start_time = datetime.strptime(ts_str, "%Y%m%dT%H%M%S")
            
            # Find end time by checking mtime of all files recursively
            max_mtime = 0
            for root, dirs, files in os.walk(log_folder):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        mtime = os.path.getmtime(fp)
                        if mtime > max_mtime:
                            max_mtime = mtime
                    except OSError:
                        pass
            
            if max_mtime > 0:
                end_time = datetime.fromtimestamp(max_mtime)
                duration = (end_time - start_time).total_seconds()
            else:
                duration = 0
                
            # Filter out zero duration or invalid future dates
            if duration < 0: 
                duration = 0
                
            sessions.append({
                "startTime": start_time.isoformat(),
                "durationSeconds": duration,
                "source": type_label,
                "id": name
            })
            
        except Exception as e:
            # print(f"Error parsing log folder {name}: {e}")
            pass
            
    return sessions

def scan_history(directory, type_label):
    """
    Scans VS Code Local History to reconstruct session activity.
    History folders contain file versions. We can use the modification times
    of these files to infer when the user was active.
    """
    activity_timestamps = []
    if not directory.exists():
        return []
        
    # Walk through all history folders
    for root, dirs, files in os.walk(directory):
        for f in files:
            # Filenames in history are often like <hash>.<ext> or entries.json
            # We care about the file modification time
            fp = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(fp)
                activity_timestamps.append(mtime)
            except OSError:
                pass
                
    if not activity_timestamps:
        return []
        
    # Sort timestamps
    activity_timestamps.sort()
    
    # Group timestamps into sessions
    # If gap > 30 minutes (1800s), start new session
    sessions = []
    if not activity_timestamps:
        return sessions
        
    current_session_start = activity_timestamps[0]
    current_session_end = activity_timestamps[0]
    
    GAP_THRESHOLD = 1800 # 30 minutes
    
    for ts in activity_timestamps[1:]:
        if ts - current_session_end > GAP_THRESHOLD:
            # End current session
            duration = current_session_end - current_session_start
            # Filter out tiny sessions (e.g. background saves)
            if duration > 60: 
                sessions.append({
                    "startTime": datetime.fromtimestamp(current_session_start).isoformat(),
                    "durationSeconds": duration,
                    "source": type_label,
                    "id": "history-reconstructed"
                })
            
            # Start new session
            current_session_start = ts
            current_session_end = ts
        else:
            # Extend current session
            current_session_end = ts
            
    # Add last session
    duration = current_session_end - current_session_start
    if duration > 60:
        sessions.append({
            "startTime": datetime.fromtimestamp(current_session_start).isoformat(),
            "durationSeconds": duration,
            "source": type_label,
            "id": "history-reconstructed"
        })
        
    return sessions

def main():
    print("Scanning VS Code data...")
    
    all_extensions = []
    all_extensions.extend(scan_extensions(VSCODE_EXT_DIR, "Stable"))
    all_extensions.extend(scan_extensions(VSCODE_INSIDERS_EXT_DIR, "Insiders"))
    print(f"Found {len(all_extensions)} extensions.")
    
    all_sessions = []
    # Scan Logs (Recent)
    print("Scanning logs...")
    all_sessions.extend(scan_logs(VSCODE_LOGS_DIR, "Stable"))
    all_sessions.extend(scan_logs(VSCODE_INSIDERS_LOGS_DIR, "Insiders"))
    
    # Scan History (Historical)
    print("Scanning local history (this may take a moment)...")
    history_sessions_stable = scan_history(VSCODE_HISTORY_DIR, "Stable")
    history_sessions_insiders = scan_history(VSCODE_INSIDERS_HISTORY_DIR, "Insiders")
    
    print(f"Reconstructed {len(history_sessions_stable)} sessions from Stable history.")
    print(f"Reconstructed {len(history_sessions_insiders)} sessions from Insiders history.")
    
    all_sessions.extend(history_sessions_stable)
    all_sessions.extend(history_sessions_insiders)
    
    print(f"Total sessions found: {len(all_sessions)}")
    
    # Sort sessions by time
    all_sessions.sort(key=lambda x: x['startTime'], reverse=True)
    
    # Scan Projects
    print("Scanning projects...")
    projects = scan_projects(VSCODE_STORAGE_FILE)
    print(f"Found {len(projects)} projects.")
    
    data = {
        "extensions": all_extensions,
        "sessions": all_sessions,
        "projects": projects,
        "generatedAt": datetime.now().isoformat()
    }
    
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        
    print(f"Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
