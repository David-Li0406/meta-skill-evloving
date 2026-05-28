"""Mutmut configuration to focus mutation testing on logic, not config data."""


def pre_mutation(context):
    """Skip mutations on configuration constants and logging statements."""
    line = context.current_source_line.strip()

    # Skip logger initialization
    if line.startswith("logger = "):
        context.skip = True
        return

    # Skip logger calls
    if line.startswith("logger."):
        context.skip = True
        return

    # Skip print statements (usually just informational output)
    if line.startswith("print(") or "print(" in line:
        context.skip = True
        return

    # Skip module-level path constants
    if "_DIR = Path" in line or "_PATH = Path" in line:
        context.skip = True
        return

    # Skip dictionary constant definitions (MODEL_COSTS, PERSONAS, etc.)
    # These are configuration data, not logic
    if line.endswith("= {") or line.endswith("= {}"):
        context.skip = True
        return

    # Skip cost/pricing constants
    if '"input":' in line or '"output":' in line:
        context.skip = True
        return

    # Skip shutil.which checks (environment-dependent)
    if "shutil.which(" in line:
        context.skip = True
        return

    # Skip tuple definitions with string constants (provider lists, etc.)
    if line.startswith("(") and line.count('"') >= 2:
        context.skip = True
        return

    # Skip help/usage message strings
    if "sys.exit(" in line:
        context.skip = True
        return

    # Skip environment variable settings
    if "os.environ[" in line:
        context.skip = True
        return

    # Skip constant assignments with string values
    if line.startswith('"') and line.endswith('",'):
        context.skip = True
        return

    # Skip frozenset/set constant definitions
    if "frozenset(" in line or line.endswith("= frozenset("):
        context.skip = True
        return

    # Skip lines inside frozenset definitions (model names)
    if line.startswith('"') and (line.endswith('",') or line.endswith('",')):
        context.skip = True
        return

    # Skip file= arguments in print calls
    if "file=sys.stderr" in line or "file=sys.stdout" in line:
        context.skip = True
        return

    # Skip f-string format specifiers (cosmetic)
    if ":," in line or ":.4f" in line or ":.2f" in line or ":.1f" in line:
        context.skip = True
        return

    # Skip warning/error message strings (don't affect program logic)
    if "Warning:" in line or "Error:" in line:
        context.skip = True
        return

    # Skip f-string warning messages
    if 'f"Warning:' in line or 'f"Error:' in line:
        context.skip = True
        return

    # Skip model name string constants in dictionaries
    if context.filename == "providers.py":
        # Skip MODEL_COSTS and BEDROCK_MODEL_MAP entries
        if ('{"input":' in line or '": "' in line) and context.current_line_index < 100:
            context.skip = True
            return
        # Skip provider info tuples in list_providers
        if "providers = [" in line or line.startswith('("'):
            context.skip = True
            return

    # Skip persona and focus area string content in prompts.py
    if context.filename == "prompts.py":
        # Skip the large string literals in FOCUS_AREAS and PERSONAS
        if context.current_line_index < 125 and '"""' not in line:
            # We're in the constant definitions section
            if line.startswith('"') or "CRITICAL FOCUS" in line:
                context.skip = True
                return

    # Skip model name constants in models.py
    if context.filename == "models.py":
        # Skip ALLOWED_CODEX_MODELS entries
        if context.current_line_index > 300 and line.startswith('"'):
            context.skip = True
            return
