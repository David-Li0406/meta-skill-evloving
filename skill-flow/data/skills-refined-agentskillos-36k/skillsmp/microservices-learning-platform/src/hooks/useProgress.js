'use client';

import { useState, useEffect } from 'react';
import { modules } from '@/data/modules';

const STORAGE_KEY = 'microservices_progress';

export function useProgress() {
    const [completedModules, setCompletedModules] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false);

    // Load progress from localStorage on mount
    useEffect(() => {
        try {
            const stored = localStorage.getItem(STORAGE_KEY);
            if (stored) {
                setCompletedModules(JSON.parse(stored));
            }
        } catch (error) {
            console.error('Failed to load progress:', error);
        } finally {
            setIsLoaded(true);
        }
    }, []);

    // Save progress whenever it changes (only after initial load)
    useEffect(() => {
        if (isLoaded) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(completedModules));
        }
    }, [completedModules, isLoaded]);

    const markAsCompleted = (slug) => {
        setCompletedModules(prev => {
            if (!prev.includes(slug)) {
                return [...prev, slug];
            }
            return prev;
        });
    };

    const toggleCompletion = (slug) => {
        setCompletedModules(prev => {
            if (prev.includes(slug)) {
                return prev.filter(s => s !== slug);
            }
            return [...prev, slug];
        });
    };

    const isCompleted = (slug) => completedModules.includes(slug);

    const getProgress = () => {
        if (modules.length === 0) return 0;
        return Math.round((completedModules.length / modules.length) * 100);
    };

    return {
        completedModules,
        markAsCompleted,
        toggleCompletion,
        isCompleted,
        getProgress,
        isLoaded
    };
}
