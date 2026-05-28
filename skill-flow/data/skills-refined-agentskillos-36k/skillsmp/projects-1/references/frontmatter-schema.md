# Project Frontmatter Schema

## Required Fields

| Field         | Type     | Description                                       |
| ------------- | -------- | ------------------------------------------------- |
| `title`       | string   | The project title displayed on the page           |
| `description` | string   | Brief summary shown in project cards and metadata |
| `publishedAt` | string   | Publication date in `YYYY-MM-DD` format           |
| `tags`        | string[] | Array of technology/category tags                 |

## Optional Fields

| Field       | Type    | Default | Description                             |
| ----------- | ------- | ------- | --------------------------------------- |
| `updatedAt` | string  | -       | Last update date in `YYYY-MM-DD` format |
| `featured`  | boolean | false   | Whether to highlight this project       |
| `image`     | string  | -       | Path to a cover image                   |

## Example Frontmatter

```yaml
---
title: Project Name
description: A brief description of what this project does.
publishedAt: 2024-01-15
updatedAt: 2024-02-20
tags:
  - React
  - TypeScript
  - Next.js
featured: true
image: /images/projects/project-name.png
---
```

## Notes

- Projects are sorted by `publishedAt` date (newest first)
- The filename (without `.mdx`) becomes the URL slug
- Tags are displayed as badges on the project detail page
