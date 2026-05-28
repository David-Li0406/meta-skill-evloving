/**
 * MarkdownViewer - Beautiful markdown document renderer
 *
 * Renders markdown with refined typography and elegant styling.
 *
 * @prop {string} content - Markdown content to render
 * @prop {string} [title] - Optional document title
 * @prop {string} [className] - Additional CSS classes
 * @prop {"default" | "compact" | "wide"} [variant] - Layout variant
 * @prop {boolean} [showTableOfContents] - Show TOC for headings (default: false)
 */
function MarkdownViewer({
  content,
  title,
  className,
  variant = "default",
  showTableOfContents = false
}) {
  const [headings, setHeadings] = useState([])

  // Extract headings for TOC
  useEffect(() => {
    if (showTableOfContents && content) {
      const matches = content.match(/^#{1,3}\s+.+$/gm) || []
      const extracted = matches.map((match, i) => {
        const level = match.match(/^#+/)[0].length
        const text = match.replace(/^#+\s+/, '')
        const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-')
        return { level, text, id }
      })
      setHeadings(extracted)
    }
  }, [content, showTableOfContents])

  // Width variants
  const widthClasses = {
    compact: "max-w-xl",
    default: "max-w-2xl",
    wide: "max-w-4xl"
  }

  // Custom components for markdown elements with explicit light colors
  const components = {
    // Headings with anchor IDs
    h1: ({ children }) => {
      const id = String(children).toLowerCase().replace(/[^a-z0-9]+/g, '-')
      return (
        <h1 id={id} className="scroll-mt-8 text-4xl font-bold tracking-tight text-gray-900 mt-8 mb-4 first:mt-0">
          {children}
        </h1>
      )
    },
    h2: ({ children }) => {
      const id = String(children).toLowerCase().replace(/[^a-z0-9]+/g, '-')
      return (
        <h2 id={id} className="scroll-mt-8 text-2xl font-semibold tracking-tight text-gray-900 mt-10 mb-4 pb-2 border-b border-gray-200">
          {children}
        </h2>
      )
    },
    h3: ({ children }) => {
      const id = String(children).toLowerCase().replace(/[^a-z0-9]+/g, '-')
      return (
        <h3 id={id} className="scroll-mt-8 text-xl font-semibold text-gray-900 mt-8 mb-3">
          {children}
        </h3>
      )
    },

    // Paragraphs with refined spacing
    p: ({ children }) => (
      <p className="text-base leading-7 text-gray-600 mb-4 [&:has(img)]:mb-6">
        {children}
      </p>
    ),

    // Links with subtle styling
    a: ({ href, children }) => (
      <a
        href={href}
        className="text-blue-600 underline underline-offset-4 decoration-blue-300 hover:decoration-blue-600 transition-colors"
        target={href?.startsWith('http') ? '_blank' : undefined}
        rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
      >
        {children}
      </a>
    ),

    // Code blocks
    pre: ({ children }) => (
      <pre className="bg-gray-100 rounded-lg p-4 overflow-x-auto my-6 text-sm border border-gray-200">
        {children}
      </pre>
    ),

    // Inline code
    code: ({ children, className: codeClassName }) => {
      // If it has a className, it's a code block (handled by pre)
      if (codeClassName) {
        return <code className="font-mono text-sm text-gray-800">{children}</code>
      }
      // Inline code
      return (
        <code className="bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono text-gray-800">
          {children}
        </code>
      )
    },

    // Blockquotes with left border
    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-blue-400 pl-4 py-1 my-6 italic text-gray-600">
        {children}
      </blockquote>
    ),

    // Lists
    ul: ({ children }) => (
      <ul className="list-disc list-outside ml-6 mb-4 space-y-2 text-gray-600 marker:text-blue-400">
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol className="list-decimal list-outside ml-6 mb-4 space-y-2 text-gray-600">
        {children}
      </ol>
    ),
    li: ({ children }) => (
      <li className="leading-7 pl-1">{children}</li>
    ),

    // Horizontal rule
    hr: () => (
      <hr className="my-8 border-t border-gray-200" />
    ),

    // Tables
    table: ({ children }) => (
      <div className="my-6 overflow-x-auto rounded-lg border border-gray-200">
        <table className="w-full text-sm">
          {children}
        </table>
      </div>
    ),
    thead: ({ children }) => (
      <thead className="bg-gray-50 border-b border-gray-200">
        {children}
      </thead>
    ),
    th: ({ children }) => (
      <th className="px-4 py-3 text-left font-semibold text-gray-900">
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td className="px-4 py-3 text-gray-600 border-t border-gray-200">
        {children}
      </td>
    ),

    // Images
    img: ({ src, alt }) => (
      <img
        src={src}
        alt={alt}
        className="rounded-lg max-w-full h-auto my-6 border border-gray-200 shadow-sm"
      />
    ),

    // Strong and emphasis
    strong: ({ children }) => (
      <strong className="font-semibold text-gray-900">{children}</strong>
    ),
    em: ({ children }) => (
      <em className="italic">{children}</em>
    )
  }

  return (
    <div className={cn("min-h-screen bg-white text-gray-900", className)}>
      <div className={cn("mx-auto px-6 py-12", widthClasses[variant])}>
        {/* Optional title */}
        {title && (
          <header className="mb-12 pb-8 border-b border-gray-200">
            <h1 className="text-5xl font-bold tracking-tight text-gray-900">
              {title}
            </h1>
          </header>
        )}

        <div className="flex gap-12">
          {/* Table of Contents */}
          {showTableOfContents && headings.length > 0 && (
            <nav className="hidden lg:block w-48 flex-shrink-0">
              <div className="sticky top-8">
                <h4 className="text-sm font-semibold text-gray-900 mb-4">
                  On this page
                </h4>
                <ul className="space-y-2 text-sm">
                  {headings.map((heading, i) => (
                    <li
                      key={i}
                      style={{ paddingLeft: `${(heading.level - 1) * 12}px` }}
                    >
                      <a
                        href={`#${heading.id}`}
                        className="text-gray-500 hover:text-gray-900 transition-colors block py-1"
                      >
                        {heading.text}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            </nav>
          )}

          {/* Main content */}
          <article className="flex-1 min-w-0">
            <Markdown
              remarkPlugins={[remarkGfm]}
              components={components}
            >
              {content || ''}
            </Markdown>
          </article>
        </div>
      </div>
    </div>
  )
}
