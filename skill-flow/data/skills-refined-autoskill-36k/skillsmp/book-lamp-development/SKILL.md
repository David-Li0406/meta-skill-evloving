---
name: book-lamp-development
description: Guidelines and workflows for developing the Book Lamp application, focusing on the Google Sheets adapter pattern and project philosophy.
---

# Book Lamp Development Skill

This skill provides comprehensive guidelines for developing, maintaining, and extending the Book Lamp application.

## Core Philosophy

Following the **Python Architecture Tutor** principles, we prioritise clarity, readability, and explicit structure:

### 1. Layered Architecture (Separation of Concerns)
The project is structured into distinct layers to separate business logic from external side effects:
- **Models/Entities**: Pure data structures (e.g., book dictionaries with defined keys).
- **Adapters (Persistence)**: Isolated in `book_lamp/services/`. `GoogleSheetsStorage` is our primary adapter for Google Sheets.
- **Service Layer**: Pure logic that sits between entry points and adapters (e.g., `book_lookup.py`).
- **Entry Points**: Flask routes in `app.py` and CLI commands.

### 2. Pure vs. Effectful Separation
- **Pure Code**: Logic should be deterministic. It should not perform I/O or rely on system time directly.
- **Effectful Code**: All I/O (Google Sheets API, network, filesystem, time) must be isolated at the edges in adapter classes or functions.
- **Dependency Injection**: Inject adapters into logic or entry points to keep them decoupled.

### 3. Mentorship & Readability
- **Explicit over Implicit**: Avoid "magic". Prefer clear connections between components.
- **British English**: All comments, documentation, and naming (where possible) MUST use British English (e.g., `serialise`, `colour`, `optimise`).
- **Standard Library**: Prefer modern Python standards (e.g., `datetime.now(timezone.utc)`, `pathlib`).

### 4. Frontend Architecture
- **Separation of Concerns**: CSS and JavaScript must be kept in dedicated files in `book_lamp/static/`.
- **CSS**: Avoid inline styles or `<style>` blocks in HTML templates. Use descriptive filenames (e.g., `base.css`, `books.css`).
- **HTML**: Keep templates focused on structure and Jinja2 logic.

## Documentation Standard
- **Docstrings**: Use **Google Style** docstrings for all public functions and classes.
- **Template**:
  ```python
  def function_name(param1: str) -> bool:
      """Short summary of the function.

      Detailed description if necessary.

      Args:
          param1: Description of param1.

      Returns:
          Description of the return value.
      """
  ```

## Working with Google Sheets Storage

The `GoogleSheetsStorage` class in `book_lamp/services/sheets_storage.py` is the primary adapter for data.

### Sheet Structure
- **Books**: `id`, `isbn13`, `title`, `author`, `publication_year`, `thumbnail_url`, `created_at`
- **ReadingRecords**: `id`, `book_id`, `status`, `start_date`, `end_date`, `rating`, `created_at`

### Dynamic Management
- On first run or if a token is present, the app creates a folder hierarchy `AppData/BookLamp` in the user's Google Drive.
- It creates/uses a spreadsheet based on the environment:
  - **Production**: `BookLampData`
  - **Development**: `DevBookLampData`

### Extending the Schema
1.  Update the `initialize_sheets` method to include new headers.
2.  Update the range in `get_all_books` or `get_reading_records`.
3.  Update the mapping logic in the getter and adder methods.
4.  Always use 1-based indexing for row deletions and updates as required by the Google Sheets API.

### Handling IDs
- IDs are managed manually by finding the maximum value in the first column of a tab and incrementing it.
- Always check for empty sheets or sheets with only headers.

## Testing Strategy

### Unit Tests
- Test pure logic with table-driven tests.
- Mock the `GoogleSheetsStorage` or use the `MOCK_STORAGE` pattern if available.
- Place unit tests in the `tests/` directory.

### E2E Tests (Playwright)
- E2E tests are located in `tests-e2e/`.
- Use `npm test` to run the suite.
- The app should automatically handle `TEST_MODE` to avoid hitting real Google APIs during testing.

## Security and Configuration

### OAuth and Authentication
- The application uses **Google OAuth2** for authentication.
- Users must authorize the application to access their Google Drive and Sheets.
- The `token.json` file stores the OAuth2 tokens.

### Secrets and Sanitization
- Never commit `credentials.json`, `token.json`, or `.env` files.
- **Required Environment Variables**:
  - `SECRET_KEY`: For Flask session management.
  - `GOOGLE_CLIENT_ID`: Google Cloud Client ID.
  - `GOOGLE_CLIENT_SECRET`: Google Cloud Client Secret.
- **Input Sanitization**: Always strip and normalize user input (ISBNs, titles) before processing or storing.

## Debugging and Diagnostics

### Common Google Sheets Errors
- **403 Forbidden**: Check if the OAuth user has given the app permission to access Google Drive and Sheets.
- **401 Unauthorized**: Ensure the user has authorized the app via the `/login` route.
- **Initialization Error**: If the app cannot create the folder hierarchy, check Drive permissions.
- **Invalid Credentials**: Delete `token.json` and re-run the login flow via the web interface.

### Logs
- Application logs are configured with standard formatting. Check terminal output for OAuth flow logs and API interactions.

## Environment Setup
1.  **Dependencies**: Run `mise install` followed by `poetry install`.
2.  **Configuration**: Copy `.env.example` to `.env` and fill in `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
3.  **Authentication**: Start the app and visit `/login` to authorize Google access.
4.  **Initialization**: The app automatically creates the necessary folders and spreadsheets on first use. You can also run `poetry run flask --app book_lamp.app init-sheets` to prepare it manually.
5.  **Local Run**: `poetry run flask --app book_lamp.app run --debug`.

## Commits and Change Discipline
- Use **Semantic Commits** (e.g., `feat:`, `fix:`, `refactor:`, `docs:`).
- Subject line: Max 50 characters.
- Body lines: Max 72 characters.
- Make small, cohesive edits. Verify each step with tests.

## Tooling
- **Tool Manager**: `mise` (manages Python, Node, and Poetry versions)
- **Python**: 3.13.x
- **Dependency Manager**: Poetry (`poetry install`, `poetry run`)
- **Formatters**: `black`, `isort`
- **Linters**: `ruff`, `mypy` (strict mode)
