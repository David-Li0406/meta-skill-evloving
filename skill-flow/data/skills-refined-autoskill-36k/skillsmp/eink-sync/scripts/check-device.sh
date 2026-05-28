#!/bin/bash
# check-device.sh - verify X4 is reachable
# usage: ./check-device.sh [ip]

IP="${1:-10.0.0.61}"

echo "Checking X4 at $IP..."

if curl -s --max-time 3 "http://$IP/" | grep -qi "crosspoint\|file.*manager"; then
  echo "Device ready"
  exit 0
else
  echo "Device not reachable"
  echo ""
  echo "To enable file transfer on X4:"
  echo "  1. Power on device"
  echo "  2. Go to Settings > File Transfer"
  echo "  3. Enable WiFi transfer"
  echo "  4. Wait for IP to appear"
  exit 1
fi
