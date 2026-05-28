---
name: team-workflow-and-code-analysis
description: Use this skill for managing team workflows, analyzing code quality, and tracking weight loss progress.
---

# Team Workflow and Code Analysis Skill

This skill combines team workflow management, code analysis, and weight loss tracking functionalities.

## Core Features

### 1. Workflow Management
- **Workflow Templates**: Supports GitFlow, GitHub Flow, etc.
- **Code Review**: Automates assignment and management of code reviews.
- **Release Management**: Handles version control and automated releases.
- **Team Standards**: Enforces commit message conventions.
- **Tool Integration**: Integrates with tools like JIRA and Slack.

#### Quick Usage
```bash
# Initialize workflow
/workflow init --template <template_name>

# Start a feature branch
/workflow start-feature <issue_id> "<feature_description>"

# Assign a review
/workflow assign-review

# Release a version
/workflow release --type <release_type>
```

### 2. Code Analysis
- **Code Quality Assessment**: Evaluates readability, naming conventions, structure, and comment quality.
- **Complexity Analysis**: Measures cyclomatic complexity, cognitive complexity, and checks for nested depth.
- **Duplicate Code Detection**: Identifies similar code snippets and suggests refactoring opportunities.
- **Best Practices Check**: Assesses the use of design patterns, SOLID principles, and error handling.

#### Supported Languages
- JavaScript/TypeScript, Python, Java, C#, Go, Ruby, PHP

### 3. Weight Loss Analysis
- **Body Composition Analysis**: Calculates BMI, body fat percentage, and waist-to-hip ratio.
- **Metabolic Rate Calculation**: Uses Harris-Benedict, Mifflin-St Jeor, and Katch-McArdle formulas to determine BMR and TDEE.
- **Energy Deficit Management**: Tracks daily caloric intake and expenditure to manage weight loss goals.
- **Phase Management**: Monitors weight loss progress, plateau detection, and maintenance phases.

#### Example Commands
```bash
# Set up weight loss plan
/fitness:weightloss-setup --weight <weight> --height <height> --age <age> --gender <gender>

# Calculate metabolic rate
/fitness:weightloss-bmr --formula <formula_name>

# Track energy deficit
/nutrition:weightloss-track --intake <caloric_intake> --exercise <caloric_expenditure>

# Generate phase report
/fitness:weightloss-report
```

## Configuration Options

### Workflow Configuration
```json
{
  "workflow": {
    "template": "<template_name>",
    "autoReview": true,
    "autoRelease": false,
    "integrations": ["<tool1>", "<tool2>"]
  }
}
```

### Code Analysis Configuration
```json
{
  "analysis": {
    "maxFunctionLength": <max_length>,
    "maxNestingDepth": <max_depth>,
    "maxComplexity": <max_complexity>,
    "excludePatterns": ["<pattern1>", "<pattern2>"],
    "rules": {
      "naming": {
        "enabled": true,
        "camelCase": true,
        "snake_case": false
      },
      "complexity": {
        "enabled": true,
        "maxCognitiveComplexity": <max_complexity>
      },
      "duplicates": {
        "enabled": true,
        "minLines": <min_lines>,
        "similarity": <similarity_threshold>
      }
    }
  }
}
```

## Best Practices
1. **For Development**: Design clear code structures, follow coding standards, and conduct self-reviews.
2. **For Team Collaboration**: Establish unified coding standards, hold regular code review meetings, and share improvement experiences.
3. **For Weight Management**: Monitor caloric intake, adjust plans based on progress, and ensure safe weight loss rates.

## Safety Principles
- Ensure caloric intake does not fall below recommended levels.
- Maintain a safe weight loss rate of 0.5-1kg per week.

---

**Skill Version**: v1.0  
**Last Updated**: 2026-01-14  
**Maintainer**: WellAlly Tech