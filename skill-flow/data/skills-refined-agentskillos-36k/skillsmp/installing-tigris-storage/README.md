# Installing Tigris Storage

This skill helps you set up and configure @tigrisdata/storage in new projects.

## What It Covers

Tigris Storage provides high-performance object storage for multi-cloud environments. This skill guides you through:

- Installing the @tigrisdata/storage package
- Creating Tigris account resources (buckets, access keys)
- Configuring environment variables
- Setting up authentication

## Installation

### Claude Code

```bash
cp -r skills/installing-tigris-storage ~/.claude/skills/
```

### claude.ai

Add the `SKILL.md` file to your project knowledge or paste its contents into the conversation.

## Usage

When you need to set up Tigris Storage in a project, trigger with:

- "Install Tigris Storage"
- "Setup object storage"
- "Configure @tigrisdata/storage"
- "Add Tigris to my project"

## Quick Start

```bash
# Install the package
npm install @tigrisdata/storage

# Set environment variables
TIGRIS_STORAGE_ACCESS_KEY_ID=tid_access_key_id
TIGRIS_STORAGE_SECRET_ACCESS_KEY=tsec_secret_access_key
TIGRIS_STORAGE_BUCKET=bucket_name
```

## Links

- **Sign up**: https://storage.new
- **Console**: https://console.tigris.dev
- **Create bucket**: https://console.tigris.dev/createbucket
- **Access keys**: https://console.tigris.dev/createaccesskey
- **Docs**: https://www.tigrisdata.com/docs

## License

MIT
