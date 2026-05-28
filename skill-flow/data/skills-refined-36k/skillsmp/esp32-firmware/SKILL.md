---
name: esp32-firmware
description: Build, flash, and monitor ESP32 firmware using ESP-IDF. Use when compiling, flashing, or debugging ESP32/ESP32-S3 firmware, viewing serial output, or working with idf.py commands.
---

# ESP32 Firmware Development

## Environment Setup

Before any ESP-IDF command, source the environment:

```bash
. ~/esp/esp-idf/export.sh
```

ESP-IDF is installed at `~/esp/esp-idf` (v5.2.2). Python venv is at `~/.espressif/python_env/idf5.2_py3.13_env/`.

## Quick Reference

| Action | Command |
|--------|---------|
| Build | `idf.py build` |
| Flash | `idf.py -p /dev/ttyACM0 flash` |
| Monitor | `idf.py -p /dev/ttyACM0 monitor` |
| Flash + Monitor | `idf.py -p /dev/ttyACM0 flash monitor` |
| Clean | `idf.py fullclean` |
| Set Target | `idf.py set-target esp32s3` |
| Menuconfig | `idf.py menuconfig` |

## Device Information

- **Port**: `/dev/ttyACM0` (USB-Serial/JTAG)
- **Chip**: ESP32-S3 (QFN56, revision v0.2)
- **Features**: WiFi, BLE, 8MB PSRAM, 16MB Flash
- **Console**: USB Serial/JTAG (configured via `CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y`)

## Build Workflow

```bash
# Navigate to project (example: hello_world)
cd /home/pncosta/domes/firmware/hello_world

# Source ESP-IDF environment
. ~/esp/esp-idf/export.sh

# Build firmware
idf.py build

# Flash to device
idf.py -p /dev/ttyACM0 flash
```

## Monitoring Serial Output

### PROHIBITED COMMANDS - NEVER USE ON SERIAL PORTS:
- `dd` - NEVER use on /dev/ttyACM* or /dev/ttyUSB*
- `cat` - NEVER use to read serial ports
- `head`/`tail` - NEVER use on serial devices

### Correct Approach

The `idf.py monitor` command requires a TTY. For non-TTY environments, use Python:

```python
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
start = time.time()
while time.time() - start < 10:  # Read for 10 seconds
    if ser.in_waiting:
        print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'), end='')
    time.sleep(0.1)
ser.close()
```

Run with ESP-IDF Python environment:

```bash
. ~/esp/esp-idf/export.sh && python3 -c "$(cat <<'EOF'
import serial, time
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
start = time.time()
while time.time() - start < 10:
    if ser.in_waiting:
        print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'), end='')
    time.sleep(0.1)
ser.close()
EOF
)"
```

## Project Structure

ESP-IDF projects require:

```
project_name/
├── CMakeLists.txt          # Top-level CMake file
├── sdkconfig               # Generated config (do not edit directly)
├── sdkconfig.defaults      # Default config overrides
├── main/
│   ├── CMakeLists.txt      # Component CMake file
│   └── main.c              # Application entry point
└── build/                  # Build output (generated)
```

### Minimal CMakeLists.txt (project root)

```cmake
cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(project_name)
```

### Minimal CMakeLists.txt (main component)

```cmake
idf_component_register(SRCS "main.c"
                       INCLUDE_DIRS "")
```

## Common sdkconfig.defaults

For ESP32-S3 with USB console:

```
CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Device not found | Check `ls /dev/ttyACM*` and ensure user is in `dialout` group |
| Flash fails | Hold BOOT button while flashing, or check USB cable |
| No serial output | Verify `CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y` in sdkconfig |
| Build errors | Run `idf.py fullclean` then rebuild |

## Creating New Projects

```bash
. ~/esp/esp-idf/export.sh
mkdir -p /home/pncosta/domes/firmware/new_project/main
cd /home/pncosta/domes/firmware/new_project

# Create project files, then:
idf.py set-target esp32s3
idf.py build
```

## Utility Scripts

**Monitor serial output** (for non-TTY environments):
```bash
. ~/esp/esp-idf/export.sh && python3 scripts/monitor_serial.py /dev/ttyACM0 10
```

**Flash and verify output**:
```bash
./scripts/flash_and_verify.sh /home/pncosta/domes/firmware/hello_world /dev/ttyACM0 "Hello"
```

## Serial OTA Testing

Test firmware updates via USB-CDC without using esptool flash:

### 1. Build firmware (don't flash)
```bash
cd /home/pncosta/domes/firmware/domes
. ~/esp/esp-idf/export.sh
idf.py build
```

### 2. Transfer via OTA sender
```bash
/home/pncosta/domes/firmware/host/build/simple_ota_sender \
    /dev/ttyACM0 \
    /home/pncosta/domes/firmware/domes/build/domes.bin \
    v1.0.0
```

### 3. Verify with serial monitor
```bash
python3 .claude/skills/esp32-firmware/scripts/monitor_serial.py /dev/ttyACM0 10
```

Or reset device and capture boot:
```python
import serial, time
port = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)
port.dtr = False; port.rts = True; time.sleep(0.1); port.rts = False
start = time.time()
while time.time() - start < 8:
    data = port.read(1024)
    if data: print(data.decode('utf-8', errors='replace'), end='')
port.close()
```

### Host tool build (if needed)
```bash
cd /home/pncosta/domes/firmware/host
cmake -B build && cd build && make simple_ota_sender
```

## Additional References

- **Configuration options**: See [CONFIGS.md](CONFIGS.md) for sdkconfig options, partition tables, and pin mappings
- **Project firmware guidelines**: See [firmware/GUIDELINES.md](../../firmware/GUIDELINES.md)
- **ESP-IDF documentation**: https://docs.espressif.com/projects/esp-idf/en/v5.2.2/
- **OTA architecture**: See `research/architecture/08-ota-updates.md`
