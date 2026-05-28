# Community & Social Features

This document covers the social and peer support aspects of the app.

## Overview
ADHD management is easier with community support. The app includes several social features for sharing, accountability, and learning from others.

## Screens

### 1. `CommunityScreen`
**Location**: `lib/presentation/views/community_screen.dart`

A feed-style screen showing:
- Popular supplement stacks from other users.
- Success stories.
- Questions & answers.

**Current State:**
UI is fully implemented with mock data. Backend integration requires Firebase Firestore community collection.

**Planned Features:**
- Upvote/downvote system.
- Comment threads.
- Report inappropriate content.

### 2. `FocusBuddiesScreen`
**Location**: `lib/presentation/views/focus_buddies_screen.dart`

A "body doubling" feature where users can match with accountability partners.

**How It Works:**
1. User sets a daily check-in time (e.g., 9 AM).
2. Matched with another user with a similar goal.
3. Both get a notification: "Did you take your morning stack?"
4. Visual confirmation when both complete.

**Psychology:**
ADHD research shows "body doubling" (doing tasks alongside someone) improves completion rates.

### 3. `ReferFriendScreen`
**Location**: `lib/presentation/views/refer_friend_screen.dart`

Referral system with built-in affiliate rewards.

**Features:**
- Personal referral code.
- Share via native share sheet (WhatsApp, SMS, Email).
- Tracks # of referrals.
- (Future) Unlock premium features after X referrals.

**Messaging:**
"Help a friend optimize their ADHD routine. You both get 1 month free!"

### 4. `ScienceHubScreen`
**Location**: `lib/presentation/views/science_hub_screen.dart`

A curated library of research articles about ADHD, supplements, and neuroscience.

**Content Types:**
- 📄 Research summaries (plain language).
- 🎥 Video explainers.
- 📊 Infographics.

**Example Topics:**
- "Why Vitamin C reduces Adderall effectiveness"
- "Omega-3 for ADHD: What the studies say"
- "L-Theanine + Caffeine synergy"

## Social Gamification
The community features integrate with the gamification system:
- Sharing a milestone unlocks badges.
- Helping others in the Q&A forum earns "Helper" status.
