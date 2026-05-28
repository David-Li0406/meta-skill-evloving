"""
Windows-specific networking (including WSL2)
"""
import logging
import subprocess
import re
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def get_wsl2_windows_host_ip() -> Optional[str]:
    """Get the Windows host IP from WSL2"""
    try:
        # Method 1: Read from /etc/resolv.conf (nameserver is the Windows host)
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    ip = line.split()[1]
                    logger.debug(f"WSL2 host IP from resolv.conf: {ip}")
                    return ip
    except Exception as e:
        logger.debug(f"Failed to get host IP from resolv.conf: {e}")

    # Method 2: Use ip route
    try:
        result = subprocess.run(
            ['ip', 'route', 'show', 'default'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            match = re.search(r'default via ([\d.]+)', result.stdout)
            if match:
                ip = match.group(1)
                logger.debug(f"WSL2 host IP from ip route: {ip}")
                return ip
    except Exception as e:
        logger.debug(f"Failed to get host IP from ip route: {e}")

    return None


def get_wsl2_lan_ip() -> Optional[str]:
    """
    Get LAN IP for WSL2

    WSL2 uses NAT, so we need to get the Windows host's LAN IP
    """
    # Query Windows for its LAN IP using PowerShell
    try:
        # Run PowerShell command on Windows host
        # Exclude: loopback (127.*), link-local (169.254.*), WSL2 vEthernet (172.*)
        # Prefer common home network ranges (192.168.*, 10.*)
        ps_command = (
            "Get-NetIPAddress -AddressFamily IPv4 "
            "| Where-Object { "
            "$_.InterfaceAlias -notlike '*WSL*' -and "
            "$_.InterfaceAlias -notlike '*vEthernet*' -and "
            "$_.IPAddress -notlike '127.*' -and "
            "$_.IPAddress -notlike '169.254.*' -and "
            "$_.IPAddress -notlike '172.*' "
            "} "
            "| Sort-Object { "
            "if ($_.IPAddress -like '192.168.*') { 1 } "
            "elseif ($_.IPAddress -like '10.*') { 2 } "
            "else { 3 } "
            "} "
            "| Select-Object -First 1 -ExpandProperty IPAddress"
        )

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and result.stdout.strip():
            ip = result.stdout.strip()
            logger.debug(f"Windows host LAN IP: {ip}")
            return ip

    except Exception as e:
        logger.error(f"Failed to get Windows LAN IP: {e}")

    # Fallback: Return None to indicate we couldn't get it
    return None


def get_wsl2_all_ips() -> List[Dict[str, str]]:
    """Get all IPs in WSL2"""
    from .linux import get_linux_all_ips
    return get_linux_all_ips()


def ensure_wsl2_port_accessible(port: int, protocol: str = 'tcp', name: str = 'app') -> Tuple[bool, str]:
    """
    Make a port accessible on LAN from WSL2

    This requires:
    1. Port forwarding from Windows to WSL2
    2. Windows Firewall rule to allow inbound connections

    Args:
        port: Port number
        protocol: 'tcp' or 'udp'
        name: Name for the firewall rule

    Returns:
        (success, message)
    """
    # Get WSL2 IP
    try:
        result = subprocess.run(
            ['hostname', '-I'],
            capture_output=True,
            text=True,
            timeout=5
        )
        wsl_ip = result.stdout.strip().split()[0]
    except Exception as e:
        return False, f"Failed to get WSL2 IP: {e}"

    # Get Windows LAN IP for display
    lan_ip = get_wsl2_lan_ip()
    if not lan_ip:
        lan_ip = "Windows-Host"  # Fallback if we can't get it

    messages = []

    # Step 1: Add Windows port forwarding
    try:
        # Delete existing rule if it exists (ignore errors)
        subprocess.run(
            ['powershell.exe', '-Command',
             f'netsh interface portproxy delete v4tov4 listenport={port} listenaddress=0.0.0.0'],
            capture_output=True,
            timeout=10
        )

        # Add new port forwarding rule
        ps_command = (
            f'netsh interface portproxy add v4tov4 '
            f'listenport={port} listenaddress=0.0.0.0 '
            f'connectport={port} connectaddress={wsl_ip}'
        )

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            messages.append(f"✓ Port forwarding: {lan_ip}:{port} → WSL2:{wsl_ip}:{port}")
        else:
            return False, f"Failed to add port forwarding: {result.stderr}"

    except Exception as e:
        return False, f"Failed to configure port forwarding: {e}"

    # Step 2: Add Windows Firewall rule
    try:
        firewall_name = f"WSL2_{name}_{port}"

        # Delete existing rule if it exists
        subprocess.run(
            ['powershell.exe', '-Command',
             f'Remove-NetFirewallRule -DisplayName "{firewall_name}" -ErrorAction SilentlyContinue'],
            capture_output=True,
            timeout=10
        )

        # Add new firewall rule
        ps_command = (
            f'New-NetFirewallRule -DisplayName "{firewall_name}" '
            f'-Direction Inbound -LocalPort {port} -Protocol {protocol.upper()} -Action Allow'
        )

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            messages.append(f"✓ Firewall rule added: {firewall_name}")
        else:
            messages.append(f"⚠ Firewall rule failed (may need admin): {result.stderr}")

    except Exception as e:
        messages.append(f"⚠ Firewall rule failed: {e}")

    return True, "\n".join(messages)


def get_windows_lan_ip() -> Optional[str]:
    """Get LAN IP on Windows (non-WSL)"""
    try:
        # Exclude: loopback (127.*), link-local (169.254.*), WSL2 vEthernet (172.*)
        # Prefer common home network ranges (192.168.*, 10.*)
        ps_command = (
            "Get-NetIPAddress -AddressFamily IPv4 "
            "| Where-Object { "
            "$_.InterfaceAlias -notlike '*WSL*' -and "
            "$_.InterfaceAlias -notlike '*vEthernet*' -and "
            "$_.IPAddress -notlike '127.*' -and "
            "$_.IPAddress -notlike '169.254.*' -and "
            "$_.IPAddress -notlike '172.*' "
            "} "
            "| Sort-Object { "
            "if ($_.IPAddress -like '192.168.*') { 1 } "
            "elseif ($_.IPAddress -like '10.*') { 2 } "
            "else { 3 } "
            "} "
            "| Select-Object -First 1 -ExpandProperty IPAddress"
        )

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

    except Exception as e:
        logger.error(f"Failed to get Windows LAN IP: {e}")

    return None


def get_windows_all_ips() -> List[Dict[str, str]]:
    """Get all IPs on Windows"""
    try:
        ps_command = (
            "Get-NetIPAddress -AddressFamily IPv4 "
            "| Where-Object { $_.IPAddress -notlike '169.254.*' } "
            "| Select-Object InterfaceAlias, IPAddress "
            "| ConvertTo-Json"
        )

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0 and result.stdout.strip():
            import json
            data = json.loads(result.stdout)
            if isinstance(data, dict):
                data = [data]

            return [
                {'interface': item['InterfaceAlias'], 'ip': item['IPAddress']}
                for item in data
            ]

    except Exception as e:
        logger.error(f"Failed to get Windows IPs: {e}")

    return []


def list_wsl2_port_forwards() -> List[Dict[str, str]]:
    """
    List all WSL2 port forwarding rules

    Returns:
        List of dicts with keys: listen_address, listen_port, connect_address, connect_port
    """
    try:
        ps_command = "netsh interface portproxy show v4tov4"

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return []

        # Parse the output
        forwards = []
        lines = result.stdout.strip().split('\n')

        # Skip header lines
        data_started = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if '---' in line:
                data_started = True
                continue
            if not data_started:
                continue

            # Parse data line: "0.0.0.0         3001          172.21.207.214  3001"
            parts = line.split()
            if len(parts) >= 4:
                forwards.append({
                    'listen_address': parts[0],
                    'listen_port': parts[1],
                    'connect_address': parts[2],
                    'connect_port': parts[3]
                })

        return forwards

    except Exception as e:
        logger.error(f"Failed to list port forwards: {e}")
        return []


def remove_wsl2_port_forward(port: int) -> Tuple[bool, str]:
    """
    Remove a WSL2 port forwarding rule

    Args:
        port: Port number to remove

    Returns:
        (success, message)
    """
    try:
        ps_command = f'netsh interface portproxy delete v4tov4 listenport={port} listenaddress=0.0.0.0'

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return True, f"✓ Removed port forwarding for port {port}"
        else:
            return False, f"Failed to remove port forwarding: {result.stderr}"

    except Exception as e:
        return False, f"Failed to remove port forwarding: {e}"


def get_wsl2_network_info() -> Dict[str, any]:
    """
    Get detailed WSL2 network information

    Returns:
        Dict with WSL2 IP, Windows host IP, Windows LAN IP, port forwards
    """
    info = {
        'wsl2_ip': None,
        'windows_host_ip': None,  # The WSL2 gateway (172.x)
        'windows_lan_ip': None,   # The actual LAN IP (192.168.x)
        'port_forwards': []
    }

    # Get WSL2 IP
    try:
        result = subprocess.run(
            ['hostname', '-I'],
            capture_output=True,
            text=True,
            timeout=5
        )
        info['wsl2_ip'] = result.stdout.strip().split()[0]
    except Exception:
        pass

    # Get Windows host IP (gateway)
    info['windows_host_ip'] = get_wsl2_windows_host_ip()

    # Get Windows LAN IP
    info['windows_lan_ip'] = get_wsl2_lan_ip()

    # Get port forwards
    info['port_forwards'] = list_wsl2_port_forwards()

    return info


def ensure_windows_port_accessible(port: int, protocol: str = 'tcp', name: str = 'app') -> Tuple[bool, str]:
    """Add Windows Firewall rule (non-WSL)"""
    try:
        firewall_name = f"{name}_{port}"

        # Delete existing rule
        subprocess.run(
            ['powershell.exe', '-Command',
             f'Remove-NetFirewallRule -DisplayName "{firewall_name}" -ErrorAction SilentlyContinue'],
            capture_output=True,
            timeout=10
        )

        # Add new rule
        ps_command = (
            f'New-NetFirewallRule -DisplayName "{firewall_name}" '
            f'-Direction Inbound -LocalPort {port} -Protocol {protocol.upper()} -Action Allow'
        )

        result = subprocess.run(
            ['powershell.exe', '-Command', ps_command],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return True, f"✓ Firewall rule added: {firewall_name}"
        else:
            return False, f"Failed to add firewall rule: {result.stderr}"

    except Exception as e:
        return False, f"Failed to configure firewall: {e}"
