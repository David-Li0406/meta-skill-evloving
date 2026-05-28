---
name: deploy-website
description: Use this skill to deploy and serve various web projects locally for preview, automatically detecting the project type and starting the appropriate development server.
---

# Skill body

## Arguments

- **workspace**: Absolute path to the workspace directory to deploy (required: false)

## Detection Logic

1. **Node.js web project**
   - Look for `package.json` in the workspace root.
   - Check if it contains a `dev` or `start` script.
   - Execute `npm run dev` (or `npm start` if `dev` is not available).

2. **Static website**
   - Look for `.html` files in the workspace (especially `index.html`).
   - Execute `python3 -m http.server 8000` to serve static files.

3. **PHP projects**
   - Look for `.php` files or `composer.json`.
   - Execute `php -S localhost:8000` to serve PHP files.
   - If `public/index.php` exists, serve from the `public` directory.

4. **Python projects**
   - **Django**: Look for `manage.py` and `settings.py`.
     - Execute `python manage.py runserver 8000`.
   - **Flask**: Look for `app.py` or `wsgi.py`.
     - Execute `python app.py` or `flask run --port=8000`.
   - **Unicorn/uWSGI**: Look for `gunicorn.conf.py` or `uwsgi.ini`.
     - Execute `gunicorn -b 0.0.0.0:8000 app:app` (adjust module name).
   - **Generic**: Look for `requirements.txt` or `pyproject.toml`.
     - Execute `python -m http.server 8000`.

5. **Go projects**
   - Look for `go.mod`.
   - Execute `go run main.go` or `go run .` (usually handles its own server).

6. **Ruby/Rails**
   - Look for `Gemfile` with `rails`.
   - Execute `rails server -p 8000` or `bundle exec rails server -p 8000`.

7. **Java/Spring Boot**
   - Look for `pom.xml` (Maven) or `build.gradle` (Gradle).
   - Execute `mvn spring-boot:run` or `./gradlew bootRun`.

8. **Rust/Axum/Actix**
   - Look for `Cargo.toml`.
   - Execute `cargo run`.

9. **README-based detection**
   - If standard detection fails, search README files (`README.md`, `README.rst`, `README.txt`, `doc/README.md`).
   - Look for keywords like `run`, `start`, `serve`, `dev`, `preview`.
   - Extract and execute the suggested command.

## Workflow

1. Detect the project type based on the above logic.
2. Start the appropriate development server in the background.
3. Optionally, request a Preview URL with the MCP Tool `request_preview`.

## Notes

- The server will run in the background or as a subagent task.
- Default port for static server is 8000.
- For Node.js projects, the port depends on the project configuration.
- Make sure dependencies are installed (`npm install`) before running Node.js projects.