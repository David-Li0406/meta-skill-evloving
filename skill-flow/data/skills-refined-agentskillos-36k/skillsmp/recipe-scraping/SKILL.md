---
name: recipe-scraping
description: Guidelines and standards for scraping recipes from external sources using automated tools.
---

# Recipe Scraping Guidelines

This document outlines the standards and procedures for scraping recipes from external sources using automated tools.

## Table of Contents
- [Tool Usage](#tool-usage)
- [Organization](#organization)
- [Metadata Requirements](#metadata-requirements)
- [Content Formatting](#content-formatting)

## Tool Usage

- **Primary Tool**: Use firecrawl-local MCP server for scraping recipe content from URLs.
- **Parameters**: Use `formats: ["markdown"]` and `onlyMainContent: true` for clean extraction.
- **Multiple Pages**: If a source links to individual recipes, crawl each recipe URL separately to get full details.

## Organization

- **Directory Structure**: Store scraped recipes in `phase0_flow/recipes/<site>/` where `<site>` is the domain name with hyphens (e.g., `newsletter-ethanchlebowski-com`).
- **File Naming**: Use kebab-case filenames based on the recipe title (e.g., `steak-and-corn-tostada.md`).
- **Grouping**: Keep recipes from the same source together in their dedicated subdirectory.

## Metadata Requirements

- **Source URL**: Include the original source URL at the top of each recipe file in the format `Source: https://example.com/recipe-url`.
- **Scraping Date**: Optional: Include scraping date in ISO 8601 format if needed for tracking.

## Content Formatting

- **Attribution**: Always include source attribution to respect original content creators.
- **Structure**: Use standard markdown with `# Title`, `### Ingredients`, `### Instructions`.
- **Ingredients**: List ingredients in bullet points, grouped by component if applicable.
- **Instructions**: Number the steps sequentially.
- **Preservation**: Maintain original recipe details including quantities, cooking times, and tips.