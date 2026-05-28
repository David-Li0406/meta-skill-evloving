---
name: checking-system-health
description: >-
  Provides comprehensive pre-flight verification for acquisition systems. Orchestrates MCP tools to check network
  mounts, hardware connectivity, and system configuration. Use before running acquisition sessions or when
  troubleshooting system issues.
---

# System Health Check

Provides comprehensive pre-flight verification for acquisition systems by orchestrating multiple MCP tools to validate
network storage, hardware connectivity, and system configuration.

---

## MCP Server Requirements

All four MCP servers must be running to perform a complete system health check.

| Server                  | Start Command      | Tools Used                                   |
|-------------------------|--------------------|----------------------------------------------|
| sl-experiment           | `sl-get mcp`       | Mount checks, Zaber discovery, projects      |
| sl-shared-assets        | `sl-configure mcp` | Working directory, credentials, templates    |
| ataraxis-video-system   | `axvs mcp`         | Camera discovery, video requirements, CTI    |
| ataraxis-comm-interface | `axci-mcp`         | Microcontroller discovery, MQTT broker       |

If any MCP server is unavailable, inform the user which server is needed and provide the start command.

---

## Complete Verification Workflow

Copy this checklist when performing a system health check:

```text
System Health Check Progress:
- [ ] Phase 1: Configuration prerequisites verified
- [ ] Phase 2: Network storage mounts accessible
- [ ] Phase 3: Hardware discovery completed
- [ ] Phase 4: Video system requirements verified
- [ ] Phase 5: Configuration validation passed
```

### Phase 1: Configuration Prerequisites

| Check                        | Tool                                | Expected Result                     |
|------------------------------|-------------------------------------|-------------------------------------|
| Working directory set        | `get_working_directory_tool`        | Returns valid path                  |
| System config exists         | `check_system_mounts_tool`          | Returns system name                 |
| Task templates directory set | `get_task_templates_directory_tool` | Returns valid path to Unity configs |

**Task templates directory** must point to the `sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations/` folder.
If not configured, use `set_task_templates_directory_tool(directory)` to set it before running experiments.

### Phase 2: Network Storage Mounts

| Check                 | Tool                       | Expected Result            |
|-----------------------|----------------------------|----------------------------|
| All mounts accessible | `check_system_mounts_tool` | All paths show "OK" status |

If any mount fails, use `check_mount_accessibility_tool(path)` for detailed diagnostics on specific paths.

**Interpreting mount results:**

- `Exists: No` indicates the path does not exist. Check mount configuration in `/etc/fstab` or systemd mount units.
- `Mount: No` indicates the path exists but is not a mount point. This may indicate a local directory is being used
  instead of network storage.
- `Writable: No` indicates the path exists but write test failed. Check permissions or mount options (uid, gid,
  file_mode, dir_mode).

### Phase 3: Hardware Discovery

| Check                     | Tool                                   | Expected Result                    |
|---------------------------|----------------------------------------|------------------------------------|
| Cameras detected          | `list_cameras`                         | Shows expected camera indices      |
| Microcontrollers detected | `list_microcontrollers`                | Shows ACTOR, SENSOR, ENCODER ports |
| Zaber motors detected     | `get_zaber_devices_tool`               | Shows all motor groups and axes    |
| MQTT broker reachable     | `check_mqtt_broker("127.0.0.1", 1883)` | Connection successful              |

### Phase 4: Video System Requirements

| Check                 | Tool                         | Expected Result                        |
|-----------------------|------------------------------|----------------------------------------|
| Runtime requirements  | `check_runtime_requirements` | FFMPEG available, GPU detected         |
| CTI file (Harvesters) | `get_cti_status`             | CTI file configured (if using GeniCam) |

### Phase 5: Configuration Validation

| Check              | Tool                                             | Expected Result              |
|--------------------|--------------------------------------------------|------------------------------|
| Projects exist     | `get_projects_tool`                              | Lists expected projects      |
| Zaber config valid | `validate_zaber_configuration_tool(port, index)` | Status: VALID for each motor |

---

## Quick Health Check

For a rapid pre-session check, run these tools in sequence:

1. `check_system_mounts_tool()` verifies all storage is accessible
2. `list_cameras()` confirms cameras are connected
3. `list_microcontrollers()` confirms microcontrollers are connected
4. `get_zaber_devices_tool()` confirms motors are connected
5. `check_mqtt_broker("127.0.0.1", 1883)` confirms Unity communication ready

If all pass, the system is ready for acquisition.

---

## Troubleshooting Guide

### Mount Failures

| Symptom                 | Likely Cause          | Resolution                                              |
|-------------------------|-----------------------|---------------------------------------------------------|
| Path does not exist     | Mount not configured  | Add entry to `/etc/fstab` or create systemd mount unit  |
| Exists but not mount    | Local directory used  | Check mount status with `mount | grep path`             |
| Not writable            | Permission issue      | Check mount options (uid, gid, file_mode, dir_mode)     |
| Stale mount             | Network disruption    | Remount: `sudo umount -l /path && sudo mount /path`     |

### Hardware Not Detected

| Symptom                  | Likely Cause             | Resolution                                            |
|--------------------------|--------------------------|-------------------------------------------------------|
| Camera not in list       | USB disconnected         | Check physical connection                             |
| Wrong camera index       | USB enumeration changed  | Re-run discovery after reboot                         |
| Microcontroller missing  | Port conflict            | Check `ls /dev/ttyACM*` and ensure no other process   |
| Zaber not responding     | Power off                | Verify motor power supply is on                       |

### MQTT Connection Failed

| Symptom             | Likely Cause        | Resolution                                         |
|---------------------|---------------------|----------------------------------------------------|
| Connection refused  | Broker not running  | Start Mosquitto: `sudo systemctl start mosquitto`  |
| Timeout             | Wrong IP/port       | Verify Unity PC IP address in configuration        |

---

## Post-Check Actions

After completing the health check:

1. **All checks pass**: System is ready for `/acquisition-system-setup` configuration or session execution.
2. **Mount failures**: Resolve OS-level mount issues before proceeding.
3. **Hardware missing**: Check physical connections and re-run discovery.
4. **Configuration invalid**: Use `/acquisition-system-setup` to update configuration.
