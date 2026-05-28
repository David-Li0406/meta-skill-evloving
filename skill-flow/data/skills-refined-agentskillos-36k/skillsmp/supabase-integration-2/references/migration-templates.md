# Supabase 마이그레이션 템플릿

자주 사용되는 마이그레이션 SQL 템플릿 모음입니다.

## 기본 테이블 생성

### 사용자 프로필

```sql
-- supabase/migrations/00001_create_profiles.sql

-- 프로필 테이블
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE,
  full_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  website TEXT,
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- updated_at 자동 갱신
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_profiles_updated
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- 회원가입 시 자동 프로필 생성
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, username, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'username',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable by everyone"
  ON public.profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);

-- 인덱스
CREATE INDEX idx_profiles_username ON public.profiles(username);
```

### 게시물 테이블

```sql
-- supabase/migrations/00002_create_posts.sql

CREATE TABLE public.posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT,
  excerpt TEXT,
  cover_image TEXT,
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
  published_at TIMESTAMPTZ,
  view_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 트리거
CREATE TRIGGER on_posts_updated
  BEFORE UPDATE ON public.posts
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- RLS
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Published posts are viewable by everyone"
  ON public.posts FOR SELECT
  USING (status = 'published' OR auth.uid() = author_id);

CREATE POLICY "Users can create posts"
  ON public.posts FOR INSERT
  WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Users can update own posts"
  ON public.posts FOR UPDATE
  USING (auth.uid() = author_id);

CREATE POLICY "Users can delete own posts"
  ON public.posts FOR DELETE
  USING (auth.uid() = author_id);

-- 인덱스
CREATE INDEX idx_posts_author ON public.posts(author_id);
CREATE INDEX idx_posts_slug ON public.posts(slug);
CREATE INDEX idx_posts_status ON public.posts(status);
CREATE INDEX idx_posts_published_at ON public.posts(published_at DESC);
```

### 댓글 테이블

```sql
-- supabase/migrations/00003_create_comments.sql

CREATE TABLE public.comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES public.posts(id) ON DELETE CASCADE,
  author_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  parent_id UUID REFERENCES public.comments(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  is_edited BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 트리거
CREATE TRIGGER on_comments_updated
  BEFORE UPDATE ON public.comments
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- RLS
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Comments are viewable by everyone"
  ON public.comments FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can create comments"
  ON public.comments FOR INSERT
  WITH CHECK (auth.uid() = author_id);

CREATE POLICY "Users can update own comments"
  ON public.comments FOR UPDATE
  USING (auth.uid() = author_id);

CREATE POLICY "Users can delete own comments"
  ON public.comments FOR DELETE
  USING (auth.uid() = author_id);

-- 인덱스
CREATE INDEX idx_comments_post ON public.comments(post_id);
CREATE INDEX idx_comments_author ON public.comments(author_id);
CREATE INDEX idx_comments_parent ON public.comments(parent_id);
```

### 태그 시스템 (다대다)

```sql
-- supabase/migrations/00004_create_tags.sql

-- 태그 테이블
CREATE TABLE public.tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT UNIQUE NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 게시물-태그 연결 (다대다)
CREATE TABLE public.post_tags (
  post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES public.tags(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (post_id, tag_id)
);

-- RLS
ALTER TABLE public.tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.post_tags ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Tags are viewable by everyone"
  ON public.tags FOR SELECT
  USING (true);

CREATE POLICY "Post tags are viewable by everyone"
  ON public.post_tags FOR SELECT
  USING (true);

CREATE POLICY "Authors can tag own posts"
  ON public.post_tags FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.posts
      WHERE id = post_id AND author_id = auth.uid()
    )
  );

CREATE POLICY "Authors can untag own posts"
  ON public.post_tags FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM public.posts
      WHERE id = post_id AND author_id = auth.uid()
    )
  );

-- 인덱스
CREATE INDEX idx_tags_slug ON public.tags(slug);
CREATE INDEX idx_post_tags_post ON public.post_tags(post_id);
CREATE INDEX idx_post_tags_tag ON public.post_tags(tag_id);
```

### 좋아요/북마크

```sql
-- supabase/migrations/00005_create_likes.sql

-- 좋아요
CREATE TABLE public.likes (
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, post_id)
);

-- 북마크
CREATE TABLE public.bookmarks (
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, post_id)
);

-- RLS
ALTER TABLE public.likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookmarks ENABLE ROW LEVEL SECURITY;

-- 좋아요 정책
CREATE POLICY "Likes are viewable by everyone"
  ON public.likes FOR SELECT
  USING (true);

CREATE POLICY "Users can like posts"
  ON public.likes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can unlike posts"
  ON public.likes FOR DELETE
  USING (auth.uid() = user_id);

-- 북마크 정책
CREATE POLICY "Users can view own bookmarks"
  ON public.bookmarks FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can bookmark posts"
  ON public.bookmarks FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can remove bookmarks"
  ON public.bookmarks FOR DELETE
  USING (auth.uid() = user_id);

-- 인덱스
CREATE INDEX idx_likes_post ON public.likes(post_id);
CREATE INDEX idx_bookmarks_user ON public.bookmarks(user_id);
```

### 알림 시스템

```sql
-- supabase/migrations/00006_create_notifications.sql

CREATE TABLE public.notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('like', 'comment', 'follow', 'mention', 'system')),
  title TEXT NOT NULL,
  body TEXT,
  data JSONB DEFAULT '{}',
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own notifications"
  ON public.notifications FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can mark own notifications as read"
  ON public.notifications FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own notifications"
  ON public.notifications FOR DELETE
  USING (auth.uid() = user_id);

-- 인덱스
CREATE INDEX idx_notifications_user ON public.notifications(user_id);
CREATE INDEX idx_notifications_unread ON public.notifications(user_id, is_read) WHERE NOT is_read;
```

## Storage 버킷 설정

```sql
-- supabase/migrations/00007_create_storage.sql

-- 아바타 버킷
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'avatars',
  'avatars',
  true,
  5242880,  -- 5MB
  ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/webp']
);

-- 포스트 이미지 버킷
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'post-images',
  'post-images',
  true,
  10485760,  -- 10MB
  ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/webp']
);

-- 아바타 Storage RLS
CREATE POLICY "Avatar images are publicly accessible"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload own avatar"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can update own avatar"
  ON storage.objects FOR UPDATE
  USING (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can delete own avatar"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

-- 포스트 이미지 Storage RLS
CREATE POLICY "Post images are publicly accessible"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'post-images');

CREATE POLICY "Users can upload post images"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'post-images' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
```

## 유용한 함수

```sql
-- supabase/migrations/00008_create_functions.sql

-- 슬러그 생성 함수
CREATE OR REPLACE FUNCTION public.generate_slug(title TEXT)
RETURNS TEXT AS $$
BEGIN
  RETURN lower(
    regexp_replace(
      regexp_replace(title, '[^a-zA-Z0-9가-힣\s]', '', 'g'),
      '\s+', '-', 'g'
    )
  ) || '-' || substr(gen_random_uuid()::text, 1, 8);
END;
$$ LANGUAGE plpgsql;

-- 게시물 조회수 증가 함수
CREATE OR REPLACE FUNCTION public.increment_view_count(post_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE public.posts
  SET view_count = view_count + 1
  WHERE id = post_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 사용자 통계 조회 함수
CREATE OR REPLACE FUNCTION public.get_user_stats(user_id UUID)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT json_build_object(
    'post_count', (SELECT COUNT(*) FROM public.posts WHERE author_id = user_id),
    'like_count', (SELECT COUNT(*) FROM public.likes l JOIN public.posts p ON l.post_id = p.id WHERE p.author_id = user_id),
    'comment_count', (SELECT COUNT(*) FROM public.comments WHERE author_id = user_id)
  ) INTO result;
  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 마이그레이션 실행

```bash
# 새 마이그레이션 생성
supabase migration new create_profiles

# 로컬에서 마이그레이션 실행
supabase db reset

# 마이그레이션 상태 확인
supabase migration list

# 원격 DB에 적용
supabase db push
```
