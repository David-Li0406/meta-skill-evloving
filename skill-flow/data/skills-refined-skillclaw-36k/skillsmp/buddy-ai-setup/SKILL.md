---
name: buddy-ai-setup
description: Configure Buddy AI with Anthropic Claude API and set up automated insight generation via cron jobs (daily, weekly, monthly). Use when setting up Buddy AI, configuring cron jobs, or troubleshooting AI insights.
allowed-tools: [Bash(python*), Bash(crontab*), Bash(sqlite3:*), Read, Grep]
---

# Buddy AI Setup & Cron Configuration

Configure Buddy AI for automated financial insights using Anthropic's Claude API.

## Setup Checklist

```
Buddy AI Setup:
- [ ] Add ANTHROPIC_API_KEY to .env
- [ ] Install anthropic package (>=0.40.0)
- [ ] Create database tables (weekly_reflections, etc.)
- [ ] Test manual insight generation
- [ ] Set up 3 cron jobs (daily, weekly, monthly)
- [ ] Create logs directory
- [ ] Verify cron jobs installed
```

## Quick Start

### 1. Add API Key

```bash
# Add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env
```

Get key from: https://console.anthropic.com/

### 2. Install Package

```bash
source .venv/bin/activate
pip install anthropic>=0.40.0
```

### 3. Create Database Tables

```bash
sqlite3 budget_buddy.db < backend/database/migrations/create_buddy_insights_tables.sql
```

Verify:
```bash
sqlite3 budget_buddy.db ".tables" | grep -E "weekly|reflection"
```

Should show:
- weekly_reflections
- weekly_plans
- monthly_reflections

### 4. Test Manual Generation

```bash
# Test daily insight
python backend/scripts/generate_buddy_daily.py

# Test weekly insight
python backend/scripts/generate_buddy_weekly.py

# Test monthly insight
python backend/scripts/generate_buddy_monthly.py
```

Expected output:
```
Generating daily insight...
Fetched 42 transactions from last 7 days
Calling Claude API...
Insight saved to database
Done!
```

### 5. Set Up Cron Jobs

```bash
# Edit crontab
crontab -e

# Add these 3 lines (use absolute paths):
0 6 * * * /full/path/to/.venv/bin/python /full/path/to/backend/scripts/generate_buddy_daily.py >> /full/path/to/logs/buddy_daily.log 2>&1
0 6 * * 1 /full/path/to/.venv/bin/python /full/path/to/backend/scripts/generate_buddy_weekly.py >> /full/path/to/logs/buddy_weekly.log 2>&1
0 6 1 * * /full/path/to/.venv/bin/python /full/path/to/backend/scripts/generate_buddy_monthly.py >> /full/path/to/logs/buddy_monthly.log 2>&1
```

**Schedule**:
- Daily: 6 AM every day (rolling 7-day insights)
- Weekly: 6 AM every Monday (full week insights)
- Monthly: 6 AM 1st of month (monthly review)

### 6. Create Logs Directory

```bash
mkdir -p logs
```

### 7. Verify Installation

```bash
# Check cron jobs
crontab -l | grep buddy

# Should show 3 lines
```

## Configuration

**Model**: `claude-sonnet-4-20250514`
**Max Tokens**: 1024
**Temperature**: 0.7
**Rate Limit**: 1 refresh per insight type per day

**Config file**: `/backend/config/buddy_config.py`

Customize model, tokens, or temperature if needed.

## Insight Scripts

**Daily** (`generate_buddy_daily.py`):
- Last 7 days transactions (rolling)
- Quick spending analysis
- Budget comparison

**Weekly** (`generate_buddy_weekly.py`):
- Last Monday-Sunday
- Full week analysis
- Category breakdowns
- Recommendations

**Monthly** (`generate_buddy_monthly.py`):
- Full previous month
- Comprehensive review
- Budget vs actual
- Long-term trends

## Common Issues

### API Key Invalid

```bash
# Check format (should start with sk-ant-)
grep ANTHROPIC_API_KEY .env

# Verify at console.anthropic.com
# Regenerate if needed
```

### No Insights Generated

```bash
# Run manually to see errors
python -u backend/scripts/generate_buddy_daily.py

# Check logs
tail -100 logs/buddy_daily.log

# Verify transactions exist
sqlite3 budget_buddy.db "SELECT COUNT(*) FROM transactions WHERE date >= date('now', '-7 days');"
```

### Cron Jobs Not Running

```bash
# View cron logs (macOS)
log show --predicate 'process == "cron"' --last 1h

# Verify absolute paths match
which python  # Should match crontab path

# Test cron syntax at https://crontab.guru/
```

### Permission Denied

```bash
# Make script executable
chmod +x backend/scripts/generate_buddy_daily.py

# Make logs writable
chmod 755 logs/
```

## Testing

### Test API Connection

```python
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Say hello!'}]
)
print(response.content[0].text)
```

### Verify Database

```bash
sqlite3 budget_buddy.db "
SELECT week_start_date, substr(spending_summary, 1, 100)
FROM weekly_reflections
ORDER BY created_at DESC
LIMIT 1;
"
```

## Detailed Setup & Troubleshooting

**Complete cron configuration and troubleshooting**: See [CRON_SETUP.md](CRON_SETUP.md)

Includes:
- Cron syntax reference
- Detailed insight script documentation
- Full configuration options
- Complete troubleshooting guide
- API cost optimization tips
- Rate limiting implementation
- Frontend integration examples

## Integration with Other Skills

- **Full-Stack Setup** - Requires ANTHROPIC_API_KEY from .env
- **Backend Server Startup** - API endpoints serve insights
- **Database Migration Runner** - Creates Buddy AI tables
- **Development Diagnostics** - Validates configuration

## References

- [CRON_SETUP.md](CRON_SETUP.md) - Complete cron and troubleshooting guide
- `/backend/config/buddy_config.py` - Configuration
- `/backend/scripts/generate_buddy_*.py` - Generation scripts
- Anthropic API: https://docs.anthropic.com/

## Last Updated

January 1, 2026
