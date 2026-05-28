'use client';

import Link from 'next/link';
import { localDevelopmentData } from '@/data/local-development';
import LocalDevelopmentContent from '@/components/LocalDevelopmentContent';

export default function LocalDevelopmentPage() {
    const { title, description, sections } = localDevelopmentData;

    return (
        <main className="min-h-screen pt-24 pb-16">
            {/* Hero Section */}
            <section className="container-custom mb-16">
                {/* Breadcrumb */}
                <nav className="flex items-center gap-2 text-sm text-slate-400 mb-8">
                    <Link href="/" className="hover:text-white transition-colors">Home</Link>
                    <span>/</span>
                    <span className="text-purple-400">Local Development Guide</span>
                </nav>

                <div className="flex items-start gap-6 mb-8">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 flex items-center justify-center text-3xl">
                        🐳
                    </div>
                    <div>
                        <h1 className="text-4xl md:text-5xl font-bold mb-4">
                            <span className="text-brand">{title}</span>
                        </h1>
                        <p className="text-xl text-slate-300 max-w-3xl">
                            {description}
                        </p>
                    </div>
                </div>

                {/* Quick Links */}
                <div className="glass rounded-2xl p-6 mb-8">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <span>🚀</span> Quick Start
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        <Link 
                            href="#monorepo-local"
                            className="flex items-center gap-3 p-4 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors group"
                        >
                            <span className="text-2xl">🏢</span>
                            <div>
                                <div className="font-medium text-white group-hover:text-purple-400 transition-colors">Monorepo Setup</div>
                                <div className="text-sm text-slate-400">Docker Compose for all services</div>
                            </div>
                        </Link>
                        <Link 
                            href="#polyrepo-local"
                            className="flex items-center gap-3 p-4 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors group"
                        >
                            <span className="text-2xl">📦</span>
                            <div>
                                <div className="font-medium text-white group-hover:text-purple-400 transition-colors">Polyrepo Setup</div>
                                <div className="text-sm text-slate-400">Individual service repos</div>
                            </div>
                        </Link>
                        <Link 
                            href="#without-docker"
                            className="flex items-center gap-3 p-4 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors group"
                        >
                            <span className="text-2xl">💻</span>
                            <div>
                                <div className="font-medium text-white group-hover:text-purple-400 transition-colors">Without Docker</div>
                                <div className="text-sm text-slate-400">Native Node.js development</div>
                            </div>
                        </Link>
                        <Link 
                            href="#local-testing"
                            className="flex items-center gap-3 p-4 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors group"
                        >
                            <span className="text-2xl">🧪</span>
                            <div>
                                <div className="font-medium text-white group-hover:text-purple-400 transition-colors">Local Testing</div>
                                <div className="text-sm text-slate-400">Unit, integration, E2E</div>
                            </div>
                        </Link>
                    </div>
                </div>

                {/* Table of Contents */}
                <div className="glass rounded-2xl p-6">
                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                        <span>📑</span> Table of Contents
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                        {sections.map((section, index) => (
                            <Link 
                                key={section.id}
                                href={`#${section.id}`}
                                className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800/50 transition-colors group"
                            >
                                <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center text-sm">
                                    {section.emoji}
                                </span>
                                <div>
                                    <div className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">
                                        {index + 1}. {section.shortTitle}
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </section>

            {/* Content Sections */}
            <section className="container-custom">
                <LocalDevelopmentContent sections={sections} />
            </section>

            {/* Related Guides */}
            <section className="container-custom mt-16">
                <div className="glass rounded-2xl p-8">
                    <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                        <span>📚</span> Related Guides
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <Link 
                            href="/production-guide"
                            className="flex items-center gap-4 p-6 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center text-2xl">
                                🚢
                            </div>
                            <div>
                                <div className="font-semibold text-white group-hover:text-purple-400 transition-colors">Production Deployment Guide</div>
                                <div className="text-sm text-slate-400">CI/CD, Kubernetes, GitOps, and more</div>
                            </div>
                            <svg className="w-5 h-5 text-slate-500 group-hover:text-purple-400 transition-colors ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </Link>
                        <Link 
                            href="/course"
                            className="flex items-center gap-4 p-6 rounded-xl bg-slate-800/50 hover:bg-slate-700/50 transition-colors group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/20 to-blue-500/20 flex items-center justify-center text-2xl">
                                📖
                            </div>
                            <div>
                                <div className="font-semibold text-white group-hover:text-purple-400 transition-colors">Microservices Course</div>
                                <div className="text-sm text-slate-400">Learn microservices from scratch</div>
                            </div>
                            <svg className="w-5 h-5 text-slate-500 group-hover:text-purple-400 transition-colors ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </Link>
                    </div>
                </div>
            </section>
        </main>
    );
}
