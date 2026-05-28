# Articles and Tutorials Reference

Complete guide to creating DocC articles and interactive tutorials.

## Articles

### Basic Article Structure

```markdown
# Article Title

A one-sentence summary of the article.

## Overview

A longer introduction explaining what the reader will learn.

## Main Section

The primary content of the article.

### Subsection

More detailed content.

## Summary

Key takeaways from the article.

## See Also

- ``RelatedSymbol``
- <doc:RelatedArticle>
```

### Article with Rich Content

```markdown
# Building Custom Views

Learn how to create reusable SwiftUI views.

@Metadata {
    @PageKind(article)
    @PageColor(blue)
}

## Overview

This article teaches you how to build custom views
that follow SwiftUI best practices.

## Creating a Basic View

Start with a simple view structure:

```swift
struct CustomButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
        }
    }
}
```

> Tip: Keep views small and focused on a single responsibility.

## Adding Customization

Add modifiers for flexibility:

```swift
struct CustomButton: View {
    let title: String
    let style: ButtonStyle
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .foregroundColor(style.textColor)
                .padding()
                .background(style.backgroundColor)
                .cornerRadius(8)
        }
    }
}
```

> Important: Test your views with different Dynamic Type sizes.
```

## Tutorials

### Tutorial Table of Contents

Create `Table-of-Contents.tutorial`:

```markdown
@Tutorials(name: "My App Tutorials") {
    @Intro(title: "Meet My App") {
        Learn how to build amazing features with My App.

        @Image(source: "tutorials-hero.png", alt: "Tutorial hero image")
    }

    @Chapter(name: "Getting Started") {
        Set up your development environment and create your first project.

        @Image(source: "chapter1-hero.png", alt: "Getting started")

        @TutorialReference(tutorial: "doc:Creating-a-Project")
        @TutorialReference(tutorial: "doc:Building-the-UI")
    }

    @Chapter(name: "Advanced Features") {
        Learn advanced techniques for power users.

        @Image(source: "chapter2-hero.png", alt: "Advanced features")

        @TutorialReference(tutorial: "doc:Custom-Animations")
        @TutorialReference(tutorial: "doc:Performance-Optimization")
    }

    @Resources {
        Explore more resources for learning.

        @Documentation(destination: "https://developer.apple.com/documentation/swiftui") {
            Browse and search SwiftUI documentation.

            - [SwiftUI](https://developer.apple.com/documentation/swiftui)
        }

        @SampleCode(destination: "https://developer.apple.com/sample-code") {
            Download and explore sample projects.

            - [Sample Code](https://developer.apple.com/sample-code)
        }
    }
}
```

### Individual Tutorial

Create `Creating-a-Project.tutorial`:

```markdown
@Tutorial(time: 15) {
    @Intro(title: "Creating Your First Project") {
        Learn how to create a new project and set up the basic structure.

        @Image(source: "intro-image.png", alt: "Project setup")
    }

    @Section(title: "Create the Project") {
        @ContentAndMedia {
            First, you'll create a new Xcode project using the SwiftUI template.

            @Image(source: "section1-image.png", alt: "Xcode new project")
        }

        @Steps {
            @Step {
                Open Xcode and select **File > New > Project**.

                @Image(source: "step1.png", alt: "New project menu")
            }

            @Step {
                Select the **App** template and click **Next**.

                @Image(source: "step2.png", alt: "Template selection")
            }

            @Step {
                Enter your project name and select **SwiftUI** for the interface.

                @Code(name: "ContentView.swift", file: "Creating-01-ContentView.swift")
            }
        }
    }

    @Section(title: "Build the Interface") {
        @ContentAndMedia {
            Now you'll build the main user interface.

            @Image(source: "section2-image.png", alt: "Building interface")
        }

        @Steps {
            @Step {
                Open `ContentView.swift` and replace the placeholder content.

                @Code(name: "ContentView.swift", file: "Creating-02-ContentView.swift") {
                    @Image(source: "preview-1.png", alt: "Preview")
                }
            }

            @Step {
                Add a navigation stack to enable navigation.

                @Code(name: "ContentView.swift", file: "Creating-03-ContentView.swift") {
                    @Image(source: "preview-2.png", alt: "Preview with navigation")
                }
            }
        }
    }

    @Assessments {
        @MultipleChoice {
            What template should you use for a SwiftUI app?

            @Choice(isCorrect: false) {
                Document App

                @Justification(reaction: "Try again!") {
                    Document App is for document-based applications.
                }
            }

            @Choice(isCorrect: true) {
                App

                @Justification(reaction: "Correct!") {
                    The App template is the standard choice for SwiftUI apps.
                }
            }

            @Choice(isCorrect: false) {
                Game

                @Justification(reaction: "Try again!") {
                    Game template is for SpriteKit or SceneKit games.
                }
            }
        }
    }
}
```

### Tutorial Code Files

Store code snippets in separate files:

```
Documentation.docc/
└── Tutorials/
    └── Resources/
        ├── Creating-01-ContentView.swift
        ├── Creating-02-ContentView.swift
        └── Creating-03-ContentView.swift
```

Example code file (`Creating-01-ContentView.swift`):

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
    }
}

#Preview {
    ContentView()
}
```

## Callout Directives

### Note
```markdown
> Note: This is additional information.
```

### Tip
```markdown
> Tip: This is a helpful suggestion.
```

### Important
```markdown
> Important: This is critical information.
```

### Warning
```markdown
> Warning: Be careful with this action.
```

### Experiment
```markdown
> Experiment: Try modifying the code to see what happens.
```

## Cross-References

### Link to Article
```markdown
See <doc:GettingStarted> for setup instructions.
```

### Link to Tutorial
```markdown
Complete <doc:Creating-a-Project> first.
```

### Link to Symbol
```markdown
Use ``ContentViewModel`` to manage state.
```

### Link to External URL
```markdown
Visit [Apple Developer](https://developer.apple.com) for more.
```

## Best Practices

### Article Best Practices

1. **Start with a clear summary** - One sentence that explains the article
2. **Use progressive disclosure** - Start simple, add complexity
3. **Include code examples** - Show, don't just tell
4. **Add callouts** - Highlight important information
5. **Link related content** - Connect to symbols and other articles

### Tutorial Best Practices

1. **Set time expectations** - Use `@Tutorial(time: X)` accurately
2. **Provide visual feedback** - Include preview images for each step
3. **Keep steps atomic** - One action per step
4. **Test your code** - Ensure all code files compile
5. **Add assessments** - Reinforce learning with questions
