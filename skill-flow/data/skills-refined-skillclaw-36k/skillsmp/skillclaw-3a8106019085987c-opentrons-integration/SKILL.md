---
name: opentrons-integration
description: Use this skill when writing protocols specifically for Opentrons hardware, leveraging the Protocol API v2 features for automation tasks on OT-2 and Flex robots.
---

# Opentrons Integration

## Overview

Opentrons is a Python-based lab automation platform for Flex and OT-2 robots. This skill enables you to write Protocol API v2 protocols for liquid handling, control hardware modules (such as heater-shakers and thermocyclers), and manage labware for automated pipetting workflows.

## When to Use This Skill

This skill should be used when:
- Writing Opentrons Protocol API v2 protocols in Python.
- Automating liquid handling workflows on Flex or OT-2 robots.
- Controlling hardware modules (temperature, magnetic, heater-shaker, thermocycler).
- Setting up labware configurations and deck layouts.
- Implementing complex pipetting operations (serial dilutions, plate replication, PCR setup).
- Managing tip usage and optimizing protocol efficiency.
- Working with multi-channel pipettes for 96-well plate operations.
- Simulating and testing protocols before robot execution.

## Core Capabilities

### 1. Protocol Structure and Metadata

Every Opentrons protocol follows a standard structure:

```python
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Protocol description',
    'apiLevel': '2.19'  # Use latest available API version
}

# Requirements (optional)
requirements = {
    'robotType': 'Flex',  # or 'OT-2'
    'apiLevel': '2.19'
}

# Run function
def run(protocol: protocol_api.ProtocolContext):
    # Protocol commands go here
    pass
```

**Key elements:**
- Import `protocol_api` from `opentrons`.
- Define `metadata` dict with protocolName, author, description, and apiLevel.
- Optional `requirements` dict for robot type and API version.
- Implement `run()` function receiving `ProtocolContext` as a parameter.
- All protocol logic goes inside the `run()` function.

### 2. Loading Hardware

**Loading Instruments (Pipettes):**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Load pipette on specific mount
    left_pipette = protocol.load_instrument(
        'p1000_single_flex',  # Instrument name
        'left',               # Mount: 'left' or 'right'
    )
```

This structure allows for the efficient setup and execution of automated lab protocols using Opentrons robots.