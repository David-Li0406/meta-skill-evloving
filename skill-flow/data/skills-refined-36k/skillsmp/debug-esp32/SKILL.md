---
name: debug-esp32
description: GDB debugging for ESP32-S3 firmware. Use when user asks to debug, gdb, breakpoint, step through, backtrace, info stack, inspect variables, or investigate crashes in ESP32 firmware.
---

# ESP32-S3 GDB Debugging Skill

Use this skill when the user asks to debug, GDB debug, step through, set breakpoints, or inspect ESP32 firmware.

## Quick Start Workflow

```bash
# 1. Start debug session
esp32_start_debug(projectPath="/home/pncosta/domes/firmware/domes")
# Save the sessionId!

# 2. Reset and halt the device
esp32_gdb_command(sessionId, "monitor reset halt")

# 3. Set breakpoint
esp32_set_breakpoint(sessionId, location="main.cpp:94")

# 4. Continue with async mode (IMPORTANT!)
esp32_gdb_command(sessionId, "c &")

# 5. Wait for breakpoint, then check if hit
sleep 3-5 seconds
esp32_gdb_command(sessionId, "-break-list")  # Check times field

# 6. Interrupt if needed
esp32_gdb_command(sessionId, "-exec-interrupt")

# 7. Inspect state
esp32_gdb_command(sessionId, "info stack")
esp32_gdb_command(sessionId, "info locals")
```

## Critical Learnings

### 1. Always Use Async Continue
The `esp32_continue` tool can timeout waiting for breakpoints. Instead use:
```
esp32_gdb_command(sessionId, "c &")
```
Then wait and check breakpoint status with `-break-list`.

### 2. Always Reset After Starting
The device might be in an unknown state. Always run:
```
esp32_gdb_command(sessionId, "monitor reset halt")
```

### 3. Verify Breakpoints Were Hit
Use MI format to check the `times` field:
```
esp32_gdb_command(sessionId, "-break-list")
# Look for times="1" or higher = breakpoint was hit
# times="0" = breakpoint not hit yet
```

### 4. Interrupt Running Target
When target is running with `c &`, interrupt with:
```
esp32_gdb_command(sessionId, "-exec-interrupt")
```

### 5. Source Code Must Match ELF
If breakpoints aren't hit or symbols are wrong:
1. Rebuild: `idf.py build`
2. Reflash: `idf.py -p /dev/ttyACM0 flash`
3. Restart debug session

### 6. Check Firmware Works First
Before debugging issues, verify firmware runs correctly:
```python
# Monitor serial output
. ~/esp/esp-idf/export.sh && python3 -c "
import serial, time
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.setRTS(True); time.sleep(0.1); ser.setRTS(False)
start = time.time()
while time.time() - start < 6:
    if ser.in_waiting:
        print(ser.read(ser.in_waiting).decode('utf-8', errors='ignore'), end='')
    time.sleep(0.1)
ser.close()
"
```

## Available MCP Tools

### Session Management
| Tool | Description |
|------|-------------|
| `esp32_start_debug` | Start OpenOCD + GDB session |
| `esp32_stop_debug` | Terminate session |
| `esp32_list_sessions` | List active sessions |

### Breakpoints
| Tool | Description |
|------|-------------|
| `esp32_set_breakpoint` | Set at function or file:line |
| `esp32_delete_breakpoint` | Remove by number |
| `esp32_list_breakpoints` | List all breakpoints |

### Execution Control
| Tool | Description |
|------|-------------|
| `esp32_continue` | Continue (may timeout - prefer `c &` via gdb_command) |
| `esp32_step` | Step into |
| `esp32_next` | Step over |
| `esp32_finish` | Run until return |
| `esp32_halt` | Pause execution |
| `esp32_reset` | Reset and halt |

### Inspection
| Tool | Description |
|------|-------------|
| `esp32_backtrace` | Call stack |
| `esp32_print` | Evaluate expression |
| `esp32_examine_memory` | Read memory |
| `esp32_info_registers` | CPU registers |
| `esp32_info_locals` | Local variables |
| `esp32_list_source` | Display source |

### FreeRTOS
| Tool | Description |
|------|-------------|
| `esp32_list_tasks` | List tasks/threads |
| `esp32_switch_task` | Switch to task |

### Raw GDB
| Tool | Description |
|------|-------------|
| `esp32_gdb_command` | Execute any GDB command |

## Useful GDB Commands (via esp32_gdb_command)

```gdb
# Reset and halt
monitor reset halt

# Async continue (doesn't block)
c &

# Interrupt running target
-exec-interrupt

# Check breakpoints with hit count
-break-list

# Stack trace
info stack
bt
where

# Local variables
info locals

# Print variable
print variableName
print *pointer
print array[0]

# Source code
list 90,100

# All threads/tasks
info threads

# Delete all breakpoints
delete

# Memory examination
x/16xb 0x3FC94200
```

## Common Issues & Solutions

### 1. Breakpoint Never Hit
- **Cause**: Target running in idle task, task not created yet
- **Solution**:
  1. Check firmware runs correctly with serial monitor
  2. Set breakpoint on `app_main` first to verify breakpoints work
  3. Wait longer (FreeRTOS task scheduling)

### 2. GDB Commands Timeout
- **Cause**: Target is running, command blocked waiting
- **Solution**: Use `-exec-interrupt` then retry

### 3. Stuck in Panic/Flash Code
- **Cause**: Firmware crashed or corrupted state
- **Solution**:
  1. Stop debug session
  2. Reflash: `idf.py -p /dev/ttyACM0 flash`
  3. Restart debug session

### 4. Wrong Source Lines / Symbols
- **Cause**: ELF doesn't match source code
- **Solution**: Rebuild and reflash firmware

### 5. "TWDT already initialized" Error
- **Cause**: ESP-IDF auto-initializes Task Watchdog
- **Solution**: Handle `ESP_ERR_INVALID_STATE` in watchdog init code

### 6. Connection Failed on Start
- **Cause**: Device busy or previous session not cleaned up
- **Solution**:
  1. Stop any existing session
  2. Wait 2 seconds
  3. Try again

## Project Defaults

| Setting | Value |
|---------|-------|
| Project Path | `/home/pncosta/domes/firmware/domes` |
| ELF File | `build/domes.elf` |
| Serial Port | `/dev/ttyACM0` |
| JTAG | Built-in USB-OTG JTAG |

## Example: Debug LED Color Change

```python
# 1. Start session
session = esp32_start_debug(projectPath="/home/pncosta/domes/firmware/domes")
sessionId = session.sessionId

# 2. Reset device
esp32_gdb_command(sessionId, "monitor reset halt")

# 3. Set breakpoint where LED color changes
esp32_set_breakpoint(sessionId, location="main.cpp:94")

# 4. Continue async
esp32_gdb_command(sessionId, "c &")

# 5. Wait for LED task to start
time.sleep(4)

# 6. Check if breakpoint hit
esp32_gdb_command(sessionId, "-break-list")  # times="1" means hit

# 7. Show stack
esp32_gdb_command(sessionId, "info stack")
# Output:
# #0  ledDemoTask (pvParameters=0x0) at main.cpp:94
# #1  0x4037b3e0 in vPortTaskWrapper ...

# 8. Show locals
esp32_gdb_command(sessionId, "info locals")
# Output: c = {r = 255, g = 0, b = 0, name = "RED"}

# 9. Continue to next color
esp32_gdb_command(sessionId, "c &")
```
