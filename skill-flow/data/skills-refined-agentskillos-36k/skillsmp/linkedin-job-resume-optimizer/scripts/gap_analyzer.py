#!/usr/bin/env python3
"""
Gap Analyzer
Identifies skill gaps between resume and job requirements
"""

import json
import argparse
import sys
from difflib import SequenceMatcher


def find_skill_match(base_skills, target_skill):
    """
    Find if target skill exists in base skills (exact or fuzzy match)
    Returns: {'match_type': 'exact'|'fuzzy'|'weak'|'none', ...}
    """
    target_lower = target_skill.lower()

    # Exact match
    for skill_info in base_skills:
        if skill_info['skill'].lower() == target_lower:
            return {
                'match_type': 'exact',
                'matched_skill': skill_info['skill'],
                'level': 'proficient'
            }

    # Fuzzy match (similar skills)
    best_similarity = 0
    best_match = None

    for skill_info in base_skills:
        similarity = SequenceMatcher(None, target_lower, skill_info['skill'].lower()).ratio()
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = skill_info['skill']

    if best_similarity > 0.8:
        return {
            'match_type': 'fuzzy',
            'matched_skill': best_match,
            'similarity': best_similarity,
            'level': 'moderate'
        }

    # Category/related match
    # Define transferable skills
    transferable_map = {
        'kubernetes': ['docker', 'container', 'orchestration', 'devops'],
        'pytorch': ['tensorflow', 'keras', 'deep learning'],
        'aws': ['azure', 'gcp', 'cloud'],
        'react': ['angular', 'vue', 'javascript'],
        'postgresql': ['mysql', 'database', 'sql'],
        'mongodb': ['nosql', 'database'],
    }

    target_key = target_lower.replace(' ', '')
    if target_key in transferable_map:
        related_keywords = transferable_map[target_key]
        for skill_info in base_skills:
            skill_lower = skill_info['skill'].lower()
            if any(keyword in skill_lower for keyword in related_keywords):
                return {
                    'match_type': 'weak',
                    'matched_skill': skill_info['skill'],
                    'level': 'beginner',
                    'transferable': True
                }

    return {'match_type': 'none'}


def find_transferable_skills(base_skills, target_skill):
    """
    Identify skills in resume that could transfer to target skill
    """
    transferable_map = {
        'Kubernetes': ['Docker', 'Container', 'DevOps', 'Cloud'],
        'PyTorch': ['TensorFlow', 'Keras', 'Deep Learning'],
        'AWS': ['Azure', 'GCP', 'Cloud'],
        'React': ['Angular', 'Vue', 'JavaScript', 'Frontend'],
        'PostgreSQL': ['MySQL', 'Database', 'SQL'],
        'MongoDB': ['NoSQL', 'Database'],
        'Jenkins': ['CI/CD', 'DevOps', 'Automation'],
        'GraphQL': ['REST API', 'API', 'Backend'],
    }

    transferable = []
    target_keywords = transferable_map.get(target_skill, [])

    for skill_info in base_skills:
        skill_name = skill_info['skill']
        for keyword in target_keywords:
            if keyword.lower() in skill_name.lower():
                transferable.append(skill_name)
                break

    return transferable


def calculate_match_score(base_skills, job):
    """
    Calculate overall compatibility percentage between resume and job
    """
    required_skills = job.get('required_skills', [])
    preferred_skills = job.get('preferred_skills', [])

    if not required_skills and not preferred_skills:
        return 0.0

    # Calculate required skills match
    required_matches = 0
    for req_skill in required_skills:
        match_result = find_skill_match(base_skills, req_skill)
        if match_result['match_type'] in ['exact', 'fuzzy']:
            required_matches += 1
        elif match_result['match_type'] == 'weak':
            required_matches += 0.5

    # Calculate preferred skills match
    preferred_matches = 0
    for pref_skill in preferred_skills:
        match_result = find_skill_match(base_skills, pref_skill)
        if match_result['match_type'] in ['exact', 'fuzzy']:
            preferred_matches += 1
        elif match_result['match_type'] == 'weak':
            preferred_matches += 0.5

    # Weighted score (required: 70%, preferred: 30%)
    required_score = (required_matches / len(required_skills)) * 0.7 if required_skills else 0
    preferred_score = (preferred_matches / len(preferred_skills)) * 0.3 if preferred_skills else 0

    total_score = (required_score + preferred_score) * 100

    return round(total_score, 1)


def analyze_skill_gaps(base_skills_data, jobs):
    """
    Compare resume skills against each job's requirements
    Returns structured gap analysis for each job
    """
    base_skills = base_skills_data.get('skills', [])
    gap_analyses = []

    for job in jobs:
        job_title = job.get('title', 'Unknown Position')
        job_url = job.get('url', '')
        required_skills = job.get('required_skills', [])
        preferred_skills = job.get('preferred_skills', [])

        print(f"\nAnalyzing gaps for: {job_title}")
        print(f"  Required skills: {len(required_skills)}")
        print(f"  Preferred skills: {len(preferred_skills)}")

        gaps = []

        # Check required skills
        for req_skill in required_skills:
            match_result = find_skill_match(base_skills, req_skill)

            if match_result['match_type'] == 'none':
                transferable = find_transferable_skills(base_skills, req_skill)
                gaps.append({
                    'skill': req_skill,
                    'gap_type': 'missing',
                    'importance': 'high',
                    'match_details': 'No direct experience found',
                    'transferable_skills': transferable,
                    'recommendation': f"Priority learning area. Consider highlighting {', '.join(transferable[:2])} experience." if transferable else "Critical gap. Recommend taking course or building project."
                })
            elif match_result['match_type'] == 'weak':
                gaps.append({
                    'skill': req_skill,
                    'gap_type': 'weak',
                    'importance': 'medium',
                    'match_details': f"Related skill found: {match_result.get('matched_skill')}",
                    'transferable_skills': [match_result.get('matched_skill')],
                    'recommendation': f"Emphasize transferable experience with {match_result.get('matched_skill')}. Study key differences."
                })

        # Check preferred skills
        for pref_skill in preferred_skills:
            match_result = find_skill_match(base_skills, pref_skill)

            if match_result['match_type'] == 'none':
                # Only add if not already in gaps from required
                if not any(g['skill'] == pref_skill for g in gaps):
                    transferable = find_transferable_skills(base_skills, pref_skill)
                    gaps.append({
                        'skill': pref_skill,
                        'gap_type': 'missing',
                        'importance': 'low',
                        'match_details': 'No direct experience found',
                        'transferable_skills': transferable,
                        'recommendation': "Nice to have. Mention if you have exposure."
                    })

        # Calculate overall match score
        match_score = calculate_match_score(base_skills, job)

        print(f"  Overall match: {match_score}%")
        print(f"  Identified {len(gaps)} gaps")

        gap_analyses.append({
            'job_title': job_title,
            'job_url': job_url,
            'company': job.get('company', 'Unknown'),
            'overall_match_score': match_score,
            'skill_gaps': gaps,
            'total_gaps': len(gaps),
            'high_priority_gaps': len([g for g in gaps if g['importance'] == 'high']),
            'linkedin_updates': generate_linkedin_recommendations(gaps, base_skills)
        })

    return gap_analyses


def generate_linkedin_recommendations(gaps, base_skills):
    """
    Generate LinkedIn profile update recommendations based on gaps
    """
    recommendations = {
        'about_section': [],
        'skills_to_add': [],
        'experience_enhancements': []
    }

    # Skills to add (focus on high priority)
    high_priority_gaps = [g for g in gaps if g['importance'] == 'high' and g['gap_type'] == 'missing']
    for gap in high_priority_gaps[:5]:  # Top 5
        recommendations['skills_to_add'].append(gap['skill'])

    # About section updates
    if high_priority_gaps:
        # Suggest emphasizing transferable skills
        for gap in high_priority_gaps[:3]:
            if gap.get('transferable_skills'):
                transferable = gap['transferable_skills'][0]
                recommendations['about_section'].append(
                    f"Emphasize {transferable} experience as it relates to {gap['skill']}"
                )

    # Experience enhancements
    weak_gaps = [g for g in gaps if g['gap_type'] == 'weak']
    for gap in weak_gaps[:3]:
        recommendations['experience_enhancements'].append(
            f"Highlight projects using {gap.get('match_details', gap['skill'])}"
        )

    return recommendations


def main():
    parser = argparse.ArgumentParser(description='Analyze skill gaps between resume and jobs')
    parser.add_argument('--base-skills', required=True, help='Path to base skills JSON file')
    parser.add_argument('--jobs', required=True, help='Path to jobs JSON file')
    parser.add_argument('--output', required=True, help='Output JSON file path')

    args = parser.parse_args()

    # Load base skills
    try:
        with open(args.base_skills, 'r', encoding='utf-8') as f:
            base_skills_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Base skills file not found: {args.base_skills}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading base skills: {e}")
        sys.exit(1)

    # Load jobs
    try:
        with open(args.jobs, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    except FileNotFoundError:
        print(f"Error: Jobs file not found: {args.jobs}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading jobs: {e}")
        sys.exit(1)

    if not jobs:
        print("Error: No jobs found in file")
        sys.exit(1)

    # Analyze gaps
    print(f"Analyzing skill gaps for {len(jobs)} jobs...")
    gap_analyses = analyze_skill_gaps(base_skills_data, jobs)

    # Save to JSON
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(gap_analyses, f, indent=2, ensure_ascii=False)
        print(f"\nGap analysis saved to: {args.output}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)

    # Print summary
    print(f"\n{'='*60}")
    print("Gap Analysis Summary")
    print(f"{'='*60}")
    for analysis in gap_analyses:
        print(f"\n{analysis['job_title']}")
        print(f"  Match Score: {analysis['overall_match_score']}%")
        print(f"  Total Gaps: {analysis['total_gaps']}")
        print(f"  High Priority: {analysis['high_priority_gaps']}")
        if analysis['linkedin_updates']['skills_to_add']:
            print(f"  Skills to Add: {', '.join(analysis['linkedin_updates']['skills_to_add'][:3])}")


if __name__ == '__main__':
    main()
