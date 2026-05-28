---
name: ai-blog-generation
description: Create high-quality, reader-first blog posts for SulitFinds that answer trending Filipino questions with affiliate monetization (default 3 affiliate links per post, 1 per product, collected from the user before insertion unless an exception is approved).
---

Use this skill when generating new blog posts or refreshing existing content.

Core philosophy:
- Reader-first: Every post must provide genuine value before any monetization consideration
- Quality over quantity: Fewer excellent posts beat many mediocre ones
- Answer real questions: Target what Filipinos are actually searching for
- Natural monetization: Include 3 product recommendations per post, 1 link per product, only when genuinely helpful. If a different count is needed, get explicit user approval.
- Always request affiliate links from the user before inserting any affiliate URLs.

Content tiers (choose based on topic depth):
- Pillar: Comprehensive guides (2,000+ words) for high-value topics
- Cluster: Standard posts (900-1,500 words) for focused topics
- Quick: Concise answers (500-900 words) for simple questions

Pre-generation requirements (MANDATORY):
1. Keyword research: Use the keyword-research skill to identify a valid topic
2. Topic registry check: Verify the topic is not already covered
3. Content tier decision: Choose Pillar, Cluster, or Quick based on topic depth
4. Value assessment: Confirm we can provide genuine, helpful content

Workflow options:

OPTION A: Content without product recommendations (exception only)
- For how-to guides, explainers, tips, and informational content where no product is genuinely helpful
- Ask the user to explicitly approve publishing without affiliate links before proceeding
- If the user wants product recommendations, switch to Option B and include a small, genuinely helpful recommendation section

OPTION B: Content with product recommendations (two-phase workflow)
- Phase 1: Product Plan (no blog content yet)
  - Propose the blog topic, target intent, and outline
  - Identify products that would genuinely help the reader (exactly 3 items unless the user approves a different count)
  - For each product, include:
    - Exact product name as it should appear in the article
    - Why it helps the reader (not just "it's available on Shopee")
    - Category tag
  - Ask the user to provide affiliate links for each recommended product
  - Stop after Phase 1 and wait for user confirmation/links
- Phase 2: Full Blog Generation (after user provides links)
  - Use only user-provided or user-confirmed links for affiliate URLs
  - Product name text must be the hyperlink
  - If any product is missing a link, either:
    - Downgrade to a mention (no link)
    - Remove from recommendations
  - Provide Affiliate Link Audit at end

Affiliate link request workflow:
- For every recommended product, present product name and reason for recommendation
- Ask: "Please provide the affiliate link for this product, or type SKIP to continue without it."
- Wait for user input before proceeding
- When content does not need product recommendations:
  - Ask the user to approve publishing without affiliate links or provide suitable products to recommend

Content quality guidelines:
- Answer the reader's question first, before any product mentions
- Provide genuine value even if the reader never clicks an affiliate link
- Do not force products into unrelated content
- Perform deep research using reputable sources
- Clearly separate verified facts from assumptions
- Do not claim personal testing or hands-on reviews
- Write clean, publication-ready copy
- Do not use em dashes or en dashes; use hyphen-minus or commas and periods

Copyright and asset usage:
- Do not use copyrighted images, text, or media without permission
- Do not copy content from brand sites, marketplaces, or other blogs
- All written content must be original and paraphrased properly
- Only use images that are public domain, CC0, or royalty-free
- Do not hotlink images from Shopee, TikTok Shop, or brand websites
- Prefer generic, non-branded visuals

Topic Registry (MANDATORY):
- Maintain at /docs/topic-registry.md
- For every published post, record:
  - Post title and slug
  - Primary search intent
  - Target keyword
  - Content tier (Pillar/Cluster/Quick)
  - Volume tier (High/Medium/Low/Emerging)
  - Core angle
  - Primary category
  - Key products mentioned (if any)
  - Status
- Update registry when new posts are generated

Pre-generation content scan (MANDATORY):
- Before generating, read the Topic Registry
- Compare proposed topic against existing entries
- Check for intent overlap, angle similarity, and audience match

Duplicate prevention rules:
- BLOCK generation if ALL are true:
  - Same primary intent as existing post
  - Same core angle
  - Value would be redundant
- ALLOW generation if ANY are true:
  - Different use case or audience
  - Different question being answered
  - Different comparison dimension
- Product reuse is allowed (same product in multiple posts)
- Duplicate blogs with same list and framing are not allowed

Content length rules:
- Pillar: 2,000+ words (comprehensive guides)
- Cluster: 900-1,500 words (focused topics)
- Quick: 500-900 words (simple answers)
- Do not pad with fluff; expand with useful sections if needed
- Word count for validation only; do not print in content

Affiliate integration rules (required per post unless user-approved exception):
- Default 3 affiliate links per post, one per product
- Exceeding 3 requires explicit user approval; if approved, stay under 6 per 1,000 words
- Link each product only once per article
- Product name text should be the hyperlink
- Use rel="sponsored noopener noreferrer" and target="_blank"
- Prefer placing links in dedicated recommendation sections
- Avoid mid-sentence links unless they add decision value
- Distinguish mentions (no link) from recommendations (link eligible)

Content integrity:
- Avoid turning posts into link farms
- Prefer one clear CTA block per recommendation section
- Never use urgency, fake scarcity, or deceptive language
- Do not promise earnings or guaranteed savings

Per-post affiliate disclosure: NOT required
- Site-wide Disclaimer page at /disclaimer handles this

Output requirements:
- Structured frontmatter: title, description, slug, date, category, tags
- Clear introduction, scannable headings, concise summaries
- Internal links to related posts when available
- Include Affiliate Link Audit (non-publishable) listing product, URL, section when links are used
- Accurate dates with "may change" disclaimer where applicable
- Provide a Facebook post script after the blog content:
  - Use the format below for readability:
    ```
    [Post Title]

    [2-4 sentence summary]

    Safety reminder: Do your own research and verify seller ratings and reviews.
    Liability note: Purchases are your responsibility.
    Read more: [PASTE LINK]
    ```

Cover image requirements:
- Every post must have a cover image in /public/images/
- Format: JPG or PNG only (no SVG)
- Ratio: 16:9 preferred
- Naming: cover-[topic-slug].jpg
- If no suitable image exists, note it and request user to provide one

New post checklist (after generation):
1. Verify content provides genuine value to the reader
2. Confirm 3 affiliate links are included (one per product), or the user approved a different count or exception
3. Confirm affiliate links are user-provided
4. Update topic-registry.md with new entries
5. Run sitemap regeneration: npm run generate:sitemap
6. Run sensitive data scan (required by copilot-instructions.md)
7. Provide a Facebook post script for the new blog

BEFORE PUSHING - Cover Image Reminder (MANDATORY):
- Stop and remind user to create cover images for all new posts
- For each post, provide:
  - Required filename: /public/images/[slug].jpg
  - Canva prompt suggestion: A simple, descriptive prompt for creating a copyright-safe cover image
  - Example: "Minimalist flat illustration of a home office desk with laptop, notebook, and coffee mug. Clean background, soft colors, 16:9 ratio."
- Canva prompt guidelines:
  - Use generic, non-branded visuals
  - Avoid logos, trademarks, or identifiable brand packaging
  - Suggest lifestyle or category illustrations over specific products
  - Specify 16:9 ratio in the prompt
- Wait for user confirmation that images are ready before proceeding to push

Pinterest Pin Reminder (MANDATORY):
- After generating a new post and receiving affiliate links, remind the user to create Pinterest pins
- For each new post, provide:
  - Pin title: Post title
  - Pin description: Post meta description
  - Pin URL: https://sulitfinds.com/blog/[slug]
  - Board: "Budget Finds Philippines" (or relevant board)
  - Suggested hashtags: 5-6 relevant tags based on post category and keywords
- Example output format:
  ```
  Pinterest Pin for: [Post Title]
  - Image: /public/images/[slug].jpg
  - Title: [Post Title]
  - Description: [Meta description]
  - URL: https://sulitfinds.com/blog/[slug]
  - Board: Budget Finds Philippines
  - Tags: #budgettips #philippines #[topic] #[category] #sulitfinds
  ```

Quality checks before publishing:
- Does the post answer the reader's question? (required)
- Would this post be valuable even without affiliate links? (required)
- Does the post include 3 affiliate links (one per product), or is there explicit approval for a different count or no links? (required)
- Clear introduction and scannable headings?
- Accurate information with sources?
- Unique title and compelling meta description?
- Natural keyword usage (not stuffed)?

Scope:
- Applies to new and refreshed blog posts
- Does not apply to About page, Disclaimer page, or UI copy
