---
name: daemon-port-management
description: Instructions for managing application ports with the AutomateLinux daemon.
---

# Port Management

The AutomateLinux daemon acts as a central registry for application ports, allowing cross-component service discovery.

## CLI Usage

Use the high-level `d` command (which aliases `daemon send`) to manage ports.

### Setting a Port
Registers a port for a specific key (e.g., `pt` for Public Transportation).

```bash
d setPort --key pt --value 3001
```

### Getting a Port
Retrieves the currently registered port for a specific key.

```bash
d getPort --key pt
```

### Listing All Ports
Displays a list of all registered applications and their assigned ports.

```bash
d listPorts
```

### Deleting a Port
Removes the port mapping for a specific key.

```bash
d deletePort --key pt
```

## How it Works

### Persistence
The daemon stores these ports in the `settings` table of its MySQL database. The keys are automatically prefixed with `port_` (e.g., `port_pt`).

### Integration
Component logic (like in `mainCommand.cpp` or `InputMapper.cpp`) can retrieve these values using the `SettingsTable` manager:

```cpp
string port = SettingsTable::getSetting("port_pt");
if (!port.empty()) {
    string url = "http://localhost:" + port;
}
```

## Port Allocation Scheme

- **3000-3499**: App prod/dev ports (2 per app, sequential)
- **3500+**: Special operational ports (WebSocket servers, bridges, etc.)

## Current Port Registry

| Key | Port | Description |
| :--- | :--- | :--- |
| cad-prod | 3000 | CAD app production |
| cad-dev | 3001 | CAD app development |
| pt-prod | 3002 | Public Transportation production |
| pt-dev | 3003 | Public Transportation development |
| loom-prod | 3004 | Loom client production |
| loom-dev | 3005 | Loom client development |
| dashboard-prod | 3006 | Dashboard frontend production |
| dashboard-dev | 3007 | Dashboard frontend development |
| loom-server | 3500 | Loom WebSocket stream server |
| dashboard-bridge | 3501 | Dashboard daemon bridge |

> [!NOTE]
> Port management is useful for macros that need to launch browsers or proxy services to specific local addresses without hardcoding them in the binary.
