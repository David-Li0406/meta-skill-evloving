---
name: Video Reels & Stories
description: Short-form video content like TikTok/Reels and ephemeral stories
---

# Video Reels & Stories Skill

## Overview
Build short-form video feeds (Reels) and ephemeral 24-hour stories.

## Reels System

### Database
```sql
CREATE TABLE reels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID REFERENCES auth.users(id),
  video_url TEXT NOT NULL,
  thumbnail_url TEXT,
  caption TEXT,
  hashtags TEXT[],
  likes_count INTEGER DEFAULT 0,
  comments_count INTEGER DEFAULT 0,
  views_count INTEGER DEFAULT 0,
  duration_seconds INTEGER,
  is_featured BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Reel Player Component
```jsx
function ReelPlayer({ reel, isActive }) {
  const videoRef = useRef();
  
  useEffect(() => {
    if (isActive) {
      videoRef.current.play();
    } else {
      videoRef.current.pause();
    }
  }, [isActive]);
  
  return (
    <div className="reel-container">
      <video
        ref={videoRef}
        src={reel.video_url}
        loop
        muted={!isActive}
        playsInline
        className="reel-video"
      />
      <ReelOverlay reel={reel} />
      <ReelSidebar 
        likes={reel.likes_count} 
        comments={reel.comments_count} 
      />
    </div>
  );
}
```

### Swipeable Feed
```jsx
import { useSwipeable } from 'react-swipeable';

function ReelsFeed({ reels }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  
  const handlers = useSwipeable({
    onSwipedUp: () => setCurrentIndex(i => Math.min(i + 1, reels.length - 1)),
    onSwipedDown: () => setCurrentIndex(i => Math.max(i - 1, 0)),
    preventScrollOnSwipe: true
  });
  
  return (
    <div {...handlers} className="reels-feed">
      {reels.map((reel, index) => (
        <ReelPlayer 
          key={reel.id} 
          reel={reel} 
          isActive={index === currentIndex}
        />
      ))}
    </div>
  );
}
```

## Stories System

### Database
```sql
CREATE TABLE stories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID REFERENCES auth.users(id),
  media_url TEXT NOT NULL,
  media_type TEXT DEFAULT 'image', -- 'image', 'video'
  duration_seconds INTEGER DEFAULT 5,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '24 hours'
);

CREATE TABLE story_views (
  story_id UUID REFERENCES stories(id),
  viewer_id UUID REFERENCES auth.users(id),
  viewed_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (story_id, viewer_id)
);
```

### Stories Bar Component
```jsx
function StoriesBar({ stories, onStoryClick }) {
  const groupedByUser = groupStoriesByUser(stories);
  
  return (
    <div className="stories-bar">
      {groupedByUser.map(userStories => (
        <StoryAvatar
          key={userStories.userId}
          user={userStories.user}
          hasUnviewed={userStories.hasUnviewed}
          onClick={() => onStoryClick(userStories)}
        />
      ))}
    </div>
  );
}
```

### Story Viewer
```jsx
function StoryViewer({ stories, onClose }) {
  const [index, setIndex] = useState(0);
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          if (index < stories.length - 1) {
            setIndex(i => i + 1);
            return 0;
          } else {
            onClose();
            return 100;
          }
        }
        return p + (100 / (stories[index].duration_seconds * 10));
      });
    }, 100);
    
    return () => clearInterval(timer);
  }, [index, stories]);
  
  return (
    <div className="story-viewer">
      <StoryProgressBars stories={stories} current={index} progress={progress} />
      <StoryMedia story={stories[index]} />
      <StoryHeader user={stories[index].author} onClose={onClose} />
    </div>
  );
}
```

## Components
- `ReelsFeed.jsx` - Full-screen vertical scroll
- `ReelPlayer.jsx` - Video player with controls
- `ReelSidebar.jsx` - Like/comment/share buttons
- `StoriesBar.jsx` - Horizontal story avatars
- `StoryViewer.jsx` - Full-screen story player
- `CreateStory.jsx` - Capture/upload story
