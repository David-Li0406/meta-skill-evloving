'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ChevronRight, Sparkles } from 'lucide-react';
import { useAuth } from '@/lib/useAuth';

// =============================================================================
// DASHBOARD ALERT - Dismissible Profile Completion Banner
// Shows when user profile is incomplete
// =============================================================================

interface DashboardAlertProps {
    /** Override the default profile completion percentage */
    completionPercentage?: number;
    /** Custom message to display */
    customMessage?: string;
    /** Link destination for the CTA */
    ctaLink?: string;
    /** CTA button text */
    ctaText?: string;
}

/**
 * Calculate profile completion percentage based on user data
 */
function calculateProfileCompletion(user: ReturnType<typeof useAuth>['user']): number {
    if (!user) return 0;
    
    let completed = 0;
    let total = 0;
    
    // Basic user fields
    total += 2;
    if (user.email) completed += 1;
    if (user.phone) completed += 1;
    
    // Profile fields (for talents)
    if (user.profile) {
        total += 6;
        if (user.profile.firstName) completed += 1;
        if (user.profile.lastName) completed += 1;
        if (user.profile.avatarUrl) completed += 1;
        if (user.profile.bio) completed += 1;
        if (user.profile.city) completed += 1;
        if (user.profile.headline) completed += 1;
        
        // Compliance status
        total += 1;
        if (user.profile.complianceStatus === 'VALIDATED' || user.profile.complianceStatus === 'SUBMITTED') {
            completed += 1;
        }
    }
    
    // Establishment fields (for clients)
    if (user.establishment) {
        total += 4;
        if (user.establishment.name) completed += 1;
        if (user.establishment.address) completed += 1;
        if (user.establishment.city) completed += 1;
        if (user.establishment.siret) completed += 1;
    }
    
    return total > 0 ? Math.round((completed / total) * 100) : 0;
}

export function DashboardAlert({
    completionPercentage,
    customMessage,
    ctaLink,
    ctaText = 'Compléter maintenant',
}: DashboardAlertProps) {
    const { user, isLoading } = useAuth();
    const [isDismissed, setIsDismissed] = useState(false);
    const [isHydrated, setIsHydrated] = useState(false);
    
    // Check localStorage for dismiss state
    useEffect(() => {
        setIsHydrated(true);
        const dismissedKey = `dashboard_alert_dismissed_${user?.id || 'guest'}`;
        const dismissedUntil = localStorage.getItem(dismissedKey);
        
        if (dismissedUntil) {
            const dismissedDate = new Date(dismissedUntil);
            if (dismissedDate > new Date()) {
                setIsDismissed(true);
            } else {
                localStorage.removeItem(dismissedKey);
            }
        }
    }, [user?.id]);
    
    const handleDismiss = () => {
        setIsDismissed(true);
        // Dismiss for 24 hours
        const dismissedKey = `dashboard_alert_dismissed_${user?.id || 'guest'}`;
        const tomorrow = new Date();
        tomorrow.setHours(tomorrow.getHours() + 24);
        localStorage.setItem(dismissedKey, tomorrow.toISOString());
    };
    
    // Calculate or use provided percentage
    const percentage = completionPercentage ?? calculateProfileCompletion(user);
    
    // Determine profile link based on role
    const profileLink = ctaLink ?? (
        user?.role === 'CLIENT' 
            ? '/dashboard/client/settings' 
            : '/dashboard/talent/profile'
    );
    
    // Don't show if loading, dismissed, hydrating, or profile is complete (>= 80%)
    if (isLoading || isDismissed || !isHydrated || percentage >= 80) {
        return null;
    }
    
    const message = customMessage ?? 
        `👋 Bienvenue ! Votre profil est à ${percentage}%. Complétez-le pour débloquer toutes les fonctionnalités.`;
    
    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20, height: 0 }}
                transition={{ duration: 0.3 }}
                className="relative overflow-hidden rounded-xl border border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50 p-4 shadow-sm"
            >
                {/* Background decoration */}
                <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-blue-100/50 blur-2xl" />
                <div className="absolute -bottom-4 -left-4 h-20 w-20 rounded-full bg-indigo-100/50 blur-2xl" />
                
                <div className="relative flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                    <div className="flex items-start gap-3 sm:items-center">
                        {/* Icon */}
                        <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-blue-100">
                            <Sparkles className="h-5 w-5 text-blue-600" />
                        </div>
                        
                        {/* Message */}
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-blue-900 sm:text-base">
                                {message}
                            </p>
                            
                            {/* Progress bar */}
                            <div className="mt-2 flex items-center gap-2">
                                <div className="h-1.5 flex-1 max-w-[200px] rounded-full bg-blue-200/50 overflow-hidden">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${percentage}%` }}
                                        transition={{ duration: 0.8, delay: 0.2 }}
                                        className="h-full rounded-full bg-blue-500"
                                    />
                                </div>
                                <span className="text-xs font-semibold text-blue-600">
                                    {percentage}%
                                </span>
                            </div>
                        </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex items-center gap-2 sm:flex-shrink-0">
                        <Link
                            href={profileLink}
                            className="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-all hover:bg-blue-700 hover:shadow-md active:scale-[0.98]"
                        >
                            {ctaText}
                            <ChevronRight className="h-4 w-4" />
                        </Link>
                        
                        <button
                            onClick={handleDismiss}
                            className="rounded-lg p-2 text-blue-400 transition-colors hover:bg-blue-100 hover:text-blue-600"
                            aria-label="Fermer l'alerte"
                        >
                            <X className="h-5 w-5" />
                        </button>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}
