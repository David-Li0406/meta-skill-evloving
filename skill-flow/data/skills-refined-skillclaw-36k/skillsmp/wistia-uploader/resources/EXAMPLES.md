# Wistia Uploader - Usage Examples

## Example 1: Simple Upload (Account Root)

**User request:**
```
Upload /Users/jvincent/Downloads/interview-recording.mp4 to Wistia
```

**Claude execution:**
```bash
cd /Users/jvincent/.claude/skills/wistia-uploader
node upload.js --file="/Users/jvincent/Downloads/interview-recording.mp4"
```

**Script output:**
```json
{
  "success": true,
  "video_id": "abc123xyz",
  "name": "interview-recording.mp4",
  "url": "https://yourcompany.wistia.com/medias/abc123xyz",
  "embed_url": "https://fast.wistia.net/embed/iframe/abc123xyz",
  "thumbnail_url": "https://embed-ssl.wistia.com/deliveries/abc123xyz.jpg",
  "duration": 1847.5,
  "transcript_url": "https://yourcompany.wistia.com/medias/abc123xyz/captions",
  "created": "2025-05-02T15:30:00Z",
  "project_id": null
}
```

**Claude response to user:**
```
✅ Video uploaded successfully to Wistia!

📹 Video: interview-recording.mp4
🔗 URL: https://yourcompany.wistia.com/medias/abc123xyz
🆔 Video ID: abc123xyz
⏱️ Duration: 30 minutes 47 seconds
📝 Transcript: https://yourcompany.wistia.com/medias/abc123xyz/captions

Note: Wistia is automatically generating a transcript for this video.
It should be ready in about 30 minutes (approximately 1 minute per minute of video).

Would you like me to check back later to download and analyze the transcript?
```

---

## Example 2: Upload to Specific Project with Custom Name

**User request:**
```
Upload /Users/jvincent/Downloads/demo.mp4 to Wistia project xyz789
and name it "Q4 2025 Product Demo"
```

**Claude execution:**
```bash
cd /Users/jvincent/.claude/skills/wistia-uploader
node upload.js \
  --file="/Users/jvincent/Downloads/demo.mp4" \
  --project="xyz789" \
  --name="Q4 2025 Product Demo"
```

**Claude response to user:**
```
✅ Video uploaded successfully to Wistia project xyz789!

📹 Video: Q4 2025 Product Demo
🔗 URL: https://yourcompany.wistia.com/medias/def456ghi
🆔 Video ID: def456ghi
📁 Project ID: xyz789
📝 Transcript: https://yourcompany.wistia.com/medias/def456ghi/captions

The video is now processing. Transcript generation will begin once processing completes.
```

---

## Example 3: Upload with Name and Description

**User request:**
```
Upload this customer interview to Wistia:
- File: /Users/jvincent/Downloads/matthew-ruxton-interview.mp4
- Name: Matthew Ruxton - Ignite Reading
- Description: Customer interview discussing membership management and registration workflows
```

**Claude execution:**
```bash
cd /Users/jvincent/.claude/skills/wistia-uploader
node upload.js \
  --file="/Users/jvincent/Downloads/matthew-ruxton-interview.mp4" \
  --name="Matthew Ruxton - Ignite Reading" \
  --description="Customer interview discussing membership management and registration workflows"
```

---

## Example 4: First-Time Setup

**User request:**
```
Upload this video to Wistia: /Users/jvincent/Downloads/video.mp4
```

**Claude checks** for `.env` file and finds it missing.

**Claude response:**
```
I need to set up your Wistia API credentials first.

To get your Wistia API token:

1. Log in to your Wistia account
2. Go to Account Settings → API Access (or visit: https://[yourcompany].wistia.com/settings/api)
3. Generate a new API token or copy an existing one

Once you have the token, please provide it and I'll configure the skill for you.
```

**User provides:** `wistia_api_token_abc123xyz`

**Claude creates `.env` file:**
```bash
cat > /Users/jvincent/.claude/skills/wistia-uploader/.env << 'EOF'
WISTIA_API_TOKEN=wistia_api_token_abc123xyz
EOF
```

**Claude response:**
```
✅ Wistia API credentials configured successfully!

Now let me upload your video...
```

---

## Example 5: Upload and Analyze Workflow

**User request:**
```
Upload this interview to Wistia and analyze the transcript:
/Users/jvincent/Downloads/GMT20250502-150851_Recording_avo_640x360.mp4
```

**Claude execution (Step 1 - Upload):**
```bash
cd /Users/jvincent/.claude/skills/wistia-uploader
node upload.js \
  --file="/Users/jvincent/Downloads/GMT20250502-150851_Recording_avo_640x360.mp4" \
  --name="Matthew Ruxton Interview - Ignite Reading"
```

**Claude response:**
```
✅ Video uploaded to Wistia!

📹 Video: Matthew Ruxton Interview - Ignite Reading
🔗 URL: https://yourcompany.wistia.com/medias/xyz789abc
🆔 Video ID: xyz789abc
⏱️ Duration: 45 minutes 23 seconds
📝 Transcript URL: https://yourcompany.wistia.com/medias/xyz789abc/captions

Wistia is now generating the transcript. Based on the video duration (45 minutes),
the transcript should be ready in approximately 45-60 minutes.

I'll wait a few minutes and then check if the transcript is ready to download
and analyze. Would you like me to proceed with that?
```

**Claude execution (Step 2 - Wait and fetch transcript):**
```bash
# Wait ~50 minutes, then fetch transcript from Wistia API
curl -u api:wistia_api_token_abc123xyz \
  "https://api.wistia.com/v1/medias/xyz789abc/captions.json"
```

**Claude execution (Step 3 - Save and analyze):**
```bash
# Save transcript as SRT file
# Then invoke video-transcript-analyzer skill
```

---

## Example 6: Error Handling - Invalid API Token

**User request:**
```
Upload video to Wistia
```

**Claude execution:**
```bash
node upload.js --file="/path/to/video.mp4"
```

**Script output:**
```json
{
  "success": false,
  "error": "Authentication failed. Check your WISTIA_API_TOKEN in .env file",
  "error_code": 401
}
```

**Claude response:**
```
❌ Upload failed: Authentication error

Your Wistia API token appears to be invalid or expired.

Please check:
1. The token in your .env file is correct
2. The token hasn't been revoked in your Wistia account settings
3. You're using the API token (not an account password)

Would you like to update your API token?
```

---

## Example 7: Error Handling - Project Not Found

**User request:**
```
Upload to Wistia project invalid_project_123
```

**Script output:**
```json
{
  "success": false,
  "error": "Project not found. Check the project ID",
  "error_code": 404
}
```

**Claude response:**
```
❌ Upload failed: Project not found

The project ID "invalid_project_123" doesn't exist in your Wistia account.

To find your project IDs:
1. Log in to Wistia
2. Navigate to the project you want to use
3. Look at the URL: https://yourcompany.wistia.com/projects/{PROJECT_ID}

Or, would you like to upload to your account root instead (no project)?
```

---

## Example 8: Integration with Customer Interview Workflow

**Complete workflow:**

1. **User provides video file**
2. **Upload to Wistia** (this skill)
3. **Wait for transcript generation** (automatic)
4. **Download transcript** (curl or Wistia API)
5. **Analyze transcript** (video-transcript-analyzer skill)
6. **Update synthesis docs** (manual or automated)

**User request:**
```
I have a customer interview recording. Upload it to Wistia and once the
transcript is ready, analyze it and update my synthesis documents.
```

**Claude workflow:**
```
1. Upload video using wistia-uploader skill
2. Wait for Wistia to generate transcript (~1 min per video minute)
3. Download transcript from Wistia API
4. Invoke video-transcript-analyzer skill
5. Generate interview analysis markdown
6. Prompt user to update relevant synthesis documents
```

---

## Finding Your Wistia Project ID

### Method 1: From the Wistia UI
1. Log in to your Wistia account
2. Click on "Projects" in the navigation
3. Click on the project you want to upload to
4. Look at the URL in your browser
5. The project ID is the alphanumeric string after `/projects/`
   - Example: `https://yourcompany.wistia.com/projects/abc123xyz`
   - Project ID: `abc123xyz`

### Method 2: Using the Wistia API
```bash
# List all projects
curl -u api:YOUR_API_TOKEN https://api.wistia.com/v1/projects.json

# Output includes project IDs:
[
  {
    "id": "abc123xyz",
    "name": "Customer Interviews",
    "mediaCount": 15
  },
  {
    "id": "def456ghi",
    "name": "Product Demos",
    "mediaCount": 8
  }
]
```

---

## Common Issues and Solutions

### Issue: "File not found"
**Cause:** Invalid or relative file path
**Solution:** Use absolute path starting with `/Users/...`

### Issue: "Unsupported video format"
**Cause:** Video file extension not supported by Wistia
**Solution:** Convert to mp4, mov, or another supported format first

### Issue: "File is too large"
**Cause:** Video exceeds Wistia account limits
**Solution:**
- Compress the video
- Upgrade Wistia account
- Split video into smaller segments

### Issue: "Transcript not ready yet"
**Cause:** Wistia is still processing the video or generating transcript
**Solution:** Wait longer (approximately 1 minute per video minute)

### Issue: "No WISTIA_API_TOKEN found"
**Cause:** `.env` file doesn't exist or is missing the token
**Solution:** Create `.env` file with your API token
