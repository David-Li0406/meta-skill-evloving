'use client';

import ReactMarkdown from 'react-markdown';

/**
 * MarkdownContent - Renders markdown with custom styling
 * @param {Object} props
 * @param {string} props.content - Markdown string to render
 */
export default function MarkdownContent({ content }) {
    return (
        <div className="markdown-content">
            <ReactMarkdown
                components={{
                    // Headings
                    h1: ({ children }) => (
                        <h1 className="text-3xl font-bold text-white mt-8 mb-4">{children}</h1>
                        
                    ),
                    h2: ({ children }) => (
                        <h2 className="text-2xl font-bold text-white mt-6 mb-3">{children}</h2>
                    ),
                    h3: ({ children }) => (
                        <h3 className="text-xl font-semibold text-white mt-4 mb-2">{children}</h3>
                    ),

                    // Paragraphs
                    p: ({ children }) => (
                        <p className="text-slate-300 leading-relaxed mb-4">{children}</p>
                    ),

                    // Lists
                    ul: ({ children }) => (
                        <ul className="list-disc list-inside space-y-2 text-slate-300 mb-4 ml-4">{children}</ul>
                    ),
                    ol: ({ children }) => (
                        <ol className="list-decimal list-inside space-y-2 text-slate-300 mb-4 ml-4">{children}</ol>
                    ),
                    li: ({ children }) => (
                        <li className="text-slate-300">{children}</li>
                    ),

                    // Inline code
                    code: ({ inline, children }) => {
                        if (inline) {
                            return (
                                <code className="px-1.5 py-0.5 rounded bg-slate-800 text-purple-400 text-sm font-mono">
                                    {children}
                                </code>
                            );
                        }
                        // Code blocks
                        return (
                            <code className="block w-full overflow-x-auto p-4 rounded-lg bg-[#1e1e2e] text-slate-300 text-sm font-mono whitespace-pre">
                                {children}
                            </code>
                        );
                    },

                    // Pre (code block wrapper)
                    pre: ({ children }) => (
                        <pre className="my-4 rounded-xl overflow-hidden border border-slate-700/50">
                            {children}
                        </pre>
                    ),

                    // Strong/Bold
                    strong: ({ children }) => (
                        <strong className="font-semibold text-white">{children}</strong>
                    ),

                    // Emphasis/Italic
                    em: ({ children }) => (
                        <em className="text-purple-400">{children}</em>
                    ),

                    // Links
                    a: ({ href, children }) => (
                        <a href={href} className="text-purple-400 hover:text-purple-300 underline" target="_blank" rel="noopener noreferrer">
                            {children}
                        </a>
                    ),

                    // Blockquote
                    blockquote: ({ children }) => (
                        <blockquote className="border-l-4 border-purple-500 pl-4 my-4 text-slate-400 italic">
                            {children}
                        </blockquote>
                    ),

                    // Horizontal rule
                    hr: () => (
                        <hr className="my-8 border-slate-700" />
                    ),

                    // Tables
                    table: ({ children }) => (
                        <div className="overflow-x-auto my-4">
                            <table className="w-full border-collapse border border-slate-700 rounded-lg overflow-hidden">
                                {children}
                            </table>
                        </div>
                    ),
                    th: ({ children }) => (
                        <th className="bg-slate-800 text-left px-4 py-2 text-white font-semibold border border-slate-700">
                            {children}
                        </th>
                    ),
                    td: ({ children }) => (
                        <td className="px-4 py-2 text-slate-300 border border-slate-700">
                            {children}
                        </td>
                    ),
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
}
