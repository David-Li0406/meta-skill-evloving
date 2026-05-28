# Document-Based Apps Reference (macOS 14+)

Comprehensive guide to building document-based applications in macOS SwiftUI.

## FileDocument Protocol

### Basic Implementation

```swift
import SwiftUI
import UniformTypeIdentifiers

struct MyDocument: FileDocument {
    // Declare supported content types
    static var readableContentTypes: [UTType] { [.plainText] }

    // Document data
    var text: String

    // Initialize empty document
    init(text: String = "") {
        self.text = text
    }

    // Read from file
    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        self.text = string
    }

    // Write to file
    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        guard let data = text.data(using: .utf8) else {
            throw CocoaError(.fileWriteInapplicableStringEncoding)
        }
        return FileWrapper(regularFileWithContents: data)
    }
}
```

### DocumentGroup Scene

```swift
@main
struct MyApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MyDocument()) { file in
            ContentView(document: file.$document)
        }
    }
}
```

## Custom UTType

### Defining in Info.plist

Add to your app's Info.plist:

```xml
<key>UTExportedTypeDeclarations</key>
<array>
    <dict>
        <key>UTTypeConformsTo</key>
        <array>
            <string>public.data</string>
            <string>public.content</string>
        </array>
        <key>UTTypeDescription</key>
        <string>My Document</string>
        <key>UTTypeIdentifier</key>
        <string>com.example.mydocument</string>
        <key>UTTypeTagSpecification</key>
        <dict>
            <key>public.filename-extension</key>
            <array>
                <string>mydoc</string>
            </array>
        </dict>
    </dict>
</array>
```

### Declaring in Code

```swift
extension UTType {
    static var myDocument: UTType {
        UTType(exportedAs: "com.example.mydocument")
    }
}

struct MyDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.myDocument] }
    static var writableContentTypes: [UTType] { [.myDocument] }

    // ...
}
```

## Complex Document Types

### JSON Document

```swift
struct Project: Codable {
    var name: String
    var description: String
    var items: [Item]
    var createdAt: Date
    var modifiedAt: Date

    struct Item: Codable, Identifiable {
        let id: UUID
        var title: String
        var completed: Bool
    }
}

struct ProjectDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.json] }

    var project: Project

    init(project: Project = Project(
        name: "Untitled",
        description: "",
        items: [],
        createdAt: .now,
        modifiedAt: .now
    )) {
        self.project = project
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        project = try decoder.decode(Project.self, from: data)
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

        var updatedProject = project
        updatedProject.modifiedAt = .now

        let data = try encoder.encode(updatedProject)
        return FileWrapper(regularFileWithContents: data)
    }
}
```

### Binary Document with Package

```swift
struct PackageDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.package] }

    var content: Content
    var assets: [String: Data]

    init(configuration: ReadConfiguration) throws {
        guard let wrapper = configuration.file.fileWrappers else {
            throw CocoaError(.fileReadCorruptFile)
        }

        // Read main content
        guard let contentWrapper = wrapper["content.json"],
              let contentData = contentWrapper.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        content = try JSONDecoder().decode(Content.self, from: contentData)

        // Read assets
        assets = [:]
        if let assetsWrapper = wrapper["assets"]?.fileWrappers {
            for (name, wrapper) in assetsWrapper {
                if let data = wrapper.regularFileContents {
                    assets[name] = data
                }
            }
        }
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let package = FileWrapper(directoryWithFileWrappers: [:])

        // Write main content
        let contentData = try JSONEncoder().encode(content)
        package.addRegularFile(withContents: contentData, preferredFilename: "content.json")

        // Write assets
        let assetsWrapper = FileWrapper(directoryWithFileWrappers: [:])
        for (name, data) in assets {
            assetsWrapper.addRegularFile(withContents: data, preferredFilename: name)
        }
        package.addFileWrapper(assetsWrapper)

        return package
    }
}
```

## ReferenceFileDocument

For documents that need more control over saving:

```swift
class EditableDocument: ReferenceFileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    @Published var text: String

    init(text: String = "") {
        self.text = text
    }

    required init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        self.text = string
    }

    func snapshot(contentType: UTType) throws -> String {
        text
    }

    func fileWrapper(snapshot: String, configuration: WriteConfiguration) throws -> FileWrapper {
        guard let data = snapshot.data(using: .utf8) else {
            throw CocoaError(.fileWriteInapplicableStringEncoding)
        }
        return FileWrapper(regularFileWithContents: data)
    }
}
```

## Undo/Redo Support

### Using UndoManager

```swift
struct DocumentView: View {
    @Binding var document: MyDocument
    @Environment(\.undoManager) private var undoManager

    var body: some View {
        TextEditor(text: $document.text)
            .onChange(of: document.text) { oldValue, newValue in
                registerUndo(from: oldValue, to: newValue)
            }
    }

    private func registerUndo(from oldValue: String, to newValue: String) {
        guard oldValue != newValue else { return }

        undoManager?.registerUndo(withTarget: self) { _ in
            document.text = oldValue
        }
        undoManager?.setActionName("Typing")
    }
}
```

### Undo with Reference Document

```swift
class EditableDocument: ReferenceFileDocument {
    @Published var text: String {
        didSet {
            undoManager?.registerUndo(withTarget: self) { doc in
                doc.text = oldValue
            }
        }
    }

    var undoManager: UndoManager?
}

struct DocumentView: View {
    @ObservedObject var document: EditableDocument
    @Environment(\.undoManager) private var undoManager

    var body: some View {
        TextEditor(text: $document.text)
            .onAppear {
                document.undoManager = undoManager
            }
    }
}
```

## Document Commands

### Export Commands

```swift
struct DocumentCommands: Commands {
    @FocusedBinding(\.document) private var document

    var body: some Commands {
        CommandGroup(after: .saveItem) {
            Button("Export as PDF...") {
                exportAsPDF()
            }
            .keyboardShortcut("e", modifiers: [.command, .shift])
            .disabled(document == nil)

            Button("Export as HTML...") {
                exportAsHTML()
            }
            .disabled(document == nil)
        }
    }
}
```

### Recent Documents

macOS automatically manages recent documents for DocumentGroup apps.

## Auto-Save

Documents in SwiftUI auto-save by default. To customize:

```swift
struct MyDocument: FileDocument {
    // Return false to disable auto-save
    var hasUnsavedChanges: Bool { true }
}
```

## Document View Patterns

### With Inspector

```swift
struct DocumentView: View {
    @Binding var document: MyDocument
    @State private var showInspector = false

    var body: some View {
        HSplitView {
            // Main editor
            TextEditor(text: $document.text)
                .frame(minWidth: 400)

            // Inspector
            if showInspector {
                InspectorView(document: document)
                    .frame(width: 250)
            }
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    showInspector.toggle()
                } label: {
                    Label("Inspector", systemImage: "sidebar.trailing")
                }
            }
        }
    }
}
```

### With Navigation

```swift
struct ProjectDocumentView: View {
    @Binding var document: ProjectDocument

    var body: some View {
        NavigationSplitView {
            // Item list
            List($document.project.items) { $item in
                NavigationLink(value: item.id) {
                    ItemRow(item: item)
                }
            }
        } detail: {
            // Item detail
        }
    }
}
```

## Document Picker Integration

```swift
struct ContentView: View {
    @State private var showDocumentPicker = false
    @State private var selectedDocument: URL?

    var body: some View {
        Button("Open Document...") {
            showDocumentPicker = true
        }
        .fileImporter(
            isPresented: $showDocumentPicker,
            allowedContentTypes: [.plainText],
            allowsMultipleSelection: false
        ) { result in
            switch result {
            case .success(let urls):
                selectedDocument = urls.first
            case .failure(let error):
                print("Error: \(error)")
            }
        }
    }
}
```

## Document Export

```swift
struct ContentView: View {
    @State private var showExporter = false
    let document: MyDocument

    var body: some View {
        Button("Export...") {
            showExporter = true
        }
        .fileExporter(
            isPresented: $showExporter,
            document: document,
            contentType: .plainText,
            defaultFilename: "export.txt"
        ) { result in
            switch result {
            case .success(let url):
                print("Exported to: \(url)")
            case .failure(let error):
                print("Error: \(error)")
            }
        }
    }
}
```

## Best Practices

1. **Choose Appropriate Protocol** - FileDocument for value types, ReferenceFileDocument for classes
2. **Define Custom UTTypes** - For app-specific document formats
3. **Implement Undo/Redo** - Users expect this in document apps
4. **Handle Errors Gracefully** - Provide clear error messages
5. **Support Auto-Save** - Let the system handle saving when possible
6. **Use Codable** - For structured data in documents
7. **Consider Package Format** - For complex documents with multiple files
8. **Test with Large Files** - Ensure performance with real-world data

## Common UTTypes

| Type | UTType |
|------|--------|
| Plain Text | .plainText |
| Rich Text | .rtf |
| Markdown | .markdown |
| JSON | .json |
| XML | .xml |
| PDF | .pdf |
| Image | .image |
| PNG | .png |
| JPEG | .jpeg |
