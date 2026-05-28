'use client';

import { useEffect, useState, useCallback } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { X, Clock, AlertTriangle } from 'lucide-react';

interface ToastProps {
    id: string;
    message: string;
    type?: 'info' | 'warning' | 'error' | 'success';
    duration?: number;
    onClose?: (id: string) => void;
}

interface ToastContainerProps {
    toasts: ToastProps[];
    onRemove: (id: string) => void;
}

const typeStyles = {
    info: 'bg-slate-800 border-slate-700 text-white',
    warning: 'bg-amber-500 border-amber-600 text-white',
    error: 'bg-red-500 border-red-600 text-white',
    success: 'bg-green-500 border-green-600 text-white',
};

const typeIcons = {
    info: Clock,
    warning: AlertTriangle,
    error: X,
    success: Clock,
};

function Toast({ id, message, type = 'info', duration = 5000, onClose }: ToastProps) {
    useEffect(() => {
        if (duration > 0) {
            const timer = setTimeout(() => {
                onClose?.(id);
            }, duration);
            return () => clearTimeout(timer);
        }
    }, [id, duration, onClose]);

    const Icon = typeIcons[type];

    return (
        <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className={`
        flex items-center gap-3 px-4 py-3 rounded-xl border shadow-lg backdrop-blur-sm
        ${typeStyles[type]}
      `}
        >
            <Icon className="w-5 h-5 flex-shrink-0" />
            <p className="text-sm font-medium">{message}</p>
            <button
                onClick={() => onClose?.(id)}
                className="p-1 rounded-lg hover:bg-white/10 transition-colors ml-2"
            >
                <X className="w-4 h-4" />
            </button>
        </motion.div>
    );
}

export function ToastContainer({ toasts, onRemove }: ToastContainerProps) {
    return (
        <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-50 flex flex-col gap-2">
            <AnimatePresence>
                {toasts.map((toast) => (
                    <Toast key={toast.id} {...toast} onClose={onRemove} />
                ))}
            </AnimatePresence>
        </div>
    );
}

// Hook for managing toasts
export function useToasts() {
    const [toasts, setToasts] = useState<ToastProps[]>([]);

    const addToast = useCallback((toast: Omit<ToastProps, 'id'>) => {
        const id = Math.random().toString(36).substr(2, 9);
        setToasts(prev => [...prev, { ...toast, id }]);
    }, []);

    const removeToast = useCallback((id: string) => {
        setToasts(prev => prev.filter(t => t.id !== id));
    }, []);

    return { toasts, addToast, removeToast };
}
