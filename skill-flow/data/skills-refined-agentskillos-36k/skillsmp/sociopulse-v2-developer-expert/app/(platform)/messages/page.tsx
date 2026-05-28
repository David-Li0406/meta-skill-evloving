'use client';

import { MessageCircle } from 'lucide-react';

// ===========================================
// MESSAGES INDEX PAGE (Desktop placeholder)
// ===========================================

export default function MessagesPage() {
    return (
        <div className="h-full flex flex-col items-center justify-center text-center p-8 bg-slate-50/50">
            {/* Icon */}
            <div className="w-20 h-20 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center mb-6">
                <MessageCircle className="w-10 h-10 text-brand-600" />
            </div>

            {/* Title */}
            <h2 className="text-xl font-semibold text-slate-900 mb-2">
                Vos messages
            </h2>

            {/* Subtitle */}
            <p className="text-slate-500 max-w-sm">
                Sélectionnez une conversation dans la liste pour commencer à échanger.
            </p>

            {/* Decorative Elements */}
            <div className="mt-8 flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-brand-300 animate-pulse" />
                <div className="w-2 h-2 rounded-full bg-brand-400 animate-pulse" style={{ animationDelay: '0.2s' }} />
                <div className="w-2 h-2 rounded-full bg-brand-500 animate-pulse" style={{ animationDelay: '0.4s' }} />
            </div>
        </div>
    );
}
