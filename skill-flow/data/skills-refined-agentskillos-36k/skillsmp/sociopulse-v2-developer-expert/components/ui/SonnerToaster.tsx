'use client';

import { Toaster } from 'sonner';

export function SonnerToaster() {
    return (
        <Toaster
            position="top-right"
            richColors
            closeButton
            expand
            toastOptions={{
                classNames: {
                    toast: 'rounded-2xl',
                    title: 'text-sm font-semibold',
                    description: 'text-sm text-slate-600',
                },
            }}
        />
    );
}

