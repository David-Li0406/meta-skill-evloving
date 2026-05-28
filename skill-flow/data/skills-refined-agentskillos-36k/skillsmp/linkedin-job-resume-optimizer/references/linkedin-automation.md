# LinkedIn Automation Guide

Guide for automating LinkedIn job searches using Playwright MCP.

## LinkedIn Job Search URL Structure

### Basic Search URL

```
https://www.linkedin.com/jobs/search/
```

### Query Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `keywords` | Search keywords | `?keywords=AI%20Engineer` |
| `location` | Job location | `&location=Remote` |
| `f_WT` | Remote filter | `&f_WT=2` (Remote only) |
| `f_TPR` | Time posted | `&f_TPR=r86400` (Past 24 hours) |
| `f_E` | Experience level | `&f_E=3` (Mid-Senior level) |
| `f_JT` | Job type | `&f_JT=F` (Full-time) |
| `start` | Pagination offset | `&start=25` (Page 2) |

### Complete Example URL

```
https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning%20Engineer&location=Remote&f_WT=2&f_TPR=r604800&f_E=3
```

This searches for "Machine Learning Engineer", Remote, Posted in last 7 days, Mid-Senior level.

## Navigation Patterns

### Step-by-Step Workflow

1. **Navigate to Search URL**
   ```python
   mcp_client.call('browser_navigate', {
       'url': 'https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer&location=Remote'
   })
   ```

2. **Wait for Page Load**
   ```python
   mcp_client.call('browser_wait_for', {'time': 3000})  # 3 seconds
   ```

3. **Get Page Snapshot**
   ```python
   snapshot = mcp_client.call('browser_snapshot', {})
   ```

4. **Parse Job Cards**
   - Look for job listing elements in snapshot
   - Extract refs for clicking

5. **Click Job Card**
   ```python
   mcp_client.call('browser_click', {
       'element': 'Job title text',
       'ref': 'e42'  # From snapshot
   })
   ```

6. **Wait for Job Details**
   ```python
   mcp_client.call('browser_wait_for', {'time': 2000})
   ```

7. **Get Job Details Snapshot**
   ```python
   job_snapshot = mcp_client.call('browser_snapshot', {})
   ```

## Element Selectors and Patterns

### Job List Page

**Job Cards**: Look for patterns like:
- "Senior AI Engineer" [ref]
- "TechCorp •" [company]
- "Remote" [location]
- "Posted X days ago"

**Navigation Elements**:
- "Next" button for pagination
- Filter dropdowns (Date posted, Experience level, etc.)

### Job Detail Page

**Key Sections**:
- Job title (usually in large font at top)
- Company name (after "at" or "•")
- "About the job" section (main description)
- "Show more" button (expand full description)
- "Apply" button

**Parsing Strategy**:
```python
def extract_job_details(snapshot_text):
    # Title: First line or large text element
    title = extract_first_line(snapshot_text)

    # Company: Look for "at CompanyName" or "• CompanyName"
    company_match = re.search(r'(?:at|•)\s+(.+?)(?:\n|•)', snapshot_text)

    # Description: After "About the job" or "Job Description"
    desc_start = snapshot_text.find('About the job')
    description = snapshot_text[desc_start:desc_start+3000]

    return {'title': title, 'company': company, 'description': description}
```

## Anti-Bot Detection Strategies

### 1. Random Delays

```python
import random
import time

# Between actions
time.sleep(random.uniform(1, 3))

# After page loads
time.sleep(random.uniform(2, 5))
```

### 2. Human-Like Patterns

- Don't scrape too fast (max 10-15 jobs per session)
- Vary wait times between requests
- Occasionally scroll or hover before clicking
- Don't follow predictable patterns

### 3. Browser Settings

```bash
# Use shared browser context
npx @playwright/mcp@latest --port 8808 --shared-browser-context

# Disable headless mode if needed (more human-like)
# (May require modifying start-server.sh)
```

### 4. User Agent Rotation

If detection occurs, consider rotating user agents:
```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    # Add more variations
]
```

### 5. Session Management

- Login manually before automation (if needed)
- Use cookies from authenticated session
- Clear cookies if rate limited

## Rate Limiting Handling

### Detection Signs

- HTTP 429 (Too Many Requests) status
- "You've been rate limited" message
- Blank snapshots or error pages
- Login wall appearing

### Response Strategy

```python
def search_with_retry(keywords, max_retries=3):
    for attempt in range(max_retries):
        try:
            jobs = search_linkedin_jobs(keywords)
            return jobs
        except RateLimitError:
            wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
    return []
```

### Prevention

- Limit scraping to 2-5 jobs per session
- Add delays between actions (2-5 seconds)
- Don't run multiple sessions simultaneously
- Use `--shared-browser-context` to maintain session state

## Snapshot Parsing Techniques

### Extracting Job Listings

```python
def extract_job_cards_from_snapshot(snapshot_text):
    job_cards = []
    lines = snapshot_text.split('\n')

    for i, line in enumerate(lines):
        # Look for job title patterns
        if any(keyword in line.lower() for keyword in ['engineer', 'developer', 'scientist']):
            # Extract ref number
            ref_match = re.search(r'\[(\d+)\]', line)
            if ref_match:
                ref = ref_match.group(1)
                title = re.sub(r'\[\d+\]', '', line).strip()
                job_cards.append({'ref': ref, 'title': title})

    return job_cards
```

### Extracting Job Description

```python
def extract_description(snapshot_text):
    # Strategy 1: Look for "About the job" section
    desc_markers = ['About the job', 'Job Description', 'Description']

    for marker in desc_markers:
        if marker in snapshot_text:
            start = snapshot_text.find(marker) + len(marker)
            # Take next 3000 chars or until next major section
            end_markers = ['Seniority level', 'Employment type', 'How you match']
            end = start + 3000
            for end_marker in end_markers:
                pos = snapshot_text.find(end_marker, start)
                if pos != -1 and pos < end:
                    end = pos
            return snapshot_text[start:end].strip()

    # Strategy 2: If no marker found, use heuristics
    # Description is usually the longest text block
    return snapshot_text[:3000]
```

### Extracting Required Skills

```python
def extract_required_skills(description):
    # Look for "Required" or "Qualifications" section
    required_section = ""
    patterns = [
        r'(?:Required|Must have|Requirements)[:\s]+(.+?)(?:Preferred|Nice to have|Plus|$)',
        r'(?:Qualifications)[:\s]+(.+?)(?:Preferred|Nice to have|Plus|$)'
    ]

    for pattern in patterns:
        match = re.search(pattern, description, re.DOTALL | re.IGNORECASE)
        if match:
            required_section = match.group(1)
            break

    # Extract technical keywords from section
    tech_keywords = ['Python', 'Java', 'AWS', 'Docker', ...]  # Full list
    found_skills = []

    for keyword in tech_keywords:
        if keyword.lower() in required_section.lower():
            found_skills.append(keyword)

    return found_skills
```

## Error Handling

### Login Wall

```python
def handle_login_wall(snapshot_text):
    if 'sign in' in snapshot_text.lower() or 'join now' in snapshot_text.lower():
        print("LinkedIn requires login")
        print("Options:")
        print("  1. Login manually in browser")
        print("  2. Provide job URLs manually")
        print("  3. Use alternative job boards")
        return True
    return False
```

### Stale Elements

```python
def safe_click(element_desc, ref, max_retries=3):
    for attempt in range(max_retries):
        try:
            mcp_client.call('browser_click', {'element': element_desc, 'ref': ref})
            return True
        except StaleElementError:
            print(f"Stale element, retry {attempt+1}/{max_retries}")
            time.sleep(1)
            # Re-get snapshot
            snapshot = mcp_client.call('browser_snapshot', {})
            # Re-find element
    return False
```

### Connection Failures

```python
def check_playwright_server():
    try:
        response = mcp_client.call('browser_snapshot', {})
        return response is not None
    except Exception:
        return False

if not check_playwright_server():
    print("Playwright server not responding")
    print("Restarting server...")
    restart_playwright_server()
```

## Alternative Strategies

### If LinkedIn Automation Fails

1. **Manual Job URL Input**
   ```python
   jobs = [
       {'url': 'https://linkedin.com/jobs/view/12345', 'title': '...'},
       {'url': 'https://linkedin.com/jobs/view/67890', 'title': '...'}
   ]
   ```

2. **Use LinkedIn API** (If you have access)
   - OAuth authentication required
   - Rate limits apply
   - May require partnership

3. **Alternative Job Boards**
   - Indeed: Often more automation-friendly
   - Glassdoor: Similar structure to LinkedIn
   - Company career pages directly

4. **RSS Feeds**
   - Some companies offer RSS feeds for jobs
   - Can be parsed without web automation

## Debugging Tips

### Save Snapshots for Analysis

```python
# Save snapshot to file
with open('/tmp/linkedin_snapshot.txt', 'w') as f:
    f.write(snapshot_text)

# Review manually to understand structure
cat /tmp/linkedin_snapshot.txt | less
```

### Take Screenshots

```python
screenshot = mcp_client.call('browser_take_screenshot', {
    'type': 'png',
    'fullPage': True
})
# Screenshot saved to file, check path in output
```

### Log All Actions

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Navigating to {url}")
logger.info(f"Clicking element: {element_desc}")
logger.info(f"Extracted {len(jobs)} jobs")
```

## Best Practices

1. **Start Small**: Test with 1-2 jobs before scaling
2. **Monitor Output**: Check snapshot files and logs
3. **Respect Rate Limits**: Don't scrape aggressively
4. **Handle Failures Gracefully**: Provide fallback options
5. **Keep Updated**: LinkedIn structure changes; update selectors
6. **User Privacy**: Don't store personal data unnecessarily
7. **Terms of Service**: Review LinkedIn's ToS and robots.txt

## Example Complete Workflow

```python
# 1. Start server
start_playwright_server()

# 2. Navigate to LinkedIn jobs
url = "https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer&location=Remote"
mcp_client.call('browser_navigate', {'url': url})

# 3. Wait and get snapshot
time.sleep(random.uniform(3, 5))
snapshot = mcp_client.call('browser_snapshot', {})

# 4. Extract job cards
job_cards = extract_job_cards(snapshot['content'])

# 5. For each job
jobs = []
for card in job_cards[:2]:  # Limit to 2
    # Click job
    mcp_client.call('browser_click', {'element': card['title'], 'ref': card['ref']})

    # Wait and get details
    time.sleep(random.uniform(2, 4))
    job_snapshot = mcp_client.call('browser_snapshot', {})

    # Extract and store
    job_data = extract_job_details(job_snapshot['content'])
    jobs.append(job_data)

# 6. Stop server
stop_playwright_server()

# 7. Return jobs
return jobs
```

## Conclusion

LinkedIn automation requires careful attention to rate limits, bot detection, and changing page structures. Always have fallback strategies (manual URLs, alternative sources) and respect the platform's terms of service.
