---
name: Refactoring Protocol
description: Safe, systematic approach to code refactoring with verification and rollback strategy.
---

# Refactoring Protocol

This skill enforces disciplined refactoring practices to improve code quality without breaking functionality.

## The Prime Directive

**"Working Code is Sacred"**
*   NEVER refactor without tests verifying current behavior
*   NEVER refactor and add features simultaneously
*   NEVER proceed if tests fail after refactoring
*   If stuck, REVERT IMMEDIATELY (do not stack fixes on broken code)

## Phase 1: Assessment & Planning

### Step 1.1: Identify Refactoring Need
Common triggers:
*   **God Object**: File > 600 lines
*   **Duplicate Code**: Same logic in multiple places
*   **Architectural Violation**: SQL in UI, business logic in repository, etc.
*   **Poor Naming**: Unclear variable/method names
*   **Deep Nesting**: If/else/for blocks > 3 levels deep
*   **Long Methods**: Functions > 50 lines
*   **Feature Envy**: Class A uses Class B's data more than its own

### Step 1.2: Capture Current Behavior
*   **Run Existing Tests**: Ensure all tests pass BEFORE starting
    ```bash
    python tools/run_tests.py
    ```
*   **Document Current Behavior**: If no tests exist, write them first
*   **Create Reproduction Script** if needed (for complex scenarios)

### Step 1.3: Plan the Refactoring
*   **Define the Goal**: What will be better after refactoring?
*   **Identify Risk Areas**: What could break?
*   **Plan Small Steps**: Break into incremental changes
*   **Present Plan to User**: Get approval before starting

## Phase 2: Execution (The Refactoring Steps)

### General Principles
*   **One Change at a Time**: Rename OR extract OR move, not all three
*   **Keep Tests Green**: Run tests after each step
*   **Commit Each Step**: Small, atomic commits (though user controls when)

### Common Refactoring Patterns

#### Pattern A: Extract Method
**When**: Method > 50 lines or does multiple things

**Steps**:
1. Identify block of code to extract
2. Determine required parameters and return value
3. Create new method with descriptive name
4. Move code to new method
5. Replace original code with method call
6. Run tests

**Example**:
```python
# BEFORE
def process_song(self, file_path: str):
    # 20 lines of file validation
    if not os.path.exists(file_path):
        raise FileNotFoundError(...)
    if not file_path.endswith('.mp3'):
        raise ValueError(...)
    # ... more validation

    # 30 lines of metadata extraction
    audio = MP3(file_path)
    title = audio.get('TIT2')
    # ... more extraction

# AFTER
def process_song(self, file_path: str):
    self._validate_file(file_path)
    metadata = self._extract_metadata(file_path)
    # ...

def _validate_file(self, file_path: str):
    # Validation logic here

def _extract_metadata(self, file_path: str) -> dict:
    # Extraction logic here
```

#### Pattern B: Extract Class
**When**: Class > 600 lines or has multiple responsibilities

**Steps**:
1. Identify cohesive group of methods/attributes
2. Create new class
3. Move methods/attributes to new class
4. Update original class to delegate to new class
5. Update all references
6. Run tests

**Example**:
```python
# BEFORE
class LibraryWidget:  # 800 lines
    def filter_by_artist(self): ...
    def filter_by_genre(self): ...
    def apply_complex_filter(self): ...
    # ... 20 more filter methods
    # ... plus 30 other widget methods

# AFTER
class LibraryWidget:  # 400 lines
    def __init__(self):
        self._filter_manager = FilterManager()

    def apply_filter(self, filter_spec):
        self._filter_manager.apply(filter_spec)

class FilterManager:  # New class, 300 lines
    def filter_by_artist(self): ...
    def filter_by_genre(self): ...
    def apply_complex_filter(self): ...
```

#### Pattern C: Move Method (Layer Correction)
**When**: Method is in wrong architectural layer

**Steps**:
1. Create method in correct layer
2. Update original method to delegate (temporarily)
3. Update all callers to use new location
4. Delete old method
5. Run tests

**Example**:
```python
# BEFORE - SQL in UI layer (VIOLATION)
class LibraryWidget:
    def load_songs(self):
        cursor.execute("SELECT * FROM songs")  # WRONG LAYER!

# AFTER - SQL in Repository
class SongRepository:
    def get_all(self) -> List[Song]:
        cursor.execute("SELECT * FROM songs")  # CORRECT LAYER
        return [self._row_to_song(row) for row in cursor.fetchall()]

class LibraryService:
    def get_all_songs(self) -> List[Song]:
        return self._song_repo.get_all()

class LibraryWidget:
    def load_songs(self):
        songs = self._library_service.get_all_songs()  # CORRECT
```

#### Pattern D: Rename (Clarity Improvement)
**When**: Names are unclear or misleading

**Steps**:
1. Use IDE's rename refactoring OR grep to find all usages
2. Rename in all locations
3. Run tests
4. Update related documentation

**Example**:
```python
# BEFORE
def proc(self, d):  # Unclear
    return d.get('val')

# AFTER
def extract_title(self, metadata: dict) -> str:  # Clear
    return metadata.get('title')
```

#### Pattern E: Introduce Parameter Object
**When**: Function has > 4 parameters

**Steps**:
1. Create dataclass for parameters
2. Update function signature
3. Update all call sites
4. Run tests

**Example**:
```python
# BEFORE
def create_song(self, title, artist, year, genre, bpm, isrc):
    pass

# AFTER
@dataclass
class SongCreationData:
    title: str
    artist: str
    year: Optional[int] = None
    genre: Optional[str] = None
    bpm: Optional[int] = None
    isrc: Optional[str] = None

def create_song(self, data: SongCreationData):
    pass
```

## Phase 3: Verification

### Step 3.1: Test Suite Validation
```bash
# Run full test suite
python tools/run_tests.py

# If any tests fail:
# 1. DO NOT PROCEED
# 2. Analyze failure
# 3. If it's a test issue, fix test
# 4. If it's a refactoring issue, REVERT
```

### Step 3.2: Manual Smoke Testing
*   **Test Main Workflows**: Import song, play song, edit metadata, etc.
*   **Test Edge Cases**: Empty library, invalid files, cancellations
*   **Visual Inspection**: UI looks correct, no layout issues

### Step 3.3: Performance Check
*   **Compare Before/After**: Did refactoring affect performance?
*   **Profile Hot Paths**: Use cProfile if concerned
*   **If Slower**: Consider optimizing or reverting

## Phase 4: The Hard Revert Rule

### When to Revert
*   Tests fail and root cause is unclear
*   Refactoring is taking too long (> 1 hour)
*   Discovering unexpected dependencies
*   User requests to stop

### How to Revert
```bash
# Discard all changes
git checkout .

# Or revert specific file
git checkout -- path/to/file.py
```

### After Reverting
*   **Analyze What Went Wrong**: Why did it fail?
*   **Plan Smaller Steps**: Break into even smaller increments
*   **Ask User**: Should we try a different approach?

## Phase 5: Completion

### Step 5.1: Documentation Updates
*   Update comments if method signatures changed
*   Update ARCHITECTURE.md if patterns changed
*   Update docstrings if behavior clarified

### Step 5.2: Checkpoint Reminder
*   **Remind User to Commit**:
    > "Refactoring complete and verified. Tests pass. Please commit when ready."
*   **Suggest Commit Message**:
    ```
    refactor(domain): Brief description

    - Extract FilterManager from LibraryWidget (800 -> 400 lines)
    - Move SQL queries from UI to SongRepository
    - No functional changes

    Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
    ```

## Refactoring Safety Checklist

Before starting:
*   ✅ All tests pass
*   ✅ User approves refactoring plan
*   ✅ Architectural goal is clear

During refactoring:
*   ✅ Making one type of change at a time
*   ✅ Tests pass after each step
*   ✅ Not adding features simultaneously

After completion:
*   ✅ All tests still pass
*   ✅ No new warnings or errors
*   ✅ Code is clearer/cleaner than before
*   ✅ No performance regression

## Common Refactoring Anti-Patterns

### ❌ Big Bang Refactoring
Don't refactor entire codebase at once. Small, incremental changes.

### ❌ Refactoring Without Tests
Always have tests verifying current behavior first.

### ❌ Refactoring + Feature Addition
Never mix refactoring with new functionality. Refactor first, then add feature.

### ❌ Premature Abstraction
Don't create abstractions until you have 3+ similar cases.

### ❌ Ignoring Test Failures
If tests fail, STOP. Don't continue with "I'll fix it later."

### ❌ Silent Behavior Changes
Refactoring should NOT change behavior. If it does, it's not refactoring.

## Example Walkthrough

**Scenario**: `LibraryService` is 850 lines and growing

**Phase 1: Assessment**
1. Identify: God Object (> 600 lines)
2. Current behavior: All tests pass
3. Plan: Extract playlist-related methods to `PlaylistService`

**Phase 2: Execution**
1. Create `src/business/services/playlist_service.py`
2. Move `create_playlist()` method → Test
3. Move `add_to_playlist()` method → Test
4. Move `remove_from_playlist()` method → Test
5. Update `LibraryService` to delegate to `PlaylistService`
6. Update all UI callers

**Phase 3: Verification**
1. Run full test suite → All pass
2. Manual test: Create playlist, add songs → Works
3. Check file sizes: `LibraryService` now 620 lines, `PlaylistService` 180 lines

**Phase 4: Completion**
1. Remind user to commit
2. Suggest: "refactor(services): Extract PlaylistService from LibraryService"
