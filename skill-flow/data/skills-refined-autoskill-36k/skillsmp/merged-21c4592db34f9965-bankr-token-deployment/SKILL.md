---
name: bankr-token-deployment
description: Use this skill when deploying, managing, or updating ERC20 tokens via Clanker, including fee claiming and metadata updates.
---

# Token Deployment Capability

Deploy and manage ERC20 tokens using natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Deploy token | `Deploy a token called <name> with symbol <symbol>` |
| Deploy with description | `Deploy token <name> (<symbol>) with description: <description>` |
| Deploy with socials | `Deploy token <name> (<symbol>) with website <url> and Twitter @<handle>` |
| Check fees | `Check my Clanker fees` |
| Claim fees | `Claim all my Clanker fees` |
| Claim for token | `Claim fees for my token <symbol>` |
| Claim legacy fees | `Claim legacy Clanker fees` |
| Update description | `Update description for <symbol>: <new_description>` |
| Update socials | `Update <symbol> Twitter to @<handle>` |
| Update image | `Update logo for <symbol> to <image_url>` |
| Update reward recipient | `Update reward recipient for <symbol> to <address>` |

## Supported Chains

- **Base**: Primary deployment chain, full Clanker support
- **Unichain**: Secondary option

## Rate Limits

| User Type | Daily Limit |
|-----------|-------------|
| Standard Users | 1 token/day |
| Bankr Club Members | 10 tokens/day |

## Common Issues

| Issue | Resolution |
|-------|------------|
| Rate limit reached | Wait 24 hours or upgrade |
| Name taken | Choose a different name |
| Symbol exists | Use a unique symbol |
| Image upload failed | Check format/size |

## Best Practices

- Choose a unique, memorable name and symbol.
- Add description and social links immediately.
- Upload a quality logo.
- Claim fees regularly.

## Usage

```typescript
import { execute } from "./bankr-client";

// Deploy token
await execute("Deploy a token called MyToken with symbol MTK");

// With socials
await execute("Deploy token MyToken (MTK) with website https://mytoken.xyz and Twitter @mytoken");

// Check and claim fees
await execute("Check my Clanker fees");
await execute("Claim all my Clanker fees");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-token-trading` - Trade deployed tokens