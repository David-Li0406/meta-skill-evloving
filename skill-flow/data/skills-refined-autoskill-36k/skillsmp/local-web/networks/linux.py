"""
Linux-specific networking
"""
import logging
import subprocess
import socket
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def get_linux_lan_ip() -> Optional[str]:
    """
    Get LAN IP on Linux

    Tries multiple methods to find the primary LAN IP
    """
    # Method 1: Use socket to connect to external IP (doesn't actually connect)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Use Google DNS as a reference (doesn't actually send data)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith('127.'):
            logger.debug(f"LAN IP from socket method: {ip}")
            return ip
    except Exception as e:
        logger.debug(f"Socket method failed: {e}")

    # Method 2: Parse ip addr output
    try:
        result = subprocess.run(
            ['ip', 'addr', 'show'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            import re
            # Look for inet X.X.X.X lines that aren't 127.0.0.1
            for line in result.stdout.split('\n'):
                match = re.search(r'inet ([\d.]+)/\d+', line)
                if match:
                    ip = match.group(1)
                    if not ip.startswith('127.') and not ip.startswith('169.254.'):
                        logger.debug(f"LAN IP from ip addr: {ip}")
                        return ip

    except Exception as e:
        logger.debug(f"ip addr method failed: {e}")

    # Method 3: Use hostname -I (gets all IPs)
    try:
        result = subprocess.run(
            ['hostname', '-I'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and result.stdout.strip():
            # Get first IP that's not loopback
            ips = result.stdout.strip().split()
            for ip in ips:
                if not ip.startswith('127.') and not ip.startswith('169.254.'):
                    logger.debug(f"LAN IP from hostname -I: {ip}")
                    return ip

    except Exception as e:
        logger.debug(f"hostname -I method failed: {e}")

    return None


def get_linux_all_ips() -> List[Dict[str, str]]:
    """Get all network interfaces and their IPs on Linux"""
    ips = []

    try:
        result = subprocess.run(
            ['ip', '-o', '-4', 'addr', 'show'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            import re
            # Parse output: "2: eth0    inet 192.168.1.100/24 ..."
            for line in result.stdout.strip().split('\n'):
                match = re.search(r'^\d+:\s+(\S+)\s+inet\s+([\d.]+)/\d+', line)
                if match:
                    interface = match.group(1)
                    ip = match.group(2)
                    ips.append({'interface': interface, 'ip': ip})

    except Exception as e:
        logger.error(f"Failed to get Linux IPs: {e}")

    return ips


def ensure_linux_port_accessible(port: int, protocol: str = 'tcp', name: str = 'app') -> Tuple[bool, str]:
    """
    Ensure port is accessible on Linux

    Checks and configures firewall if needed (ufw or firewalld)
    """
    messages = []

    # Check if ufw is installed and active
    try:
        result = subprocess.run(
            ['ufw', 'status'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and 'Status: active' in result.stdout:
            # UFW is active, add rule
            rule_result = subprocess.run(
                ['ufw', 'allow', f'{port}/{protocol}'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if rule_result.returncode == 0:
                messages.append(f"✓ UFW rule added: allow {port}/{protocol}")
            else:
                messages.append(f"⚠ UFW rule failed (may need sudo): {rule_result.stderr}")

            return True, "\n".join(messages) if messages else "UFW checked"

    except FileNotFoundError:
        logger.debug("ufw not found, checking firewalld")
    except Exception as e:
        logger.debug(f"ufw check failed: {e}")

    # Check if firewalld is installed
    try:
        result = subprocess.run(
            ['firewall-cmd', '--state'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 and 'running' in result.stdout.lower():
            # firewalld is active, add rule
            rule_result = subprocess.run(
                ['firewall-cmd', f'--add-port={port}/{protocol}', '--permanent'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if rule_result.returncode == 0:
                # Reload firewall
                subprocess.run(['firewall-cmd', '--reload'], timeout=10)
                messages.append(f"✓ firewalld rule added: {port}/{protocol}")
            else:
                messages.append(f"⚠ firewalld rule failed (may need sudo): {rule_result.stderr}")

            return True, "\n".join(messages) if messages else "firewalld checked"

    except FileNotFoundError:
        logger.debug("firewalld not found")
    except Exception as e:
        logger.debug(f"firewalld check failed: {e}")

    # No active firewall found
    return True, "No active firewall detected (ufw/firewalld)"
