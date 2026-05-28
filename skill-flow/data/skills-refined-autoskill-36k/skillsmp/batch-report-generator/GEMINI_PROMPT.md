# Gemini Deep Research Prompt

Copy and paste this into Gemini for Deep Research.

---

## PROMPT TO COPY:

```
Find the top 10 most viral disinformation topics currently spreading across InfoWars, Breitbart, X (Twitter), Reddit, Facebook, Truth Social, Telegram, and TikTok.

For each topic, research a fact-check and return:
- 15+ primary sources (NO Wikipedia)
- A summary of why it's false/misleading

Return your research as JSON in this exact format:

{
  "reports": [
    {
      "slug": "topic-name-2025",
      "title": "Full Title of the Claim",
      "verdict": "FALSE",
      "claim": "One sentence: what was claimed",
      "claimant": "Who made/spread the claim",
      "date": "January 2025",
      "category": "Category Name",
      "sources": [
        {
          "title": "Source Article Title",
          "url": "https://full-url.com/article",
          "quote": "Key quote from the source..."
        }
      ],
      "context": "3 sentences explaining why this verdict was reached."
    }
  ]
}

Categories to use: U.S. Politics & Policy, Health & Medical, AI & Deepfakes, Immigration & Border, International Affairs, Economic Claims, Conspiracy & Hoaxes, Platform & Tech, Media & Journalism

Verdicts to use: FALSE, MISLEADING, MIXED, CONTEXT NEEDED

IMPORTANT:
- 15+ sources per topic (NO Wikipedia)
- Include fact-checker sources (PolitiFact, Snopes, FactCheck.org)
- Quotes must be verbatim from sources
- URLs must be valid and accessible
- Slug format: lowercase-with-dashes-2025
```

---

## After Gemini Research

1. Copy Gemini's JSON output
2. Run `/batch-report` in Claude Code
3. Paste the JSON
4. Reports generate automatically

---

## Variations

**Regional focus:**
```
Find the top 10 most viral disinformation topics about [AFRICA/INDIA/EUROPE/etc] spreading across...
```

**Topic focus:**
```
Find the top 10 most viral disinformation topics about [VACCINES/ELECTIONS/AI/etc] spreading across...
```

**Time-bound:**
```
Find the top 10 most viral disinformation topics from [THIS WEEK/JANUARY 2025/etc] spreading across...
```
