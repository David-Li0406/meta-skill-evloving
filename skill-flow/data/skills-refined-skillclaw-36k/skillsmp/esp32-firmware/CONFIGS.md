# ESP-IDF Configuration Reference

## Common sdkconfig Options

### Console Configuration

```
# USB Serial/JTAG console (ESP32-S3/C3/C6)
CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y

# UART console (default)
CONFIG_ESP_CONSOLE_UART_DEFAULT=y

# USB CDC console
CONFIG_ESP_CONSOLE_USB_CDC=y
```

### Flash Configuration

```
# Flash size
CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y
CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y
CONFIG_ESPTOOLPY_FLASHSIZE_16MB=y

# Flash mode
CONFIG_ESPTOOLPY_FLASHMODE_QIO=y
CONFIG_ESPTOOLPY_FLASHMODE_DIO=y

# Flash frequency
CONFIG_ESPTOOLPY_FLASHFREQ_80M=y
CONFIG_ESPTOOLPY_FLASHFREQ_40M=y
```

### PSRAM Configuration

```
# Enable PSRAM
CONFIG_SPIRAM=y

# PSRAM mode (ESP32-S3)
CONFIG_SPIRAM_MODE_OCT=y
CONFIG_SPIRAM_MODE_QUAD=y

# PSRAM speed
CONFIG_SPIRAM_SPEED_80M=y
```

### FreeRTOS Configuration

```
# Tick rate
CONFIG_FREERTOS_HZ=1000

# Enable FreeRTOS stats
CONFIG_FREERTOS_USE_TRACE_FACILITY=y
CONFIG_FREERTOS_GENERATE_RUN_TIME_STATS=y
```

### Logging Configuration

```
# Default log level
CONFIG_LOG_DEFAULT_LEVEL_NONE=y
CONFIG_LOG_DEFAULT_LEVEL_ERROR=y
CONFIG_LOG_DEFAULT_LEVEL_WARN=y
CONFIG_LOG_DEFAULT_LEVEL_INFO=y
CONFIG_LOG_DEFAULT_LEVEL_DEBUG=y
CONFIG_LOG_DEFAULT_LEVEL_VERBOSE=y

# Log colors
CONFIG_LOG_COLORS=y
```

### WiFi Configuration

```
# Enable WiFi
CONFIG_ESP_WIFI_ENABLED=y

# WiFi mode
CONFIG_ESP_WIFI_MODE_STA=y
CONFIG_ESP_WIFI_MODE_AP=y
CONFIG_ESP_WIFI_MODE_APSTA=y
```

### Bluetooth Configuration

```
# Enable Bluetooth
CONFIG_BT_ENABLED=y

# BLE only
CONFIG_BT_NIMBLE_ENABLED=y

# Classic + BLE
CONFIG_BT_BLUEDROID_ENABLED=y
```

## Partition Tables

### Default (single OTA)

```csv
# Name,   Type, SubType, Offset,  Size,    Flags
nvs,      data, nvs,     0x9000,  0x6000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 1M,
```

### With OTA Support

```csv
# Name,   Type, SubType, Offset,  Size,    Flags
nvs,      data, nvs,     0x9000,  0x4000,
otadata,  data, ota,     0xd000,  0x2000,
phy_init, data, phy,     0xf000,  0x1000,
ota_0,    app,  ota_0,   0x10000, 1856K,
ota_1,    app,  ota_1,   ,        1856K,
```

## Pin Mappings (ESP32-S3-WROOM-1)

| Function | GPIO |
|----------|------|
| USB D+ | GPIO20 (internal) |
| USB D- | GPIO19 (internal) |
| UART0 TX | GPIO43 |
| UART0 RX | GPIO44 |
| I2C SDA | GPIO8 (typical) |
| I2C SCL | GPIO9 (typical) |
| SPI MOSI | GPIO11 |
| SPI MISO | GPIO13 |
| SPI CLK | GPIO12 |

## Common idf.py Commands

```bash
# Build and flash
idf.py build
idf.py -p PORT flash
idf.py -p PORT flash monitor

# Configuration
idf.py menuconfig
idf.py set-target esp32s3
idf.py reconfigure

# Cleaning
idf.py clean
idf.py fullclean

# Information
idf.py size
idf.py size-components
idf.py size-files

# Debugging
idf.py openocd
idf.py gdb
```
