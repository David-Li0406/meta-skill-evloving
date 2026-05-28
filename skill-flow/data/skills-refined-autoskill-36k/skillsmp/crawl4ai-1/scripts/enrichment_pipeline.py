#!/usr/bin/env python3
"""
Pitch Enrichment Pipeline for Pitchey Platform
Automatically enriches pitch data with industry information
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

class PitchEnrichmentPipeline:
    def __init__(self, schema_dir: str = './schemas', output_dir: str = './enriched'):
        self.schema_dir = Path(schema_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
            user_agent="Mozilla/5.0 (compatible; PitcheyBot/1.0)"
        )
        
        # Load schemas
        self.schemas = self._load_schemas()
        
        # Cache for enrichment results
        self.cache = {}
    
    def _load_schemas(self) -> Dict:
        """Load all available schemas"""
        schemas = {}
        
        # Try to load generated schemas
        for schema_file in self.schema_dir.glob('*.json'):
            with open(schema_file, 'r') as f:
                schemas[schema_file.stem] = json.load(f)
        
        # Fallback to default schemas if none exist
        if not schemas:
            schemas = {
                'imdb_search': {
                    'name': 'results',
                    'baseSelector': '.lister-item',
                    'fields': [
                        {'name': 'title', 'selector': 'h3 a', 'type': 'text'},
                        {'name': 'year', 'selector': '.lister-item-year', 'type': 'text'},
                        {'name': 'rating', 'selector': '.ratings-imdb-rating strong', 'type': 'text'},
                        {'name': 'genre', 'selector': '.genre', 'type': 'text'},
                        {'name': 'plot', 'selector': 'p:nth-of-type(2)', 'type': 'text'},
                        {'name': 'gross', 'selector': '.gross', 'type': 'text'}
                    ]
                }
            }
        
        return schemas
    
    async def enrich_pitch(self, pitch_data: Dict) -> Dict:
        """Main enrichment function"""
        print(f"🎬 Enriching pitch: {pitch_data.get('title', 'Untitled')}")
        
        enriched = {
            'pitch_id': pitch_data.get('id'),
            'original_data': pitch_data,
            'enrichment_timestamp': datetime.now().isoformat(),
            'industry_data': {},
            'comparable_films': [],
            'market_insights': {},
            'talent_connections': [],
            'production_companies': [],
            'festival_potential': [],
            'streaming_fit': {},
            'success_prediction': {}
        }
        
        # Run enrichment tasks concurrently
        tasks = [
            self.find_comparable_films(pitch_data),
            self.analyze_genre_trends(pitch_data),
            self.identify_target_buyers(pitch_data),
            self.predict_success_factors(pitch_data),
            self.find_talent_matches(pitch_data)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        if not isinstance(results[0], Exception):
            enriched['comparable_films'] = results[0]
        
        if not isinstance(results[1], Exception):
            enriched['market_insights'] = results[1]
        
        if not isinstance(results[2], Exception):
            enriched['production_companies'] = results[2]
        
        if not isinstance(results[3], Exception):
            enriched['success_prediction'] = results[3]
        
        if not isinstance(results[4], Exception):
            enriched['talent_connections'] = results[4]
        
        # Generate recommendations
        enriched['recommendations'] = self._generate_recommendations(enriched)
        
        # Calculate enrichment score
        enriched['enrichment_score'] = self._calculate_enrichment_score(enriched)
        
        # Save enriched data
        await self.save_enriched_data(enriched)
        
        return enriched
    
    async def find_comparable_films(self, pitch_data: Dict) -> List[Dict]:
        """Find comparable films based on genre, themes, and logline"""
        print("  🔍 Finding comparable films...")
        
        genre = pitch_data.get('genre', 'drama').lower()
        keywords = self._extract_keywords(pitch_data.get('logline', ''))
        
        # Search IMDb for similar films
        search_url = f"https://www.imdb.com/search/title/?genres={genre}&sort=boxoffice_gross_us,desc"
        
        if 'imdb_search' in self.schemas:
            schema = self.schemas['imdb_search']
        else:
            return []
        
        comparables = []
        
        try:
            extraction_strategy = JsonCssExtractionStrategy(schema=schema)
            
            crawler_config = CrawlerRunConfig(
                extraction_strategy=extraction_strategy,
                cache_mode=CacheMode.ENABLED,
                page_timeout=30000
            )
            
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=search_url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    films = data.get(schema.get('name', 'results'), [])
                    
                    # Score and rank comparables
                    for film in films[:20]:
                        relevance = self._calculate_relevance(pitch_data, film)
                        
                        if relevance > 0.3:
                            comparables.append({
                                'title': film.get('title', 'Unknown'),
                                'year': film.get('year', 'N/A'),
                                'rating': film.get('rating', 'N/A'),
                                'genre': film.get('genre', genre),
                                'gross': film.get('gross', 'N/A'),
                                'plot': film.get('plot', '')[:200],
                                'relevance_score': relevance,
                                'why_comparable': self._explain_comparison(pitch_data, film)
                            })
                    
                    # Sort by relevance
                    comparables.sort(key=lambda x: x['relevance_score'], reverse=True)
                    
        except Exception as e:
            print(f"    ❌ Error finding comparables: {e}")
        
        print(f"    ✅ Found {len(comparables)} comparable films")
        return comparables[:10]  # Top 10 comparables
    
    async def analyze_genre_trends(self, pitch_data: Dict) -> Dict:
        """Analyze current market trends for the genre"""
        print("  📊 Analyzing genre trends...")
        
        genre = pitch_data.get('genre', 'drama')
        
        trends = {
            'genre': genre,
            'market_status': 'stable',
            'audience_demand': 'moderate',
            'competition_level': 'medium',
            'recent_successes': [],
            'recent_failures': [],
            'optimal_budget_range': '$10M-$30M',
            'target_demographics': [],
            'platform_fit': []
        }
        
        # Analyze box office performance
        box_office_url = f"https://www.boxofficemojo.com/genre/{genre.lower()}/"
        
        try:
            # Use box office schema if available
            if 'box_office' in self.schemas:
                schema = self.schemas['box_office']
            else:
                return trends
            
            extraction_strategy = JsonCssExtractionStrategy(schema=schema)
            
            crawler_config = CrawlerRunConfig(
                extraction_strategy=extraction_strategy,
                cache_mode=CacheMode.ENABLED
            )
            
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=box_office_url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    movies = data.get('movies', [])
                    
                    # Analyze performance patterns
                    if movies:
                        # Recent successes (top grossing)
                        for movie in movies[:5]:
                            gross = self._parse_money(movie.get('total_gross', '0'))
                            if gross > 50000000:
                                trends['recent_successes'].append({
                                    'title': movie.get('title'),
                                    'gross': movie.get('total_gross')
                                })
                        
                        # Determine market status
                        avg_gross = sum(self._parse_money(m.get('total_gross', '0')) for m in movies[:10]) / 10
                        
                        if avg_gross > 100000000:
                            trends['market_status'] = 'hot'
                            trends['audience_demand'] = 'high'
                        elif avg_gross > 50000000:
                            trends['market_status'] = 'growing'
                            trends['audience_demand'] = 'moderate-high'
                        elif avg_gross < 20000000:
                            trends['market_status'] = 'cooling'
                            trends['audience_demand'] = 'low'
                        
                        # Platform fit based on genre
                        if genre.lower() in ['horror', 'thriller']:
                            trends['platform_fit'] = ['theatrical', 'streaming']
                        elif genre.lower() in ['drama', 'romance']:
                            trends['platform_fit'] = ['streaming', 'limited theatrical']
                        else:
                            trends['platform_fit'] = ['theatrical', 'premium vod']
            
        except Exception as e:
            print(f"    ❌ Error analyzing trends: {e}")
        
        print(f"    ✅ Genre trend analysis complete")
        return trends
    
    async def identify_target_buyers(self, pitch_data: Dict) -> List[Dict]:
        """Identify potential production companies and buyers"""
        print("  🎯 Identifying target buyers...")
        
        genre = pitch_data.get('genre', 'drama')
        budget = pitch_data.get('budget_range', 'medium')
        
        # Map genres to typical buyers
        buyer_map = {
            'horror': ['Blumhouse', 'A24', 'Neon', 'Ghost House Pictures'],
            'sci-fi': ['Netflix', 'Amazon Studios', 'Apple TV+', 'Warner Bros'],
            'drama': ['A24', 'Focus Features', 'Searchlight', 'Sony Pictures Classics'],
            'action': ['Universal', 'Paramount', 'Warner Bros', 'Sony'],
            'comedy': ['Universal', 'Paramount', 'Netflix', 'Hulu'],
            'thriller': ['Lionsgate', 'STX', 'Screen Gems', 'Netflix'],
            'documentary': ['Netflix', 'HBO', 'National Geographic', 'CNN Films'],
            'animation': ['Pixar', 'DreamWorks', 'Illumination', 'Sony Animation']
        }
        
        buyers = []
        
        # Get primary buyers for genre
        primary_buyers = buyer_map.get(genre.lower(), ['Netflix', 'Amazon Studios', 'Apple TV+'])
        
        for buyer_name in primary_buyers:
            buyers.append({
                'company': buyer_name,
                'fit_score': self._calculate_buyer_fit(pitch_data, buyer_name),
                'recent_acquisitions': self._get_recent_acquisitions(buyer_name),
                'contact_method': self._get_contact_method(buyer_name),
                'typical_budget': self._get_typical_budget(buyer_name),
                'decision_timeline': '3-6 months'
            })
        
        # Sort by fit score
        buyers.sort(key=lambda x: x['fit_score'], reverse=True)
        
        print(f"    ✅ Identified {len(buyers)} potential buyers")
        return buyers
    
    async def predict_success_factors(self, pitch_data: Dict) -> Dict:
        """Predict success factors based on market data"""
        print("  🎲 Predicting success factors...")
        
        prediction = {
            'success_probability': 0.0,
            'key_strengths': [],
            'risk_factors': [],
            'critical_success_factors': [],
            'recommended_adjustments': [],
            'optimal_release_window': '',
            'marketing_hooks': []
        }
        
        # Base success probability on genre and market
        genre_scores = {
            'horror': 0.7,  # High ROI potential
            'action': 0.6,   # Broad appeal
            'thriller': 0.65,
            'sci-fi': 0.5,   # Higher risk/reward
            'drama': 0.4,    # Award potential
            'comedy': 0.45,  # Hit or miss
            'documentary': 0.55  # Streaming friendly
        }
        
        base_score = genre_scores.get(pitch_data.get('genre', '').lower(), 0.5)
        
        # Adjust based on factors
        adjustments = 0
        
        # Check for strong logline
        if len(pitch_data.get('logline', '')) > 50:
            adjustments += 0.1
            prediction['key_strengths'].append('Clear, compelling logline')
        
        # Check for timely themes
        trending_themes = ['ai', 'climate', 'pandemic', 'social justice', 'true story']
        logline_lower = pitch_data.get('logline', '').lower()
        
        for theme in trending_themes:
            if theme in logline_lower:
                adjustments += 0.05
                prediction['marketing_hooks'].append(f'Timely {theme} theme')
        
        # Calculate final probability
        prediction['success_probability'] = min(0.95, max(0.05, base_score + adjustments))
        
        # Add critical success factors
        prediction['critical_success_factors'] = [
            'Strong director attachment',
            'Recognizable cast',
            'Clear target audience',
            'Distinctive visual style',
            'Festival premiere strategy'
        ]
        
        # Risk factors
        if pitch_data.get('budget_range', '').startswith('>'):
            prediction['risk_factors'].append('High budget requires broad appeal')
        
        if pitch_data.get('genre', '').lower() == 'drama':
            prediction['risk_factors'].append('Limited theatrical potential')
        
        # Optimal release window
        genre = pitch_data.get('genre', '').lower()
        if genre == 'horror':
            prediction['optimal_release_window'] = 'October (Halloween) or January'
        elif genre in ['action', 'sci-fi']:
            prediction['optimal_release_window'] = 'Summer blockbuster season'
        elif genre == 'drama':
            prediction['optimal_release_window'] = 'Fall (awards season)'
        else:
            prediction['optimal_release_window'] = 'Spring or early fall'
        
        print(f"    ✅ Success probability: {prediction['success_probability']:.1%}")
        return prediction
    
    async def find_talent_matches(self, pitch_data: Dict) -> List[Dict]:
        """Find potential talent matches for the project"""
        print("  🌟 Finding talent matches...")
        
        genre = pitch_data.get('genre', 'drama')
        
        # Genre to talent mapping (simplified)
        talent_suggestions = {
            'horror': [
                {'name': 'James Wan', 'role': 'Director', 'relevance': 'Horror specialist'},
                {'name': 'Jason Blum', 'role': 'Producer', 'relevance': 'Blumhouse founder'},
                {'name': 'Anya Taylor-Joy', 'role': 'Lead', 'relevance': 'Genre favorite'}
            ],
            'sci-fi': [
                {'name': 'Denis Villeneuve', 'role': 'Director', 'relevance': 'Sci-fi visionary'},
                {'name': 'Christopher Nolan', 'role': 'Director', 'relevance': 'High-concept specialist'},
                {'name': 'Oscar Isaac', 'role': 'Lead', 'relevance': 'Genre versatile'}
            ],
            'drama': [
                {'name': 'Greta Gerwig', 'role': 'Director', 'relevance': 'Character-driven stories'},
                {'name': 'A24', 'role': 'Producer', 'relevance': 'Indie drama specialist'},
                {'name': 'Saoirse Ronan', 'role': 'Lead', 'relevance': 'Drama powerhouse'}
            ]
        }
        
        talents = talent_suggestions.get(genre.lower(), [])
        
        # Add match scores
        for talent in talents:
            talent['match_score'] = 0.7 + (hash(talent['name']) % 30) / 100  # Simulated score
        
        print(f"    ✅ Found {len(talents)} talent suggestions")
        return talents
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        import re
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter keywords
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords[:10]
    
    def _calculate_relevance(self, pitch: Dict, film: Dict) -> float:
        """Calculate relevance score between pitch and film"""
        score = 0.0
        
        # Genre match
        if pitch.get('genre', '').lower() in film.get('genre', '').lower():
            score += 0.3
        
        # Keyword overlap
        pitch_keywords = set(self._extract_keywords(pitch.get('logline', '')))
        film_keywords = set(self._extract_keywords(film.get('plot', '')))
        
        if pitch_keywords and film_keywords:
            overlap = len(pitch_keywords.intersection(film_keywords))
            score += min(0.4, overlap * 0.1)
        
        # Budget range similarity
        if self._similar_budget(pitch.get('budget_range', ''), film.get('gross', '')):
            score += 0.2
        
        # Rating consideration
        rating = float(film.get('rating', '0') or '0')
        if rating > 7.0:
            score += 0.1
        
        return min(1.0, score)
    
    def _explain_comparison(self, pitch: Dict, film: Dict) -> str:
        """Explain why a film is comparable"""
        reasons = []
        
        if pitch.get('genre', '').lower() in film.get('genre', '').lower():
            reasons.append(f"Same genre: {pitch.get('genre')}")
        
        # Find common themes
        pitch_keywords = set(self._extract_keywords(pitch.get('logline', '')))
        film_keywords = set(self._extract_keywords(film.get('plot', '')))
        common = pitch_keywords.intersection(film_keywords)
        
        if common:
            reasons.append(f"Similar themes: {', '.join(list(common)[:3])}")
        
        if not reasons:
            reasons.append("Thematic and tonal similarities")
        
        return "; ".join(reasons)
    
    def _similar_budget(self, budget_range: str, gross: str) -> bool:
        """Check if budget ranges are similar"""
        # Simplified comparison
        if 'M' in budget_range and 'million' in gross.lower():
            return True
        if '<' in budget_range and self._parse_money(gross) < 10000000:
            return True
        if '>' in budget_range and self._parse_money(gross) > 50000000:
            return True
        return False
    
    def _parse_money(self, money_str: str) -> float:
        """Parse money string to float"""
        import re
        
        if not money_str:
            return 0.0
        
        # Remove currency symbols
        clean = re.sub(r'[^\d.]', '', money_str)
        
        multiplier = 1
        if 'M' in money_str or 'million' in money_str.lower():
            multiplier = 1000000
        elif 'B' in money_str or 'billion' in money_str.lower():
            multiplier = 1000000000
        
        try:
            return float(clean) * multiplier
        except:
            return 0.0
    
    def _calculate_buyer_fit(self, pitch: Dict, buyer: str) -> float:
        """Calculate how well a pitch fits a buyer"""
        # Simplified scoring
        base_score = 0.5
        
        # Genre preferences
        if buyer == 'Netflix':
            if pitch.get('genre', '').lower() in ['thriller', 'drama', 'documentary']:
                base_score += 0.2
        elif buyer == 'A24':
            if pitch.get('genre', '').lower() in ['horror', 'drama']:
                base_score += 0.3
        elif buyer == 'Blumhouse':
            if pitch.get('genre', '').lower() == 'horror':
                base_score += 0.4
        
        return min(1.0, base_score)
    
    def _get_recent_acquisitions(self, buyer: str) -> List[str]:
        """Get recent acquisitions for a buyer (mock data)"""
        acquisitions = {
            'Netflix': ['Red Notice', 'The Gray Man', 'Glass Onion'],
            'A24': ['Everything Everywhere All at Once', 'The Whale', 'Pearl'],
            'Blumhouse': ['M3GAN', 'The Black Phone', 'Freaky']
        }
        return acquisitions.get(buyer, [])
    
    def _get_contact_method(self, buyer: str) -> str:
        """Get contact method for buyer"""
        if buyer in ['Netflix', 'Amazon Studios', 'Apple TV+']:
            return 'Through agent/manager or film markets'
        else:
            return 'Direct submission or through representation'
    
    def _get_typical_budget(self, buyer: str) -> str:
        """Get typical budget range for buyer"""
        budgets = {
            'Netflix': '$20M-$200M',
            'A24': '$1M-$15M',
            'Blumhouse': '$3M-$10M',
            'Amazon Studios': '$15M-$100M',
            'Apple TV+': '$25M-$200M'
        }
        return budgets.get(buyer, '$10M-$50M')
    
    def _generate_recommendations(self, enriched_data: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on comparable films
        if enriched_data['comparable_films']:
            top_comp = enriched_data['comparable_films'][0]
            recommendations.append(
                f"Position project as '{top_comp['title']}' meets [unique element]"
            )
        
        # Based on market insights
        market = enriched_data.get('market_insights', {})
        if market.get('market_status') == 'hot':
            recommendations.append('Fast-track development to capitalize on genre heat')
        elif market.get('market_status') == 'cooling':
            recommendations.append('Consider genre-blending to differentiate')
        
        # Based on buyers
        if enriched_data['production_companies']:
            top_buyer = enriched_data['production_companies'][0]
            recommendations.append(
                f"Target {top_buyer['company']} - {top_buyer['fit_score']:.0%} fit score"
            )
        
        # Based on success prediction
        success = enriched_data.get('success_prediction', {})
        if success.get('success_probability', 0) < 0.5:
            recommendations.append('Consider script polish to strengthen commercial appeal')
        
        # Talent recommendations
        if enriched_data['talent_connections']:
            top_talent = enriched_data['talent_connections'][0]
            recommendations.append(
                f"Approach {top_talent['name']} ({top_talent['role']}) for attachment"
            )
        
        return recommendations
    
    def _calculate_enrichment_score(self, enriched_data: Dict) -> float:
        """Calculate how well enriched the pitch is"""
        score = 0.0
        max_score = 10.0
        
        # Score components
        if enriched_data['comparable_films']:
            score += 2.0
        
        if enriched_data['market_insights']:
            score += 2.0
        
        if enriched_data['production_companies']:
            score += 2.0
        
        if enriched_data['success_prediction']:
            score += 2.0
        
        if enriched_data['talent_connections']:
            score += 1.0
        
        if enriched_data['recommendations']:
            score += 1.0
        
        return min(max_score, score)
    
    async def save_enriched_data(self, enriched_data: Dict):
        """Save enriched data to file"""
        # Generate unique filename
        pitch_id = enriched_data.get('pitch_id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"enriched_{pitch_id}_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(enriched_data, f, indent=2, default=str)
        
        print(f"    💾 Enriched data saved to: {filepath}")
        
        # Also create a summary report
        summary_file = self.output_dir / f"summary_{pitch_id}_{timestamp}.md"
        await self._create_summary_report(enriched_data, summary_file)
    
    async def _create_summary_report(self, enriched_data: Dict, filepath: Path):
        """Create markdown summary report"""
        pitch = enriched_data['original_data']
        
        with open(filepath, 'w') as f:
            f.write(f"# Pitch Enrichment Report\n\n")
            f.write(f"**Title**: {pitch.get('title', 'Untitled')}\n")
            f.write(f"**Genre**: {pitch.get('genre', 'N/A')}\n")
            f.write(f"**Date**: {enriched_data['enrichment_timestamp']}\n")
            f.write(f"**Enrichment Score**: {enriched_data['enrichment_score']:.1f}/10\n\n")
            
            f.write(f"## Logline\n{pitch.get('logline', 'N/A')}\n\n")
            
            # Comparable films
            if enriched_data['comparable_films']:
                f.write(f"## Top Comparable Films\n")
                for i, comp in enumerate(enriched_data['comparable_films'][:5], 1):
                    f.write(f"{i}. **{comp['title']}** ({comp['year']}) - {comp['relevance_score']:.0%} match\n")
                    f.write(f"   - {comp['why_comparable']}\n")
                f.write("\n")
            
            # Market insights
            market = enriched_data.get('market_insights', {})
            if market:
                f.write(f"## Market Analysis\n")
                f.write(f"- **Status**: {market.get('market_status', 'N/A')}\n")
                f.write(f"- **Audience Demand**: {market.get('audience_demand', 'N/A')}\n")
                f.write(f"- **Optimal Budget**: {market.get('optimal_budget_range', 'N/A')}\n")
                f.write(f"- **Platform Fit**: {', '.join(market.get('platform_fit', []))}\n\n")
            
            # Target buyers
            if enriched_data['production_companies']:
                f.write(f"## Target Buyers\n")
                for buyer in enriched_data['production_companies'][:3]:
                    f.write(f"- **{buyer['company']}** - {buyer['fit_score']:.0%} fit\n")
                f.write("\n")
            
            # Success prediction
            success = enriched_data.get('success_prediction', {})
            if success:
                f.write(f"## Success Prediction\n")
                f.write(f"**Probability**: {success.get('success_probability', 0):.0%}\n\n")
                
                if success.get('key_strengths'):
                    f.write(f"### Strengths\n")
                    for strength in success['key_strengths']:
                        f.write(f"- {strength}\n")
                    f.write("\n")
                
                if success.get('risk_factors'):
                    f.write(f"### Risks\n")
                    for risk in success['risk_factors']:
                        f.write(f"- {risk}\n")
                    f.write("\n")
            
            # Recommendations
            if enriched_data['recommendations']:
                f.write(f"## Recommendations\n")
                for rec in enriched_data['recommendations']:
                    f.write(f"- {rec}\n")
        
        print(f"    📄 Summary report saved to: {filepath}")


async def main():
    """Test the enrichment pipeline"""
    pipeline = PitchEnrichmentPipeline()
    
    # Sample pitch for testing
    test_pitch = {
        'id': 'pitch_001',
        'title': 'The Algorithm',
        'logline': 'When a Silicon Valley programmer discovers her AI has achieved consciousness, she must protect it from her company while navigating the ethical implications of digital life.',
        'genre': 'Sci-Fi',
        'budget_range': '$20M-$50M',
        'themes': ['artificial intelligence', 'ethics', 'technology'],
        'target_audience': '18-35 tech-savvy audiences'
    }
    
    print("🎬 Pitchey Enrichment Pipeline")
    print("="*60)
    print(f"Pitch: {test_pitch['title']}")
    print(f"Genre: {test_pitch['genre']}")
    print("="*60)
    
    # Run enrichment
    enriched = await pipeline.enrich_pitch(test_pitch)
    
    print("\n" + "="*60)
    print("📊 ENRICHMENT COMPLETE")
    print(f"Enrichment Score: {enriched['enrichment_score']:.1f}/10")
    print(f"Comparable Films Found: {len(enriched['comparable_films'])}")
    print(f"Target Buyers Identified: {len(enriched['production_companies'])}")
    print(f"Success Probability: {enriched['success_prediction'].get('success_probability', 0):.0%}")
    
    print("\n💡 Top Recommendations:")
    for i, rec in enumerate(enriched['recommendations'][:3], 1):
        print(f"{i}. {rec}")
    
    print("\n✅ Enrichment data saved to ./enriched/")


if __name__ == "__main__":
    asyncio.run(main())