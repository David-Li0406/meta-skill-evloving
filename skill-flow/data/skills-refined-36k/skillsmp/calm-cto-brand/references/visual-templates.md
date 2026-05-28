# Visual Templates

Ready-to-use HTML templates for image generation. All templates use WCAG AA compliant colours.

## Base HTML Structure

All templates start with this wrapper:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Caveat:wght@400;500&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'DM Sans', sans-serif;
      width: 1200px;
      height: 630px;
    }
  </style>
</head>
<body>
  <!-- Template content here -->
</body>
</html>
```

---

## 1. Process Flow

Linear progression through 2-4 steps. Uses Sage → Coral → Sky colour sequence.

```html
<div style="
  background: #F8F6F3;
  width: 1200px;
  height: 630px;
  padding: 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Title -->
  <h1 style="
    font-size: 28px;
    font-weight: 700;
    color: #2D3436;
    text-align: center;
    margin: 24px 0;
    letter-spacing: -0.5px;
  ">[TITLE]</h1>

  <!-- Flow -->
  <div style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 24px;
    flex: 1;
  ">
    <div style="background: #5F8A5A; color: white; padding: 24px 36px; border-radius: 12px; text-align: center;">
      <div style="font-size: 18px; font-weight: 600;">[Step 1]</div>
      <div style="font-size: 13px; opacity: 0.9; margin-top: 4px;">[Subtitle]</div>
    </div>

    <span style="color: #D4C5B5; font-size: 28px;">→</span>

    <div style="background: #C4716A; color: white; padding: 24px 36px; border-radius: 12px; text-align: center;">
      <div style="font-size: 18px; font-weight: 600;">[Step 2]</div>
      <div style="font-size: 13px; opacity: 0.9; margin-top: 4px;">[Subtitle]</div>
    </div>

    <span style="color: #D4C5B5; font-size: 28px;">→</span>

    <div style="background: #4A8FA0; color: white; padding: 24px 36px; border-radius: 12px; text-align: center;">
      <div style="font-size: 18px; font-weight: 600;">[Step 3]</div>
      <div style="font-size: 13px; opacity: 0.9; margin-top: 4px;">[Subtitle]</div>
    </div>
  </div>

  <!-- Annotation -->
  <div style="font-family: 'Caveat', cursive; font-size: 20px; color: #57606A; text-align: center;">
    [Annotation]
  </div>
</div>
```

---

## 2. Quote Card

Statement with attribution. Use for beliefs, principles, memorable lines.

```html
<div style="
  background: linear-gradient(135deg, #5F8A5A 0%, #4A7548 100%);
  width: 1200px;
  height: 630px;
  padding: 56px 48px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
">
  <!-- Decorative Quote -->
  <div style="
    position: absolute;
    top: -30px;
    left: 20px;
    font-size: 250px;
    font-family: Georgia, serif;
    color: rgba(255,255,255,0.1);
    line-height: 1;
  ">"</div>

  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px; position: relative; z-index: 1;">
    <div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.8); letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Quote -->
  <div style="margin: auto 0; position: relative; z-index: 1;">
    <p style="
      font-size: 32px;
      font-weight: 600;
      color: white;
      line-height: 1.35;
      letter-spacing: -0.3px;
      max-width: 700px;
    ">[Quote text here]</p>

    <div style="font-size: 14px; color: rgba(255,255,255,0.75); margin-top: 24px;">
      — On [topic]
    </div>
  </div>
</div>
```

---

## 3. Concept Grid

2-4 related concepts in a grid layout.

```html
<div style="
  background: #F8F6F3;
  width: 1200px;
  height: 630px;
  padding: 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Title -->
  <h1 style="font-size: 28px; font-weight: 700; color: #2D3436; text-align: center; margin: 24px 0; letter-spacing: -0.5px;">
    [TITLE]
  </h1>

  <!-- Grid -->
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; flex: 1; align-content: center;">
    <div style="background: #5F8A5A; color: white; padding: 24px; border-radius: 12px; text-align: center;">
      <div style="font-size: 28px; margin-bottom: 8px;">[emoji]</div>
      <div style="font-size: 18px; font-weight: 600;">[Concept 1]</div>
      <div style="font-size: 13px; opacity: 0.85; margin-top: 4px;">[Description]</div>
    </div>

    <div style="background: #C4716A; color: white; padding: 24px; border-radius: 12px; text-align: center;">
      <div style="font-size: 28px; margin-bottom: 8px;">[emoji]</div>
      <div style="font-size: 18px; font-weight: 600;">[Concept 2]</div>
      <div style="font-size: 13px; opacity: 0.85; margin-top: 4px;">[Description]</div>
    </div>

    <div style="background: #4A8FA0; color: white; padding: 24px; border-radius: 12px; text-align: center;">
      <div style="font-size: 28px; margin-bottom: 8px;">[emoji]</div>
      <div style="font-size: 18px; font-weight: 600;">[Concept 3]</div>
      <div style="font-size: 13px; opacity: 0.85; margin-top: 4px;">[Description]</div>
    </div>
  </div>

  <!-- Annotation -->
  <div style="font-family: 'Caveat', cursive; font-size: 20px; color: #57606A; text-align: center;">
    [Annotation]
  </div>
</div>
```

---

## 4. Comparison (Before/After or Vs)

Side-by-side comparison of two states or options.

```html
<div style="
  background: #F8F6F3;
  width: 1200px;
  height: 630px;
  padding: 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Title -->
  <h1 style="font-size: 28px; font-weight: 700; color: #2D3436; text-align: center; margin: 24px 0; letter-spacing: -0.5px;">
    [TITLE]
  </h1>

  <!-- Comparison -->
  <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 24px; flex: 1; align-items: center;">
    <!-- Left (Before/Bad) -->
    <div style="background: white; border: 2px solid #E5E7EB; padding: 32px; border-radius: 12px;">
      <div style="font-size: 14px; font-weight: 600; color: #C4716A; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;">
        [BEFORE / WITHOUT]
      </div>
      <ul style="list-style: none; font-size: 16px; color: #4B5563; line-height: 2;">
        <li>✗ [Point 1]</li>
        <li>✗ [Point 2]</li>
        <li>✗ [Point 3]</li>
      </ul>
    </div>

    <!-- Arrow -->
    <div style="font-size: 32px; color: #D4C5B5;">→</div>

    <!-- Right (After/Good) -->
    <div style="background: white; border: 2px solid #5F8A5A; padding: 32px; border-radius: 12px;">
      <div style="font-size: 14px; font-weight: 600; color: #5F8A5A; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;">
        [AFTER / WITH]
      </div>
      <ul style="list-style: none; font-size: 16px; color: #4B5563; line-height: 2;">
        <li>✓ [Point 1]</li>
        <li>✓ [Point 2]</li>
        <li>✓ [Point 3]</li>
      </ul>
    </div>
  </div>
</div>
```

---

## 5. Stats Card

Big numbers with supporting context. Dark background.

```html
<div style="
  background: #2D3436;
  width: 1200px;
  height: 630px;
  padding: 56px 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #9CA3AF; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Title -->
  <h1 style="font-size: 24px; font-weight: 700; color: white; margin: 24px 0; letter-spacing: -0.5px;">
    [TITLE]
  </h1>

  <!-- Stats Grid -->
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; flex: 1; align-content: center;">
    <div style="text-align: center;">
      <div style="font-size: 64px; font-weight: 700; color: #8FAE8B; line-height: 1;">[XX]</div>
      <div style="font-size: 14px; color: #9CA3AF; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">[Label]</div>
    </div>

    <div style="text-align: center;">
      <div style="font-size: 64px; font-weight: 700; color: #E8998D; line-height: 1;">[XX]</div>
      <div style="font-size: 14px; color: #9CA3AF; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">[Label]</div>
    </div>

    <div style="text-align: center;">
      <div style="font-size: 64px; font-weight: 700; color: #89B9C4; line-height: 1;">[XX]</div>
      <div style="font-size: 14px; color: #9CA3AF; margin-top: 8px; text-transform: uppercase; letter-spacing: 1px;">[Label]</div>
    </div>
  </div>

  <!-- Source -->
  <div style="font-size: 12px; color: #6B7280; text-align: center;">
    [Source or context]
  </div>
</div>
```

---

## 6. Timeline

Chronological steps with time indicators.

```html
<div style="
  background: #F8F6F3;
  width: 1200px;
  height: 630px;
  padding: 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Title -->
  <h1 style="font-size: 24px; font-weight: 700; color: #2D3436; text-align: center; margin: 24px 0;">
    [TITLE]
  </h1>

  <!-- Timeline -->
  <div style="display: flex; align-items: center; justify-content: center; gap: 8px; flex: 1;">
    <div style="text-align: center;">
      <div style="background: #5F8A5A; color: white; padding: 20px 32px; border-radius: 8px; font-size: 16px; font-weight: 500;">
        [Step 1]
      </div>
      <div style="font-family: 'Caveat', cursive; font-size: 18px; color: #57606A; margin-top: 12px;">[time]</div>
    </div>

    <div style="width: 48px; height: 2px; background: #D4C5B5;"></div>

    <div style="text-align: center;">
      <div style="background: #C4716A; color: white; padding: 20px 32px; border-radius: 8px; font-size: 16px; font-weight: 500;">
        [Step 2]
      </div>
      <div style="font-family: 'Caveat', cursive; font-size: 18px; color: #57606A; margin-top: 12px;">[time]</div>
    </div>

    <div style="width: 48px; height: 2px; background: #D4C5B5;"></div>

    <div style="text-align: center;">
      <div style="background: #4A8FA0; color: white; padding: 20px 32px; border-radius: 8px; font-size: 16px; font-weight: 500;">
        [Step 3]
      </div>
      <div style="font-family: 'Caveat', cursive; font-size: 18px; color: #57606A; margin-top: 12px;">[time]</div>
    </div>
  </div>

  <!-- Annotation -->
  <div style="font-family: 'Caveat', cursive; font-size: 20px; color: #57606A; text-align: center;">
    [Annotation]
  </div>
</div>
```

---

## 7. List Card

Checklist or bullet points.

```html
<div style="
  background: white;
  border: 1px solid #E5E7EB;
  width: 1200px;
  height: 630px;
  padding: 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Title -->
  <h1 style="font-size: 32px; font-weight: 700; color: #2D3436; margin: 24px 0; letter-spacing: -0.5px;">
    [TITLE]
  </h1>

  <!-- List -->
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px 48px; flex: 1; align-content: center;">
    <div style="display: flex; align-items: flex-start; gap: 12px;">
      <div style="width: 24px; height: 24px; background: #5F8A5A; border-radius: 6px; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">✓</div>
      <span style="font-size: 18px; color: #2D3436;">[Item 1]</span>
    </div>

    <div style="display: flex; align-items: flex-start; gap: 12px;">
      <div style="width: 24px; height: 24px; background: #5F8A5A; border-radius: 6px; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">✓</div>
      <span style="font-size: 18px; color: #2D3436;">[Item 2]</span>
    </div>

    <div style="display: flex; align-items: flex-start; gap: 12px;">
      <div style="width: 24px; height: 24px; background: #5F8A5A; border-radius: 6px; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">✓</div>
      <span style="font-size: 18px; color: #2D3436;">[Item 3]</span>
    </div>

    <div style="display: flex; align-items: flex-start; gap: 12px;">
      <div style="width: 24px; height: 24px; background: #5F8A5A; border-radius: 6px; color: white; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">✓</div>
      <span style="font-size: 18px; color: #2D3436;">[Item 4]</span>
    </div>
  </div>

  <!-- Footer -->
  <div style="font-family: 'Caveat', cursive; font-size: 20px; color: #57606A; text-align: center;">
    [Annotation]
  </div>
</div>
```

---

## 8. Social Text Post

Text-focused for LinkedIn/Twitter. No diagrams, just words.

```html
<div style="
  background: #F8F6F3;
  width: 1200px;
  height: 630px;
  padding: 56px 64px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #6B7280; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Main Text -->
  <div style="margin: auto 0;">
    <p style="
      font-size: 36px;
      font-weight: 700;
      color: #2D3436;
      line-height: 1.3;
      letter-spacing: -0.5px;
      max-width: 900px;
    ">[Main statement or hook goes here. Keep it punchy and memorable.]</p>
  </div>

  <!-- Tags -->
  <div style="display: flex; gap: 12px;">
    <span style="background: #5F8A5A; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">[Tag]</span>
    <span style="background: rgba(0,0,0,0.05); color: #6B7280; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">nicalpi.com</span>
  </div>
</div>
```

---

## 9. Bold Statement (Dark)

Provocative headline with highlighted phrase.

```html
<div style="
  background: #2D3436;
  width: 1200px;
  height: 630px;
  padding: 56px 48px;
  display: flex;
  flex-direction: column;
">
  <!-- Brand Mark -->
  <div style="display: flex; align-items: center; gap: 8px;">
    <div style="width: 8px; height: 8px; background: #8FAE8B; border-radius: 50%;"></div>
    <span style="font-size: 12px; font-weight: 500; color: #9CA3AF; letter-spacing: 0.5px;">THE CALM CTO</span>
  </div>

  <!-- Statement -->
  <div style="margin: auto 0;">
    <h1 style="
      font-size: 42px;
      font-weight: 700;
      color: white;
      line-height: 1.15;
      letter-spacing: -0.5px;
    ">
      [First line of statement]<br>
      <span style="color: #E8998D;">[Highlighted phrase]</span>
    </h1>

    <p style="font-size: 18px; color: #9CA3AF; margin-top: 16px; max-width: 600px;">
      [Optional subtitle or context]
    </p>
  </div>

  <!-- Tags -->
  <div style="display: flex; gap: 12px;">
    <span style="background: #5F8A5A; color: white; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;">[Tag]</span>
  </div>
</div>
```
