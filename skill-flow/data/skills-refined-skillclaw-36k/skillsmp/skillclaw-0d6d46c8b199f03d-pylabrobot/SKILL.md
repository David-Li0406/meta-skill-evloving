---
name: pylabrobot
description: Use this skill when you need to automate laboratory workflows across multiple equipment types, such as liquid handling robots and plate readers, with a unified programming interface.
---

# PyLabRobot

## Overview

PyLabRobot is a hardware-agnostic, pure Python Software Development Kit for automated and autonomous laboratories. Use this skill to control liquid handling robots, plate readers, pumps, heater shakers, incubators, centrifuges, and other laboratory automation equipment through a unified Python interface that works across platforms (Windows, macOS, Linux).

## When to Use This Skill

Use this skill when:
- Programming liquid handling robots (Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO)
- Automating laboratory workflows involving pipetting, sample preparation, or analytical measurements
- Managing deck layouts and laboratory resources (plates, tips, containers, troughs)
- Integrating multiple lab devices (liquid handlers, plate readers, heater shakers, pumps)
- Creating reproducible laboratory protocols with state management
- Simulating protocols before running on physical hardware
- Reading plates using BMG CLARIOstar or other supported plate readers
- Controlling temperature, shaking, centrifugation, or other material handling operations
- Working with laboratory automation in Python

## Core Capabilities

PyLabRobot provides comprehensive laboratory automation through several main capability areas:

### 1. Liquid Handling

Control liquid handling robots for aspirating, dispensing, and transferring liquids. Key operations include:
- **Basic Operations**: Aspirate, dispense, transfer liquids between wells
- **Tip Management**: Pick up, drop, and track pipette tips automatically
- **Advanced Techniques**: Multi-channel pipetting, serial dilutions, plate replication
- **Volume Tracking**: Automatic tracking of liquid volumes in wells
- **Hardware Support**: Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO, and others

### 2. Resource Management

Manage laboratory resources in a hierarchical system:
- **Resource Types**: Plates, tip racks, troughs, tubes, carriers, and custom labware
- **Deck Layouts**: Define and manage the arrangement of resources on the lab deck

### 3. Protocol Simulation

Simulate laboratory protocols before executing them on physical hardware to ensure accuracy and efficiency.

### 4. State Management

Maintain the state of laboratory processes to ensure reproducibility and reliability in experiments.

## License

This skill is licensed under the MIT license.