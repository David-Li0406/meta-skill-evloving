import Link from 'next/link';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ModuleCard from '@/components/ModuleCard';
import CourseProgress from '@/components/CourseProgress';
import { modules } from '@/data/modules';

export const metadata = {
    title: 'Course Overview | Master Microservices',
    description: 'Explore all 18 modules of the complete microservices course. From deciding whether to use microservices to production deployment.',
};

export default function CoursePage() {
    const beginnerModules = modules.filter(m => m.difficulty === 'beginner');
    const intermediateModules = modules.filter(m => m.difficulty === 'intermediate');
    const advancedModules = modules.filter(m => m.difficulty === 'advanced');

    return (
        <>
            <Navbar />

            {/* Hero */}
            <section className="pt-32 pb-16">
                <div className="container-custom">
                    <div className="max-w-3xl">
                        <Link href="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-6">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                            Back to Home
                        </Link>
                        <h1 className="text-4xl md:text-5xl font-bold mb-4">
                            Course <span className="gradient-text">Curriculum</span>
                        </h1>
                        <p className="text-xl text-slate-400 mb-8">
                            15 comprehensive modules covering everything from microservices fundamentals
                            to production deployment. Learn at your own pace.
                        </p>

                        {/* Progress */}
                        <CourseProgress />

                        {/* Quick Stats */}
                        <div className="flex flex-wrap gap-6">
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-green-400"></span>
                                <span className="text-slate-400">{beginnerModules.length} Beginner</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-yellow-400"></span>
                                <span className="text-slate-400">{intermediateModules.length} Intermediate</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded-full bg-red-400"></span>
                                <span className="text-slate-400">{advancedModules.length} Advanced</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Modules */}
            <section className="pb-20">
                <div className="container-custom">
                    {/* Beginner */}
                    <div className="mb-16">
                        <div className="flex items-center gap-3 mb-8">
                            <div className="w-10 h-10 rounded-xl bg-green-500/20 flex items-center justify-center">
                                <span className="text-green-400 font-bold">🟢</span>
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-white">Fundamentals</h2>
                                <p className="text-slate-400 text-sm">Start here if you're new to microservices</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {beginnerModules.map((module) => (
                                <ModuleCard key={module.slug} {...module} />
                            ))}
                        </div>
                    </div>

                    {/* Intermediate */}
                    <div className="mb-16">
                        <div className="flex items-center gap-3 mb-8">
                            <div className="w-10 h-10 rounded-xl bg-yellow-500/20 flex items-center justify-center">
                                <span className="text-yellow-400 font-bold">🟡</span>
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-white">Intermediate</h2>
                                <p className="text-slate-400 text-sm">Build real-world microservices patterns</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {intermediateModules.map((module) => (
                                <ModuleCard key={module.slug} {...module} />
                            ))}
                        </div>
                    </div>

                    {/* Advanced */}
                    <div>
                        <div className="flex items-center gap-3 mb-8">
                            <div className="w-10 h-10 rounded-xl bg-red-500/20 flex items-center justify-center">
                                <span className="text-red-400 font-bold">🔴</span>
                            </div>
                            <div>
                                <h2 className="text-2xl font-bold text-white">Advanced</h2>
                                <p className="text-slate-400 text-sm">Production-ready skills and deployment</p>
                            </div>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {advancedModules.map((module) => (
                                <ModuleCard key={module.slug} {...module} />
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            <Footer />
        </>
    );
}
