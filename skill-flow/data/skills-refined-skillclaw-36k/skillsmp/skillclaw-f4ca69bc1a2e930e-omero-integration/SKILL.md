---
name: omero-integration
description: Use this skill when you need to manage, visualize, and analyze microscopy images and metadata using the OMERO Python API.
---

# OMERO Integration

## Overview

OMERO is an open-source platform for managing, visualizing, and analyzing microscopy images and metadata. This skill allows you to access images via the Python API, retrieve datasets, analyze pixel data, manage regions of interest (ROIs) and annotations, and perform batch processing for high-content screening and microscopy workflows.

## When to Use This Skill

This skill should be used when:
- Working with the OMERO Python API (omero-py) to access microscopy data.
- Retrieving images, datasets, projects, or screening data programmatically.
- Analyzing pixel data and creating derived images.
- Creating or managing ROIs (regions of interest) on microscopy images.
- Adding annotations, tags, or metadata to OMERO objects.
- Storing measurement results in OMERO tables.
- Creating server-side scripts for batch processing.
- Performing high-content screening analysis.

## Core Capabilities

This skill covers several major capability areas:

### 1. Connection & Session Management
Establish secure connections to OMERO servers, manage sessions, handle authentication, and work with group contexts.

**Common scenarios:**
- Connect to OMERO server with credentials.
- Use existing session IDs.
- Switch between group contexts.
- Manage connection lifecycle with context managers.

### 2. Data Access & Retrieval
Navigate OMERO's hierarchical data structure (Projects → Datasets → Images) and screening data (Screens → Plates → Wells). Retrieve objects, query by attributes, and access metadata.

**Common scenarios:**
- List all projects and datasets for a user.
- Retrieve images by ID or dataset.
- Access screening plate data.
- Query objects with filters.

### 3. Metadata & Annotations
Create and manage annotations including tags, key-value pairs, file attachments, and comments. Link annotations to images, datasets, or other objects.

**Common scenarios:**
- Add tags to images.
- Attach analysis results as files.
- Create custom key-value metadata.
- Query annotations by namespace.

### 4. Image Processing & Rendering
Access raw pixel data and perform image processing tasks as needed.

**Common scenarios:**
- Process images to extract features.
- Render images for visualization.
- Create derived images based on analysis.

## Additional Information
For detailed documentation on each capability, refer to the relevant sections in the references directory.