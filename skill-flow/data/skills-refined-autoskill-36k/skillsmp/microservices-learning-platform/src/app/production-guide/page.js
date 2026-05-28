import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import { productionGuideData } from '@/data/production-guide';
import ProductionGuideContent from '@/components/ProductionGuideContent';

export const metadata = {
    title: 'Production Deployment Guide | Master Microservices',
    description: 'Complete guide to deploying microservices to production - Monorepo vs Polyrepo, CI/CD pipelines, Kubernetes, Docker, and best practices.',
};

export default function ProductionGuidePage() {
    return (
        <>
            <Navbar />

            <div className="pt-24 pb-20">
                <div className="container-custom">
                    {/* Breadcrumb */}
                    <div className="flex items-center gap-2 text-sm text-slate-400 mb-6">
                        <Link href="/" className="hover:text-white transition-colors">Home</Link>
                        <span>/</span>
                        <span className="text-white">Production Deployment Guide</span>
                    </div>

                    {/* Hero Header */}
                    <div className="glass rounded-2xl p-8 mb-8">
                        <div className="flex flex-wrap items-center gap-3 mb-4">
                            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-500/30 flex items-center justify-center text-2xl">
                                🚀
                            </div>
                            <span className="badge badge-advanced">
                                🔴 Production Ready
                            </span>
                        </div>

                        <h1 className="text-3xl md:text-4xl font-bold mb-4 text-brand">
                            Production-Level Microservices Deployment Guide
                        </h1>

                        <p className="text-lg text-slate-400 mb-6">
                            A comprehensive guide covering everything you need to deploy and maintain 
                            microservices in production - from repository strategies to Kubernetes deployment.
                        </p>

                        {/* Quick Links */}
                        <div className="flex flex-wrap gap-2 mb-6">
                            {productionGuideData.sections.map((section, index) => (
                                <a 
                                    key={index}
                                    href={`#${section.id}`}
                                    className="text-sm px-3 py-1.5 rounded-lg bg-slate-800/50 text-slate-300 border border-slate-700/50 hover:bg-slate-700/50 hover:text-white transition-all"
                                >
                                    {section.emoji} {section.shortTitle}
                                </a>
                            ))}
                        </div>

                        <div className="flex flex-wrap gap-4 text-sm text-slate-400">
                            <span className="flex items-center gap-2">
                                ⏱️ Reading time: ~45 minutes
                            </span>
                            <span className="flex items-center gap-2">
                                📚 15+ Topics covered
                            </span>
                            <span className="flex items-center gap-2">
                                💻 Production-ready code
                            </span>
                        </div>
                    </div>

                    {/* Table of Contents */}
                    <div className="glass rounded-2xl p-6 mb-8">
                        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            📋 Table of Contents
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {productionGuideData.sections.map((section, index) => (
                                <a 
                                    key={index}
                                    href={`#${section.id}`}
                                    className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/30 hover:bg-slate-700/50 transition-all group"
                                >
                                    <span className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500/20 to-blue-500/20 flex items-center justify-center text-sm">
                                        {section.emoji}
                                    </span>
                                    <div>
                                        <span className="text-white group-hover:text-purple-400 transition-colors font-medium">
                                            {section.title}
                                        </span>
                                    </div>
                                </a>
                            ))}
                        </div>
                    </div>

                    {/* Main Content */}
                    <ProductionGuideContent data={productionGuideData} />

                    {/* Bottom Navigation */}
                    <div className="glass rounded-2xl p-6 mt-8">
                        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                            <Link 
                                href="/course"
                                className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                                </svg>
                                Back to Course
                            </Link>

                            <div className="flex items-center gap-4">
                                <a 
                                    href="#deployment-strategies"
                                    className="btn-primary text-sm"
                                >
                                    <span>Start Reading</span>
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <Footer />
        </>
    );
}
