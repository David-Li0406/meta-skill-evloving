#!/usr/bin/env python3
"""
Process Monitor - Muestra información de procesos del sistema
"""

import json
import subprocess
import argparse


def get_top_processes(limit=10, sort_by="cpu"):
    """Obtiene los procesos ordenados por CPU o memoria"""
    
    # Usar ps para obtener procesos
    if sort_by == "mem":
        cmd = ["ps", "aux", "--sort=-%mem"]
    else:
        cmd = ["ps", "aux", "--sort=-%cpu"]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    
    processes = []
    # Saltar header
    for line in lines[1:limit+1]:
        parts = line.split(None, 10)
        if len(parts) >= 11:
            processes.append({
                "user": parts[0],
                "pid": int(parts[1]),
                "cpu": float(parts[2]),
                "mem": float(parts[3]),
                "command": parts[10][:50]  # Truncar comando
            })
    
    return processes


def get_system_stats():
    """Obtiene estadísticas generales del sistema"""
    stats = {}
    
    # CPU info
    try:
        with open('/proc/loadavg', 'r') as f:
            load = f.read().strip().split()
            stats["load_avg"] = {
                "1min": float(load[0]),
                "5min": float(load[1]),
                "15min": float(load[2])
            }
    except:
        stats["load_avg"] = None
    
    # Memory info
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    meminfo[key] = int(value)
            
            total = meminfo.get('MemTotal', 0)
            available = meminfo.get('MemAvailable', 0)
            used = total - available
            
            stats["memory"] = {
                "total_gb": round(total / 1024 / 1024, 2),
                "used_gb": round(used / 1024 / 1024, 2),
                "available_gb": round(available / 1024 / 1024, 2),
                "percent_used": round(used / total * 100, 1) if total > 0 else 0
            }
    except:
        stats["memory"] = None
    
    # Uptime
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.read().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            stats["uptime"] = f"{days}d {hours}h {minutes}m"
    except:
        stats["uptime"] = None
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Monitor de procesos del sistema")
    parser.add_argument("--top", "-t", type=int, default=10, 
                        help="Número de procesos a mostrar (default: 10)")
    parser.add_argument("--sort", "-s", choices=["cpu", "mem"], default="cpu",
                        help="Ordenar por cpu o mem (default: cpu)")
    parser.add_argument("--stats-only", action="store_true",
                        help="Mostrar solo estadísticas del sistema")
    args = parser.parse_args()
    
    result = {
        "system": get_system_stats()
    }
    
    if not args.stats_only:
        result["top_processes"] = get_top_processes(args.top, args.sort)
        result["sorted_by"] = args.sort
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
