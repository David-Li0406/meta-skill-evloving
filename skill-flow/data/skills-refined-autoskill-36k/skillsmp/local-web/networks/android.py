"""
Android/Termux-specific networking
"""
import logging
import subprocess
import socket
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def get_android_lan_ip() -> Optional[str]:
    """Get LAN IP on Android/Termux"""
    # Method 1: Use socket method (same as Linux)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            logger.debug(f"Android LAN IP from socket: {ip}")
            return ip
    except Exception as e:
        logger.debug(f"Socket method failed: {e}")

    # Method 2: Use ip addr (if available in Termux)
    try:
        result = subprocess.run(
            ['ip', 'addr', 'show'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            import re
            for line in result.stdout.split('\n'):
                match = re.search(r'inet ([\d.]+)/\d+', line)
                if match:
                    ip = match.group(1)
                    if not ip.startswith('127.') and not ip.startswith('169.254.'):
                        logger.debug(f"Android LAN IP from ip addr: {ip}")
                        return ip

    except Exception as e:
        logger.debug(f"ip addr method failed: {e}")

    # Method 3: Use ifconfig (older method, might work on some devices)
    try:
        result = subprocess.run(
            ['ifconfig'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            import re
            # Look for inet addr:X.X.X.X
            for line in result.stdout.split('\n'):
                match = re.search(r'inet (?:addr:)?([\d.]+)', line)
                if match:
                    ip = match.group(1)
                    if not ip.startswith('127.') and not ip.startswith('169.254.'):
                        logger.debug(f"Android LAN IP from ifconfig: {ip}")
                        return ip

    except Exception as e:
        logger.debug(f"ifconfig method failed: {e}")

    return None


def get_android_all_ips() -> List[Dict[str, str]]:
    """Get all network interfaces on Android/Termux"""
    ips = []

    # Try ip addr first
    try:
        result = subprocess.run(
            ['ip', '-o', '-4', 'addr', 'show'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            import re
            for line in result.stdout.strip().split('\n'):
                match = re.search(r'^\d+:\s+(\S+)\s+inet\s+([\d.]+)/\d+', line)
                if match:
                    interface = match.group(1)
                    ip = match.group(2)
                    ips.append({'interface': interface, 'ip': ip})

            if ips:
                return ips

    except Exception as e:
        logger.debug(f"ip addr failed: {e}")

    # Fallback to ifconfig
    try:
        result = subprocess.run(
            ['ifconfig'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            import re
            current_interface = None

            for line in result.stdout.split('\n'):
                # Interface line (starts without whitespace)
                if line and not line[0].isspace():
                    match = re.match(r'^(\S+)', line)
                    if match:
                        current_interface = match.group(1).rstrip(':')

                # IP line (has whitespace at start)
                elif current_interface:
                    match = re.search(r'inet (?:addr:)?([\d.]+)', line)
                    if match:
                        ip = match.group(1)
                        ips.append({'interface': current_interface, 'ip': ip})
                        current_interface = None

    except Exception as e:
        logger.debug(f"ifconfig failed: {e}")

    return ips
