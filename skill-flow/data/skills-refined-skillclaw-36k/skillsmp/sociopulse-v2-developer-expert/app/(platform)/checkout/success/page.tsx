'use client';

import Link from 'next/link';

export default function CheckoutSuccessPage() {
    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
            <div className="w-full max-w-md bg-white rounded-2xl shadow-soft border border-slate-100 p-8 text-center space-y-4">
                <h1 className="text-xl font-semibold text-slate-900">
                    Paiement valide !
                </h1>
                <p className="text-sm text-slate-500">
                    Bienvenue dans le club Pro.
                </p>
                <Link
                    href="/dashboard"
                    className="inline-flex items-center justify-center mt-2 px-4 py-2 rounded-xl bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors"
                >
                    Retour au Dashboard
                </Link>
            </div>
        </div>
    );
}

