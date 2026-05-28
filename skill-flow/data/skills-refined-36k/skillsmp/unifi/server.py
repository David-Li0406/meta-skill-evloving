#!/usr/bin/env python3
"""
Unifi Network MCP Server

Provides Claude Code with tools to monitor and manage Ubiquiti Unifi networks.
"""

import os
import sys
from typing import Any, Optional
from datetime import datetime
from pathlib import Path

# Load environment variables from .env.local
try:
    from dotenv import load_dotenv
    # Load from the same directory as this script
    env_path = Path(__file__).parent / ".env.local"
    load_dotenv(env_path)
except ImportError:
    pass  # dotenv is optional, env vars might be set directly

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: mcp package not found. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

try:
    from unifi_os_controller import UniFiOSController
except ImportError:
    print("Error: unifi_os_controller module not found", file=sys.stderr)
    sys.exit(1)


# Initialize FastMCP server
mcp = FastMCP("unifi")

# Global controller instance (initialized on first use)
_controller: Optional[UniFiOSController] = None


def get_controller() -> UniFiOSController:
    """Get or create the Unifi controller connection."""
    global _controller

    if _controller is not None:
        return _controller

    # Get credentials from environment
    host = os.getenv("UNIFI_HOST")
    username = os.getenv("UNIFI_USERNAME")
    password = os.getenv("UNIFI_PASSWORD")
    port = int(os.getenv("UNIFI_PORT", "443"))
    site = os.getenv("UNIFI_SITE", "default")

    if not all([host, username, password]):
        raise ValueError(
            "Missing required environment variables: UNIFI_HOST, UNIFI_USERNAME, UNIFI_PASSWORD"
        )

    _controller = UniFiOSController(
        host=host,
        username=username,
        password=password,
        port=port,
        site_id=site,
        ssl_verify=False  # Most self-hosted controllers use self-signed certs
    )

    return _controller


@mcp.tool()
def list_devices(device_type: Optional[str] = None) -> dict[str, Any]:
    """
    List all network devices (access points, switches, gateways).

    Args:
        device_type: Filter by device type (uap=access points, usw=switches, ugw=gateways).
                     Leave empty to show all devices.

    Returns:
        Dictionary containing list of devices with their details (name, model, IP, status, uptime).
    """
    ctrl = get_controller()
    devices = ctrl.get_aps()  # Despite the name, this returns all device types

    # Filter by type if specified
    if device_type:
        devices = [d for d in devices if d.get("type") == device_type]

    # Format the response
    formatted_devices = []
    for device in devices:
        formatted_devices.append({
            "name": device.get("name", "Unnamed"),
            "mac": device.get("mac"),
            "model": device.get("model"),
            "type": device.get("type"),
            "ip": device.get("ip"),
            "state": device.get("state"),
            "adopted": device.get("adopted"),
            "uptime": device.get("uptime", 0),
            "uptime_days": round(device.get("uptime", 0) / 86400, 1),
            "version": device.get("version"),
        })

    return {
        "count": len(formatted_devices),
        "devices": formatted_devices
    }


@mcp.tool()
def list_clients(connection_type: Optional[str] = None) -> dict[str, Any]:
    """
    List all connected clients on the network.

    Args:
        connection_type: Filter by connection type ('wireless' or 'wired').
                        Leave empty to show all clients.

    Returns:
        Dictionary containing list of clients with their connection details.
    """
    ctrl = get_controller()
    clients = ctrl.get_clients()

    # Filter by connection type if specified
    if connection_type == "wireless":
        clients = [c for c in clients if c.get("is_wired") is False]
    elif connection_type == "wired":
        clients = [c for c in clients if c.get("is_wired") is True]

    # Format the response
    formatted_clients = []
    for client in clients:
        formatted_clients.append({
            "name": client.get("name") or client.get("hostname", "Unknown"),
            "mac": client.get("mac"),
            "ip": client.get("ip"),
            "is_wired": client.get("is_wired"),
            "ap_mac": client.get("ap_mac"),
            "essid": client.get("essid"),
            "channel": client.get("channel"),
            "signal": client.get("signal"),
            "uptime": client.get("uptime", 0),
            "uptime_hours": round(client.get("uptime", 0) / 3600, 1),
            "tx_bytes": client.get("tx_bytes", 0),
            "rx_bytes": client.get("rx_bytes", 0),
        })

    return {
        "count": len(formatted_clients),
        "clients": formatted_clients
    }


@mcp.tool()
def get_device_stats(device_mac: str) -> dict[str, Any]:
    """
    Get detailed statistics for a specific network device.

    Args:
        device_mac: MAC address of the device (format: aa:bb:cc:dd:ee:ff)

    Returns:
        Dictionary with detailed device statistics including performance metrics.
    """
    ctrl = get_controller()
    devices = ctrl.get_aps()

    # Find the specific device
    device = next((d for d in devices if d.get("mac") == device_mac), None)

    if not device:
        return {"error": f"Device with MAC {device_mac} not found"}

    return {
        "name": device.get("name"),
        "mac": device.get("mac"),
        "model": device.get("model"),
        "ip": device.get("ip"),
        "state": device.get("state"),
        "uptime": device.get("uptime"),
        "uptime_days": round(device.get("uptime", 0) / 86400, 1),
        "version": device.get("version"),
        "num_sta": device.get("num_sta", 0),  # Number of connected stations
        "user-num_sta": device.get("user-num_sta", 0),
        "guest-num_sta": device.get("guest-num_sta", 0),
        "satisfaction": device.get("satisfaction"),
        "bytes": device.get("bytes", 0),
        "tx_bytes": device.get("tx_bytes", 0),
        "rx_bytes": device.get("rx_bytes", 0),
        "uplink": device.get("uplink"),
    }


@mcp.tool()
def restart_device(device_mac: str) -> dict[str, Any]:
    """
    Restart a network device (access point, switch, or gateway).

    Args:
        device_mac: MAC address of the device to restart (format: aa:bb:cc:dd:ee:ff)

    Returns:
        Dictionary confirming the restart command was sent.
    """
    ctrl = get_controller()

    # Verify device exists first
    devices = ctrl.get_aps()
    device = next((d for d in devices if d.get("mac") == device_mac), None)

    if not device:
        return {"error": f"Device with MAC {device_mac} not found"}

    # Restart the device
    ctrl.restart_ap(device_mac)

    return {
        "status": "success",
        "message": f"Restart command sent to {device.get('name', 'device')} ({device_mac})",
        "device_name": device.get("name"),
        "device_mac": device_mac
    }


@mcp.tool()
def block_client(client_mac: str) -> dict[str, Any]:
    """
    Block a client from accessing the network.

    Args:
        client_mac: MAC address of the client to block (format: aa:bb:cc:dd:ee:ff)

    Returns:
        Dictionary confirming the client was blocked.
    """
    ctrl = get_controller()
    ctrl.block_client(client_mac)

    return {
        "status": "success",
        "message": f"Client {client_mac} has been blocked",
        "client_mac": client_mac
    }


@mcp.tool()
def unblock_client(client_mac: str) -> dict[str, Any]:
    """
    Unblock a previously blocked client.

    Args:
        client_mac: MAC address of the client to unblock (format: aa:bb:cc:dd:ee:ff)

    Returns:
        Dictionary confirming the client was unblocked.
    """
    ctrl = get_controller()
    ctrl.unblock_client(client_mac)

    return {
        "status": "success",
        "message": f"Client {client_mac} has been unblocked",
        "client_mac": client_mac
    }


@mcp.tool()
def authorize_guest(guest_mac: str, minutes: int = 480, up_bandwidth_kbps: Optional[int] = None,
                   down_bandwidth_kbps: Optional[int] = None) -> dict[str, Any]:
    """
    Authorize a guest client with optional time and bandwidth limits.

    Args:
        guest_mac: MAC address of the guest client (format: aa:bb:cc:dd:ee:ff)
        minutes: Number of minutes to authorize (default: 480 = 8 hours)
        up_bandwidth_kbps: Upload bandwidth limit in Kbps (optional)
        down_bandwidth_kbps: Download bandwidth limit in Kbps (optional)

    Returns:
        Dictionary confirming the guest was authorized with the specified limits.
    """
    ctrl = get_controller()

    ctrl.authorize_guest(
        guest_mac,
        minutes=minutes,
        up_bandwidth=up_bandwidth_kbps,
        down_bandwidth=down_bandwidth_kbps
    )

    return {
        "status": "success",
        "message": f"Guest {guest_mac} authorized for {minutes} minutes",
        "guest_mac": guest_mac,
        "minutes": minutes,
        "expires_at": datetime.now().timestamp() + (minutes * 60),
        "up_bandwidth_kbps": up_bandwidth_kbps,
        "down_bandwidth_kbps": down_bandwidth_kbps
    }


@mcp.tool()
def list_alerts(limit: int = 20) -> dict[str, Any]:
    """
    List recent network alerts and events.

    Args:
        limit: Maximum number of alerts to return (default: 20)

    Returns:
        Dictionary containing recent alerts with timestamps and details.
    """
    ctrl = get_controller()
    alarms = ctrl.get_alarms()

    # Limit and format
    alarms = alarms[:limit] if len(alarms) > limit else alarms

    formatted_alarms = []
    for alarm in alarms:
        formatted_alarms.append({
            "datetime": datetime.fromtimestamp(alarm.get("datetime", 0) / 1000).isoformat(),
            "key": alarm.get("key"),
            "message": alarm.get("msg"),
            "subsystem": alarm.get("subsystem"),
            "site_id": alarm.get("site_id"),
            "archived": alarm.get("archived", False),
        })

    return {
        "count": len(formatted_alarms),
        "alerts": formatted_alarms
    }


@mcp.tool()
def get_network_health() -> dict[str, Any]:
    """
    Get overall network health status and statistics.

    Returns:
        Dictionary with network health metrics including device status, client counts, and system info.
    """
    ctrl = get_controller()

    # Gather various stats
    devices = ctrl.get_aps()
    clients = ctrl.get_clients()
    health = ctrl.get_healthinfo()

    # Calculate health metrics
    total_devices = len(devices)
    adopted_devices = len([d for d in devices if d.get("adopted")])
    connected_devices = len([d for d in devices if d.get("state") == 1])

    total_clients = len(clients)
    wireless_clients = len([c for c in clients if not c.get("is_wired")])
    wired_clients = len([c for c in clients if c.get("is_wired")])

    return {
        "devices": {
            "total": total_devices,
            "adopted": adopted_devices,
            "connected": connected_devices,
            "disconnected": total_devices - connected_devices
        },
        "clients": {
            "total": total_clients,
            "wireless": wireless_clients,
            "wired": wired_clients
        },
        "health_info": health
    }


@mcp.tool()
def get_site_info() -> dict[str, Any]:
    """
    Get information about the Unifi site/controller.

    Returns:
        Dictionary with site configuration and version information.
    """
    ctrl = get_controller()
    sites = ctrl.get_sites()

    return {
        "sites": sites,
        "controller_version": os.getenv("UNIFI_VERSION", "unknown")
    }


if __name__ == "__main__":
    mcp.run()
