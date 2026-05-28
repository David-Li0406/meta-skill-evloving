# McKinsey Design System Reference

Complete design specifications for McKinsey/BCG-style presentations.

## Color Palette

| Color Type | Hex Code | Usage |
|------------|----------|-------|
| Primary Background | `#FFFFFF` | Slide background |
| Header Background | `#000000` | Title bars |
| Primary Accent | `#F85d42` | Key highlights, CTAs |
| Secondary Accent | `#74788d` | Supporting text |
| Deep Blue | `#556EE6` | Charts, data points |
| Green | `#34c38f` | Success indicators |
| Blue | `#50a5f1` | Neutral emphasis |
| Yellow | `#f1b44c` | Warnings, notes |

## Typography Specifications

- **Title**: 48-64px, Bold, Black (`#000000`)
- **Subtitle**: 28-36px, Bold, Accent Color
- **Body**: 16-20px, Regular, Dark Gray (`#333333`)
- **Chart Labels**: 12-14px, Clear, Readable

## Layout Standards

- **Padding**: 40-60px on all slides
- **Element Spacing**: 20-30px between components
- **Two-column Gap**: 30-40px
- **Chart Container**: min-height 400px

## Responsive Breakpoints

- **Desktop**: 1200px+ (full layout)
- **Tablet**: 768px-1199px (adjusted spacing)
- **Mobile**: <768px (single column)

## Design Principles

1. **Modern Business Style**: Clean, professional, minimal clutter
2. **Visual Hierarchy**: Clear distinction between titles, subtitles, and body
3. **Consistency**: Uniform design language across all slides
4. **Data-Driven**: Use charts and visualizations for quantitative information
5. **White Space**: Generous spacing for readability

## CSS Variables Template

```css
:root {
    --primary-background: #FFFFFF;
    --header-background: #000000;
    --primary-accent: #F85d42;
    --secondary-accent: #74788d;
    --deep-blue: #556EE6;
    --green: #34c38f;
    --blue: #50a5f1;
    --yellow: #f1b44c;
    --text-dark: #333333;
    --text-black: #000000;
    --text-light: #FFFFFF;
}
```

## Component Styling Guidelines

### Slide Title
- Font-size: 48-64px
- Font-weight: bold
- Color: `#000000`
- Margin-bottom: 30px

### Slide Subtitle
- Font-size: 28-36px
- Font-weight: bold
- Color: `#F85d42` or `#556EE6`
- Margin-bottom: 20px

### Text Content
- Font-size: 16-20px- Line-height: 1.6
- Color: `#333333`
- Max-width: 800px for readability

### Bullet Lists
- Bullet color: `#F85d42`
- Item spacing: 15px
- Indent: 20px

### Charts
- Background: transparent or white
- Border: none or 1px solid `#e0e0e0`
- Padding: 20px
- Border-radius: 8px (optional)

### Emphasis Boxes
- Background: `#f8f9fa`
- Border-left: 4px so5d42`
- Padding: 20px
- Margin: 20px 0

## Animation Standards

- **Fade-in Duration**: 0.6s
- **Slide Transition**: 0.3s ease
- **Hover Effects**: 0.2s ease
- **Easing Function**: ease-in-out

## Navigation Elements

- **Button Background**: `#F85d42`
- **Button Hover**: `#d64a35`
- **Button Text**: `#FFFFFF`
- **Button Padding**: 12px 24px
- **Button Border-radius**: 6px
