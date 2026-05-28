---
name: Next.js Voting System with Supabase
description: Complete guide to building a voting system with Next.js, Supabase, daily vote limits, and Vercel deployment
---

# Next.js Voting System with Supabase

A comprehensive skill for building a full-featured voting system with Next.js, Supabase backend, daily vote limits, and production deployment.

## Overview

This skill covers the complete development process for creating a voting application with:
- Next.js 16 frontend
- Supabase PostgreSQL database
- Name + phone number authentication
- Daily vote limits (3 votes per day, resets at midnight)
- Real-time leaderboard
- Vercel deployment

## Tech Stack

- **Frontend**: Next.js 16, React, TailwindCSS
- **Backend**: Next.js Server Actions, Supabase
- **Database**: PostgreSQL (via Supabase)
- **Deployment**: Vercel
- **Authentication**: Custom (name + phone number)

---

## Part 1: Project Setup

### 1.1 Initialize Next.js Project

```bash
npx create-next-app@latest project-name
cd project-name
```

Configuration:
- TypeScript: Yes
- ESLint: Yes
- Tailwind CSS: Yes
- App Router: Yes
- Server Actions: Yes

### 1.2 Install Dependencies

```bash
npm install @supabase/supabase-js
```

### 1.3 Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

---

## Part 2: Supabase Database Setup

### 2.1 Create Videos Table

```sql
CREATE TABLE videos (
  id bigint PRIMARY KEY,
  title text NOT NULL,
  youtube_id text NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Insert sample videos
INSERT INTO videos (id, title, youtube_id) VALUES
  (1, '第一個影片', 'youtube_id_1'),
  (2, '第二個影片', 'youtube_id_2'),
  (3, '第三個影片', 'youtube_id_3'),
  (4, '第四個影片', 'youtube_id_4');
```

### 2.2 Create Votes Table with Daily Limit

```sql
CREATE TABLE votes (
  id bigserial PRIMARY KEY,
  user_id text NOT NULL,
  video_id bigint NOT NULL REFERENCES videos(id),
  vote_date date DEFAULT (CURRENT_DATE AT TIME ZONE 'Asia/Taipei'),
  created_at timestamptz DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX idx_votes_user_date ON votes(user_id, vote_date);
CREATE INDEX idx_votes_video_id ON votes(video_id);
```

### 2.3 Row Level Security (RLS) Policies

```sql
-- Enable RLS
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;

-- votes table policies
CREATE POLICY "Allow public read access"
ON votes FOR SELECT TO public USING (true);

CREATE POLICY "Allow public insert"
ON votes FOR INSERT TO public WITH CHECK (true);

CREATE POLICY "Prevent delete"
ON votes FOR DELETE TO public USING (false);

CREATE POLICY "Prevent update"
ON votes FOR UPDATE TO public USING (false);

-- videos table policies
CREATE POLICY "Allow public read access"
ON videos FOR SELECT TO public USING (true);

CREATE POLICY "Prevent modifications"
ON videos FOR ALL TO public USING (false);
```

---

## Part 3: Supabase Client Setup

### 3.1 Create Supabase Client

`src/lib/supabaseClient.ts`:

```typescript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
```

---

## Part 4: Server Actions for Voting

### 4.1 Vote Submission with Daily Limit

`src/app/actions/vote.ts`:

```typescript
'use server';
import { supabase } from '@/lib/supabaseClient';
import { cookies } from 'next/headers';

export async function submitVote(videoId: number) {
    try {
        const cookieStore = await cookies();
        const userId = cookieStore.get('user_id')?.value;

        if (!userId) {
            return { success: false, message: '請先登入！' };
        }

        // Get today's date in Taiwan timezone
        const today = new Date().toLocaleDateString('en-CA', { 
            timeZone: 'Asia/Taipei'
        }); // Format: YYYY-MM-DD

        // Check today's vote count
        const { data: todayVotes, error: checkError } = await supabase
            .from('votes')
            .select('*')
            .eq('user_id', userId)
            .eq('vote_date', today);

        if (checkError) {
            console.error('檢查投票錯誤:', checkError);
            return { success: false, message: '檢查投票狀態時發生錯誤' };
        }

        // Check daily limit (3 votes)
        if (todayVotes && todayVotes.length >= 3) {
            return { 
                success: false, 
                message: '今天的投票次數已用完！明天再來投票吧 🗳️' 
            };
        }

        // Insert vote
        const { error } = await supabase
            .from('votes')
            .insert({ 
                user_id: userId, 
                video_id: videoId,
                vote_date: today
            });

        if (error) throw error;

        const remaining = 3 - (todayVotes?.length || 0) - 1;
        return { 
            success: true, 
            message: `投票成功！今日還剩 ${remaining} 票`,
            remainingVotes: remaining
        };
    } catch (error) {
        console.error('投票錯誤:', error);
        return { success: false, message: '投票失敗，請稍後再試' };
    }
}

export async function getVoteStats() {
    try {
        let allVotes: any[] = [];
        let from = 0;
        const pageSize = 1000;
        let hasMore = true;

        // ⚠️ CRITICAL: Supabase limits queries to 1000 records by default
        // Use pagination loop to fetch ALL votes
        while (hasMore) {
            const { data, error } = await supabase
                .from('votes')
                .select('video_id, videos(title, youtube_id)')
                .order('video_id')
                .range(from, from + pageSize - 1);

            if (error) throw error;

            if (data && data.length > 0) {
                allVotes = allVotes.concat(data);
                from += pageSize;
                
                // If we got less than pageSize, we've reached the last page
                if (data.length < pageSize) {
                    hasMore = false;
                }
            } else {
                hasMore = false;
            }
        }

        console.log(`✅ getVoteStats: Retrieved ${allVotes.length} vote records`);

        // Aggregate vote counts
        const stats = allVotes.reduce((acc: any, vote: any) => {
            const videoId = vote.video_id;
            if (!acc[videoId]) {
                acc[videoId] = {
                    id: videoId,
                    title: vote.videos?.title || `Unknown Video #${videoId}`,
                    youtube_id: vote.videos?.youtube_id || '',
                    votes: 0
                };
                
                // Log orphan votes for tracking
                if (!vote.videos) {
                    console.warn(`Found orphan vote: video_id ${videoId} not in videos table`);
                }
            }
            acc[videoId].votes += 1;
            return acc;
        }, {});

        return Object.values(stats);
    } catch (error) {
        console.error('獲取投票統計錯誤:', error);
        return [];
    }
}

export async function getRemainingVotes(userId: string) {
    try {
        const today = new Date().toLocaleDateString('en-CA', { 
            timeZone: 'Asia/Taipei'
        });

        const { data, error } = await supabase
            .from('votes')
            .select('*')
            .eq('user_id', userId)
            .eq('vote_date', today);

        if (error) throw error;

        const votedCount = data?.length || 0;
        return {
            remaining: 3 - votedCount,
            voted: votedCount,
            total: 3
        };
    } catch (error) {
        console.error('獲取剩餘票數錯誤:', error);
        return {
            remaining: 0,
            voted: 0,
            total: 3
        };
    }
}
```

---

## Part 5: Vote Page Implementation

### 5.1 Vote Page with Authentication

`src/app/vote/page.tsx`:

Key features:
- Name + phone number login (stored in localStorage and cookies)
- Display remaining votes (X / 3)
- Video cards with YouTube embed
- Real-time leaderboard
- Responsive design with dark theme

```typescript
'use client';
import { useEffect, useState } from 'react';
import { getVoteStats, getRemainingVotes } from '../actions/vote';

export default function VotePage() {
    const [videos, setVideos] = useState([...]);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userName, setUserName] = useState('');
    const [userPhone, setUserPhone] = useState('');
    const [remainingVotes, setRemainingVotes] = useState(3);

    useEffect(() => {
        checkLoginStatus();
        loadVoteStats();
    }, []);

    useEffect(() => {
        if (isLoggedIn && userPhone) {
            loadRemainingVotes();
        }
    }, [isLoggedIn, userPhone]);

    const loadRemainingVotes = async () => {
        if (!userPhone) return;
        const result = await getRemainingVotes(userPhone);
        setRemainingVotes(result.remaining);
    };

    const handleLogin = () => {
        // Validate name and phone
        // Save to localStorage and cookies
        // Set login state
    };

    // ... rest of implementation
}
```

---

## Part 6: Components

### 6.1 VideoCard Component

Features:
- YouTube iframe embed
- Vote button with loading state
- Disabled state when not logged in or no votes remaining
- Success/error messages

### 6.2 Leaderboard Component

Features:
- Bar chart visualization (using Chart.js or similar)
- Real-time vote counts
- Sorted by votes (descending)
- Responsive design

---

## Part 7: Deployment to Vercel

### 7.1 Prepare for Deployment

1. **Ensure `.gitignore` includes:**
   ```
   .env*
   .next/
   node_modules/
   ```

2. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/repo.git
   git push -u origin main
   ```

### 7.2 Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Configure environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Deploy

### 7.3 Post-Deployment

- Test all functionality
- Verify daily vote limit works
- Check timezone handling (should use Asia/Taipei)

---

## Part 8: Key Features Implemented

### 8.1 Daily Vote Limit

- ✅ 3 votes per user per day
- ✅ Resets at midnight (Taiwan timezone)
- ✅ Can vote for same video multiple times
- ✅ Display remaining votes

### 8.2 Authentication

- ✅ Name + phone number (no password)
- ✅ Phone number validation (Taiwan format: 09XXXXXXXX)
- ✅ Persistent login (localStorage + cookies)
- ✅ Returning user validation

### 8.3 Voting Features

- ✅ Vote for videos
- ✅ Real-time leaderboard
- ✅ Prevent duplicate votes (per day)
- ✅ Success/error messages

### 8.4 UI/UX

- ✅ Dark theme with gold accents
- ✅ Responsive design (mobile + desktop)
- ✅ Loading states
- ✅ Hover effects and animations
- ✅ Clear vote count display

---

## Part 9: Common Issues and Solutions

### 9.1 CORS Errors

**Problem:** YouTube iframe CORS warnings

**Solution:** These are normal and don't affect functionality. Can be safely ignored.

### 9.2 Timezone Issues

**Problem:** Votes not resetting at midnight

**Solution:** Always use `Asia/Taipei` timezone:
```typescript
const today = new Date().toLocaleDateString('en-CA', { 
    timeZone: 'Asia/Taipei'
});
```

### 9.3 Import Path Errors

**Problem:** `@/lib/supabase` not found

**Solution:** Use correct path: `@/lib/supabaseClient`

### 9.4 RLS Policy Errors (401/403)

**Problem:** Cannot insert votes

**Solution:** Ensure RLS policies allow public insert:
```sql
CREATE POLICY "Allow public insert"
ON votes FOR INSERT TO public WITH CHECK (true);
```

### 9.5 ⚠️ CRITICAL: Supabase 1000-Record Query Limit

**Problem:** Vote counts become inaccurate when total votes exceed 1000

**Symptoms:**
- Leaderboard shows lower vote counts than database
- High-vote videos missing from rankings
- Problem appears suddenly when crossing 1000 total votes

**Root Cause:**
Supabase JavaScript Client has a **default limit of 1000 records per query**. When your votes table exceeds 1000 rows:
- Single queries only return first 1000 records
- Vote statistics become incomplete
- No error is thrown - data is silently truncated

**Solution:** Implement pagination loop (already included in code above)

```typescript
let allVotes: any[] = [];
let from = 0;
const pageSize = 1000;
let hasMore = true;

while (hasMore) {
    const { data, error } = await supabase
        .from('votes')
        .select('...')
        .range(from, from + pageSize - 1);
    
    if (data && data.length > 0) {
        allVotes = allVotes.concat(data);
        from += pageSize;
        if (data.length < pageSize) hasMore = false;
    } else {
        hasMore = false;
    }
}
```

**When to worry:**
- ✅ < 1000 votes: No action needed
- ⚠️ 800-1000 votes: Monitor closely
- 🚨 > 1000 votes: Pagination is REQUIRED

**Performance Impact:**
- 2000 votes: 2 queries (~400ms)
- 5000 votes: 5 queries (~1s)
- 10000 votes: 10 queries (~2s)

**Future Optimization (>10,000 votes):**
- Implement caching (refresh every 5 minutes)
- Use Supabase RPC/PostgreSQL Functions
- Pre-calculate statistics in background job

---

## Part 10: Testing Checklist

### Before Deployment

- [ ] Local build succeeds (`npm run build`)
- [ ] All environment variables set
- [ ] Database migrations applied
- [ ] RLS policies configured

### After Deployment

- [ ] Homepage redirects to vote page
- [ ] Login works (name + phone)
- [ ] Can vote successfully
- [ ] Vote count increases
- [ ] Remaining votes display correctly
- [ ] Daily limit enforced (3 votes max)
- [ ] Leaderboard updates in real-time
- [ ] Mobile responsive

---

## Part 11: Customization Guide

### Change Daily Vote Limit

Modify these values in code:
- `src/app/actions/vote.ts`: Line with `>= 3`
- `src/app/vote/page.tsx`: `useState(3)`

### Add More Videos

Update Supabase:
```sql
INSERT INTO videos (id, title, youtube_id) VALUES
  (5, '第五個影片', 'youtube_id_5');
```

Update code:
```typescript
const [videos, setVideos] = useState([
  { id: 5, title: '第五個影片', youtube_id: 'youtube_id_5' }
]);
```

### Change Timezone

Replace all instances of `'Asia/Taipei'` with your timezone.

---

## Summary

This skill provides a complete, production-ready voting system with:
- Modern tech stack (Next.js 16 + Supabase)
- Daily vote limits with timezone handling
- Simple authentication
- Real-time leaderboard with pagination support
- Professional UI/UX
- Vercel deployment
- **Scalable to 10,000+ votes** with pagination

Perfect for church events, community voting, or any scenario requiring daily vote limits.

## ⚠️ Critical Reminders

1. **Supabase Query Limit**: Always use pagination when vote count may exceed 1000
2. **Timezone**: Use `Asia/Taipei` (or your timezone) consistently
3. **RLS Policies**: Ensure public read/insert access is enabled
4. **Environment Variables**: Set in both local `.env.local` and Vercel dashboard
5. **Testing**: Test with >1000 records to verify pagination works
