'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { modules } from '@/data/modules';

export default function Search() {
    const [query, setQuery] = useState
    ('');
    const [results, setResults] = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const searchRef = useRef(null);

    // Close on click outside
    useEffect(() => {
        function handleClickOutside(event) {
            if (searchRef.current && !searchRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    
    // Search logic
    useEffect(() => {
        if (!query) {
            setResults([]);
            return;
        }

        const lowerQuery = query.toLowerCase();
        const filtered = modules.filter(mod => {
            return (
                mod.title.toLowerCase().includes(lowerQuery) ||
                mod.description.toLowerCase().includes(lowerQuery) ||
                mod.topics.some(topic => topic.toLowerCase().includes(lowerQuery))
            );
        }).slice(0, 8); // Limit to top 8 results

        setResults(filtered);
    }, [query]);

    return (
        <div className="relative mb-6" ref={searchRef}>
            <div className="relative">
                <input
                    type="text"
                    placeholder="Search modules..."
                    value={query}
                    onChange={(e) => {
                        setQuery(e.target.value);
                        setIsOpen(true);
                    }}
                    onFocus={() => setIsOpen(true)}
                    className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all pl-10"
                />
                <svg className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
            </div>

            {/* Results Dropdown */}
            {isOpen && (query.length > 0) && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-slate-900/95 backdrop-blur-xl border border-slate-700/50 rounded-xl shadow-2xl overflow-hidden z-50">
                    {results.length > 0 ? (
                        <div className="py-2">
                            {results.map((result) => (
                                <Link
                                    key={result.slug}
                                    href={`/course/${result.slug}`}
                                    onClick={() => {
                                        setIsOpen(false);
                                        setQuery(''); // Optional: clear query on select
                                    }}
                                    className="block px-4 py-3 hover:bg-slate-800/50 transition-colors"
                                >
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center text-xs font-bold text-slate-400 flex-shrink-0">
                                            {result.number.toString().padStart(2, '0')}
                                        </div>
                                        <div>
                                            <div className="text-sm font-medium text-white">{result.title}</div>
                                            <div className="text-xs text-slate-500 line-clamp-1">{result.description}</div>
                                        </div>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    ) : (
                        <div className="p-4 text-center text-sm text-slate-500">
                            No modules found matching "{query}"
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
