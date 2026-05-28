'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';

/**
 * Navbar - Sticky navigation with glassmorphism effect
 */
export default function Navbar() {
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        
        <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'glass-strong py-3' : 'py-5'
            }`}>
            <div className="container-custom flex items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-3 group">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                    </div>
                    <span className="text-xl font-bold text-brand">MicroLearn</span>
                </Link>

                {/* Navigation Links */}
                <div className="hidden md:flex items-center gap-6">
                    <Link href="/#modules" className="text-slate-300 hover:text-white transition-colors duration-200 font-medium">
                        Modules
                    </Link>
                    <Link href="/local-development" className="text-slate-300 hover:text-white transition-colors duration-200 font-medium flex items-center gap-1">
                        <span>🐳</span>
                        <span>Local Dev</span>
                    </Link>
                    <Link href="/production-guide" className="text-slate-300 hover:text-white transition-colors duration-200 font-medium flex items-center gap-1">
                        <span>🚀</span>
                        <span>Production</span>
                    </Link>
                    <Link href="/#about" className="text-slate-300 hover:text-white transition-colors duration-200 font-medium">
                        About
                    </Link>
                </div>

                {/* CTA Button */}
                <Link href="/course" className="btn-primary text-sm">
                    <span>Start Learning</span>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                </Link>
            </div>
        </nav>
    );
}
