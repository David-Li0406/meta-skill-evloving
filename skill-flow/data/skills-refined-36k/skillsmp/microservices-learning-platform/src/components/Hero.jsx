import Link from 'next/link';

/**
 * Hero - Main landing section with animated gradient background
 */
export default function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
            {/* Animated Background Elements */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                {/* Gradient Orbs */}
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-float"></div>
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-float delay-200"></div>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-500/10 rounded-full blur-3xl"></div>
            </div>

            <div className="container-custom relative z-10 text-center">
                {/* Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8 animate-fade-in-up">
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
                    <span className="text-sm text-slate-300">Comprehensive Microservices Course</span>
                </div>

                {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 animate-fade-in-up delay-100 text-brand">
                    Master
                    <br />
                    Microservices
                </h1>

                {/* Subheading */}
                <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-10 animate-fade-in-up delay-200">
                    From fundamentals to production deployment. Learn NestJS, Docker,
                    Kubernetes, and build scalable distributed systems.
                </p>

                {/* Stats */}
                <div className="flex flex-wrap justify-center gap-8 mb-12 animate-fade-in-up delay-300">
                    <div className="text-center">
                        <div className="text-3xl font-bold text-brand">15</div>
                        <div className="text-sm text-slate-400">Modules</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl font-bold text-brand">60+</div>
                        <div className="text-sm text-slate-400">Topics</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl font-bold text-brand">100%</div>
                        <div className="text-sm text-slate-400">Hands-on</div>
                    </div>
                </div>

                {/* CTA Buttons */}
                <div className="flex flex-wrap justify-center gap-4 animate-fade-in-up delay-400">
                    <Link href="/course" className="btn-primary text-lg px-8 py-4">
                        <span>Start Free Course</span>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                        </svg>
                    </Link>
                    <Link href="/#modules" className="btn-secondary text-lg px-8 py-4">
                        <span>View Curriculum</span>
                    </Link>
                </div>

                {/* Scroll Indicator */}
                <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce">
                    <svg className="w-6 h-6 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                    </svg>
                </div>
            </div>

            {/* Architecture Illustration */}
            <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#0a0a0f] to-transparent pointer-events-none"></div>
        </section>
    );
}


