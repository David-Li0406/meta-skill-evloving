---
name: meme-generation
description: Use this skill to generate memes using the memegen.link API when users request humor, visual aids for social media, or engaging content.
---

# Meme Generation with Memegen.link

This skill enables the creation of memes using the free and open-source memegen.link API, supporting over 100 popular templates with custom text and styling options.

## Quick Reference

**Basic Meme Structure:**
```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.{extension}
```

**Example:**
```
https://api.memegen.link/images/buzz/memes/memes_everywhere.png
```

## Text Formatting

| Character | Encoding |
|-----------|----------|
| Space | `_` or `-` |
| Newline | `~n` |
| Question mark | `~q` |
| Percent | `~p` |
| Slash | `~s` |
| Hash | `~h` |
| Single quote | `''` |
| Double quote | `""` |

## Popular Templates

| Template | Use Case | Example |
|----------|----------|---------|
| `buzz` | X, X everywhere | bugs/bugs_everywhere |
| `drake` | Comparisons | manual_testing/automated_testing |
| `success` | Victories | deployed/no_errors |
| `fine` | Things going wrong | server_on_fire/this_is_fine |
| `fry` | Uncertainty | not_sure_if_bug/or_feature |
| `changemind` | Hot takes | tabs_are_better_than_spaces |
| `distracted` | Priorities | my_code/new_framework/current_project |
| `mordor` | One does not simply | one_does_not_simply/deploy_on_friday |

## Advanced Features

### Image Formats

| Extension | Use Case |
|-----------|----------|
| `.png` | Best quality, default |
| `.jpg` | Smaller file size |
| `.webp` | Modern, good compression |
| `.gif` | Animated templates |

### Dimensions

Control dimensions with:
```
?width=800
?height=600
```

### Layout Options

Control text positioning with:
```
?layout=top     # Text at top only
?layout=bottom  # Text at bottom only
?layout=default # Standard top/bottom
```

### Custom Images

Use any image as background:
```
?style=https://example.com/image.jpg
```

## Workflow Integration

### Generating Memes in Response

When a user requests a meme or you want to add humor:
```markdown
Here's a relevant meme about your situation:

![Meme](https://api.memegen.link/images/buzz/bugs/bugs_everywhere.png)
```

### Dynamic Meme Generation

Generate memes based on context:
```python
def generate_status_meme(status: str, message: str):
    template_map = {
        "success": "success",
        "failure": "fine",
        "review": "fry",
        "deploy": "interesting"
    }

    template = template_map.get(status, "buzz")
    top_text = message.split()[0:3]  # First 3 words
    bottom_text = message.split()[3:6]  # Next 3 words

    top = "_".join(top_text)
    bottom = "_".join(bottom_text)

    return f"https://api.memegen.link/images/{template}/{top}/{bottom}.png"
```

## Best Practices

1. **Keep Text Concise**: Aim for 2-6 words per line.
2. **Choose Appropriate Templates**: Match the template to your message.
3. **Consider Context**: Know your audience and keep it professional when necessary.
4. **Optimize for Platform**: Use dimensions suitable for the intended platform.
5. **Test Your URLs**: Preview memes before sharing.

## Error Handling

If a meme URL doesn't work:
1. Check the template name at `https://api.memegen.link/templates/`.
2. Verify text formatting (underscores for spaces).
3. Check for special characters that need encoding.
4. Ensure the extension is valid (.png, .jpg, etc.).
5. Test in a browser before sharing.

## Summary

The memegen.link API is a powerful tool for generating contextual memes. Use it to add humor to conversations, create visual aids for social media, and communicate complex ideas simply. Remember: A good meme is concise, relevant, and uses the right template for the message.