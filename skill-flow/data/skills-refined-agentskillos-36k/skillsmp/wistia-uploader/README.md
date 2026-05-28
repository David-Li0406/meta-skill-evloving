# Wistia Video Uploader Skill

Upload video files to Wistia using the Data API with automatic transcript generation.

## Quick Start

### 1. Install Dependencies
```bash
cd /Users/jvincent/.claude/skills/wistia-uploader
npm install
```

### 2. Configure API Token
```bash
# Copy the example config
cp .env.example .env

# Edit .env and add your Wistia API token
# Get your token from: https://[yourcompany].wistia.com/settings/api
```

### 3. Upload a Video
Tell Claude:
```
Upload /path/to/video.mp4 to Wistia
```

## Features

- ✅ Upload videos to Wistia account root or specific projects
- ✅ Automatic transcript generation by Wistia
- ✅ Custom video names and descriptions
- ✅ Support for all common video formats (mp4, mov, avi, etc.)
- ✅ Integration with video-transcript-analyzer skill
- ✅ Comprehensive error handling

## Usage Examples

### Basic Upload
```
Upload this video to Wistia: /Users/jvincent/Downloads/interview.mp4
```

### Upload to Specific Project
```
Upload /Users/jvincent/Downloads/demo.mp4 to Wistia project abc123
and name it "Q4 Product Demo"
```

### Upload and Analyze
```
Upload this customer interview to Wistia and analyze the transcript
once it's ready: /Users/jvincent/Downloads/interview.mp4
```

## Finding Your Project ID

1. Log in to Wistia
2. Navigate to the project
3. Check the URL: `https://yourcompany.wistia.com/projects/{PROJECT_ID}`

Or use the API:
```bash
curl -u api:YOUR_API_TOKEN https://api.wistia.com/v1/projects.json
```

## Transcript Generation

Wistia automatically generates transcripts for all uploaded videos:
- Processing time: ~1 minute per minute of video
- Accessible at: `https://yourcompany.wistia.com/medias/{VIDEO_ID}/captions`
- Can be downloaded in SRT, VTT, or plain text format

## Integration with Customer Interview Workflow

This skill integrates seamlessly with the customer interview analysis workflow:

1. **Upload video** → Wistia (this skill)
2. **Wait for transcript** → Automatic (Wistia)
3. **Download transcript** → SRT or text
4. **Analyze transcript** → video-transcript-analyzer skill
5. **Update syntheses** → Manual or guided by Claude

## Troubleshooting

### "WISTIA_API_TOKEN not found"
Create a `.env` file with your API token (see Setup above)

### "Authentication failed"
Check that your API token is valid and hasn't been revoked

### "Project not found"
Verify the project ID exists in your Wistia account

### "Unsupported video format"
Convert to mp4, mov, or another supported format

## Supported Video Formats

- mp4
- mov
- avi
- wmv
- flv
- mkv
- webm
- ogv
- mpg/mpeg

## API Reference

- Wistia Upload API: https://wistia.com/support/developers/upload-api
- Wistia Data API: https://wistia.com/support/developers/data-api

## File Structure

```
wistia-uploader/
├── Skill.md              # Skill definition for Claude
├── README.md             # This file
├── upload.js             # Upload script
├── package.json          # Node.js dependencies
├── .env.example          # Example configuration
├── .env                  # Your configuration (gitignored)
└── resources/
    └── EXAMPLES.md       # Detailed usage examples
```
