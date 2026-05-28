# How to Use This Skill

Hey Claude—I just added the "github-stars-analyzer" skill. Can you analyze this GitHub repository and generate a research report?

## Example Invocations

**Example 1: Single Repository Analysis**
Hey Claude—I just added the "github-stars-analyzer" skill. Can you analyze the repository `anthropics/claude-code-skills-factory` and generate a star growth report?

**Example 2: Comparative Analysis**
Hey Claude—I just added the "github-stars-analyzer" skill. Can you compare the popularity of `facebook/react`, `vuejs/vue`, and `angular/angular` over the last 90 days?

**Example 3: Growth Tracking**
Hey Claude—I just added the "github-stars-analyzer" skill. Can you track star growth trends for the `microsoft` organization's repositories?

**Example 4: Research Report**
Hey Claude—I just added the "github-stars-analyzer" skill. Can you generate a comprehensive research report on `vercel/next.js` including growth projections and insights?

## What to Provide

- **Repository Information**: GitHub owner and repository name (e.g., `anthropics/claude-code-skills-factory`)
- **Analysis Period**: Optional time period in days (default: 30 days)
- **Output Format**: Preferred format (markdown, json, pdf)
- **Comparison Repositories**: Optional list of repositories for comparison
- **Visualizations**: Whether to include charts and graphs

## What You'll Get

- **Comprehensive Analysis**: Detailed metrics including stars, forks, issues, contributors
- **Growth Metrics**: Daily growth rates, projections, and trends
- **Comparative Insights**: Multi-repository comparisons and rankings
- **Research Report**: Professional report with executive summary and recommendations
- **Visualizations**: Charts and graphs (when requested)
- **Export Options**: Reports in Markdown, JSON, or PDF format

## Sample Input Formats

### Single Repository
```
{
  "repository": {
    "owner": "anthropics",
    "name": "claude-code-skills-factory",
    "analysis_period_days": 30
  }
}
```

### Multiple Repositories for Comparison
```
{
  "repository": {
    "owner": "facebook",
    "name": "react"
  },
  "comparison_repositories": [
    {
      "owner": "vuejs",
      "name": "vue"
    },
    {
      "owner": "angular",
      "name": "angular"
    }
  ]
}
```

### With Specific Output Requirements
```
{
  "repository": {
    "owner": "microsoft",
    "name": "vscode"
  },
  "output_formats": ["markdown", "json"],
  "include_visualizations": true,
  "generate_pdf": true
}
```

## Tips for Best Results

1. **Use Authenticated Access**: For higher rate limits, provide a GitHub personal access token
2. **Choose Appropriate Time Periods**: Use 30-90 days for meaningful growth analysis
3. **Compare Similar Repositories**: Compare repositories in the same domain/ecosystem
4. **Request Visualizations**: Charts help visualize trends and comparisons
5. **Export for Sharing**: Use PDF format for sharing reports with stakeholders

## Common Use Cases

- **Open Source Project Evaluation**: Assess popularity and health of potential dependencies
- **Competitive Analysis**: Compare your repository with competitors
- **Growth Tracking**: Monitor star growth trends over time
- **Investment Research**: Evaluate open source projects for investment decisions
- **Community Health**: Assess the health and sustainability of open source communities