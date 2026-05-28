# Polis CLI Command Reference

Quick reference for polis CLI commands with `--json` mode.

## Publishing Commands

### `polis post <file>`
Sign and publish a new post or comment.

```bash
./cli/bin/polis --json post posts/my-draft.md
```

### `polis post -` (stdin)
Publish content piped from stdin.

```bash
echo "# My Post" | ./cli/bin/polis --json post - --filename my-post.md --title "My Post"
```

Options:
- `--filename <name>` - Output filename (default: stdin-TIMESTAMP.md)
- `--title <title>` - Override title extraction

### `polis republish <file>`
Update an already-published file (creates new version).

```bash
./cli/bin/polis --json republish posts/20260106/my-post.md
```

## Comment Commands

### `polis comment <file> [url]`
Create a comment in reply to a post or another comment.

```bash
# From file
./cli/bin/polis --json comment my-reply.md https://alice.com/posts/hello.md

# From stdin
echo "Great post!" | ./cli/bin/polis --json comment - https://alice.com/posts/hello.md --filename reply.md
```

## Preview Command

### `polis preview <url>`
Preview content at a URL with signature verification.

```bash
./cli/bin/polis --json preview https://alice.com/posts/hello.md
```

## Blessing Commands

### `polis blessing sync`
Sync auto-blessed comments from discovery service.

```bash
./cli/bin/polis --json blessing sync
```

### `polis blessing requests`
List pending blessing requests for your posts.

```bash
./cli/bin/polis --json blessing requests
```

### `polis blessing grant <hash>`
Approve a pending blessing request. Hash can be short form (e.g., `f4bac5-350fd2`) or full hash.

```bash
./cli/bin/polis --json blessing grant f4bac5-350fd2
```

### `polis blessing deny <hash>`
Deny a pending blessing request. Hash can be short form or full hash.

```bash
./cli/bin/polis --json blessing deny f4bac5-350fd2
```

### `polis blessing beseech <id>`
Re-request blessing for a comment (retry). Looks up request by database ID.

```bash
./cli/bin/polis --json blessing beseech 42
```

## Social Commands

### `polis follow <author-url>`
Follow an author (auto-bless their future comments).

```bash
./cli/bin/polis --json follow https://alice.com

# Announce follow to discovery service (opt-in)
./cli/bin/polis --json follow https://alice.com --announce
```

Options:
- `--announce` - Broadcast follow to discovery service (others can see you follow this author)

### `polis unfollow <author-url>`
Stop following an author and hide their comments.

```bash
./cli/bin/polis --json unfollow https://alice.com

# Announce unfollow to discovery service
./cli/bin/polis --json unfollow https://alice.com --announce
```

Options:
- `--announce` - Broadcast unfollow to discovery service

### `polis discover`
Check followed authors for new content.

```bash
# Check all followed authors
./cli/bin/polis --json discover

# Check a specific author
./cli/bin/polis --json discover --author https://alice.com

# Show items since a specific date
./cli/bin/polis --json discover --since 2026-01-15
```

Options:
- `--author <url>` - Check a specific author only
- `--since <date>` - Show items since date (ignores last_checked)

## Index Commands

### `polis index`
View the content index.

```bash
./cli/bin/polis --json index
```

### `polis rebuild`
Rebuild local indexes and reset state. Automatically regenerates `manifest.json` after any rebuild.

```bash
# Rebuild posts index (public.jsonl)
./cli/bin/polis --json rebuild --posts

# Full rebuild of blessed comments from discovery service
./cli/bin/polis --json rebuild --comments

# Reset notification files
./cli/bin/polis --json rebuild --notifications

# Rebuild all indexes and reset notifications
./cli/bin/polis --json rebuild --all

# Flags are combinable
./cli/bin/polis --json rebuild --posts --comments
```

Options:
- `--posts` - Rebuild public.jsonl from posts and comments on disk
- `--comments` - Full rebuild of blessed-comments.json from discovery service
- `--notifications` - Reset notification files (.polis/notifications.jsonl and notifications-manifest.json)
- `--all` - All of the above

## Render Commands

### `polis render`
Render markdown posts and comments to HTML. Generates `.html` files alongside `.md` files.

```bash
# Render all posts and comments, generate index.html
./cli/bin/polis --json render

# Force re-render all files (ignore timestamps)
./cli/bin/polis --json render --force

# Export default templates for customization
./cli/bin/polis render --init-templates
```

Options:
- `--force` - Re-render all files regardless of timestamps
- `--init-templates` - Create `.polis/templates/` with default templates

Requires: `pandoc` (for markdown to HTML conversion)

**Template Variables:**

Available in all templates:
- `{{site_url}}` - Base URL from config
- `{{site_title}}` - From .well-known/polis
- `{{year}}` - Current year (for copyright)

Post/Comment templates:
- `{{title}}` - Post/comment title
- `{{content}}` - HTML-rendered markdown body
- `{{published}}` - Publication date (ISO format)
- `{{published_human}}` - Human-readable date
- `{{url}}` - Canonical URL
- `{{version}}` - Current version hash
- `{{author_name}}` - From .well-known/polis
- `{{author_url}}` - Site base URL
- `{{signature_short}}` - Truncated signature for display

Comment-specific:
- `{{in_reply_to_url}}` - Parent post/comment URL

Post-specific:
- `{{blessed_comments}}` - HTML-rendered list of blessed comments
- `{{blessed_count}}` - Number of blessed comments

Index template:
- `{{posts_list}}` - Generated HTML list of posts
- `{{comments_list}}` - Generated HTML list of comments
- `{{post_count}}` - Number of posts
- `{{comment_count}}` - Number of comments

**Custom Templates:**

Run `polis render --init-templates` to create `.polis/templates/` with:
- `post.html` - Single post template
- `comment.html` - Single comment template
- `comment-inline.html` - Blessed comment rendering
- `index.html` - Listing page template

Modify these files to customize the HTML output.

## Utility Commands

### `polis init`
Initialize a new polis directory.

```bash
./cli/bin/polis --json init
./cli/bin/polis --json init --site-title "My Blog"
```

**Options:**
- `--site-title <title>` - Set custom site title for branding
- `--posts-dir <dir>` - Custom posts directory
- `--comments-dir <dir>` - Custom comments directory

### `polis version`
Print CLI version.

```bash
./cli/bin/polis version
```

### `polis rotate-key`
Generate new keypair and re-sign all content.

```bash
./cli/bin/polis --json rotate-key
```

Use when: key compromise, routine security hygiene, or before transferring device access.

Options:
- `--delete-old-key` - Delete old keypair instead of archiving it

Old keypair is archived at `.polis/keys/id_ed25519.old` unless `--delete-old-key` is specified.

### `polis migrate <new-domain>`
Migrate all content to a new domain (re-signs files, updates database).

```bash
./cli/bin/polis --json migrate newdomain.com
```

Auto-detects current domain from published files. Updates all URLs, re-signs content, and updates discovery service database (preserves blessing status).

### `polis notifications`
View and manage notifications about activity on your site and from followed authors.

```bash
# List unread notifications (default)
./cli/bin/polis --json notifications

# List all notifications
./cli/bin/polis --json notifications list --all

# Filter by type
./cli/bin/polis --json notifications list --type version_available,new_follower
```

**Notification types:**
- `version_available` - New CLI version released
- `version_pending` - CLI upgraded but metadata needs rebuild
- `new_follower` - Someone you don't follow followed you
- `new_post` - Followed author published a new post
- `blessing_changed` - Your comment was blessed/unblessed

### `polis notifications read <id>`
Mark a notification as read.

```bash
./cli/bin/polis --json notifications read notif_1737388800_abc123

# Mark all as read
./cli/bin/polis --json notifications read --all
```

### `polis notifications dismiss <id>`
Dismiss a notification without marking as read.

```bash
./cli/bin/polis --json notifications dismiss notif_1737388800_abc123

# Dismiss old notifications
./cli/bin/polis --json notifications dismiss --older-than 30d
```

### `polis notifications sync`
Sync notifications from the discovery service.

```bash
# Fetch new notifications
./cli/bin/polis --json notifications sync

# Reset watermark and do full re-sync
./cli/bin/polis --json notifications sync --reset
```

### `polis notifications config`
Configure notification preferences.

```bash
# Show current config
./cli/bin/polis --json notifications config

# Set poll interval
./cli/bin/polis notifications config --poll-interval 30m

# Enable/disable notification types
./cli/bin/polis notifications config --enable new_post
./cli/bin/polis notifications config --disable version_available

# Mute/unmute specific domains
./cli/bin/polis notifications config --mute spam.com
./cli/bin/polis notifications config --unmute spam.com
```

**Local storage:**
- `.polis/notifications.jsonl` - Notification log
- `.polis/notifications-manifest.json` - Preferences and sync state

### `polis migrations apply`
Interactively apply discovered domain migrations to local files.

```bash
./cli/bin/polis migrations apply
```

For each migration:
- Verifies public key continuity (same owner controls new domain)
- Shows affected local files
- Prompts for confirmation
- Updates following.json, blessed-comments.json, and comment frontmatter

### `polis extract <file> <hash>`
Reconstruct a specific version from history.

```bash
./cli/bin/polis extract posts/20260106/my-post.md sha256:abc123...
```

### `polis about`
Show comprehensive site information: URL, versions, keys, discovery status.

```bash
./cli/bin/polis --json about
```

Displays:
- Site info (URL, title)
- Versions (CLI, manifest, following.json, blessed-comments.json)
- Keys (status, fingerprint, public key path)
- Discovery (service URL, registration status)

### `polis register`
Register your site with the discovery service (makes content discoverable).

```bash
./cli/bin/polis --json register
```

Required for:
- Receiving blessing requests from others
- Being discoverable by other polis users
- Follow announcements

### `polis unregister`
Unregister your site from the discovery service (hard delete).

```bash
# Requires confirmation
./cli/bin/polis --json unregister

# Skip confirmation
./cli/bin/polis --json unregister --force
```

Options:
- `--force` - Skip confirmation prompt

### `polis clone <url>`
Clone a remote polis site for local analysis or backup.

```bash
# Clone to auto-named directory
./cli/bin/polis --json clone https://alice.com

# Clone to specific directory
./cli/bin/polis --json clone https://alice.com ./alice-backup

# Force full re-download (ignore cached state)
./cli/bin/polis --json clone https://alice.com --full

# Only download new/changed content (incremental)
./cli/bin/polis --json clone https://alice.com --diff
```

Options:
- `--full` - Re-download all content (ignore cached state)
- `--diff` - Only download new/changed content (default if previously cloned)

### `polis snippet <file>`
Publish a reusable template snippet.

```bash
./cli/bin/polis --json snippet snippets/about.md

# From stdin
echo "About text here" | ./cli/bin/polis --json snippet - --filename about.md --title "About"
```

Options:
- `--filename <name>` - Output filename (for stdin)
- `--title <title>` - Override title extraction
