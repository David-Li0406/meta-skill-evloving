---
name: posting-social-media
description: Use this skill when you need to automate posting content to social media platforms like Instagram and Facebook using the Meta Graph API.
---

# Social Media Poster Skill

Automated posting to Instagram and Facebook via Meta Graph API.

## Quick Start

```bash
# Post to Instagram with image
python scripts/run.py --post "Caption here" --image "https://example.com/image.jpg" --hashtags "business,automation"

# Post to Facebook with link
python scripts/run.py --post "Check this out!" --link "https://example.com"

# Get insights for the last 7 days
python scripts/run.py --insights --days 7

# Verify setup
python scripts/verify.py
```

## Setup

### 1. Requirements

- Instagram Business Account (connected to Facebook Page)
- Facebook Page with Admin access

### 2. Get Credentials

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an App
3. Add "Instagram" and "Pages" products
4. Generate access token with permissions:
   - For Instagram: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`
   - For Facebook: `pages_manage_posts`, `pages_read_engagement`
5. Get your Instagram Business Account ID and Facebook Page ID

### 3. Configure Environment

Add to `.env`:
```
META_ACCESS_TOKEN=your_access_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id_here
FACEBOOK_PAGE_ID=your_page_id_here
GRAPH_API_VERSION=v18.0
```

## Features

### Posting
- Image posts with captions for Instagram
- Text posts with optional links for Facebook
- Hashtag optimization for Instagram (up to 30)
- Approval workflow (default)
- Rate limiting (25 posts/day, 5/hour)

### Analytics
- Engagement metrics for both platforms
- Reach and impressions
- Follower growth for Instagram
- Page impressions and post performance for Facebook

## Approval Workflow

Posts create files in `Vault/Pending_Approval/`:
- Review caption and image for Instagram
- Review and edit content for Facebook
- Move to `Vault/Approved/` to publish
- Or delete to reject

## Rate Limits

- **Daily:** 25 posts
- **Hourly:** 5 posts

## Verification

Run: `python scripts/verify.py`

Expected: `✓ posting-social-media valid`

## References

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Meta Graph API Docs](https://developers.facebook.com/docs/graph-api)
- [Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
- [Pages API](https://developers.facebook.com/docs/pages/overview)