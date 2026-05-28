# fetch

Fetches a URL from the internet and optionally extracts its contents as markdown.

Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| url | string | Yes | - | URL to fetch (must be valid URI format) |
| max_length | integer | No | 5000 | Maximum number of characters to return (0 < max_length < 1000000) |
| start_index | integer | No | 0 | Start content from this character index, useful if previous fetch was truncated |
| raw | boolean | No | false | Get actual HTML content without markdown conversion |

## Example

```bash
node ./scripts/mcp-caller.mjs call fetch '{"url": "https://example.com"}'
```

Expected output:
```json
{
  "content": [{"type": "text", "text": "# Example Domain\n\nThis domain is for use in illustrative examples..."}]
}
```

## Chunked Reading Example

For long content, use `start_index` to read in chunks:

```bash
# First chunk
node ./scripts/mcp-caller.mjs call fetch '{"url": "https://example.com/long-article", "max_length": 5000}'

# Continue from where it left off
node ./scripts/mcp-caller.mjs call fetch '{"url": "https://example.com/long-article", "max_length": 5000, "start_index": 5000}'
```

## Raw HTML Example

To get the actual HTML without markdown conversion:

```bash
node ./scripts/mcp-caller.mjs call fetch '{"url": "https://example.com", "raw": true}'
```
