# Python Code Style Guide

Conventions for Python code in Sun Lab projects.

---

## Contents

- [Docstrings](#docstrings)
- [Type Annotations](#type-annotations)
- [Naming Conventions](#naming-conventions)
- [Function Calls](#function-calls)
- [Error Handling](#error-handling)
- [Ataraxis Library Preferences](#ataraxis-library-preferences)
- [Numba Functions](#numba-functions)
- [Comments](#comments)
- [Imports](#imports)
- [Class Design](#class-design)
- [Dataclass Conventions](#dataclass-conventions)
- [I/O Separation](#io-separation)
- [Context Managers](#context-managers)
- [Comprehensions](#comprehensions)
- [Blank Lines](#blank-lines)
- [Pathlib Conventions](#pathlib-conventions)
- [Trailing Commas](#trailing-commas)
- [Line Length and Formatting](#line-length-and-formatting)
- [Linting and Code Quality](#linting-and-code-quality)
- [Test Files](#test-files)
- [Input/Output Examples](#inputoutput-examples)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Verification Checklist](#verification-checklist)

---

## Docstrings

Use **Google-style docstrings** with sections in this order:
**Summary → Extended Description → Notes → Args → Returns → Raises**

```python
def function_name(param1: int, param2: str = "default") -> bool:
    """Brief one-line summary of what the function does.

    Extended description goes here if needed. This is optional and should only be used when the
    function's behavior is too complex to be fully explained by the summary line. Most functions
    should not need this section.

    Notes:
        Additional context, background, or implementation details. Use this for explaining algorithms,
        referencing papers, or clarifying non-obvious behavior. Multi-sentence explanations go here.

    Args:
        param1: Description without repeating the type (types are in signature).
        param2: Description of parameter with default value behavior if relevant.

    Returns:
        Description of return value. For simple returns, one line is sufficient. For complex returns
        (tuples, dicts), describe each element in prose form.

    Raises:
        ValueError: When this error occurs and why.
        TypeError: When this error occurs and why.
    """
```

**Section order**: Summary line first, then extended description (if needed), then Notes, Args, Returns, and Raises.
Do not include Examples sections or in-code examples in docstrings.

### Rules

- **Punctuation**: Always use proper punctuation in all documentation.
- **Imperative mood**: Use verbs like "Computes...", "Defines...", "Configures..." for ALL members.
- **Boolean descriptions**: Use "Determines whether..." for boolean parameters.
- **Parameters**: Start descriptions with uppercase. Don't repeat type info.
- **Returns**: Describe what is returned, not the type.
- **Prose over lists**: Always use prose instead of bullet lists or dashes in docstrings.

### Class Docstrings with Attributes

For classes, include an Attributes section listing all instance attributes:

```python
class DataProcessor:
    """Processes experimental data for analysis.

    Args:
        data_path: Path to the input data file.
        sampling_rate: The sampling rate in Hz.
        enable_filtering: Determines whether to apply bandpass filtering.

    Attributes:
        _data_path: Cached path to input data.
        _sampling_rate: Cached sampling rate parameter.
        _enable_filtering: Cached filtering flag.
        _processed_data: Dictionary storing processed results.
    """
```

### Enum and Dataclass Attributes

For enums and dataclasses, document each attribute inline using triple-quoted strings:

```python
class VisualizerMode(IntEnum):
    """Defines the display modes for the BehaviorVisualizer."""

    LICK_TRAINING = 0
    """Displays only lick sensor and valve plots."""
    RUN_TRAINING = 1
    """Displays lick, valve, and running speed plots."""
    EXPERIMENT = 2
    """Displays all plots including the trial performance panel."""


@dataclass
class SessionConfig:
    """Defines the configuration parameters for an experiment session."""

    animal_id: str
    """The unique identifier for the animal."""
    session_duration: float
    """The duration of the session in seconds."""
```

### Property Docstrings

```python
@property
def field_shape(self) -> tuple[int, int]:
    """Returns the shape of the data field as (height, width)."""
    return self._field_shape
```

### Module Docstrings

Follow the same imperative mood pattern as other docstrings:

```python
"""Provides assets for processing and analyzing neural imaging data."""
```

### CLI Command Docstrings

CLI commands use a specialized format because Click parses these into help messages. Do not use standard docstring
sections (Notes, Args, Returns, Raises) as they will appear verbatim in the CLI help output.

```python
@click.command()
def process_data(input_path: Path, output_path: Path) -> None:
    """Processes raw experimental data and saves the results.

    This command reads data from the input path, applies standard preprocessing
    steps, and writes the processed output to the specified location.
    """
```

### MCP Server Tool Docstrings

MCP tools serve dual purposes: documenting for developers and providing instructions to AI agents.

```python
@mcp.tool()
def start_video_session(
    output_directory: str,
    frame_rate: int = 30,
) -> str:
    """Starts a video capture session with the specified parameters.

    Creates a VideoSystem instance and begins acquiring frames from the camera.

    Important:
        The AI agent calling this tool MUST ask the user to provide the output_directory path
        before calling this tool. Do not assume or guess the output directory.

    Args:
        output_directory: The path to the directory where video files will be saved.
        frame_rate: The target frame rate in frames per second. Defaults to 30.
    """
```

### MCP Server Response Formatting

MCP tool responses should be concise and information-dense.

```python
# Good - concise, information-dense
return f"Session started: {interface} #{camera_index} {width}x{height}@{frame_rate}fps -> {output_directory}"

# Avoid - verbose multi-line formatting
return (
    f"Video Session Started\n"
    f"• Interface: {interface}\n"
    f"• Camera: {camera_index}\n"
)
```

**Formatting conventions**:

- **Concise output**: Keep responses to a single line when possible
- **Key-value pairs**: Use `Key: value` format with `|` separators for multiple items
- **Errors**: Start with "Error:" followed by a brief description

---

## Type Annotations

### General Rules

- All function parameters and return types must have annotations
- Use `-> None` for functions that don't return a value
- Use `| None` for optional types (not `Optional[T]`)
- Use lowercase `tuple`, `list`, `dict` (not `Tuple`, `List`, `Dict`)
- Avoid `any` type; use explicit union types instead

### NumPy Arrays

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.typing import NDArray

def process(data: NDArray[np.float32]) -> NDArray[np.float32]:
    ...
```

- Always specify dtype explicitly: `NDArray[np.float32]`, `NDArray[np.uint16]`, `NDArray[np.bool_]`
- Never use unparameterized `NDArray`
- Use `TYPE_CHECKING` block for `NDArray` to avoid runtime import overhead

### Class Attributes

```python
def __init__(self, height: int, width: int) -> None:
    self._field_shape: tuple[int, int] = (height, width)
```

---

## Naming Conventions

### Variables

Use **full words**, not abbreviations:

| Avoid             | Prefer                              |
|-------------------|-------------------------------------|
| `t`, `t_sq`       | `interpolation_factor`, `t_squared` |
| `coeff`, `coeffs` | `coefficient`, `coefficients`       |
| `pos`, `idx`      | `position`, `index`                 |
| `img`, `val`      | `image`, `value`                    |
| `num`, `dnum`     | `numerator`, `denominator`          |

### Functions

- Use descriptive verb phrases: `compute_coefficients`, `extract_features`
- Private functions start with underscore: `_process_batch`, `_validate_input`
- Avoid generic names like `process`, `handle`, `do_something`

### Constants

Module-level constants with type annotations and descriptive names:

```python
# Minimum number of samples required for statistical validity.
_MINIMUM_SAMPLE_COUNT: int = 100
```

---

## Function Calls

**Always use keyword arguments** for clarity:

```python
# Good
np.zeros((4,), dtype=np.float32)
compute_coefficients(interpolation_factor=t, output=result)
self._get_data(dimension=0)

# Avoid
np.zeros((4,), np.float32)
compute_coefficients(t, result)
self._get_data(0)
```

Exception: Single positional arguments for obvious cases like `range(4)`, `len(array)`.

---

## Error Handling

Use `console.error` from `ataraxis_base_utilities`:

```python
from ataraxis_base_utilities import console

def process_data(self, data: NDArray[np.float32], threshold: float) -> None:
    if not (0 < threshold <= 1):
        message = (
            f"Unable to process data with the given threshold. The threshold must be in range "
            f"(0, 1], but got {threshold}."
        )
        console.error(message=message, error=ValueError)
```

### Error Message Format

- Start with context: "Unable to [action] using [input]."
- Explain the constraint: "The [parameter] must be [constraint]"
- Show actual value: "but got {value}."
- Use f-strings for interpolation

---

## Ataraxis Library Preferences

Sun Lab projects use a suite of ataraxis libraries that provide standardized, high-performance utilities. **Always prefer
these libraries** over standard library alternatives or reimplementation for their designated tasks.

### Console Output (ataraxis-base-utilities)

Use `console.echo()` for **all console output** instead of `print()`:

```python
from ataraxis_base_utilities import console

# Good - use console.echo() for all output
console.echo(message="Processing frame 1 of 100...")
console.echo(message="Analysis complete.", level="SUCCESS")
console.echo(message="Potential memory issue detected.", level="WARNING")

# Avoid - do not use print()
print("Processing frame 1 of 100...")  # Wrong - use console.echo()
```

**Log levels**: `DEBUG`, `INFO` (default), `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`

The global `console` instance is pre-configured and shared across all Sun Lab projects. Call `console.enable()` at
application entry points if needed.

**Exception**: Use `print()` or `click.echo()` when output requires specific formatting that would be disrupted by
console's line-width formatting, such as tables created with `tabulate` or manually aligned ASCII tables:

```python
from tabulate import tabulate

# Good - print() for pre-formatted tabulate output
table = tabulate(data, headers=["Port", "Device", "Status"], tablefmt="grid")
print("Device Information:")
print(table)

# Good - click.echo() for manually aligned CLI tables
click.echo("Precision | Duration | Mean Time")
click.echo("----------+----------+----------")
for row in results:
    click.echo(f"{row.precision:9} | {row.duration:8} | {row.mean:9.3f}")
```

When using this exception, add a comment explaining why standard console output is not used (see
`sl-experiment/mesoscope_vr/zaber_bindings.py:164` for an example).

### List Conversion (ataraxis-base-utilities)

Use `ensure_list()` to normalize inputs to list form:

```python
from ataraxis_base_utilities import ensure_list

# Good - handles scalars, numpy arrays, and iterables
items = ensure_list(input_item=user_input)

# Avoid - manual type checking
if isinstance(user_input, list):
    items = user_input
elif isinstance(user_input, np.ndarray):
    items = user_input.tolist()
else:
    items = [user_input]
```

### Iterable Chunking (ataraxis-base-utilities)

Use `chunk_iterable()` for batching operations:

```python
from ataraxis_base_utilities import chunk_iterable

# Good - preserves numpy array types
for batch in chunk_iterable(iterable=large_array, chunk_size=100):
    process_batch(batch=batch)

# Avoid - manual slicing logic
for i in range(0, len(large_array), 100):
    batch = large_array[i:i + 100]
```

### Timing and Delays (ataraxis-time)

Use `PrecisionTimer` for all timing operations:

```python
from ataraxis_time import PrecisionTimer, TimerPrecisions

# Good - high-precision interval timing
timer = PrecisionTimer(precision=TimerPrecisions.MICROSECOND)
timer.reset()
# ... operation ...
elapsed_us = timer.elapsed

# Good - non-blocking delay (releases GIL for other threads)
timer.delay(delay=5000, allow_sleep=True, block=False)  # 5ms delay

# Avoid - time.sleep() for precision timing
import time
time.sleep(0.005)  # Wrong for microsecond precision work
```

**Precision options**: `NANOSECOND`, `MICROSECOND` (default), `MILLISECOND`, `SECOND`

### Timestamps (ataraxis-time)

Use `get_timestamp()` for generating timestamps:

```python
from ataraxis_time import get_timestamp, TimestampFormats

# Good - string format for filenames
timestamp = get_timestamp(output_format=TimestampFormats.STRING)
output_path = data_directory / f"session_{timestamp}.npy"

# Good - integer format for calculations (microseconds since epoch)
timestamp_us = get_timestamp(output_format=TimestampFormats.INTEGER)

# Good - bytes format for binary serialization
timestamp_bytes = get_timestamp(output_format=TimestampFormats.BYTES)

# Avoid - datetime manipulation
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")  # Wrong
```

### Time Unit Conversion (ataraxis-time)

Use `convert_time()` for converting between time units:

```python
from ataraxis_time import convert_time, TimeUnits

# Good - explicit unit conversion
duration_seconds = convert_time(
    time=elapsed_microseconds,
    from_units=TimeUnits.MICROSECOND,
    to_units=TimeUnits.SECOND,
)

# Avoid - manual conversion with magic numbers
duration_seconds = elapsed_microseconds / 1_000_000  # Wrong
```

**Supported units**: `NANOSECOND`, `MICROSECOND`, `MILLISECOND`, `SECOND`, `MINUTE`, `HOUR`, `DAY`

### YAML Configuration (ataraxis-data-structures)

Use `YamlConfig` as a base class for configuration dataclasses:

```python
from dataclasses import dataclass
from pathlib import Path
from ataraxis_data_structures import YamlConfig

# Good - subclass YamlConfig for YAML serialization
@dataclass
class ExperimentConfig(YamlConfig):
    """Defines experiment configuration parameters."""

    animal_id: str
    """The unique identifier for the animal."""
    session_duration: float
    """The duration in seconds."""

# Saving and loading
config = ExperimentConfig(animal_id="M001", session_duration=3600.0)
config.to_yaml(file_path=Path("config.yaml"))
loaded_config = ExperimentConfig.from_yaml(file_path=Path("config.yaml"))

# Avoid - manual YAML handling
import yaml
with open("config.yaml", "w") as file:
    yaml.dump(config.__dict__, file)  # Wrong
```

### Shared Memory (ataraxis-data-structures)

Use `SharedMemoryArray` for inter-process data sharing:

```python
from ataraxis_data_structures import SharedMemoryArray
import numpy as np

# Good - create shared array in main process
prototype = np.zeros((100, 100), dtype=np.float32)
shared_array = SharedMemoryArray.create_array(name="frame_buffer", prototype=prototype)

# In child process - connect before use
shared_array.connect()
with shared_array.array() as arr:  # Thread-safe access
    arr[:] = new_data
shared_array.disconnect()

# Cleanup in main process
shared_array.destroy()

# Avoid - multiprocessing.Array or manual shared memory
from multiprocessing import Array
shared = Array('f', 10000)  # Wrong for complex array operations
```

### Data Logging (ataraxis-data-structures)

Use `DataLogger` and `LogPackage` for high-throughput logging:

```python
from pathlib import Path
from ataraxis_data_structures import DataLogger, LogPackage
import numpy as np

# Good - dedicated logger process for parallel I/O
logger = DataLogger(
    output_directory=Path("/data/experiment"),
    instance_name="neural_data",
    thread_count=5,
)
logger.start()

# Package and submit data
package = LogPackage(
    source_id=np.uint8(1),
    acquisition_time=np.uint64(elapsed_us),
    serialized_data=data_array.tobytes(),
)
logger.input_queue.put(package)

# Cleanup
logger.stop()

# Avoid - direct file writes in acquisition loop
np.save(f"frame_{i}.npy", data)  # Wrong - blocks acquisition
```

### Quick Reference Table

| Task                    | Use This                    | Not This                                |
|-------------------------|-----------------------------|-----------------------------------------|
| Console output          | `console.echo()`            | `print()` (exception: formatted tables) |
| Error handling          | `console.error()`           | `raise Exception()`                     |
| Convert to list         | `ensure_list()`             | Manual type checking                    |
| Batch iteration         | `chunk_iterable()`          | Manual slicing                          |
| Precision timing        | `PrecisionTimer`            | `time.time()`, `time.perf_counter()`    |
| Delays                  | `PrecisionTimer.delay()`    | `time.sleep()`                          |
| Timestamps              | `get_timestamp()`           | `datetime.now().strftime()`             |
| Time unit conversion    | `convert_time()`            | Manual division/multiplication          |
| YAML serialization      | `YamlConfig` subclass       | `yaml.dump()`/`yaml.load()`             |
| Inter-process arrays    | `SharedMemoryArray`         | `multiprocessing.Array`                 |
| High-throughput logging | `DataLogger` + `LogPackage` | Direct file writes                      |

---

## Numba Functions

### Decorator Patterns

```python
# Standard cached function
@numba.njit(cache=True)
def _compute_values(...) -> None:
    ...

# Parallelized function
@numba.njit(cache=True, parallel=True)
def _process_batch(...) -> None:
    for i in prange(data.shape[0]):  # Parallel outer loop
        for j in range(data.shape[1]):  # Sequential inner loop
            ...

# Inlined helper (for small, frequently-called functions)
@numba.njit(cache=True, inline="always")
def compute_coefficients(...) -> None:
    ...
```

### Guidelines

- Always use `cache=True` for disk caching (avoids recompilation)
- Use `parallel=True` with `prange` only when no race conditions exist
- Use `inline="always"` for small helper functions called in hot loops
- Don't use `nogil` unless explicitly using threading
- Use Python type hints (not Numba signature strings) for readability

---

## Comments

### Inline Comments

- Use third person imperative ("Configures..." not "This section configures...")
- Place above the code, not at end of line (unless very short)
- Use comments to explain non-obvious logic or provide context

```python
# The constant 2.046392675 is the theoretical injectivity bound for 2D cubic B-splines.
limit = (1.0 / 2.046392675) * self._grid_sampling * factor

# Configures the speed axis, which only exists in RUN_TRAINING and experiment modes.
if self._speed_axis is not None:
    ...
```

### What to Avoid

- Don't reiterate the obvious (e.g., `# Set x to 5` before `x = 5`)
- Don't add docstrings/comments to code you didn't write or modify
- Don't add type annotations as comments (use actual type hints)
- Don't use heavy section separator blocks (e.g., `# ======` or `# ------`). Use blank lines to separate sections

---

## Imports

### Organization

```python
"""Module docstring."""

from typing import TYPE_CHECKING

import numba
from numba import prange
import numpy as np
from ataraxis_base_utilities import console

if TYPE_CHECKING:
    from numpy.typing import NDArray
```

Order:
1. Future imports (if any)
2. Standard library
3. `TYPE_CHECKING` import from typing
4. Third-party imports (alphabetical)
5. Local imports
6. `if TYPE_CHECKING:` block for type-only imports

---

## Class Design

### Constructor Parameters

Use explicit parameters instead of tuples/dicts:

```python
# Good
def __init__(self, field_height: int, field_width: int, sampling: float) -> None:
    self._field_shape: tuple[int, int] = (field_height, field_width)

# Avoid
def __init__(self, field_shape: tuple[int, int], sampling: float) -> None:
    self._field_shape = field_shape
```

### Properties vs Methods

- Use `@property` for simple attribute access that may involve computation
- Use methods for operations that clearly "do something" or take parameters

### Method Types

- **Instance methods** (no decorator): Use when the method accesses instance attributes (`self`)
- **`@staticmethod`**: Use when the method doesn't access instance or class attributes
- **`@classmethod`**: Use when the method needs access to class attributes but not instance attributes

### Visibility (Public vs Private)

- **Private** (`_` prefix): Use for anything internal to the class/module
- **Public** (no prefix): Use only for methods intended to be used from other modules

---

## Dataclass Conventions

Use dataclasses for grouping related data.

```python
from dataclasses import dataclass, field

# Immutable configuration - use frozen=True
@dataclass(frozen=True)
class ExperimentConfig:
    """Defines configuration parameters for an experiment session."""

    animal_id: str
    """The unique identifier for the animal."""
    session_duration: float
    """The duration of the session in seconds."""
    trial_count: int = 10
    """The number of trials to run. Defaults to 10."""


# Mutable state tracker - omit frozen=True
@dataclass
class ProcessingState:
    """Tracks the runtime state of a processing pipeline."""

    status: int = 0
    """The current processing status code."""
    completed_jobs: list[str] = field(default_factory=list)
    """The list of completed job identifiers."""

    def mark_complete(self, job_id: str) -> None:
        """Marks the specified job as complete."""
        self.completed_jobs.append(job_id)
```

### Guidelines

- Use `frozen=True` for configuration objects that should not be modified after creation
- Omit `frozen=True` for dataclasses that require mutation (state trackers, caches, builders)
- Use `field(default_factory=...)` for mutable default values (lists, dicts, sets)
- Use `field(repr=False)` for internal fields that should not appear in string representation
- Document each field with inline docstrings using triple-quoted strings

---

## I/O Separation

Separate I/O operations from processing logic. This makes code easier to test, maintain, and reuse.

```python
# Good - I/O separated from logic
def load_session_data(file_path: Path) -> NDArray[np.float32]:
    """Loads session data from file."""
    return np.load(file_path)

def analyze_session(data: NDArray[np.float32]) -> dict[str, float]:
    """Analyzes session data and returns statistics."""
    return {"mean": float(np.mean(data)), "std": float(np.std(data))}

# Avoid - I/O mixed with logic
def load_and_analyze(file_path: Path) -> dict[str, float]:
    """Loads and analyzes session data."""
    data = np.load(file_path)  # I/O operation
    return {"mean": float(np.mean(data))}  # Processing logic
```

### Guidelines

- I/O functions should only perform I/O (take filepath, return data)
- Processing functions should take standard data types and return standard data types
- This separation enables easier unit testing without file system dependencies

---

## Context Managers

Use context managers (`with` statements) for resource management.

```python
# Good - use context managers for file handling
with open(file_path, "r") as file:
    data = file.read()

# Good - multiple context managers (Python 3.10+)
with (
    open(input_path, "r") as input_file,
    open(output_path, "w") as output_file,
):
    output_file.write(input_file.read())

# Good - context manager for temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir) / "output.txt"
    process_data(output_path=temp_path)
```

### Guidelines

- Always use context managers for files, locks, database connections, and temporary resources
- Use parentheses for multiple context managers on separate lines
- Prefer context managers over try/finally for resource cleanup

---

## Comprehensions

Use comprehensions for simple transformations. Prefer explicit loops for complex logic.

```python
# Good - simple comprehension on one line
squares = [x ** 2 for x in range(10)]
valid_items = {key: value for key, value in data.items() if value > 0}

# Good - complex comprehension split across lines
filtered_data = [
    process_value(value)
    for value in raw_data
    if value > threshold
]

# Avoid - overly complex comprehension (use explicit loop instead)
# Bad: nested comprehensions with multiple conditions
result = [[x * y for x in row if x > 0] for row in matrix if sum(row) > threshold]

# Good - explicit loop for complex logic
result = []
for row in matrix:
    if sum(row) > threshold:
        processed_row = []
        for x in row:
            if x > 0:
                processed_row.append(x * y)
        result.append(processed_row)
```

---

## Blank Lines

Use blank lines to separate logical sections of code.

```python
"""Module docstring."""

from pathlib import Path

import numpy as np
from ataraxis_base_utilities import console


class FirstClass:
    """First class definition."""

    def method_one(self) -> None:
        """First method."""
        pass

    def method_two(self) -> None:
        """Second method."""
        pass


class SecondClass:
    """Second class definition."""

    pass
```

### Guidelines

- **Two blank lines** between top-level definitions (classes, functions)
- **One blank line** between method definitions within a class
- **No blank line** after a `def` line before the docstring
- **One blank line** after import blocks before code

---

## Pathlib Conventions

Use `pathlib.Path` for all path manipulation instead of string operations.

```python
from pathlib import Path

# Good - use pathlib for path manipulation
config_path = Path(base_directory) / "config" / "settings.yaml"
output_directory = Path(output_path).parent
file_stem = Path(file_path).stem
file_suffix = Path(file_path).suffix

# Good - check existence and create directories
if not output_directory.exists():
    output_directory.mkdir(parents=True)

# Good - iterate over files
for yaml_file in config_directory.glob("*.yaml"):
    process_config(file_path=yaml_file)

# Avoid - string concatenation for paths
config_path = base_directory + "/config/settings.yaml"
```

---

## Trailing Commas

Use trailing commas in multi-line structures to simplify diffs and reduce merge conflicts.

```python
# Good - trailing comma when elements on separate lines
config = {
    "animal_id": "M001",
    "session_duration": 3600.0,
    "trial_count": 10,
}

function_call(
    first_argument=value_one,
    second_argument=value_two,
    third_argument=value_three,
)

# Good - no trailing comma when on single line
config = {"animal_id": "M001", "session_duration": 3600.0}
result = function_call(first_argument=value_one, second_argument=value_two)
```

### Guidelines

- Always use trailing commas when the closing bracket is on a separate line
- Do not use trailing commas when everything is on one line
- Trailing commas make adding new items cleaner in version control diffs

---

## Line Length and Formatting

- Maximum line length: 120 characters
- Break long function calls across multiple lines:

```python
result = compute_transformation(
    input_data=self._data,
    parameters=self._get_parameters(dimension=dimension),
    weights=weights,
)
```

- Use parentheses for multi-line strings in error messages:

```python
message = (
    f"Unable to process the input data. The threshold must be in range "
    f"(0, 1], but got {threshold}."
)
```

- **F-string consistency**: When any line requires interpolation, use the `f` prefix on **all** lines:

```python
# Good - consistent f-prefix on all lines
message = (
    f"Unable to resolve the path to the credentials file, as the previously configured "
    f"file does not exist at the expected path ({credentials_path}). Set a new path "
    f"by using the 'sl-configure credentials' CLI command."
)
```

---

## Linting and Code Quality

### Running the Linter

Run `tox -e lint` after making changes. All issues must either be resolved or marked with proper `# noqa` ignore
statements.

### Resolution Policy

Prefer resolving issues unless the resolution would:
- Make the code unnecessarily complex
- Hurt performance by adding redundant checks
- Harm codebase readability instead of helping it

### Magic Numbers (PLR2004)

For magic number warnings, prefer defining constants:

```python
def calculate_threshold(self, value: float) -> float:
    """Calculates the adjusted threshold."""
    adjustment_factor = 1.5  # Empirically determined scaling factor.
    return value * adjustment_factor
```

### Using noqa

When suppressing a warning, always include the specific error code:

```python
if mode == 3:  # noqa: PLR2004 - LICK_TRAINING mode value from VisualizerMode enum.
    ...
```

---

## Test Files

Test files follow simplified documentation conventions.

### Module Docstrings

Test module docstrings use the "Contains tests for..." format:

```python
"""Contains tests for classes and methods provided by the saver.py module."""
```

### Test Function Docstrings

Test function docstrings use imperative mood with "Verifies...":

```python
def test_video_saver_init_repr(tmp_path, has_ffmpeg):
    """Verifies the functioning of the VideoSaver __init__() and __repr__() methods."""
```

**Important**: Test function docstrings do not include Args, Returns, or Raises sections.

### Fixture Docstrings

Pytest fixtures use imperative mood docstrings describing what the fixture provides:

```python
@pytest.fixture(scope="session")
def has_nvidia():
    """Checks for NVIDIA GPU availability in the test environment."""
    ...
```

---

## Input/Output Examples

Transform code to match Sun Lab style:

| Input (What you wrote)                 | Output (Correct style)                                         |
|----------------------------------------|----------------------------------------------------------------|
| `def calc(x):`                         | `def calculate_value(x: float) -> float:`                      |
| `pos = get_pos()`                      | `position = get_position()`                                    |
| `np.zeros((4,), np.float32)`           | `np.zeros((4,), dtype=np.float32)`                             |
| `# set x to 5`                         | Remove comment (self-explanatory code)                         |
| `data: NDArray`                        | `data: NDArray[np.float32]`                                    |
| `"""A class that processes data."""`   | `"""Processes experimental data."""`                           |
| `"""Whether to enable filtering."""`   | `"""Determines whether to enable filtering."""`                |
| `raise ValueError("Bad input")`        | `console.error(message="...", error=ValueError)`               |
| `print("Starting...")`                 | `console.echo(...)` (exception: tabulate/formatted tables)     |
| `time.sleep(0.005)`                    | `timer.delay(delay=5000)`  (microseconds)                      |
| `elapsed = time.time() - start`        | `elapsed = timer.elapsed` (use PrecisionTimer)                 |
| `datetime.now().strftime("%Y-%m-%d")`  | `get_timestamp(output_format=TimestampFormats.STRING)`         |
| `duration_s = duration_us / 1_000_000` | `convert_time(time=duration_us, from_units=..., to_units=...)` |
| `yaml.dump(config.__dict__, file)`     | `config.to_yaml(file_path=path)` (subclass YamlConfig)         |

---

## Anti-Patterns to Avoid

### Documentation Anti-Patterns

| Anti-Pattern                         | Problem                     | Solution                             |
|--------------------------------------|-----------------------------|--------------------------------------|
| `"""A class that processes data."""` | Noun phrase, not imperative | `"""Processes experimental data."""` |
| Bullet lists in docstrings           | Breaks prose flow           | Use complete sentences instead       |
| `# Set x to 5` before `x = 5`        | States the obvious          | Remove or explain *why*              |
| Missing dtype in `NDArray`           | Type checking fails         | Always specify `NDArray[np.float32]` |
| `Whether to...` for booleans         | Incomplete phrasing         | Use `Determines whether to...`       |
| `# ======` section separators        | Visual clutter              | Use blank lines to separate sections |

### Naming Anti-Patterns

| Anti-Pattern        | Problem              | Solution                           |
|---------------------|----------------------|------------------------------------|
| `pos`, `idx`, `val` | Abbreviations        | `position`, `index`, `value`       |
| `curIdx`            | Missing underscore   | `_current_index`                   |
| `process()`         | Too generic          | `process_frame_data()`             |
| `data1`, `data2`    | Non-descriptive      | `input_data`, `output_data`        |

### Code Anti-Patterns

| Anti-Pattern                         | Problem                  | Solution                                      |
|--------------------------------------|--------------------------|-----------------------------------------------|
| `np.zeros((4,), np.float32)`         | Positional dtype arg     | `np.zeros((4,), dtype=np.float32)`            |
| `raise ValueError(...)`              | Wrong error handling     | `console.error(message=..., error=ValueError)`|
| `from typing import Optional`        | Old-style optional       | Use `Type | None` instead                     |
| `@numba.njit` without `cache=True`   | Recompiles every run     | `@numba.njit(cache=True)`                     |
| Inconsistent f-string prefixes       | Confusing multi-line     | Use `f` prefix on all lines                   |

### Ataraxis Library Anti-Patterns

| Anti-Pattern                         | Problem                         | Solution                                                             |
|--------------------------------------|---------------------------------|----------------------------------------------------------------------|
| `print("message")` for plain text    | No logging, inconsistent        | `console.echo(message="...")` (exception: tabulate/formatted tables) |
| `time.sleep(0.001)`                  | Low precision, blocks GIL       | `PrecisionTimer.delay(delay=1000)`                                   |
| `time.time()` for intervals          | Insufficient precision          | `PrecisionTimer.elapsed`                                             |
| `datetime.now().strftime(...)`       | Inconsistent format             | `get_timestamp()`                                                    |
| `elapsed_us / 1_000_000`             | Magic number conversion         | `convert_time(time=..., from_units=..., to_units=...)`               |
| Manual YAML dump/load                | No type safety                  | Subclass `YamlConfig`                                                |
| `multiprocessing.Array`              | Limited dtype support           | `SharedMemoryArray`                                                  |
| Direct file writes in loops          | Blocks acquisition              | `DataLogger` with `LogPackage`                                       |
| Manual `isinstance()` for list check | Verbose, error-prone            | `ensure_list()`                                                      |
| Manual slice batching                | Verbose, doesn't preserve dtype | `chunk_iterable()`                                                   |

---

## Verification Checklist

**You MUST verify your edits against this checklist before submitting any changes to Python files.**

```
Python Style Compliance:
- [ ] Google-style docstrings on all public and private members
- [ ] Docstring section order: Summary → Extended Description → Notes → Args → Returns → Raises
- [ ] No Examples sections or in-code examples in docstrings
- [ ] Imperative mood in summaries ("Processes..." not "This method processes...")
- [ ] Prose used instead of bullet lists in docstrings
- [ ] All parameters and returns have type annotations
- [ ] NumPy arrays specify dtype explicitly (NDArray[np.float32])
- [ ] Full words used (no abbreviations like `pos`, `idx`, `val`)
- [ ] Private members use `_underscore` prefix
- [ ] Keyword arguments used for function calls
- [ ] Error handling uses console.error() from ataraxis_base_utilities
- [ ] Lines under 120 characters
- [ ] Imports ordered: standard library, TYPE_CHECKING, third-party, local
- [ ] Inline comments use third person imperative
- [ ] No heavy section separator blocks (# ====== or # ------)
- [ ] Numba functions use cache=True
- [ ] Dataclasses use frozen=True for immutable configs (omit for mutable state)
- [ ] I/O operations separated from processing logic
- [ ] Context managers used for resource management
- [ ] Pathlib used for path manipulation (not string concatenation)
- [ ] Two blank lines between top-level definitions
- [ ] Trailing commas in multi-line structures

Ataraxis Library Preferences:
- [ ] Console output uses console.echo() instead of print() (exception: tabulate/formatted tables)
- [ ] Error handling uses console.error() instead of raise
- [ ] List conversion uses ensure_list() instead of manual type checks
- [ ] Batch iteration uses chunk_iterable() instead of manual slicing
- [ ] Precision timing uses PrecisionTimer instead of time.time()/perf_counter()
- [ ] Delays use PrecisionTimer.delay() instead of time.sleep()
- [ ] Timestamps use get_timestamp() instead of datetime.strftime()
- [ ] Time unit conversion uses convert_time() instead of manual math
- [ ] YAML-serializable configs subclass YamlConfig
- [ ] Inter-process arrays use SharedMemoryArray instead of multiprocessing.Array
- [ ] High-throughput logging uses DataLogger/LogPackage instead of direct writes
```
