---
name: audit-website
description: Use this skill to audit websites for SEO, technical, content, performance, and security issues using the squirrelscan CLI, providing actionable recommendations and health scores.
---

# Website Audit Skill

Audit websites for SEO, technical, content, performance, and security issues using the squirrelscan CLI.

squirrelscan provides a CLI tool `squirrel` - available for macOS, Windows, and Linux. It carries out extensive website auditing by emulating a browser, search crawler, and analyzing the website's structure and content against over 140+ rules.

It will provide you a list of issues as well as suggestions on how to fix them.

## Links 

* squirrelscan website is at [https://squirrelscan.com](https://squirrelscan.com)
* documentation (including rule references) are at [https://docs.squirrelscan.com](https://docs.squirrelscan.com)

You can look up the docs for any rule with this template:

```
https://docs.squirrelscan.com/rules/{rule_category}/{rule_id}
```

## What This Skill Does

This skill enables AI agents to audit websites for over 140 rules in 20 categories, including:

- **SEO issues**: Meta tags, titles, descriptions, canonical URLs, Open Graph tags
- **Technical problems**: Broken links, redirect chains, page speed, mobile-friendliness
- **Performance**: Page load time, resource usage, caching
- **Content quality**: Heading structure, image alt text, content analysis
- **Security**: Leaked secrets, HTTPS usage, security headers, mixed content
- **Accessibility**: Alt text, color contrast, keyboard navigation
- **Usability**: Form validation, error handling, user flow
- **Links**: Checks for broken internal and external links
- **E-E-A-T**: Expertise, Experience, Authority, Trustworthiness
- **User Experience**: User flow, error handling, form validation
- **Mobile**: Checks for mobile-friendliness, responsive design, touch-friendly elements
- **Crawlability**: Checks for crawlability, robots.txt, sitemap.xml, and more
- **Schema**: Schema.org markup, structured data, rich snippets
- **Legal**: Compliance with legal requirements, privacy policies, terms of service