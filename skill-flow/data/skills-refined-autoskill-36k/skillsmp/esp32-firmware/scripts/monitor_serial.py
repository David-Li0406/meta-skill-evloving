#!/usr/bin/env python3
"""
Serial monitor for ESP32 devices.
Usage: python monitor_serial.py [port] [duration_seconds]

Defaults: /dev/ttyACM0, 10 seconds
"""

import serial
import sys
import time


def monitor(port: str = "/dev/ttyACM0", duration: int = 10, baudrate: int = 115200):
    """Read serial output from ESP32 device."""
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Monitoring {port} at {baudrate} baud for {duration}s...")
        print("-" * 50)

        start = time.time()
        while time.time() - start < duration:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                print(data.decode('utf-8', errors='ignore'), end='', flush=True)
            time.sleep(0.05)

        print("\n" + "-" * 50)
        print("Monitoring complete.")
        ser.close()
        return 0
    except serial.SerialException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    sys.exit(monitor(port, duration))
