---
name: News & Content Feed
description: Poker news aggregation, articles, and content discovery
---

# News & Content Feed Skill

## Overview
Aggregate poker news from multiple sources, display articles, and provide content discovery.

## News Sources
| Source | Type | Frequency |
|--------|------|-----------|
| PokerNews | RSS | Hourly |
| Card Player | RSS | Hourly |
| 2+2 Forums | Scrape | Daily |
| Twitter/X | API | Real-time |
| YouTube | API | Hourly |
| WSOP.com | Scrape | Daily |

## Database Schema
```sql
CREATE TABLE news_articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source TEXT NOT NULL,
  source_url TEXT UNIQUE,
  title TEXT NOT NULL,
  summary TEXT,
  content TEXT,
  image_url TEXT,
  author TEXT,
  category TEXT, -- 'tournament', 'strategy', 'player', 'industry'
  published_at TIMESTAMPTZ,
  scraped_at TIMESTAMPTZ DEFAULT NOW(),
  view_count INTEGER DEFAULT 0
);

CREATE INDEX idx_articles_published ON news_articles(published_at DESC);
CREATE INDEX idx_articles_category ON news_articles(category);
```

## RSS Feed Parser
```javascript
import Parser from 'rss-parser';

async function fetchRSSNews(feedUrl, sourceName) {
  const parser = new Parser();
  const feed = await parser.parseURL(feedUrl);
  
  const articles = feed.items.map(item => ({
    source: sourceName,
    source_url: item.link,
    title: item.title,
    summary: item.contentSnippet,
    image_url: extractImageFromContent(item.content),
    published_at: item.pubDate
  }));
  
  // Upsert to avoid duplicates
  await supabase.from('news_articles').upsert(articles, {
    onConflict: 'source_url'
  });
}
```

## News Feed API
```javascript
// pages/api/news/articles.js
export default async function handler(req, res) {
  const { category, page = 0, limit = 20 } = req.query;
  
  let query = supabase
    .from('news_articles')
    .select('*')
    .order('published_at', { ascending: false })
    .range(page * limit, (page + 1) * limit - 1);
  
  if (category) {
    query = query.eq('category', category);
  }
  
  const { data, error } = await query;
  res.json({ articles: data, error });
}
```

## Components
- `NewsFeed.jsx` - Infinite scroll article list
- `ArticleCard.jsx` - Summary card with image
- `ArticleReader.jsx` - Full article view
- `CategoryTabs.jsx` - Category filter
- `TrendingNews.jsx` - Popular articles sidebar

## Cron Job
```javascript
// /api/cron/scrape-news.js
export default async function handler(req, res) {
  const feeds = [
    { url: 'https://pokernews.com/rss.xml', source: 'PokerNews' },
    { url: 'https://cardplayer.com/feed', source: 'CardPlayer' }
  ];
  
  for (const feed of feeds) {
    await fetchRSSNews(feed.url, feed.source);
  }
  
  res.json({ success: true });
}
```
