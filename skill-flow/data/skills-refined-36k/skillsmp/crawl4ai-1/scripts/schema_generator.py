#!/usr/bin/env python3
"""
Schema Generator for Pitchey Platform
Generates and manages extraction schemas for various data sources
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Optional

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

class SchemaGenerator:
    def __init__(self, schema_dir: str = './schemas'):
        self.schema_dir = Path(schema_dir)
        self.schema_dir.mkdir(exist_ok=True)
        
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080
        )
        
        # Predefined schema templates for common sources
        self.templates = {
            'imdb': self._get_imdb_template(),
            'variety': self._get_variety_template(),
            'boxofficemojo': self._get_boxofficemojo_template(),
            'production_company': self._get_production_company_template()
        }
    
    def _get_imdb_template(self) -> Dict:
        """IMDb schema template"""
        return {
            'search_results': {
                'name': 'movies',
                'baseSelector': '.lister-item, .titleColumn',
                'fields': [
                    {'name': 'title', 'selector': 'h3 a, .titleColumn a', 'type': 'text'},
                    {'name': 'year', 'selector': '.lister-item-year, .secondaryInfo', 'type': 'text'},
                    {'name': 'rating', 'selector': '.ratings-imdb-rating strong, .imdbRating strong', 'type': 'text'},
                    {'name': 'genre', 'selector': '.genre', 'type': 'text'},
                    {'name': 'runtime', 'selector': '.runtime', 'type': 'text'},
                    {'name': 'plot', 'selector': 'p:nth-of-type(2)', 'type': 'text'},
                    {'name': 'director', 'selector': 'p:nth-of-type(3) a:first-child', 'type': 'text'},
                    {'name': 'stars', 'selector': 'p:nth-of-type(3)', 'type': 'text'},
                    {'name': 'gross', 'selector': '.gross', 'type': 'text'},
                    {'name': 'link', 'selector': 'h3 a, .titleColumn a', 'type': 'attribute', 'attribute': 'href'},
                    {'name': 'image', 'selector': '.lister-item-image img', 'type': 'attribute', 'attribute': 'src'}
                ]
            },
            'movie_details': {
                'name': 'details',
                'baseSelector': 'body',
                'fields': [
                    {'name': 'title', 'selector': 'h1', 'type': 'text'},
                    {'name': 'year', 'selector': '.TitleBlockMetaData__ListItemText-sc-12ein40-2:first-child', 'type': 'text'},
                    {'name': 'rating', 'selector': 'span[class*="AggregateRatingButton__RatingScore"]', 'type': 'text'},
                    {'name': 'plot', 'selector': 'span[data-testid="plot-xl"]', 'type': 'text'},
                    {'name': 'genres', 'selector': 'a[href*="/genre/"]', 'type': 'text', 'all': True},
                    {'name': 'budget', 'selector': 'li[data-testid="title-boxoffice-budget"] .ipc-metadata-list-item__content-container', 'type': 'text'},
                    {'name': 'gross_worldwide', 'selector': 'li[data-testid="title-boxoffice-cumulativeworldwidegross"] .ipc-metadata-list-item__content-container', 'type': 'text'},
                    {'name': 'production_companies', 'selector': 'a[href*="/company/"]', 'type': 'text', 'all': True}
                ]
            }
        }
    
    def _get_variety_template(self) -> Dict:
        """Variety news schema template"""
        return {
            'articles': {
                'name': 'articles',
                'baseSelector': 'article, .c-card',
                'fields': [
                    {'name': 'title', 'selector': 'h2, h3, .c-title', 'type': 'text'},
                    {'name': 'excerpt', 'selector': '.c-card__excerpt, .excerpt', 'type': 'text'},
                    {'name': 'author', 'selector': '.c-byline__item a, .author', 'type': 'text'},
                    {'name': 'date', 'selector': 'time', 'type': 'attribute', 'attribute': 'datetime'},
                    {'name': 'category', 'selector': '.c-card__kicker, .category', 'type': 'text'},
                    {'name': 'link', 'selector': 'a.c-title__link, h2 a', 'type': 'attribute', 'attribute': 'href'},
                    {'name': 'image', 'selector': 'img', 'type': 'attribute', 'attribute': 'src'}
                ]
            }
        }
    
    def _get_boxofficemojo_template(self) -> Dict:
        """Box Office Mojo schema template"""
        return {
            'box_office': {
                'name': 'movies',
                'baseSelector': 'tr[id*="row"], .a-section',
                'fields': [
                    {'name': 'rank', 'selector': 'td:first-child', 'type': 'text'},
                    {'name': 'title', 'selector': '.a-text-left a, td:nth-child(2) a', 'type': 'text'},
                    {'name': 'weekend_gross', 'selector': 'td:nth-child(3)', 'type': 'text'},
                    {'name': 'total_gross', 'selector': 'td:nth-child(4)', 'type': 'text'},
                    {'name': 'theaters', 'selector': 'td:nth-child(5)', 'type': 'text'},
                    {'name': 'average_per_theater', 'selector': 'td:nth-child(6)', 'type': 'text'},
                    {'name': 'weeks_in_release', 'selector': 'td:nth-child(7)', 'type': 'text'},
                    {'name': 'distributor', 'selector': 'td:nth-child(8)', 'type': 'text'},
                    {'name': 'link', 'selector': '.a-text-left a, td:nth-child(2) a', 'type': 'attribute', 'attribute': 'href'}
                ]
            }
        }
    
    def _get_production_company_template(self) -> Dict:
        """Production company schema template"""
        return {
            'company_info': {
                'name': 'company',
                'baseSelector': 'body',
                'fields': [
                    {'name': 'name', 'selector': 'h1, .company-name', 'type': 'text'},
                    {'name': 'description', 'selector': '.about, .company-description', 'type': 'text'},
                    {'name': 'founded', 'selector': '.founded, .establishment-date', 'type': 'text'},
                    {'name': 'headquarters', 'selector': '.location, .headquarters', 'type': 'text'},
                    {'name': 'website', 'selector': 'a[href*="http"]', 'type': 'attribute', 'attribute': 'href'},
                    {'name': 'recent_projects', 'selector': '.project, .film-title', 'type': 'text', 'all': True},
                    {'name': 'executives', 'selector': '.executive, .team-member', 'type': 'text', 'all': True}
                ]
            }
        }
    
    async def generate_schema(self, url: str, extraction_goal: str, schema_name: str) -> Optional[Dict]:
        """Generate a new schema using LLM analysis"""
        print(f"🔍 Generating schema for: {url}")
        print(f"   Goal: {extraction_goal}")
        
        extraction_strategy = LLMExtractionStrategy(
            provider="openai/gpt-4o-mini",
            instruction=f"""
            Analyze this webpage structure and create a CSS/JSON extraction schema.
            
            Goal: {extraction_goal}
            
            Return a valid JSON schema with CSS selectors that can reliably extract the required data.
            The schema should follow this exact format:
            {{
                "name": "items",
                "baseSelector": "container_selector_for_items",
                "fields": [
                    {{"name": "field1", "selector": "css_selector", "type": "text"}},
                    {{"name": "field2", "selector": "css_selector", "type": "attribute", "attribute": "href"}},
                    {{"name": "field3", "selector": "css_selector", "type": "text", "all": true}}
                ]
            }}
            
            Rules:
            - Make selectors specific to avoid false matches
            - Use "type": "text" for text content
            - Use "type": "attribute" with "attribute": "name" for attributes
            - Use "all": true to extract all matching elements
            - Test selectors for reliability
            """
        )
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            wait_for="css:body",
            remove_overlay_elements=True,
            page_timeout=30000
        )
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    # Parse the generated schema
                    schema = json.loads(result.extracted_content)
                    
                    # Validate schema structure
                    if self._validate_schema(schema):
                        # Save schema
                        schema_file = self.schema_dir / f"{schema_name}.json"
                        with open(schema_file, 'w') as f:
                            json.dump(schema, f, indent=2)
                        
                        print(f"✅ Schema generated and saved to: {schema_file}")
                        return schema
                    else:
                        print("⚠️ Generated schema failed validation")
                        return None
                else:
                    print(f"❌ Failed to generate schema: {result.error_message if result else 'Unknown error'}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error generating schema: {e}")
            return None
    
    def _validate_schema(self, schema: Dict) -> bool:
        """Validate schema structure"""
        required_fields = ['name', 'fields']
        
        # Check required fields
        for field in required_fields:
            if field not in schema:
                print(f"Missing required field: {field}")
                return False
        
        # Validate fields array
        if not isinstance(schema['fields'], list):
            print("Fields must be an array")
            return False
        
        # Validate each field
        for field in schema['fields']:
            if 'name' not in field or 'selector' not in field or 'type' not in field:
                print(f"Invalid field structure: {field}")
                return False
        
        return True
    
    async def test_schema(self, url: str, schema_path: str) -> Dict:
        """Test a schema against a URL"""
        print(f"🧪 Testing schema: {schema_path}")
        print(f"   Against URL: {url}")
        
        # Load schema
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
        
        extraction_strategy = JsonCssExtractionStrategy(
            schema=schema,
            verbose=True
        )
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            wait_for="css:body"
        )
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    items = data.get(schema.get('name', 'items'), [])
                    
                    print(f"✅ Extraction successful!")
                    print(f"   Items extracted: {len(items)}")
                    
                    if items:
                        print(f"   Sample item:")
                        print(json.dumps(items[0], indent=2)[:500])
                    
                    return {
                        'success': True,
                        'item_count': len(items),
                        'sample': items[0] if items else None,
                        'data': data
                    }
                else:
                    print(f"❌ Extraction failed")
                    return {'success': False, 'error': 'Extraction failed'}
                    
        except Exception as e:
            print(f"❌ Error testing schema: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_template(self, template_name: str) -> Optional[Dict]:
        """Get a predefined template"""
        return self.templates.get(template_name)
    
    def list_schemas(self) -> list:
        """List all saved schemas"""
        schemas = []
        for schema_file in self.schema_dir.glob('*.json'):
            with open(schema_file, 'r') as f:
                schema = json.load(f)
                schemas.append({
                    'name': schema_file.stem,
                    'file': str(schema_file),
                    'fields': len(schema.get('fields', [])),
                    'selector': schema.get('baseSelector', schema.get('selector', 'N/A'))
                })
        return schemas
    
    async def generate_all_schemas(self):
        """Generate schemas for all major data sources"""
        sources = [
            {
                'url': 'https://www.imdb.com/chart/top/',
                'goal': 'Extract movie titles, ratings, years, and links',
                'name': 'imdb_top_movies'
            },
            {
                'url': 'https://variety.com/v/film/',
                'goal': 'Extract article titles, excerpts, dates, authors, and links',
                'name': 'variety_news'
            },
            {
                'url': 'https://www.boxofficemojo.com/weekend/chart/',
                'goal': 'Extract movie titles, box office gross, theaters, and rankings',
                'name': 'box_office_weekend'
            },
            {
                'url': 'https://www.hollywoodreporter.com/c/business/business-news/',
                'goal': 'Extract news articles with titles, excerpts, and publication dates',
                'name': 'thr_business_news'
            }
        ]
        
        for source in sources:
            print(f"\n{'='*60}")
            print(f"Generating schema: {source['name']}")
            print(f"{'='*60}")
            
            schema = await self.generate_schema(
                url=source['url'],
                extraction_goal=source['goal'],
                schema_name=source['name']
            )
            
            if schema:
                # Test the generated schema
                print(f"\n📊 Testing generated schema...")
                test_result = await self.test_schema(
                    url=source['url'],
                    schema_path=self.schema_dir / f"{source['name']}.json"
                )
                
                if test_result['success']:
                    print(f"✅ Schema {source['name']} is working!")
                else:
                    print(f"⚠️ Schema {source['name']} needs adjustment")
            
            # Add delay between requests
            await asyncio.sleep(2)
        
        print(f"\n{'='*60}")
        print(f"Schema generation complete!")
        print(f"Schemas saved in: {self.schema_dir}")
        print(f"{'='*60}")
        
        # List all schemas
        print("\n📁 Available Schemas:")
        for schema in self.list_schemas():
            print(f"  - {schema['name']}: {schema['fields']} fields")


async def main():
    """Main execution"""
    generator = SchemaGenerator()
    
    print("🎬 Pitchey Schema Generator")
    print("="*60)
    
    # Option 1: Generate all schemas
    await generator.generate_all_schemas()
    
    # Option 2: Generate a single custom schema
    # custom_schema = await generator.generate_schema(
    #     url="https://example.com",
    #     extraction_goal="Extract specific data points",
    #     schema_name="custom_schema"
    # )
    
    # Option 3: Test an existing schema
    # test_result = await generator.test_schema(
    #     url="https://www.imdb.com/chart/top/",
    #     schema_path="./schemas/imdb_top_movies.json"
    # )


if __name__ == "__main__":
    asyncio.run(main())