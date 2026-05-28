'use client';

import { CheckCircle, Zap, Clock } from 'lucide-react';

// ===========================================
// TYPES
// ===========================================

export interface SuccessItem {
    id: string;
    establishmentName: string;
    jobTitle: string;
    talentName: string;
    completedAt: string | Date;
}

export interface SuccessWidgetProps {
    recentSuccess: SuccessItem[];
}

// ===========================================
// HELPERS
// ===========================================

function formatRelativeTime(date: string | Date): string {
    const now = new Date();
    const then = new Date(date);
    const diffMs = now.getTime() - then.getTime();
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffMinutes < 60) return `il y a ${diffMinutes} min`;
    if (diffHours < 24) return `il y a ${diffHours}h`;
    if (diffDays === 1) return 'hier';
    if (diffDays < 7) return `il y a ${diffDays}j`;
    return then.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
}

// ===========================================
// COMPONENT
// ===========================================

export function SuccessWidget({ recentSuccess }: SuccessWidgetProps) {
    if (!recentSuccess || recentSuccess.length === 0) {
        return null; // Empty state: ne rien afficher
    }

    return (
        <div className="bg-white rounded-2xl shadow-sm p-5">
            {/* Header */}
            <div className="flex items-center gap-2 mb-4">
                <Zap className="w-4 h-4 text-teal-500" />
                <h3 className="font-semibold text-slate-900">
                    ⚡️ Ça vient de matcher !
                </h3>
            </div>

            {/* Success List */}
            <div className="space-y-3">
                {recentSuccess.map((item) => (
                    <div
                        key={item.id}
                        className="flex items-start gap-3 p-3 rounded-xl bg-gradient-to-r from-teal-50 to-emerald-50 border border-teal-100"
                    >
                        {/* Success Icon */}
                        <div className="flex-shrink-0 mt-0.5">
                            <CheckCircle className="w-5 h-5 text-teal-500" />
                        </div>

                        {/* Content */}
                        <div className="flex-1 min-w-0">
                            {/* Main text */}
                            <p className="text-sm text-slate-700 leading-snug">
                                <span className="font-semibold text-slate-900">
                                    {item.establishmentName}
                                </span>
                                {' '}a trouvé un{' '}
                                <span className="font-medium text-teal-700">
                                    {item.jobTitle}
                                </span>
                            </p>

                            {/* Extra name + time */}
                            <div className="flex items-center gap-2 mt-1.5">
                                <span className="text-xs text-slate-500">
                                    👤 {item.talentName}
                                </span>
                                <span className="text-xs text-slate-400 flex items-center gap-1">
                                    <Clock className="w-3 h-3" />
                                    {formatRelativeTime(item.completedAt)}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Footer CTA (optional) */}
            <div className="mt-4 pt-3 border-t border-slate-100">
                <p className="text-xs text-center text-slate-400">
                    🎉 Plus de {recentSuccess.length * 10}+ missions pourvues ce mois
                </p>
            </div>
        </div>
    );
}
