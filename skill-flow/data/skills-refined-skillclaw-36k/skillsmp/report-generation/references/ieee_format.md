# IEEE Citation Format Reference

Complete guide to IEEE citation formatting for project planning reports.

## In-Text Citation Rules

### Basic Format
- Use square brackets: `[1]`, `[2]`, etc.
- Numbers assigned in order of first appearance
- Same source = same number throughout document

### Citation Placement
- Place before punctuation: `...demonstrated this [1].`
- Multiple citations: `[1], [2]` or `[1, 2]` or `[1]-[3]`
- Space before bracket: `text [1]` not `text[1]`

### Examples
```
The study shows significant results [1].
Multiple sources confirm this [1], [2], [5].
A range of studies support this claim [1]-[4].
As noted in [1], the approach is effective.
```

## Reference List Format

### General Structure
```
[N] Author(s), "Title," Source, additional info, Date. [Online]. Available: URL
```

### Author Formatting
| Scenario | Format | Example |
|----------|--------|---------|
| Single author | F. Lastname | J. Smith |
| Two authors | F. Last and F. Last | J. Smith and M. Jones |
| Three authors | F. Last, F. Last, and F. Last | J. Smith, M. Jones, and R. Lee |
| Four+ authors | F. Last et al. | J. Smith et al. |
| Organization | Full name | Microsoft Research |

### Date Formatting
- Full date: `15-Mar.-2024`
- Month-year: `Mar. 2024`
- Year only: `2024`
- No date: `n.d.`

### Month Abbreviations
| Month | Abbrev. | Month | Abbrev. |
|-------|---------|-------|---------|
| January | Jan. | July | Jul. |
| February | Feb. | August | Aug. |
| March | Mar. | September | Sep. |
| April | Apr. | October | Oct. |
| May | May | November | Nov. |
| June | Jun. | December | Dec. |

## Reference Types

### Website / Online Article
```
[1] A. Smith, "Article title," Website Name, 15-Mar.-2024. [Online].
    Available: https://example.com/article
```

**With no author:**
```
[2] "Article title," Website Name, 2024. [Online].
    Available: https://example.com/article
```

**With access date (only if no publication date):**
```
[3] A. Smith, "Article title," Website Name. [Online].
    Available: https://example.com/article. [Accessed: 15-Mar.-2024].
```

### Journal Article
```
[4] M. Smith and J. Jones, "Article title here," Journal Name,
    vol. 12, no. 3, pp. 45-67, Mar. 2024, doi: 10.1234/example.
```

### Conference Paper
```
[5] R. Lee, "Paper title," in Proc. IEEE Int. Conf. Example,
    City, Country, 2024, pp. 100-105.
```

### Book
```
[6] A. Author, Book Title, 3rd ed. City, State: Publisher, 2024.
```

### Technical Report
```
[7] A. Smith, "Report title," Company/Institution, City, State,
    Rep. ABC-123, 2024.
```

### GitHub Repository
```
[8] Username, "Repository name," GitHub, 2024. [Online].
    Available: https://github.com/user/repo
```

### Blog Post
```
[9] A. Smith, "Blog post title," Blog Name, 15-Mar.-2024. [Online].
    Available: https://blog.example.com/post
```

## Common Sources for Project Planning

### Cloud Provider Documentation
```
[10] Amazon Web Services, "AWS Lambda documentation," AWS, 2024. [Online].
     Available: https://docs.aws.amazon.com/lambda/
```

### API Documentation
```
[11] Stripe, "Stripe API reference," Stripe Documentation, 2024. [Online].
     Available: https://stripe.com/docs/api
```

### Technology Comparison
```
[12] ThoughtWorks, "Technology Radar," ThoughtWorks, Apr. 2024. [Online].
     Available: https://www.thoughtworks.com/radar
```

### Industry Report
```
[13] Gartner, "Magic Quadrant for Cloud Infrastructure,"
     Gartner Research, Rep. G00123456, Oct. 2024.
```

## Quality Guidelines

### What Makes a Good Citation
1. **Authoritative source** - Prefer official documentation, peer-reviewed papers
2. **Recent** - Prioritize 2020-2026 publications for technology topics
3. **Accessible** - URL should be publicly accessible
4. **Complete** - Include all available metadata (author, date, title)

### Source Hierarchy (Most to Least Authoritative)
1. Official documentation (AWS, Google Cloud, etc.)
2. Peer-reviewed papers (IEEE, ACM, Nature)
3. Industry reports (Gartner, Forrester, McKinsey)
4. Reputable tech blogs (AWS Blog, Google Cloud Blog)
5. Community resources (Stack Overflow, Medium)

### When to Cite
- Statistics and market data
- Technology comparisons
- Best practices claims
- Architecture patterns
- Security recommendations
- Performance benchmarks

### When NOT to Cite
- Common knowledge ("APIs use HTTP")
- Your own analysis and recommendations
- General project management practices
- Self-evident conclusions
