---
name: hello-world
description: A template skill that demonstrates the standard directory structure and
  configuration. Use this as a reference when creating new skills.
license: MIT
metadata:
  author: agent-starter
  version: '1.0'
allowed-tools: Bash(python:*) Read
tags: 30_Resources
---
# Hello World Skill

This is a simple test skill that demonstrates how to use Python to output an input string. It serves as a template for creating new skills following the Agent Skills specification.

## Purpose

This skill accepts a string input and outputs it using a Python script. It's designed to test the basic skill functionality and demonstrate the standard folder structure.

## Usage

When you need to output a string using this skill:

1. Call the Python script located at `scripts/hello.py`
2. Pass the input string as a command-line argument
3. The script will output the string to stdout

## Instructions

To use this skill:

```bash
python scripts/hello.py "Your message here"
```

The script will output the exact string you provide.

## Example

Input: "Hello, World!"
Output: "Hello, World!"

## References

- [Agent Skills Specification](https://agentskills.io/specification)
