#!/usr/bin/env python3
"""
Python Worker for Crawl4AI Operations
Handles web scraping, validation, and enrichment tasks
Designed to run as a separate service called by Cloudflare Workers
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import os
import sys
from datetime import datetime, timedelta
import json
import hashlib
from pathlib import Path

# Add script directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Import our Crawl4AI modules
from industry_news_feed import IndustryNewsScraper
from pitch_validator import PitchValidator
from enrichment_pipeline import PitchEnrichmentPipeline
from schema_generator import SchemaGenerator

app = FastAPI(
    title="Pitchey Crawl4AI Worker",
    description="Web scraping and enrichment service for Pitchey platform",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scrapers
news_scraper = IndustryNewsScraper()
pitch_validator = PitchValidator()
enrichment_pipeline = PitchEnrichmentPipeline()
schema_generator = SchemaGenerator()

# Cache directory
CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)

# Request models
class NewsRequest(BaseModel):
    sources: List[str] = ['variety', 'hollywood_reporter', 'deadline']
    limit: int = 10

class PitchValidationRequest(BaseModel):
    title: str
    genre: str
    logline: Optional[str] = None
    format: str = 'feature'

class PitchEnrichmentRequest(BaseModel):
    pitch_id: str
    title: str
    genre: Optional[str] = None
    budget: Optional[str] = None
    target_audience: Optional[str] = None

class CompetitorAnalysisRequest(BaseModel):
    title: str
    genre: Optional[str] = None
    keywords: Optional[List[str]] = None

class SchemaGenerationRequest(BaseModel):
    url: str
    goal: str
    name: str

# Helper functions
def get_cache_key(prefix: str, data: Dict) -> str:
    """Generate cache key from prefix and data"""
    data_str = json.dumps(data, sort_keys=True)
    hash_val = hashlib.md5(data_str.encode()).hexdigest()[:8]
    return f"{prefix}_{hash_val}"

async def get_cached_or_compute(cache_key: str, compute_fn, ttl_hours: int = 24):
    """Get from cache or compute if missing"""
    cache_file = CACHE_DIR / f"{cache_key}.json"
    
    # Check if cache exists and is fresh
    if cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=ttl_hours):
            with open(cache_file, 'r') as f:
                return json.load(f)
    
    # Compute fresh data
    data = await compute_fn()
    
    # Save to cache
    with open(cache_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return data

# Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pitchey-crawl4ai-worker",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/scrape/news")
async def scrape_news(request: NewsRequest):
    """Scrape industry news from multiple sources"""
    try:
        cache_key = get_cache_key("news", request.dict())
        
        async def compute():
            widget_data = await news_scraper.get_widget_data()
            # Filter by requested sources and limit
            filtered_items = [
                item for item in widget_data['items']
                if item['source'] in request.sources
            ][:request.limit]
            widget_data['items'] = filtered_items
            return widget_data
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=0.5)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate/pitch")
async def validate_pitch(request: PitchValidationRequest):
    """Validate pitch uniqueness and viability"""
    try:
        cache_key = get_cache_key("validation", request.dict())
        
        async def compute():
            result = await pitch_validator.validate_pitch(
                title=request.title,
                genre=request.genre,
                logline=request.logline,
                format=request.format
            )
            return result
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=24)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/enrich/pitch")
async def enrich_pitch(request: PitchEnrichmentRequest):
    """Enrich pitch with market data"""
    try:
        cache_key = get_cache_key("enrichment", {"pitch_id": request.pitch_id})
        
        async def compute():
            pitch_data = {
                'title': request.title,
                'genre': request.genre,
                'budget': request.budget,
                'target_audience': request.target_audience
            }
            result = await enrichment_pipeline.enrich_pitch(pitch_data)
            return result
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=168)  # 7 days
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trends/{genre}")
async def get_genre_trends(genre: str):
    """Get market trends for a specific genre"""
    try:
        cache_key = f"trends_{genre}_{datetime.now().strftime('%Y%m%d')}"
        
        async def compute():
            # Scrape box office data for genre analysis
            from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
            
            browser_config = BrowserConfig(headless=True)
            crawler_config = CrawlerRunConfig(
                wait_for="css:table",
                remove_overlay_elements=True
            )
            
            trends = {
                'genre': genre,
                'date': datetime.now().isoformat(),
                'top_performers': [],
                'average_gross': 0,
                'trend': 'stable'
            }
            
            # This would normally scrape real data
            # For now, return sample data
            trends['top_performers'] = [
                {'title': 'Sample Movie 1', 'gross': '$50M'},
                {'title': 'Sample Movie 2', 'gross': '$30M'}
            ]
            trends['average_gross'] = '$40M'
            trends['trend'] = 'growing'
            
            return trends
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=6)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/boxoffice/{timeframe}")
async def get_box_office(timeframe: str = "weekend"):
    """Get box office data for specified timeframe"""
    try:
        cache_key = f"boxoffice_{timeframe}_{datetime.now().strftime('%Y%m%d')}"
        
        async def compute():
            # This would scrape Box Office Mojo
            # For now, return sample data
            return {
                'timeframe': timeframe,
                'date': datetime.now().isoformat(),
                'top_10': [
                    {'rank': 1, 'title': 'Movie A', 'gross': '$25M', 'theaters': 3500},
                    {'rank': 2, 'title': 'Movie B', 'gross': '$18M', 'theaters': 3200},
                ],
                'total_gross': '$150M'
            }
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=6)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/competitors")
async def analyze_competitors(request: CompetitorAnalysisRequest):
    """Analyze competing projects"""
    try:
        cache_key = get_cache_key("competitors", request.dict())
        
        async def compute():
            # Search for similar projects
            similar = await pitch_validator.find_similar_projects(
                title=request.title,
                genre=request.genre
            )
            
            # Analyze competition
            analysis = {
                'title': request.title,
                'similar_projects': similar[:5] if similar else [],
                'market_saturation': 'medium',
                'differentiation_needed': True,
                'recommendations': [
                    'Focus on unique angle',
                    'Target different demographic',
                    'Consider different format'
                ]
            }
            
            return analysis
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=24)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/company/{name}")
async def get_company_info(name: str):
    """Get production company information"""
    try:
        cache_key = f"company_{name.lower().replace(' ', '_')}"
        
        async def compute():
            # This would scrape company websites and industry databases
            # For now, return sample data
            return {
                'name': name,
                'type': 'production_company',
                'recent_projects': [
                    {'title': 'Recent Film 1', 'year': 2024},
                    {'title': 'Recent Film 2', 'year': 2023}
                ],
                'genres': ['drama', 'thriller'],
                'budget_range': '$10M - $50M',
                'contact': 'submissions@example.com'
            }
        
        data = await get_cached_or_compute(cache_key, compute, ttl_hours=168)  # 7 days
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schemas/generate")
async def generate_schema(request: SchemaGenerationRequest):
    """Generate extraction schema for a URL"""
    try:
        schema = await schema_generator.generate_schema(
            url=request.url,
            extraction_goal=request.goal,
            schema_name=request.name
        )
        
        if schema:
            return schema
        else:
            raise HTTPException(status_code=400, detail="Failed to generate schema")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schemas")
async def list_schemas():
    """List all available schemas"""
    try:
        schemas = schema_generator.list_schemas()
        return {"schemas": schemas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schemas/test")
async def test_schema(url: str, schema_name: str):
    """Test a schema against a URL"""
    try:
        schema_path = Path(f"./schemas/{schema_name}.json")
        if not schema_path.exists():
            raise HTTPException(status_code=404, detail="Schema not found")
        
        result = await schema_generator.test_schema(url, str(schema_path))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cache/{cache_type}")
async def clear_cache(cache_type: str):
    """Clear cache for specific type"""
    try:
        pattern = f"{cache_type}_*.json"
        cleared = 0
        
        for cache_file in CACHE_DIR.glob(pattern):
            cache_file.unlink()
            cleared += 1
        
        return {"message": f"Cleared {cleared} cache entries for {cache_type}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background tasks
async def refresh_news_cache():
    """Background task to refresh news cache"""
    while True:
        try:
            await news_scraper.get_widget_data()
        except Exception as e:
            print(f"News refresh error: {e}")
        await asyncio.sleep(300)  # 5 minutes

@app.on_event("startup")
async def startup_event():
    """Initialize background tasks on startup"""
    # Start background news refresh
    asyncio.create_task(refresh_news_cache())
    print("Pitchey Crawl4AI Worker started")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Pitchey Crawl4AI Worker shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)