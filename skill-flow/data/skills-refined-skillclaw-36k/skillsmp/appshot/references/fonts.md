# Embedded Fonts

10 font families bundled with appshot, always available without system installation.

## Modern UI Fonts

| Font | Variants | Best For |
|------|----------|----------|
| **Inter** | Regular, Bold, Italic, Bold Italic | Clean, modern interfaces |
| **Poppins** | Regular, Bold, Italic, Bold Italic | Friendly, geometric headings |
| **Montserrat** | Regular, Bold, Italic, Bold Italic | Professional, versatile |
| **DM Sans** | Regular | Modern, geometric |

## Web-Safe Fonts

| Font | Variants | Best For |
|------|----------|----------|
| **Roboto** | Regular, Bold, Italic, Bold Italic | Android-style, neutral |
| **Open Sans** | Regular | Highly readable body text |
| **Lato** | Regular, Bold, Italic, Bold Italic | Warm, humanist sans-serif |
| **Work Sans** | Regular | Modern web typography |

## Monospace Fonts

| Font | Variants | Best For |
|------|----------|----------|
| **JetBrains Mono** | Regular, Bold, Italic, Bold Italic | Code, technical apps |
| **Fira Code** | Regular, Bold | Code with ligatures |

## Font Recommendations by App Type

| App Category | Recommended Font |
|--------------|------------------|
| Finance/Business | Inter, Montserrat |
| Social/Lifestyle | Poppins, Lato |
| Productivity | Open Sans, Work Sans |
| Developer Tools | JetBrains Mono, Fira Code |
| Health/Fitness | Roboto, DM Sans |

## Usage

List embedded fonts:
```
appshot_fonts with action: "embedded"
```

Validate a font:
```
appshot_fonts with action: "validate", font: "Inter"
```

Configure font in project:
```
appshot_config with device: "iphone", font: "Montserrat Bold"
```
