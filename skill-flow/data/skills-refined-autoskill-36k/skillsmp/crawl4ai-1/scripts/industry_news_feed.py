#!/usr/bin/env python3
"""
Industry News Feed Scraper for Pitchey Platform
Aggregates entertainment industry news from multiple sources
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# News source configurations
NEWS_SOURCES = {
    'variety': {
        'url': 'https://variety.com/v/film/',
        'schema': {
            'name': 'articles',
            'baseSelector': 'article.c-card',
            'fields': [
                {'name': 'title', 'selector': 'h3.c-title', 'type': 'text'},
                {'name': 'excerpt', 'selector': '.c-card__excerpt', 'type': 'text'},
                {'name': 'date', 'selector': 'time', 'type': 'attribute', 'attribute': 'datetime'},
                {'name': 'link', 'selector': 'a.c-title__link', 'type': 'attribute', 'attribute': 'href'},
                {'name': 'image', 'selector': 'img', 'type': 'attribute', 'attribute': 'src'},
                {'name': 'category', 'selector': '.c-card__kicker', 'type': 'text'}
            ]
        }
    },
    'hollywood_reporter': {
        'url': 'https://www.hollywoodreporter.com/c/business/business-news/',
        'schema': {
            'name': 'articles',
            'baseSelector': 'article.lrv-u-flex',
            'fields': [
                {'name': 'title', 'selector': 'h3', 'type': 'text'},
                {'name': 'excerpt', 'selector': 'p.a-font-primary-regular-s', 'type': 'text'},
                {'name': 'date', 'selector': 'time', 'type': 'text'},
                {'name': 'link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
                {'name': 'author', 'selector': '.c-tagline__author', 'type': 'text'}
            ]
        }
    },
    'deadline': {
        'url': 'https://deadline.com/v/film/',
        'schema': {
            'name': 'articles',
            'baseSelector': 'article',
            'fields': [
                {'name': 'title', 'selector': 'h2', 'type': 'text'},
                {'name': 'excerpt', 'selector': '.excerpt', 'type': 'text'},
                {'name': 'date', 'selector': 'time', 'type': 'text'},
                {'name': 'link', 'selector': 'h2 a', 'type': 'attribute', 'attribute': 'href'}
            ]
        }
    }
}

class IndustryNewsFeed:
    def __init__(self, cache_dir: str = './cache', output_dir: str = './output'):
        self.cache_dir = Path(cache_dir)
        self.output_dir = Path(output_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Browser configuration for stealth crawling
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
    async def fetch_news_from_source(self, source_name: str, source_config: dict) -> List[Dict]:
        """Fetch news from a single source"""
        print(f"📰 Fetching news from {source_name}...")
        
        extraction_strategy = JsonCssExtractionStrategy(
            schema=source_config['schema'],
            verbose=False
        )
        
        # Use content filtering for relevance
        content_filter = BM25ContentFilter(
            user_query="film movie streaming production investment acquisition deal",
            bm25_threshold=0.5
        )
        
        md_generator = DefaultMarkdownGenerator(content_filter=content_filter)
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            markdown_generator=md_generator,
            cache_mode=CacheMode.ENABLED,  # Cache for development
            page_timeout=30000,
            wait_for="css:article",
            remove_overlay_elements=True
        )
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(
                    url=source_config['url'],
                    config=crawler_config
                )
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    articles = data.get('articles', [])
                    
                    # Enhance with source and timestamp
                    for article in articles:
                        article['source'] = source_name
                        article['fetched_at'] = datetime.now().isoformat()
                        article['relevance_score'] = self._calculate_relevance(article)
                    
                    print(f"   ✅ Found {len(articles)} articles from {source_name}")
                    return articles
                else:
                    print(f"   ⚠️ Failed to extract from {source_name}")
                    return []
                    
        except Exception as e:
            print(f"   ❌ Error fetching from {source_name}: {e}")
            return []
    
    def _calculate_relevance(self, article: Dict) -> float:
        """Calculate relevance score based on keywords"""
        keywords = [
            'streaming', 'netflix', 'disney', 'amazon', 'apple',
            'box office', 'production', 'investment', 'acquisition',
            'deal', 'franchise', 'sequel', 'reboot', 'adaptation',
            'festival', 'cannes', 'sundance', 'oscar', 'award'
        ]
        
        text = f"{article.get('title', '')} {article.get('excerpt', '')}".lower()
        score = sum(1 for keyword in keywords if keyword in text) / len(keywords)
        return min(score * 10, 10.0)  # Scale to 0-10
    
    async def aggregate_all_sources(self) -> List[Dict]:
        """Fetch news from all configured sources"""
        all_articles = []
        
        # Fetch from all sources concurrently
        tasks = []
        for source_name, source_config in NEWS_SOURCES.items():
            tasks.append(self.fetch_news_from_source(source_name, source_config))
        
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        for articles in results:
            all_articles.extend(articles)
        
        # Sort by relevance and date
        all_articles.sort(key=lambda x: (x.get('relevance_score', 0), x.get('date', '')), reverse=True)
        
        return all_articles
    
    async def get_trending_topics(self, articles: List[Dict]) -> Dict:
        """Extract trending topics and themes from articles"""
        topics = {}
        
        # Common themes to track
        theme_keywords = {
            'streaming_wars': ['netflix', 'disney+', 'hbo max', 'paramount+', 'apple tv+'],
            'box_office': ['box office', 'weekend', 'million', 'billion', 'gross'],
            'awards_season': ['oscar', 'emmy', 'golden globe', 'cannes', 'sundance'],
            'franchise': ['sequel', 'franchise', 'universe', 'reboot', 'remake'],
            'indie': ['independent', 'indie', 'a24', 'neon', 'festival'],
            'international': ['foreign', 'international', 'bollywood', 'korean', 'japanese']
        }
        
        for article in articles:
            text = f"{article.get('title', '')} {article.get('excerpt', '')}".lower()
            
            for theme, keywords in theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    if theme not in topics:
                        topics[theme] = {'count': 0, 'articles': []}
                    topics[theme]['count'] += 1
                    topics[theme]['articles'].append(article['title'])
        
        return topics
    
    async def generate_pitch_insights(self, articles: List[Dict]) -> Dict:
        """Generate insights relevant for pitch creators"""
        insights = {
            'hot_genres': [],
            'trending_formats': [],
            'active_buyers': [],
            'investment_trends': [],
            'success_patterns': []
        }
        
        # Analyze articles for patterns
        genre_mentions = {}
        format_mentions = {}
        company_mentions = {}
        
        for article in articles:
            text = f"{article.get('title', '')} {article.get('excerpt', '')}".lower()
            
            # Track genres
            genres = ['horror', 'comedy', 'drama', 'action', 'thriller', 'sci-fi', 'romance']
            for genre in genres:
                if genre in text:
                    genre_mentions[genre] = genre_mentions.get(genre, 0) + 1
            
            # Track formats
            formats = ['limited series', 'miniseries', 'feature film', 'documentary', 'anthology']
            for fmt in formats:
                if fmt in text:
                    format_mentions[fmt] = format_mentions.get(fmt, 0) + 1
            
            # Track companies
            companies = ['netflix', 'amazon', 'apple', 'disney', 'warner', 'universal', 'sony']
            for company in companies:
                if company in text:
                    company_mentions[company] = company_mentions.get(company, 0) + 1
        
        # Compile insights
        insights['hot_genres'] = sorted(genre_mentions.items(), key=lambda x: x[1], reverse=True)[:5]
        insights['trending_formats'] = sorted(format_mentions.items(), key=lambda x: x[1], reverse=True)[:3]
        insights['active_buyers'] = sorted(company_mentions.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return insights
    
    async def save_feed(self, articles: List[Dict], insights: Dict):
        """Save the aggregated feed and insights"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save articles
        articles_file = self.output_dir / f'news_feed_{timestamp}.json'
        with open(articles_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'article_count': len(articles),
                'articles': articles[:50],  # Top 50 articles
                'insights': insights
            }, f, indent=2)
        
        print(f"💾 Saved news feed to {articles_file}")
        
        # Generate markdown summary
        summary_file = self.output_dir / f'news_summary_{timestamp}.md'
        with open(summary_file, 'w') as f:
            f.write(f"# Industry News Summary\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
            
            f.write("## 🔥 Top Stories\n\n")
            for article in articles[:10]:
                f.write(f"### {article.get('title', 'Untitled')}\n")
                f.write(f"*Source: {article.get('source', 'Unknown')} | ")
                f.write(f"Relevance: {article.get('relevance_score', 0):.1f}/10*\n\n")
                f.write(f"{article.get('excerpt', 'No excerpt available.')}\n")
                f.write(f"[Read more]({article.get('link', '#')})\n\n---\n\n")
            
            f.write("## 📊 Market Insights\n\n")
            f.write("### Hot Genres\n")
            for genre, count in insights.get('hot_genres', []):
                f.write(f"- **{genre.title()}**: {count} mentions\n")
            
            f.write("\n### Trending Formats\n")
            for fmt, count in insights.get('trending_formats', []):
                f.write(f"- **{fmt.title()}**: {count} mentions\n")
            
            f.write("\n### Active Buyers\n")
            for company, count in insights.get('active_buyers', []):
                f.write(f"- **{company.title()}**: {count} mentions\n")
        
        print(f"📄 Saved summary to {summary_file}")
        
        return articles_file, summary_file
    
    async def create_widget_data(self, articles: List[Dict], max_items: int = 5) -> Dict:
        """Create data structure for frontend widget"""
        widget_data = {
            'timestamp': datetime.now().isoformat(),
            'items': []
        }
        
        for article in articles[:max_items]:
            widget_data['items'].append({
                'id': hash(article.get('title', '')),
                'title': article.get('title', 'Untitled'),
                'excerpt': article.get('excerpt', '')[:150] + '...',
                'source': article.get('source', 'Unknown'),
                'link': article.get('link', '#'),
                'date': article.get('date', ''),
                'relevance': article.get('relevance_score', 0),
                'image': article.get('image', '/placeholder.jpg')
            })
        
        # Save widget data
        widget_file = self.output_dir / 'news_widget.json'
        with open(widget_file, 'w') as f:
            json.dump(widget_data, f, indent=2)
        
        print(f"🔧 Created widget data: {widget_file}")
        return widget_data


async def main():
    """Main execution function"""
    print("🎬 Pitchey Industry News Feed Aggregator")
    print("=" * 50)
    
    feed = IndustryNewsFeed()
    
    # Fetch all news
    articles = await feed.aggregate_all_sources()
    print(f"\n📊 Total articles collected: {len(articles)}")
    
    # Extract trending topics
    trending = await feed.get_trending_topics(articles)
    print(f"\n🔥 Trending topics identified: {len(trending)}")
    
    # Generate pitch insights
    insights = await feed.generate_pitch_insights(articles)
    print("\n💡 Pitch Insights Generated:")
    print(f"   - Hot genres: {len(insights['hot_genres'])}")
    print(f"   - Trending formats: {len(insights['trending_formats'])}")
    print(f"   - Active buyers: {len(insights['active_buyers'])}")
    
    # Save everything
    await feed.save_feed(articles, insights)
    
    # Create widget data
    widget_data = await feed.create_widget_data(articles)
    print(f"\n✨ Widget ready with {len(widget_data['items'])} items")
    
    print("\n✅ News feed aggregation complete!")
    print("   Check ./output/ directory for results")


if __name__ == "__main__":
    asyncio.run(main())