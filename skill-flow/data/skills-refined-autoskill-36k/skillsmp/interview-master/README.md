# Interview Master Skill

Comprehensive interview preparation and career development skill for Claude Code.

## Features

1. **Interview Question Generation** - Generate role-specific technical interview questions
2. **Resume Optimization** - Analyze and improve resume content
3. **Mock Interview Simulation** - Conduct realistic interview practice sessions
4. **Git-Based Resume Generation** - Extract project experience from git commits
5. **Interview Preparation Guidance** - Personalized study roadmaps

## Installation

Copy this skill directory to your Claude Code plugin's `skills/` directory:

```bash
cp -r interview-master /path/to/your-plugin/skills/
```

## Usage Examples

### Generate Interview Questions
```
User: "Generate interview questions for a senior full-stack developer position"
Claude: [Uses interview-questions-bank.md to create tailored questions]
```

### Optimize Resume
```
User: "Review my resume and give me feedback"
Claude: [Analyzes resume using resume-best-practices.md]
```

### Generate Resume from Git
```
User: "Analyze my commits in this repository and generate resume content"
Claude: [Executes git analysis scripts and generates resume sections]
```

### Mock Interview
```
User: "Conduct a mock interview for backend engineer role"
Claude: [Simulates realistic interview with questions and feedback]
```

## Git Analysis Scripts

### Prerequisites
- Git 2.20+
- Bash 4.0+
- Python 3.8+ (for calculate-impact.py)

### Running Scripts Manually

**Analyze Commits:**
```bash
./scripts/analyze-commits.sh "Your Name" /path/to/repo
```

**Extract Tech Stack:**
```bash
./scripts/extract-tech-stack.sh /path/to/repo "Your Name"
```

**Calculate Impact:**
```bash
python scripts/calculate-impact.py /path/to/repo "Your Name"
```

**Generate Complete Resume Data:**
```bash
./scripts/generate-resume-data.sh "Your Name" /path/to/repo > resume-data.json
```

## File Structure

```
interview-master/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
├── scripts/                    # Git analysis automation
│   ├── analyze-commits.sh      # Commit history analysis
│   ├── extract-tech-stack.sh   # Technology detection
│   ├── calculate-impact.py     # Impact score calculation
│   └── generate-resume-data.sh # Data aggregation
├── references/                 # Detailed guides
│   ├── interview-questions-bank.md
│   ├── resume-best-practices.md
│   ├── algorithm-prep.md
│   ├── system-design-prep.md
│   ├── behavioral-interview.md
│   ├── tech-stack-keywords.md
│   └── project-impact-metrics.md
├── examples/                   # Working examples
│   ├── good-resume-examples.md
│   ├── interview-questions-set.md
│   ├── mock-interview-dialogue.md
│   └── git-analysis-output.json
└── assets/                     # Templates
    ├── resume-template.md
    └── resume-template.json
```

## Skill Triggers

This skill activates when users say:
- "generate interview questions"
- "prepare for interview"
- "optimize resume"
- "conduct mock interview"
- "analyze git commits for resume"
- "generate resume from code"
- "review my resume"

## Customization

### Adding Interview Questions
Edit `references/interview-questions-bank.md` to add questions for new roles or categories.

### Updating Tech Keywords
Modify `references/tech-stack-keywords.md` to recognize new technologies.

### Adjusting Impact Scoring
Edit `scripts/calculate-impact.py` to change impact score weightings.

## Best Practices

1. **Git Analysis**: Ensure clean commit history for best results
2. **Resume Review**: Provide context about target role for tailored feedback
3. **Mock Interviews**: Specify seniority level and focus areas
4. **Privacy**: Redact sensitive information before sharing resume

## Troubleshooting

**Scripts not executable:**
```bash
chmod +x scripts/*.sh
```

**Python script fails:**
```bash
python3 scripts/calculate-impact.py /path/to/repo "Author Name"
```

**No commits found:**
- Check author name spelling
- Verify git repository path
- Try using email instead of name

## Contributing

To extend this skill:
1. Add new reference files for additional topics
2. Create example files for new scenarios
3. Update SKILL.md to reference new resources
4. Test with various user queries

## Version

v0.1.0 - Initial release

## License

MIT License
