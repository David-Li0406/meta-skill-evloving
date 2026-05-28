'use client';

import { useState } from 'react';
import CodeBlock from './CodeBlock';
import MarkdownContent from './MarkdownContent';

/**
 * LocalDevelopmentContent - Renders the local development guide sections
 */
export default function LocalDevelopmentContent({ sections }) {
    const [expandedSections, setExpandedSections] = useState(
        sections.reduce((acc, section) => ({ ...acc, [section.id]: true }), {})
    );

    const toggleSection = (sectionId) => {
        setExpandedSections(prev => ({
            ...prev,
            [sectionId]: !prev[sectionId]
        }));
    };

    return (
        <div className="space-y-8">
            {sections.map((section) => (
                <div
                    key={section.id}
                    id={section.id}
                    className="glass rounded-2xl overflow-hidden scroll-mt-24"
                >
                    {/* Section Header */}
                    <button
                        onClick={() => toggleSection(section.id)}
                        className="w-full flex items-center justify-between p-6 hover:bg-slate-800/30 transition-colors"
                    >
                        <div className="flex items-center gap-4">
                            <span className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 flex items-center justify-center text-xl">
                                {section.emoji}
                            </span>
                            <div className="text-left">
                                <h2 className="text-2xl font-bold text-white">{section.title}</h2>
                                {section.subtitle && (
                                    <p className="text-slate-400 mt-1">{section.subtitle}</p>
                                )}
                            </div>
                        </div>
                        <svg
                            className={`w-6 h-6 text-slate-400 transform transition-transform ${expandedSections[section.id] ? 'rotate-180' : ''}`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                    </button>

                    {/* Section Content */}
                    {expandedSections[section.id] && (
                        <div className="px-6 pb-6">
                            {/* Description */}
                            {section.description && (
                                <div className="mb-6 text-slate-300 leading-relaxed">
                                    <MarkdownContent content={section.description} />
                                </div>
                            )}

                            {/* Diagram */}
                            {section.diagram && (
                                <div className="mb-6">
                                    <div className="bg-slate-900/50 rounded-xl p-4 overflow-x-auto">
                                        <pre className="text-xs md:text-sm text-cyan-400 font-mono whitespace-pre">
                                            {section.diagram}
                                        </pre>
                                    </div>
                                </div>
                            )}

                            {/* Checklist */}
                            {section.checklist && (
                                <div className="mb-6 bg-slate-800/30 rounded-xl p-4">
                                    <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wide mb-3">
                                        Prerequisites Checklist
                                    </h4>
                                    <div className="space-y-2">
                                        {section.checklist.map((item, index) => (
                                            <div key={index} className="flex items-start gap-2 text-slate-300">
                                                <span className="text-green-400 flex-shrink-0">{item.substring(0, 2)}</span>
                                                <span>{item.substring(2)}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Subsections */}
                            {section.subsections && (
                                <div className="space-y-6">
                                    {section.subsections.map((subsection, subIndex) => (
                                        <div key={subIndex} className="border-l-2 border-blue-500/30 pl-4">
                                            <h3 className="text-lg font-semibold text-white mb-3">
                                                {subsection.title}
                                            </h3>
                                            
                                            {subsection.content && (
                                                <div className="mb-4 text-slate-300">
                                                    <MarkdownContent content={subsection.content} />
                                                </div>
                                            )}
                                            
                                            {subsection.code && (
                                                <div className="mb-4">
                                                    <CodeBlock
                                                        code={subsection.code}
                                                        language={subsection.codeLanguage || 'bash'}
                                                        filename={subsection.codeFilename}
                                                    />
                                                </div>
                                            )}

                                            {/* Key Points */}
                                            {subsection.keyPoints && (
                                                <div className="mt-4 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                                                    <h4 className="text-sm font-semibold text-blue-400 mb-2 flex items-center gap-2">
                                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                        </svg>
                                                        Key Points
                                                    </h4>
                                                    <ul className="space-y-1">
                                                        {subsection.keyPoints.map((point, pointIndex) => (
                                                            <li key={pointIndex} className="flex items-start gap-2 text-sm text-slate-300">
                                                                <svg className="w-4 h-4 text-blue-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                                </div>
                            )}

                            {/* Key Points (section level) */}
                            {section.keyPoints && !section.subsections && (
                                <div className="mt-4 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                                    <h4 className="text-sm font-semibold text-blue-400 mb-2">Key Points</h4>
                                    <ul className="space-y-1">
                                        {section.keyPoints.map((point, pointIndex) => (
                                            <li key={pointIndex} className="flex items-start gap-2 text-sm text-slate-300">
                                                <svg className="w-4 h-4 text-blue-400 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                </svg>
                                                {point}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {/* Warning */}
                            {section.warning && (
                                <div className="mt-6 bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
                                    <div className="flex items-start gap-3">
                                        <span className="text-amber-400 text-xl">⚠️</span>
                                        <div className="text-amber-200 text-sm">
                                            <MarkdownContent content={section.warning} />
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Tip */}
                            {section.tip && (
                                <div className="mt-6 bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                                    <div className="flex items-start gap-3">
                                        <span className="text-green-400 text-xl">💡</span>
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
