#!/usr/bin/env python3
"""
Source Evaluator Module - Evaluate and filter sources by trustworthiness

Phase 2 Enhancement: 소스 신뢰도 기반 필터링으로 리서치 품질 향상
"""

import re
import logging
from typing import List, Dict, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class SourceEvaluator:
    """Evaluates source trustworthiness and filters low-quality sources.
    
    Scoring system:
    - 0.9+: Academic, official documentation
    - 0.7-0.9: Reputable tech sources
    - 0.5-0.7: General sources
    - 0.3-0.5: User-generated content
    - <0.3: Low trust sources
    """
    
    # High trust domains with their scores
    HIGH_TRUST_DOMAINS: Dict[str, float] = {
        # Academic
        "arxiv.org": 0.95,
        "scholar.google.com": 0.95,
        "acm.org": 0.95,
        "ieee.org": 0.95,
        "nature.com": 0.95,
        "science.org": 0.95,
        
        # Official documentation
        "docs.python.org": 0.90,
        "developer.mozilla.org": 0.90,
        "docs.microsoft.com": 0.90,
        "cloud.google.com": 0.90,
        "docs.aws.amazon.com": 0.90,
        "kubernetes.io": 0.90,
        "reactjs.org": 0.90,
        
        # Reputable tech sources
        "github.com": 0.85,
        "stackoverflow.com": 0.80,
        "hackernews.com": 0.75,
        "dev.to": 0.70,
        "thenewstack.io": 0.75,
        "infoq.com": 0.75,
        
        # News and analysis
        "techcrunch.com": 0.70,
        "wired.com": 0.70,
        "arstechnica.com": 0.75,
        "theregister.com": 0.70,
    }
    
    # Low trust patterns (regex)
    LOW_TRUST_PATTERNS: List[Tuple[str, float]] = [
        (r".*\.blogspot\.com", 0.35),
        (r".*\.wordpress\.com", 0.35),
        (r"medium\.com/@[^/]+$", 0.40),  # Personal medium blogs
        (r".*\.tumblr\.com", 0.30),
        (r".*\.weebly\.com", 0.30),
        (r"quora\.com", 0.45),
        (r"reddit\.com", 0.50),  # Can be useful but variable quality
    ]
    
    # Medium trust patterns (specific subdomains/paths)
    MEDIUM_TRUST_PATTERNS: List[Tuple[str, float]] = [
        (r"medium\.com/[^@]", 0.60),  # Publication medium blogs
        (r".*\.github\.io", 0.65),  # GitHub pages (usually project docs)
        (r"blog\.", 0.55),  # Company blogs
    ]
    
    DEFAULT_SCORE = 0.50
    
    def __init__(self):
        """Initialize the source evaluator."""
        pass
    
    def evaluate(self, url: str) -> float:
        """Evaluate the trustworthiness of a URL.
        
        Args:
            url: URL to evaluate
            
        Returns:
            Trust score between 0.0 and 1.0
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            full_url = url.lower()
            
            # Check high trust domains first
            for trusted_domain, score in self.HIGH_TRUST_DOMAINS.items():
                if trusted_domain in domain:
                    logger.debug(f"High trust match: {trusted_domain} -> {score}")
                    return score
            
            # Check low trust patterns
            for pattern, score in self.LOW_TRUST_PATTERNS:
                if re.match(pattern, full_url):
                    logger.debug(f"Low trust pattern match: {pattern} -> {score}")
                    return score
            
            # Check medium trust patterns
            for pattern, score in self.MEDIUM_TRUST_PATTERNS:
                if re.search(pattern, full_url):
                    logger.debug(f"Medium trust pattern match: {pattern} -> {score}")
                    return score
            
            # Default score for unknown domains
            return self.DEFAULT_SCORE
            
        except Exception as e:
            logger.warning(f"Error evaluating URL {url}: {e}")
            return self.DEFAULT_SCORE
    
    def filter_urls(
        self,
        urls: List[str],
        min_trust: float = 0.3
    ) -> List[str]:
        """Filter URLs by minimum trust score.
        
        Args:
            urls: List of URLs to filter
            min_trust: Minimum trust score (0.0 - 1.0)
            
        Returns:
            Filtered list of URLs meeting the threshold
        """
        filtered = []
        for url in urls:
            score = self.evaluate(url)
            if score >= min_trust:
                filtered.append(url)
            else:
                logger.info(f"Filtered out low-trust URL ({score:.2f}): {url}")
        
        return filtered
    
    def rank_urls(self, urls: List[str]) -> List[Tuple[str, float]]:
        """Rank URLs by trust score (highest first).
        
        Args:
            urls: List of URLs to rank
            
        Returns:
            List of (url, score) tuples sorted by score descending
        """
        scored = [(url, self.evaluate(url)) for url in urls]
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def get_evaluation_report(self, urls: List[str]) -> Dict:
        """Generate a detailed evaluation report for URLs.
        
        Args:
            urls: List of URLs to evaluate
            
        Returns:
            Report dictionary with statistics and per-URL scores
        """
        evaluations = [(url, self.evaluate(url)) for url in urls]
        scores = [score for _, score in evaluations]
        
        return {
            "total_urls": len(urls),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "high_trust": len([s for s in scores if s >= 0.7]),
            "medium_trust": len([s for s in scores if 0.4 <= s < 0.7]),
            "low_trust": len([s for s in scores if s < 0.4]),
            "evaluations": [
                {"url": url, "score": score, "tier": self._get_tier(score)}
                for url, score in evaluations
            ]
        }
    
    def _get_tier(self, score: float) -> str:
        """Get the trust tier for a score.
        
        Args:
            score: Trust score
            
        Returns:
            Tier name
        """
        if score >= 0.9:
            return "academic"
        elif score >= 0.7:
            return "reputable"
        elif score >= 0.5:
            return "general"
        elif score >= 0.3:
            return "user-generated"
        else:
            return "low-trust"


# Convenience function
def evaluate_source(url: str) -> float:
    """Evaluate a single URL's trustworthiness.
    
    Args:
        url: URL to evaluate
        
    Returns:
        Trust score (0.0 - 1.0)
    """
    evaluator = SourceEvaluator()
    return evaluator.evaluate(url)
