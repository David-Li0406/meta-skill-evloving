# Troubleshooting: Extract Stitch Mockups

Common issues and solutions for mockup extraction.

---

## Installation Issues

### Browser Not Available

**Error:**
```
Browser tools not available
```

**Solution:**
Ensure you're using Cursor IDE with the built-in browser (MCP browser tools). The browser is automatically available in Cursor.

---


## Authentication Issues

### Not Signed Into Google

**Symptoms:**
- Browser redirects to sign-in page
- No images captured
- Snapshot shows sign-in prompt

**Solution:**
1. Navigate to `https://stitch.withgoogle.com` in Cursor's browser
2. Sign in with your Google account
3. The browser maintains the session automatically
4. Re-run extraction

### Session Expired

**Symptoms:**
- Previously worked but now fails
- Redirects to sign-in

**Solution:**
Refresh Google session in Cursor's browser. Navigate to Stitch and sign in again if needed.

---

## Extraction Issues

### No Images Found

**Error:**
```
No mockup images found on the page.
Make sure the project has completed generating.
```

**Possible causes:**

1. **Project is empty**
   - The project exists but has no generated designs
   - Solution: Generate designs in Stitch first

2. **Generation failed**
   - Stitch generation failed silently
   - Solution: Check project in Stitch UI, regenerate if needed

3. **Page didn't fully load**
   - Network issues or slow connection
   - Solution: Wait longer after navigation (use `browser_wait_for` with more time)

4. **URL pattern changed**
   - Google updated image hosting
   - Solution: Check snapshot for image elements and verify URL patterns in `src` attributes

5. **Snapshot parsing issue**
   - Image URLs not found in DOM snapshot
   - Solution: Inspect snapshot structure and adjust parsing logic

### Still Generating

**Error:**
```
Error: Project is still generating.
Please wait for generation to complete and try again.
```

**Solution:**
1. Open project URL in browser
2. Wait for generation to complete (~40 seconds)
3. Verify mockups are visible
4. Re-run extraction

### Wrong Images Extracted

**Symptoms:**
- Script saves UI elements, avatars, or icons instead of mockups

**Cause:**
Image filtering not strict enough.

**Solution:**
Filter for `lh3.googleusercontent.com/aida/` URLs in the `src` attribute of `<img>` elements. If wrong images appear:
1. Check the actual URLs of unwanted images in the snapshot
2. Add additional filtering in the snapshot parsing logic
3. Verify the image element's dimensions or other attributes if needed

---

## URL Issues

### Invalid URL Format

**Error:**
```
Error: Invalid Stitch project URL: <url>
Expected format: https://stitch.withgoogle.com/projects/<id>
```

**Solution:**
Use the full project URL, not:
- Just the project ID
- The landing page URL
- A shortened URL

**Correct format:**
```
https://stitch.withgoogle.com/projects/3236066188909813678
```

### Project Not Found

**Symptoms:**
- Page shows 404 or error
- No images captured

**Possible causes:**
1. Project was deleted
2. Project belongs to different account
3. Typo in URL

**Solution:**
1. Verify URL in browser first
2. Check you're signed into correct Google account
3. Copy URL directly from browser address bar

---

## Directory Issues

### Feature Directory Not Found

**Error:**
```
Could not auto-detect feature directory.
Existing feature directories:
  1. dashboard
  2. eco-travel

Please re-run with --feature <name> to specify target directory.
```

**Solutions:**

1. **Specify manually:**
   ```bash
   python scripts/extract_images.py "<url>" --feature dashboard
   ```

2. **Create feature first:**
   Use authoring-stitch-prompts skill to create the feature directory structure, then extract.

3. **Let script create new:**
   If no features exist, script automatically creates one based on project title.

### Permission Denied

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'design-intent/google-stitch/feature/exports/mockup-1.png'
```

**Solution:**
Ensure the output directory is writable:
```bash
chmod -R u+w design-intent/google-stitch/
```

Or create the directory structure first:
```bash
mkdir -p design-intent/google-stitch/{feature}/exports
```

### Directory Already Has Files

**Behavior:**
Script overwrites existing `mockup-*.png` files.

**To preserve existing:**
1. Rename existing files first
2. Or use `--output` to save to different location

---

## Performance Issues

### Slow Extraction

**Symptoms:**
- Extraction takes >30 seconds
- Page loads slowly

**Possible causes:**
1. Slow network connection
2. Large number of images
3. Heavy page content

**Solutions:**
1. Check internet connection
2. Wait longer for page load using `browser_wait_for`
3. Verify project generation is complete before extraction

---

## Debugging

### Check Snapshot Content

1. Take a snapshot after navigating to the Stitch URL
2. Inspect the snapshot structure to find image elements
3. Verify image URLs contain `lh3.googleusercontent.com/aida/`

### Manual Inspection

1. Navigate to the Stitch project URL in Cursor's browser
2. Take a snapshot to see the page structure
3. Check if "Generating..." text is present
4. Verify mockup images are visible in the page
5. Inspect image elements in the snapshot

### Verify Image URLs

1. Parse the snapshot to find all `<img>` elements
2. Filter for `src` attributes containing `lh3.googleusercontent.com/aida/`
3. Verify these URLs are valid and accessible

---

## Getting Help

If issues persist:

1. **Check investigation notes:** `docs/stitch/stitch-investigation.md`
2. **Verify Stitch is accessible:** Open URL in browser
3. **Test with simple project:** Create new project in Stitch, then extract
4. **Check script output:** Look for specific error messages
