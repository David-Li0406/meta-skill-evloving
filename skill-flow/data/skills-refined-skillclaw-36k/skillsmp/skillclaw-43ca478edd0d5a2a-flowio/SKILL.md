---
name: flowio
description: Use this skill when you need to parse Flow Cytometry Standard (FCS) files, extract event data as NumPy arrays, and convert flow cytometry data for preprocessing and analysis.
---

# FlowIO: Flow Cytometry Standard File Handler

## Overview

FlowIO is a lightweight Python library for reading and writing Flow Cytometry Standard (FCS) files. It supports FCS versions 2.0, 3.0, and 3.1, allowing for efficient parsing of FCS metadata, extraction of event data, and creation of new FCS files with minimal dependencies.

## When to Use This Skill

This skill should be used when:

- You need to parse FCS files or extract metadata.
- Flow cytometry data requires conversion to NumPy arrays.
- You need to export event data to FCS format.
- You are working with multi-dataset FCS files that need separation.
- You need to extract channel information (scatter, fluorescence, time).
- You want to validate or inspect cytometry files.
- You are preparing data for advanced analysis workflows.

**Related Tools:** For advanced flow cytometry analysis including compensation, gating, and FlowJo/GatingML support, consider using the FlowKit library alongside FlowIO.

## Installation

```bash
pip install flowio
```

Requires Python 3.9 or later.

## Quick Start

### Basic File Reading

```python
from flowio import FlowData

# Read FCS file
flow_data = FlowData('experiment.fcs')

# Access basic information
print(f"FCS Version: {flow_data.version}")
print(f"Events: {flow_data.event_count}")
print(f"Channels: {flow_data.pnn_labels}")

# Get event data as NumPy array
events = flow_data.as_array()  # Shape: (events, channels)
```

### Creating FCS Files

```python
import numpy as np
from flowio import create_fcs

# Prepare data
data = np.array([[100, 200, 50], [150, 180, 60]])  # 2 events, 3 channels
channels = ['FSC-A', 'SSC-A', 'FL1-A']

# Create FCS file
create_fcs('output.fcs', data, channels)
```

## Core Workflows

### Reading and Parsing FCS Files

The FlowData class provides the primary interface for reading FCS files.

**Standard Reading:**

```python
from flowio import FlowData

# Basic reading
flow = FlowData('sample.fcs')

# Access attributes
version = flow.version              # '3.0', '3.1', etc.
event_count = flow.event_count      # Number of events
channel_count = flow.channel_count  # Number of channels
pnn_labels = flow.pnn_labels        # Short channel names
pns_labels = flow.pns_labels        # Descriptive stain names
```