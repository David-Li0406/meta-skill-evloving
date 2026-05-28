"""
Core networking API - Routes to platform-specific implementations
"""
import logging
import socket
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import sys

# Add cross_platform to path if needed
try:
    from cross_platform import SystemUtils
except ImportError:
    # Add parent modules directory to path
    modules_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(modules_dir))
    from cross_platform import SystemUtils

logger = logging.getLogger(__name__)

# Create SystemUtils instance
sys_utils = SystemUtils()


def get_lan_ip() -> Optional[str]:
    """
    Get the primary LAN-accessible IP address

    Returns:
        IP address string (e.g., "192.168.1.100") or None if not found

    Examples:
        >>> ip = get_lan_ip()
        >>> print(f"Access this server at: http://{ip}:3000")
    """
    if sys_utils.is_wsl2():
        from .windows import get_wsl2_lan_ip
        return get_wsl2_lan_ip()
    elif sys_utils.is_windows():
        from .windows import get_windows_lan_ip
        return get_windows_lan_ip()
    elif sys_utils.is_linux():
        from .linux import get_linux_lan_ip
        return get_linux_lan_ip()
    elif sys_utils.is_android():
        from .android import get_android_lan_ip
        return get_android_lan_ip()
    else:
        logger.warning(f"Unsupported platform: {sys.platform}")
        return None


def get_all_ips() -> List[Dict[str, str]]:
    """
    Get all network interfaces and their IP addresses

    Returns:
        List of dicts with 'interface' and 'ip' keys

    Examples:
        >>> ips = get_all_ips()
        >>> for info in ips:
        ...     print(f"{info['interface']}: {info['ip']}")
    """
    if sys_utils.is_wsl2():
        from .windows import get_wsl2_all_ips
        return get_wsl2_all_ips()
    elif sys_utils.is_windows():
        from .windows import get_windows_all_ips
        return get_windows_all_ips()
    elif sys_utils.is_linux():
        from .linux import get_linux_all_ips
        return get_linux_all_ips()
    elif sys_utils.is_android():
        from .android import get_android_all_ips
        return get_android_all_ips()
    else:
        return []


def get_network_info() -> Dict[str, any]:
    """
    Get comprehensive network information

    Returns:
        Dict with keys:
        - 'lan_ip': Primary LAN IP
        - 'all_ips': List of all interface IPs
        - 'hostname': System hostname
        - 'is_wsl': True if running in WSL2
        - 'wsl_host_ip': Windows host IP (WSL2 only)
    """
    info = {
        'lan_ip': get_lan_ip(),
        'all_ips': get_all_ips(),
        'hostname': socket.gethostname(),
        'is_wsl': sys_utils.is_wsl2(),
        'wsl_host_ip': None,
    }

    if info['is_wsl']:
        info['wsl_host_ip'] = get_wsl2_host_ip()

    return info


def ensure_port_accessible(port: int, protocol: str = 'tcp', name: Optional[str] = None) -> Tuple[bool, str]:
    """
    Ensure a port is accessible on the LAN

    Handles platform-specific requirements:
    - WSL2: Sets up port forwarding from Windows to WSL2
    - Windows: Adds firewall rule
    - Linux: Checks firewall (ufw/firewalld)

    Args:
        port: Port number to make accessible
        protocol: 'tcp' or 'udp' (default: 'tcp')
        name: Optional name for firewall rule

    Returns:
        Tuple of (success: bool, message: str)

    Examples:
        >>> success, msg = ensure_port_accessible(3000, name='koweb')
        >>> if success:
        ...     print(f"Port 3000 is accessible on LAN")
        ... else:
        ...     print(f"Failed: {msg}")
    """
    if not name:
        name = f"port_{port}"

    if sys_utils.is_wsl2():
        from .windows import ensure_wsl2_port_accessible
        return ensure_wsl2_port_accessible(port, protocol, name)
    elif sys_utils.is_windows():
        from .windows import ensure_windows_port_accessible
        return ensure_windows_port_accessible(port, protocol, name)
    elif sys_utils.is_linux():
        from .linux import ensure_linux_port_accessible
        return ensure_linux_port_accessible(port, protocol, name)
    elif sys_utils.is_android():
        # Android/Termux doesn't need firewall rules typically
        return True, "Android: No firewall configuration needed"
    else:
        return False, f"Unsupported platform: {sys.platform}"


def check_port_open(host: str, port: int, timeout: float = 2.0) -> bool:
    """
    Check if a port is open on a host

    Args:
        host: Hostname or IP address
        port: Port number
        timeout: Connection timeout in seconds

    Returns:
        True if port is open, False otherwise
    """
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception as e:
        logger.debug(f"Port check failed: {e}")
        return False


def get_wsl2_host_ip() -> Optional[str]:
    """
    Get the Windows host IP address from WSL2

    Returns:
        Windows host IP or None if not in WSL2
    """
    if not sys_utils.is_wsl2():
        return None

    from .windows import get_wsl2_windows_host_ip
    return get_wsl2_windows_host_ip()


def get_wsl2_network_info() -> Optional[Dict[str, any]]:
    """
    Get detailed WSL2 network information

    Returns:
        Dict with WSL2 IP, Windows IPs, and port forwards, or None if not in WSL2
    """
    if not sys_utils.is_wsl2():
        return None

    from .windows import get_wsl2_network_info as _get_wsl2_network_info
    return _get_wsl2_network_info()


def list_port_forwards() -> List[Dict[str, str]]:
    """
    List all port forwarding rules (WSL2 only)

    Returns:
        List of port forwarding rules
    """
    if not sys_utils.is_wsl2():
        return []

    from .windows import list_wsl2_port_forwards
    return list_wsl2_port_forwards()


def remove_port_forward(port: int) -> Tuple[bool, str]:
    """
    Remove a port forwarding rule (WSL2 only)

    Args:
        port: Port number to remove

    Returns:
        Tuple of (success: bool, message: str)
    """
    if not sys_utils.is_wsl2():
        return False, "Not running in WSL2"

    from .windows import remove_wsl2_port_forward
    return remove_wsl2_port_forward(port)
