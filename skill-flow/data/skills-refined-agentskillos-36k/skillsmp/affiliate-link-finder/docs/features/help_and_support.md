# Help & Support System

This document describes the in-app help and customer support features.

## Overview
Users can access educational content, troubleshooting guides, and contact support without leaving the app.

## Screens

### 1. `HelpAndSupportCenterScreen`
**Location**: `lib/presentation/views/help_and_support_screen.dart`

The main hub for all help resources.

**Sections:**
- **📚 FAQ**: Common questions ("How do I reset my password?", "Why isn't my streak updating?").
- **🎓 Tutorials**: Video walkthroughs for key features.
- **🐛 Report a Bug**: In-app bug reporting form.
- **💬 Contact Support**: Email or chat with support team.

**Search:**
Full-text search across all help articles.

### 2. `ArticleDetailScreen`
**Location**: `lib/presentation/views/article_detail_screen.dart`

Displays individual help articles in a reader-friendly format.

**Features:**
- Markdown rendering.
- TL;DR summary at the top (for ADHD-friendly skimming).
- "Was this helpful?" feedback buttons.
- Share button.

**Content Examples:**
- "How to interpret your Insights charts"
- "Understanding Grace Days"
- "Tips for building an effective morning stack"

### 3. `ScienceLibraryUpdateScreen`
**Location**: `lib/presentation/views/science_library_update_screen.dart`

Notifies users when new research articles are added to the Science Hub.

**UI:**
- "New Research Available" banner.
- Preview of new articles.
- Link to full Science Hub.

## Support Channels
**In-App:**
- Bug reports sent to backend (Firebase Cloud Functions).
- Feature requests tracked in Firestore.

**External:**
- Email: support@focusstackapp.com (fictional).
- Community forum link.

## Content Management
Help articles are stored in Firestore and can be updated remotely without app updates.

**Structure:**
```json
{
  "id": "reset-password",
  "title": "How to Reset Your Password",
  "tldr": "Use the 'Forgot Password' link on the login screen.",
  "body": "...",
  "category": "account"
}
```
