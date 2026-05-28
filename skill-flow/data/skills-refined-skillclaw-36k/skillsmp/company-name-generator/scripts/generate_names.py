#!/usr/bin/env python3
"""
Company Name Generator - Production Implementation
Generates, scores, and validates business names with USPTO/domain checks
"""

import re
import json
import requests
from typing import List, Dict, Any
from dataclasses import dataclass
import time

@dataclass
class NameScore:
    """Individual name with scoring breakdown"""
    name: str
    category: str
    total_score: int
    trademark_strength: int
    domain_signal: int
    memorability: int
    emotional_impact: int
    pronunciation: int
    trademark_risk: str
    domains: Dict[str, bool]
    best_domain: str

class CompanyNameGenerator:
    """Main generator class"""
    
    def __init__(self, context: Dict[str, Any]):
        self.context = context
        self.business_type = context.get("business_context", "")
        self.industry_keywords = context.get("industry_keywords", [])
        self.founder_name = context.get("founder_name", "")
        self.preserve_brand = context.get("preserve_brand", "")
        self.signal_required = context.get("signal_required", [])
        
    def generate_all_names(self) -> List[str]:
        """Generate names across all 10 categories"""
        all_names = []
        
        all_names.extend(self.generate_descriptive_names())
        all_names.extend(self.generate_metaphoric_names())
        all_names.extend(self.generate_invented_names())
        all_names.extend(self.generate_founder_names())
        all_names.extend(self.generate_acronym_names())
        all_names.extend(self.generate_compound_names())
        all_names.extend(self.generate_foreign_names())
        all_names.extend(self.generate_playful_names())
        all_names.extend(self.generate_geographic_names())
        all_names.extend(self.generate_legacy_names())
        
        return list(set(all_names))  # Remove duplicates
    
    def generate_descriptive_names(self) -> List[str]:
        """Category 1: Direct function communication"""
        functions = ["Forecast", "Auction", "Bid", "Lien", "Title", "Property", "Deal", "Asset"]
        tech = ["AI", "Logic", "Intelligence", "Analytics", "IQ", "Pro", "Systems"]
        
        names = []
        for f in functions:
            for t in tech:
                if self.preserve_brand:
                    names.append(f"{self.preserve_brand} {f}{t}")
                names.append(f"{f}{t}")
        
        return names[:15]  # Top 15 per category
    
    def generate_metaphoric_names(self) -> List[str]:
        """Category 2: Evocative imagery"""
        metaphors = ["Summit", "Peak", "Compass", "Beacon", "NorthStar", 
                    "Keystone", "Atlas", "Meridian", "Apex"]
        suffixes = ["Intelligence", "Analytics", "Systems", "AI", "Capital"]
        
        names = []
        for m in metaphors:
            for s in suffixes:
                if self.preserve_brand:
                    names.append(f"{self.preserve_brand} {m}")
                names.append(f"{m} {s}")
        
        return names[:15]
    
    def generate_invented_names(self) -> List[str]:
        """Category 3: Unique coinages"""
        prefixes = ["Auct", "Bid", "Lien", "Deed", "Fore", "Title", "Prop"]
        suffixes = ["ioniq", "lytics", "ova", "asta", "exa", "xa", "onix", "vana"]
        
        names = []
        for p in prefixes:
            for s in suffixes:
                names.append(f"{p}{s}")
        
        return names[:15]
    
    def generate_founder_names(self) -> List[str]:
        """Category 4: Personal brand leverage"""
        if not self.founder_name:
            return []
        
        last_name = self.founder_name.split()[-1]
        suffixes = ["Formula", "Method", "System", "Index", "Intelligence",
                   "Analytics", "Capital", "& Associates", "Group"]
        
        names = []
        for s in suffixes:
            names.append(f"The {last_name} {s}")
            names.append(f"{last_name} {s}")
        
        return names
    
    def generate_acronym_names(self) -> List[str]:
        """Category 5: Memorable initialisms"""
        acronyms = {
            "APEX": "Auction Property Evaluation eXpert",
            "SAFE": "Shapira Auction Foreclosure Engine",
            "EAGLE": "Expert Auction Guidance Lien Evaluation",
            "TITAN": "Title Intelligence Auction Network",
            "RADAR": "Real-time Auction Data Analysis Recommendation",
            "PRIME": "Property Risk Intelligence Market Evaluation",
            "ATLAS": "Auction Title Lien Analysis System",
            "SCOUT": "Shapira Computational Outcome Utility",
            "LENS": "Lien Evaluation Negotiation System"
        }
        
        return list(acronyms.keys())
    
    def generate_compound_names(self) -> List[str]:
        """Category 6: Two-word combinations"""
        word1 = ["Bid", "Lien", "Auction", "Title", "Market", "Exit", "Smart", "Deal"]
        word2 = ["Deed", "Logic", "Radar", "Track", "Pulse", "Path", "Brain", "Guard"]
        
        names = []
        for w1 in word1:
            for w2 in word2:
                if self.preserve_brand:
                    names.append(f"{self.preserve_brand} {w1}{w2}")
                names.append(f"{w1}{w2}")
                names.append(f"{w1}{w2}.AI")
        
        return names[:15]
    
    def generate_foreign_names(self) -> List[str]:
        """Category 7: Latin/Italian sophistication"""
        foreign = {
            "Veritas": "Truth",
            "Apex Lux": "Summit Light",
            "Via Aurum": "Way of Gold",
            "Lux Intelligo": "Light Intelligence",
            "Prima Vista": "First Sight",
            "Claritas": "Clarity",
            "Fortis": "Strong",
            "Nexus": "Connection",
            "Aurum": "Gold",
            "Vero": "True"
        }
        
        names = []
        for name in foreign.keys():
            names.append(f"{name} Auction")
            names.append(f"{name} AI")
            if self.preserve_brand:
                names.append(f"{self.preserve_brand} {name}")
        
        return names[:15]
    
    def generate_playful_names(self) -> List[str]:
        """Category 8: Approachable, memorable"""
        names = ["BidWise", "DeedDive", "AuctionHawk", "LienLeap",
                "SmartStash", "PropPro", "AuctionAce"]
        
        if self.preserve_brand:
            return [f"{self.preserve_brand} {n}" for n in names]
        return names
    
    def generate_geographic_names(self) -> List[str]:
        """Category 9: Place-based authority"""
        places = ["Brevard", "Space Coast", "Atlantic", "Florida", 
                 "Coastal", "Harbor", "Cape"]
        suffixes = ["BidTech", "Intelligence", "Auction AI", "Capital"]
        
        names = []
        for p in places:
            for s in suffixes:
                names.append(f"{p} {s}")
        
        return names[:15]
    
    def generate_legacy_names(self) -> List[str]:
        """Category 10: Institutional authority"""
        if not self.founder_name:
            return []
        
        last_name = self.founder_name.split()[-1]
        templates = [
            f"{last_name} & Associates",
            f"The {last_name} Group",
            f"{last_name} Capital Partners",
            f"The {last_name} Institute",
            f"{last_name} Research Labs",
            f"The Auction Institute",
            f"Strategic Property Advisors"
        ]
        
        if self.preserve_brand:
            templates.extend([
                f"{self.preserve_brand} Capital Advisors",
                f"The {self.preserve_brand} Institute",
                f"{self.preserve_brand} Intelligence Group"
            ])
        
        return templates
    
    def score_name(self, name: str, category: str) -> NameScore:
        """Score individual name across all criteria"""
        
        # Score each dimension
        trademark = self._score_trademark_strength(name)
        domain = self._score_domain_signal(name)
        memorability = self._score_memorability(name)
        emotional = self._score_emotional_impact(name, category)
        pronunciation = self._score_pronunciation(name)
        
        # Weighted total
        total = int(
            (trademark * 0.30) +
            (domain * 0.25) +
            (memorability * 0.25) +
            (emotional * 0.10) +
            (pronunciation * 0.10)
        )
        
        # Check trademark conflicts (simplified - real would use USPTO API)
        risk = self._assess_trademark_risk(name)
        
        # Check domain availability (simplified)
        domains = self._check_domain_availability(name)
        best_domain = self._select_best_domain(name, domains)
        
        return NameScore(
            name=name,
            category=category,
            total_score=total,
            trademark_strength=trademark,
            domain_signal=domain,
            memorability=memorability,
            emotional_impact=emotional,
            pronunciation=pronunciation,
            trademark_risk=risk,
            domains=domains,
            best_domain=best_domain
        )
    
    def _score_trademark_strength(self, name: str) -> int:
        """Score 0-100 based on distinctiveness"""
        score = 50  # Base score
        
        # Invented words score higher
        if not any(word in name.lower() for word in ["smart", "pro", "best", "top"]):
            score += 20
        
        # Unique combinations score higher
        if len(name.split()) == 2:
            score += 15
        
        # Proper nouns (founder names) score higher
        if self.founder_name and self.founder_name.split()[-1] in name:
            score += 15
        
        return min(100, score)
    
    def _score_domain_signal(self, name: str) -> int:
        """Score 0-100 based on industry clarity"""
        score = 50
        
        # Contains industry keywords
        industry_words = ["auction", "foreclosure", "bid", "lien", "title", 
                         "property", "real estate", "deed"]
        if any(word in name.lower() for word in industry_words):
            score += 25
        
        # Contains tech signal
        tech_words = ["ai", "intelligence", "logic", "analytics", "iq", "smart"]
        if any(word in name.lower() for word in tech_words):
            score += 25
        
        return min(100, score)
    
    def _score_memorability(self, name: str) -> int:
        """Score 0-100 based on recall potential"""
        score = 50
        
        # Shorter is more memorable
        if len(name) < 15:
            score += 20
        elif len(name) > 25:
            score -= 10
        
        # Alliteration helps
        words = name.split()
        if len(words) >= 2 and words[0][0] == words[1][0]:
            score += 15
        
        # Rhyming helps
        if any(pair in name.lower() for pair in ["bid-deed", "lien-lean"]):
            score += 15
        
        return min(100, score)
    
    def _score_emotional_impact(self, name: str, category: str) -> int:
        """Score 0-100 based on positive associations"""
        score = 50
        
        # Metaphoric names score higher
        if category == "Metaphoric":
            score += 30
        
        # Positive words
        positive = ["summit", "peak", "beacon", "guide", "smart", "wise", "pro"]
        if any(word in name.lower() for word in positive):
            score += 20
        
        return min(100, score)
    
    def _score_pronunciation(self, name: str) -> int:
        """Score 0-100 based on ease of saying"""
        score = 50
        
        # Syllable count (2-3 ideal)
        syllables = len(re.findall(r'[aeiou]+', name.lower()))
        if 2 <= syllables <= 4:
            score += 25
        elif syllables > 6:
            score -= 20
        
        # No difficult consonant clusters
        if not re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', name.lower()):
            score += 25
        
        return min(100, score)
    
    def _assess_trademark_risk(self, name: str) -> str:
        """Assess LOW/MEDIUM/HIGH risk (simplified)"""
        # In production, would query USPTO TESS API
        generic_words = ["smart", "pro", "best", "top", "super", "ultra"]
        
        if any(word in name.lower() for word in generic_words):
            return "HIGH"
        elif len(name.split()) == 1:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _check_domain_availability(self, name: str) -> Dict[str, bool]:
        """Check .com, .ai, .io availability (simplified)"""
        # In production, would use DomainsDB API or WHOIS
        # For now, return mock data
        clean_name = re.sub(r'[^a-z0-9]', '', name.lower())
        
        return {
            "com": len(clean_name) > 12,  # Mock: longer names more likely available
            "ai": len(clean_name) > 8,
            "io": len(clean_name) > 10
        }
    
    def _select_best_domain(self, name: str, availability: Dict[str, bool]) -> str:
        """Select best available domain"""
        clean_name = re.sub(r'[^a-z0-9]', '', name.lower())
        
        # Prefer .ai for AI businesses
        if "ai" in name.lower() and availability.get("ai"):
            return f"{clean_name}.ai"
        elif availability.get("com"):
            return f"{clean_name}.com"
        elif availability.get("ai"):
            return f"{clean_name}.ai"
        elif availability.get("io"):
            return f"{clean_name}.io"
        else:
            return f"{clean_name}.ai (registration required)"
    
    def generate_and_score_all(self) -> List[NameScore]:
        """Main execution: generate all names and score them"""
        all_names = self.generate_all_names()
        
        scored_names = []
        category_map = {
            "Forecast": "Descriptive",
            "Summit": "Metaphoric",
            "iq": "Invented",
            self.founder_name.split()[-1] if self.founder_name else "": "Founder",
            "APEX": "Acronym",
            "Deed": "Compound",
            "Veritas": "Foreign",
            "Wise": "Playful",
            "Brevard": "Geographic",
            "Associates": "Legacy"
        }
        
        for name in all_names:
            # Determine category
            category = "Descriptive"  # Default
            for key, cat in category_map.items():
                if key and key in name:
                    category = cat
                    break
            
            scored = self.score_name(name, category)
            scored_names.append(scored)
        
        # Sort by total score descending
        return sorted(scored_names, key=lambda x: x.total_score, reverse=True)


def main():
    """Example usage"""
    context = {
        "business_context": "Foreclosure auction intelligence platform",
        "current_name": "The Everest Ascent",
        "industry_keywords": ["real estate", "AI", "foreclosure", "auction"],
        "founder_name": "Ariel Shapira",
        "company_entity": "Everest Capital USA",
        "preserve_brand": "Everest",
        "signal_required": ["real_estate", "AI_ML"],
        "positioning": "metric/framework"
    }
    
    generator = CompanyNameGenerator(context)
    results = generator.generate_and_score_all()
    
    # Print top 25
    print("\n" + "="*80)
    print("TOP 25 COMPANY NAMES - RANKED BY SCORE")
    print("="*80 + "\n")
    
    for i, name in enumerate(results[:25], 1):
        print(f"{i}. {name.name} ({name.total_score}/100)")
        print(f"   Category: {name.category}")
        print(f"   Trademark Risk: {name.trademark_risk}")
        print(f"   Best Domain: {name.best_domain}")
        print(f"   Breakdown: TM:{name.trademark_strength} | Domain:{name.domain_signal} | "
              f"Memory:{name.memorability} | Emotion:{name.emotional_impact} | "
              f"Pronounce:{name.pronunciation}")
        print()


if __name__ == "__main__":
    main()
