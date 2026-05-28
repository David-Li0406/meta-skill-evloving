---
name: add-service-to-readme
description: Adds new services to the README.md list in alphabetical order
version: 1.0.0
---

# Add Service to README.md List

This skill assists in adding new services to the README.md file's services list in the correct alphabetical position.

## Instructions

When you are asked to add a service to the README.md list, follow these steps:

1. **Identify the service**: Determine the service name from the git status or provided context
2. **Check if already exists**: Search the README.md file to see if the service is already listed
3. **Get service description**: Read the service's README.md file to extract the description
4. **Determine status**: Check if the service should have a status marker ("在用" for active services, empty for inactive)
5. **Find insertion point**: Locate the correct alphabetical position in the services table
6. **Add to list**: Insert the service entry in the format: `| [status] | [service](./service/) | [description] |`
7. **Verify**: Confirm the service was added in the correct position

## Format

The service entry should follow this format:
```
| [status] | [service_name](./service_name/) | [description] |
```

Where:
- `[status]` is "在用" for active services, or empty for inactive services
- `[service_name]` is the actual service directory name
- `[description]` is the service description from the service's README.md

## Examples

**Example 1:**
- Input: Add cloudflared service
- Output: `| | [cloudflared](./cloudflared/) | Cloudflare 隧道客户端。将 Cloudflare 网络的流量代理到你的起源节点。|`

**Example 2:**
- Input: Add a new active service called "new-service"
- Output: `| 在用 | [new-service](./new-service/) | [description from service README] |`

## Usage

Use this skill when:
- New services are added to the repository (indicated by new directories with compose.yaml files)
- Services need to be added to the README.md services list
- The service directory contains a README.md file with proper description

The skill will automatically:
- Read the service's README.md to extract the description
- Determine the correct alphabetical position
- Insert the service entry in the proper format
- Handle both active ("在用") and inactive services
