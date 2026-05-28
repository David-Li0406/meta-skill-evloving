# LinkedIn Post Maker Skill

## Overview
The `linkedin-post-maker` skill automatically generates high-quality, engaging LinkedIn posts on any topic while maintaining professional standards and best practices.

## Features

- **Smart Clarification**: Asks targeted questions when topic details are vague or missing
- **Multi-Format Support**: Creates different post types (personal stories, educational content, thought leadership, etc.)
- **Professional Standards**: Follows LinkedIn best practices for formatting, engagement, and readability
- **Automatic Organization**: Saves all posts to `LinkedIn-Posts/` directory with proper naming
- **Comprehensive Templates**: Includes reference materials and templates for consistent quality

## How It Works

### Automatic Activation
Claude will automatically use this skill when you ask to:
- "Create a LinkedIn post about..."
- "Write a social media post for LinkedIn on..."
- "Generate LinkedIn content about..."
- "Help me write a professional post about..."

### The Workflow

1. **Information Gathering**: If your topic is vague or missing key details, Claude will ask clarifying questions about:
   - Target audience
   - Desired tone (professional, casual, inspirational, etc.)
   - Post length
   - Key message and takeaways
   - Call-to-action preferences

2. **Content Generation**: Creates a well-structured post with:
   - Attention-grabbing hook
   - Valuable content body
   - Clear takeaways
   - Engaging call-to-action
   - Relevant hashtags (3-5)

3. **File Organization**: Automatically saves the post to:
   ```
   LinkedIn-Posts/YYYY-MM-DD_topic-keywords.md
   ```

## File Structure

```
.claude/skills/linkedin-post-maker/
├── SKILL.md              # Main skill definition and instructions
├── BEST-PRACTICES.md     # LinkedIn best practices reference
├── POST-TEMPLATE.md      # Quick reference templates
└── README.md            # This file
```

## Usage Examples

### Simple Request
```
You: "Create a LinkedIn post about remote work benefits"

Claude: Will ask 1-2 clarifying questions about audience and tone,
        then generate a tailored post
```

### Detailed Request (No Questions Needed)
```
You: "Write a casual LinkedIn post for software developers about the
     importance of code reviews. Make it around 400 words with a
     conversational tone and ask them to share their experiences."

Claude: Proceeds directly to generate the post based on your specifications
```

### Vague Request (More Clarification)
```
You: "Make a post about technology"

Claude: Will ask about:
        - Specific technology topic/angle
        - Target audience
        - Main message
        Then generates the post
```

## Post Quality Standards

Every generated post includes:

✓ **Hook** - Attention-grabbing opening that stops scrolling
✓ **Value** - Clear insights, lessons, or actionable information
✓ **Structure** - Short paragraphs, visual breaks, scannable format
✓ **Engagement** - Call-to-action that encourages comments/discussion
✓ **Discoverability** - 3-5 relevant, strategic hashtags
✓ **Professional formatting** - Proper use of white space, bullets, emphasis

## Supporting Resources

### BEST-PRACTICES.md
Comprehensive reference including:
- Hook formulas that work
- Content types that perform well
- Hashtag strategy (3-5 rule)
- Engagement optimization tips
- Common mistakes to avoid
- Platform algorithm factors

### POST-TEMPLATE.md
Quick reference templates for:
- Personal stories
- Educational/tips posts
- Thought leadership
- List/framework posts
- Problem-solution format
- Short & punchy posts

## Post Output Format

Each saved post includes:

```markdown
# LinkedIn Post: [Topic Title]

**Date Created:** YYYY-MM-DD
**Target Audience:** [audience]
**Tone:** [style]
**Length:** [word count] words

---

## Post Content

[The actual LinkedIn post ready to copy and paste]

---

## Metadata
- Main Topic: [topic]
- Key Themes: [themes]
- Hashtags: [tags]
- Estimated Reading Time: [time]
```

## Customization

You can customize posts by specifying:
- **Tone**: Professional, Casual, Inspirational, Educational, Story-driven
- **Length**: Short (150-300 words), Medium (300-600), Long (600-1000)
- **Audience**: Developers, Entrepreneurs, Managers, Industry-specific
- **Style**: Personal story, How-to, Thought leadership, List format
- **CTA Type**: Question, Share request, Discussion prompt, Connection invite

## Tips for Best Results

1. **Be Specific**: The more context you provide, the better the output
2. **Know Your Audience**: Mention who you're targeting for tailored content
3. **Define Success**: Tell Claude what engagement you want (comments, shares, etc.)
4. **Iterate**: Ask for revisions if the first version isn't quite right
5. **Add Personal Touch**: Request personal anecdotes or specific examples to include

## Examples of Good Prompts

✓ "Create a LinkedIn post for CTOs about AI adoption challenges, professional tone, around 500 words"

✓ "Write an inspirational post about overcoming imposter syndrome for junior developers"

✓ "Generate a thought leadership post on the future of remote work, contrarian perspective"

✓ "Make a short, casual post about productivity tips for busy founders with a question CTA"

## Troubleshooting

**Claude isn't using the skill:**
- Make sure you mention "LinkedIn post" or "social media content"
- Be explicit: "Use the linkedin-post-maker skill to..."

**Too many questions:**
- Provide more details upfront about audience, tone, and topic specifics

**Post doesn't match expectations:**
- Ask for specific revisions: "Make it more casual" or "Add a personal story"
- Request a different template: "Rewrite using the list format"

## Version History
- v1.0.0 (2025-12-21): Initial release with core functionality

## Feedback and Improvements

As you use this skill, note what works well and what could be improved. The skill can be updated with:
- Additional templates
- New hook formulas
- Industry-specific guidance
- More examples
- Enhanced clarification questions

---

**Ready to create your first LinkedIn post?** Just ask Claude to create a LinkedIn post on your topic!
