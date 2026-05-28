#!/usr/bin/env python3
"""
Company Name Generator - Core Generation Engine
Generates business names across 10 categories with scoring
"""

import json
import re
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class NameCandidate:
    name: str
    category: str
    trademark_score: int
    domain_signal_score: int
    tech_signal_score: int
    metaphor_score: int
    pronunciation_score: int
    
    @property
    def total_score(self) -> int:
        return int(
            (self.trademark_score * 0.30) +
            (self.domain_signal_score * 0.25) +
            (self.tech_signal_score * 0.25) +
            (self.metaphor_score * 0.10) +
            (self.pronunciation_score * 0.10)
        )
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'category': self.category,
            'scores': {
                'trademark': self.trademark_score,
                'domain_signal': self.domain_signal_score,
                'tech_signal': self.tech_signal_score,
                'metaphor': self.metaphor_score,
                'pronunciation': self.pronunciation_score,
                'total': self.total_score
            }
        }


class NameGenerator:
    """Generate names across 10 categories"""
    
    def __init__(self, industry: str, signals: List[str], existing_brand: str = None):
        self.industry = industry
        self.signals = signals
        self.existing_brand = existing_brand
        
    def generate_all(self) -> List[NameCandidate]:
        """Generate names across all 10 categories"""
        all_names = []
        
        all_names.extend(self.generate_descriptive())
        all_names.extend(self.generate_metaphoric())
        all_names.extend(self.generate_invented())
        all_names.extend(self.generate_founder_based())
        all_names.extend(self.generate_acronym())
        all_names.extend(self.generate_compound())
        all_names.extend(self.generate_foreign())
        all_names.extend(self.generate_playful())
        all_names.extend(self.generate_geographic())
        all_names.extend(self.generate_legacy())
        
        return all_names
    
    def score_name(self, name: str, category: str) -> NameCandidate:
        """Score a name across all criteria"""
        return NameCandidate(
            name=name,
            category=category,
            trademark_score=self._score_trademark(name),
            domain_signal_score=self._score_domain_signal(name),
            tech_signal_score=self._score_tech_signal(name),
            metaphor_score=self._score_metaphor(name, category),
            pronunciation_score=self._score_pronunciation(name)
        )
    
    def _score_trademark(self, name: str) -> int:
        """Score trademark strength (higher = more distinctive)"""
        # Invented words score highest
        if not any(word in name.lower() for word in ['the', 'and', 'of', 'for']):
            # Count syllables and uniqueness
            word_count = len(name.split())
            if word_count == 1 and len(name) > 6:
                return 95  # Single invented word
            elif word_count == 2:
                return 85  # Compound
        
        # Common words score lower
        common_words = ['smart', 'pro', 'plus', 'max', 'tech', 'data']
        if any(word in name.lower() for word in common_words):
            return 70
        
        return 80  # Default decent score
    
    def _score_domain_signal(self, name: str) -> int:
        """Score how well name signals industry/domain"""
        name_lower = name.lower()
        
        # Explicit industry terms
        explicit = ['auction', 'foreclosure', 'lien', 'title', 'deed', 'bid', 'property']
        if any(term in name_lower for term in explicit):
            return 95
        
        # Clear with context
        clear = ['forecast', 'market', 'capital', 'asset', 'real estate']
        if any(term in name_lower for term in clear):
            return 85
        
        # Implied
        implied = ['intelligence', 'analytics', 'insights', 'edge']
        if any(term in name_lower for term in implied):
            return 70
        
        return 60  # Generic
    
    def _score_tech_signal(self, name: str) -> int:
        """Score AI/ML/tech signal strength"""
        name_lower = name.lower()
        
        # Explicit AI/ML
        if any(term in name_lower for term in ['ai', ' ml', 'algorithm', 'neural', 'intelligence']):
            return 100
        
        # Strong tech
        if name_lower.endswith('.ai') or 'analytics' in name_lower or 'logic' in name_lower:
            return 90
        
        # Tech-forward
        if any(term in name_lower for term in ['smart', 'auto', 'cognitive', 'predict']):
            return 80
        
        # Implied
        if any(term in name_lower for term in ['systems', 'platform', 'engine']):
            return 70
        
        return 60  # No signal
    
    def _score_metaphor(self, name: str, category: str) -> int:
        """Score metaphorical power"""
        if category == 'metaphoric':
            # High metaphor categories get bonus
            metaphor_words = ['summit', 'compass', 'beacon', 'oracle', 'atlas', 
                            'radar', 'eagle', 'keystone', 'apex', 'peak']
            if any(word in name.lower() for word in metaphor_words):
                return 95
            return 85
        elif category in ['invented', 'acronym']:
            return 70  # Neutral
        else:
            return 60  # Literal
    
    def _score_pronunciation(self, name: str) -> int:
        """Score ease of pronunciation"""
        # Remove spaces and special chars
        clean = re.sub(r'[^a-zA-Z]', '', name)
        syllables = self._count_syllables(clean)
        
        if syllables <= 2:
            return 95
        elif syllables == 3:
            return 85
        elif syllables == 4:
            return 75
        else:
            return 65
    
    def _count_syllables(self, word: str) -> int:
        """Rough syllable counter"""
        word = word.lower()
        count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e'):
            count -= 1
        
        return max(1, count)
    
    # Category generators
    def generate_descriptive(self) -> List[NameCandidate]:
        """Generate descriptive names"""
        templates = [
            "{signal}Logic",
            "{signal}Intel",
            "{signal}Analytics",
            "{domain} Intelligence",
            "Smart{domain}",
            "{domain}Predict",
            "{signal}Systems",
            "{domain}{signal}Pro"
        ]
        
        return self._generate_from_templates(templates, 'descriptive')
    
    def generate_metaphoric(self) -> List[NameCandidate]:
        """Generate metaphoric names"""
        metaphors = ['Summit', 'Compass', 'Beacon', 'Oracle', 'Atlas', 'Keystone', 
                     'Meridian', 'Apex', 'NorthStar', 'Horizon']
        
        if self.existing_brand:
            names = [f"{self.existing_brand} {m}" for m in metaphors]
        else:
            names = [f"{m} Intelligence" for m in metaphors]
        
        return [self.score_name(name, 'metaphoric') for name in names]
    
    def generate_invented(self) -> List[NameCandidate]:
        """Generate invented/coined names"""
        # Portmanteaus and unique coinages
        names = [
            "Auctioniq",
            "Bidlytics", 
            "Lienova",
            "Forecasta",
            "Deedex",
            "Titlexa",
            "Auctronix",
            "Propteq",
            "Lienix"
        ]
        
        return [self.score_name(name, 'invented') for name in names]
    
    def generate_founder_based(self) -> List[NameCandidate]:
        """Generate founder-based names"""
        # These would use actual founder name from context
        return [
            self.score_name("The Shapira Formula™", 'founder-based'),
            self.score_name("Shapira Intelligence", 'founder-based'),
            self.score_name("Shapira Systems", 'founder-based'),
            self.score_name("Shapira Analytics", 'founder-based'),
        ]
    
    def generate_acronym(self) -> List[NameCandidate]:
        """Generate acronym names"""
        acronyms = [
            ("APEX", "Auction Property Evaluation eXpert"),
            ("SAFE", "Shapira Auction Foreclosure Engine"),
            ("EAGLE", "Expert Auction Guidance Lien Evaluation"),
            ("RADAR", "Real-time Auction Data Analysis Recommendation"),
            ("PRIME", "Property Risk Intelligence Market Evaluation")
        ]
        
        return [self.score_name(acro[0], 'acronym') for acro in acronyms]
    
    def generate_compound(self) -> List[NameCandidate]:
        """Generate compound two-word names"""
        if self.existing_brand:
            compounds = [
                f"{self.existing_brand}Logic",
                f"{self.existing_brand}Intel",
                f"{self.existing_brand} ForecastAI",
                f"{self.existing_brand} BidIntelligence"
            ]
        else:
            compounds = [
                "BidDeed.AI",
                "LienLogic",
                "TitleTrack",
                "MarketPulse",
                "SmartBid"
            ]
        
        return [self.score_name(name, 'compound') for name in compounds]
    
    def generate_foreign(self) -> List[NameCandidate]:
        """Generate foreign language names"""
        names = [
            "Veritas Auction",  # Latin: Truth
            "Apex Lux",  # Latin: Summit Light
            "Prima Vista",  # Italian: First Sight
            "Claritas AI",  # Latin: Clarity
            "Aurum Logic"  # Latin: Gold
        ]
        
        return [self.score_name(name, 'foreign') for name in names]
    
    def generate_playful(self) -> List[NameCandidate]:
        """Generate playful/approachable names"""
        names = [
            "BidWise",
            "DeedDive",
            "AuctionHawk",
            "LienLeap",
            "SmartStash"
        ]
        
        return [self.score_name(name, 'playful') for name in names]
    
    def generate_geographic(self) -> List[NameCandidate]:
        """Generate geographic names"""
        names = [
            "Brevard BidTech",
            "Space Coast Intelligence",
            "Atlantic Auction AI",
            "Coastal Capital AI"
        ]
        
        return [self.score_name(name, 'geographic') for name in names]
    
    def generate_legacy(self) -> List[NameCandidate]:
        """Generate legacy/institutional names"""
        names = [
            "Shapira & Associates",
            "The Shapira Group",
            "Shapira Capital Partners",
            "The Everest Institute"
        ]
        
        return [self.score_name(name, 'legacy') for name in names]
    
    def _generate_from_templates(self, templates: List[str], category: str) -> List[NameCandidate]:
        """Generate names from templates"""
        names = []
        
        for template in templates:
            # Replace placeholders
            for signal in self.signals[:3]:  # Use first 3 signals
                name = template.format(
                    signal=signal.capitalize(),
                    domain=self.industry.split()[0].capitalize()
                )
                names.append(self.score_name(name, category))
        
        return names


if __name__ == "__main__":
    # Example usage
    generator = NameGenerator(
        industry="foreclosure real estate",
        signals=["AI", "Forecast", "Auction", "Intelligence"],
        existing_brand="Everest"
    )
    
    all_names = generator.generate_all()
    
    # Sort by score
    all_names.sort(key=lambda x: x.total_score, reverse=True)
    
    # Output top 25
    print("# Top 25 Company Names\n")
    print("| Rank | Name | Category | Score | Trademark | Domain | Tech | Metaphor | Pronunciation |")
    print("|------|------|----------|-------|-----------|--------|------|----------|---------------|")
    
    for i, name in enumerate(all_names[:25], 1):
        print(f"| {i} | {name.name} | {name.category} | {name.total_score} | {name.trademark_score} | {name.domain_signal_score} | {name.tech_signal_score} | {name.metaphor_score} | {name.pronunciation_score} |")
