#!/usr/bin/env python3
"""
Workflow Orchestrator
Main entry point that coordinates the complete job search and resume optimization workflow
"""

import subprocess
import json
import argparse
import sys
import os
from pathlib import Path
import time


def load_config(config_path=None):
    """
    Load configuration from config.json
    """
    if not config_path:
        script_dir = Path(__file__).parent.parent
        config_path = script_dir / 'config.json'

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: Config file not found at {config_path}")
        return {}
    except Exception as e:
        print(f"Warning: Error loading config: {e}")
        return {}


def start_playwright_server():
    """
    Start Playwright MCP server
    """
    print("\n" + "="*60)
    print("Starting Playwright MCP server...")
    print("="*60)

    start_script = "/mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/start-server.sh"

    try:
        result = subprocess.run(['bash', start_script], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Playwright server started")
            time.sleep(2)  # Give server time to fully start
            return True
        else:
            print(f"Warning: Server start returned code {result.returncode}")
            print("Server may already be running. Continuing...")
            return True
    except subprocess.TimeoutExpired:
        print("Server start timeout - may already be running. Continuing...")
        return True
    except Exception as e:
        print(f"Error starting server: {e}")
        print("You may need to start it manually:")
        print(f"  bash {start_script}")
        return False


def stop_playwright_server():
    """
    Stop Playwright MCP server
    """
    print("\n" + "="*60)
    print("Stopping Playwright MCP server...")
    print("="*60)

    stop_script = "/mnt/d/Ali_Home/Learning/AgenticAI/AI-P009/Assignments/ProjectA1/resume_optimizer/.claude/skills/browsing-with-playwright/scripts/stop-server.sh"

    try:
        subprocess.run(['bash', stop_script], capture_output=True, text=True, timeout=10)
        print("✓ Playwright server stopped")
        return True
    except Exception as e:
        print(f"Warning: Error stopping server: {e}")
        return False


def run_linkedin_scraper(keywords, count, output_path, scripts_dir):
    """
    Run LinkedIn scraper to find jobs
    """
    print("\n" + "="*60)
    print(f"Searching LinkedIn for: {keywords}")
    print(f"Target: {count} jobs")
    print("="*60)

    scraper_script = scripts_dir / 'linkedin_scraper.py'

    try:
        result = subprocess.run([
            'python3', str(scraper_script),
            '--keywords', keywords,
            '--count', str(count),
            '--output', output_path
        ], capture_output=True, text=True, timeout=180)

        print(result.stdout)

        if result.returncode != 0:
            print(f"Error: LinkedIn scraper failed")
            print(result.stderr)
            return False

        return True
    except subprocess.TimeoutExpired:
        print("Error: LinkedIn scraper timed out (3 minutes)")
        return False
    except Exception as e:
        print(f"Error running LinkedIn scraper: {e}")
        return False


def run_resume_analyzer(resume_path, output_path, scripts_dir):
    """
    Analyze base resume to extract skills
    """
    print("\n" + "="*60)
    print("Analyzing base resume...")
    print("="*60)

    # Convert DOCX to markdown first
    temp_md = '/tmp/base_resume.md'
    try:
        subprocess.run([
            'pandoc', '--track-changes=accept',
            resume_path, '-o', temp_md
        ], check=True, capture_output=True)
        print("✓ Resume converted to markdown")
    except subprocess.CalledProcessError as e:
        print(f"Error converting resume: {e}")
        return False

    # Run analyzer
    analyzer_script = scripts_dir / 'resume_analyzer.py'

    try:
        result = subprocess.run([
            'python3', str(analyzer_script),
            '--resume-md', temp_md,
            '--output', output_path
        ], capture_output=True, text=True, timeout=60)

        print(result.stdout)

        if result.returncode != 0:
            print(f"Error: Resume analyzer failed")
            print(result.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error running resume analyzer: {e}")
        return False


def run_ats_optimizer(base_resume_path, jobs_path, output_dir, scripts_dir):
    """
    Generate tailored resumes for each job
    """
    print("\n" + "="*60)
    print("Generating ATS-optimized tailored resumes...")
    print("="*60)

    optimizer_script = scripts_dir / 'ats_optimizer.py'

    try:
        result = subprocess.run([
            'python3', str(optimizer_script),
            '--base-resume', base_resume_path,
            '--jobs', jobs_path,
            '--output-dir', output_dir
        ], capture_output=True, text=True, timeout=300)

        print(result.stdout)

        if result.returncode != 0:
            print(f"Warning: ATS optimizer encountered issues")
            print(result.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error running ATS optimizer: {e}")
        return False


def run_gap_analyzer(base_skills_path, jobs_path, output_path, scripts_dir):
    """
    Analyze skill gaps between resume and job requirements
    """
    print("\n" + "="*60)
    print("Analyzing skill gaps...")
    print("="*60)

    gap_script = scripts_dir / 'gap_analyzer.py'

    try:
        result = subprocess.run([
            'python3', str(gap_script),
            '--base-skills', base_skills_path,
            '--jobs', jobs_path,
            '--output', output_path
        ], capture_output=True, text=True, timeout=60)

        print(result.stdout)

        if result.returncode != 0:
            print(f"Error: Gap analyzer failed")
            print(result.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error running gap analyzer: {e}")
        return False


def run_question_generator(gap_analysis_path, output_path, questions_per_gap, scripts_dir):
    """
    Generate interview preparation questions
    """
    print("\n" + "="*60)
    print("Generating interview preparation questions...")
    print("="*60)

    question_script = scripts_dir / 'question_generator.py'

    try:
        result = subprocess.run([
            'python3', str(question_script),
            '--gap-analysis', gap_analysis_path,
            '--questions-per-gap', str(questions_per_gap),
            '--output', output_path
        ], capture_output=True, text=True, timeout=60)

        print(result.stdout)

        if result.returncode != 0:
            print(f"Error: Question generator failed")
            print(result.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error running question generator: {e}")
        return False


def generate_summary_report(jobs_path, gap_analysis_path, output_dir):
    """
    Generate final summary report
    """
    print("\n" + "="*60)
    print("Generating summary report...")
    print("="*60)

    try:
        # Load data
        with open(jobs_path, 'r') as f:
            jobs = json.load(f)

        with open(gap_analysis_path, 'r') as f:
            gap_analysis = json.load(f)

        # Generate markdown report
        report = "# Job Search Results Summary\n\n"
        report += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += f"## Jobs Found: {len(jobs)}\n\n"

        for i, (job, analysis) in enumerate(zip(jobs, gap_analysis), 1):
            report += f"### Job {i}: {job['title']} - {job.get('company', 'Unknown')}\n\n"
            report += f"- **LinkedIn URL**: {job.get('url', 'N/A')}\n"

            # Find tailored resume
            safe_title = job['title'].replace(' ', '_').replace('/', '_')
            resume_file = f"resume_tailored_{safe_title}.docx"
            report += f"- **Tailored Resume**: {resume_file}\n"

            report += f"- **Match Score**: {analysis.get('overall_match_score', 0)}%\n"
            report += f"- **Key Requirements**: {', '.join(job.get('required_skills', [])[:5])}\n"

            high_priority_gaps = [g for g in analysis.get('skill_gaps', []) if g['importance'] == 'high']
            if high_priority_gaps:
                gap_names = [g['skill'] for g in high_priority_gaps[:3]]
                report += f"- **Skill Gaps (High Priority)**: {', '.join(gap_names)}\n"

            report += "\n"

        # LinkedIn recommendations
        report += "## LinkedIn Profile Recommendations\n\n"
        report += "### Skills to Add\n\n"

        all_skills_to_add = set()
        for analysis in gap_analysis:
            linkedin_updates = analysis.get('linkedin_updates', {})
            skills = linkedin_updates.get('skills_to_add', [])
            all_skills_to_add.update(skills[:3])

        for skill in sorted(all_skills_to_add)[:10]:
            report += f"- {skill}\n"

        report += "\n### About Section Updates\n\n"
        report += "- Emphasize your experience with transferable technologies\n"
        report += "- Highlight production-scale deployment experience\n"
        report += "- Mention cross-functional collaboration in technical projects\n"

        report += "\n## Next Steps\n\n"
        report += f"1. Review tailored resumes in `{output_dir}/`\n"
        report += "2. Study interview prep questions in `interview_prep.md`\n"
        report += "3. Update LinkedIn profile per recommendations above\n"
        report += "4. Apply to jobs with tailored resumes\n"
        report += "5. Practice answering interview questions\n"

        # Save report
        report_path = os.path.join(output_dir, 'summary_report.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✓ Summary report saved to: {report_path}")
        return True

    except Exception as e:
        print(f"Error generating summary report: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='LinkedIn Job Resume Optimizer - Complete Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with defaults from config.json
  python3 workflow_orchestrator.py

  # Custom job search
  python3 workflow_orchestrator.py --job-keywords "Machine Learning Engineer" --job-count 3

  # Custom resume path
  python3 workflow_orchestrator.py --resume-path /path/to/resume.docx --output-dir ./output
        """
    )

    parser.add_argument('--resume-path', help='Path to base resume DOCX file')
    parser.add_argument('--job-keywords', help='Job search keywords')
    parser.add_argument('--job-count', type=int, help='Number of jobs to find')
    parser.add_argument('--output-dir', help='Output directory for results')
    parser.add_argument('--config', help='Path to config.json file')
    parser.add_argument('--skip-linkedin', action='store_true', help='Skip LinkedIn scraping (use existing jobs.json)')
    parser.add_argument('--manual-jobs', help='Path to manually created jobs JSON file')

    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # Get parameters (CLI args override config)
    resume_path = args.resume_path or config.get('resume_path')
    output_dir = args.output_dir or config.get('output_directory', './resume_optimizer/output')
    job_keywords = args.job_keywords or config.get('job_search', {}).get('default_keywords', 'AI Engineer remote')
    job_count = args.job_count or config.get('job_search', {}).get('default_count', 2)
    questions_per_gap = config.get('interview_prep', {}).get('questions_per_gap', 10)

    # Validate inputs
    if not resume_path:
        print("Error: Resume path not specified. Use --resume-path or set in config.json")
        sys.exit(1)

    if not os.path.exists(resume_path):
        print(f"Error: Resume not found at {resume_path}")
        sys.exit(1)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Get scripts directory
    scripts_dir = Path(__file__).parent

    # Define output paths
    jobs_path = os.path.join(output_dir, 'jobs.json')
    base_skills_path = os.path.join(output_dir, 'base_skills.json')
    gap_analysis_path = os.path.join(output_dir, 'gap_analysis.json')
    interview_prep_path = os.path.join(output_dir, 'interview_prep.md')

    print("\n" + "="*60)
    print("LINKEDIN JOB RESUME OPTIMIZER")
    print("="*60)
    print(f"Resume: {resume_path}")
    print(f"Job Keywords: {job_keywords}")
    print(f"Job Count: {job_count}")
    print(f"Output Directory: {output_dir}")
    print("="*60)

    # Step 1: Start Playwright server (if not skipping LinkedIn)
    if not args.skip_linkedin and not args.manual_jobs:
        if not start_playwright_server():
            print("\nError: Failed to start Playwright server")
            print("You can still run the workflow with --manual-jobs jobs.json")
            sys.exit(1)

    # Step 2: Search LinkedIn jobs (or use manual/existing)
    if args.manual_jobs:
        print(f"\nUsing manual jobs file: {args.manual_jobs}")
        import shutil
        shutil.copy(args.manual_jobs, jobs_path)
    elif args.skip_linkedin:
        if not os.path.exists(jobs_path):
            print(f"Error: --skip-linkedin specified but {jobs_path} not found")
            sys.exit(1)
        print(f"\nSkipping LinkedIn scraping, using existing: {jobs_path}")
    else:
        if not run_linkedin_scraper(job_keywords, job_count, jobs_path, scripts_dir):
            print("\nError: LinkedIn scraping failed")
            stop_playwright_server()
            sys.exit(1)

    # Step 3: Analyze base resume
    if not run_resume_analyzer(resume_path, base_skills_path, scripts_dir):
        print("\nError: Resume analysis failed")
        if not args.skip_linkedin:
            stop_playwright_server()
        sys.exit(1)

    # Step 4: Generate tailored resumes
    if not run_ats_optimizer(resume_path, jobs_path, output_dir, scripts_dir):
        print("\nWarning: Some tailored resumes may not have been generated")

    # Step 5: Analyze skill gaps
    if not run_gap_analyzer(base_skills_path, jobs_path, gap_analysis_path, scripts_dir):
        print("\nError: Skill gap analysis failed")
        if not args.skip_linkedin:
            stop_playwright_server()
        sys.exit(1)

    # Step 6: Generate interview questions
    if not run_question_generator(gap_analysis_path, interview_prep_path, questions_per_gap, scripts_dir):
        print("\nError: Interview question generation failed")
        if not args.skip_linkedin:
            stop_playwright_server()
        sys.exit(1)

    # Step 7: Generate summary report
    if not generate_summary_report(jobs_path, gap_analysis_path, output_dir):
        print("\nWarning: Summary report generation failed")

    # Step 8: Stop Playwright server
    if not args.skip_linkedin and not args.manual_jobs:
        stop_playwright_server()

    # Final summary
    print("\n" + "="*60)
    print("✓ WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\nOutput files in: {output_dir}")
    print("  - jobs.json (Job data)")
    print("  - base_skills.json (Your resume skills)")
    print("  - gap_analysis.json (Skill gaps)")
    print("  - interview_prep.md (Interview questions)")
    print("  - summary_report.md (Summary)")
    print("  - resume_tailored_*.docx (Tailored resumes)")
    print("\nNext steps:")
    print(f"  1. Read summary_report.md")
    print(f"  2. Review tailored resumes")
    print(f"  3. Study interview_prep.md")
    print(f"  4. Update your LinkedIn profile")
    print(f"  5. Apply to jobs!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
