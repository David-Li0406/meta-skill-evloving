#!/usr/bin/env python3
"""
Question Generator
Generates targeted interview preparation questions based on skill gaps
"""

import json
import argparse
import sys


# Question templates by skill
QUESTION_TEMPLATES = {
    'Kubernetes': {
        'fundamental': [
            "Explain the core components of Kubernetes architecture (pods, services, deployments).",
            "What is the difference between a Deployment and a StatefulSet in Kubernetes?",
            "How does Kubernetes handle service discovery and load balancing?",
            "Describe the Kubernetes pod lifecycle and different pod states.",
            "What are ConfigMaps and Secrets in Kubernetes, and when would you use each?",
            "Explain how Kubernetes scheduling works and what factors influence pod placement.",
            "What is a Kubernetes namespace and why is it important for multi-tenancy?",
            "Describe how horizontal pod autoscaling works in Kubernetes."
        ],
        'scenario': [
            "A production pod keeps crashing and restarting. Walk me through your debugging process using kubectl.",
            "You need to deploy a stateful application (like a database) on Kubernetes. How would you approach this?",
            "Your team wants to implement blue-green deployments. How would you configure this in Kubernetes?",
            "A service is experiencing high latency. How would you investigate and resolve this in a Kubernetes environment?",
            "How would you implement zero-downtime deployments in Kubernetes?",
            "Design a Kubernetes deployment strategy for a microservices application with 10 services."
        ]
    },
    'PyTorch': {
        'fundamental': [
            "Explain the difference between PyTorch and TensorFlow in terms of computational graphs.",
            "What is a PyTorch tensor and how does it differ from a NumPy array?",
            "Describe the concept of autograd in PyTorch and how automatic differentiation works.",
            "How do you define a custom neural network layer in PyTorch?",
            "Explain the difference between model.train() and model.eval() in PyTorch.",
            "What are PyTorch DataLoaders and why are they important for training?",
            "How does backpropagation work in PyTorch's computational graph?",
            "Describe the PyTorch model saving and loading process using torch.save() and torch.load()."
        ],
        'scenario': [
            "Your PyTorch model is overfitting on the training data. What techniques would you use to address this?",
            "You need to train a model on multiple GPUs. How would you implement distributed training in PyTorch?",
            "A PyTorch model is running slowly during inference. How would you optimize it for production?",
            "How would you implement transfer learning for a computer vision task in PyTorch?",
            "Design a custom loss function in PyTorch for a specific use case (e.g., imbalanced classification).",
            "Your model's training loss is not converging. What debugging steps would you take?"
        ]
    },
    'AWS': {
        'fundamental': [
            "Explain the core AWS services: EC2, S3, RDS, Lambda, and their use cases.",
            "What is the difference between S3 and EBS storage in AWS?",
            "Describe AWS IAM and how you would implement least-privilege access control.",
            "What are AWS VPCs and how do they provide network isolation?",
            "Explain the difference between AWS Lambda and EC2 for compute workloads.",
            "How does AWS CloudFormation enable infrastructure as code?",
            "What is AWS Auto Scaling and when would you use it?",
            "Describe AWS security best practices for production applications."
        ],
        'scenario': [
            "Design a scalable, highly available web application architecture on AWS.",
            "An EC2 instance is experiencing high CPU usage. How would you diagnose and resolve this?",
            "You need to migrate a legacy application to AWS. What's your migration strategy?",
            "How would you implement disaster recovery for a critical application on AWS?",
            "Design a cost-effective data pipeline for processing terabytes of data daily on AWS.",
            "Your S3 bucket was accidentally made public. What steps would you take to secure it?"
        ]
    },
    'Docker': {
        'fundamental': [
            "Explain what Docker containers are and how they differ from virtual machines.",
            "What is a Dockerfile and what are its key instructions (FROM, RUN, COPY, CMD)?",
            "Describe Docker images vs. Docker containers.",
            "How do Docker volumes work and why are they important?",
            "What is Docker Compose and when would you use it?",
            "Explain Docker networking modes (bridge, host, overlay).",
            "What are Docker layers and how do they optimize build time?",
            "How would you minimize Docker image size?"
        ],
        'scenario': [
            "A containerized application is running out of memory. How would you diagnose and fix this?",
            "Design a multi-container application using Docker Compose (e.g., web app + database + cache).",
            "Your Docker build is taking too long. What optimization strategies would you use?",
            "How would you implement secrets management in Docker containers?",
            "Explain your strategy for monitoring and logging Docker containers in production.",
            "A container can't connect to another container. How would you troubleshoot this?"
        ]
    },
    'Machine Learning': {
        'fundamental': [
            "Explain the difference between supervised, unsupervised, and reinforcement learning.",
            "What is overfitting and how can you prevent it?",
            "Describe the bias-variance tradeoff in machine learning.",
            "What is cross-validation and why is it important?",
            "Explain regularization techniques (L1, L2) and when to use them.",
            "What is the difference between classification and regression?",
            "Describe common evaluation metrics: precision, recall, F1-score, AUC-ROC.",
            "What is feature engineering and why is it important?"
        ],
        'scenario': [
            "You have an imbalanced dataset (95% negative, 5% positive). How would you handle this?",
            "Walk me through your process for building a machine learning model from scratch.",
            "Your model performs well in development but poorly in production. What might be wrong?",
            "How would you explain a complex ML model's predictions to non-technical stakeholders?",
            "Design an A/B testing framework for evaluating ML model improvements.",
            "You need to reduce model inference time by 50%. What approaches would you try?"
        ]
    }
}


def generate_fundamental_questions(skill, count=4):
    """
    Generate foundational knowledge questions
    """
    if skill in QUESTION_TEMPLATES and 'fundamental' in QUESTION_TEMPLATES[skill]:
        return QUESTION_TEMPLATES[skill]['fundamental'][:count]

    # Generic fundamental questions
    return [
        f"Explain the core concepts and principles of {skill}.",
        f"What are the main use cases and applications of {skill}?",
        f"Describe the key features that make {skill} useful.",
        f"What are common alternatives to {skill} and how do they compare?"
    ][:count]


def generate_scenario_questions(skill, count=3):
    """
    Generate scenario-based problem-solving questions
    """
    if skill in QUESTION_TEMPLATES and 'scenario' in QUESTION_TEMPLATES[skill]:
        return QUESTION_TEMPLATES[skill]['scenario'][:count]

    # Generic scenario questions
    return [
        f"Describe a challenging problem you would solve using {skill}.",
        f"How would you debug an issue with {skill} in a production environment?",
        f"Design a system architecture that leverages {skill} effectively."
    ][:count]


def generate_transferable_questions(skill, transferable_skills, count=3):
    """
    Generate questions about leveraging transferable experience
    """
    questions = []

    if transferable_skills:
        related = transferable_skills[0]
        questions.append(
            f"You have experience with {related}. How would you leverage that knowledge to quickly learn {skill}?"
        )
        questions.append(
            f"Compare and contrast {skill} with {related}. What are the key differences?"
        )

    questions.append(
        f"Describe a time you learned a new technology similar to {skill}. What was your approach?"
    )

    return questions[:count]


def generate_depth_questions(skill, count=4):
    """
    Generate deep technical questions for weak skills
    """
    return [
        f"Explain advanced features of {skill} that optimize performance.",
        f"What are common pitfalls and anti-patterns when working with {skill} at scale?",
        f"Compare {skill} with alternative technologies. When would you choose {skill}?",
        f"Describe a complex problem you solved using {skill}. Use the STAR method (Situation, Task, Action, Result)."
    ][:count]


def generate_questions_for_gap(gap, count=10):
    """
    Generate diverse questions for a specific skill gap
    """
    skill = gap['skill']
    gap_type = gap['gap_type']
    transferable_skills = gap.get('transferable_skills', [])

    questions = []

    if gap_type == 'missing':
        # For missing skills: fundamentals + transferable + scenarios
        questions.extend(generate_fundamental_questions(skill, count=4))
        questions.extend(generate_transferable_questions(skill, transferable_skills, count=3))
        questions.extend(generate_scenario_questions(skill, count=3))

    elif gap_type == 'weak':
        # For weak skills: depth + practical + troubleshooting
        questions.extend(generate_depth_questions(skill, count=4))
        questions.extend(generate_scenario_questions(skill, count=6))

    else:
        # Default: mixed questions
        questions.extend(generate_fundamental_questions(skill, count=5))
        questions.extend(generate_scenario_questions(skill, count=5))

    return questions[:count]


def generate_interview_questions(gap_analysis, questions_per_gap=10):
    """
    Generate targeted interview prep questions for each skill gap
    """
    all_questions = []

    for job_analysis in gap_analysis:
        job_title = job_analysis['job_title']
        skill_gaps = job_analysis.get('skill_gaps', [])

        print(f"\nGenerating questions for: {job_title}")
        print(f"  Skill gaps: {len(skill_gaps)}")

        job_questions = {
            'job_title': job_title,
            'company': job_analysis.get('company', 'Unknown'),
            'job_url': job_analysis.get('job_url', ''),
            'overall_match_score': job_analysis.get('overall_match_score', 0),
            'questions_by_gap': []
        }

        for gap in skill_gaps:
            skill = gap['skill']
            print(f"  Generating {questions_per_gap} questions for: {skill}")

            questions = generate_questions_for_gap(gap, count=questions_per_gap)

            job_questions['questions_by_gap'].append({
                'skill': skill,
                'gap_type': gap['gap_type'],
                'importance': gap['importance'],
                'questions': questions
            })

        all_questions.append(job_questions)

    return all_questions


def format_markdown_output(interview_questions):
    """
    Format interview questions as markdown
    """
    md = "# Interview Preparation Guide\n\n"
    md += "Generated interview questions based on skill gap analysis.\n\n"

    for job_data in interview_questions:
        md += f"## {job_data['job_title']}\n\n"
        md += f"**Company**: {job_data['company']}\n\n"
        md += f"**Match Score**: {job_data['overall_match_score']}%\n\n"
        if job_data['job_url']:
            md += f"**Job URL**: {job_data['job_url']}\n\n"

        md += "---\n\n"

        for gap_data in job_data['questions_by_gap']:
            skill = gap_data['skill']
            importance = gap_data['importance']
            gap_type = gap_data['gap_type']

            md += f"### {skill}\n\n"
            md += f"**Gap Type**: {gap_type}  \n"
            md += f"**Priority**: {importance.upper()}\n\n"

            md += "#### Questions:\n\n"
            for i, question in enumerate(gap_data['questions'], 1):
                md += f"{i}. {question}\n\n"

            md += "---\n\n"

    # Add study recommendations
    md += "\n## Study Recommendations\n\n"
    md += "### For Missing Skills (High Priority)\n"
    md += "1. Take an online course or tutorial\n"
    md += "2. Build a small project to gain hands-on experience\n"
    md += "3. Read official documentation\n"
    md += "4. Practice with sample problems or exercises\n\n"

    md += "### For Weak Skills (Medium Priority)\n"
    md += "1. Deepen your understanding with advanced tutorials\n"
    md += "2. Study best practices and design patterns\n"
    md += "3. Review production-scale use cases\n"
    md += "4. Practice explaining concepts clearly\n\n"

    md += "### Interview Preparation Tips\n"
    md += "- Practice answering questions out loud\n"
    md += "- Use the STAR method for behavioral questions\n"
    md += "- Prepare specific examples from your experience\n"
    md += "- Research the company and role thoroughly\n"
    md += "- Have questions ready to ask the interviewer\n"

    return md


def main():
    parser = argparse.ArgumentParser(description='Generate interview prep questions from gap analysis')
    parser.add_argument('--gap-analysis', required=True, help='Path to gap analysis JSON file')
    parser.add_argument('--questions-per-gap', type=int, default=10, help='Number of questions per skill gap')
    parser.add_argument('--output', required=True, help='Output markdown file path')

    args = parser.parse_args()

    # Load gap analysis
    try:
        with open(args.gap_analysis, 'r', encoding='utf-8') as f:
            gap_analysis = json.load(f)
    except FileNotFoundError:
        print(f"Error: Gap analysis file not found: {args.gap_analysis}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading gap analysis: {e}")
        sys.exit(1)

    # Generate questions
    print(f"Generating interview preparation questions...")
    interview_questions = generate_interview_questions(gap_analysis, args.questions_per_gap)

    # Format as markdown
    markdown_output = format_markdown_output(interview_questions)

    # Save to file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print(f"\nInterview prep guide saved to: {args.output}")
    except Exception as e:
        print(f"Error saving output: {e}")
        sys.exit(1)

    # Print summary
    total_questions = sum(
        len(gap['questions'])
        for job in interview_questions
        for gap in job['questions_by_gap']
    )
    print(f"Generated {total_questions} total questions across {len(interview_questions)} jobs")


if __name__ == '__main__':
    main()
