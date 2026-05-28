---
name: Feature Implementation Workflow
description: Structured workflow for implementing new features with planning, verification, and documentation.
---

# Feature Implementation Workflow
**NOTE: All operational logic is now governed by the GSD (Get Shit Done) Protocol in `rules/operating_directives.md`.**

This skill provides a systematic approach to implementing new features in Gosling2, ensuring architectural compliance and quality.

## Phase 1: Discovery & Planning

### Step 1.1: Understand Requirements
*   **Read the Request**: Carefully parse what the user wants
*   **Ask Clarifying Questions**: Use the AskUserQuestion tool if:
    *   Multiple valid approaches exist
    *   Requirements are ambiguous
    *   User preferences matter (UI placement, behavior, etc.)
*   **Document Assumptions**: State any assumptions you're making

### Step 1.2: Survey the Codebase
*   **Find Related Code**: Search for similar features
    ```
    - Grep for relevant class names
    - Glob for similar widgets/services
    - Read related files to understand patterns
    ```
*   **Identify Affected Layers**:
    *   UI Layer: Which widgets need changes?
    *   Service Layer: Which services need new methods?
    *   Data Layer: Which repositories/models need updates?
*   **Check for God Objects**: If any file > 600 lines needs changes, plan to refactor first

### Step 1.3: Design the Solution
*   **Blueprint the Approach**: Write a plain English plan:
    1. What models/dataclasses are needed?
    2. What repository methods are needed?
    3. What service methods orchestrate the logic?
    4. What UI components need to be created/modified?
    5. What signals/slots connect everything?
*   **Verify Architecture Compliance**:
    *   NO SQL in UI or Service layers
    *   NO business logic in Repositories
    *   NO widget references in Services
    *   Use GlowFactory components, not raw PyQt6 widgets
*   **Present Plan to User**: Wait for approval if changes are significant

## Phase 2: Implementation

### Step 2.1: Data Layer First
*   **Create/Update Models** (`src/data/models/`):
    ```python
    @dataclass
    class MyNewEntity:
        id: int
        name: str
        # ... fields
    ```
*   **Create/Update Repositories** (`src/data/repositories/`):
    ```python
    class MyEntityRepository:
        def get_by_id(self, id: int) -> Optional[MyNewEntity]:
            # SQL query here
        def insert(self, entity: MyNewEntity) -> int:
            # INSERT query
    ```
*   **Test Immediately**: Write unit tests for repository methods

### Step 2.2: Service Layer Second
*   **Create/Update Service** (`src/business/services/`):
    ```python
    class MyFeatureService(QObject):
        # Define signals
        entity_added = pyqtSignal(int)

        def __init__(self, repo: MyEntityRepository):
            super().__init__()
            self._repo = repo

        def add_entity(self, data: MyEntityData) -> int:
            # Validate
            # Call repository
            # Emit signal
            entity_id = self._repo.insert(entity)
            self.entity_added.emit(entity_id)
            return entity_id
    ```
*   **Test Immediately**: Mock repository, test business logic

### Step 2.3: UI Layer Last
*   **Create Glow Components** if needed (`src/presentation/widgets/glow/`):
    ```python
    from .base import GlowWidget

    class GlowMyNewWidget(GlowWidget):
        def __init__(self):
            super().__init__()
            self._init_ui()
            self._connect_signals()
    ```
*   **Create/Update Main Widget** (`src/presentation/widgets/`):
    ```python
    class MyFeatureWidget(QWidget):
        def __init__(self, service: MyFeatureService):
            super().__init__()
            self._service = service
            self._init_ui()
            self._connect_signals()

        def _connect_signals(self):
            self._service.entity_added.connect(self._on_entity_added)
    ```
*   **Style with theme.qss**: Use objectName, NO inline styles
*   **Test UI Components**: Use pytest-qt with qtbot

### Step 2.4: Integration
*   **Wire Up in MainWindow**:
    *   Instantiate service
    *   Pass service to widget
    *   Connect any cross-widget signals
*   **Update Menu/Toolbar** if needed

## Phase 3: Verification

### Step 3.1: Manual Testing
*   **Test Happy Path**: Does the feature work as expected?
*   **Test Edge Cases**:
    *   Empty inputs
    *   Invalid data
    *   Cancellation
    *   Rapid repeated actions
*   **Test UI Responsiveness**: No freezing on long operations

### Step 3.2: Automated Testing
*   **Run All Tests**:
    ```bash
    python tools/run_tests.py
    ```
*   **Check Coverage**: New code should have tests
*   **Fix Any Regressions**: If existing tests fail, fix before proceeding

### Step 3.3: Code Review Checklist
*   ✅ Follows 3-tier architecture (UI → Service → Repository)
*   ✅ No SQL in UI or Service layers
*   ✅ Uses GlowFactory components
*   ✅ All user-facing text follows "Night Shift DJ" rule
*   ✅ No files exceed 600 lines
*   ✅ All methods have type hints
*   ✅ Error handling is specific, not bare except
*   ✅ No magic numbers (extracted to constants)

## Phase 4: Documentation & Completion

### Step 4.1: Update Documentation
*   **User-Facing Changes**: Update README.md if needed
*   **Architecture Changes**: Update ARCHITECTURE.md if new patterns introduced
*   **Field Registry**: Update if new database fields added

### Step 4.2: Checkpoint Reminder
*   **Remind User to Commit**:
    > "Feature is complete and verified. Please commit your changes when ready."
*   **Suggest Commit Message** (but don't commit automatically):
    ```
    feat(domain): Brief description

    - Implementation detail 1
    - Implementation detail 2

    Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
    ```

### Step 4.3: Field Notes
*   **Report Any Issues Found**: If you found unrelated bugs/messy code during implementation:
    > **Field Notes**:
    > - Found unused import in `old_file.py:45`
    > - `SomeWidget` exceeds 600 lines, should be refactored
    > - Hardcoded color in `other_widget.py:123`

## Anti-Patterns to Avoid

### ❌ Don't Start Coding Immediately
Always plan first, get user approval for significant changes

### ❌ Don't Mix Concerns
Don't add business logic while fixing UI bugs

### ❌ Don't Skip Tests
Tests verify correctness and prevent regressions

### ❌ Don't Auto-Commit
Always let user commit manually

### ❌ Don't Refactor Without Asking
If you find messy code, log in Field Notes, don't silently fix

## Example Walkthrough

**User Request**: "Add ability to tag songs with custom labels"

**Phase 1: Planning**
1. Ask: "Should labels be global or per-song? Can a song have multiple labels?"
2. Survey: Check if tagging system exists, find similar features
3. Design:
   - Data: Create `Tag` model, `TagRepository`
   - Service: Add `TagService` with CRUD operations
   - UI: Create `TagWidget` for display, `TagEditor` dialog for editing
4. Present plan, wait for approval

**Phase 2: Implementation**
1. Create `src/data/models/tag.py`
2. Create `src/data/repositories/tag_repository.py`
3. Write tests for repository
4. Create `src/business/services/tag_service.py`
5. Write tests for service
6. Create `src/presentation/widgets/tag_widget.py` using GlowFactory
7. Integrate in MainWindow

**Phase 3: Verification**
1. Test manually: Add tags, edit tags, delete tags
2. Run pytest: All tests pass
3. Review code: Follows all architectural rules

**Phase 4: Completion**
1. Update README if needed
2. Remind user to commit
3. Report any issues found in Field Notes
