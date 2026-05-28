#!/usr/bin/env python3
"""
LinkedIn Scraper
Automates LinkedIn job search using Playwright MCP server
"""

import subprocess
import json
import re
import time
import random
import argparse
import sys
from pathlib import Path


def call_mcp_client(url, tool, params):
    """
    Call the MCP client to interact with Playwright server
    """
    mcp_client_path = "/mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/mcp-client.py"

    try:
        cmd = [
            'python3', mcp_client_path, 'call',
            '-u', url,
            '-t', tool,
            '-p', json.dumps(params)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"MCP client error: {result.stderr}")
            return None

        # Parse JSON response
        try:
            response = json.loads(result.stdout)
            return response
        except json.JSONDecodeError:
            # Return raw output if not JSON
            return {'raw_output': result.stdout}

    except subprocess.TimeoutExpired:
        print("MCP client timeout")
        return None
    except Exception as e:
        print(f"Error calling MCP client: {e}")
        return None


def extract_job_cards_from_snapshot(snapshot_text):
    """
    Parse snapshot to find job listing refs
    """
    job_cards = []

    # Look for patterns like "Job listing" or "job card" with refs
    # This is a simplified extraction - actual implementation depends on LinkedIn's structure
    lines = snapshot_text.split('\n')

    for i, line in enumerate(lines):
        # Look for job title patterns
        if any(keyword in line.lower() for keyword in ['job', 'position', 'role']):
            # Try to extract ref number
            ref_match = re.search(r'\[(\d+)\]', line)
            if ref_match:
                ref = ref_match.group(1)
                # Extract title (text before ref)
                title = re.sub(r'\[\d+\]', '', line).strip()
                job_cards.append({
                    'ref': ref,
                    'title': title,
                    'line_number': i
                })

    return job_cards


def extract_job_details_from_snapshot(snapshot_text):
    """
    Extract job details from the full job page snapshot
    """
    job_data = {
        'title': '',
        'company': '',
        'location': '',
        'description': '',
        'required_skills': [],
        'preferred_skills': []
    }

    # Extract title (usually near top)
    title_match = re.search(r'^(.+?)\s+\[', snapshot_text, re.MULTILINE)
    if title_match:
        job_data['title'] = title_match.group(1).strip()

    # Extract company name (look for "at" or "•")
    company_match = re.search(r'(?:at|•)\s+(.+?)(?:\n|•)', snapshot_text)
    if company_match:
        job_data['company'] = company_match.group(1).strip()

    # Extract description (everything after common headers)
    description_headers = ['About the job', 'Job Description', 'Description', 'Responsibilities']
    for header in description_headers:
        if header in snapshot_text:
            desc_start = snapshot_text.find(header) + len(header)
            # Take next 3000 chars as description
            job_data['description'] = snapshot_text[desc_start:desc_start+3000].strip()
            break

    # If no description found, use entire snapshot
    if not job_data['description']:
        job_data['description'] = snapshot_text[:3000]

    # Extract skills from description
    required_skills, preferred_skills = extract_skills_from_description(job_data['description'])
    job_data['required_skills'] = required_skills
    job_data['preferred_skills'] = preferred_skills

    return job_data


def extract_skills_from_description(description):
    """
    Extract required and preferred skills from job description using NLP and pattern matching
    """
    required_skills = []
    preferred_skills = []

    # Technical skills keyword list
    tech_keywords = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
        'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
        'AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
        'Git', 'Jenkins', 'CI/CD', 'MLOps', 'DevOps',
        'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
        'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
        'SQL', 'NoSQL', 'REST API', 'GraphQL', 'Microservices'
    ]

    description_lower = description.lower()

    # Find "required" section
    required_section_patterns = [
        r'(?:required|must have|requirements)[:\s]+(.+?)(?:preferred|nice to have|plus|$)',
        r'(?:qualifications)[:\s]+(.+?)(?:preferred|nice to have|plus|$)'
    ]

    required_section = ""
    for pattern in required_section_patterns:
        match = re.search(pattern, description_lower, re.DOTALL | re.IGNORECASE)
        if match:
            required_section = match.group(1)
            break

    # If no required section found, use first half of description
    if not required_section:
        required_section = description[:len(description)//2]

    # Find "preferred" section
    preferred_section_patterns = [
        r'(?:preferred|nice to have|plus|bonus)[:\s]+(.+?)$',
        r'(?:nice-to-have)[:\s]+(.+?)$'
    ]

    preferred_section = ""
    for pattern in preferred_section_patterns:
        match = re.search(pattern, description_lower, re.DOTALL | re.IGNORECASE)
        if match:
            preferred_section = match.group(1)
            break

    # Extract skills from each section
    for keyword in tech_keywords:
        keyword_lower = keyword.lower()

        # Check required section
        if keyword_lower in required_section.lower():
            if keyword not in required_skills:
                required_skills.append(keyword)
        # Check preferred section
        elif keyword_lower in preferred_section.lower():
            if keyword not in preferred_skills:
                preferred_skills.append(keyword)
        # Check full description (lower priority)
        elif keyword_lower in description_lower:
            if keyword not in required_skills and keyword not in preferred_skills:
                # Count occurrences to determine importance
                count = description_lower.count(keyword_lower)
                if count >= 2:
                    required_skills.append(keyword)
                else:
                    preferred_skills.append(keyword)

    return required_skills, preferred_skills


def search_linkedin_jobs(keywords, count=2, mcp_url="http://localhost:8808"):
    """
    Search LinkedIn for jobs matching keywords
    Returns list of job dictionaries with full descriptions
    """
    print(f"Searching LinkedIn for: {keywords}")
    print(f"Target count: {count} jobs")

    # Construct LinkedIn search URL
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keywords.replace(' ', '%20')}"
    print(f"Navigating to: {search_url}")

    # Navigate to LinkedIn jobs
    response = call_mcp_client(mcp_url, 'browser_navigate', {'url': search_url})

    if not response:
        print("Error: Failed to navigate to LinkedIn")
        return []

    # Wait for page load
    print("Waiting for page to load...")
    time.sleep(random.uniform(3, 5))

    # Get page snapshot
    print("Capturing page snapshot...")
    snapshot_response = call_mcp_client(mcp_url, 'browser_snapshot', {})

    if not snapshot_response:
        print("Error: Failed to get page snapshot")
        return []

    snapshot_text = snapshot_response.get('content', snapshot_response.get('raw_output', ''))

    # Save snapshot for debugging
    with open('/tmp/linkedin_snapshot.txt', 'w') as f:
        f.write(snapshot_text)
    print("Snapshot saved to /tmp/linkedin_snapshot.txt")

    # Extract job cards
    print("Extracting job listings...")
    job_cards = extract_job_cards_from_snapshot(snapshot_text)

    if not job_cards:
        print("Warning: No job cards found in snapshot")
        print("This might be due to:")
        print("  - LinkedIn requiring login")
        print("  - Rate limiting")
        print("  - Changed page structure")
        print("\nPlease check /tmp/linkedin_snapshot.txt for the actual page content")
        return []

    print(f"Found {len(job_cards)} job listings")

    # Click on each job to get full details
    jobs = []
    for i, job_card in enumerate(job_cards[:count]):
        print(f"\nProcessing job {i+1}/{min(count, len(job_cards))}: {job_card['title']}")

        # Click on job card
        click_response = call_mcp_client(mcp_url, 'browser_click', {
            'element': job_card['title'],
            'ref': job_card['ref']
        })

        # Random delay to appear human-like
        delay = random.uniform(2, 4)
        print(f"Waiting {delay:.1f}s for job details to load...")
        time.sleep(delay)

        # Get job details snapshot
        job_snapshot_response = call_mcp_client(mcp_url, 'browser_snapshot', {})

        if not job_snapshot_response:
            print(f"  Warning: Failed to get details for job {i+1}")
            continue

        job_snapshot_text = job_snapshot_response.get('content', job_snapshot_response.get('raw_output', ''))

        # Extract job details
        job_data = extract_job_details_from_snapshot(job_snapshot_text)

        # Get current URL for job link
        url_response = call_mcp_client(mcp_url, 'browser_evaluate', {
            'function': 'return window.location.href'
        })
        if url_response:
            job_data['url'] = url_response.get('result', search_url)
        else:
            job_data['url'] = search_url

        print(f"  Title: {job_data['title']}")
        print(f"  Company: {job_data['company']}")
        print(f"  Required skills: {', '.join(job_data['required_skills'][:5])}")
        if len(job_data['required_skills']) > 5:
            print(f"                   ... and {len(job_data['required_skills']) - 5} more")

        jobs.append(job_data)

    print(f"\nSuccessfully scraped {len(jobs)} jobs")
    return jobs


def main():
    parser = argparse.ArgumentParser(description='Scrape LinkedIn job postings')
    parser.add_argument('--keywords', required=True, help='Job search keywords')
    parser.add_argument('--count', type=int, default=2, help='Number of jobs to scrape')
    parser.add_argument('--output', required=True, help='Output JSON file path')
    parser.add_argument('--mcp-url', default='http://localhost:8808', help='Playwright MCP server URL')

    args = parser.parse_args()

    # Check if MCP server is running
    try:
        test_response = call_mcp_client(args.mcp_url, 'browser_snapshot', {})
        if not test_response:
            print("Error: Playwright MCP server not responding")
            print("Please start the server first:")
            print("  bash /mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/start-server.sh")
            sys.exit(1)
    except Exception as e:
        print(f"Error: Cannot connect to MCP server: {e}")
        sys.exit(1)

    # Search jobs
    jobs = search_linkedin_jobs(args.keywords, args.count, args.mcp_url)

    if not jobs:
        print("\nNo jobs found. This could be due to:")
        print("  1. LinkedIn requiring login")
        print("  2. Search keywords too specific")
        print("  3. Rate limiting")
        print("\nTry:")
        print("  - Using broader keywords")
        print("  - Logging into LinkedIn in the browser first")
        print("  - Waiting a few minutes before retrying")
        sys.exit(1)

    # Save to JSON
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"\nJobs data saved to: {args.output}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
