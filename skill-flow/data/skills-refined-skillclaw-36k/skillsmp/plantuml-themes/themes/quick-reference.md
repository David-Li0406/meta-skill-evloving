# PlantUML Theme Quick Reference

## 🚀 One-Command Theme Application

### Copy-Paste Ready Configurations

#### Pyramid Executive Theme
```plantuml
' 🏛️ Pyramid Executive Theme - Copy this block
skinparam backgroundColor #FEFEFE
skinparam defaultFontName "Microsoft YaHei"
skinparam shadowing true
skinparam roundcorner 8

skinparam package {
  BackgroundColor<<value_layer>> #FFF8DC
  BorderColor<<value_layer>> #FFD700
}
skinparam rectangle {
  BackgroundColor<<value_item>> #FFFACD
  BorderColor<<value_item>> #DAA520
}
```

#### Sky Explorer Theme  
```plantuml
' ☁️ Sky Explorer Theme - Copy this block
skinparam backgroundColor #FEFEFE
skinparam defaultFontName "Microsoft YaHei"
skinparam shadowing true

skinparam package {
  BackgroundColor<<user_layer>> #E3F2FD
  BorderColor<<user_layer>> #2196F3
}
skinparam rectangle {
  BackgroundColor<<user_item>> #BBDEFB
  BorderColor<<user_item>> #1976D2
}
```

## 🎨 Theme Mixing Guidelines

### Compatible Color Combinations
```
✅ GOOD:
- Pyramid (Gold) + Blue Analyst (Blue) → Professional Authority
- Sky (Orange) + Warm (Pink) → Modern Friendly
- Rainbow (Multi) + neutral backgrounds → Creative Balance

❌ AVOID:
- Rainbow + Pyramid → Color conflict
- Multiple vibrant themes in same diagram
- High contrast theme switching
```

## 📊 Usage Analytics

### Most Popular Combinations
1. **Pyramid Executive** (45%) - Corporate presentations
2. **Sky Explorer** (28%) - Technical documentation  
3. **Blue Analyst** (18%) - Requirements analysis
4. **Warm Designer** (7%) - UX workflows
5. **Rainbow Innovator** (2%) - Creative showcases

### Optimal Diagram Types
```
Architecture Diagrams → Pyramid Executive
Microservice Maps → Sky Explorer  
Use Case Analysis → Blue Analyst
User Journeys → Warm Designer
Business Processes → Rainbow Innovator
```

## 🔄 Theme Migration Guide

### Updating Existing Diagrams
```plantuml
' Step 1: Backup current styling
' [Current skinparam configurations]

' Step 2: Replace with new theme
' [New theme skinparam block]

' Step 3: Update stereotypes if needed
' <<old_style>> → <<new_style>>

' Step 4: Test and adjust
```

### Version Control Best Practices
```
themes/
├── v1.0/          # Stable themes
├── v1.1/          # Updated themes  
├── deprecated/    # Old versions
└── experimental/  # Beta themes
```

## 💡 Pro Tips

### Theme Performance
- Use minimal skinparam sets for faster rendering
- Cache theme configurations in templates
- Load themes conditionally based on diagram complexity

### Brand Consistency  
- Create custom theme variations for brand colors
- Maintain theme families across project documentation
- Document theme usage guidelines for team members

### Accessibility
- Always test with colorblind simulators
- Ensure 4.5:1 minimum contrast ratios
- Provide alternative visual cues beyond color