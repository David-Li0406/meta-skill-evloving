---
name: deployment-guide
description: SiteGround deployment setup including SSH keys and GitHub secrets. Use when user wants to deploy, go live, publish, or set up hosting.
allowed-tools: Read, Bash, AskUserQuestion
---

# Deployment Guide

Walk users through deploying their website to SiteGround hosting.

## Prerequisites Check

Before starting, verify the user has:

1. **GitHub repository** - Code pushed to GitHub
2. **SiteGround account** - With SSH access enabled
3. **Domain configured** - Domain pointing to SiteGround

Ask: "Do you have a SiteGround account with SSH access enabled?"

---

## Step 1: SSH Key Generation

Guide the user to generate an SSH key pair for deployment:

```bash
# Generate key (no passphrase for automated deployment)
ssh-keygen -t rsa -b 4096 -f ~/.ssh/siteground_deploy -N ""
```

After running:

```bash
# View public key (add to SiteGround)
cat ~/.ssh/siteground_deploy.pub

# View private key (add to GitHub secrets)
cat ~/.ssh/siteground_deploy
```

---

## Step 2: SiteGround Configuration

Guide the user through SiteGround's interface:

1. Log in to **SiteGround Site Tools**
2. Navigate to **Devs** → **SSH Keys Manager**
3. Click **Import** and paste the public key
4. Name it (e.g., "GitHub Deploy")
5. Click **Manage SSH Access** to get connection details:
   - **Host**: Server hostname
   - **Port**: Usually `18765` (SiteGround's non-standard port)
   - **Username**: SSH username

Ask: "Can you share your SSH host, port, and username from SiteGround?"

---

## Step 3: GitHub Secrets Configuration

Guide the user to add repository secrets:

1. Go to GitHub repository → **Settings**
2. Navigate to **Secrets and variables** → **Actions**
3. Add these **Repository secrets**:

| Secret Name | Value |
|-------------|-------|
| `SSH_PRIVATE_KEY` | Contents of `~/.ssh/siteground_deploy` (private key) |
| `SSH_HOST` | SiteGround server hostname |
| `SSH_PORT` | `18765` (or provided port) |
| `SSH_USERNAME` | SiteGround SSH username |

---

## Step 4: Verify Domain Configuration

Check that `.github/workflows/deploy.yml` has the correct domain:

```yaml
env:
  DOMAIN: your-domain.com  # Should match user's domain
```

If not set, update it.

---

## Step 5: Test Deployment

Guide the user through the first deployment:

1. Commit and push changes to `main` branch:
   ```bash
   git add -A
   git commit -m "Configure deployment"
   git push origin main
   ```

2. Monitor deployment:
   ```bash
   gh run list --limit 1
   ```

3. Verify the website at `https://{domain}`

---

## Troubleshooting

### SSH Connection Failed
- Verify SSH key is correctly added to SiteGround
- Check port number (SiteGround uses `18765`, not `22`)
- Confirm hostname is correct

### Permission Denied
- Verify SSH username matches SiteGround account
- Check public key is active in SiteGround

### Files Not Updating
- Check rsync exclude patterns in `deploy.yml`
- Verify `DOMAIN` matches your setup
- Ensure deployment path exists on SiteGround

---

## Success Message

Once deployment succeeds:

> Your website is live at https://{domain}
>
> Future changes will deploy automatically when you push to the `main` branch.
