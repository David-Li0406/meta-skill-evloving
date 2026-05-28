#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter Pro Max Design System Generator - Aggregates search results and applies reasoning
to generate comprehensive design system recommendations for Flutter apps.

Usage:
    from design_system import generate_design_system
    result = generate_design_system("fintech banking app", "MyApp")
    
    # With persistence (Master + Overrides pattern)
    result = generate_design_system("fintech banking app", "MyApp", persist=True)
    result = generate_design_system("fintech banking app", "MyApp", persist=True, page="dashboard")
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from core import search, DATA_DIR


# ============ CONFIGURATION ============
REASONING_FILE = "ui-reasoning.csv"

SEARCH_CONFIG = {
    "product": {"max_results": 1},
    "style": {"max_results": 3},
    "color": {"max_results": 2},
    "typography": {"max_results": 2},
    "pattern": {"max_results": 3},
    "architect": {"max_results": 2},
    "landing": {"max_results": 2}  # Landing page patterns for screen structure
}


# ============ DESIGN SYSTEM GENERATOR ============
class DesignSystemGenerator:
    """Generates design system recommendations from aggregated searches."""

    def __init__(self) -> None:
        self.reasoning_data: list[dict[str, str]] = self._load_reasoning()

    def _load_reasoning(self) -> list[dict[str, str]]:
        """Load reasoning rules from CSV."""
        filepath = DATA_DIR / REASONING_FILE
        if not filepath.exists():
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def _multi_domain_search(self, query: str, style_priority: list[str] | None = None) -> dict[str, Any]:
        """Execute searches across multiple domains."""
        results: dict[str, Any] = {}
        for domain, config in SEARCH_CONFIG.items():
            if domain == "style" and style_priority:
                # For style, also search with priority keywords
                priority_query = " ".join(style_priority[:2]) if style_priority else query
                combined_query = f"{query} {priority_query}"
                results[domain] = search(combined_query, domain, config["max_results"])
            else:
                results[domain] = search(query, domain, config["max_results"])
        return results

    def _find_reasoning_rule(self, category: str) -> dict[str, str]:
        """Find matching reasoning rule for a category."""
        category_lower = category.lower()

        # Try exact match first
        for rule in self.reasoning_data:
            if rule.get("App_Category", "").lower() == category_lower:
                return rule

        # Try partial match
        for rule in self.reasoning_data:
            app_cat = rule.get("App_Category", "").lower()
            if app_cat in category_lower or category_lower in app_cat:
                return rule

        # Try keyword match
        for rule in self.reasoning_data:
            app_cat = rule.get("App_Category", "").lower()
            keywords = app_cat.replace("/", " ").replace("-", " ").split()
            if any(kw in category_lower for kw in keywords):
                return rule

        return {}

    def _apply_reasoning(self, category: str, search_results: dict[str, Any]) -> dict[str, Any]:
        """Apply reasoning rules to search results with intelligent decision processing."""
        rule = self._find_reasoning_rule(category)

        if not rule:
            return {
                "pattern": "Clean Architecture + Feature-First",
                "style_priority": ["Minimalism", "Flat Design"],
                "color_mood": "Professional",
                "typography_mood": "Clean",
                "key_effects": "Subtle animations, smooth transitions",
                "anti_patterns": "",
                "decision_rules": {},
                "severity": "MEDIUM",
                "must_have_features": [],
                "conversion_focus": ""
            }

        # Parse decision rules JSON and extract must_have features
        decision_rules: dict[str, Any] = {}
        must_have_features: list[Any] = []
        try:
            decision_rules = json.loads(str(rule.get("Decision_Rules", "{}")))  
            # Extract must_have from decision rules
            for key, value in decision_rules.items():
                if key == "must_have" or key.startswith("must_have"):
                    must_have_features.append(value)
        except json.JSONDecodeError:
            pass

        # Determine conversion focus based on category
        conversion_focus = self._determine_conversion_focus(category)

        return {
            "pattern": rule.get("Recommended_Pattern", ""),
            "style_priority": [s.strip() for s in rule.get("Style_Priority", "").split("+")],
            "color_mood": rule.get("Color_Mood", ""),
            "typography_mood": rule.get("Typography_Mood", ""),
            "key_effects": rule.get("Key_Effects", ""),
            "anti_patterns": rule.get("Anti_Patterns", ""),
            "decision_rules": decision_rules,
            "severity": rule.get("Severity", "MEDIUM"),
            "must_have_features": must_have_features,
            "conversion_focus": conversion_focus
        }

    def _determine_conversion_focus(self, category: str) -> str:
        """Determine conversion focus based on app category."""
        category_lower = category.lower()
        
        conversion_map: dict[str, str] = {
            "e-commerce": "Purchase conversion, Add to cart, Quick checkout",
            "fintech": "Trust building, Security perception, Transaction completion",
            "banking": "Trust building, Security perception, Transaction completion",
            "health": "Appointment booking, Trust signals, Accessibility",
            "fitness": "Engagement, Progress motivation, Habit formation",
            "social": "Engagement, Retention, Content sharing",
            "education": "Progress tracking, Completion rates, Engagement",
            "productivity": "Task completion, Efficiency, Quick actions",
            "food": "Order conversion, Reorder, Quick checkout",
            "travel": "Booking conversion, Search efficiency, Trust",
            "gaming": "Engagement, Retention, In-app purchases",
        }
        
        for key, focus in conversion_map.items():
            if key in category_lower:
                return focus
        
        return "User engagement and task completion"

    def _select_best_match(self, results: list[dict[str, Any]], priority_keywords: list[str]) -> dict[str, Any]:
        """Select best matching result based on priority keywords."""
        if not results:
            return {}

        if not priority_keywords:
            return results[0]

        # First: try exact style name match
        for priority in priority_keywords:
            priority_lower = priority.lower().strip()
            for result in results:
                style_name = result.get("Style Category", "").lower()
                if priority_lower in style_name or style_name in priority_lower:
                    return result

        # Second: score by keyword match in all fields
        scored: list[tuple[int, dict[str, Any]]] = []
        for result in results:
            result_str = str(result).lower()
            score = 0
            for kw in priority_keywords:
                kw_lower = kw.lower().strip()
                # Higher score for style name match
                if kw_lower in result.get("Style Category", "").lower():
                    score += 10
                # Lower score for keyword field match
                elif kw_lower in result.get("Keywords", "").lower():
                    score += 3
                # Even lower for other field matches
                elif kw_lower in result_str:
                    score += 1
            scored.append((score, result))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored and scored[0][0] > 0 else results[0]

    def _extract_results(self, search_result: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract results list from search result dict."""
        return search_result.get("results", [])

    def generate(self, query: str, project_name: str | None = None) -> dict[str, Any]:
        """Generate complete design system recommendation with landing pattern intelligence."""
        # Step 1: First search product to get category
        product_result = search(query, "product", 1)
        product_results = product_result.get("results", [])
        category = "General"
        product_info = {}
        if product_results:
            product_info = product_results[0]
            category = product_info.get("Product Type", "General")

        # Step 2: Get reasoning rules for this category
        reasoning = self._apply_reasoning(category, {})
        style_priority = reasoning.get("style_priority", [])

        # Step 3: Multi-domain search with style priority hints
        search_results = self._multi_domain_search(query, style_priority)
        search_results["product"] = product_result  # Reuse product search

        # Step 4: Select best matches from each domain using priority
        style_results = self._extract_results(search_results.get("style", {}))
        color_results = self._extract_results(search_results.get("color", {}))
        typography_results = self._extract_results(search_results.get("typography", {}))
        pattern_results = self._extract_results(search_results.get("pattern", {}))
        architect_results = self._extract_results(search_results.get("architect", {}))
        landing_results = self._extract_results(search_results.get("landing", {}))

        best_style = self._select_best_match(style_results, reasoning.get("style_priority", []))
        best_color = color_results[0] if color_results else {}
        best_typography = typography_results[0] if typography_results else {}
        best_landing = landing_results[0] if landing_results else {}

        # Step 5: Build final recommendation
        # Combine effects from both reasoning and style search
        style_effects = best_style.get("Effects & Animation", "")
        reasoning_effects = reasoning.get("key_effects", "")
        combined_effects = style_effects if style_effects else reasoning_effects
        
        # Get landing pattern info
        landing_effects = best_landing.get("Recommended Effects", "")
        if landing_effects and not combined_effects:
            combined_effects = landing_effects

        return {
            "project_name": project_name or query.upper(),
            "category": category,
            "pattern": {
                "name": reasoning.get("pattern", "Clean Architecture"),
                "architecture": architect_results[0].get("layer", "") if architect_results else "Feature-First",
                "state_management": "Riverpod / BLoC",
                "recommended_patterns": [p.get("pattern_name", "") for p in pattern_results[:3]]
            },
            # NEW: Landing/Screen pattern from UI-UX Pro Max
            "screen_pattern": {
                "name": best_landing.get("Pattern Name", "Hero + Features + CTA"),
                "sections": best_landing.get("Section Order", "Hero > Features > CTA"),
                "cta_placement": best_landing.get("Primary CTA Placement", "Bottom + Sticky"),
                "color_strategy": best_landing.get("Color Strategy", ""),
                "conversion_optimization": best_landing.get("Conversion Optimization", "")
            },
            "style": {
                "name": best_style.get("Style Category", "Minimalism"),
                "type": best_style.get("Type", "General"),
                "effects": style_effects,
                "keywords": best_style.get("Keywords", ""),
                "best_for": best_style.get("Best For", ""),
                "do_not_use": best_style.get("Do Not Use For", "")
            },
            "colors": {
                "primary": best_color.get("Primary (Hex)", "#2563EB"),
                "secondary": best_color.get("Secondary (Hex)", "#3B82F6"),
                "cta": best_color.get("CTA (Hex)", "#F97316"),
                "background": "#FFFFFF",
                "surface": "#F8FAFC",
                "text": "#1E293B",
                "notes": best_color.get("Notes", ""),
                "strategy": best_landing.get("Color Strategy", reasoning.get("color_mood", ""))
            },
            "typography": {
                "heading": best_typography.get("Heading Font", "Inter"),
                "body": best_typography.get("Body Font", "Inter"),
                "mood": best_typography.get("Mood/Style Keywords", reasoning.get("typography_mood", "")),
                "best_for": best_typography.get("Best For", ""),
                "google_fonts_url": best_typography.get("Google Fonts URL", "")
            },
            "key_effects": combined_effects,
            "anti_patterns": reasoning.get("anti_patterns", ""),
            "decision_rules": reasoning.get("decision_rules", {}),
            "severity": reasoning.get("severity", "MEDIUM"),
            # NEW: Conversion and must-have features
            "conversion_focus": reasoning.get("conversion_focus", ""),
            "must_have_features": reasoning.get("must_have_features", [])
        }


# ============ OUTPUT FORMATTERS ============
BOX_WIDTH = 90

def format_ascii_box(design_system: dict[str, Any]) -> str:
    """Format design system as ASCII box for Flutter apps with screen pattern intelligence."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    screen_pattern = design_system.get("screen_pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    conversion_focus = design_system.get("conversion_focus", "")
    must_have_features = design_system.get("must_have_features", [])

    def wrap_text(text: str, prefix: str, width: int) -> list[str]:
        """Wrap long text into multiple lines."""
        if not text:
            return []
        words = text.split()
        lines: list[str] = []
        current_line = prefix
        for word in words:
            if len(current_line) + len(word) + 1 <= width - 2:
                current_line += (" " if current_line != prefix else "") + word
            else:
                if current_line != prefix:
                    lines.append(current_line)
                current_line = prefix + word
        if current_line != prefix:
            lines.append(current_line)
        return lines

    # Build output lines
    lines: list[str] = []
    w = BOX_WIDTH - 1

    lines.append("+" + "-" * w + "+")
    lines.append(f"|  TARGET: {project} - FLUTTER DESIGN SYSTEM".ljust(BOX_WIDTH) + "|")
    lines.append("+" + "-" * w + "+")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # NEW: Screen Pattern section (from UI-UX Pro Max)
    if screen_pattern.get("name"):
        lines.append(f"|  SCREEN PATTERN: {screen_pattern.get('name', '')}".ljust(BOX_WIDTH) + "|")
        if screen_pattern.get("sections"):
            sections_str = screen_pattern.get("sections", "")[:65]
            lines.append(f"|     Sections: {sections_str}".ljust(BOX_WIDTH) + "|")
        if screen_pattern.get("cta_placement"):
            lines.append(f"|     CTA: {screen_pattern.get('cta_placement', '')}".ljust(BOX_WIDTH) + "|")
        if screen_pattern.get("conversion_optimization"):
            for line in wrap_text(f"Conversion: {screen_pattern.get('conversion_optimization', '')}", "|     ", BOX_WIDTH):
                lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Architecture Pattern section
    lines.append(f"|  ARCHITECTURE: {pattern.get('name', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Structure: Feature-First / Clean Architecture".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     State: {pattern.get('state_management', 'Riverpod')}".ljust(BOX_WIDTH) + "|")
    if pattern.get('recommended_patterns'):
        patterns_str = ", ".join(filter(None, pattern.get('recommended_patterns', [])))[:60]
        lines.append(f"|     Patterns: {patterns_str}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Style section
    lines.append(f"|  UI STYLE: {style.get('name', '')}".ljust(BOX_WIDTH) + "|")
    if style.get("keywords"):
        for line in wrap_text(f"Keywords: {style.get('keywords', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if style.get("best_for"):
        for line in wrap_text(f"Best For: {style.get('best_for', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Colors section
    lines.append("|  COLOR PALETTE:".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Primary:    {colors.get('primary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Secondary:  {colors.get('secondary', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     CTA:        {colors.get('cta', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Background: {colors.get('background', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Surface:    {colors.get('surface', '')}".ljust(BOX_WIDTH) + "|")
    lines.append(f"|     Text:       {colors.get('text', '')}".ljust(BOX_WIDTH) + "|")
    if colors.get("notes"):
        for line in wrap_text(f"Notes: {colors.get('notes', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if colors.get("strategy"):
        for line in wrap_text(f"Strategy: {colors.get('strategy', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Typography section
    lines.append(f"|  TYPOGRAPHY: {typography.get('heading', '')} / {typography.get('body', '')}".ljust(BOX_WIDTH) + "|")
    if typography.get("mood"):
        for line in wrap_text(f"Mood: {typography.get('mood', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    if typography.get("best_for"):
        for line in wrap_text(f"Best For: {typography.get('best_for', '')}", "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    # Key Effects section
    if effects:
        lines.append("|  KEY EFFECTS:".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(effects, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # NEW: Conversion Focus section
    if conversion_focus:
        lines.append("|  CONVERSION FOCUS:".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(conversion_focus, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # NEW: Must-Have Features section
    if must_have_features:
        lines.append("|  MUST-HAVE FEATURES:".ljust(BOX_WIDTH) + "|")
        for feature in must_have_features:
            lines.append(f"|     ✓ {feature}".ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Anti-patterns section
    if anti_patterns:
        lines.append("|  AVOID (Anti-patterns):".ljust(BOX_WIDTH) + "|")
        for line in wrap_text(anti_patterns, "|     ", BOX_WIDTH):
            lines.append(line.ljust(BOX_WIDTH) + "|")
        lines.append("|" + " " * BOX_WIDTH + "|")

    # Flutter-specific checklist
    lines.append("|  PRE-DELIVERY CHECKLIST:".ljust(BOX_WIDTH) + "|")
    checklist_items = [
        "[ ] const constructors for immutable widgets",
        "[ ] Keys for lists and animated widgets",
        "[ ] Proper widget decomposition (no God widgets)",
        "[ ] Responsive: 375px, 768px, 1024px breakpoints",
        "[ ] Accessibility: Semantics labels, touch targets >= 48px",
        "[ ] Performance: ListView.builder for long lists",
        "[ ] Error handling: proper error/loading states"
    ]
    for item in checklist_items:
        lines.append(f"|     {item}".ljust(BOX_WIDTH) + "|")
    lines.append("|" + " " * BOX_WIDTH + "|")

    lines.append("+" + "-" * w + "+")

    return "\n".join(lines)


def format_markdown(design_system: dict[str, Any]) -> str:
    """Format design system as markdown with screen pattern intelligence."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    screen_pattern = design_system.get("screen_pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    conversion_focus = design_system.get("conversion_focus", "")
    must_have_features = design_system.get("must_have_features", [])

    lines: list[str] = []
    lines.append(f"## Flutter Design System: {project}")
    lines.append("")

    # NEW: Screen Pattern section (from UI-UX Pro Max)
    if screen_pattern.get("name"):
        lines.append("### Screen Pattern")
        lines.append(f"- **Pattern:** {screen_pattern.get('name', '')}")
        if screen_pattern.get("sections"):
            lines.append(f"- **Sections:** {screen_pattern.get('sections', '')}")
        if screen_pattern.get("cta_placement"):
            lines.append(f"- **CTA Placement:** {screen_pattern.get('cta_placement', '')}")
        if screen_pattern.get("conversion_optimization"):
            lines.append(f"- **Conversion:** {screen_pattern.get('conversion_optimization', '')}")
        lines.append("")

    # Architecture section
    lines.append("### Architecture")
    lines.append(f"- **Pattern:** {pattern.get('name', '')}")
    lines.append(f"- **Structure:** Feature-First / Clean Architecture")
    lines.append(f"- **State Management:** {pattern.get('state_management', 'Riverpod')}")
    if pattern.get('recommended_patterns'):
        patterns_str = ", ".join(filter(None, pattern.get('recommended_patterns', [])))
        lines.append(f"- **Recommended Patterns:** {patterns_str}")
    lines.append("")

    # Style section
    lines.append("### UI Style")
    lines.append(f"- **Name:** {style.get('name', '')}")
    if style.get('keywords'):
        lines.append(f"- **Keywords:** {style.get('keywords', '')}")
    if style.get('best_for'):
        lines.append(f"- **Best For:** {style.get('best_for', '')}")
    if style.get('do_not_use'):
        lines.append(f"- **Do Not Use For:** {style.get('do_not_use', '')}")
    lines.append("")

    # Colors section
    lines.append("### Color Palette")
    lines.append(f"| Role | Hex | Flutter |")
    lines.append(f"|------|-----|---------|")
    lines.append(f"| Primary | `{colors.get('primary', '')}` | `Color(0xFF{colors.get('primary', '#2563EB')[1:]})` |")
    lines.append(f"| Secondary | `{colors.get('secondary', '')}` | `Color(0xFF{colors.get('secondary', '#3B82F6')[1:]})` |")
    lines.append(f"| CTA | `{colors.get('cta', '')}` | `Color(0xFF{colors.get('cta', '#F97316')[1:]})` |")
    lines.append(f"| Background | `{colors.get('background', '')}` | `Color(0xFF{colors.get('background', '#FFFFFF')[1:]})` |")
    lines.append(f"| Surface | `{colors.get('surface', '')}` | `Color(0xFF{colors.get('surface', '#F8FAFC')[1:]})` |")
    lines.append(f"| Text | `{colors.get('text', '')}` | `Color(0xFF{colors.get('text', '#1E293B')[1:]})` |")
    if colors.get("notes"):
        lines.append(f"\n*Notes: {colors.get('notes', '')}*")
    if colors.get("strategy"):
        lines.append(f"\n*Color Strategy: {colors.get('strategy', '')}*")
    lines.append("")

    # Typography section
    lines.append("### Typography")
    lines.append(f"- **Heading:** {typography.get('heading', '')}")
    lines.append(f"- **Body:** {typography.get('body', '')}")
    if typography.get("mood"):
        lines.append(f"- **Mood:** {typography.get('mood', '')}")
    if typography.get("best_for"):
        lines.append(f"- **Best For:** {typography.get('best_for', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** {typography.get('google_fonts_url', '')}")
    lines.append("")

    # Key Effects section
    if effects:
        lines.append("### Key Effects")
        lines.append(f"{effects}")
        lines.append("")

    # NEW: Conversion Focus section
    if conversion_focus:
        lines.append("### Conversion Focus")
        lines.append(f"{conversion_focus}")
        lines.append("")

    # NEW: Must-Have Features section
    if must_have_features:
        lines.append("### Must-Have Features")
        for feature in must_have_features:
            lines.append(f"- ✓ {feature}")
        lines.append("")

    # Anti-patterns section
    if anti_patterns:
        lines.append("### Avoid (Anti-patterns)")
        newline_bullet = '\n- '
        lines.append(f"- {anti_patterns.replace(' + ', newline_bullet)}")
        lines.append("")

    # Pre-Delivery Checklist section
    lines.append("### Pre-Delivery Checklist")
    lines.append("- [ ] `const` constructors for immutable widgets")
    lines.append("- [ ] Keys for lists and animated widgets")
    lines.append("- [ ] Proper widget decomposition (no God widgets)")
    lines.append("- [ ] Responsive: 375px, 768px, 1024px breakpoints")
    lines.append("- [ ] Accessibility: Semantics labels, touch targets >= 48px")
    lines.append("- [ ] Performance: ListView.builder for long lists")
    lines.append("- [ ] Error handling: proper error/loading states")
    lines.append("")

    return "\n".join(lines)


# ============ PERSISTENCE FUNCTIONS ============
def persist_design_system(design_system: dict[str, Any], page: str | None = None, output_dir: str | None = None, page_query: str | None = None) -> dict[str, Any]:
    """
    Persist design system to design-system/<project>/ folder using Master + Overrides pattern.
    """
    base_dir = Path(output_dir) if output_dir else Path.cwd()
    
    # Use project name for project-specific folder
    project_name = design_system.get("project_name", "default")
    project_slug = project_name.lower().replace(' ', '-')
    
    design_system_dir = base_dir / "design-system" / project_slug
    pages_dir = design_system_dir / "pages"
    
    created_files: list[str] = []
    
    # Create directories
    design_system_dir.mkdir(parents=True, exist_ok=True)
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    master_file = design_system_dir / "MASTER.md"
    
    # Generate and write MASTER.md
    master_content = format_master_md(design_system)
    with open(master_file, 'w', encoding='utf-8') as f:
        f.write(master_content)
    created_files.append(str(master_file))
    
    # If page is specified, create page override file
    if page:
        page_file = pages_dir / f"{page.lower().replace(' ', '-')}.md"
        page_content = format_page_override_md(design_system, page, page_query)
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(page_content)
        created_files.append(str(page_file))
    
    return {
        "status": "success",
        "design_system_dir": str(design_system_dir),
        "created_files": created_files
    }


def format_master_md(design_system: dict[str, Any]) -> str:
    """Format design system as MASTER.md with hierarchical override logic."""
    project = design_system.get("project_name", "PROJECT")
    pattern = design_system.get("pattern", {})
    style = design_system.get("style", {})
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    effects = design_system.get("key_effects", "")
    anti_patterns = design_system.get("anti_patterns", "")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines: list[str] = []
    
    # Logic header
    lines.append("# Flutter Design System Master File")
    lines.append("")
    lines.append("> **LOGIC:** When building a specific screen, first check `design-system/pages/[screen-name].md`.")
    lines.append("> If that file exists, its rules **override** this Master file.")
    lines.append("> If not, strictly follow the rules below.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Project:** {project}")
    lines.append(f"**Generated:** {timestamp}")
    lines.append(f"**Category:** {design_system.get('category', 'General')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Architecture section
    lines.append("## Architecture")
    lines.append("")
    lines.append(f"- **Pattern:** {pattern.get('name', 'Clean Architecture')}")
    lines.append(f"- **Structure:** Feature-First")
    lines.append(f"- **State Management:** {pattern.get('state_management', 'Riverpod')}")
    lines.append("")
    lines.append("### Folder Structure")
    lines.append("```")
    lines.append("lib/")
    lines.append("├── core/                    # Shared utilities, constants, themes")
    lines.append("│   ├── theme/")
    lines.append("│   ├── utils/")
    lines.append("│   └── widgets/             # Reusable widgets")
    lines.append("├── features/")
    lines.append("│   └── [feature_name]/")
    lines.append("│       ├── data/            # Repositories, data sources")
    lines.append("│       ├── domain/          # Entities, use cases")
    lines.append("│       └── presentation/    # Screens, widgets, state")
    lines.append("└── main.dart")
    lines.append("```")
    lines.append("")
    
    # Global Rules section
    lines.append("## Global Rules")
    lines.append("")
    
    # Color Palette
    lines.append("### Color Palette")
    lines.append("")
    lines.append("| Role | Hex | Flutter Color |")
    lines.append("|------|-----|---------------|")
    primary_hex = colors.get('primary', '#2563EB').lstrip('#')
    secondary_hex = colors.get('secondary', '#3B82F6').lstrip('#')
    cta_hex = colors.get('cta', '#F97316').lstrip('#')
    bg_hex = colors.get('background', '#FFFFFF').lstrip('#')
    surface_hex = colors.get('surface', '#F8FAFC').lstrip('#')
    text_hex = colors.get('text', '#1E293B').lstrip('#')
    
    lines.append(f"| Primary | `#{primary_hex}` | `Color(0xFF{primary_hex.upper()})` |")
    lines.append(f"| Secondary | `#{secondary_hex}` | `Color(0xFF{secondary_hex.upper()})` |")
    lines.append(f"| CTA/Accent | `#{cta_hex}` | `Color(0xFF{cta_hex.upper()})` |")
    lines.append(f"| Background | `#{bg_hex}` | `Color(0xFF{bg_hex.upper()})` |")
    lines.append(f"| Surface | `#{surface_hex}` | `Color(0xFF{surface_hex.upper()})` |")
    lines.append(f"| Text | `#{text_hex}` | `Color(0xFF{text_hex.upper()})` |")
    lines.append("")
    
    if colors.get("notes"):
        lines.append(f"**Color Notes:** {colors.get('notes', '')}")
        lines.append("")
    
    # Typography
    lines.append("### Typography")
    lines.append("")
    lines.append(f"- **Heading Font:** {typography.get('heading', 'Inter')}")
    lines.append(f"- **Body Font:** {typography.get('body', 'Inter')}")
    if typography.get("mood"):
        lines.append(f"- **Mood:** {typography.get('mood', '')}")
    if typography.get("google_fonts_url"):
        lines.append(f"- **Google Fonts:** [{typography.get('heading', '')} + {typography.get('body', '')}]({typography.get('google_fonts_url', '')})")
    lines.append("")
    
    lines.append("**Font Sizes (Scale):**")
    lines.append("```dart")
    lines.append("// Display")
    lines.append("displayLarge: 57, displayMedium: 45, displaySmall: 36")
    lines.append("// Headline")
    lines.append("headlineLarge: 32, headlineMedium: 28, headlineSmall: 24")
    lines.append("// Title")
    lines.append("titleLarge: 22, titleMedium: 16, titleSmall: 14")
    lines.append("// Body")
    lines.append("bodyLarge: 16, bodyMedium: 14, bodySmall: 12")
    lines.append("// Label")
    lines.append("labelLarge: 14, labelMedium: 12, labelSmall: 11")
    lines.append("```")
    lines.append("")
    
    # Spacing
    lines.append("### Spacing")
    lines.append("")
    lines.append("| Token | Value | Usage |")
    lines.append("|-------|-------|-------|")
    lines.append("| `xs` | `4` | Tight gaps |")
    lines.append("| `sm` | `8` | Icon gaps, inline spacing |")
    lines.append("| `md` | `16` | Standard padding |")
    lines.append("| `lg` | `24` | Section padding |")
    lines.append("| `xl` | `32` | Large gaps |")
    lines.append("| `xxl` | `48` | Section margins |")
    lines.append("")
    
    # Border Radius
    lines.append("### Border Radius")
    lines.append("")
    lines.append("| Token | Value | Usage |")
    lines.append("|-------|-------|-------|")
    lines.append("| `xs` | `4` | Small chips, badges |")
    lines.append("| `sm` | `8` | Buttons, inputs |")
    lines.append("| `md` | `12` | Cards |")
    lines.append("| `lg` | `16` | Modals, bottom sheets |")
    lines.append("| `xl` | `24` | Large containers |")
    lines.append("| `full` | `9999` | Pills, circular |")
    lines.append("")
    
    # Style section
    lines.append("---")
    lines.append("")
    lines.append("## Style Guidelines")
    lines.append("")
    lines.append(f"**Style:** {style.get('name', 'Minimalism')}")
    lines.append("")
    if style.get("keywords"):
        lines.append(f"**Keywords:** {style.get('keywords', '')}")
        lines.append("")
    if style.get("best_for"):
        lines.append(f"**Best For:** {style.get('best_for', '')}")
        lines.append("")
    if effects:
        lines.append(f"**Key Effects:** {effects}")
        lines.append("")
    
    # Anti-Patterns section
    lines.append("---")
    lines.append("")
    lines.append("## Anti-Patterns (Do NOT Use)")
    lines.append("")
    if anti_patterns:
        anti_list = [a.strip() for a in anti_patterns.split("+")]
        for anti in anti_list:
            if anti:
                lines.append(f"- ❌ {anti}")
    lines.append("")
    lines.append("### Flutter-Specific Forbidden Patterns")
    lines.append("")
    lines.append("- ❌ **God Widgets** — Widgets > 200 lines, split into smaller components")
    lines.append("- ❌ **Business logic in UI** — Move to providers/blocs/use cases")
    lines.append("- ❌ **Missing const** — Always use `const` for immutable widgets")
    lines.append("- ❌ **setState abuse** — Use proper state management for complex state")
    lines.append("- ❌ **Hardcoded strings/colors** — Use theme and localization")
    lines.append("- ❌ **Missing error states** — Always handle loading/error/empty states")
    lines.append("")
    
    # Pre-Delivery Checklist
    lines.append("---")
    lines.append("")
    lines.append("## Pre-Delivery Checklist")
    lines.append("")
    lines.append("Before delivering any Flutter code, verify:")
    lines.append("")
    lines.append("- [ ] `const` constructors used for immutable widgets")
    lines.append("- [ ] Proper Keys for lists and animated widgets")
    lines.append("- [ ] Widget decomposition (no files > 300 lines)")
    lines.append("- [ ] Responsive: works on 375px, 768px, 1024px")
    lines.append("- [ ] Accessibility: Semantics widgets, touch targets >= 48x48")
    lines.append("- [ ] Performance: ListView.builder for long lists")
    lines.append("- [ ] State management: no setState for complex state")
    lines.append("- [ ] Theme: colors and text styles from ThemeData")
    lines.append("- [ ] Error handling: loading, error, empty states")
    lines.append("- [ ] Null safety: no force unwrapping (!)")
    lines.append("")
    
    return "\n".join(lines)


def format_page_override_md(design_system: dict[str, Any], page_name: str, page_query: str | None = None) -> str:
    """Format a page-specific override file."""
    project = design_system.get("project_name", "PROJECT")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_title = page_name.replace("-", " ").replace("_", " ").title()
    
    # Detect page type and generate intelligent overrides
    page_overrides = _generate_intelligent_overrides(page_name, page_query, design_system)
    
    lines: list[str] = []
    
    lines.append(f"# {page_title} Screen Overrides")
    lines.append("")
    lines.append(f"> **PROJECT:** {project}")
    lines.append(f"> **Generated:** {timestamp}")
    lines.append(f"> **Screen Type:** {page_overrides.get('page_type', 'General')}")
    lines.append("")
    lines.append("> ⚠️ **IMPORTANT:** Rules in this file **override** the Master file (`design-system/MASTER.md`).")
    lines.append("> Only deviations from the Master are documented here. For all other rules, refer to the Master.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Screen-specific rules
    lines.append("## Screen-Specific Rules")
    lines.append("")
    
    # Layout Overrides
    lines.append("### Layout Overrides")
    lines.append("")
    layout = page_overrides.get("layout", {})
    if layout:
        for key, value in layout.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- No overrides — use Master layout")
    lines.append("")
    
    # Widget Recommendations
    lines.append("### Recommended Widgets")
    lines.append("")
    widgets = page_overrides.get("widgets", [])
    if widgets:
        for widget in widgets:
            lines.append(f"- {widget}")
    else:
        lines.append("- Use standard widgets from Master")
    lines.append("")
    
    # State Management
    lines.append("### State Management")
    lines.append("")
    state = page_overrides.get("state", {})
    if state:
        for key, value in state.items():
            lines.append(f"- **{key}:** {value}")
    else:
        lines.append("- No overrides — use Master state management")
    lines.append("")
    
    # Recommendations
    lines.append("---")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    recommendations = page_overrides.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            lines.append(f"- {rec}")
    lines.append("")
    
    return "\n".join(lines)


def _generate_intelligent_overrides(page_name: str, page_query: str | None, design_system: dict[str, Any]) -> dict[str, Any]:
    """
    Generate intelligent overrides based on page type using layered search.
    Enhanced with UX guidelines and landing pattern intelligence from UI-UX Pro Max.
    """
    from core import search
    
    page_lower = page_name.lower()
    query_lower = (page_query or "").lower()
    combined_context = f"{page_lower} {query_lower}"
    
    # Multi-domain search for page-specific guidance
    pattern_search = search(combined_context, "pattern", max_results=2)
    widget_search = search(combined_context, "widget", max_results=3)
    ux_search = search(combined_context, "ux", max_results=3)
    landing_search = search(combined_context, "landing", max_results=1)
    
    pattern_results = pattern_search.get("results", [])
    widget_results = widget_search.get("results", [])
    ux_results = ux_search.get("results", [])
    landing_results = landing_search.get("results", [])
    
    # Detect page type
    page_type = _detect_page_type(combined_context)
    
    # Build overrides
    layout: dict[str, str] = {}
    widgets: list[str] = []
    state: dict[str, str] = {}
    recommendations: list[str] = []
    ux_guidelines: list[str] = []
    
    # Extract widget recommendations
    for widget in widget_results:
        widget_name = widget.get("Widget Name", "")
        if widget_name:
            widgets.append(f"`{widget_name}` - {widget.get('Description', '')[:60]}...")
    
    # Extract pattern recommendations
    for pattern in pattern_results:
        pattern_name = pattern.get("pattern_name", "")
        if pattern_name:
            recommendations.append(f"Consider `{pattern_name}` pattern")
    
    # NEW: Extract UX guidelines as recommendations
    for ux in ux_results:
        category = ux.get("Category", "")
        do_text = ux.get("Do", "")
        dont_text = ux.get("Don't", "")
        if do_text:
            ux_guidelines.append(f"✓ {category}: {do_text[:80]}...")
        if dont_text:
            ux_guidelines.append(f"✗ Avoid: {dont_text[:80]}...")
    
    # NEW: Extract landing pattern info for screen structure
    if landing_results:
        landing = landing_results[0]
        sections = landing.get("Section Order", "")
        cta_placement = landing.get("Primary CTA Placement", "")
        conversion = landing.get("Conversion Optimization", "")
        
        if sections:
            layout["Sections"] = sections[:80]
        if cta_placement:
            layout["CTA Placement"] = cta_placement
        if conversion:
            recommendations.append(f"Conversion: {conversion[:80]}...")
    
    # Add page-type specific defaults
    if "dashboard" in page_lower or "analytics" in page_lower:
        layout["Grid"] = "Use GridView or Wrap for widget cards"
        layout["Scrolling"] = "CustomScrollView with slivers"
        state["Refresh"] = "Pull-to-refresh with RefreshIndicator"
        state["Real-time"] = "Consider StreamBuilder for live data"
    elif "list" in page_lower or "search" in page_lower:
        layout["List"] = "ListView.builder for performance"
        layout["Pagination"] = "Infinite scroll with lazy loading"
        state["Search"] = "Debounced search with 300ms delay"
        state["Empty State"] = "Show helpful empty state with action"
    elif "form" in page_lower or "profile" in page_lower or "settings" in page_lower:
        layout["Form"] = "Single column, max 600px width"
        state["Validation"] = "Form validation with FormField"
        state["Autosave"] = "Consider debounced autosave for settings"
    elif "login" in page_lower or "auth" in page_lower:
        layout["Layout"] = "Centered, max 400px width"
        state["Auth"] = "Handle loading, error, success states"
        state["Biometric"] = "Consider biometric authentication"
    elif "checkout" in page_lower or "payment" in page_lower:
        layout["Layout"] = "Single column, focused flow"
        state["Progress"] = "Show step indicator for multi-step"
        state["Validation"] = "Real-time validation for payment fields"
    elif "chat" in page_lower or "message" in page_lower:
        layout["List"] = "Reversed ListView for chat bubbles"
        state["Real-time"] = "WebSocket or Firebase for live updates"
        state["Typing"] = "Show typing indicator"
    
    # Add UX guidelines to recommendations
    recommendations.extend(ux_guidelines[:3])  # Limit to top 3
    
    if not recommendations:
        recommendations = [
            "Refer to MASTER.md for all design rules",
            "Add specific overrides as needed for this screen"
        ]
    
    return {
        "page_type": page_type,
        "layout": layout,
        "widgets": widgets,
        "state": state,
        "recommendations": recommendations
    }


def _detect_page_type(context: str) -> str:
    """Detect page type from context."""
    context_lower = context.lower()
    
    page_patterns: list[tuple[list[str], str]] = [
        (["dashboard", "admin", "analytics", "metrics", "stats", "overview"], "Dashboard"),
        (["list", "search", "browse", "filter", "catalog"], "List / Search"),
        (["detail", "product", "item", "view"], "Detail View"),
        (["form", "edit", "create", "add", "new"], "Form / Input"),
        (["profile", "settings", "account", "preferences"], "Settings / Profile"),
        (["login", "signin", "signup", "register", "auth"], "Authentication"),
        (["home", "landing", "welcome"], "Home / Landing"),
        (["chat", "message", "conversation"], "Chat / Messaging"),
        (["checkout", "payment", "cart", "order"], "Checkout / Payment"),
    ]
    
    for keywords, page_type in page_patterns:
        if any(kw in context_lower for kw in keywords):
            return page_type
    
    return "General"


# ============ MAIN ENTRY POINT ============
def generate_design_system(query: str, project_name: str | None = None, output_format: str = "ascii", 
                           persist: bool = False, page: str | None = None, output_dir: str | None = None) -> str:
    """
    Main entry point for design system generation.

    Args:
        query: Search query (e.g., "fintech banking app", "e-commerce mobile")
        project_name: Optional project name for output header
        output_format: "ascii" (default) or "markdown"
        persist: If True, save design system to design-system/ folder
        page: Optional page name for page-specific override file
        output_dir: Optional output directory (defaults to current working directory)

    Returns:
        Formatted design system string
    """
    generator = DesignSystemGenerator()
    design_system = generator.generate(query, project_name)
    
    # Persist to files if requested
    if persist:
        persist_design_system(design_system, page, output_dir, query)

    if output_format == "markdown":
        return format_markdown(design_system)
    return format_ascii_box(design_system)


# ============ CLI SUPPORT ============
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Flutter Design System")
    parser.add_argument("query", help="Search query (e.g., 'fintech banking app')")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Output format")
    parser.add_argument("--persist", action="store_true", help="Save to design-system/ folder")
    parser.add_argument("--page", type=str, default=None, help="Create page-specific override file")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory")

    args = parser.parse_args()

    result = generate_design_system(
        args.query, 
        args.project_name, 
        args.format,
        persist=args.persist,
        page=args.page,
        output_dir=args.output_dir
    )
    print(result)
    
    if args.persist:
        project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
        print("\n" + "=" * 60)
        print(f"✅ Design system persisted to design-system/{project_slug}/")
        print(f"   📄 design-system/{project_slug}/MASTER.md (Global Source of Truth)")
        if args.page:
            page_filename = args.page.lower().replace(' ', '-')
            print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md (Screen Overrides)")
        print("")
        print(f"📖 Usage: When building a screen, check design-system/{project_slug}/pages/[screen].md first.")
        print(f"   If exists, its rules override MASTER.md. Otherwise, use MASTER.md.")
        print("=" * 60)
