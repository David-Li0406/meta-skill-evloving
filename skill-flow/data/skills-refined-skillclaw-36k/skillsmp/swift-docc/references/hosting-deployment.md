# Hosting and Deployment Reference

Complete guide to building, hosting, and deploying DocC documentation.

## Building Documentation

### Xcode

Build documentation in Xcode:

1. Select **Product → Build Documentation** (⌃⇧⌘D)
2. Documentation opens in Developer Documentation window
3. Export: **Product → Build Documentation Archive**

### Swift Package Manager

Add the DocC plugin:

```swift
// Package.swift
let package = Package(
    name: "MyPackage",
    dependencies: [
        .package(url: "https://github.com/apple/swift-docc-plugin", from: "1.3.0")
    ],
    // ...
)
```

Generate documentation:

```bash
# Generate documentation
swift package generate-documentation --target MyTarget

# Generate with custom output
swift package --allow-writing-to-directory ./docs \
    generate-documentation \
    --target MyTarget \
    --output-path ./docs

# Preview documentation locally
swift package --disable-sandbox preview-documentation --target MyTarget
```

### Command Line (xcrun)

Use `xcrun docc` directly:

```bash
# Convert symbol graph to documentation
xcrun docc convert MyTarget.symbols.json \
    --output-path ./docs \
    --fallback-display-name MyTarget \
    --fallback-bundle-identifier com.example.mytarget \
    --fallback-bundle-version 1.0.0

# Preview documentation
xcrun docc preview Documentation.docc \
    --fallback-display-name MyTarget
```

## Static Hosting

### Transform for Static Hosting

Generate static files for web hosting:

```bash
swift package --allow-writing-to-directory ./docs \
    generate-documentation \
    --target MyTarget \
    --output-path ./docs \
    --transform-for-static-hosting \
    --hosting-base-path my-repo-name
```

The `--hosting-base-path` should match your hosting path:
- GitHub Pages: Repository name (e.g., `my-repo`)
- Custom domain root: Use `/` or omit

### Output Structure

```
docs/
├── index.html
├── css/
├── js/
├── data/
│   └── documentation/
│       └── mytarget/
├── images/
└── documentation/
    └── mytarget/
        └── index.html
```

## GitHub Pages Deployment

### Basic Workflow

Create `.github/workflows/documentation.yml`:

```yaml
name: Documentation

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: macos-14
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.2.app

      - name: Build Documentation
        run: |
          swift package --allow-writing-to-directory ./docs \
            generate-documentation \
            --target MyTarget \
            --output-path ./docs \
            --transform-for-static-hosting \
            --hosting-base-path ${{ github.event.repository.name }}

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Enable GitHub Pages

1. Go to repository **Settings → Pages**
2. Set **Source** to "GitHub Actions"
3. Push to trigger the workflow

### Multiple Targets

Document multiple targets:

```yaml
- name: Build Documentation
  run: |
    # Build first target
    swift package --allow-writing-to-directory ./docs/target1 \
      generate-documentation \
      --target Target1 \
      --output-path ./docs/target1 \
      --transform-for-static-hosting \
      --hosting-base-path ${{ github.event.repository.name }}/target1

    # Build second target
    swift package --allow-writing-to-directory ./docs/target2 \
      generate-documentation \
      --target Target2 \
      --output-path ./docs/target2 \
      --transform-for-static-hosting \
      --hosting-base-path ${{ github.event.repository.name }}/target2
```

## XcodeGen Projects

For XcodeGen-based projects:

### Add to project.yml

```yaml
targets:
  MyApp:
    type: application
    platform: iOS
    sources:
      - Sources/MyApp
      - path: Sources/MyApp/Documentation.docc
        type: folder
```

### Generate with xcodebuild

```yaml
- name: Build Documentation
  run: |
    xcodebuild docbuild \
      -scheme MyApp \
      -destination 'generic/platform=iOS' \
      -derivedDataPath .build \
      OTHER_DOCC_FLAGS="--transform-for-static-hosting --hosting-base-path ${{ github.event.repository.name }}"

    # Find and move the archive
    ARCHIVE=$(find .build -name "*.doccarchive" | head -1)
    cp -R "$ARCHIVE" ./docs
```

## Custom Domain

### Configure Base Path

For custom domain at root:

```bash
swift package generate-documentation \
    --target MyTarget \
    --output-path ./docs \
    --transform-for-static-hosting
    # No --hosting-base-path needed for root domain
```

For subdirectory:

```bash
swift package generate-documentation \
    --target MyTarget \
    --output-path ./docs \
    --transform-for-static-hosting \
    --hosting-base-path /docs
```

### CNAME File

Create `CNAME` file for custom domain:

```yaml
- name: Configure Custom Domain
  run: echo "docs.example.com" > ./docs/CNAME
```

## Alternative Hosting

### Netlify

Create `netlify.toml`:

```toml
[build]
  command = "swift package --allow-writing-to-directory ./docs generate-documentation --target MyTarget --output-path ./docs --transform-for-static-hosting"
  publish = "docs"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Vercel

Create `vercel.json`:

```json
{
  "buildCommand": "swift package generate-documentation --target MyTarget --output-path ./docs --transform-for-static-hosting",
  "outputDirectory": "docs",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Firebase Hosting

Create `firebase.json`:

```json
{
  "hosting": {
    "public": "docs",
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

## Local Development

### Preview Server

```bash
# Swift Package Manager
swift package --disable-sandbox preview-documentation --target MyTarget

# Opens at http://localhost:8080/documentation/mytarget
```

### Python HTTP Server

```bash
# After generating static docs
cd docs
python3 -m http.server 8000

# Opens at http://localhost:8000
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| 404 on GitHub Pages | Check `--hosting-base-path` matches repo name |
| Blank page | Ensure static hosting transform was applied |
| Missing images | Verify Resources folder is included |
| Old content | Clear browser cache or use incognito |

### Debug Build

Add verbose output:

```bash
swift package generate-documentation \
    --target MyTarget \
    --output-path ./docs \
    --transform-for-static-hosting \
    --hosting-base-path my-repo \
    --verbose
```

### Verify Output

Check generated files:

```bash
ls -la docs/
# Should contain: index.html, css/, js/, data/, documentation/
```
