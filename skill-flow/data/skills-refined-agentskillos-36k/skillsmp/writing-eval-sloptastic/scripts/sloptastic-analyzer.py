#!/usr/bin/env python3
"""
Sloptastic - AI Writing Analyzer
Deterministic metrics calculator for detecting AI-generated prose patterns.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class TextStats:
    """Basic text statistics."""
    word_count: int
    sentence_count: int
    char_count: int

    @property
    def words_per_sentence(self) -> float:
        return self.word_count / max(self.sentence_count, 1)


@dataclass
class DeterministicMetrics:
    """Metrics that can be calculated without AI/NLP."""
    # Connector disease
    connector_phrases: List[Tuple[str, int]]  # (phrase, count)
    connector_percentage: float

    # Hedging language
    hedging_words: List[Tuple[str, int]]  # (word, count)
    hedging_count: int
    hedging_per_100_words: float

    # Universal quantifiers
    universal_quantifiers: List[Tuple[str, int]]  # (word, count)
    universal_count: int
    universal_per_100_words: float

    # Definitional tautologies
    tautology_patterns: List[str]  # Matched patterns
    tautology_count: int

    # Vague intensifiers
    vague_intensifiers: List[Tuple[str, int]]  # (pattern, count)
    intensifier_count: int

    # Platitudes (from known dictionary)
    detected_platitudes: List[Tuple[str, int]]  # (platitude, count)
    platitude_density: float  # Platitudes per sentence

    # Common AI phrases
    common_ai_phrases: List[Tuple[str, int]]  # (phrase, count)
    ai_phrase_count: int

    # Emoji patterns
    emoji_count: int
    emoji_as_bullets: bool  # Detected emojis used as structural elements

    # Contradiction patterns
    contradiction_pairs: List[str]  # Matched contradiction patterns
    contradiction_count: int


class SlopAnalyzer:
    """Analyzes text for AI slop patterns using deterministic methods."""

    # Connector phrases that indicate simulated coherence
    CONNECTORS = [
        "that's why", "that is why", "this is why",
        "that's because", "that is because", "this is because",
        "that's when", "that is when", "this is when",
        "that's how", "that is how", "this is how",
        "therefore", "thus", "hence", "consequently"
    ]

    # Hedging language - epistemic humility markers
    HEDGING_WORDS = [
        "maybe", "perhaps", "possibly", "probably",
        "might", "may", "could", "would", "should",
        "sometimes", "often", "usually", "generally",
        "tends to", "appears to", "seems to",
        "likely", "unlikely", "potential", "potentially",
        "arguably", "supposedly", "presumably"
    ]

    # Universal quantifiers - absolute claims
    UNIVERSAL_QUANTIFIERS = [
        "every", "all", "always", "never", "none",
        "every single", "each and every", "without exception",
        "absolutely", "completely", "totally", "entirely",
        "forever", "eternal", "constant", "invariably"
    ]

    # Vague intensifier patterns
    VAGUE_INTENSIFIERS = [
        r"real\s+\w+",  # "real provision", "real growth"
        r"true\s+\w+",  # "true understanding"
        r"natural\s+\w+",  # "natural growth"
        r"genuine\s+\w+",  # "genuine connection"
        r"authentic\s+\w+",  # "authentic experience"
    ]

    # Common platitudes dictionary
    PLATITUDES = [
        "stress is softened",
        "chaos becomes calm",
        "effort is turned into something meaningful",
        "growth feels natural",
        "multiply the life",
        "aligned with intention",
        "built with intention",
        "honor their role",
        "expanded, aligned, and built",
        "meets it at every level",
        "in ways money never could",
        "from the outside",
        "not flashy",
        "handled with care"
    ]

    # Common AI opening/transition phrases
    COMMON_AI_PHRASES = [
        "what impressed me most",
        "what struck me most",
        "what stands out most",
        "it's worth noting that",
        "it's important to note that",
        "it's interesting to note that",
        "at the end of the day",
        "the key takeaway is",
        "the bottom line is",
        "what's fascinating is",
        "what's remarkable is",
        "what's particularly interesting",
        "this is particularly important",
        "it's crucial to understand",
        "it's essential to recognize",
        "dive deep into",
        "delve into",
        "unpack this",
        "let's explore",
        "let's break this down",
        "here's the thing",
        "the reality is",
        "the truth is",
        "in today's world",
        "in today's landscape",
        "navigate the complexities",
        "it's no secret that",
        "goes without saying"
    ]

    # Definitional tautology patterns (X isn't just Y, it's Z)
    TAUTOLOGY_PATTERNS = [
        r"(\w+)\s+(?:isn't|is not|aren't|are not)\s+just\s+(\w+),?\s+(?:it's|it is|they're|they are)\s+(\w+)",
        r"(\w+)\s+doesn't\s+just\s+(\w+),?\s+(?:she|he|it|they)\s+(\w+)",
    ]

    # Contradiction patterns (claims quiet then loud)
    CONTRADICTION_PATTERNS = [
        (r"(quiet|subtle|not flashy|understated|modest)",
         r"(shows up in|it's felt in|manifests in|appears in)"),
    ]

    def __init__(self, text: str):
        """Initialize analyzer with text."""
        self.text = text
        self.text_lower = text.lower()
        self.stats = self._calculate_stats()

    def _calculate_stats(self) -> TextStats:
        """Calculate basic text statistics."""
        # Count words
        words = re.findall(r'\b\w+\b', self.text)
        word_count = len(words)

        # Count sentences (simplified - looks for . ! ?)
        sentences = re.split(r'[.!?]+', self.text)
        sentence_count = len([s for s in sentences if s.strip()])

        return TextStats(
            word_count=word_count,
            sentence_count=sentence_count,
            char_count=len(self.text)
        )

    def _count_phrases(self, phrases: List[str]) -> List[Tuple[str, int]]:
        """Count occurrences of phrases (case-insensitive)."""
        results = []
        for phrase in phrases:
            count = len(re.findall(re.escape(phrase), self.text_lower))
            if count > 0:
                results.append((phrase, count))
        return results

    def _count_patterns(self, patterns: List[str]) -> List[Tuple[str, int]]:
        """Count regex pattern matches."""
        results = []
        for pattern in patterns:
            matches = re.findall(pattern, self.text_lower)
            if matches:
                results.append((pattern, len(matches)))
        return results

    def analyze(self) -> DeterministicMetrics:
        """Run all deterministic analyses."""

        # 1. Connector disease
        connector_matches = self._count_phrases(self.CONNECTORS)
        connector_total = sum(count for _, count in connector_matches)
        connector_pct = (connector_total / self.stats.word_count) * 100 if self.stats.word_count > 0 else 0

        # 2. Hedging language
        hedging_matches = self._count_phrases(self.HEDGING_WORDS)
        hedging_total = sum(count for _, count in hedging_matches)
        hedging_per_100 = (hedging_total / self.stats.word_count) * 100 if self.stats.word_count > 0 else 0

        # 3. Universal quantifiers
        universal_matches = self._count_phrases(self.UNIVERSAL_QUANTIFIERS)
        universal_total = sum(count for _, count in universal_matches)
        universal_per_100 = (universal_total / self.stats.word_count) * 100 if self.stats.word_count > 0 else 0

        # 4. Definitional tautologies
        tautology_matches = []
        for pattern in self.TAUTOLOGY_PATTERNS:
            matches = re.findall(pattern, self.text_lower)
            for match in matches:
                tautology_matches.append(f"{match[0]} isn't just {match[1]}, it's {match[2]}")

        # 5. Vague intensifiers
        intensifier_matches = self._count_patterns(self.VAGUE_INTENSIFIERS)
        intensifier_total = sum(count for _, count in intensifier_matches)

        # 6. Platitudes
        platitude_matches = self._count_phrases(self.PLATITUDES)
        platitude_total = sum(count for _, count in platitude_matches)
        platitude_density = platitude_total / max(self.stats.sentence_count, 1)

        # 7. Common AI phrases
        ai_phrase_matches = self._count_phrases(self.COMMON_AI_PHRASES)
        ai_phrase_total = sum(count for _, count in ai_phrase_matches)

        # 8. Emoji patterns
        # Detect emojis (simple pattern matching for common emoji formats)
        emoji_pattern = r':[a-z_]+:|[\U0001F300-\U0001F9FF]|[\u2600-\u26FF]|[\u2700-\u27BF]'
        emoji_matches = re.findall(emoji_pattern, self.text)
        emoji_total = len(emoji_matches)

        # Detect if emojis are used as bullets (line starts with emoji or :emoji:)
        emoji_bullets = bool(re.search(r'(^|\n)\s*(?::[a-z_]+:|[\U0001F300-\U0001F9FF])', self.text, re.MULTILINE))

        # 9. Contradiction patterns
        contradiction_matches = []
        for quiet_pattern, loud_pattern in self.CONTRADICTION_PATTERNS:
            quiet_found = re.search(quiet_pattern, self.text_lower)
            if quiet_found:
                # Check if loud pattern appears within next 100 words
                pos = quiet_found.end()
                next_chunk = self.text_lower[pos:pos+500]
                loud_found = re.search(loud_pattern, next_chunk)
                if loud_found:
                    contradiction_matches.append(
                        f"'{quiet_found.group()}' followed by '{loud_found.group()}'"
                    )

        return DeterministicMetrics(
            connector_phrases=connector_matches,
            connector_percentage=connector_pct,
            hedging_words=hedging_matches,
            hedging_count=hedging_total,
            hedging_per_100_words=hedging_per_100,
            universal_quantifiers=universal_matches,
            universal_count=universal_total,
            universal_per_100_words=universal_per_100,
            tautology_patterns=tautology_matches,
            tautology_count=len(tautology_matches),
            vague_intensifiers=intensifier_matches,
            intensifier_count=intensifier_total,
            detected_platitudes=platitude_matches,
            platitude_density=platitude_density,
            common_ai_phrases=ai_phrase_matches,
            ai_phrase_count=ai_phrase_total,
            emoji_count=emoji_total,
            emoji_as_bullets=emoji_bullets,
            contradiction_pairs=contradiction_matches,
            contradiction_count=len(contradiction_matches)
        )

    def generate_report(self, metrics: DeterministicMetrics) -> str:
        """Generate a markdown report of deterministic metrics."""
        report = []

        report.append("# Deterministic Slop Metrics Report\n")

        # Text statistics
        report.append("## Text Statistics\n")
        report.append(f"- **Word count**: {self.stats.word_count}")
        report.append(f"- **Sentence count**: {self.stats.sentence_count}")
        report.append(f"- **Avg words/sentence**: {self.stats.words_per_sentence:.1f}\n")

        # Connector disease
        report.append("## 1. Connector Disease\n")
        report.append(f"**Total connectors**: {sum(c for _, c in metrics.connector_phrases)}")
        report.append(f"**Percentage of text**: {metrics.connector_percentage:.2f}%")
        report.append(f"**AI Tell**: >1.5% indicates simulated coherence\n")
        if metrics.connector_phrases:
            report.append("**Found connectors**:")
            for phrase, count in sorted(metrics.connector_phrases, key=lambda x: x[1], reverse=True):
                report.append(f"- '{phrase}': {count}")
        report.append("")

        # Hedging language
        report.append("## 2. Hedging Language Absence\n")
        report.append(f"**Total hedging words**: {metrics.hedging_count}")
        report.append(f"**Per 100 words**: {metrics.hedging_per_100_words:.2f}")
        report.append(f"**AI Tell**: <1 per 100 words indicates low epistemic humility\n")
        if metrics.hedging_words:
            report.append("**Found hedging words**:")
            for word, count in sorted(metrics.hedging_words, key=lambda x: x[1], reverse=True):
                report.append(f"- '{word}': {count}")
        else:
            report.append("**⚠️ ZERO hedging words found** - absolute certainty throughout")
        report.append("")

        # Universal quantifiers
        report.append("## 3. Universal Quantifiers\n")
        report.append(f"**Total universal quantifiers**: {metrics.universal_count}")
        report.append(f"**Per 100 words**: {metrics.universal_per_100_words:.2f}")
        report.append(f"**AI Tell**: >3 per 100 words indicates absolutism\n")
        if metrics.universal_quantifiers:
            report.append("**Found quantifiers**:")
            for word, count in sorted(metrics.universal_quantifiers, key=lambda x: x[1], reverse=True):
                report.append(f"- '{word}': {count}")
        report.append("")

        # Tautologies
        report.append("## 4. Definitional Tautologies\n")
        report.append(f"**Total tautology patterns**: {metrics.tautology_count}")
        report.append(f"**AI Tell**: >2 instances suggests strawman correction habit\n")
        if metrics.tautology_patterns:
            report.append("**Found patterns**:")
            for pattern in metrics.tautology_patterns:
                report.append(f"- {pattern}")
        report.append("")

        # Vague intensifiers
        report.append("## 5. Vague Intensifiers\n")
        report.append(f"**Total vague intensifiers**: {metrics.intensifier_count}")
        report.append(f"**AI Tell**: High frequency indicates abstraction without specificity\n")
        if metrics.vague_intensifiers:
            report.append("**Found patterns**:")
            for pattern, count in sorted(metrics.vague_intensifiers, key=lambda x: x[1], reverse=True):
                report.append(f"- Pattern '{pattern}': {count} matches")
        report.append("")

        # Platitudes
        report.append("## 6. Platitude Density\n")
        report.append(f"**Total platitudes detected**: {sum(c for _, c in metrics.detected_platitudes)}")
        report.append(f"**Platitudes per sentence**: {metrics.platitude_density:.2f}")
        report.append(f"**AI Tell**: >0.5 per sentence (1 per 2 sentences) indicates vapid language\n")
        if metrics.detected_platitudes:
            report.append("**Found platitudes**:")
            for platitude, count in sorted(metrics.detected_platitudes, key=lambda x: x[1], reverse=True):
                report.append(f"- '{platitude}': {count}")
        report.append("")

        # Common AI Phrases
        report.append("## 7. Common AI Phrases\n")
        report.append(f"**Total AI phrases detected**: {metrics.ai_phrase_count}")
        report.append(f"**AI Tell**: Presence of common AI opening/transition phrases\n")
        if metrics.common_ai_phrases:
            report.append("**Found AI phrases**:")
            for phrase, count in sorted(metrics.common_ai_phrases, key=lambda x: x[1], reverse=True):
                report.append(f"- '{phrase}': {count}")
        report.append("")

        # Emoji patterns
        report.append("## 8. Emoji Overuse as Structure\n")
        report.append(f"**Total emojis detected**: {metrics.emoji_count}")
        report.append(f"**Emojis as bullets**: {'Yes' if metrics.emoji_as_bullets else 'No'}")
        report.append(f"**AI Tell**: >3 mechanical emojis or emojis as structural bullets\n")
        if metrics.emoji_count > 0:
            if metrics.emoji_as_bullets:
                report.append("**⚠️ Emojis detected as structural elements (bullet points)**")
            if metrics.emoji_count >= 3:
                report.append(f"**⚠️ High emoji count ({metrics.emoji_count}) suggests mechanical usage**")
        report.append("")

        # Contradictions
        report.append("## 9. Contradiction Patterns\n")
        report.append(f"**Total contradictions**: {metrics.contradiction_count}")
        report.append(f"**AI Tell**: Claims of subtlety followed by obvious manifestations\n")
        if metrics.contradiction_pairs:
            report.append("**Found contradictions**:")
            for pair in metrics.contradiction_pairs:
                report.append(f"- {pair}")
        report.append("")

        # Summary
        report.append("## Summary of AI Tells\n")
        ai_tells = []

        if metrics.connector_percentage > 1.5:
            ai_tells.append(f"✗ High connector density ({metrics.connector_percentage:.1f}%)")

        if metrics.hedging_count == 0:
            ai_tells.append("✗ ZERO hedging language (absolute certainty)")
        elif metrics.hedging_per_100_words < 1.0:
            ai_tells.append(f"✗ Low hedging ({metrics.hedging_per_100_words:.1f} per 100 words)")

        if metrics.universal_per_100_words > 3.0:
            ai_tells.append(f"✗ High universal quantifiers ({metrics.universal_per_100_words:.1f} per 100 words)")

        if metrics.tautology_count > 2:
            ai_tells.append(f"✗ Multiple tautologies ({metrics.tautology_count})")

        if metrics.platitude_density > 0.5:
            ai_tells.append(f"✗ High platitude density ({metrics.platitude_density:.2f} per sentence)")

        if metrics.ai_phrase_count > 0:
            ai_tells.append(f"✗ Common AI phrases detected ({metrics.ai_phrase_count})")

        if metrics.emoji_count >= 3 or metrics.emoji_as_bullets:
            emoji_note = f"✗ Emoji overuse as structure ({metrics.emoji_count} emojis"
            if metrics.emoji_as_bullets:
                emoji_note += ", used as bullets"
            emoji_note += ")"
            ai_tells.append(emoji_note)

        if metrics.contradiction_count > 0:
            ai_tells.append(f"✗ Contradiction patterns detected ({metrics.contradiction_count})")

        if ai_tells:
            for tell in ai_tells:
                report.append(tell)
        else:
            report.append("✓ No major AI tells detected in deterministic metrics")

        report.append("\n---\n")
        report.append("**Note**: This report covers only deterministic metrics. ")
        report.append("For complete analysis, use the full sloptastic framework including:")
        report.append("- Parallel construction density (requires parsing)")
        report.append("- Concrete vs abstract noun ratio (requires NLP)")
        report.append("- Chiasmus detection (requires structure analysis)")
        report.append("- Emotional labor asymmetry (requires subject-verb analysis)")

        return "\n".join(report)


def main():
    """CLI interface for the sloptastic analyzer."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python sloptastic-analyzer.py <text_file>")
        print("   or: python sloptastic-analyzer.py --stdin")
        sys.exit(1)

    # Read input
    if sys.argv[1] == "--stdin":
        text = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()

    # Analyze
    analyzer = SlopAnalyzer(text)
    metrics = analyzer.analyze()
    report = analyzer.generate_report(metrics)

    # Output
    print(report)


if __name__ == "__main__":
    main()
