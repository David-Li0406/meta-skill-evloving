# MyAgentive API Keys Setup Guide

API keys are stored in `~/.myagentive/config` and automatically loaded as environment variables when MyAgentive starts.

## Adding API Keys

To add a new API key:
```bash
echo "KEY_NAME=your_api_key_here" >> ~/.myagentive/config
```

Or edit the config file directly:
```bash
nano ~/.myagentive/config
```

**Important:** No quotes around values, no trailing spaces.

---

## Deepgram (Audio/Video Transcription)

**Variable:** `DEEPGRAM_API_KEY`

**Purpose:** Transcribe audio files (MP3, WAV, M4A, AAC) and video files (MP4, MOV, AVI). Used by the `deepgram-transcription` skill.

**Free Tier:** $200 credit for new accounts (no credit card required)

### Setup Steps

1. Go to https://deepgram.com
2. Click "Sign Up" and create a free account
3. Navigate to Console > API Keys
4. Click "Create a New API Key"
5. Give it a name (e.g., "MyAgentive")
6. Copy the generated key
7. Add to config:
   ```bash
   echo "DEEPGRAM_API_KEY=your_key_here" >> ~/.myagentive/config
   ```

### Usage

Once configured, MyAgentive can transcribe:
- Voice messages sent via Telegram
- Audio files uploaded to the chat
- Video files (audio extracted automatically)

---

## Google Gemini (Image Generation)

**Variable:** `GEMINI_API_KEY`

**Purpose:** Generate images from text descriptions using Google's Imagen model. Used by the `gemini-imagen` skill.

**Free Tier:** Limited requests per minute (sufficient for personal use)

### Setup Steps

1. Go to https://ai.google.dev
2. Sign in with your Google account
3. Click "Get API key" or go to https://aistudio.google.com/apikey
4. Create a new API key
5. Copy the key
6. Add to config:
   ```bash
   echo "GEMINI_API_KEY=your_key_here" >> ~/.myagentive/config
   ```

### Supported Models

- `imagen-3.0-generate-002` - Latest image generation
- `gemini-2.0-flash-exp` - Multimodal with image output

---

## ElevenLabs (Voice Synthesis)

**Variable:** `ELEVENLABS_API_KEY`

**Purpose:** Generate natural AI voices for phone calls. Used by the `twilio-phone` skill.

**Free Tier:** 10,000 characters per month

### Setup Steps

1. Go to https://elevenlabs.io
2. Sign up for a free account
3. Go to Profile > API Keys
4. Copy your API key
5. Add to config:
   ```bash
   echo "ELEVENLABS_API_KEY=your_key_here" >> ~/.myagentive/config
   ```

### Voice Options

ElevenLabs offers various preset voices. Common choices:
- `rachel` - Professional female
- `adam` - Professional male
- `antoni` - Casual male

---

## Anthropic API (Optional)

**Variable:** `ANTHROPIC_API_KEY`

**Purpose:** Use Anthropic's pay-per-use API instead of Claude Code subscription.

**When to Use:** Only set this if you want to pay per API call. Leave empty/unset to use your Claude Code subscription (recommended for most users).

### Setup Steps

1. Go to https://console.anthropic.com
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new API key
5. Add to config:
   ```bash
   echo "ANTHROPIC_API_KEY=your_key_here" >> ~/.myagentive/config
   ```

### Pricing

Pay-per-use based on token count:
- Claude Opus: Higher cost, best quality
- Claude Sonnet: Balanced cost/quality
- Claude Haiku: Lowest cost, fastest

---

## LinkedIn API (Social Media Posting)

**Variables:**
- `LINKEDIN_CLIENT_ID`
- `LINKEDIN_CLIENT_SECRET`
- `LINKEDIN_ACCESS_TOKEN`

**Purpose:** Post content to LinkedIn. Used by the `social-media-poster` skill.

**Requirement:** Must have a LinkedIn Company Page

### Setup Steps

1. Go to https://www.linkedin.com/developers/apps
2. Create a new app
3. Request "Share on LinkedIn" permission
4. Get Client ID and Client Secret from app settings
5. Generate access token using OAuth 2.0 flow:
   - Use the script at `scripts/get_token.py` (in social-media-poster skill)
   - Or follow LinkedIn's OAuth documentation
6. Add to config:
   ```bash
   echo "LINKEDIN_CLIENT_ID=your_id" >> ~/.myagentive/config
   echo "LINKEDIN_CLIENT_SECRET=your_secret" >> ~/.myagentive/config
   echo "LINKEDIN_ACCESS_TOKEN=your_token" >> ~/.myagentive/config
   ```

### Token Refresh

LinkedIn access tokens expire after ~60 days. When expired:
1. Run the token refresh script
2. Update `LINKEDIN_ACCESS_TOKEN` in config

---

## Twitter/X API (Social Media Posting)

**Variables:**
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`

**Purpose:** Post content to Twitter/X. Used by the `social-media-poster` skill.

**Free Tier:** 1,500 tweets per month

### Setup Steps

1. Go to https://developer.x.com/en/portal/dashboard
2. Create a new project and app
3. In App Settings > User authentication settings:
   - Enable OAuth 1.0a
   - Set App permissions to "Read and write"
4. Go to Keys and Tokens:
   - Copy API Key and API Key Secret
   - Generate Access Token and Secret (with read+write permissions)
   - Generate Bearer Token
5. Add to config:
   ```bash
   echo "TWITTER_API_KEY=your_key" >> ~/.myagentive/config
   echo "TWITTER_API_SECRET=your_secret" >> ~/.myagentive/config
   echo "TWITTER_ACCESS_TOKEN=your_token" >> ~/.myagentive/config
   echo "TWITTER_ACCESS_TOKEN_SECRET=your_token_secret" >> ~/.myagentive/config
   echo "TWITTER_BEARER_TOKEN=your_bearer" >> ~/.myagentive/config
   ```

**Important:** After changing permissions, you must regenerate your tokens.

---

## OpenAI API (Android Vision)

**Variable:** `OPENAI_API_KEY`

**Purpose:** Optional vision-based UI detection for the `android-use` skill. Not required for basic Android control via ADB.

### Setup Steps

1. Go to https://platform.openai.com
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new API key
5. Add to config:
   ```bash
   echo "OPENAI_API_KEY=your_key_here" >> ~/.myagentive/config
   ```

---

## Twilio (Phone Calls and SMS)

**Variables:**
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`

**Purpose:** Make phone calls and send SMS. Used by the `twilio-phone` skill.

**Free Trial:** Includes trial credits for testing

### Setup Steps

1. Go to https://www.twilio.com
2. Sign up for a free trial
3. Verify your phone number
4. Get a Twilio phone number
5. Copy Account SID and Auth Token from Console Dashboard
6. Add to config:
   ```bash
   echo "TWILIO_ACCOUNT_SID=your_sid" >> ~/.myagentive/config
   echo "TWILIO_AUTH_TOKEN=your_token" >> ~/.myagentive/config
   echo "TWILIO_PHONE_NUMBER=+1234567890" >> ~/.myagentive/config
   ```

---

## Verifying API Keys

To check which keys are configured:

```bash
# List all configured keys (values hidden)
grep "_KEY\|_TOKEN\|_SECRET\|_SID" ~/.myagentive/config | cut -d'=' -f1

# Check specific key exists
grep "DEEPGRAM_API_KEY" ~/.myagentive/config
```

To validate configuration:

```bash
python .claude/skills/myagentive/scripts/check_config.py
```

---

## Troubleshooting

**"API key not found" errors:**
- Check key is in config: `grep KEY_NAME ~/.myagentive/config`
- Ensure no quotes around value
- Restart MyAgentive after adding keys

**"Invalid API key" errors:**
- Verify key is correct (no extra spaces)
- Check key has required permissions
- Some keys expire - generate a new one

**Keys not being loaded:**
- Config file must be at `~/.myagentive/config`
- Each key on its own line: `KEY_NAME=value`
- No spaces around `=`
