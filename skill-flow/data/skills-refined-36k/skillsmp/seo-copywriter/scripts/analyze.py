#!/usr/bin/env python3
"""SEO text analysis script - analyzes text for copywriting metrics."""

import re
import sys
from collections import Counter
from pathlib import Path

# Common passive voice indicators
PASSIVE_INDICATORS = [
    r'\b(am|is|are|was|were|be|been|being)\s+\w+ed\b',
    r'\b(am|is|are|was|were|be|been|being)\s+\w+en\b',
]

# Stopwords to exclude from keyword analysis
STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
    'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
    'shall', 'can', 'need', 'dare', 'ought', 'used', 'it', 'its', 'this', 'that',
    'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they', 'what', 'which', 'who',
    'whom', 'whose', 'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
    'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there', 'then',
    'once', 'if', 'about', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'between', 'under', 'again', 'further', 'while', 'up', 'down', 'out',
    'off', 'over', 'any', 'your', 'our', 'my', 'his', 'her', 'their', 'am', 'being',
}

# Power words that trigger emotional response
POWER_WORDS = {
    'urgency': ['now', 'hurry', 'instant', 'immediately', 'fast', 'quick', 'limited', 'deadline', 'urgent', 'today'],
    'exclusivity': ['exclusive', 'members', 'only', 'limited', 'private', 'secret', 'insider', 'vip'],
    'trust': ['guaranteed', 'proven', 'certified', 'official', 'authentic', 'verified', 'trusted', 'secure', 'safe'],
    'value': ['free', 'bonus', 'save', 'discount', 'deal', 'bargain', 'affordable', 'cheap', 'value'],
    'curiosity': ['secret', 'discover', 'revealed', 'hidden', 'unlock', 'mystery', 'surprising', 'shocking'],
    'emotion': ['amazing', 'incredible', 'powerful', 'remarkable', 'stunning', 'breakthrough', 'revolutionary'],
}

def count_syllables(word):
    """Estimate syllable count for readability calculation."""
    word = word.lower()
    if len(word) <= 3:
        return 1
    word = re.sub(r'(es|ed|e)$', '', word)
    vowels = re.findall(r'[aeiouy]+', word)
    return max(1, len(vowels))

def analyze_text(text):
    """Analyze text and return SEO metrics."""
    results = {}

    # Clean text
    clean_text = text.strip()

    # 1. Character counts
    chars_with_spaces = len(clean_text.replace('\n', ''))
    chars_no_spaces = len(clean_text.replace('\n', '').replace(' ', ''))
    results['characters'] = {
        'with_spaces': chars_with_spaces,
        'without_spaces': chars_no_spaces,
    }

    # 2. Word analysis
    words = re.findall(r'\b[a-zA-Z]+\b', clean_text.lower())
    word_count = len(words)
    word_freq = Counter(words)

    results['word_count'] = word_count
    results['unique_words'] = len(word_freq)

    # Keyword frequency (excluding stopwords) - these are SEO-relevant
    keywords = [w for w in words if w not in STOPWORDS]
    keyword_freq = Counter(keywords)
    keyword_count = len(keywords)

    results['keyword_count'] = keyword_count
    results['keyword_frequency'] = [
        {'word': word, 'count': count, 'percent': round(count / word_count * 100, 1)}
        for word, count in keyword_freq.most_common(20)
    ]

    # 3. Word pairs (bigrams)
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    bigram_freq = Counter(bigrams)
    results['word_pairs'] = [
        {'phrase': phrase, 'count': count}
        for phrase, count in bigram_freq.most_common(15)
        if count > 1
    ]

    # 4. Word triples (trigrams)
    trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
    trigram_freq = Counter(trigrams)
    results['word_triples'] = [
        {'phrase': phrase, 'count': count}
        for phrase, count in trigram_freq.most_common(10)
        if count > 1
    ]

    # 5. Sentence analysis
    sentences = re.split(r'[.!?]+', clean_text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]

    if sentence_lengths:
        results['sentences'] = {
            'count': len(sentences),
            'avg_length': round(sum(sentence_lengths) / len(sentence_lengths), 1),
            'min_length': min(sentence_lengths),
            'max_length': max(sentence_lengths),
            'long_sentences': sum(1 for l in sentence_lengths if l > 25),
        }

    # 6. Paragraph analysis
    paragraphs = [p.strip() for p in clean_text.split('\n\n') if p.strip()]
    para_lengths = [len(re.findall(r'\b\w+\b', p)) for p in paragraphs]

    if para_lengths:
        results['paragraphs'] = {
            'count': len(paragraphs),
            'avg_length': round(sum(para_lengths) / len(para_lengths), 1),
            'long_paragraphs': sum(1 for l in para_lengths if l > 100),
        }

    # 7. Readability (Flesch-Kincaid Grade Level)
    if word_count > 0 and len(sentences) > 0:
        total_syllables = sum(count_syllables(w) for w in words)
        fk_grade = 0.39 * (word_count / len(sentences)) + 11.8 * (total_syllables / word_count) - 15.59
        fk_ease = 206.835 - 1.015 * (word_count / len(sentences)) - 84.6 * (total_syllables / word_count)
        fk_grade = round(max(0, fk_grade), 1)
        fk_ease = round(min(100, max(0, fk_ease)), 1)

        # Interpret grade level
        if fk_grade <= 6:
            grade_rating = "Excellent (elementary)"
        elif fk_grade <= 8:
            grade_rating = "Good (middle school)"
        elif fk_grade <= 10:
            grade_rating = "OK (high school)"
        elif fk_grade <= 12:
            grade_rating = "Difficult (college)"
        else:
            grade_rating = "Very difficult (graduate)"

        # Interpret ease score
        if fk_ease >= 80:
            ease_rating = "Very easy"
        elif fk_ease >= 60:
            ease_rating = "Easy - ideal for web"
        elif fk_ease >= 50:
            ease_rating = "Fairly easy"
        elif fk_ease >= 30:
            ease_rating = "Difficult"
        else:
            ease_rating = "Very difficult"

        results['readability'] = {
            'flesch_kincaid_grade': fk_grade,
            'grade_rating': grade_rating,
            'flesch_ease': fk_ease,
            'ease_rating': ease_rating,
            'avg_syllables_per_word': round(total_syllables / word_count, 2),
        }

    # 8. Passive voice detection
    passive_count = sum(len(re.findall(p, clean_text, re.IGNORECASE)) for p in PASSIVE_INDICATORS)
    results['passive_voice'] = {
        'count': passive_count,
        'percent': round(passive_count / len(sentences) * 100, 1) if sentences else 0,
    }

    # 9. Power words analysis
    power_word_matches = {}
    total_power = 0
    for category, word_list in POWER_WORDS.items():
        matches = [w for w in words if w in word_list]
        if matches:
            power_word_matches[category] = Counter(matches).most_common()
            total_power += len(matches)

    results['power_words'] = {
        'total': total_power,
        'percent': round(total_power / word_count * 100, 2) if word_count else 0,
        'by_category': power_word_matches,
    }

    # 10. Questions count
    questions = len(re.findall(r'\?', clean_text))
    results['questions'] = questions

    # 11. SEO recommendations
    results['recommendations'] = []

    if results.get('readability', {}).get('flesch_kincaid_grade', 0) > 12:
        results['recommendations'].append("Simplify language - grade level too high for web content")

    if results.get('sentences', {}).get('avg_length', 0) > 20:
        results['recommendations'].append("Shorten sentences - aim for 15-20 words average")

    if results.get('sentences', {}).get('long_sentences', 0) > 0:
        results['recommendations'].append(f"Break up {results['sentences']['long_sentences']} long sentences (>25 words)")

    if results.get('paragraphs', {}).get('long_paragraphs', 0) > 0:
        results['recommendations'].append(f"Split {results['paragraphs']['long_paragraphs']} long paragraphs (>100 words)")

    if results.get('passive_voice', {}).get('percent', 0) > 15:
        results['recommendations'].append("Reduce passive voice - aim for <15%")

    if results.get('power_words', {}).get('percent', 0) < 1:
        results['recommendations'].append("Add more power words for emotional impact")

    if questions == 0 and word_count > 100:
        results['recommendations'].append("Consider adding questions to engage readers")

    return results

def format_output(results):
    """Format results for display."""
    lines = []

    lines.append("=" * 60)
    lines.append("SEO TEXT ANALYSIS")
    lines.append("=" * 60)

    # Basic counts
    lines.append(f"\n📊 BASIC METRICS")
    lines.append(f"   Words: {results['word_count']} | Keywords: {results['keyword_count']} | Unique: {results['unique_words']}")
    lines.append(f"   Characters: {results['characters']['with_spaces']} (with spaces) | {results['characters']['without_spaces']} (no spaces)")

    # Sentences
    if 'sentences' in results:
        s = results['sentences']
        lines.append(f"\n📝 SENTENCES ({s['count']} total)")
        lines.append(f"   Length: avg {s['avg_length']} | min {s['min_length']} | max {s['max_length']}")
        if s['long_sentences']:
            lines.append(f"   ⚠️  Long sentences (>25 words): {s['long_sentences']}")

    # Paragraphs
    if 'paragraphs' in results:
        p = results['paragraphs']
        lines.append(f"\n📄 PARAGRAPHS ({p['count']} total)")
        lines.append(f"   Avg length: {p['avg_length']} words")

    # Readability
    if 'readability' in results:
        r = results['readability']
        lines.append(f"\n📖 READABILITY")
        lines.append(f"   Grade Level: {r['flesch_kincaid_grade']} - {r['grade_rating']}")
        lines.append(f"   Ease Score: {r['flesch_ease']} - {r['ease_rating']}")
        lines.append(f"   Avg syllables/word: {r['avg_syllables_per_word']}")
        lines.append(f"   (Web copy target: Grade 6-8, Ease 60-80)")

    # Passive voice
    pv = results['passive_voice']
    lines.append(f"\n🔄 PASSIVE VOICE")
    lines.append(f"   Instances: {pv['count']} ({pv['percent']}% of sentences)")

    # Power words
    pw = results['power_words']
    lines.append(f"\n⚡ POWER WORDS ({pw['total']} total, {pw['percent']}%)")
    for cat, words in pw['by_category'].items():
        word_str = ', '.join(f"{w}({c})" for w, c in words[:5])
        lines.append(f"   {cat}: {word_str}")

    # Questions
    lines.append(f"\n❓ QUESTIONS: {results['questions']}")

    # Keyword frequency (stopwords excluded)
    lines.append(f"\n📈 TOP KEYWORDS - stopwords excluded (count, %)")
    for item in results['keyword_frequency'][:10]:
        lines.append(f"   {item['word']}: {item['count']} ({item['percent']}%)")

    # Word pairs
    if results['word_pairs']:
        lines.append(f"\n🔗 WORD PAIRS")
        for item in results['word_pairs'][:8]:
            lines.append(f"   '{item['phrase']}': {item['count']}")

    # Word triples
    if results['word_triples']:
        lines.append(f"\n🔗 WORD TRIPLES")
        for item in results['word_triples'][:5]:
            lines.append(f"   '{item['phrase']}': {item['count']}")

    # Recommendations
    if results['recommendations']:
        lines.append(f"\n💡 RECOMMENDATIONS")
        for rec in results['recommendations']:
            lines.append(f"   • {rec}")
    else:
        lines.append(f"\n✅ No major issues detected")

    lines.append("\n" + "=" * 60)

    return '\n'.join(lines)

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        # Read from stdin if no file provided
        if not sys.stdin.isatty():
            text = sys.stdin.read()
        else:
            print("Usage: analyze.py <file> or pipe text via stdin")
            print("Example: analyze.py content.txt")
            print("Example: echo 'text' | analyze.py -")
            sys.exit(1)
    elif sys.argv[1] == '-':
        text = sys.stdin.read()
    else:
        filepath = Path(sys.argv[1])
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            sys.exit(1)
        text = filepath.read_text()

    results = analyze_text(text)
    print(format_output(results))

if __name__ == '__main__':
    main()
