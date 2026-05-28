# Pattern 10: CLI User Experience

**Problem**: The tool is hard to use. Options are confusing, output is ugly, and there's no help when things go wrong.

**Solution**: Follow CLI conventions, provide multiple output modes, add color and progress indicators, and guide users through setup.

---

## Concept

CLI UX answers: **"Is this tool pleasant to use?"**

Good CLI UX provides:
1. **Discoverability** — Users find features without reading docs
2. **Feedback** — Tool shows progress and results clearly
3. **Flexibility** — Output adapts to context (human vs script)
4. **Forgiveness** — Mistakes are easy to recover from

---

## Output Modes

Every CLI should support three output modes:

| Mode | Flag | Use Case |
|------|------|----------|
| **Human** | (default) | Interactive terminal use |
| **JSON** | `--json` | Script consumption, AI processing |
| **Quiet** | `--quiet` | Suppress non-essential output |

```python
import json
import sys
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class OutputConfig:
    json_mode: bool = False
    quiet: bool = False
    verbose: bool = False
    no_color: bool = False

class Output:
    """Unified output handling for all modes."""

    def __init__(self, config: OutputConfig):
        self.config = config
        self._results = []

    def info(self, message: str):
        """Informational message (hidden in quiet mode)."""
        if not self.config.quiet and not self.config.json_mode:
            print(message)

    def success(self, message: str):
        """Success message with green color."""
        if not self.config.quiet and not self.config.json_mode:
            if self.config.no_color:
                print(f"✓ {message}")
            else:
                print(f"\033[92m✓ {message}\033[0m")

    def error(self, message: str):
        """Error message (always shown, stderr)."""
        if self.config.json_mode:
            self._results.append({"type": "error", "message": message})
        else:
            if self.config.no_color:
                print(f"✗ {message}", file=sys.stderr)
            else:
                print(f"\033[91m✗ {message}\033[0m", file=sys.stderr)

    def result(self, data: dict):
        """Structured result data."""
        if self.config.json_mode:
            self._results.append(data)
        else:
            # Pretty print for humans
            for key, value in data.items():
                print(f"  {key}: {value}")

    def finish(self):
        """Output final JSON if in JSON mode."""
        if self.config.json_mode:
            print(json.dumps(self._results, indent=2))
```

---

## Progress Indicators

### Python: rich library

```python
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.console import Console

console = Console()

def process_with_progress(items: list):
    """Process items with a progress bar."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=len(items))

        for item in items:
            process_item(item)
            progress.update(task, advance=1)

# For indeterminate operations
def fetch_with_spinner():
    """Fetch data with a spinner."""
    with console.status("[bold green]Fetching data...") as status:
        data = fetch_from_api()
        status.update("[bold blue]Processing...")
        result = process_data(data)
    return result
```

### Node.js: ora spinner

```javascript
const ora = require('ora');

async function processWithSpinner() {
  const spinner = ora('Fetching data...').start();

  try {
    const data = await fetchFromApi();
    spinner.text = 'Processing...';

    const result = await processData(data);
    spinner.succeed('Done!');

    return result;
  } catch (error) {
    spinner.fail(`Error: ${error.message}`);
    throw error;
  }
}

// Progress bar with cli-progress
const cliProgress = require('cli-progress');

function processWithProgressBar(items) {
  const bar = new cliProgress.SingleBar({
    format: 'Progress |{bar}| {percentage}% | {value}/{total}',
  });

  bar.start(items.length, 0);

  for (const item of items) {
    processItem(item);
    bar.increment();
  }

  bar.stop();
}
```

---

## Interactive Setup

```python
def setup_wizard():
    """Guide users through first-time setup."""
    print("Welcome to My Tool! Let's get you set up.\n")

    # Step 1: Check dependencies
    print("Step 1/3: Checking dependencies...")
    if not check_dependencies():
        print("  Some dependencies are missing. Run 'my-tool doctor' for details.")
        return False
    print("  ✓ All dependencies found\n")

    # Step 2: Configure credentials
    print("Step 2/3: Configuring credentials...")
    api_key = input("  Enter your API key: ").strip()
    if not api_key:
        print("  ✗ API key is required")
        return False

    # Save config
    save_config({"api_key": api_key})
    print("  ✓ Credentials saved\n")

    # Step 3: Verify
    print("Step 3/3: Verifying setup...")
    if not verify_api_key(api_key):
        print("  ✗ API key is invalid")
        return False
    print("  ✓ Setup complete!\n")

    print("You're all set! Try running: my-tool --help")
    return True
```

---

## Help Text

### Argparse (Python)

```python
import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog="my-tool",
        description="Process files with advanced transformations.",
        epilog="Examples:\n"
               "  my-tool process input.txt -o output.txt\n"
               "  my-tool process *.txt --format json\n"
               "  my-tool doctor  # Check dependencies",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "input",
        help="Input file or glob pattern"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: stdout)"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-essential output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser
```

### Commander (Node.js)

```javascript
const { Command } = require('commander');

const program = new Command();

program
  .name('my-tool')
  .description('Process files with advanced transformations')
  .version('1.0.0');

program
  .command('process <input>')
  .description('Process input file(s)')
  .option('-o, --output <path>', 'Output file (default: stdout)')
  .option('-f, --format <type>', 'Output format (text|json|csv)', 'text')
  .option('-v, --verbose', 'Enable verbose output')
  .option('-q, --quiet', 'Suppress non-essential output')
  .option('--json', 'Output results as JSON')
  .option('--dry-run', 'Preview changes without applying')
  .addHelpText('after', `
Examples:
  $ my-tool process input.txt -o output.txt
  $ my-tool process "*.txt" --format json
  $ my-tool doctor  # Check dependencies
`)
  .action((input, options) => {
    // Handle command
  });

program
  .command('doctor')
  .description('Check dependencies and configuration')
  .action(() => {
    runDoctor();
  });

program.parse();
```

---

## Confirmation Prompts

```python
def confirm(message: str, default: bool = False) -> bool:
    """Ask user for confirmation."""
    suffix = " [Y/n] " if default else " [y/N] "
    response = input(message + suffix).strip().lower()

    if not response:
        return default
    return response in ("y", "yes")

# Usage
def delete_files(files: list, force: bool = False):
    if not force and len(files) > 10:
        print(f"This will delete {len(files)} files:")
        for f in files[:5]:
            print(f"  - {f}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")

        if not confirm("\nProceed?", default=False):
            print("Cancelled.")
            return

    # Actually delete
    for f in files:
        os.remove(f)
```

---

## Color Conventions

| Color | Meaning |
|-------|---------|
| **Green** | Success, completion |
| **Red** | Error, failure |
| **Yellow** | Warning, attention |
| **Blue/Cyan** | Information, progress |
| **Bold** | Important text |
| **Dim** | Secondary information |

```python
# Simple ANSI colors (no dependencies)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def colored(text: str, color: str) -> str:
    return f"{color}{text}{Colors.RESET}"

# Usage
print(colored("Success!", Colors.GREEN))
print(colored("Warning: something", Colors.YELLOW))
print(colored("Error: failed", Colors.RED))
```

---

## Checklist

- [ ] `--help` shows usage, options, and examples
- [ ] `--version` shows version number
- [ ] `--json` outputs machine-readable JSON
- [ ] `--quiet` suppresses non-essential output
- [ ] `--verbose` shows detailed progress
- [ ] `--dry-run` previews destructive operations
- [ ] Progress bars for long operations
- [ ] Colored output (with `--no-color` option)
- [ ] Confirmation prompts for destructive actions
- [ ] Interactive setup wizard for first run

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Wall of text | Hard to scan | Use sections, colors, whitespace |
| No progress | User thinks it's stuck | Add spinner or progress bar |
| Required confirmation | Breaks scripts | Use `--yes` flag |
| Color in pipes | Garbled output | Detect TTY, add `--no-color` |
