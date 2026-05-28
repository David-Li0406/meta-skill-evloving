# Ghost Cards Reference for Claude Code

## Overview

Ghost cards are special content blocks that provide rich functionality beyond basic HTML. They can be embedded in posts using HTML card wrappers or Lexical format. Cards enable interactive elements, media embeds, code highlighting, and custom layouts.

## Card Integration Methods

### Method 1: HTML Card Wrapper (Recommended for Claude Code)
```html
<!--kg-card-begin: CARD_TYPE-->
CARD_CONTENT
<!--kg-card-end: CARD_TYPE-->
```

### Method 2: JSON Card Data (for complex cards)
```html
<!--kg-card-begin: CARD_TYPE-->
{"property": "value", "anotherProperty": "value"}
<!--kg-card-end: CARD_TYPE-->
```

## Available Ghost Cards

### 1. HTML Card
**Purpose:** Custom HTML, styling, embeds, complex layouts
**Usage:** Any HTML that needs exact preservation

```html
<!--kg-card-begin: html-->
<div class="custom-container" style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
    <h3 style="color: #333; margin-top: 0;">Custom Styled Section</h3>
    <p>This HTML will be preserved <em>exactly</em> as written.</p>
    <ul style="color: #666;">
        <li>Custom CSS styling</li>
        <li>Complex layouts</li>
        <li>Embed codes</li>
    </ul>
</div>
<!--kg-card-end: html-->
```

### 2. Code Card
**Purpose:** Syntax-highlighted code blocks
**Usage:** Programming code, configuration files, command line examples

```html
<!--kg-card-begin: code-->
```javascript
// JavaScript example
const ghostAPI = {
    url: 'https://yoursite.com',
    key: 'your_api_key',
    version: 'v6.0'
};

async function createPost(title, content) {
    const response = await fetch(`${ghostAPI.url}/ghost/api/admin/posts/`, {
        method: 'POST',
        headers: {
            'Authorization': `Ghost ${generateJWT()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            posts: [{
                title: title,
                html: content,
                status: 'draft'
            }]
        })
    });
    return response.json();
}
```
<!--kg-card-end: code-->
```

**Multiple Language Examples:**
```html
<!--kg-card-begin: code-->
```python
# Python example
import requests
import jwt

def create_ghost_post(title, content):
    token = generate_jwt_token()
    headers = {
        'Authorization': f'Ghost {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'posts': [{
            'title': title,
            'html': content,
            'status': 'draft'
        }]
    }
    response = requests.post('https://yoursite.com/ghost/api/admin/posts/', 
                           headers=headers, json=data)
    return response.json()
```
<!--kg-card-end: code-->
```

### 3. Markdown Card
**Purpose:** Preserve exact Markdown formatting
**Usage:** When Markdown syntax needs to be maintained precisely

```html
<!--kg-card-begin: markdown-->
## Quick Reference Guide

### API Authentication
- **Token Required:** JWT generated from API key
- **Expiry:** 5 minutes maximum
- **Format:** `Authorization: Ghost {token}`

### Common Operations
1. **Create Post:** `POST /admin/posts/`
2. **Update Post:** `PUT /admin/posts/{id}/`
3. **Delete Post:** `DELETE /admin/posts/{id}/`

> **Important:** Always include `updated_at` when updating posts

### Code Example
```bash
curl -X POST \
  -H "Authorization: Ghost $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"posts":[{"title":"Test","status":"draft"}]}' \
  https://yoursite.com/ghost/api/admin/posts/
```

**Supported formats:** JSON, HTML, Lexical
<!--kg-card-end: markdown-->
```

### 4. Callout Card
**Purpose:** Highlighted notes, tips, warnings, important information
**Usage:** Draw attention to key points

```html
<!--kg-card-begin: callout-->
{"calloutEmoji": "💡", "calloutText": "Pro Tip: Always test API calls with draft posts first to avoid publishing mistakes."}
<!--kg-card-end: callout-->
```

**Different Callout Types:**
```html
<!-- Information -->
<!--kg-card-begin: callout-->
{"calloutEmoji": "ℹ️", "calloutText": "The Ghost Admin API uses JWT tokens that expire after 5 minutes."}
<!--kg-card-end: callout-->

<!-- Warning -->
<!--kg-card-begin: callout-->
{"calloutEmoji": "⚠️", "calloutText": "Never expose your API keys in client-side code or public repositories."}
<!--kg-card-end: callout-->

<!-- Success/Tip -->
<!--kg-card-begin: callout-->
{"calloutEmoji": "✅", "calloutText": "Your post was created successfully! You can now publish or schedule it."}
<!--kg-card-end: callout-->

<!-- Error/Danger -->
<!--kg-card-begin: callout-->
{"calloutEmoji": "🚨", "calloutText": "This action will permanently delete the post and cannot be undone."}
<!--kg-card-end: callout-->
```

### 5. Toggle Card
**Purpose:** Collapsible content sections, FAQ, detailed explanations
**Usage:** Hide/show additional information

```html
<!--kg-card-begin: toggle-->
{"toggleHeading": "How do I get my Ghost API key?", "toggleContent": "<p>To get your API key:</p><ol><li>Go to Ghost Admin dashboard</li><li>Navigate to <strong>Settings → Integrations</strong></li><li>Click <strong>Add custom integration</strong></li><li>Give it a name and save</li><li>Copy the <strong>Admin API Key</strong></li></ol><p>Keep this key secure and never share it publicly!</p>"}
<!--kg-card-end: toggle-->
```

**Complex Toggle Content:**
```html
<!--kg-card-begin: toggle-->
{"toggleHeading": "Troubleshooting API Errors", "toggleContent": "<h3>Common Issues</h3><h4>401 Unauthorized</h4><ul><li>JWT token expired (generate new one)</li><li>Invalid API key format</li><li>Missing Authorization header</li></ul><h4>422 Validation Error</h4><ul><li>Missing required fields (title)</li><li>Invalid JSON format</li><li>Malformed HTML content</li></ul><h4>409 Conflict</h4><ul><li>Outdated <code>updated_at</code> timestamp</li><li>Concurrent edits detected</li></ul><p><strong>Solution:</strong> Fetch latest post data before updating.</p>"}
<!--kg-card-end: toggle-->
```

### 6. Bookmark Card
**Purpose:** Rich link previews with thumbnails and descriptions
**Usage:** External resources, references, related content

```html
<!--kg-card-begin: bookmark-->
{"url": "https://docs.ghost.org/admin-api/", "title": "Ghost Admin API Documentation", "description": "Complete reference for Ghost's Admin API including authentication, endpoints, and examples.", "icon": "https://docs.ghost.org/favicon.ico", "thumbnail": "https://docs.ghost.org/images/meta/admin-api.png"}
<!--kg-card-end: bookmark-->
```

**Development Resources:**
```html
<!--kg-card-begin: bookmark-->
{"url": "https://github.com/TryGhost/Ghost", "title": "Ghost on GitHub", "description": "Open source headless CMS built on Node.js", "icon": "https://github.com/favicon.ico"}
<!--kg-card-end: bookmark-->
```

### 7. Button Card
**Purpose:** Call-to-action buttons, navigation, sign-ups
**Usage:** Drive user actions and engagement

```html
<!--kg-card-begin: button-->
{"buttonUrl": "https://yoursite.com/signup", "buttonText": "Get Started Free", "buttonAlignment": "center"}
<!--kg-card-end: button-->
```

**Different Button Styles:**
```html
<!-- Left aligned -->
<!--kg-card-begin: button-->
{"buttonUrl": "https://docs.yoursite.com", "buttonText": "View Documentation", "buttonAlignment": "left"}
<!--kg-card-end: button-->

<!-- Right aligned -->
<!--kg-card-begin: button-->
{"buttonUrl": "https://yoursite.com/contact", "buttonText": "Contact Support", "buttonAlignment": "right"}
<!--kg-card-end: button-->
```

### 8. Gallery Card
**Purpose:** Multiple images in a grid layout
**Usage:** Photo collections, before/after, step-by-step visuals

```html
<!--kg-card-begin: gallery-->
{"images": [
    {"src": "https://yoursite.com/images/step1.jpg", "alt": "Step 1: Setup", "caption": "Initial setup screen"},
    {"src": "https://yoursite.com/images/step2.jpg", "alt": "Step 2: Configure", "caption": "Configuration options"},
    {"src": "https://yoursite.com/images/step3.jpg", "alt": "Step 3: Deploy", "caption": "Deployment complete"}
]}
<!--kg-card-end: gallery-->
```

### 9. Image Card
**Purpose:** Single images with captions and links
**Usage:** Featured images, diagrams, screenshots

```html
<!--kg-card-begin: image-->
{"src": "https://yoursite.com/content/images/api-workflow.png", "alt": "Ghost API Workflow Diagram", "caption": "Complete workflow for creating posts via Ghost Admin API", "href": "https://yoursite.com/api-guide"}
<!--kg-card-end: image-->
```

### 10. Video Card
**Purpose:** Video embeds and uploads
**Usage:** Tutorials, demos, embedded content

```html
<!--kg-card-begin: video-->
{"src": "https://yoursite.com/content/video/api-tutorial.mp4", "caption": "How to use Ghost Admin API - Complete Tutorial", "loop": false, "muted": false}
<!--kg-card-end: video-->
```

**YouTube/Vimeo Embeds:**
```html
<!--kg-card-begin: embed-->
{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "html": "<iframe width='560' height='315' src='https://www.youtube.com/embed/dQw4w9WgXcQ' frameborder='0' allowfullscreen></iframe>", "type": "video"}
<!--kg-card-end: embed-->
```

## Practical Integration Examples

### Example 1: Technical Tutorial Post
```html
<p>Learn how to integrate with the Ghost Admin API step by step.</p>

<!--kg-card-begin: callout-->
{"calloutEmoji": "📋", "calloutText": "Prerequisites: Node.js installed, Ghost site with Admin access, API key generated"}
<!--kg-card-end: callout-->

<h2>Step 1: Authentication Setup</h2>
<p>First, let's set up JWT token generation:</p>

<!--kg-card-begin: code-->
```javascript
const jwt = require('jsonwebtoken');

function generateGhostToken(apiKey) {
    const [id, secret] = apiKey.split(':');
    const header = { alg: 'HS256', typ: 'JWT', kid: id };
    const payload = {
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + (5 * 60), // 5 minutes
        aud: '/admin/'
    };
    
    return jwt.sign(payload, Buffer.from(secret, 'hex'), { header });
}
```
<!--kg-card-end: code-->

<!--kg-card-begin: toggle-->
{"toggleHeading": "Why does the token expire so quickly?", "toggleContent": "<p>Ghost API tokens expire after 5 minutes for security reasons:</p><ul><li><strong>Reduced attack window:</strong> Limits exposure if token is compromised</li><li><strong>Forces fresh generation:</strong> Ensures you're always using valid tokens</li><li><strong>Best practice:</strong> Generate tokens just before API calls</li></ul><p>This is similar to how AWS and other secure APIs work.</p>"}
<!--kg-card-end: toggle-->

<h2>Step 2: Create Your First Post</h2>

<!--kg-card-begin: code-->
```bash
curl -X POST \
  -H "Authorization: Ghost $JWT_TOKEN" \
  -H "Accept-Version: v6.0" \
  -H "Content-Type: application/json" \
  -d '{
    "posts": [{
      "title": "My API-Created Post",
      "html": "<p>Hello from the API!</p>",
      "status": "draft"
    }]
  }' \
  https://yoursite.com/ghost/api/admin/posts/?source=html
```
<!--kg-card-end: code-->

<!--kg-card-begin: callout-->
{"calloutEmoji": "✅", "calloutText": "Success! Your post is now created as a draft. Check your Ghost admin to see it."}
<!--kg-card-end: callout-->

<!--kg-card-begin: bookmark-->
{"url": "https://docs.ghost.org/admin-api/", "title": "Ghost Admin API Reference", "description": "Complete API documentation with all endpoints and examples"}
<!--kg-card-end: bookmark-->

<!--kg-card-begin: button-->
{"buttonUrl": "https://yoursite.com/api-examples", "buttonText": "See More Examples", "buttonAlignment": "center"}
<!--kg-card-end: button-->
```

### Example 2: Resource Collection Post
```html
<p>Essential tools and resources for Ghost developers.</p>

<h2>Official Resources</h2>

<!--kg-card-begin: bookmark-->
{"url": "https://ghost.org/docs/", "title": "Ghost Documentation", "description": "Complete guides for users and developers"}
<!--kg-card-end: bookmark-->

<!--kg-card-begin: bookmark-->
{"url": "https://github.com/TryGhost/Ghost", "title": "Ghost on GitHub", "description": "Open source code and issue tracking"}
<!--kg-card-end: bookmark-->

<h2>Development Tools</h2>

<!--kg-card-begin: callout-->
{"calloutEmoji": "🛠️", "calloutText": "These tools will speed up your Ghost development workflow significantly."}
<!--kg-card-end: callout-->

<!--kg-card-begin: toggle-->
{"toggleHeading": "JavaScript Admin API Client", "toggleContent": "<p>Official JavaScript client for Ghost Admin API:</p><pre><code>npm install @tryghost/admin-api</code></pre><p>Handles JWT generation, authentication, and provides convenient methods for all API operations.</p>"}
<!--kg-card-end: toggle-->

<!--kg-card-begin: toggle-->
{"toggleHeading": "Postman Collection", "toggleContent": "<p>Pre-configured Postman collection with all Ghost API endpoints:</p><ul><li>Authentication examples</li><li>All CRUD operations</li><li>Error handling examples</li></ul><p>Perfect for testing and development.</p>"}
<!--kg-card-end: toggle-->
```

### Example 3: FAQ/Documentation Post
```html
<h1>Ghost API Frequently Asked Questions</h1>

<p>Common questions and solutions for Ghost API developers.</p>

<!--kg-card-begin: toggle-->
{"toggleHeading": "How do I handle authentication?", "toggleContent": "<p>Ghost uses JWT tokens for authentication:</p><ol><li>Generate JWT from your API key</li><li>Include in Authorization header</li><li>Token expires in 5 minutes</li><li>Generate fresh token for each request</li></ol><!--kg-card-begin: code-->```javascript\nconst token = generateJWT(apiKey);\nconst headers = {\n  'Authorization': `Ghost ${token}`,\n  'Content-Type': 'application/json'\n};\n```<!--kg-card-end: code-->"}
<!--kg-card-end: toggle-->

<!--kg-card-begin: toggle-->
{"toggleHeading": "What's the difference between HTML and Lexical?", "toggleContent": "<p><strong>Lexical</strong> (Ghost's native format):</p><ul><li>Full Ghost editor compatibility</li><li>All features supported</li><li>Complex JSON structure</li></ul><p><strong>HTML</strong> (converted to Lexical):</p><ul><li>Easy to generate programmatically</li><li>Some formatting may be lost</li><li>Use <code>?source=html</code> parameter</li></ul><p>For most use cases, HTML is sufficient and much easier to work with.</p>"}
<!--kg-card-end: toggle-->

<!--kg-card-begin: toggle-->
{"toggleHeading": "How do I upload images?", "toggleContent": "<p>Upload images using multipart form data:</p><!--kg-card-begin: code-->```bash\ncurl -X POST \\\n  -F 'file=@image.jpg' \\\n  -F 'purpose=image' \\\n  -H \"Authorization: Ghost $TOKEN\" \\\n  https://yoursite.com/ghost/api/admin/images/upload/\n```<!--kg-card-end: code--><p>Then use the returned URL in your post content.</p>"}
<!--kg-card-end: toggle-->
```

## API Integration Patterns

### Pattern 1: HTML with Embedded Cards
```json
{
  "posts": [{
    "title": "My Post with Cards",
    "html": "<p>Introduction paragraph.</p><!--kg-card-begin: callout-->{\"calloutEmoji\": \"💡\", \"calloutText\": \"This is important!\"}<!--kg-card-end: callout--><p>More content after the callout.</p>",
    "status": "draft"
  }]
}
```

### Pattern 2: Building Content Programmatically
```javascript
function buildPostContent(sections) {
    let content = '';
    
    sections.forEach(section => {
        switch(section.type) {
            case 'paragraph':
                content += `<p>${section.text}</p>`;
                break;
            case 'callout':
                content += `<!--kg-card-begin: callout-->{"calloutEmoji": "${section.emoji}", "calloutText": "${section.text}"}<!--kg-card-end: callout-->`;
                break;
            case 'code':
                content += `<!--kg-card-begin: code-->\`\`\`${section.language}\n${section.code}\n\`\`\`<!--kg-card-end: code-->`;
                break;
            case 'toggle':
                content += `<!--kg-card-begin: toggle-->{"toggleHeading": "${section.heading}", "toggleContent": "${section.content}"}<!--kg-card-end: toggle-->`;
                break;
        }
    });
    
    return content;
}

// Usage
const postSections = [
    { type: 'paragraph', text: 'Welcome to this tutorial.' },
    { type: 'callout', emoji: '📋', text: 'Prerequisites: Basic JavaScript knowledge' },
    { type: 'code', language: 'javascript', code: 'console.log("Hello, Ghost!");' }
];

const content = buildPostContent(postSections);
```

## Best Practices for Claude Code

### 1. Card Priority for API Usage
- **High Priority:** HTML, Code, Callout (cover 90% of use cases)
- **Medium Priority:** Toggle, Bookmark, Button (specific features)
- **Low Priority:** Gallery, Video, Image (media-heavy content)

### 2. Content Generation Strategy
```javascript
// Template approach for consistent card usage
const cardTemplates = {
    tip: (text) => `<!--kg-card-begin: callout-->{"calloutEmoji": "💡", "calloutText": "${text}"}<!--kg-card-end: callout-->`,
    warning: (text) => `<!--kg-card-begin: callout-->{"calloutEmoji": "⚠️", "calloutText": "${text}"}<!--kg-card-end: callout-->`,
    code: (lang, code) => `<!--kg-card-begin: code-->\`\`\`${lang}\n${code}\n\`\`\`<!--kg-card-end: code-->`,
    faq: (question, answer) => `<!--kg-card-begin: toggle-->{"toggleHeading": "${question}", "toggleContent": "${answer}"}<!--kg-card-end: toggle-->`
};
```

### 3. Error Prevention
- Escape quotes in JSON card data: `"` becomes `\"`
- Validate JSON structure before embedding
- Test cards in simple posts first
- Use HTML cards for complex custom content

### 4. Performance Considerations
- Don't overuse cards in a single post
- Limit toggle cards to prevent overwhelming readers
- Use appropriate card types (don't use HTML cards for simple text)
- Consider mobile rendering for complex cards

This reference covers all major Ghost cards and their implementation patterns for programmatic content creation.