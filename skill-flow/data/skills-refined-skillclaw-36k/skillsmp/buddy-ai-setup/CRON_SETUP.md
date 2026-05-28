# Buddy AI Cron Setup and Troubleshooting

Detailed cron configuration, insight generation scripts, and troubleshooting for Buddy AI.

## Cron Schedule Reference

### Cron Syntax

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, 0/7=Sunday)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

### Budget Buddy Cron Jobs

```bash
# Daily: Rolling 7-day insights (6 AM every day)
0 6 * * * /Users/franklindickinson/Projects/budget-buddy-2/.venv/bin/python /Users/franklindickinson/Projects/budget-buddy-2/backend/scripts/generate_buddy_daily.py >> /Users/franklindickinson/Projects/budget-buddy-2/logs/buddy_daily.log 2>&1

# Weekly: Full week insights (6 AM every Monday)
0 6 * * 1 /Users/franklindickinson/Projects/budget-buddy-2/.venv/bin/python /Users/franklindickinson/Projects/budget-buddy-2/backend/scripts/generate_buddy_weekly.py >> /Users/franklindickinson/Projects/budget-buddy-2/logs/buddy_weekly.log 2>&1

# Monthly: Full month insights (6 AM 1st of month)
0 6 1 * * /Users/franklindickinson/Projects/budget-buddy-2/.venv/bin/python /Users/franklindickinson/Projects/budget-buddy-2/backend/scripts/generate_buddy_monthly.py >> /Users/franklindickinson/Projects/budget-buddy-2/logs/buddy_monthly.log 2>&1
```

**CRITICAL**: Use absolute paths!

### Common Cron Schedules

```bash
# Every day at 6 AM
0 6 * * *

# Every Monday at 6 AM
0 6 * * 1

# 1st of every month at 6 AM
0 6 1 * *

# Every hour
0 * * * *

# Every 30 minutes
*/30 * * * *
```

## Insight Generation Scripts

### Daily Script

**Path**: `/backend/scripts/generate_buddy_daily.py`

**What it does**:
- Fetches transactions from last 7 days (rolling window)
- Analyzes spending patterns
- Compares to budget
- Generates quick insights

**Manual run**:
```bash
python backend/scripts/generate_buddy_daily.py
```

### Weekly Script

**Path**: `/backend/scripts/generate_buddy_weekly.py`

**What it does**:
- Fetches transactions from last Monday-Sunday
- Full week analysis
- Category breakdowns
- Goal progress tracking
- Recommendations for next week

**Manual run**:
```bash
python backend/scripts/generate_buddy_weekly.py
```

### Monthly Script

**Path**: `/backend/scripts/generate_buddy_monthly.py`

**What it does**:
- Fetches all transactions from previous month
- Comprehensive monthly review
- Budget vs actual comparison
- Sinking fund progress
- Long-term trend analysis
- Planning for next month

**Manual run**:
```bash
python backend/scripts/generate_buddy_monthly.py
```

## Buddy AI Configuration

### Configuration File

Located at `/backend/config/buddy_config.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

BUDDY_CONFIG = {
    # Anthropic API
    'api_key': os.getenv('ANTHROPIC_API_KEY'),
    'model': 'claude-sonnet-4-20250514',
    'max_tokens': 1024,
    'temperature': 0.7,

    # Rate Limiting
    'rate_limit_per_day': 1,

    # Cron Schedule
    'daily_cron': '0 6 * * *',
    'weekly_cron': '0 6 * * 1',
    'monthly_cron': '0 6 1 * *',
}
```

### Customization

**Change Model**:
```python
'model': 'claude-opus-4-20241113',  # More powerful, higher cost
```

**Increase Max Tokens** (longer insights):
```python
'max_tokens': 2048,
```

**Adjust Temperature** (creativity):
```python
'temperature': 0.5,  # More consistent
'temperature': 0.9,  # More creative
```

## Troubleshooting

### Issue: API Key Invalid

**Error**: `AuthenticationError: Invalid API key`

**Solution**:
```bash
# Check API key format
grep ANTHROPIC_API_KEY .env
# Should start with: sk-ant-

# Verify key at console.anthropic.com
# Regenerate if needed

# Update .env
nano .env
# Restart backend
```

### Issue: No Insights Generated

**Possible Causes**:
1. No transactions in database
2. API key missing/invalid
3. Script error

**Debug**:
```bash
# Run script manually with verbose output
python -u backend/scripts/generate_buddy_daily.py

# Check logs
tail -100 logs/buddy_daily.log

# Verify transactions exist
sqlite3 budget_buddy.db "SELECT COUNT(*) FROM transactions WHERE date >= date('now', '-7 days');"
```

### Issue: Cron Jobs Not Running

**Debug**:
```bash
# View cron logs (macOS)
log show --predicate 'process == "cron"' --last 1h

# Test cron syntax at https://crontab.guru/

# Verify absolute paths
which python  # Should match path in crontab
```

### Issue: Permission Denied

**Solution**:
```bash
# Ensure script is executable
chmod +x backend/scripts/generate_buddy_daily.py

# Ensure log directory is writable
chmod 755 logs/

# Use full paths in crontab
```

### Issue: High API Costs

**Solutions**:

1. **Reduce frequency**:
   ```bash
   # Weekly instead of daily
   0 6 * * 1 python ...generate_buddy_weekly.py
   ```

2. **Use smaller model**:
   ```python
   'model': 'claude-haiku-3',  # Faster, cheaper
   ```

3. **Reduce max_tokens**:
   ```python
   'max_tokens': 512,
   ```

4. **Monitor usage** at Anthropic console

## Testing Buddy AI

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

Expected: `Hello! How can I help you today?`

### Test Insight Generation

```bash
# Generate with verbose logging
python -u backend/scripts/generate_buddy_daily.py
```

Check output:
- ✅ "Fetched X transactions"
- ✅ "Calling Claude API"
- ✅ "Insight saved to database"
- ✅ No errors

### Verify Database

```bash
sqlite3 budget_buddy.db "
SELECT
    week_start_date,
    substr(spending_summary, 1, 100),
    created_at
FROM weekly_reflections
ORDER BY created_at DESC
LIMIT 1;
"
```

## Rate Limiting

**Rule**: Each insight type can only be refreshed once per day

**Implementation**:
```python
from datetime import datetime, timedelta

def can_refresh_insight(insight_type: str) -> bool:
    last_insight = db.query(Reflection).filter(
        Reflection.type == insight_type
    ).order_by(Reflection.created_at.desc()).first()

    if not last_insight:
        return True

    time_since_last = datetime.now() - last_insight.created_at
    return time_since_last >= timedelta(hours=24)
```

**User Experience**:
- Refresh button disabled if refreshed within 24 hours
- Shows "Last updated: X hours ago"

## Integration with Frontend

### API Endpoints

```
GET /api/v2/buddy/weekly-reflection
GET /api/v2/buddy/weekly-plan
POST /api/v2/buddy/refresh-weekly
```

### React Component Example

```javascript
const fetchWeeklyInsight = async () => {
  setLoading(true);
  try {
    const response = await fetch('/api/v2/buddy/weekly-reflection');
    const data = await response.json();
    setInsight(data);
  } catch (error) {
    console.error('Error fetching insight:', error);
  } finally {
    setLoading(false);
  }
};

useEffect(() => {
  fetchWeeklyInsight();
}, []);
```
