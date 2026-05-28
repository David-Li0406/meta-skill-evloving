"""Language detection and comment pattern mapping."""

from typing import Dict, List, Tuple


# Extension to language mapping
EXTENSION_TO_LANG: Dict[str, str] = {
    # Compiled languages
    ".rs": "Rust",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".java": "Java",
    ".go": "Go",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".cs": "C#",

    # Scripting languages
    ".py": "Python",
    ".rb": "Ruby",
    ".php": "PHP",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".lua": "Lua",
    ".pl": "Perl",
    ".sh": "Shell",
    ".bash": "Bash",
    ".zsh": "Zsh",

    # Markup/Data
    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".tex": "LaTeX",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "Sass",
    ".less": "Less",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".xml": "XML",
    ".toml": "TOML",
    ".ini": "INI",

    # Config/Build
    ".cmake": "CMake",
    "Makefile": "Makefile",
    ".mk": "Makefile",
    "Dockerfile": "Docker",
    ".dockerfile": "Docker",
}


# Comment patterns for each language
# Format: {'line': ['//', '#'], 'block': [('/*', '*/'), ('<!--', '-->')]}
COMMENT_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    "Rust": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "C": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "C++": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "C/C++ Header": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "C++ Header": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Java": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Go": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Swift": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Kotlin": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "C#": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Python": {
        "line": ["#"],
        "block_start": ['"""', "'''"],
        "block_end": ['"""', "'''"],
    },
    "Ruby": {
        "line": ["#"],
        "block_start": ["=begin"],
        "block_end": ["=end"],
    },
    "PHP": {
        "line": ["//", "#"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "JavaScript": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "TypeScript": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Lua": {
        "line": ["--"],
        "block_start": ["--[[", "--[["],
        "block_end": ["]]", "]]"],
    },
    "Perl": {
        "line": ["#"],
        "block_start": ["=pod", "=begin"],
        "block_end": ["=cut", "=end"],
    },
    "Shell": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "Bash": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "Zsh": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "Markdown": {
        "line": ["<!--"],  # HTML comments in MD
        "block_start": [],
        "block_end": [],
    },
    "reStructuredText": {
        "line": [".."],
        "block_start": [],
        "block_end": [],
    },
    "LaTeX": {
        "line": ["%"],
        "block_start": [],
        "block_end": [],
    },
    "HTML": {
        "line": ["//"],
        "block_start": ["<!--"],
        "block_end": ["-->"],
    },
    "CSS": {
        "line": [],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Sass": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "Less": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },
    "JSON": {
        "line": [],
        "block_start": [],
        "block_end": [],
    },
    "YAML": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "XML": {
        "line": [],
        "block_start": ["<!--"],
        "block_end": ["-->"],
    },
    "TOML": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "INI": {
        "line": ["#", ";"],
        "block_start": [],
        "block_end": [],
    },
    "CMake": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "Makefile": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
    "Docker": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
}


def detect_language(extension: str) -> str:
    """
    Detect language from file extension.

    Args:
        extension: File extension including the dot (e.g., '.rs', '.py')

    Returns:
        Language name as string, or 'Unknown' if not recognized
    """
    # Normalize extension to lowercase
    ext = extension.lower()

    # Direct lookup
    if ext in EXTENSION_TO_LANG:
        return EXTENSION_TO_LANG[ext]

    # Check for special files without dots
    if not ext:
        return "Unknown"

    # Return Unknown for unrecognized extensions
    return "Unknown"


def get_comment_patterns(language: str) -> Dict[str, List[str]]:
    """
    Get comment patterns for a language.

    Args:
        language: Language name

    Returns:
        Dictionary with keys:
        - 'line': list of line comment markers
        - 'block_start': list of block comment start markers
        - 'block_end': list of block comment end markers (corresponds to block_start)
    """
    if language in COMMENT_PATTERNS:
        return COMMENT_PATTERNS[language]

    # Default patterns for unknown languages
    return {
        "line": [],
        "block_start": [],
        "block_end": [],
    }


def is_line_comment(line: str, patterns: List[str]) -> bool:
    """
    Check if a line is a line comment.

    Args:
        line: Stripped line content
        patterns: List of line comment markers

    Returns:
        True if the line starts with any line comment marker
    """
    if not patterns:
        return False

    return any(line.startswith(marker) for marker in patterns)


def find_block_comment_start(line: str, patterns: List[str]) -> Tuple[bool, int]:
    """
    Find the start of a block comment in a line.

    Args:
        line: Stripped line content
        patterns: List of block comment start markers

    Returns:
        Tuple of (found, index) where index is the position of the marker
    """
    if not patterns:
        return False, -1

    for marker in patterns:
        idx = line.find(marker)
        if idx != -1:
            # Check if it's not inside a string (simple check)
            if not any(line[:idx].count(quote) % 2 == 1 for quote in ['"', "'"]):
                return True, idx

    return False, -1


def find_block_comment_end(line: str, patterns: List[str]) -> Tuple[bool, int]:
    """
    Find the end of a block comment in a line.

    Args:
        line: Stripped line content
        patterns: List of block comment end markers

    Returns:
        Tuple of (found, index) where index is the position after the marker
    """
    if not patterns:
        return False, -1

    for marker in patterns:
        idx = line.find(marker)
        if idx != -1:
            return True, idx + len(marker)

    return False, -1