import Link from 'next/link';
import { notFound } from 'next/navigation';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import CodeBlock from '@/components/CodeBlock';
import MarkdownContent from '@/components/MarkdownContent';
import Footer from '@/components/Footer';
import ModuleFooter from '@/components/ModuleFooter';
import { modules, getModuleBySlug, getAllModuleSlugs } from '@/data/modules';

// Generate static params for all modules
export async function generateStaticParams() {
    return getAllModuleSlugs().map((slug) => ({
        module: slug,
    }));
}

// Generate metadata for each module page
export async function generateMetadata({ params }) {
    const { module: moduleSlug } = await params;
    const moduleData = getModuleBySlug(moduleSlug);

    if (!moduleData) {
        return { title: 'Module Not Found' };
    }

    return {
        title: `${moduleData.title} | Master Microservices`,
        description: moduleData.description,
    };
}

export default async function ModulePage({ params }) {
    const { module: moduleSlug } = await params;
    const moduleData = getModuleBySlug(moduleSlug);

    if (!moduleData) {
        notFound();
    }

    const currentIndex = modules.findIndex(m => m.slug === moduleSlug);
    const prevModule = currentIndex > 0 ? modules[currentIndex - 1] : null;
    const nextModule = currentIndex < modules.length - 1 ? modules[currentIndex + 1] : null;

    const difficultyStyles = {
        beginner: 'badge-beginner',
        intermediate: 'badge-intermediate',
        advanced: 'badge-advanced'
    };

    return (
        <>
            <Navbar />

            <div className="pt-24 pb-20">
                <div className="container-custom">
                    <div className="flex gap-8">
                        {/* Sidebar */}
                        <Sidebar modules={modules} />

                        {/* Main Content */}
                        <main className="flex-1 min-w-0">
                            {/* Breadcrumb */}
                            <div className="flex items-center gap-2 text-sm text-slate-400 mb-6">
                                <Link href="/" className="hover:text-white transition-colors">Home</Link>
                                <span>/</span>
                                <Link href="/course" className="hover:text-white transition-colors">Course</Link>
                                <span>/</span>
                                <span className="text-white">{moduleData.title}</span>
                            </div>

                            {/* Module Header */}
                            <div className="glass rounded-2xl p-8 mb-8">
                                <div className="flex flex-wrap items-center gap-3 mb-4">
                                    <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500/20 to-blue-500/20 border border-purple-500/30 flex items-center justify-center text-2xl font-bold text-purple-400">
                                        {moduleData.number.toString().padStart(2, '0')}
                                    </div>
                                    <span className={`badge ${difficultyStyles[moduleData.difficulty]}`}>
                                        {moduleData.difficulty === 'beginner' && '🟢 Beginner'}
                                        {moduleData.difficulty === 'intermediate' && '🟡 Intermediate'}
                                        {moduleData.difficulty === 'advanced' && '🔴 Advanced'}
                                    </span>
                                </div>

                                <h1 className="text-3xl md:text-4xl font-bold mb-4 text-brand">
                                    {moduleData.title}
                                </h1>

                                <p className="text-lg text-slate-400 mb-6">
                                    {moduleData.description}
                                </p>

                                {/* Topics */}
                                <div className="flex flex-wrap gap-2">
                                    {moduleData.topics.map((topic, index) => (
                                        <span key={index} className="text-sm px-3 py-1.5 rounded-lg bg-slate-800/50 text-slate-300 border border-slate-700/50">
                                            {topic}
                                        </span>
                                    ))}
                                </div>

                                {/* Estimated Time (content-oriented) */}
                                {moduleData.estimatedTime && (
                                    <div className="mt-4 text-sm text-slate-400">⏱ Estimated time: {moduleData.estimatedTime}</div>
                                )}

                                {/* Table of Contents for sections */}
                                {moduleData.content?.sections?.length > 0 && (
                                    <div className="mt-6 glass rounded-2xl p-6">
                                        <h4 className="text-sm font-semibold text-white mb-3 uppercase tracking-wider">Contents</h4>
                                        <ol className="list-decimal pl-6 text-slate-300">
                                            {moduleData.content.sections.map((sec, idx) => (
                                                <li key={idx} className="mb-1">{sec.title}</li>
                                            ))}
                                        </ol>
                                    </div>
                                )}
                            </div>

                                {/* Content */}
                            <div className="prose prose-invert prose-lg max-w-none">
                                {/* Introduction */}
                                <div className="glass rounded-2xl p-8 mb-8">
                                    <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-3">
                                        <span className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center text-purple-400 text-sm">📖</span>
                                        Introduction
                                    </h2>
                                    <MarkdownContent content={moduleData.content.intro} />
                                </div>

                                {/* Sections */}
                                {moduleData.content.sections.map((section, index) => (
                                    <div key={index} className="glass rounded-2xl p-8 mb-8">
                                        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-3">
                                            <span className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center text-blue-400 text-sm">
                                                {index + 1}
                                            </span>
                                            {section.title}
                                        </h2>

                                        <MarkdownContent content={section.content} />

                                        {section.keyPoints && (
                                            <div className="bg-slate-800/30 rounded-xl p-6 border border-slate-700/50 mt-6">
                                                <h4 className="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-4">✅ Key Takeaways</h4>
                                                <ul className="space-y-3">
                                                    {section.keyPoints.map((point, i) => (
                                                        <li key={i} className="flex items-start gap-3 text-slate-300">
                                                            <svg className="w-5 h-5 text-purple-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                                                            </svg>
                                                            {point}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}

                                        {section.comparison && (
                                            <div className="grid md:grid-cols-2 gap-6 mt-6">
                                                <div className="bg-slate-800/30 rounded-xl p-6 border border-slate-700/50">
                                                    <h4 className="text-lg font-semibold text-white mb-4">🏢 Monolith</h4>
                                                    <div className="mb-4">
                                                        <span className="text-sm text-green-400 font-medium">Pros:</span>
                                                        <ul className="mt-2 space-y-2">
                                                            {section.comparison.monolith.pros.map((pro, i) => (
                                                                <li key={i} className="text-slate-400 text-sm flex items-start gap-2">
                                                                    <span className="text-green-400 mt-0.5">✓</span> {pro}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                    <div>
                                                        <span className="text-sm text-red-400 font-medium">Cons:</span>
                                                        <ul className="mt-2 space-y-2">
                                                            {section.comparison.monolith.cons.map((con, i) => (
                                                                <li key={i} className="text-slate-400 text-sm flex items-start gap-2">
                                                                    <span className="text-red-400 mt-0.5">✗</span> {con}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                </div>
                                                <div className="bg-purple-500/5 rounded-xl p-6 border border-purple-500/20">
                                                    <h4 className="text-lg font-semibold text-white mb-4">🔷 Microservices</h4>
                                                    <div className="mb-4">
                                                        <span className="text-sm text-green-400 font-medium">Pros:</span>
                                                        <ul className="mt-2 space-y-2">
                                                            {section.comparison.microservices.pros.map((pro, i) => (
                                                                <li key={i} className="text-slate-400 text-sm flex items-start gap-2">
                                                                    <span className="text-green-400 mt-0.5">✓</span> {pro}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                    <div>
                                                        <span className="text-sm text-red-400 font-medium">Cons:</span>
                                                        <ul className="mt-2 space-y-2">
                                                            {section.comparison.microservices.cons.map((con, i) => (
                                                                <li key={i} className="text-slate-400 text-sm flex items-start gap-2">
                                                                    <span className="text-red-400 mt-0.5">✗</span> {con}
                                                                </li>
                                                            ))}
                                                        </ul>
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ))}

                                { /* Prerequisites and Learning Outcomes blocks moved below for a single location */ }

                                {/* Code Example */}
                                {moduleData.content.codeExample && (
                                    <div className="glass rounded-2xl p-8 mb-8">
                                        <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-3">
                                            <span className="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center text-cyan-400 text-sm">💻</span>
                                            Code Example
                                        </h2>
                                        <p className="text-slate-400 mb-4">{moduleData.content.codeExample.title}</p>
                                        <CodeBlock
                                            code={moduleData.content.codeExample.code}
                                            language={moduleData.content.codeExample.language}
                                            filename={moduleData.content.codeExample.filename}
                                        />
                                    </div>
                                )}

                                {/* Prerequisites (content-oriented) */}
                                {moduleData.prerequisites?.length > 0 && (
                                    <div className="mt-4 glass rounded-2xl p-6">
                                        <h4 className="text-lg font-semibold text-white mb-2">Prerequisites</h4>
                                        <ul className="text-slate-300 list-disc pl-6">
                                            {moduleData.prerequisites.map((p, i) => (
                                                <li key={i}>{p}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Learning Outcomes (content-oriented) */}
                                {moduleData.learningOutcomes?.length > 0 && (
                                    <div className="mt-4 glass rounded-2xl p-6">
                                        <h4 className="text-lg font-semibold text-white mb-2">Learning Outcomes</h4>
                                        <ul className="text-slate-300 list-disc pl-6">
                                            {moduleData.learningOutcomes.map((o, i) => (
                                                <li key={i}>{o}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Next Steps */}
                                {moduleData.content.nextSteps && (
                                    <div className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-2xl p-6 border border-purple-500/20 mb-8">
                                        <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                                            <span>🎯</span> What's Next?
                                        </h3>
                                        <p className="text-slate-300">{moduleData.content.nextSteps}</p>
                                    </div>
                                )}

                                {/* Navigation */}
                                <ModuleFooter
                                    moduleSlug={moduleSlug}
                                    nextModule={nextModule}
                                    prevModule={prevModule}
                                />
                            </div>
                        </main>
                    </div>
                </div>
            </div>

            <Footer />
        </>
    );
}
