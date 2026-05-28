#!/usr/bin/env python3
"""
ATS Optimizer
Generates ATS-optimized tailored resumes based on job descriptions
"""

import re
import json
import argparse
import sys
import subprocess
import os
from pathlib import Path
from difflib import SequenceMatcher


def extract_job_keywords(job_description):
    """
    Extract keywords from job description with priority weighting
    """
    # Technical skills keywords
    tech_keywords = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
        'AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
        'Git', 'Jenkins', 'CI/CD', 'MLOps', 'DevOps',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
        'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
        'SQL', 'NoSQL', 'REST API', 'GraphQL', 'Microservices',
        'Agile', 'Scrum', 'Spark', 'Hadoop', 'Kafka'
    ]

    keywords = {
        'required': [],
        'preferred': []
    }

    description_lower = description.lower()

    # Find required section
    required_section = ""
    required_patterns = [
        r'(?:required|must have|requirements)[:\s]+(.+?)(?:preferred|nice to have|plus|benefits|$)',
        r'(?:qualifications)[:\s]+(.+?)(?:preferred|nice to have|plus|benefits|$)'
    ]

    for pattern in required_patterns:
        match = re.search(pattern, job_description.lower(), re.DOTALL | re.IGNORECASE)
        if match:
            required_section = match.group(1)
            break

    # Find preferred section
    preferred_section = ""
    preferred_patterns = [
        r'(?:preferred|nice to have|plus|bonus)[:\s]+(.+?)(?:benefits|$)',
    ]

    for pattern in preferred_patterns:
        match = re.search(pattern, job_description.lower(), re.DOTALL | re.IGNORECASE)
        if match:
            preferred_section = match.group(1)
            break

    # Extract keywords
    for keyword in tech_keywords:
        keyword_lower = keyword.lower()

        if keyword_lower in required_section.lower():
            keywords['required'].append({'term': keyword, 'weight': 1.0})
        elif keyword_lower in preferred_section.lower():
            keywords['preferred'].append({'term': keyword, 'weight': 0.6})
        elif keyword_lower in job_description.lower():
            # Count occurrences
            count = job_description.lower().count(keyword_lower)
            if count >= 2:
                keywords['required'].append({'term': keyword, 'weight': 0.8})

    return keywords


def analyze_keyword_coverage(resume_text, job_keywords):
    """
    Calculate keyword coverage percentage
    """
    coverage = {}
    resume_lower = resume_text.lower()

    for keyword_info in job_keywords.get('required', []):
        keyword = keyword_info['term']
        if keyword.lower() in resume_lower:
            coverage[keyword] = 1
        else:
            coverage[keyword] = 0

    for keyword_info in job_keywords.get('preferred', []):
        keyword = keyword_info['term']
        if keyword not in coverage:  # Don't override if already in required
            if keyword.lower() in resume_lower:
                coverage[keyword] = 1
            else:
                coverage[keyword] = 0

    return coverage


def update_summary(summary_text, job_title, top_keywords):
    """
    Update professional summary with job title and keywords
    """
    if not summary_text:
        # Create new summary
        keywords_str = ", ".join([kw['term'] for kw in top_keywords[:5]])
        return f"# Professional Summary\n\n{job_title} with expertise in {keywords_str}. Proven track record of delivering high-quality solutions and driving innovation."

    # Enhance existing summary
    lines = summary_text.split('\n')
    enhanced_lines = []

    for line in lines:
        enhanced_lines.append(line)
        # After first paragraph, add job title focus
        if line.strip() and not line.startswith('#'):
            keywords_str = ", ".join([kw['term'] for kw in top_keywords[:3]])
            if keywords_str.lower() not in line.lower():
                enhanced_lines.append(f"Specialized in {keywords_str} with focus on {job_title} responsibilities.")
            break

    return '\n'.join(enhanced_lines)


def enhance_skills_section(skills_text, job_keywords):
    """
    Enhance skills section with exact keyword matches
    """
    if not skills_text:
        skills_text = "# Skills\n\n"

    # Get all keywords
    all_keywords = []
    for kw in job_keywords.get('required', []):
        if kw['term'] not in all_keywords:
            all_keywords.append(kw['term'])
    for kw in job_keywords.get('preferred', [])[:5]:  # Limit preferred
        if kw['term'] not in all_keywords:
            all_keywords.append(kw['term'])

    # Check which keywords are missing
    missing_keywords = []
    skills_lower = skills_text.lower()
    for keyword in all_keywords:
        if keyword.lower() not in skills_lower:
            missing_keywords.append(keyword)

    # Add missing keywords
    if missing_keywords:
        skills_text += "\n\n**Additional Technologies**: " + ", ".join(missing_keywords)

    return skills_text


def integrate_keywords_into_experience(experience_text, missing_keywords, job_keywords):
    """
    Naturally weave missing keywords into experience bullet points
    """
    if not experience_text or not missing_keywords:
        return experience_text

    lines = experience_text.split('\n')
    enhanced_lines = []
    keywords_integrated = 0

    for i, line in enumerate(lines):
        enhanced_lines.append(line)

        # Look for bullet points
        if re.match(r'^\s*[•\-\*]', line) and keywords_integrated < len(missing_keywords):
            # Try to integrate a keyword
            keyword = missing_keywords[keywords_integrated]

            # Create enhanced bullet with keyword
            # Find related technology in bullet point
            if any(tech in line.lower() for tech in ['develop', 'build', 'implement', 'design', 'create']):
                # Add keyword after action verb
                enhanced_line = line.rstrip()
                if not enhanced_line.endswith('.'):
                    enhanced_line += '.'
                enhanced_line += f" Utilized {keyword} for implementation."
                enhanced_lines[-1] = enhanced_line
                keywords_integrated += 1

    return '\n'.join(enhanced_lines)


def optimize_resume_content(base_resume_text, job_keywords, missing_keywords, job_title):
    """
    Optimize resume content for ATS by naturally integrating keywords
    """
    # Parse resume into sections
    sections = {}

    # Simple section parser
    section_patterns = {
        'summary': r'(#{1,2}\s*(?:Professional\s+Summary|Summary|Profile|Objective|About).*?)(?=\n#{1,2}\s|\Z)',
        'skills': r'(#{1,2}\s*(?:Skills|Technical\s+Skills|Core\s+Competencies).*?)(?=\n#{1,2}\s|\Z)',
        'experience': r'(#{1,2}\s*(?:Experience|Work\s+Experience|Professional\s+Experience).*?)(?=\n#{1,2}\s|\Z)',
        'education': r'(#{1,2}\s*(?:Education|Academic\s+Background).*?)(?=\n#{1,2}\s|\Z)'
    }

    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, base_resume_text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        if match:
            sections[section_name] = match.group(1)
        else:
            sections[section_name] = ''

    # Optimize each section
    if sections.get('summary'):
        sections['summary'] = update_summary(
            sections['summary'],
            job_title=job_title,
            top_keywords=job_keywords.get('required', [])[:5]
        )

    if sections.get('skills'):
        sections['skills'] = enhance_skills_section(
            sections['skills'],
            job_keywords=job_keywords
        )

    if sections.get('experience'):
        sections['experience'] = integrate_keywords_into_experience(
            sections['experience'],
            missing_keywords=missing_keywords[:5],  # Integrate top 5 missing keywords
            job_keywords=job_keywords
        )

    # Reconstruct resume
    optimized_resume = ""
    if sections.get('summary'):
        optimized_resume += sections['summary'] + "\n\n"
    if sections.get('skills'):
        optimized_resume += sections['skills'] + "\n\n"
    if sections.get('experience'):
        optimized_resume += sections['experience'] + "\n\n"
    if sections.get('education'):
        optimized_resume += sections['education'] + "\n\n"

    return optimized_resume


def sanitize_filename(filename):
    """
    Sanitize filename by removing invalid characters
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Limit length
    if len(filename) > 50:
        filename = filename[:50]
    return filename


def create_docx_from_markdown(markdown_content, output_path):
    """
    Create DOCX from markdown using pandoc
    """
    try:
        # Save markdown to temp file
        temp_md = '/tmp/temp_resume.md'
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Convert to DOCX using pandoc
        subprocess.run([
            'pandoc', temp_md,
            '-f', 'markdown',
            '-t', 'docx',
            '-o', output_path
        ], check=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating DOCX: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_tailored_resume(base_resume_path, job_data, output_dir):
    """
    Generate ATS-optimized resume tailored to specific job
    """
    job_title = job_data.get('title', 'Unknown_Position')
    job_description = job_data.get('description', '')

    print(f"\nGenerating tailored resume for: {job_title}")

    # Convert base resume to markdown
    print("  Converting resume to markdown...")
    try:
        temp_md = '/tmp/base_resume.md'
        subprocess.run([
            'pandoc', '--track-changes=accept',
            base_resume_path, '-o', temp_md
        ], check=True)

        with open(temp_md, 'r', encoding='utf-8') as f:
            base_resume_text = f.read()
    except Exception as e:
        print(f"  Error converting resume: {e}")
        return None

    # Extract job keywords
    print("  Extracting job keywords...")
    job_keywords = extract_job_keywords(job_description)
    required_count = len(job_keywords.get('required', []))
    preferred_count = len(job_keywords.get('preferred', []))
    print(f"  Found {required_count} required, {preferred_count} preferred skills")

    # Analyze keyword coverage
    print("  Analyzing keyword coverage...")
    coverage = analyze_keyword_coverage(base_resume_text, job_keywords)
    total_keywords = len(coverage)
    covered_keywords = sum(coverage.values())
    if total_keywords > 0:
        coverage_pct = (covered_keywords / total_keywords) * 100
        print(f"  Current coverage: {coverage_pct:.1f}% ({covered_keywords}/{total_keywords})")

    # Identify missing keywords
    missing_keywords = [kw for kw, cov in coverage.items() if cov == 0]
    print(f"  Missing {len(missing_keywords)} keywords")

    # Generate optimized content
    print("  Optimizing content...")
    optimized_content = optimize_resume_content(
        base_resume_text=base_resume_text,
        job_keywords=job_keywords,
        missing_keywords=missing_keywords,
        job_title=job_title
    )

    # Create output filename
    safe_title = sanitize_filename(job_title)
    output_filename = f"resume_tailored_{safe_title}.docx"
    output_path = os.path.join(output_dir, output_filename)

    # Create DOCX
    print(f"  Creating DOCX: {output_filename}")
    success = create_docx_from_markdown(optimized_content, output_path)

    if success:
        print(f"  ✓ Saved to: {output_path}")
        # Re-calculate coverage
        new_coverage = analyze_keyword_coverage(optimized_content, job_keywords)
        new_covered = sum(new_coverage.values())
        if total_keywords > 0:
            new_coverage_pct = (new_covered / total_keywords) * 100
            print(f"  New coverage: {new_coverage_pct:.1f}% ({new_covered}/{total_keywords})")
        return output_path
    else:
        print(f"  ✗ Failed to create DOCX")
        # Save markdown as fallback
        md_path = output_path.replace('.docx', '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
        print(f"  Saved markdown fallback to: {md_path}")
        return md_path


def main():
    parser = argparse.ArgumentParser(description='Generate ATS-optimized tailored resume')
    parser.add_argument('--base-resume', required=True, help='Path to base resume DOCX')
    parser.add_argument('--jobs', required=True, help='Path to jobs JSON file')
    parser.add_argument('--output-dir', required=True, help='Output directory')

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.base_resume):
        print(f"Error: Base resume not found: {args.base_resume}")
        sys.exit(1)

    if not os.path.exists(args.jobs):
        print(f"Error: Jobs file not found: {args.jobs}")
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Load jobs
    try:
        with open(args.jobs, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    except Exception as e:
        print(f"Error loading jobs: {e}")
        sys.exit(1)

    if not jobs:
        print("Error: No jobs found in file")
        sys.exit(1)

    # Generate tailored resume for each job
    tailored_resumes = []
    for i, job in enumerate(jobs):
        print(f"\n{'='*60}")
        print(f"Job {i+1}/{len(jobs)}")
        resume_path = generate_tailored_resume(args.base_resume, job, args.output_dir)
        if resume_path:
            tailored_resumes.append({
                'job_title': job.get('title'),
                'resume_path': resume_path
            })

    print(f"\n{'='*60}")
    print(f"Generated {len(tailored_resumes)} tailored resumes")
    for item in tailored_resumes:
        print(f"  - {item['job_title']}: {item['resume_path']}")


if __name__ == '__main__':
    main()
