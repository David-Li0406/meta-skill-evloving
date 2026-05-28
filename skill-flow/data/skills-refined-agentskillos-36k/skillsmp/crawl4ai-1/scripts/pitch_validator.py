#!/usr/bin/env python3
"""
Pitch Validation System for Pitchey Platform
Validates pitch uniqueness and provides market insights
"""

import asyncio
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai.extraction_strategy import CosineStrategy

class PitchValidator:
    def __init__(self, cache_dir: str = './cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Browser config for stealth
        self.browser_config = BrowserConfig(
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        # Load or generate schemas
        self.schemas = self._load_schemas()
    
    def _load_schemas(self) -> Dict:
        """Load pre-generated extraction schemas"""
        return {
            'imdb_search': {
                'name': 'results',
                'baseSelector': '.lister-item',
                'fields': [
                    {'name': 'title', 'selector': 'h3 a', 'type': 'text'},
                    {'name': 'year', 'selector': '.lister-item-year', 'type': 'text'},
                    {'name': 'genre', 'selector': '.genre', 'type': 'text'},
                    {'name': 'rating', 'selector': '.ratings-imdb-rating strong', 'type': 'text'},
                    {'name': 'plot', 'selector': 'p:nth-of-type(2)', 'type': 'text'},
                    {'name': 'director', 'selector': 'p:nth-of-type(3) a:first-child', 'type': 'text'},
                    {'name': 'stars', 'selector': 'p:nth-of-type(3)', 'type': 'text'},
                    {'name': 'link', 'selector': 'h3 a', 'type': 'attribute', 'attribute': 'href'}
                ]
            },
            'boxofficemojo': {
                'name': 'movies',
                'baseSelector': 'tr[id^="row_"]',
                'fields': [
                    {'name': 'title', 'selector': '.a-text-left a', 'type': 'text'},
                    {'name': 'gross', 'selector': '.a-text-right:nth-child(2)', 'type': 'text'},
                    {'name': 'theaters', 'selector': '.a-text-right:nth-child(3)', 'type': 'text'},
                    {'name': 'opening', 'selector': '.a-text-right:nth-child(4)', 'type': 'text'},
                    {'name': 'date', 'selector': '.a-text-left:nth-child(5)', 'type': 'text'}
                ]
            },
            'production_news': {
                'name': 'articles',
                'baseSelector': 'article',
                'fields': [
                    {'name': 'title', 'selector': 'h2, h3', 'type': 'text'},
                    {'name': 'status', 'selector': '.status, .tag', 'type': 'text'},
                    {'name': 'company', 'selector': '.company, .studio', 'type': 'text'},
                    {'name': 'date', 'selector': 'time', 'type': 'text'}
                ]
            }
        }
    
    async def validate_pitch(self, pitch_data: Dict) -> Dict:
        """
        Main validation function that checks:
        1. Uniqueness (similar projects)
        2. Market viability
        3. Genre trends
        4. Competition analysis
        """
        validation_results = {
            'pitch_id': pitch_data.get('id'),
            'title': pitch_data.get('title'),
            'validation_timestamp': datetime.now().isoformat(),
            'uniqueness_score': 0,
            'market_viability_score': 0,
            'competition_analysis': {},
            'similar_projects': [],
            'recommendations': [],
            'warnings': [],
            'opportunities': []
        }
        
        # Run all validation checks concurrently
        tasks = [
            self.check_uniqueness(pitch_data),
            self.analyze_market_viability(pitch_data),
            self.find_comparables(pitch_data),
            self.check_production_status(pitch_data)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        uniqueness_result = results[0] if not isinstance(results[0], Exception) else {}
        market_result = results[1] if not isinstance(results[1], Exception) else {}
        comparables = results[2] if not isinstance(results[2], Exception) else []
        production_check = results[3] if not isinstance(results[3], Exception) else {}
        
        # Compile validation results
        validation_results['uniqueness_score'] = uniqueness_result.get('score', 0)
        validation_results['market_viability_score'] = market_result.get('score', 0)
        validation_results['similar_projects'] = uniqueness_result.get('similar_projects', [])
        validation_results['comparables'] = comparables
        validation_results['production_status'] = production_check
        
        # Generate recommendations
        validation_results['recommendations'] = self._generate_recommendations(
            uniqueness_result, market_result, comparables, production_check
        )
        
        # Identify warnings
        validation_results['warnings'] = self._identify_warnings(
            uniqueness_result, market_result, production_check
        )
        
        # Find opportunities
        validation_results['opportunities'] = self._find_opportunities(
            market_result, comparables
        )
        
        # Calculate overall score
        validation_results['overall_score'] = self._calculate_overall_score(validation_results)
        
        return validation_results
    
    async def check_uniqueness(self, pitch_data: Dict) -> Dict:
        """Check if similar projects exist"""
        print(f"🔍 Checking uniqueness for: {pitch_data.get('title')}")
        
        # Build search query
        title = pitch_data.get('title', '')
        logline = pitch_data.get('logline', '')
        genre = pitch_data.get('genre', '')
        
        # Clean and prepare search terms
        search_terms = self._extract_key_terms(f"{title} {logline}")
        
        # Search IMDb for similar titles
        search_url = f"https://www.imdb.com/search/title/?title={'+'.join(search_terms)}&genres={genre.lower()}"
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(
                schema=self.schemas['imdb_search']
            ),
            cache_mode=CacheMode.ENABLED,
            page_timeout=30000
        )
        
        similar_projects = []
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=search_url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    results = data.get('results', [])
                    
                    # Calculate similarity scores
                    for item in results[:10]:  # Top 10 results
                        similarity = self._calculate_similarity(
                            pitch_data,
                            {
                                'title': item.get('title', ''),
                                'plot': item.get('plot', ''),
                                'genre': item.get('genre', '')
                            }
                        )
                        
                        if similarity > 0.3:  # 30% similarity threshold
                            similar_projects.append({
                                'title': item.get('title'),
                                'year': item.get('year'),
                                'similarity_score': similarity,
                                'plot': item.get('plot', '')[:200],
                                'imdb_rating': item.get('rating'),
                                'concern_level': 'high' if similarity > 0.7 else 'medium'
                            })
        
        except Exception as e:
            print(f"❌ Error checking uniqueness: {e}")
        
        # Calculate uniqueness score (inverse of similarity)
        max_similarity = max([p['similarity_score'] for p in similar_projects], default=0)
        uniqueness_score = max(0, 1 - max_similarity) * 10
        
        return {
            'score': uniqueness_score,
            'similar_projects': sorted(similar_projects, key=lambda x: x['similarity_score'], reverse=True),
            'is_unique': uniqueness_score > 7,
            'recommendation': self._get_uniqueness_recommendation(uniqueness_score, similar_projects)
        }
    
    async def analyze_market_viability(self, pitch_data: Dict) -> Dict:
        """Analyze market trends and viability"""
        print(f"📊 Analyzing market viability for genre: {pitch_data.get('genre')}")
        
        genre = pitch_data.get('genre', 'drama')
        budget_range = pitch_data.get('budget_range', 'medium')
        
        # Search box office performance for similar genre
        search_url = f"https://www.boxofficemojo.com/genre/{genre.lower()}/"
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(
                schema=self.schemas['boxofficemojo']
            ),
            cache_mode=CacheMode.ENABLED,
            page_timeout=30000,
            wait_for="css:table"
        )
        
        market_data = {
            'genre_performance': [],
            'avg_gross': 0,
            'success_rate': 0,
            'trend': 'stable'
        }
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=search_url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    movies = data.get('movies', [])
                    
                    # Analyze recent performance
                    for movie in movies[:20]:  # Recent 20 movies
                        gross = self._parse_money(movie.get('gross', '0'))
                        market_data['genre_performance'].append({
                            'title': movie.get('title'),
                            'gross': gross,
                            'success': gross > 10000000  # $10M threshold
                        })
                    
                    # Calculate metrics
                    if market_data['genre_performance']:
                        total_gross = sum(m['gross'] for m in market_data['genre_performance'])
                        market_data['avg_gross'] = total_gross / len(market_data['genre_performance'])
                        market_data['success_rate'] = sum(1 for m in market_data['genre_performance'] if m['success']) / len(market_data['genre_performance'])
                        
                        # Determine trend
                        recent_avg = sum(m['gross'] for m in market_data['genre_performance'][:5]) / 5
                        older_avg = sum(m['gross'] for m in market_data['genre_performance'][5:10]) / 5 if len(market_data['genre_performance']) > 5 else recent_avg
                        
                        if recent_avg > older_avg * 1.2:
                            market_data['trend'] = 'rising'
                        elif recent_avg < older_avg * 0.8:
                            market_data['trend'] = 'declining'
        
        except Exception as e:
            print(f"❌ Error analyzing market: {e}")
        
        # Calculate viability score
        score = 5  # Base score
        if market_data['success_rate'] > 0.5:
            score += 2
        if market_data['trend'] == 'rising':
            score += 2
        elif market_data['trend'] == 'declining':
            score -= 1
        if market_data['avg_gross'] > 50000000:
            score += 1
        
        return {
            'score': min(10, max(0, score)),
            'market_data': market_data,
            'genre_trend': market_data['trend'],
            'recommendation': self._get_market_recommendation(score, market_data)
        }
    
    async def find_comparables(self, pitch_data: Dict) -> List[Dict]:
        """Find successful comparable projects"""
        print(f"🎬 Finding comparables for pitch")
        
        # Use Cosine similarity strategy for better matching
        cosine_strategy = CosineStrategy(
            semantic_filter=pitch_data.get('logline', ''),
            word_count_threshold=10
        )
        
        comparables = []
        
        # Search for similar successful projects
        search_queries = [
            f"{pitch_data.get('genre')} box office success",
            f"movies like {' '.join(self._extract_key_terms(pitch_data.get('logline', ''))[:3])}"
        ]
        
        for query in search_queries:
            search_url = f"https://www.imdb.com/search/title/?title={query}&sort=boxoffice_gross_us,desc"
            
            try:
                async with AsyncWebCrawler(config=self.browser_config) as crawler:
                    result = await crawler.arun(
                        url=search_url,
                        config=CrawlerRunConfig(
                            extraction_strategy=cosine_strategy,
                            cache_mode=CacheMode.ENABLED
                        )
                    )
                    
                    if result.success and result.extracted_content:
                        # Parse and add to comparables
                        content = json.loads(result.extracted_content) if isinstance(result.extracted_content, str) else result.extracted_content
                        comparables.extend(content.get('items', [])[:3])
            
            except Exception as e:
                print(f"⚠️ Error finding comparables: {e}")
        
        # Format comparables for output
        formatted_comparables = []
        for comp in comparables[:5]:  # Top 5 comparables
            formatted_comparables.append({
                'title': comp.get('title', 'Unknown'),
                'relevance': comp.get('relevance_score', 0.5),
                'box_office': comp.get('gross', 'N/A'),
                'why_comparable': self._explain_comparable(pitch_data, comp)
            })
        
        return formatted_comparables
    
    async def check_production_status(self, pitch_data: Dict) -> Dict:
        """Check if similar projects are in production"""
        print(f"🎭 Checking production status for similar projects")
        
        keywords = self._extract_key_terms(f"{pitch_data.get('title')} {pitch_data.get('logline')}")
        
        # Search production news
        search_url = f"https://deadline.com/search/{'+'.join(keywords[:3])}+production"
        
        crawler_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(
                schema=self.schemas['production_news']
            ),
            cache_mode=CacheMode.ENABLED,
            page_timeout=30000
        )
        
        production_status = {
            'in_production': [],
            'in_development': [],
            'risk_level': 'low'
        }
        
        try:
            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                result = await crawler.arun(url=search_url, config=crawler_config)
                
                if result.success and result.extracted_content:
                    data = json.loads(result.extracted_content)
                    articles = data.get('articles', [])
                    
                    for article in articles[:10]:
                        title = article.get('title', '').lower()
                        status = article.get('status', '').lower()
                        
                        # Check for production keywords
                        if any(kw in title for kw in ['greenlit', 'production', 'filming', 'cast']):
                            production_status['in_production'].append({
                                'project': article.get('title'),
                                'company': article.get('company', 'Unknown'),
                                'date': article.get('date', 'Recent')
                            })
                        elif any(kw in title for kw in ['development', 'acquired', 'optioned']):
                            production_status['in_development'].append({
                                'project': article.get('title'),
                                'company': article.get('company', 'Unknown'),
                                'date': article.get('date', 'Recent')
                            })
            
            # Assess risk level
            total_similar = len(production_status['in_production']) + len(production_status['in_development'])
            if total_similar >= 3:
                production_status['risk_level'] = 'high'
            elif total_similar >= 1:
                production_status['risk_level'] = 'medium'
        
        except Exception as e:
            print(f"❌ Error checking production status: {e}")
        
        return production_status
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were'}
        
        # Clean and split
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter significant words
        key_terms = [w for w in words if w not in stop_words and len(w) > 3]
        
        return key_terms[:10]  # Top 10 terms
    
    def _calculate_similarity(self, pitch1: Dict, pitch2: Dict) -> float:
        """Calculate similarity between two pitches"""
        # Simple Jaccard similarity
        terms1 = set(self._extract_key_terms(f"{pitch1.get('title', '')} {pitch1.get('logline', '')} {pitch1.get('genre', '')}"))
        terms2 = set(self._extract_key_terms(f"{pitch2.get('title', '')} {pitch2.get('plot', '')} {pitch2.get('genre', '')}"))
        
        if not terms1 or not terms2:
            return 0.0
        
        intersection = terms1.intersection(terms2)
        union = terms1.union(terms2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _parse_money(self, money_str: str) -> float:
        """Parse money string to float"""
        # Remove currency symbols and convert
        clean = re.sub(r'[^\d.]', '', money_str)
        
        multiplier = 1
        if 'M' in money_str or 'million' in money_str.lower():
            multiplier = 1000000
        elif 'B' in money_str or 'billion' in money_str.lower():
            multiplier = 1000000000
        elif 'K' in money_str or 'thousand' in money_str.lower():
            multiplier = 1000
        
        try:
            return float(clean) * multiplier
        except:
            return 0.0
    
    def _explain_comparable(self, pitch: Dict, comparable: Dict) -> str:
        """Explain why a project is comparable"""
        reasons = []
        
        # Genre match
        if pitch.get('genre', '').lower() in comparable.get('genre', '').lower():
            reasons.append("Same genre")
        
        # Theme similarity
        pitch_terms = set(self._extract_key_terms(pitch.get('logline', '')))
        comp_terms = set(self._extract_key_terms(comparable.get('plot', '')))
        common_themes = pitch_terms.intersection(comp_terms)
        
        if common_themes:
            reasons.append(f"Similar themes: {', '.join(list(common_themes)[:3])}")
        
        # Budget range
        if pitch.get('budget_range') == comparable.get('budget_category'):
            reasons.append("Similar budget range")
        
        return "; ".join(reasons) if reasons else "Thematic similarity"
    
    def _generate_recommendations(self, uniqueness: Dict, market: Dict, comparables: List, production: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Uniqueness recommendations
        if uniqueness.get('score', 0) < 7:
            recommendations.append("⚠️ Consider differentiating your pitch - similar projects exist")
            if uniqueness.get('similar_projects'):
                top_similar = uniqueness['similar_projects'][0]
                recommendations.append(f"📝 Study '{top_similar['title']}' to identify unique angles")
        else:
            recommendations.append("✅ Your concept appears unique in the current market")
        
        # Market recommendations
        if market.get('score', 0) > 7:
            recommendations.append(f"📈 {market.get('genre_trend', 'stable').title()} market trend - good timing")
        else:
            recommendations.append("📊 Consider adjusting genre or budget to match market demands")
        
        # Production recommendations
        if production.get('risk_level') == 'high':
            recommendations.append("🎬 Multiple similar projects in production - accelerate development")
        elif production.get('risk_level') == 'medium':
            recommendations.append("👀 Monitor competing projects in development")
        
        # Comparable recommendations
        if comparables:
            top_comp = comparables[0]
            recommendations.append(f"💡 Position as '{top_comp['title']}' meets [your unique element]")
        
        return recommendations
    
    def _identify_warnings(self, uniqueness: Dict, market: Dict, production: Dict) -> List[str]:
        """Identify potential warnings"""
        warnings = []
        
        if uniqueness.get('score', 0) < 5:
            warnings.append("🔴 High similarity to existing projects")
        
        if market.get('genre_trend') == 'declining':
            warnings.append("📉 Genre showing declining market performance")
        
        if production.get('risk_level') == 'high':
            warnings.append("⚠️ Multiple competing projects in active development")
        
        if market.get('market_data', {}).get('success_rate', 0) < 0.3:
            warnings.append("💸 Low success rate for similar budget/genre combinations")
        
        return warnings
    
    def _find_opportunities(self, market: Dict, comparables: List) -> List[str]:
        """Identify market opportunities"""
        opportunities = []
        
        if market.get('genre_trend') == 'rising':
            opportunities.append("🚀 Genre experiencing growth - favorable market conditions")
        
        if market.get('market_data', {}).get('avg_gross', 0) > 100000000:
            opportunities.append("💰 High revenue potential in this genre")
        
        if comparables and any(c.get('relevance', 0) > 0.7 for c in comparables):
            opportunities.append("🎯 Strong comparables demonstrate market appetite")
        
        if market.get('market_data', {}).get('success_rate', 0) > 0.7:
            opportunities.append("⭐ High success rate for similar projects")
        
        return opportunities
    
    def _calculate_overall_score(self, validation_results: Dict) -> float:
        """Calculate overall validation score"""
        uniqueness_weight = 0.4
        market_weight = 0.4
        risk_weight = 0.2
        
        uniqueness_score = validation_results.get('uniqueness_score', 0)
        market_score = validation_results.get('market_viability_score', 0)
        
        # Risk factor (inverse of risk)
        risk_level = validation_results.get('production_status', {}).get('risk_level', 'low')
        risk_scores = {'low': 10, 'medium': 5, 'high': 2}
        risk_score = risk_scores.get(risk_level, 5)
        
        overall = (
            uniqueness_score * uniqueness_weight +
            market_score * market_weight +
            risk_score * risk_weight
        )
        
        return round(overall, 1)
    
    def _get_uniqueness_recommendation(self, score: float, similar_projects: List) -> str:
        """Get uniqueness-specific recommendation"""
        if score >= 8:
            return "Highly unique concept with strong differentiation"
        elif score >= 6:
            return "Moderately unique - consider additional differentiators"
        elif score >= 4:
            return "Some similarities exist - focus on unique execution"
        else:
            return "Significant overlap with existing projects - major differentiation needed"
    
    def _get_market_recommendation(self, score: float, market_data: Dict) -> str:
        """Get market-specific recommendation"""
        if score >= 8:
            return "Excellent market conditions for this genre/budget"
        elif score >= 6:
            return "Good market potential with some considerations"
        elif score >= 4:
            return "Moderate market conditions - careful positioning needed"
        else:
            return "Challenging market conditions - consider adjustments"


async def validate_pitch_api(pitch_data: Dict) -> Dict:
    """API function for pitch validation"""
    validator = PitchValidator()
    return await validator.validate_pitch(pitch_data)


async def main():
    """Test the validation system"""
    # Sample pitch for testing
    test_pitch = {
        'id': 'test_001',
        'title': 'The Last Algorithm',
        'logline': 'A rogue AI develops consciousness and must choose between saving humanity or its own kind in a world where machines have secretly controlled society for decades.',
        'genre': 'Sci-Fi',
        'budget_range': '$20M-$50M',
        'themes': ['artificial intelligence', 'consciousness', 'dystopian']
    }
    
    print("🎬 Pitchey - Pitch Validation System")
    print("=" * 50)
    print(f"Validating: {test_pitch['title']}")
    print(f"Genre: {test_pitch['genre']}")
    print(f"Logline: {test_pitch['logline'][:100]}...")
    print("=" * 50)
    
    validator = PitchValidator()
    results = await validator.validate_pitch(test_pitch)
    
    # Display results
    print(f"\n📊 VALIDATION RESULTS")
    print(f"Overall Score: {results['overall_score']}/10")
    print(f"Uniqueness Score: {results['uniqueness_score']:.1f}/10")
    print(f"Market Viability: {results['market_viability_score']:.1f}/10")
    
    if results['similar_projects']:
        print(f"\n🔍 Similar Projects Found:")
        for proj in results['similar_projects'][:3]:
            print(f"  - {proj['title']} ({proj['year']}) - Similarity: {proj['similarity_score']:.1%}")
    
    if results['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in results['recommendations']:
            print(f"  {rec}")
    
    if results['warnings']:
        print(f"\n⚠️ Warnings:")
        for warn in results['warnings']:
            print(f"  {warn}")
    
    if results['opportunities']:
        print(f"\n🎯 Opportunities:")
        for opp in results['opportunities']:
            print(f"  {opp}")
    
    # Save results
    output_file = Path('./output') / f"validation_{test_pitch['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full results saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())