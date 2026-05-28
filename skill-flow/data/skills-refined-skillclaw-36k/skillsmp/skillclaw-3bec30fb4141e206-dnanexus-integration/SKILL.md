---
name: dnanexus-integration
description: Use this skill when you need to build and manage applications on the DNAnexus cloud platform for genomics data analysis, including data operations and workflow execution.
---

# DNAnexus Integration

## Overview

DNAnexus is a cloud platform for biomedical data analysis and genomics. This skill enables you to build and deploy apps/applets, manage data objects, run workflows, and utilize the dxpy Python SDK for genomics pipeline development and execution.

## When to Use This Skill

Use this skill when:
- Creating, building, or modifying DNAnexus apps/applets
- Uploading, downloading, searching, or organizing files and records
- Running analyses, monitoring jobs, and creating workflows
- Writing scripts using dxpy to interact with the platform
- Setting up dxapp.json, managing dependencies, and using Docker
- Processing FASTQ, BAM, VCF, or other bioinformatics files
- Managing projects, permissions, or platform resources

## Core Capabilities

The skill is organized into two main areas:

### 1. App Development

**Purpose**: Create executable programs (apps/applets) that run on the DNAnexus platform.

**Key Operations**:
- Generate app skeleton with `dx-app-wizard`
- Write Python or Bash apps with proper entry points
- Handle input/output data objects
- Deploy with `dx build` or `dx build --app`
- Test apps on the platform

**Common Use Cases**:
- Bioinformatics pipelines (alignment, variant calling)
- Data processing workflows
- Quality control and filtering
- Format conversion tools

### 2. Data Operations

**Purpose**: Manage files, records, and other data objects on the platform.

**Key Operations**:
- Upload/download files with `dxpy.upload_local_file()` and `dxpy.download_dxfile()`
- Create and manage records with metadata
- Search for data objects by name, properties, or type
- Clone data between projects
- Manage project folders and permissions

**Common Use Cases**:
- Uploading sequencing data (FASTQ files)
- Organizing analysis results
- Searching for specific samples or experiments
- Backing up data across projects
- Managing reference genomes and annotations

## Compatibility

Requires a DNAnexus account to access the platform and its features.