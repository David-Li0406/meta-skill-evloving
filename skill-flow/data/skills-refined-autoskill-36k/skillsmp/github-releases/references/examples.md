# Examples: GitHub Releases

The following examples demonstrate how to use the `gh release` CLI for common tasks.

## 1. Creating a Release

### Create a Draft Release
```bash
gh release create v1.0.0 --title "Initial Release" --notes "First production ready version." --draft
```

### Create a Release from a Specific Branch
```bash
gh release create v1.1.0-beta --target develop --prerelease --notes "Beta testing for the new feature."
```

---

## 2. Managing Assets

### Upload Assets to an Existing Release
```bash
gh release upload v1.0.0 ./bin/app.exe ./docs/manual.pdf
```

### Download All Assets from the Latest Release
```bash
gh release download --dir ./downloads
```

---

## 3. Informational & Cleanup

### List Recent Releases
```bash
gh release list --limit 5
```

### Publish a Previously Drafted Release
```bash
gh release edit v1.0.0 --draft=false
```

### Delete a Release and its Tag
```bash
gh release delete v0.1.0-old --yes --cleanup-tag
```
