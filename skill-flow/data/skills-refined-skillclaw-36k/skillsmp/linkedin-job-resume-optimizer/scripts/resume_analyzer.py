#!/usr/bin/env python3
"""
Resume Analyzer
Extracts skills, experience, and keywords from base resume using NLP
"""

import re
import json
import argparse
import sys
from pathlib import Path

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Warning: spaCy not available. Using basic extraction only.")


def parse_resume_sections(markdown_text):
    """
    Parse resume markdown into sections (Skills, Experience, Education, Summary)
    """
    sections = {
        'summary': '',
        'skills': '',
        'experience': '',
        'education': ''
    }

    # Common section headers (case-insensitive)
    section_patterns = {
        'summary': r'(?:^|\n)#{1,2}\s*(Professional\s+Summary|Summary|Profile|Objective|About)',
        'skills': r'(?:^|\n)#{1,2}\s*(Skills|Technical\s+Skills|Core\s+Competencies|Technologies)',
        'experience': r'(?:^|\n)#{1,2}\s*(Experience|Work\s+Experience|Professional\s+Experience|Employment)',
        'education': r'(?:^|\n)#{1,2}\s*(Education|Academic\s+Background|Qualifications)'
    }

    # Find section boundaries
    section_positions = {}
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, markdown_text, re.IGNORECASE | re.MULTILINE)
        if match:
            section_positions[section_name] = match.start()

    # Extract section content
    sorted_positions = sorted(section_positions.items(), key=lambda x: x[1])

    for i, (section_name, start_pos) in enumerate(sorted_positions):
        # Find end position (start of next section or end of document)
        if i + 1 < len(sorted_positions):
            end_pos = sorted_positions[i + 1][1]
        else:
            end_pos = len(markdown_text)

        sections[section_name] = markdown_text[start_pos:end_pos].strip()

    return sections


def extract_explicit_skills(skills_text):
    """
    Extract skills from Skills section using pattern matching
    """
    skills = []

    # Remove section header
    skills_text = re.sub(r'^#{1,2}\s*.*?\n', '', skills_text, flags=re.MULTILINE)

    # Pattern 1: Bullet points (-, *, •)
    bullet_pattern = r'[•\-\*]\s*(.+?)(?:\n|$)'
    bullets = re.findall(bullet_pattern, skills_text)
    for bullet in bullets:
        # Split comma-separated skills within bullets
        bullet_skills = [s.strip() for s in re.split(r'[,;]', bullet) if s.strip()]
        skills.extend(bullet_skills)

    # Pattern 2: Comma-separated list (if no bullets found)
    if not skills:
        # Remove newlines and split by comma/semicolon
        flat_text = skills_text.replace('\n', ' ')
        comma_separated = [s.strip() for s in re.split(r'[,;]', flat_text) if s.strip()]
        skills.extend(comma_separated)

    # Pattern 3: Skill categories (e.g., "Programming: Python, Java")
    category_pattern = r'([A-Z][A-Za-z\s&]+):\s*([^:\n]+)'
    categories = re.findall(category_pattern, skills_text)
    for category, skill_list in categories:
        category_skills = [s.strip() for s in re.split(r'[,;]', skill_list) if s.strip()]
        skills.extend(category_skills)

    # Clean and deduplicate
    cleaned_skills = []
    seen = set()
    for skill in skills:
        # Remove parenthetical notes
        skill = re.sub(r'\([^)]*\)', '', skill).strip()
        # Remove trailing punctuation
        skill = skill.rstrip('.,;:')
        # Skip if empty or too short
        if len(skill) < 2 or len(skill) > 50:
            continue
        # Skip if already seen (case-insensitive)
        skill_lower = skill.lower()
        if skill_lower not in seen:
            seen.add(skill_lower)
            cleaned_skills.append(skill)

    return cleaned_skills


def extract_skills_from_experience(experience_text):
    """
    Use NLP and pattern matching to extract technical skills from experience descriptions
    """
    skills = []

    # Technical skill keywords (expandable)
    tech_keywords = {
        'programming': [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'SQL'
        ],
        'ml_frameworks': [
            'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'scikit-learn',
            'XGBoost', 'LightGBM', 'Hugging Face', 'OpenCV', 'NLTK', 'spaCy'
        ],
        'cloud': [
            'AWS', 'Azure', 'GCP', 'Google Cloud', 'Kubernetes', 'Docker',
            'Terraform', 'CloudFormation', 'Lambda', 'EC2', 'S3', 'Heroku'
        ],
        'databases': [
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'DynamoDB', 'Cassandra', 'Neo4j', 'SQLite', 'Oracle', 'SQL Server'
        ],
        'tools': [
            'Git', 'GitHub', 'GitLab', 'Jenkins', 'CI/CD', 'MLOps', 'DevOps',
            'Airflow', 'Spark', 'Hadoop', 'Kafka', 'RabbitMQ', 'Pandas', 'NumPy'
        ],
        'web': [
            'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask',
            'FastAPI', 'Spring', 'REST', 'GraphQL', 'HTML', 'CSS'
        ]
    }

    # Flatten all keywords
    all_keywords = []
    for category, keywords in tech_keywords.items():
        for keyword in keywords:
            all_keywords.append({'skill': keyword, 'category': category})

    # Search for keywords in experience text
    found_skills = []
    experience_lower = experience_text.lower()

    for keyword_info in all_keywords:
        keyword = keyword_info['skill']
        # Case-insensitive search
        if keyword.lower() in experience_lower:
            # Extract context (sentence containing the keyword)
            context = extract_context_sentence(experience_text, keyword)
            found_skills.append({
                'skill': keyword,
                'category': keyword_info['category'],
                'context': context
            })

    # Use spaCy for additional extraction if available
    if SPACY_AVAILABLE:
        try:
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(experience_text[:10000])  # Limit to first 10k chars for performance

            # Extract named entities that might be technologies
            for ent in doc.ents:
                if ent.label_ in ['PRODUCT', 'ORG'] and len(ent.text) > 2:
                    # Check if it's not already in found_skills
                    if not any(s['skill'].lower() == ent.text.lower() for s in found_skills):
                        found_skills.append({
                            'skill': ent.text,
                            'category': 'other',
                            'context': extract_context_sentence(experience_text, ent.text)
                        })
        except Exception as e:
            print(f"Warning: spaCy extraction failed: {e}")

    return found_skills


def extract_context_sentence(text, keyword):
    """
    Extract the sentence containing the keyword for context
    """
    # Find keyword position (case-insensitive)
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    match = pattern.search(text)

    if not match:
        return ""

    keyword_pos = match.start()

    # Find sentence boundaries
    # Look backwards for sentence start
    start = max(0, keyword_pos - 200)
    sentence_start_pattern = r'[.!?]\s+'
    before_text = text[start:keyword_pos]
    sentence_starts = list(re.finditer(sentence_start_pattern, before_text))
    if sentence_starts:
        start = start + sentence_starts[-1].end()

    # Look forwards for sentence end
    end = min(len(text), keyword_pos + 200)
    after_text = text[keyword_pos:end]
    sentence_end_match = re.search(sentence_start_pattern, after_text)
    if sentence_end_match:
        end = keyword_pos + sentence_end_match.start() + 1

    context = text[start:end].strip()

    # Truncate if too long
    if len(context) > 300:
        context = context[:297] + "..."

    return context


def extract_skills_from_resume(resume_markdown):
    """
    Main function: Parse resume markdown and extract structured skills
    Returns dict with skills, experience, education, summary
    """
    # Parse sections
    sections = parse_resume_sections(resume_markdown)

    # Extract skills from explicit Skills section
    explicit_skills = extract_explicit_skills(sections.get('skills', ''))

    # Extract skills from experience descriptions using NLP
    experience_skills = extract_skills_from_experience(sections.get('experience', ''))

    # Merge and deduplicate
    all_skills = []
    seen_skills = set()

    # Add explicit skills first (higher confidence)
    for skill in explicit_skills:
        skill_lower = skill.lower()
        if skill_lower not in seen_skills:
            seen_skills.add(skill_lower)
            all_skills.append({
                'skill': skill,
                'source': 'explicit',
                'category': 'unknown',
                'context': ''
            })

    # Add experience skills
    for skill_info in experience_skills:
        skill_lower = skill_info['skill'].lower()
        if skill_lower not in seen_skills:
            seen_skills.add(skill_lower)
            all_skills.append({
                'skill': skill_info['skill'],
                'source': 'experience',
                'category': skill_info['category'],
                'context': skill_info['context']
            })

    return {
        'skills': all_skills,
        'experience': sections.get('experience', ''),
        'education': sections.get('education', ''),
        'summary': sections.get('summary', ''),
        'total_skills_count': len(all_skills)
    }


def main():
    parser = argparse.ArgumentParser(description='Extract skills from resume markdown')
    parser.add_argument('--resume-md', required=True, help='Path to resume markdown file')
    parser.add_argument('--output', required=True, help='Output JSON file path')

    args = parser.parse_args()

    # Read resume markdown
    try:
        with open(args.resume_md, 'r', encoding='utf-8') as f:
            resume_markdown = f.read()
    except FileNotFoundError:
        print(f"Error: Resume file not found: {args.resume_md}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading resume: {e}")
        sys.exit(1)

    # Extract skills
    print("Extracting skills from resume...")
    skills_data = extract_skills_from_resume(resume_markdown)

    print(f"Found {skills_data['total_skills_count']} skills:")
    for skill_info in skills_data['skills'][:10]:
        print(f"  - {skill_info['skill']} ({skill_info['source']})")
    if skills_data['total_skills_count'] > 10:
        print(f"  ... and {skills_data['total_skills_count'] - 10} more")

    # Save to JSON
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(skills_data, f, indent=2, ensure_ascii=False)
        print(f"\nSkills data saved to: {args.output}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
