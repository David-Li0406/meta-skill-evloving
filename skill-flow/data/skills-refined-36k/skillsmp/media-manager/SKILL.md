---
name: media-manager
description: Manage campaign media assets including images, tokens, and file organization
license: MIT
compatibility: opencode
metadata:
  audience: campaign-managers
  workflow: jekyll
---

## What I do
- Organize and rename campaign image assets following naming conventions
- Generate placeholder character tokens for new NPCs and enemies
- Validate that all referenced images exist and are properly formatted
- Create optimized versions of images for web display
- Generate image reference reports and missing asset lists

## When to use me
Use this when:
- Adding new character or faction images to the campaign
- Creating character tokens for new NPCs or enemies
- Organizing campaign media assets systematically
- Verifying that all image references are functional
- Preparing assets for site publication

## Usage Examples

### Token Generation
```
/skill({ name: "media-manager" })
Operation: Generate token
Character: Marla Mossfur
Style: Campaign standard (rounded, 200x200px)
Output: assets/images/MarlaMossfur_Token.png
```

### Asset Organization
```
/skill({ name: "media-manager" })
Operation: Organize assets
Source: Uploads folder (mixed formats)
Target: assets/images/ organized by type
Actions: Rename, resize, categorize, generate references
```

### Reference Validation
```
/skill({ name: "media-manager" })
Operation: Check references
Scope: All campaign articles
Report: Missing images, broken links, optimization suggestions
```

## Asset Types and Standards

### Character Tokens
- **Format**: PNG with transparency
- **Size**: 200x200px for campaign standard
- **Naming**: `CharacterName_Token.png` (CamelCase)
- **Style**: Rounded corners, drop shadow optional
- **Background**: Transparent or campaign color

### Faction Symbols
- **Format**: SVG or PNG
- **Size**: 100x100px for icons
- **Naming**: `FactionName_Symbol.svg`
- **Style**: Simplified, recognizable silhouette
- **Color**: Faction-specific color palette

### Location Images
- **Format**: WebP or JPEG
- **Size**: Optimized for web (max 800px width)
- **Naming**: `LocationName_View.jpg` (e.g., `NorthernClearing_Wide.jpg`)
- **Quality**: High resolution with compression
- **Orientation**: Landscape for scenes, portrait for important locations

### Document Screenshots
- **Format**: PNG
- **Size**: Full resolution with text readability
- **Naming**: `DocumentName_Screenshot.png`
- **Content**: Important campaign documents or maps
- **Annotations**: Redacted or highlighted key information

## Asset Organization

### Directory Structure
```
assets/
├── images/
│   ├── tokens/          # Character and enemy tokens
│   ├── factions/        # Faction symbols and icons
│   ├── locations/       # Scene and location images
│   ├── documents/       # Document screenshots and maps
│   └── misc/           # Other campaign assets
```

### File Naming Conventions
- **Tokens**: `CharacterName_Token.png`
- **Factions**: `FactionName_Symbol.svg`
- **Locations**: `LocationName_Description.jpg`
- **Documents**: `DocumentName_Type.png`
- **Generic**: `Category_Description.png`

## Image Operations

### Token Creation
1. Generate base token shape (circle or rounded square)
2. Add character silhouette or iconic feature
3. Apply campaign color scheme
4. Add subtle effects (shadow, glow, etc.)
5. Optimize for web display
6. Save in multiple sizes if needed

### Asset Optimization
1. Compress images without quality loss
2. Generate multiple formats for different uses
3. Create responsive versions for mobile devices
4. Generate WebP versions for modern browsers
5. Maintain original high-resolution versions

### Reference Management
1. Scan all campaign files for image references
2. Check that referenced files exist in correct locations
3. Validate file extensions and path formats
4. Update broken references with correct paths
5. Generate missing image lists for creation

## Quality Assurance

### Image Validation
- File format and compatibility checking
- Size and dimension verification
- Color profile and transparency validation
- Loading time and performance testing
- Accessibility compliance (alt text references)

### Consistency Checking
- Visual style consistency across tokens
- Color scheme alignment with campaign theme
- Naming convention compliance
- Reference format validation
- Size and proportion standardization

## Reports Generated

### Asset Inventory
- Complete list of campaign media assets
- Categorization by type and usage
- File sizes and optimization status
- Missing asset recommendations
- Duplicate detection and cleanup suggestions

### Reference Analysis
- Images referenced in campaign content
- Broken or missing image reports
- Optimization opportunities
- Usage frequency and importance ranking
- Asset organization recommendations

### Creation Recommendations
- Missing character tokens to generate
- Faction symbols needing creation
- Location images that would enhance content
- Document screenshots for plot points
- Asset improvement suggestions

## Media Workflow Integration

### Content Creation
- Generate placeholder tokens for new articles
- Create asset reference templates
- Suggest image additions based on content
- Maintain consistent visual style
- Optimize images for site performance

### Publication Preparation
- Validate all image references before site build
- Generate compressed versions for deployment
- Create responsive image sets
- Check licensing and attribution
- Generate media manifest for version control

Ask clarifying questions about:
- Preferred visual style for character tokens
- Color scheme requirements for faction symbols
- Image resolution and quality preferences
- Naming convention customization needs
- How to handle missing or broken references
- Whether to generate placeholder assets automatically