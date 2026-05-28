# Drag & Drop / Pasteboard Reference (macOS 14+)

Comprehensive guide to implementing drag and drop and pasteboard operations in macOS SwiftUI.

## Transferable Protocol

### Basic Transferable

```swift
struct MyItem: Transferable, Codable, Identifiable {
    let id: UUID
    var name: String
    var content: String

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .myItem)
    }
}

// Define custom UTType
extension UTType {
    static var myItem: UTType {
        UTType(exportedAs: "com.example.myitem")
    }
}
```

### Multiple Representations

```swift
struct Document: Transferable {
    var title: String
    var content: String

    static var transferRepresentation: some TransferRepresentation {
        // Primary: Custom type
        CodableRepresentation(contentType: .document)

        // Fallback: Plain text
        ProxyRepresentation(exporting: \.content)

        // File export
        FileRepresentation(exportedContentType: .plainText) { document in
            let data = document.content.data(using: .utf8)!
            let url = FileManager.default.temporaryDirectory
                .appendingPathComponent(document.title)
                .appendingPathExtension("txt")
            try data.write(to: url)
            return SentTransferredFile(url)
        }
    }
}
```

### Image Transferable

```swift
struct ImageItem: Transferable {
    var image: NSImage

    static var transferRepresentation: some TransferRepresentation {
        DataRepresentation(exportedContentType: .png) { item in
            guard let tiff = item.image.tiffRepresentation,
                  let bitmap = NSBitmapImageRep(data: tiff),
                  let png = bitmap.representation(using: .png, properties: [:]) else {
                throw TransferError.exportFailed
            }
            return png
        }

        DataRepresentation(importedContentType: .png) { data in
            guard let image = NSImage(data: data) else {
                throw TransferError.importFailed
            }
            return ImageItem(image: image)
        }
    }
}
```

## Draggable Modifier

### Basic Dragging

```swift
struct ItemView: View {
    let item: MyItem

    var body: some View {
        Text(item.name)
            .draggable(item)
    }
}
```

### Drag Preview

```swift
Text(item.name)
    .draggable(item) {
        // Custom drag preview
        HStack {
            Image(systemName: "doc")
            Text(item.name)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
```

### Multiple Items

```swift
struct GridView: View {
    @State private var items: [MyItem] = []
    @State private var selection: Set<MyItem.ID> = []

    var body: some View {
        LazyVGrid(columns: columns) {
            ForEach(items) { item in
                ItemCell(item: item, isSelected: selection.contains(item.id))
                    .draggable(item)
            }
        }
    }
}
```

## Drop Destination

### Basic Drop

```swift
struct DropZoneView: View {
    @State private var items: [MyItem] = []

    var body: some View {
        VStack {
            ForEach(items) { item in
                Text(item.name)
            }
        }
        .dropDestination(for: MyItem.self) { droppedItems, location in
            items.append(contentsOf: droppedItems)
            return true
        }
    }
}
```

### Drop with Validation

```swift
.dropDestination(for: MyItem.self) { droppedItems, location in
    // Validate items
    let validItems = droppedItems.filter { $0.isValid }
    guard !validItems.isEmpty else { return false }

    items.append(contentsOf: validItems)
    return true
} isTargeted: { isTargeted in
    // Visual feedback when dragging over
    self.isTargeted = isTargeted
}
```

### Multiple Types

```swift
.dropDestination(for: String.self) { strings, location in
    // Handle text drops
    return true
}
.dropDestination(for: URL.self) { urls, location in
    // Handle URL drops
    return true
}
.dropDestination(for: MyItem.self) { items, location in
    // Handle custom type drops
    return true
}
```

## List Drag and Drop

### Reordering

```swift
struct ReorderableList: View {
    @State private var items: [MyItem] = []

    var body: some View {
        List {
            ForEach(items) { item in
                Text(item.name)
            }
            .onMove { source, destination in
                items.move(fromOffsets: source, toOffset: destination)
            }
        }
    }
}
```

### Drag and Drop Between Lists

```swift
struct TwoListView: View {
    @State private var sourceItems: [MyItem] = []
    @State private var destinationItems: [MyItem] = []

    var body: some View {
        HStack {
            List(sourceItems) { item in
                Text(item.name)
                    .draggable(item)
            }

            List {
                ForEach(destinationItems) { item in
                    Text(item.name)
                }
            }
            .dropDestination(for: MyItem.self) { items, location in
                destinationItems.append(contentsOf: items)
                // Optionally remove from source
                sourceItems.removeAll { item in
                    items.contains { $0.id == item.id }
                }
                return true
            }
        }
    }
}
```

## Table Drag and Drop

```swift
struct TableView: View {
    @State private var items: [Item] = []
    @State private var selection: Set<Item.ID> = []

    var body: some View {
        Table(items, selection: $selection) {
            TableColumn("Name", value: \.name)
            TableColumn("Type", value: \.type)
        }
        .draggable(for: Item.self) { itemIDs in
            items.filter { itemIDs.contains($0.id) }
        }
        .dropDestination(for: Item.self) { items, location in
            self.items.append(contentsOf: items)
            return true
        }
    }
}
```

## File Drops

### Accepting File Drops

```swift
struct FileDropView: View {
    @State private var files: [URL] = []
    @State private var isTargeted = false

    var body: some View {
        VStack {
            ForEach(files, id: \.self) { url in
                Text(url.lastPathComponent)
            }
        }
        .frame(width: 300, height: 200)
        .background(isTargeted ? Color.blue.opacity(0.3) : Color.gray.opacity(0.1))
        .dropDestination(for: URL.self) { urls, location in
            files.append(contentsOf: urls)
            return true
        } isTargeted: { targeted in
            isTargeted = targeted
        }
    }
}
```

### File Drops with Type Filtering

```swift
.dropDestination(for: URL.self) { urls, location in
    let imageURLs = urls.filter { url in
        let uti = UTType(filenameExtension: url.pathExtension)
        return uti?.conforms(to: .image) ?? false
    }
    imageFiles.append(contentsOf: imageURLs)
    return !imageURLs.isEmpty
}
```

## Pasteboard Operations

### Copy to Pasteboard

```swift
func copyToPasteboard(_ item: MyItem) {
    let pasteboard = NSPasteboard.general
    pasteboard.clearContents()

    // Write custom type
    if let data = try? JSONEncoder().encode(item) {
        pasteboard.setData(data, forType: .init("com.example.myitem"))
    }

    // Also write as plain text
    pasteboard.setString(item.name, forType: .string)
}
```

### Read from Pasteboard

```swift
func readFromPasteboard() -> MyItem? {
    let pasteboard = NSPasteboard.general

    // Try custom type first
    if let data = pasteboard.data(forType: .init("com.example.myitem")),
       let item = try? JSONDecoder().decode(MyItem.self, from: data) {
        return item
    }

    // Fallback to string
    if let string = pasteboard.string(forType: .string) {
        return MyItem(id: UUID(), name: string, content: "")
    }

    return nil
}
```

### Pasteboard Change Monitoring

```swift
class PasteboardMonitor: ObservableObject {
    @Published var changeCount = 0
    private var timer: Timer?

    init() {
        changeCount = NSPasteboard.general.changeCount

        timer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { [weak self] _ in
            let currentCount = NSPasteboard.general.changeCount
            if currentCount != self?.changeCount {
                self?.changeCount = currentCount
                // Pasteboard changed
            }
        }
    }
}
```

## onCopyCommand / onPasteCommand

```swift
struct EditorView: View {
    @State private var selectedItems: [MyItem] = []
    @State private var items: [MyItem] = []

    var body: some View {
        ItemListView(items: items, selection: $selectedItems)
            .onCopyCommand {
                selectedItems.map { item in
                    NSItemProvider(object: item.name as NSString)
                }
            }
            .onPasteCommand(of: [.plainText]) { providers in
                for provider in providers {
                    provider.loadObject(ofClass: String.self) { string, _ in
                        if let name = string {
                            DispatchQueue.main.async {
                                items.append(MyItem(id: UUID(), name: name, content: ""))
                            }
                        }
                    }
                }
            }
    }
}
```

## Spring Loading

```swift
struct FolderView: View {
    let folder: Folder
    @State private var isExpanded = false

    var body: some View {
        DisclosureGroup(isExpanded: $isExpanded) {
            ForEach(folder.children) { child in
                FolderView(folder: child)
            }
        } label: {
            Label(folder.name, systemImage: "folder")
        }
        .dropDestination(for: MyItem.self) { items, location in
            folder.add(items)
            return true
        } isTargeted: { targeted in
            // Auto-expand when hovering with drag
            if targeted {
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
                    isExpanded = true
                }
            }
        }
    }
}
```

## Best Practices

1. **Implement Transferable** - For custom data types
2. **Provide multiple representations** - Support different drop targets
3. **Use appropriate UTTypes** - Define custom types when needed
4. **Provide visual feedback** - Show when drop is possible
5. **Validate drops** - Check data before accepting
6. **Support standard types** - Text, URLs, files when relevant
7. **Consider pasteboard** - For copy/paste operations
8. **Test drag operations** - Between apps, within app, from Finder

## Common UTTypes

| Type | UTType |
|------|--------|
| Plain Text | .plainText |
| Rich Text | .rtf |
| HTML | .html |
| URL | .url |
| File URL | .fileURL |
| Image | .image |
| PNG | .png |
| JPEG | .jpeg |
| PDF | .pdf |
| JSON | .json |
| Data | .data |
