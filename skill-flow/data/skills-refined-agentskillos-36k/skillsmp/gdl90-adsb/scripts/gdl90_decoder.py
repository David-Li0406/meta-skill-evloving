#!/usr/bin/env python3
"""
GDL 90 Protocol Decoder for ADS-B receivers.

Decodes GDL 90 messages from Stratux, ForeFlight Sentry, and other compatible devices.

Usage:
    python gdl90_decoder.py --port 4000
    python gdl90_decoder.py --input sample_traffic.bin
"""

import argparse
import socket
import struct
from dataclasses import dataclass
from typing import Optional


# GDL 90 Message Types
MSG_HEARTBEAT = 0x00
MSG_UPLINK = 0x07
MSG_OWNSHIP = 0x0A
MSG_OWNSHIP_GEO_ALT = 0x0B
MSG_TRAFFIC = 0x14
MSG_STRATUX_STATUS = 0xCC
MSG_STRATUX_AHRS = 0x4C

# Emitter categories
EMITTER_CATEGORIES = {
    0: 'Unknown',
    1: 'Light',
    2: 'Small',
    3: 'Large',
    4: 'High Vortex Large',
    5: 'Heavy',
    6: 'Highly Maneuverable',
    7: 'Rotorcraft',
    9: 'Glider',
    10: 'Lighter Than Air',
    11: 'Parachutist',
    12: 'Ultralight',
    14: 'UAV',
    15: 'Space Vehicle',
    17: 'Surface Emergency',
    18: 'Surface Service',
    19: 'Point Obstacle',
    20: 'Cluster Obstacle',
    21: 'Line Obstacle',
}


@dataclass
class TrafficReport:
    """Decoded traffic report."""
    icao_address: int
    callsign: str
    latitude: float
    longitude: float
    altitude: int
    track: int
    ground_speed: int
    vertical_speed: int
    emitter_category: int
    emitter_category_name: str
    on_ground: bool
    alert: bool
    nic: int
    nacp: int


@dataclass
class Heartbeat:
    """Decoded heartbeat message."""
    gps_valid: bool
    maintenance_required: bool
    uat_initialized: bool
    timestamp: int


@dataclass
class OwnshipReport:
    """Decoded ownship position report."""
    latitude: float
    longitude: float
    altitude: int
    track: int
    ground_speed: int
    vertical_speed: int
    nic: int
    nacp: int


class GDL90Decoder:
    """Decode GDL 90 protocol messages."""

    FLAG_BYTE = 0x7E
    ESCAPE_BYTE = 0x7D

    def __init__(self):
        self.buffer = bytearray()

    def decode(self, data: bytes) -> list:
        """Decode raw bytes into GDL 90 messages."""
        messages = []
        self.buffer.extend(data)

        while True:
            # Find start flag
            try:
                start = self.buffer.index(self.FLAG_BYTE)
                self.buffer = self.buffer[start:]
            except ValueError:
                self.buffer.clear()
                break

            # Find end flag
            try:
                end = self.buffer.index(self.FLAG_BYTE, 1)
            except ValueError:
                break

            # Extract and process frame
            frame = bytes(self.buffer[1:end])
            self.buffer = self.buffer[end:]

            msg = self._decode_frame(frame)
            if msg:
                messages.append(msg)

        return messages

    def _decode_frame(self, frame: bytes) -> Optional[dict]:
        """Decode a single GDL 90 frame."""
        # Unescape
        unescaped = self._unescape(frame)
        if len(unescaped) < 3:
            return None

        # Verify CRC
        if not self._verify_crc(unescaped):
            return None

        msg_id = unescaped[0]
        payload = unescaped[1:-2]

        if msg_id == MSG_HEARTBEAT:
            return self._decode_heartbeat(payload)
        elif msg_id == MSG_TRAFFIC:
            return self._decode_traffic(payload)
        elif msg_id == MSG_OWNSHIP:
            return self._decode_ownship(payload)
        elif msg_id == MSG_OWNSHIP_GEO_ALT:
            return self._decode_ownship_geo_alt(payload)
        else:
            return {'type': 'unknown', 'msg_id': msg_id, 'payload': payload.hex()}

    def _unescape(self, data: bytes) -> bytes:
        """Remove escape sequences."""
        result = bytearray()
        i = 0
        while i < len(data):
            if data[i] == self.ESCAPE_BYTE and i + 1 < len(data):
                result.append(data[i + 1] ^ 0x20)
                i += 2
            else:
                result.append(data[i])
                i += 1
        return bytes(result)

    def _verify_crc(self, data: bytes) -> bool:
        """Verify CRC-16 checksum."""
        if len(data) < 3:
            return False
        crc_received = struct.unpack('<H', data[-2:])[0]
        crc_calculated = self._calculate_crc(data[:-2])
        return crc_received == crc_calculated

    def _calculate_crc(self, data: bytes) -> int:
        """Calculate CRC-16 (CCITT)."""
        crc = 0
        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc

    def _decode_heartbeat(self, payload: bytes) -> dict:
        """Decode heartbeat message."""
        if len(payload) < 7:
            return None

        status1 = payload[0]
        status2 = payload[1]

        return {
            'type': 'heartbeat',
            'gps_valid': bool(status1 & 0x80),
            'maintenance_required': bool(status1 & 0x40),
            'uat_initialized': bool(status1 & 0x01),
            'ratcs': bool(status2 & 0x04),
            'timestamp': struct.unpack('>H', payload[5:7])[0],
        }

    def _decode_traffic(self, payload: bytes) -> dict:
        """Decode traffic report message."""
        if len(payload) < 28:
            return None

        # Status and address
        status = payload[0]
        alert = bool(status & 0x10)
        addr_type = status & 0x0F

        icao = (payload[1] << 16) | (payload[2] << 8) | payload[3]

        # Position (24-bit latitude/longitude)
        lat_raw = (payload[4] << 16) | (payload[5] << 8) | payload[6]
        lon_raw = (payload[7] << 16) | (payload[8] << 8) | payload[9]

        # Convert from semicircles
        if lat_raw & 0x800000:
            lat_raw -= 0x1000000
        if lon_raw & 0x800000:
            lon_raw -= 0x1000000

        latitude = lat_raw * (180.0 / 0x800000)
        longitude = lon_raw * (180.0 / 0x800000)

        # Altitude (12-bit, 25ft resolution, -1000ft offset)
        alt_raw = ((payload[10] << 4) | (payload[11] >> 4)) & 0xFFF
        altitude = (alt_raw * 25) - 1000

        # Misc flags
        misc = payload[11] & 0x0F
        on_ground = bool(misc & 0x01)

        # NIC and NACp
        nic = (payload[12] >> 4) & 0x0F
        nacp = payload[12] & 0x0F

        # Velocity
        horiz_vel = ((payload[13] << 4) | (payload[14] >> 4)) & 0xFFF
        vert_vel_raw = ((payload[14] & 0x0F) << 8) | payload[15]
        if vert_vel_raw & 0x800:
            vert_vel_raw -= 0x1000
        vertical_speed = vert_vel_raw * 64  # 64 fpm resolution

        # Track
        track = payload[16] * 360 // 256

        # Emitter category
        emitter = payload[17]

        # Callsign (8 bytes)
        callsign = payload[18:26].decode('ascii', errors='ignore').strip()

        return {
            'type': 'traffic',
            'icao_address': icao,
            'callsign': callsign,
            'latitude': latitude,
            'longitude': longitude,
            'altitude': altitude,
            'track': track,
            'ground_speed': horiz_vel,
            'vertical_speed': vertical_speed,
            'emitter_category': emitter,
            'emitter_category_name': EMITTER_CATEGORIES.get(emitter, 'Unknown'),
            'on_ground': on_ground,
            'alert': alert,
            'nic': nic,
            'nacp': nacp,
        }

    def _decode_ownship(self, payload: bytes) -> dict:
        """Decode ownship position report."""
        # Same format as traffic report
        traffic = self._decode_traffic(payload)
        if traffic:
            traffic['type'] = 'ownship'
        return traffic

    def _decode_ownship_geo_alt(self, payload: bytes) -> dict:
        """Decode ownship geometric altitude."""
        if len(payload) < 5:
            return None

        alt_raw = struct.unpack('>h', payload[0:2])[0]
        altitude = alt_raw * 5  # 5 ft resolution

        merit = struct.unpack('>H', payload[2:4])[0]
        warning = bool(payload[4] & 0x80)

        return {
            'type': 'ownship_geo_alt',
            'altitude': altitude,
            'vertical_merit': merit,
            'vertical_warning': warning,
        }


def main():
    parser = argparse.ArgumentParser(description='GDL 90 Decoder')
    parser.add_argument('--port', '-p', type=int, default=4000, help='UDP port')
    parser.add_argument('--input', '-i', help='Input file instead of UDP')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    decoder = GDL90Decoder()

    if args.input:
        with open(args.input, 'rb') as f:
            data = f.read()
            messages = decoder.decode(data)
            for msg in messages:
                print(msg)
    else:
        print(f"Listening on UDP port {args.port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', args.port))

        try:
            while True:
                data, addr = sock.recvfrom(4096)
                messages = decoder.decode(data)
                for msg in messages:
                    if msg['type'] == 'traffic':
                        print(f"Traffic: {msg['callsign']:8} "
                              f"ICAO:{msg['icao_address']:06X} "
                              f"Alt:{msg['altitude']:5}ft "
                              f"Trk:{msg['track']:03}° "
                              f"GS:{msg['ground_speed']:3}kt")
                    elif msg['type'] == 'heartbeat':
                        if args.verbose:
                            print(f"Heartbeat: GPS={'valid' if msg['gps_valid'] else 'invalid'}")
        except KeyboardInterrupt:
            print("\nStopped")
        finally:
            sock.close()


if __name__ == '__main__':
    main()
