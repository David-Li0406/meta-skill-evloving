'use client';

import { useState } from 'react';

/**
 * CodeBlock - Syntax highlighted code block with copy functionality
 * @param {Object} props
 * @param {string} props.code - The code to display
 * @param {string} props.language - Programming language
 * @param {string} props.filename - Optional filename to show
 */
export default function CodeBlock({ code, language = 'javascript', filename }) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        await navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="rounded-xl overflow-hidden border border-slate-700/50 my-6">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-slate-800/50 border-b border-slate-700/50">
                <div className="flex items-center gap-3">
                    {/* Window dots */}
                    <div className="flex items-center gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                        <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                        <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
                    </div>
                    {filename && (
                        <span className="text-sm text-slate-400 font-mono">{filename}</span>
                    )}
                </div>
                
                <div className="flex items-center gap-3">
                    <span className="text-xs text-slate-500 uppercase font-medium">{language}</span>
                    <button
                        onClick={handleCopy}
                        className="flex items-center gap-1 text-xs text-slate-400 hover:text-white transition-colors duration-200 px-2 py-1 rounded hover:bg-slate-700/50"
                    >
                        {copied ? (
                            <>
                                <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                                <span className="text-green-400">Copied!</span>
                            </>
                        ) : (
                            <>
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                </svg>
                                <span>Copy</span>
                            </>
                        )}
                    </button>
                </div>
            </div>

            {/* Code Content */}
            <div className="code-block p-4 overflow-x-auto">
                <pre className="text-sm leading-relaxed">
                    <code className="text-slate-300">{code}</code>
                </pre>
            </div>
        </div>
    );
}
