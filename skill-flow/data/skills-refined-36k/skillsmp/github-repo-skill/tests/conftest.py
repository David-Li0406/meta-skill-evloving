"""Pytest configuration for cmm-ai-automation tests.

This file is automatically loaded by pytest and sets up test fixtures
and configuration that are shared across all test modules.
"""

from dotenv import load_dotenv

# Load .env file so tests can access API keys
# This runs before any tests are collected
load_dotenv()
