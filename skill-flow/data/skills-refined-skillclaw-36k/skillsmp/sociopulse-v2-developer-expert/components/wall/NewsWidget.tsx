'use client';

import { ExternalLink, Newspaper, Clock } from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface NewsItem {
    id: string;
    title: string;
    source: string;
    url: string;
    excerpt?: string;
    publishedAt: string | Date;
}

export interface NewsWidgetProps {
    news: NewsItem[];
}

// ===========================================
// HELPERS
// ===========================================

function formatRelativeTime(date: string | Date): string {
    const now = new Date();
    const then = new Date(date);
    const diffMs = now.getTime() - then.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffHours < 1) return "À l'instant";
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    if (diffDays === 1) return 'Hier';
    if (diffDays < 7) return `Il y a ${diffDays}j`;
    return then.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
}

function getSourceColor(source: string): string {
    const colors: Record<string, string> = {
        'ASH': 'bg-blue-100 text-blue-700',
        'Ministère': 'bg-rose-100 text-rose-700',
        'Légifrance': 'bg-amber-100 text-amber-700',
        'Santé.gouv': 'bg-teal-100 text-teal-700',
    };
    return colors[source] || 'bg-slate-100 text-slate-600';
}

// ===========================================
// COMPONENT
// ===========================================

export function NewsWidget({ news }: NewsWidgetProps) {
    if (!news || news.length === 0) {
        return null; // Empty state: ne rien afficher
    }

    return (
        <div className="bg-white rounded-2xl shadow-sm p-5">
            {/* Header */}
            <div className="flex items-center gap-2 mb-4">
                <Newspaper className="w-4 h-4 text-brand-600" />
                <h3 className="font-semibold text-slate-900">
                    📰 Veille Sectorielle
                </h3>
            </div>

            {/* News List */}
            <div className="space-y-3">
                {news.map((item, index) => (
                    <a
                        key={item.id}
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="group block p-3 rounded-xl hover:bg-slate-50 transition-colors border border-transparent hover:border-slate-200"
                    >
                        {/* Title */}
                        <h4 className="text-sm font-medium text-slate-900 line-clamp-2 group-hover:text-brand-600 transition-colors">
                            {item.title}
                        </h4>

                        {/* Meta row */}
                        <div className="flex items-center gap-2 mt-2">
                            {/* Source Badge */}
                            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${getSourceColor(item.source)}`}>
                                {item.source}
                            </span>
                            
                            {/* Time */}
                            <span className="text-xs text-slate-400 flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {formatRelativeTime(item.publishedAt)}
                            </span>

                            {/* External icon */}
                            <ExternalLink className="w-3 h-3 text-slate-300 group-hover:text-brand-500 ml-auto transition-colors" />
                        </div>
                    </a>
                ))}
            </div>
        </div>
    );
}
