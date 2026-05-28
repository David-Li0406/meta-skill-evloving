---
name: Social & Community
description: Build social features including posts, comments, likes, and user interactions
---

# Social & Community Skill

## Overview
Build the social layer (Orb #1) with posts, comments, likes, follows, and community features.

## Database Schema

### social_posts
```sql
CREATE TABLE social_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID REFERENCES auth.users(id),
  content TEXT NOT NULL,
  content_type TEXT DEFAULT 'text', -- 'text', 'image', 'video', 'link'
  media_url TEXT,
  metadata JSONB DEFAULT '{}',
  likes_count INTEGER DEFAULT 0,
  comments_count INTEGER DEFAULT 0,
  shares_count INTEGER DEFAULT 0,
  is_pinned BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### social_likes
```sql
CREATE TABLE social_likes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  post_id UUID REFERENCES social_posts(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, post_id)
);
```

### social_comments
```sql
CREATE TABLE social_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID REFERENCES social_posts(id),
  author_id UUID REFERENCES auth.users(id),
  content TEXT NOT NULL,
  parent_id UUID REFERENCES social_comments(id), -- For replies
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### user_follows
```sql
CREATE TABLE user_follows (
  follower_id UUID REFERENCES auth.users(id),
  following_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (follower_id, following_id)
);
```

## Post Creation
```javascript
async function createPost(userId, content, contentType = 'text', mediaUrl = null) {
  const { data: post, error } = await supabase
    .from('social_posts')
    .insert({
      author_id: userId,
      content,
      content_type: contentType,
      media_url: mediaUrl
    })
    .select()
    .single();
  
  // Award XP for posting
  await supabase.rpc('award_xp', {
    p_user_id: userId,
    p_amount: 10,
    p_source: 'post_created'
  });
  
  return post;
}
```

## Feed Queries
```javascript
// Get personalized feed (following + popular)
async function getFeed(userId, page = 0, limit = 20) {
  const { data: posts } = await supabase
    .from('social_posts')
    .select(`
      *,
      author:profiles!author_id(id, username, avatar_url, full_name),
      likes:social_likes(user_id),
      comments:social_comments(count)
    `)
    .order('created_at', { ascending: false })
    .range(page * limit, (page + 1) * limit - 1);
  
  return posts.map(post => ({
    ...post,
    isLiked: post.likes.some(l => l.user_id === userId),
    commentsCount: post.comments[0]?.count || 0
  }));
}
```

## Like/Unlike
```javascript
async function toggleLike(userId, postId) {
  const { data: existing } = await supabase
    .from('social_likes')
    .select('id')
    .eq('user_id', userId)
    .eq('post_id', postId)
    .single();
  
  if (existing) {
    await supabase.from('social_likes').delete().eq('id', existing.id);
    await supabase.rpc('decrement_likes', { p_post_id: postId });
    return false;
  } else {
    await supabase.from('social_likes').insert({ user_id: userId, post_id: postId });
    await supabase.rpc('increment_likes', { p_post_id: postId });
    return true;
  }
}
```

## Real-time Updates
```javascript
// Subscribe to new posts
supabase.channel('social_feed')
  .on('postgres_changes', { 
    event: 'INSERT', 
    schema: 'public', 
    table: 'social_posts' 
  }, (payload) => {
    addNewPost(payload.new);
  })
  .subscribe();
```

## Components
- `PostComposer.jsx` - Create new posts
- `PostCard.jsx` - Display single post
- `FeedList.jsx` - Infinite scroll feed
- `CommentSection.jsx` - Comments & replies
- `UserProfile.jsx` - Profile with posts
- `FollowButton.jsx` - Follow/unfollow
