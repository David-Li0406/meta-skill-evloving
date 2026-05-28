# DocC Catalog Structure Reference

Complete guide to organizing DocC documentation catalogs.

## Directory Structure

### Basic Structure

```
Sources/
└── MyTarget/
    ├── MyTarget.swift
    └── Documentation.docc/
        ├── Documentation.md        # Landing page (required)
        └── Resources/              # Images and media
            └── hero-image.png
```

### Full Structure

```
Documentation.docc/
├── Documentation.md                # Landing page
├── Articles/
│   ├── GettingStarted.md
│   ├── Architecture.md
│   └── BestPractices.md
├── Tutorials/
│   ├── Table-of-Contents.tutorial  # Tutorial overview
│   └── Chapter1/
│       ├── Creating-Your-First-App.tutorial
│       └── Adding-Features.tutorial
├── Extensions/
│   ├── MyClass.md                  # Symbol extensions
│   └── MyProtocol.md
└── Resources/
    ├── hero-image.png
    ├── architecture-diagram.png
    └── tutorial-step-1.png
```

## Landing Page (Documentation.md)

The landing page is required and must match your module name:

```markdown
# ``ModuleName``

A brief description of your module.

## Overview

A longer description explaining what the module does,
its main features, and when to use it.

![Hero image showing the module in action](hero-image)

## Featured

@Links(visualStyle: detailedGrid) {
    - <doc:GettingStarted>
    - <doc:Architecture>
}

## Topics

### Essentials

- <doc:GettingStarted>
- <doc:Configuration>

### Views

- ``ContentView``
- ``DetailView``
- ``SettingsView``

### View Models

- ``ContentViewModel``
- ``DetailViewModel``

### Models

- ``User``
- ``Item``
- ``Settings``

### Services

- ``NetworkService``
- ``StorageService``
```

## Symbol Extensions

Extend documentation for existing symbols:

```markdown
# ``MyClass``

@Metadata {
    @DocumentationExtension(mergeBehavior: append)
}

## Overview

Additional overview content that will be appended
to the symbol's existing documentation.

## Topics

### Additional Methods

- ``newMethod()``
- ``anotherMethod()``
```

## Directives Reference

### @Metadata

Configure page behavior:

```markdown
@Metadata {
    @TitleHeading("Getting Started")
    @PageKind(article)
    @PageColor(blue)
    @CallToAction(url: "https://example.com", purpose: link, label: "Learn More")
}
```

### @Options

Set display options:

```markdown
@Options(scope: local) {
    @AutomaticSeeAlso(disabled)
    @AutomaticTitleHeading(disabled)
    @AutomaticArticleSubheading(disabled)
}
```

### @Links

Create visual link grids:

```markdown
@Links(visualStyle: detailedGrid) {
    - <doc:Article1>
    - <doc:Article2>
    - <doc:Article3>
}

@Links(visualStyle: compactGrid) {
    - ``Symbol1``
    - ``Symbol2``
}

@Links(visualStyle: list) {
    - <doc:Topic1>
    - <doc:Topic2>
}
```

### @Image

Include images:

```markdown
@Image(source: "diagram.png", alt: "Architecture diagram")
```

### @Video

Include videos:

```markdown
@Video(source: "demo.mp4", poster: "demo-poster.png")
```

### @Row and @Column

Create layouts:

```markdown
@Row {
    @Column {
        First column content.
    }
    
    @Column {
        Second column content.
    }
}
```

### @TabNavigator

Create tabbed content:

```markdown
@TabNavigator {
    @Tab("Swift") {
        ```swift
        let x = 1
        ```
    }
    
    @Tab("Objective-C") {
        ```objc
        int x = 1;
        ```
    }
}
```

### @Small

Smaller text:

```markdown
@Small {
    Copyright 2024. All rights reserved.
}
```

## Articles

### Basic Article

```markdown
# Article Title

A brief summary of the article.

## Overview

Introduction to the topic.

## Section 1

Content for section 1.

### Subsection

More detailed content.

## Section 2

Content for section 2.

## See Also

- ``RelatedSymbol``
- <doc:RelatedArticle>
```

### Article with Metadata

```markdown
# Advanced Configuration

@Metadata {
    @PageKind(article)
    @PageColor(purple)
}

## Overview

This article covers advanced configuration options.
```

## Resource Management

### Supported Image Formats

- PNG (recommended for diagrams)
- JPEG (for photos)
- SVG (for scalable graphics)

### Image Naming Conventions

```
Resources/
├── hero-image.png           # Landing page hero
├── hero-image~dark.png      # Dark mode variant
├── step-1.png               # Tutorial step
├── step-1@2x.png            # Retina variant
└── architecture.svg         # Scalable diagram
```

### Referencing Resources

```markdown
![Alt text](image-name)           # Simple reference
![Alt text](image-name.png)       # With extension
@Image(source: "image.png", alt: "Description")  # Directive
```

## XcodeGen Integration

Add to `project.yml`:

```yaml
targets:
  MyApp:
    sources:
      - Sources/MyApp
      - path: Sources/MyApp/Documentation.docc
        type: folder
        buildPhase: none
```

## Common Patterns

### Module Overview Page

```markdown
# ``handheld``

@Metadata {
    @DisplayName("Handheld App")
}

Plan and navigate sightseeing trips with ease.

@Options(scope: global) {
    @AutomaticSeeAlso(enabled)
}

## Overview

handheld is an iOS application that helps users plan
optimal sightseeing routes using MapKit and SwiftUI.

## Topics

### Getting Started

- <doc:Installation>
- <doc:QuickStart>

### Core Features

- <doc:RoutePlanning>
- <doc:LookAround>
- <doc:FavoriteSpots>

### Architecture

- <doc:MVVMArchitecture>
- <doc:DataFlow>
```
