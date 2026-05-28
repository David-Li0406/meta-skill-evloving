# P6 Project Controls Skill - Installation Guide

## Overview

This skill provides specialized capabilities for building automation tools that interface with Oracle Primavera P6 for mining and engineering project controls at BHP.

## What This Skill Provides

### Core Capabilities

1. **P6 Integration Knowledge**
   - P6 EPPM Web Services API (REST/SOAP)
   - XER file parsing and manipulation
   - Direct database access patterns
   - Authentication and session management

2. **Schedule Analysis Tools**
   - Automated schedule quality validation (DCMA 14-Point, AACE standards)
   - Critical path analysis
   - Float management and trending
   - Logic density checks
   - Constraint analysis

3. **Mining Industry Best Practices**
   - BHP-specific scheduling standards
   - Mining project phase definitions
   - Activity duration limits
   - Resource management guidelines
   - Weather and seasonal constraints
   - Risk management approaches

4. **Code Generation**
   - P6 API client templates
   - XER file parser (Python)
   - Schedule validator with HTML reporting
   - Database query patterns
   - Baseline comparison tools

### Bundled Resources

#### Scripts (`scripts/`)
- **parse_xer.py**: Complete XER file parser with data extraction
- **schedule_validator.py**: Automated schedule quality validation with HTML reporting

#### References (`references/`)
- **p6-database-schema.md**: P6 database tables, fields, and relationships
- **p6-api-guide.md**: P6 EPPM Web Services API documentation and examples
- **schedule-quality-rules.md**: Industry-standard validation rules (DCMA/AACE)
- **mining-standards.md**: Mining industry best practices and BHP standards

#### Assets (`assets/`)
- Directory structure for report templates and sample schedules

## Installation

### Option 1: Direct Installation (Recommended)

1. Copy the entire `p6-project-controls` folder to your Claude skills directory:
   ```
   .claude/skills/p6-project-controls/
   ```

2. Restart Claude Code or reload your configuration

3. Verify the skill is loaded:
   - The skill will appear in your available skills list
   - Claude will automatically use it when working with P6-related tasks

### Option 2: From Archive

1. Extract the skill archive to `.claude/skills/`:
   ```bash
   cd .claude/skills
   tar -xzf p6-project-controls.tar.gz
   ```

2. Verify the structure:
   ```
   .claude/skills/p6-project-controls/
   ├── SKILL.md
   ├── scripts/
   │   ├── parse_xer.py
   │   └── schedule_validator.py
   ├── references/
   │   ├── p6-database-schema.md
   │   ├── p6-api-guide.md
   │   ├── schedule-quality-rules.md
   │   └── mining-standards.md
   └── assets/
       └── README.md
   ```

## Using the Skill

### Automatic Activation

Claude will automatically activate this skill when you:
- Work with XER files
- Discuss P6 schedules or APIs
- Request schedule analysis or validation
- Build P6 automation tools
- Ask about mining project scheduling

### Example Prompts

**Schedule Analysis:**
```
Analyze this XER file for schedule quality issues following DCMA standards
```

**Code Generation:**
```
Create a Python script to connect to P6 API and extract critical activities
```

**Baseline Comparison:**
```
Build a tool to compare current schedule against baseline and identify variances >5 days
```

**Resource Analysis:**
```
Generate a resource histogram showing crew loading for the next 12 weeks
```

**Mining Standards:**
```
What are the activity duration limits for construction phase in mining projects?
```

### Using Bundled Scripts

**XER Parser:**
```python
from scripts.parse_xer import XERParser

parser = XERParser('my_schedule.xer')
activities = parser.get_activities()
critical = parser.get_critical_activities()
stats = parser.get_statistics()
parser.export_to_json('output.json')
```

**Schedule Validator:**
```python
from scripts.schedule_validator import ScheduleValidator

validator = ScheduleValidator()
issues = validator.validate_xer_file('schedule.xer')
validator.generate_html_report(issues, 'validation_report.html')
```

## Skill Customization

### Adding BHP-Specific Standards

Edit [references/mining-standards.md](references/mining-standards.md) to add:
- Project-specific activity codes
- Custom validation thresholds
- Company-specific WBS structures
- Internal reporting requirements

### Adding Report Templates

Place Excel, HTML, or PowerPoint templates in `assets/report-templates/`:
```
assets/
└── report-templates/
    ├── variance_report_template.xlsx
    ├── dashboard_template.html
    └── executive_summary.pptx
```

Reference them in your code generation requests.

### Adding Sample Schedules

Place test XER files in `assets/sample-schedules/` for:
- Development testing
- Demo purposes
- Validation edge cases

## Dependencies

The bundled Python scripts require:
- Python 3.7+
- No external dependencies (uses standard library only)

For API integration, you may need:
```bash
pip install requests
```

## Troubleshooting

### Skill Not Loading

1. Verify file location: `.claude/skills/p6-project-controls/SKILL.md`
2. Check YAML frontmatter is valid
3. Restart Claude Code

### Scripts Not Found

- Ensure scripts have execute permissions
- Use relative paths from skill directory
- Check Python is available in your environment

### Reference Files Not Loading

- Claude loads references automatically when needed
- Large reference files are loaded on-demand
- Check file paths in SKILL.md match actual locations

## Support

For issues or enhancements:
1. Check the skill's SKILL.md for usage guidance
2. Review reference documentation in `references/`
3. Examine example scripts in `scripts/`
4. Consult P6 official documentation for API details

## Version

**Version:** 1.0
**Created:** 2026-01-09
**For:** BHP Project Controls - Lead Developer

## License

This skill is created for internal use at BHP for project controls automation.
