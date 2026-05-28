'use client';

import { useState } from 'react';
import CodeBlock from './CodeBlock';
import MarkdownContent from './MarkdownContent';

/**
 * ProductionGuideContent - Renders the production guide sections
 */
export default function ProductionGuideContent({ data }) {
    const [expandedSections, setExpandedSections] = useState(
        // All sections expanded by default
        data.sections.reduce((acc, section) => ({ ...acc, [section.id]: true }), {})
    );

    const toggleSection = (sectionId) => {
        setExpandedSections(prev => ({
            ...prev,
            [sectionId]: !prev[sectionId]
        }));
    };

    return (
        <div className="space-y-8">
            {data.sections.map((section, sectionIndex) => (
                <div 
                    key={section.id} 
                    id={section.id}
                    className="glass rounded-2xl overflow-hidden"
                >
                    {/* Section Header */}
                    <button
                        onClick={() => toggleSection(section.id)}
                        className="w-full p-6 flex items-center justify-between hover:bg-slate-800/30 transition-colors"
                    >
                        <div className="flex items-center gap-4">
                            <span className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/20 to-blue-500/20 border border-purple-500/30 flex items-center justify-center text-xl">
                                {section.emoji}
                            </span>
                            <div className="text-left">
                                <h2 className="text-xl md:text-2xl font-bold text-white">
                                    {section.title}
                                </h2>
                                {section.subtitle && (
                                    <p className="text-slate-400 text-sm mt-1">{section.subtitle}</p>
                                )}
                            </div>
                        </div>
                        <svg 
                            className={`w-6 h-6 text-slate-400 transition-transform ${expandedSections[section.id] ? 'rotate-180' : ''}`}
                            fill="none" 
                            stroke="currentColor" 
                            viewBox="0 0 24 24"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>

                    {/* Section Content */}
                    {expandedSections[section.id] && (
                        <div className="px-6 pb-6 space-y-6">
                            {/* Overview/Description */}
                            {section.description && (
                                <div className="bg-slate-800/30 rounded-xl p-4 border-l-4 border-purple-500">
                                    <MarkdownContent content={section.description} />
                                </div>
                            )}

                            {/* Diagram/ASCII Art */}
                            {section.diagram && (
                                <div className="bg-[#1e1e2e] rounded-xl p-4 overflow-x-auto border border-slate-700/50">
                                    <pre className="text-sm text-slate-300 font-mono whitespace-pre">
                                        {section.diagram}
                                    </pre>
                                </div>
                            )}

                            {/* Subsections */}
                            {section.subsections?.map((subsection, subIndex) => (
                                <div key={subIndex} className="space-y-4">
                                    <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                                        <span className="w-6 h-6 rounded-lg bg-blue-500/20 flex items-center justify-center text-blue-400 text-xs">
                                            {subIndex + 1}
                                        </span>
                                        {subsection.title}
                                    </h3>

                                    {subsection.content && (
                                        <MarkdownContent content={subsection.content} />
                                    )}

                                    {/* Code Example */}
                                    {subsection.code && (
                                        <div className="mt-4">
                                            {subsection.codeTitle && (
                                                <div className="text-sm text-slate-400 mb-2 font-medium">
                                                    📄 {subsection.codeTitle}
                                                </div>
                                            )}
                                            <CodeBlock
                                                code={subsection.code}
                                                language={subsection.codeLanguage || 'typescript'}
                                                filename={subsection.codeFilename}
                                            />
                                        </div>
                                    )}

                                    {/* Key Points */}
                                    {subsection.keyPoints && (
                                        <div className="bg-slate-800/30 rounded-xl p-4 border border-slate-700/50">
                                            <h4 className="text-sm font-semibold text-green-400 uppercase tracking-wider mb-3">
                                                ✅ Key Takeaways
                                            </h4>
                                            <ul className="space-y-2">
                                                {subsection.keyPoints.map((point, i) => (
                                                    <li key={i} className="flex items-start gap-2 text-slate-300 text-sm">
                                                        <svg className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                        </svg>
                                                        {point}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            ))}

                            {/* Code Example (Section Level) */}
                            {section.code && (
                                <div className="mt-4">
                                    {section.codeTitle && (
                                        <div className="flex items-center gap-2 text-sm text-slate-400 mb-2 font-medium">
                                            <span className="w-5 h-5 rounded bg-slate-700 flex items-center justify-center text-xs">💻</span>
                                            {section.codeTitle}
                                        </div>
                                    )}
                                    <CodeBlock
                                        code={section.code}
                                        language={section.codeLanguage || 'typescript'}
                                        filename={section.codeFilename}
                                    />
                                </div>
                            )}

                            {/* Comparison Table */}
                            {section.comparison && (
                                <div className="overflow-x-auto">
                                    <table className="w-full text-sm">
                                        <thead>
                                            <tr className="border-b border-slate-700">
                                                <th className="text-left py-3 px-4 text-slate-400 font-medium">Aspect</th>
                                                <th className="text-left py-3 px-4 text-purple-400 font-medium">Monorepo</th>
                                                <th className="text-left py-3 px-4 text-blue-400 font-medium">Polyrepo</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {section.comparison.map((row, i) => (
                                                <tr key={i} className="border-b border-slate-800">
                                                    <td className="py-3 px-4 text-slate-300 font-medium">{row.aspect}</td>
                                                    <td className="py-3 px-4 text-slate-300">{row.monorepo}</td>
                                                    <td className="py-3 px-4 text-slate-300">{row.polyrepo}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}

                            {/* Checklist */}
                            {section.checklist && (
                                <div className="bg-slate-800/30 rounded-xl p-4 border border-slate-700/50">
                                    <h4 className="text-sm font-semibold text-amber-400 uppercase tracking-wider mb-3">
                                        📋 Checklist
                                    </h4>
                                    <ul className="space-y-2">
                                        {section.checklist.map((item, i) => (
                                            <li key={i} className="flex items-start gap-2 text-slate-300 text-sm">
                                                <input type="checkbox" className="mt-1 rounded border-slate-600" />
                                                {item}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Warning/Note */}
                            {section.warning && (
                                <div className="bg-amber-500/10 rounded-xl p-4 border border-amber-500/30">
                                    <div className="flex items-start gap-3">
                                        <span className="text-xl">⚠️</span>
                                        <div className="text-amber-200 text-sm">
                                            <MarkdownContent content={section.warning} />
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Pro Tip */}
                            {section.tip && (
                                <div className="bg-green-500/10 rounded-xl p-4 border border-green-500/30">
                                    <div className="flex items-start gap-3">
                                        <span className="text-xl">💡</span>
                                        <div className="text-green-200 text-sm">
                                            <MarkdownContent content={section.tip} />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
