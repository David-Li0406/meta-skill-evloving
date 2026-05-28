"""
Custom UniFi OS Controller for Cloud Key Gen 2 Plus and other UniFi OS devices.

This handles the UniFi OS authentication flow which is different from legacy controllers.
"""

import requests
import urllib3
from typing import Any, Optional

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UniFiOSController:
    """
    Controller for UniFi OS devices (Cloud Key Gen 2 Plus, UDM Pro, etc.)

    Uses the UniFi OS authentication and API paths.
    """

    def __init__(self, host: str, username: str, password: str, port: int = 443,
                 site_id: str = "default", ssl_verify: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.site_id = site_id
        self.ssl_verify = ssl_verify
        self.base_url = f"https://{host}:{port}"
        self.session = requests.Session()
        self.session.verify = ssl_verify

        # Authenticate
        self._login()

    def _login(self):
        """Authenticate with UniFi OS"""
        login_url = f"{self.base_url}/api/auth/login"

        response = self.session.post(
            login_url,
            json={"username": self.username, "password": self.password},
            timeout=10
        )

        if response.status_code != 200:
            raise Exception(f"Login failed with status {response.status_code}: {response.text}")

        # Cookies are automatically stored in the session

    def _api_url(self, endpoint: str) -> str:
        """Build API URL for Network application"""
        # UniFi OS uses /proxy/network for the Network application API
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.base_url}/proxy/network/api/s/{self.site_id}{endpoint}"

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make GET request to API"""
        url = self._api_url(endpoint)
        response = self.session.get(url, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        data = response.json()
        return data.get("data", [])

    def _post(self, endpoint: str, json_data: Optional[dict] = None) -> dict:
        """Make POST request to API"""
        url = self._api_url(endpoint)
        response = self.session.post(url, json=json_data, timeout=10)

        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")

        data = response.json()
        return data.get("data", [])

    # Device Methods

    def get_aps(self) -> list[dict[str, Any]]:
        """Get all devices (APs, switches, gateways)"""
        return self._get("/stat/device")

    def restart_ap(self, mac: str):
        """Restart a device by MAC address"""
        return self._post(f"/cmd/devmgr", {"cmd": "restart", "mac": mac})

    # Client Methods

    def get_clients(self) -> list[dict[str, Any]]:
        """Get all connected clients"""
        return self._get("/stat/sta")

    def block_client(self, mac: str):
        """Block a client by MAC address"""
        return self._post("/cmd/stamgr", {"cmd": "block-sta", "mac": mac})

    def unblock_client(self, mac: str):
        """Unblock a client by MAC address"""
        return self._post("/cmd/stamgr", {"cmd": "unblock-sta", "mac": mac})

    def authorize_guest(self, mac: str, minutes: int = 480,
                       up_bandwidth: Optional[int] = None,
                       down_bandwidth: Optional[int] = None):
        """Authorize a guest client with optional bandwidth limits"""
        cmd_data = {
            "cmd": "authorize-guest",
            "mac": mac,
            "minutes": minutes
        }

        if up_bandwidth:
            cmd_data["up"] = up_bandwidth
        if down_bandwidth:
            cmd_data["down"] = down_bandwidth

        return self._post("/cmd/stamgr", cmd_data)

    def disconnect_client(self, mac: str):
        """Disconnect a client (for reassociation)"""
        return self._post("/cmd/stamgr", {"cmd": "kick-sta", "mac": mac})

    # System Methods

    def get_alarms(self) -> list[dict[str, Any]]:
        """Get system alarms/alerts"""
        return self._get("/list/alarm")

    def get_healthinfo(self) -> list[dict[str, Any]]:
        """Get health information"""
        return self._get("/stat/health")

    def get_sites(self) -> list[dict[str, Any]]:
        """Get list of sites"""
        # Sites list is at controller level, not site-specific
        url = f"{self.base_url}/proxy/network/api/self/sites"
        response = self.session.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Failed to get sites: {response.status_code}")

        data = response.json()
        return data.get("data", [])
