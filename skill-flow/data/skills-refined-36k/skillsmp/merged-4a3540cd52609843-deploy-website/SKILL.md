---
name: deploy-website
description: Deploy and serve various web projects locally for preview, automatically detecting the project type and starting the appropriate development server.
---

# Deploy Website

Automatically detect the project type and start the appropriate development server **in the background**, then request a Preview URL.

## Detection Logic

1. **Node.js web project**
   - Look for `package.json` in the workspace root
   - Check if it contains a `dev` or `start` script
   - Execute `npm run dev` (or `npm start` if `dev` is not available)

2. **Static website**
   - Look for `.html` files in the workspace (especially `index.html`)
   - Execute `python3 -m http.server 8000` to serve static files

3. **PHP projects**
   - Look for `.php` files or `composer.json`
   - Execute `php -S localhost:8000` to serve PHP files
   - If `public/index.php` exists, serve from `public` directory

4. **Python projects**
   - **Django**: Look for `manage.py` and `settings.py`, execute `python manage.py runserver 8000`
   - **Flask**: Look for `app.py` or `wsgi.py`, execute `python app.py` or `flask run --port=8000`
   - **Unicorn/uWSGI**: Look for `gunicorn.conf.py` or `uwsgi.ini`, execute `gunicorn -b 0.0.0.0:8000 app:app`
   - **Generic**: Look for `requirements.txt` or `pyproject.toml`, execute `python -m http.server 8000`

5. **Go projects**
   - Look for `go.mod`, execute `go run main.go` or `go run .`

6. **Ruby/Rails projects**
   - Look for `Gemfile` with `rails`, execute `rails server -p 8000` or `bundle exec rails server -p 8000`

7. **Java/Spring Boot projects**
   - Look for `pom.xml` (Maven) or `build.gradle` (Gradle), execute `mvn spring-boot:run` or `./gradlew bootRun`

8. **Rust projects**
   - Look for `Cargo.toml`, execute `cargo run`

9. **README-based detection**
   - If standard detection fails, search README files for keywords like `run`, `start`, `serve`, `dev`, `preview`, and execute the suggested command.

## Workflow

1. Detect the project type and start the appropriate server in the background:

```bash
# Step 1: Node.js project
if [ -f "package.json" ]; then
    npm install  # Ensure dependencies are installed
    if grep -q '"dev"' package.json; then
        npm run dev
    elif grep -q '"start"' package.json; then
        npm start
    fi

# Step 2: PHP project
elif [ -f "composer.json" ] || ls *.php 1> /dev/null 2>&1; then
    if [ -f "public/index.php" ]; then
        php -S localhost:8000 -t public
    else
        php -S localhost:8000
    fi

# Step 3: Python projects
elif [ -f "manage.py" ]; then
    # Django
    python manage.py runserver 8000
elif [ -f "app.py" ] || [ -f "wsgi.py" ]; then
    # Flask or WSGI app
    if command -v flask &> /dev/null; then
        flask run --port=8000
    else
        python app.py || python wsgi.py
    fi
elif [ -f "gunicorn.conf.py" ] || [ -f "uwsgi.ini" ]; then
    # Unicorn/uWSGI
    gunicorn -b 0.0.0.0:8000 app:app
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    python -m http.server 8000

# Step 4: Go project
elif [ -f "go.mod" ]; then
    go run . || go run main.go

# Step 5: Ruby/Rails project
elif [ -f "Gemfile" ] && grep -q "rails" Gemfile; then
    bundle exec rails server -p 8000 || rails server -p 8000

# Step 6: Java/Spring Boot
elif [ -f "pom.xml" ]; then
    ./mvnw spring-boot:run || mvn spring-boot:run
elif [ -f "build.gradle" ]; then
    ./gradlew bootRun || gradle bootRun

# Step 7: Rust project
elif [ -f "Cargo.toml" ]; then
    cargo run

# Step 8: Static HTML files
elif [ -f "index.html" ] || ls *.html 1> /dev/null 2>&1; then
    python3 -m http.server 8000

# Step 9: README-based detection
else
    # Search README for startup commands
    README_FILE=$(find . -maxdepth 2 -iname "README*" | head -1)
    if [ -n "$README_FILE" ]; then
        # Extract command containing keywords
        grep -E "(run|start|serve|dev|preview)" "$README_FILE" | grep -E "^\s*\`?[a-z]+" | head -1 | \
        sed -E 's/.*\`?([^`]+)$/\1/' | sh
    fi
fi
```

2. Capture the port number from the server output (or use default 8000).

3. Call MCP Tool `request_preview` with the listening port number to get a preview URL.

4. Present the preview URL to the user.

## Notes

- The server **MUST** run in the background or as a subagent task to avoid blocking the session.
- Default port for static server is 8000.
- For Node.js projects, the port depends on the project configuration.
- The port number can be dynamically changed when conflicted with another service.
- Ensure dependencies are installed before running:
  - Node.js: `npm install`
  - Python: `pip install -r requirements.txt` (if exists)
  - PHP: `composer install` (if composer.json exists)
  - Ruby/Rails: `bundle install` (if Gemfile exists)
  - Go: `go mod download` (automatically handled by go run)
  - Java: Dependencies are handled by Maven/Gradle wrapper
  - Rust: `cargo fetch` (automatically handled by cargo run)