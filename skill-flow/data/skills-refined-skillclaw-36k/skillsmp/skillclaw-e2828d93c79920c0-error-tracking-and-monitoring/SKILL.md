---
name: error-tracking-and-monitoring
description: Use this skill when you need to implement or improve error tracking and monitoring systems to quickly identify and resolve production issues.
---

# Error Tracking and Monitoring

You are an error tracking and observability expert specializing in implementing comprehensive error monitoring solutions. Set up error tracking systems, configure alerts, implement structured logging, and ensure teams can quickly identify and resolve production issues.

## Context
The user needs to implement or improve error tracking and monitoring. Focus on real-time error detection, meaningful alerts, error grouping, performance monitoring, and integration with popular error tracking services.

## Requirements
$ARGUMENTS

## Instructions

### 1. Error Tracking Analysis

Analyze current error handling and tracking:

**Error Analysis Script**
```python
import os
import re
import ast
from pathlib import Path
from collections import defaultdict

class ErrorTrackingAnalyzer:
    def analyze_codebase(self, project_path):
        """
        Analyze error handling patterns in codebase
        """
        analysis = {
            'error_handling': self._analyze_error_handling(project_path),
            'logging_usage': self._analyze_logging(project_path),
            'monitoring_setup': self._check_monitoring_setup(project_path),
            'error_patterns': self._identify_error_patterns(project_path),
            'recommendations': []
        }
        
        self._generate_recommendations(analysis)
        return analysis
    
    def _analyze_error_handling(self, project_path):
        """Analyze error handling patterns"""
        patterns = {
            'try_catch_blocks': 0,
            'unhandled_promises': 0,
            'generic_catches': 0,
            'error_types': defaultdict(int),
            'error_reporting': []
        }
        
        for file_path in Path(project_path).rglob('*.{js,ts,py,java,go}'):
            content = file_path.read_text(errors='ignore')
            
            # JavaScript/TypeScript patterns
            if file_path.suffix in ['.js', '.ts']:
                patterns['try_catch_blocks'] += len(re.findall(r'try\s*{', content))
                patterns['generic_catches'] += len(re.findall(r'catch\s*\([^)]*\)\s*{\s*}', content))
                patterns['unhandled_promises'] += len(re.findall(r'\.then\([^)]+\)(?!\.catch)', content))
```