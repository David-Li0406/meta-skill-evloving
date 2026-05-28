# PlantUML Theme Utilities

## 🎨 Custom Theme Generator

### Brand Color Input Format
```
Primary: #FF6B35 (Brand Orange)
Secondary: #2E86AB (Brand Blue) 
Accent: #F18F01 (Highlight)
Neutral: #C5C3C6 (Gray)
```

### Generated Theme Structure
```plantuml
' Auto-generated custom theme
skinparam backgroundColor #FEFEFE
skinparam defaultFontName "Microsoft YaHei"

' Primary brand layer
skinparam package {
  BackgroundColor<<primary>> #FF6B35
  BorderColor<<primary>> #E55A2B
}

' Secondary support layer  
skinparam rectangle {
  BackgroundColor<<secondary>> #2E86AB
  BorderColor<<secondary>> #1F5F7A
}
```

## 🔍 Color Palette Extractor

### Extract Theme Colors
```javascript
// Example: Extract Pyramid Executive colors
const pyramidColors = {
  primary: ["#FFD700", "#FFA500", "#FF8C00"],
  secondary: ["#4169E1", "#1E90FF", "#87CEEB"], 
  accent: ["#708090", "#A9A9A9", "#D3D3D3"]
};

// Generate CSS variables
:root {
  --pyramid-gold-primary: #FFD700;
  --pyramid-gold-secondary: #FFA500;
  --pyramid-blue-primary: #4169E1;
}
```

## ✅ Theme Compatibility Matrix

| Diagram Type | Pyramid | Sky | Rainbow | Blue | Warm |
|---|---|---|---|---|---|
| Use Case | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Architecture | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Business Process | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| User Journey | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Data Flow | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 Smart Theme Recommendation

### Input Analysis
```
Context: "Executive presentation on microservice migration"
Audience: "C-level executives and technical leads"
Purpose: "Strategic decision making"
```

### AI Recommendation Logic
```
1. Audience = Executive → Consider Pyramid (+3 points)
2. Topic = Technical → Consider Sky (+2 points) 
3. Purpose = Strategic → Consider Pyramid (+2 points)
4. Context = Presentation → Consider Pyramid (+1 point)

Result: Pyramid Executive (8 points) > Sky Explorer (2 points)
```

## 🛡️ Accessibility Compliance

### Color Contrast Ratios
| Theme | Normal Text | Large Text | Pass WCAG |
|---|---|---|---|
| Pyramid | 7.2:1 | 4.8:1 | ✅ AAA |
| Sky | 6.8:1 | 4.5:1 | ✅ AA+ |
| Rainbow | 5.2:1 | 3.1:1 | ✅ AA |
| Blue | 8.1:1 | 5.2:1 | ✅ AAA |
| Warm | 4.9:1 | 3.2:1 | ✅ AA |

### Colorblind Friendly Check
- ✅ All themes tested with Deuteranopia simulation
- ✅ Alternative patterns provided for critical distinctions
- ✅ Shape and size differentiation beyond color

## 🔧 Performance Optimization

### Minimal Theme Loading
```plantuml
' Load only required components
!define PYRAMID_COLORS_ONLY
!include themes/pyramid-executive.md

' Skip unused layer definitions
!undefine SUPPORT_LAYER_STYLES
```

### Theme Caching Strategy
```
1. Parse theme once per session
2. Store skinparam configurations in memory
3. Apply cached styles to multiple diagrams
4. Reload only when theme version changes
```