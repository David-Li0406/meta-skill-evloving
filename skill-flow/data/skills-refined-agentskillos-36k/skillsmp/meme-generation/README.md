# Meme Generation Skill

Generate relevant memes using the [memegen.link](https://memegen.link) API.

## What is this?

This skill enables Claude Code to generate memes using the free and open-source memegen.link API. Perfect for adding humor to conversations, creating social media content, or making technical discussions more engaging.

**📚 New:** Check out the [Complete Markdown Memes Guide](complete-markdown-memes-guide.md) for comprehensive coverage of both **textual meme formats** (greentext, copypasta, ASCII art, chat logs, etc.) and **image memes** via URL.

## Quick Start

### Basic Usage

Simply ask Claude to create a meme:
- "Create a meme about bugs everywhere"
- "Generate a Drake meme comparing manual vs automated testing"
- "Make a success kid meme about passing tests"

### Example

```
User: "Create a meme about our deployment going smoothly"

Claude: "Here's a relevant meme:

![Deployment Success](https://api.memegen.link/images/success/deployed_to_production/no_errors.png)
```

## Features

- 100+ popular meme templates
- Custom text (top and bottom)
- Multiple image formats (PNG, JPG, WebP, GIF)
- Custom dimensions for social media
- No API key required (free and open-source)
- Custom backgrounds and styling

## Popular Templates

| Template | Use Case | Example |
|----------|----------|---------|
| `buzz` | X, X everywhere | Bugs, features, PRs |
| `drake` | Comparing two options | Old way vs new way |
| `success` | Celebrating wins | Tests passing, deployments |
| `fine` | Things going wrong | Production fires, incidents |
| `fry` | Uncertainty | Not sure if bug or feature |
| `changemind` | Controversial opinions | Tech debates |
| `distracted` | Priorities | Shiny new framework vs current work |

## URL Structure

```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.{extension}
```

**Example:**
```
https://api.memegen.link/images/buzz/memes/memes_everywhere.png
```

### Text Formatting

- Use `_` or `-` for spaces
- Use `~n` for newlines
- Keep text concise (2-6 words per line)

## Resources

- **Interactive Docs**: https://api.memegen.link/docs/
- **All Templates**: https://api.memegen.link/templates/
- **Fonts**: https://api.memegen.link/fonts/
- **GitHub**: https://github.com/jacebrowning/memegen

## Helper Script

The included `meme_generator.py` script provides a Python interface:

```python
from meme_generator import MemeGenerator

meme = MemeGenerator()

# Generate a basic meme
url = meme.generate("buzz", "features", "features everywhere")
print(url)

# Generate with options
url = meme.generate(
    template="drake",
    top="manual testing",
    bottom="automated testing",
    width=1200,
    height=630
)
print(url)

# Get random template suggestion
template = meme.suggest_template_for_context("deployment success")
print(template)
```

## Use Cases

### Code Reviews
```
https://api.memegen.link/images/fry/not_sure_if_bug/or_feature.png
```

### Successful Deployments
```
https://api.memegen.link/images/success/deployed_to_production/zero_errors.png
```

### Performance Issues
```
https://api.memegen.link/images/fine/server_load_at_100~/this_is_fine.png
```

### Documentation
```
https://api.memegen.link/images/yodawg/yo_dawg_i_heard_you_like_docs/so_i_documented_your_docs.png
```

## Tips

1. **Match context** - Choose templates that fit the situation
2. **Keep it concise** - Short text works best
3. **Be relevant** - Connect memes to current conversation
4. **Know your audience** - Keep it professional when needed
5. **Test first** - Preview URLs before sharing

## Examples for Egregora

Since this project deals with WhatsApp message processing and LLM content generation:

```python
# Privacy/Anonymization
https://api.memegen.link/images/buzz/pii/pii_everywhere.png

# Data Processing
https://api.memegen.link/images/yodawg/yo_dawg_i_parsed_your_messages/so_you_can_read_while_you_read.png

# LLM Content
https://api.memegen.link/images/fry/not_sure_if_ai_generated/or_human_written.png

# Success Stories
https://api.memegen.link/images/success/all_pii_removed/zero_leaks.png
```

## Contributing

To add more templates or improve the skill:
1. Check the latest templates at https://api.memegen.link/templates/
2. Update SKILL.md with new examples
3. Test URLs before committing
4. Keep documentation clear and concise

## License

This skill uses the free and open-source memegen.link API. No API key or authentication required.

The memegen API is maintained by [Jace Browning](https://github.com/jacebrowning/memegen).
