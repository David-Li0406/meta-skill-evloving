import Link from 'next/link';

/**
 * Footer - Site footer with links and info
 */
export default function Footer() {
    return (
        <footer className="border-t border-slate-800/50 mt-20">
            <div className="container-custom py-16">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
                    {/* Brand */}
                    <div className="col-span-1 md:col-span-2">
                        <Link href="/" className="flex items-center gap-3 mb-4">
                            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
                                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                                </svg>
                            </div>
                            <span className="text-xl font-bold gradient-text">MicroLearn</span>
                        </Link>
                        <p className="text-slate-400 max-w-md mb-6">
                            Learn microservices architecture from scratch. Master NestJS, Docker,
                            Kubernetes, and build scalable distributed systems.
                        </p>
                        <div className="flex items-center gap-4">
                            <a href="#" className="w-10 h-10 rounded-lg glass flex items-center justify-center text-slate-400 hover:text-white hover:bg-purple-500/20 transition-all duration-200">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                                </svg>
                            </a>
                            <a href="#" className="w-10 h-10 rounded-lg glass flex items-center justify-center text-slate-400 hover:text-white hover:bg-purple-500/20 transition-all duration-200">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                                </svg>
                            </a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="font-semibold text-white mb-4">Quick Links</h4>
                        <ul className="space-y-3">
                            <li><Link href="/course" className="text-slate-400 hover:text-white transition-colors">Start Course</Link></li>
                            <li><Link href="/#modules" className="text-slate-400 hover:text-white transition-colors">All Modules</Link></li>
                            <li><Link href="/#features" className="text-slate-400 hover:text-white transition-colors">Features</Link></li>
                            <li><Link href="/#about" className="text-slate-400 hover:text-white transition-colors">About</Link></li>
                        </ul>
                    </div>

                    {/* Topics */}
                    <div>
                        <h4 className="font-semibold text-white mb-4">Topics Covered</h4>
                        <ul className="space-y-3">
                            <li><span className="text-slate-400">NestJS Framework</span></li>
                            <li><span className="text-slate-400">Docker & Kubernetes</span></li>
                            <li><span className="text-slate-400">API Gateway</span></li>
                            <li><span className="text-slate-400">Message Queues</span></li>
                        </ul>
                    </div>
                </div>

                {/* Bottom Bar */}
                <div className="mt-12 pt-8 border-t border-slate-800/50 flex flex-col md:flex-row items-center justify-between gap-4">
                    <p className="text-slate-500 text-sm">
                        © 2024 MicroLearn. Open source learning platform.
                    </p>
                    <p className="text-slate-500 text-sm">
                        Made with 💜 for developers
                    </p>
                </div>
            </div>
        </footer>
    );
}
