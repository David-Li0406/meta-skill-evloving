'use client';

import { useEffect } from 'react';
import { AlertTriangle, RotateCcw } from 'lucide-react';

export default function ReliefError({
    error,
    reset,
}: {
    error: Error & { digest?: string };
    reset: () => void;
}) {
    useEffect(() => {
        console.error(error);
    }, [error]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
            <div className="max-w-md w-full bg-white border border-slate-200 rounded-2xl shadow-sm p-6 text-center space-y-4">
                <div className="w-14 h-14 mx-auto rounded-full bg-rose-100 flex items-center justify-center text-rose-700">
                    <AlertTriangle className="w-7 h-7" />
                </div>
                <div>
                    <h2 className="text-lg font-semibold text-slate-900">Erreur sur les missions SOS</h2>
                    <p className="text-sm text-slate-500 mt-1">
                        Le module SOS Renfort ne repond pas. Reessayez ou contactez le support si le probleme persiste.
                    </p>
                </div>
                <button
                    onClick={reset}
                    className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-600 text-white text-sm font-medium hover:bg-rose-700 transition-colors"
                >
                    <RotateCcw className="w-4 h-4" />
                    Reessayer
                </button>
            </div>
        </div>
    );
}
