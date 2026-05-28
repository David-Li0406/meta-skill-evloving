#!/usr/bin/env python3
"""
Agent Evaluation Tool for Copilot FC
Performs deterministic agent evaluation based on query analysis, file patterns, and intent patterns.
Inspired by Claude Code skill activation hooks.
"""

import json
import sys
import re
from typing import Dict, List, Tuple, Optional

class AgentEvaluator:
    def __init__(self):
        self.agents = {
            "Diataxis-Documentation-Expert": {
                "description": "Specialized agent for creating and organizing documentation using the Diátaxis framework",
                "keywords": ["documentation", "docs", "diataxis", "tutorial", "guide", "readme", "api docs", "extract knowledge"],
                "file_patterns": ["*.md", "docs/**", "README*", "CHANGELOG*", "**/docs/**"],
                "intent_patterns": [r"\b(create|write|organize)\b.*\b(documentation|docs|readme)\b", r"\b(diataxis|tutorial|guide)\b"],
                "priority": "high",
                "relevance_score": 0
            },
            "Generic-Research-Agent": {
                "description": "Expert researcher delivering validated, implementation-ready findings across any domain using available tools",
                "keywords": ["research", "investigate", "find", "analyze", "study", "explore", "discover", "conduct research"],
                "file_patterns": [],
                "intent_patterns": [r"\b(research|investigate|analyze|study|explore)\b.*\b(find|discover|learn)\b", r"\b(how to|what is|explain)\b.*\b(work|function|implement)\b"],
                "priority": "high",
                "relevance_score": 0
            },
            "Git-Committer": {
                "description": "Handles git operations including atomic commits, conventional commit messages, and git workflow management",
                "keywords": ["commit", "push", "git", "atomic commit", "atomic commits plan"],
                "file_patterns": [],
                "intent_patterns": [r"\b(commit|push|merge)\b.*\b(changes|code|files)\b", r"\b(git|version control)\b.*\b(operation|workflow)\b"],
                "priority": "critical",
                "relevance_score": 0
            },
            "Instruction-Writer": {
                "description": "Creates path-specific GitHub Copilot `*.instructions.md` files that follow the official frontmatter (`applyTo`) format, include examples, and validate common glob targets",
                "keywords": ["instruction", "guideline", "rule", "coding standard", "best practice", "copilot", "instruction file", "revise custom instruction", "create custom instruction"],
                "file_patterns": ["*.instructions.md", "**/instructions/**", ".github/**/*.md", ".vscode/**/*.md"],
                "intent_patterns": [r"\b(create|write|generate)\b.*\b(instruction|coding standard|guideline)\b", r"\b(copilot|github)\b.*\b(instruction|rule)\b"],
                "priority": "high",
                "relevance_score": 0
            },
            "Knowledge-Graph-Agent": {
                "description": "Generic sub-agent for Knowledge Graph memory management - handles entity resolution, relation mapping, and context retrieval for any parent agent",
                "keywords": ["knowledge", "graph", "memory", "entity", "relation", "context", "data structure"],
                "file_patterns": [],
                "intent_patterns": [r"\b(knowledge|memory|context)\b.*\b(graph|structure|relation)\b", r"\b(entity|node|edge)\b.*\b(resolution|mapping)\b"],
                "priority": "low",
                "relevance_score": 0
            },
            "Mermaid-Agent": {
                "description": "Generate, validate, and render Mermaid diagrams from natural language descriptions",
                "keywords": ["diagram", "mermaid", "flowchart", "chart", "graph", "visual", "uml"],
                "file_patterns": ["*.mmd", "**/diagrams/**", "**/charts/**"],
                "intent_patterns": [r"\b(create|generate|draw)\b.*\b(diagram|chart|flowchart|graph)\b", r"\b(mermaid|uml|visual)\b.*\b(representation|design)\b"],
                "priority": "high",
                "relevance_score": 0
            },
            "Meta-Agent": {
                "description": "Expert architect for creating VS Code Custom Agents (.agent.md files)",
                "keywords": ["agent", "create", "custom agent", "persona", "tool", "meta", "architecture", "create new custom agent", "revise custom agent"],
                "file_patterns": ["*.agent.md", "**/agents/**", ".github/**/*.md"],
                "intent_patterns": [r"\b(create|build|design)\b.*\b(agent|persona|tool)\b", r"\b(custom|vs code)\b.*\b(agent|extension)\b"],
                "priority": "high",
                "relevance_score": 0
            },
            "PM-Changelog": {
                "description": "Generates monthly changelog summaries for non-tech stakeholders from weekly raw changelogs",
                "keywords": ["changelog", "release", "summary", "monthly", "stakeholder", "communication", "generate monthly summary", "generate monthly changelog"],
                "file_patterns": ["CHANGELOG*", "**/changelogs/**", "**/releases/**"],
                "intent_patterns": [r"\b(create|generate|write)\b.*\b(changelog|release notes)\b", r"\b(monthly|summary)\b.*\b(stakeholder|communication)\b"],
                "priority": "medium",
                "relevance_score": 0
            }
        }

    def match_file_patterns(self, file_path: str, patterns: List[str]) -> bool:
        """
        Convert glob patterns to regex and match against file path.
        Based on Claude Code hook implementation.
        """
        if not file_path or not patterns:
            return False

        for pattern in patterns:
            if not pattern.strip():  # Skip empty or whitespace-only patterns
                continue
            try:
                # Convert glob to regex: ** → .*, * → [^/]*, ? → .
                regex_pattern = pattern.replace('**', '.*').replace('*', '[^/]*').replace('?', '.')
                if re.search(regex_pattern, file_path, re.IGNORECASE):
                    return True
            except re.error:
                continue  # Skip invalid patterns
        return False

    def match_intent_patterns(self, text: str, patterns: List[str]) -> bool:
        """
        Match against regex intent patterns with error handling.
        Based on Claude Code hook implementation.
        """
        if not text or not patterns:
            return False

        for pattern in patterns:
            if not pattern.strip():  # Skip empty or whitespace-only patterns
                continue
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    return True
            except re.error:
                continue  # Skip invalid patterns
        return False

    def evaluate_query(self, query: str, file_path: Optional[str] = None) -> Dict:
        """
        Evaluate all agents against the query using keyword matching, intent patterns, and file patterns.
        Returns structured evaluation results with REQUIRED vs SUGGESTED sections.
        """
        query_lower = query.lower()

        evaluations = {}
        activated_agents = []
        required_agents = []  # Critical + High priority
        suggested_agents = []  # Medium + Low priority

        for agent_name, agent_data in self.agents.items():
            # Initialize scoring components
            keyword_matches = 0
            intent_matches = 0
            file_matches = 0

            # 1. Keyword matching (with word boundaries)
            for keyword in agent_data["keywords"]:
                if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', query_lower):
                    keyword_matches += 1

            # 2. Intent pattern matching
            if self.match_intent_patterns(query, agent_data["intent_patterns"]):
                intent_matches = 1

            # 3. File pattern matching
            if file_path and self.match_file_patterns(file_path, agent_data["file_patterns"]):
                file_matches = 1

            # Calculate relevance score (0-10)
            base_score = min(keyword_matches * 2, 6)  # Max 6 from keywords
            if intent_matches:
                base_score += 3  # Intent pattern match is strong signal
            if file_matches:
                base_score += 2  # File pattern match is contextual boost

            # Context-aware scoring boosts
            if "create" in query_lower and agent_name in ["Meta-Agent", "Instruction-Writer"]:
                base_score += 1
            if "document" in query_lower and agent_name == "Diataxis-Documentation-Expert":
                base_score += 1
            if ("research" in query_lower or "find" in query_lower) and agent_name == "Generic-Research-Agent":
                base_score += 1

            relevance_score = min(base_score, 10)
            agent_data["relevance_score"] = relevance_score

            # Priority-based activation thresholds
            priority = agent_data["priority"]
            if priority in ["critical", "high"]:
                is_relevant = relevance_score >= 4  # Lower threshold for high-priority agents
            else:
                is_relevant = relevance_score >= 6  # Higher threshold for medium/low priority

            # Special case: Git-Committer should activate on any git-related query
            if agent_name == "Git-Committer" and keyword_matches > 0:
                is_relevant = True

            evaluations[agent_name] = {
                "yes_no": "YES" if is_relevant else "NO",
                "reasoning": self._generate_reasoning(agent_name, relevance_score, keyword_matches, intent_matches, file_matches),
                "relevance_score": relevance_score,
                "keyword_matches": keyword_matches,
                "intent_matches": intent_matches,
                "file_matches": file_matches,
                "priority": priority
            }

            if is_relevant:
                activated_agents.append(agent_name)
                if priority in ["critical", "high"]:
                    required_agents.append(agent_name)
                else:
                    suggested_agents.append(agent_name)

        # Generate structured output like Claude hook
        context_parts = []
        if required_agents:
            context_parts.append('IMPORTANT GUIDELINES:')
            context_parts.append('')

            for agent_name in required_agents[:1]:  # Focus on primary agent
                agent_display = agent_name.replace('-', ' ')
                description = self.agents[agent_name]["description"]
                context_parts.append(f'The "{agent_display}" agent contains critical best practices for this request.')
                context_parts.append('Before proceeding, incorporate the agent\'s specialized knowledge to ensure:')
                context_parts.append('- Adherence to project patterns and conventions')
                context_parts.append('- Proper implementation approach')
                context_parts.append('- Quality and consistency with existing practices')
                if description:
                    context_parts.append('')
                    context_parts.append(f'This agent specializes in: {description}')

            if len(required_agents) > 1:
                other_agents = [name.replace('-', ' ') for name in required_agents[1:]]
                context_parts.append('')
                context_parts.append(f'Also consider: {", ".join(other_agents)} agents')
            context_parts.append('')

        if suggested_agents:
            if required_agents:
                context_parts.append('ADDITIONAL SUGGESTIONS:')
            else:
                context_parts.append('SUGGESTED AGENTS:')
            context_parts.append('')

            agent_names = [name.replace('-', ' ') for name in suggested_agents]
            context_parts.append(f'- Consider these agents for enhanced results: {", ".join(agent_names)}')

        return {
            "query": query,
            "file_path": file_path,
            "evaluations": evaluations,
            "activated_agents": activated_agents,
            "required_agents": required_agents,
            "suggested_agents": suggested_agents,
            "total_agents_evaluated": len(self.agents),
            "activation_count": len(activated_agents),
            "additional_context": '\n'.join(context_parts) if context_parts else ""
        }

    def _generate_reasoning(self, agent_name: str, score: int, keyword_matches: int, intent_matches: int, file_matches: int) -> str:
        """Generate deterministic reasoning based on scoring and match types."""
        match_types = []
        if keyword_matches > 0:
            match_types.append(f"keywords ({keyword_matches})")
        if intent_matches > 0:
            match_types.append("intent pattern")
        if file_matches > 0:
            match_types.append("file pattern")

        match_description = ", ".join(match_types) if match_types else "minimal overlap"

        if score >= 8:
            return f"High relevance ({score}/10) - strong match ({match_description}) and contextual fit"
        elif score >= 5:
            return f"Moderate relevance ({score}/10) - {match_description} detected"
        else:
            return f"Low relevance ({score}/10) - {match_description}"

def main():
    """Main entry point for the evaluation tool."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Query required",
            "usage": "python agent_evaluator.py 'your query here' [optional_file_path]"
        }))
        sys.exit(1)

    query = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else None

    evaluator = AgentEvaluator()
    result = evaluator.evaluate_query(query, file_path)

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()