// Document-Based macOS App (macOS 14+)
// Demonstrates FileDocument, DocumentGroup, and Undo/Redo

import SwiftUI
import UniformTypeIdentifiers

// MARK: - App Entry Point

@main
struct DocumentApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: TextDocument()) { file in
            TextDocumentView(document: file.$document)
        }
        .commands {
            DocumentCommands()
            TextFormattingCommands()
        }

        DocumentGroup(newDocument: MarkdownDocument()) { file in
            MarkdownDocumentView(document: file.$document)
        }
    }
}

// MARK: - Text Document

struct TextDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    var text: String
    var metadata: DocumentMetadata

    struct DocumentMetadata: Codable {
        var author: String
        var createdAt: Date
        var lastModified: Date

        static var new: DocumentMetadata {
            DocumentMetadata(
                author: NSFullUserName(),
                createdAt: .now,
                lastModified: .now
            )
        }
    }

    init(text: String = "") {
        self.text = text
        self.metadata = .new
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        self.text = string
        self.metadata = .new
        self.metadata.createdAt = configuration.file.fileAttributes[FileAttributeKey.creationDate] as? Date ?? .now
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        guard let data = text.data(using: .utf8) else {
            throw CocoaError(.fileWriteInapplicableStringEncoding)
        }
        return FileWrapper(regularFileWithContents: data)
    }
}

// MARK: - Text Document View

struct TextDocumentView: View {
    @Binding var document: TextDocument
    @State private var showInspector = false
    @FocusState private var isTextFieldFocused: Bool
    @Environment(\.undoManager) private var undoManager

    var body: some View {
        HSplitView {
            // Main editor
            TextEditor(text: $document.text)
                .font(.system(.body, design: .monospaced))
                .focused($isTextFieldFocused)
                .frame(minWidth: 400)
                .onChange(of: document.text) { oldValue, newValue in
                    registerUndo(from: oldValue, to: newValue)
                }

            // Inspector panel
            if showInspector {
                DocumentInspectorView(document: $document)
                    .frame(width: 250)
            }
        }
        .toolbar {
            ToolbarItemGroup(placement: .primaryAction) {
                Button {
                    showInspector.toggle()
                } label: {
                    Label("Inspector", systemImage: "sidebar.trailing")
                }
            }

            ToolbarItemGroup {
                Text("\(document.text.count) characters")
                    .foregroundStyle(.secondary)
                    .font(.caption)
            }
        }
        .focusedSceneValue(\.document, $document)
    }

    private func registerUndo(from oldValue: String, to newValue: String) {
        guard oldValue != newValue else { return }

        undoManager?.registerUndo(withTarget: document) { _ in
            document.text = oldValue
        }
        undoManager?.setActionName("Typing")

        document.metadata.lastModified = .now
    }
}

// MARK: - Document Inspector

struct DocumentInspectorView: View {
    @Binding var document: TextDocument

    var body: some View {
        Form {
            Section("Statistics") {
                LabeledContent("Characters", value: "\(document.text.count)")
                LabeledContent("Words", value: "\(wordCount)")
                LabeledContent("Lines", value: "\(lineCount)")
            }

            Section("Metadata") {
                LabeledContent("Author", value: document.metadata.author)
                LabeledContent("Created", value: document.metadata.createdAt.formatted())
                LabeledContent("Modified", value: document.metadata.lastModified.formatted())
            }
        }
        .formStyle(.grouped)
        .padding(.vertical)
    }

    private var wordCount: Int {
        document.text.split { $0.isWhitespace || $0.isNewline }.count
    }

    private var lineCount: Int {
        document.text.components(separatedBy: .newlines).count
    }
}

// MARK: - Markdown Document

struct MarkdownDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.markdown] }

    var content: String
    var title: String

    init(content: String = "", title: String = "Untitled") {
        self.content = content
        self.title = title
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        self.content = string

        // Extract title from first heading
        let lines = string.components(separatedBy: .newlines)
        if let firstHeading = lines.first(where: { $0.hasPrefix("# ") }) {
            self.title = String(firstHeading.dropFirst(2))
        } else {
            self.title = "Untitled"
        }
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        guard let data = content.data(using: .utf8) else {
            throw CocoaError(.fileWriteInapplicableStringEncoding)
        }
        return FileWrapper(regularFileWithContents: data)
    }
}

// MARK: - Markdown Document View

struct MarkdownDocumentView: View {
    @Binding var document: MarkdownDocument
    @State private var showPreview = true

    var body: some View {
        HSplitView {
            // Editor
            VStack(alignment: .leading, spacing: 0) {
                Text("Editor")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .padding(.horizontal)
                    .padding(.top, 8)

                TextEditor(text: $document.content)
                    .font(.system(.body, design: .monospaced))
            }
            .frame(minWidth: 300)

            // Preview
            if showPreview {
                VStack(alignment: .leading, spacing: 0) {
                    Text("Preview")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .padding(.horizontal)
                        .padding(.top, 8)

                    ScrollView {
                        MarkdownPreviewView(content: document.content)
                            .padding()
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
                .frame(minWidth: 300)
                .background(.background)
            }
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Toggle(isOn: $showPreview) {
                    Label("Preview", systemImage: "eye")
                }
            }
        }
        .navigationTitle(document.title)
    }
}

// MARK: - Markdown Preview (Simple Implementation)

struct MarkdownPreviewView: View {
    let content: String

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            ForEach(Array(content.components(separatedBy: .newlines).enumerated()), id: \.offset) { _, line in
                renderLine(line)
            }
        }
    }

    @ViewBuilder
    private func renderLine(_ line: String) -> some View {
        if line.hasPrefix("# ") {
            Text(line.dropFirst(2))
                .font(.title)
                .fontWeight(.bold)
        } else if line.hasPrefix("## ") {
            Text(line.dropFirst(3))
                .font(.title2)
                .fontWeight(.semibold)
        } else if line.hasPrefix("### ") {
            Text(line.dropFirst(4))
                .font(.title3)
                .fontWeight(.medium)
        } else if line.hasPrefix("- ") || line.hasPrefix("* ") {
            HStack(alignment: .top, spacing: 8) {
                Text("\u{2022}")
                Text(line.dropFirst(2))
            }
        } else if line.hasPrefix("> ") {
            Text(line.dropFirst(2))
                .foregroundStyle(.secondary)
                .padding(.leading)
                .overlay(alignment: .leading) {
                    Rectangle()
                        .fill(.secondary)
                        .frame(width: 3)
                }
        } else if line.hasPrefix("```") {
            // Code block marker - simplified
            EmptyView()
        } else if !line.isEmpty {
            Text(line)
        } else {
            Spacer()
                .frame(height: 8)
        }
    }
}

// MARK: - Document Commands

struct DocumentCommands: Commands {
    @FocusedBinding(\.document) private var document: TextDocument?

    var body: some Commands {
        CommandGroup(after: .saveItem) {
            Button("Export as PDF...") {
                // Export functionality
            }
            .keyboardShortcut("e", modifiers: [.command, .shift])
            .disabled(document == nil)
        }
    }
}

// MARK: - Text Formatting Commands

struct TextFormattingCommands: Commands {
    var body: some Commands {
        CommandMenu("Format") {
            Button("Bold") {
                // Apply bold
            }
            .keyboardShortcut("b", modifiers: .command)

            Button("Italic") {
                // Apply italic
            }
            .keyboardShortcut("i", modifiers: .command)

            Button("Underline") {
                // Apply underline
            }
            .keyboardShortcut("u", modifiers: .command)

            Divider()

            Button("Increase Font Size") {
                // Increase size
            }
            .keyboardShortcut("+", modifiers: .command)

            Button("Decrease Font Size") {
                // Decrease size
            }
            .keyboardShortcut("-", modifiers: .command)
        }
    }
}

// MARK: - Focused Values

struct FocusedDocumentKey: FocusedValueKey {
    typealias Value = Binding<TextDocument>
}

extension FocusedValues {
    var document: Binding<TextDocument>? {
        get { self[FocusedDocumentKey.self] }
        set { self[FocusedDocumentKey.self] = newValue }
    }
}

// MARK: - UTType Extension

extension UTType {
    static var markdown: UTType {
        UTType(importedAs: "net.daringfireball.markdown")
    }
}

// MARK: - Preview

#Preview("Text Editor") {
    TextDocumentView(document: .constant(TextDocument(text: "Hello, World!\n\nThis is a sample document.")))
        .frame(width: 800, height: 600)
}

#Preview("Markdown Editor") {
    MarkdownDocumentView(document: .constant(MarkdownDocument(
        content: """
        # Welcome

        This is a **markdown** document.

        ## Features

        - Easy to write
        - Preview support
        - Cross-platform

        > This is a quote

        ### Code

        ```swift
        let hello = "world"
        ```
        """,
        title: "Welcome"
    )))
    .frame(width: 900, height: 600)
}
