'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar,
    ChevronDown,
    ExternalLink,
    Download,
} from 'lucide-react';
import { getCalendarLinks, downloadICS, openCalendarLink, type CalendarEvent } from '@/lib/calendar';

// =============================================================================
// TYPES
// =============================================================================

export interface AddToCalendarProps {
    event: CalendarEvent;
    variant?: 'button' | 'dropdown' | 'icon';
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

// =============================================================================
// ICONS
// =============================================================================

function GoogleIcon({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="currentColor">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
        </svg>
    );
}

function OutlookIcon({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="currentColor">
            <path d="M24 7.387v10.478c0 .23-.08.424-.238.576-.16.154-.352.23-.578.23h-8.547v-6.959l1.6 1.229c.102.086.227.129.375.129.148 0 .273-.043.375-.129l6.637-5.043c.079-.063.176-.094.293-.094h.001c.078 0 .148.023.211.07.063.046.108.098.137.156.028.058.047.113.055.164.009.051.013.094.013.127v-.094l-.334.16z" fill="#0072C6"/>
            <path d="M15.937 9.932l-1.535-1.18v7.219h8.282V8.068l-6.747 5.024c-.102.086-.227.129-.375.129-.148 0-.273-.043-.375-.129v-.16z" fill="#0072C6"/>
            <path d="M14.402 5.479v1.664l1.941 1.488-.002-3.152h-1.939z" fill="#0072C6"/>
            <path d="M9.07 7.313H.186c-.103 0-.186.084-.186.188v9c0 .104.083.188.186.188H9.07c.103 0 .186-.084.186-.188v-9c0-.104-.083-.188-.186-.188z" fill="#0072C6"/>
            <path d="M7.605 12c0 1.883-1.039 3.41-2.32 3.41s-2.32-1.527-2.32-3.41 1.039-3.41 2.32-3.41 2.32 1.527 2.32 3.41zm-1.113 0c0-1.332-.541-2.412-1.207-2.412s-1.207 1.08-1.207 2.412.541 2.412 1.207 2.412 1.207-1.08 1.207-2.412z" fill="#fff"/>
        </svg>
    );
}

function AppleIcon({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox="0 0 24 24" fill="currentColor">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
        </svg>
    );
}

// =============================================================================
// COMPONENT
// =============================================================================

export function AddToCalendar({
    event,
    variant = 'dropdown',
    size = 'md',
    className = '',
}: AddToCalendarProps) {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        function handleClickOutside(e: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
                setIsOpen(false);
            }
        }

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const links = getCalendarLinks(event);

    const sizeClasses = {
        sm: 'text-xs px-2 py-1',
        md: 'text-sm px-3 py-2',
        lg: 'text-base px-4 py-2.5',
    };

    const iconSizes = {
        sm: 'w-3 h-3',
        md: 'w-4 h-4',
        lg: 'w-5 h-5',
    };

    const handleGoogleClick = () => {
        openCalendarLink(links.google);
        setIsOpen(false);
    };

    const handleOutlookClick = () => {
        openCalendarLink(links.outlookWeb);
        setIsOpen(false);
    };

    const handleICSClick = () => {
        downloadICS(event);
        setIsOpen(false);
    };

    // Simple icon button variant
    if (variant === 'icon') {
        return (
            <div className={`relative ${className}`} ref={dropdownRef}>
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="p-2 rounded-lg text-slate-400 hover:text-primary-600 hover:bg-primary-50 transition-colors"
                    title="Ajouter au calendrier"
                >
                    <Calendar className={iconSizes[size]} />
                </button>

                <AnimatePresence>
                    {isOpen && (
                        <CalendarDropdownMenu
                            onGoogleClick={handleGoogleClick}
                            onOutlookClick={handleOutlookClick}
                            onICSClick={handleICSClick}
                        />
                    )}
                </AnimatePresence>
            </div>
        );
    }

    // Full button variant
    if (variant === 'button') {
        return (
            <div className={`relative ${className}`} ref={dropdownRef}>
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className={`
                        inline-flex items-center gap-2 rounded-lg font-medium
                        bg-white border border-slate-200 text-slate-700
                        hover:bg-slate-50 hover:border-slate-300 transition-colors
                        ${sizeClasses[size]}
                    `}
                >
                    <Calendar className={iconSizes[size]} />
                    Ajouter au calendrier
                    <ChevronDown className={`${iconSizes[size]} transition-transform ${isOpen ? 'rotate-180' : ''}`} />
                </button>

                <AnimatePresence>
                    {isOpen && (
                        <CalendarDropdownMenu
                            onGoogleClick={handleGoogleClick}
                            onOutlookClick={handleOutlookClick}
                            onICSClick={handleICSClick}
                        />
                    )}
                </AnimatePresence>
            </div>
        );
    }

    // Default dropdown variant (with visual cue)
    return (
        <div className={`relative ${className}`} ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`
                    inline-flex items-center gap-2 rounded-xl font-medium
                    bg-gradient-to-r from-primary-500 to-primary-600 text-white
                    hover:from-primary-600 hover:to-primary-700 
                    shadow-sm hover:shadow-md transition-all
                    ${sizeClasses[size]}
                `}
            >
                <Calendar className={iconSizes[size]} />
                <span>Ajouter au calendrier</span>
                <ChevronDown className={`${iconSizes[size]} transition-transform ${isOpen ? 'rotate-180' : ''}`} />
            </button>

            <AnimatePresence>
                {isOpen && (
                    <CalendarDropdownMenu
                        onGoogleClick={handleGoogleClick}
                        onOutlookClick={handleOutlookClick}
                        onICSClick={handleICSClick}
                    />
                )}
            </AnimatePresence>
        </div>
    );
}

// =============================================================================
// DROPDOWN MENU SUB-COMPONENT
// =============================================================================

interface CalendarDropdownMenuProps {
    onGoogleClick: () => void;
    onOutlookClick: () => void;
    onICSClick: () => void;
}

function CalendarDropdownMenu({
    onGoogleClick,
    onOutlookClick,
    onICSClick,
}: CalendarDropdownMenuProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-full mt-2 w-56 bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden z-50"
        >
            <div className="py-1">
                {/* Google Calendar */}
                <button
                    onClick={onGoogleClick}
                    className="w-full flex items-center gap-3 px-4 py-3 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                >
                    <GoogleIcon className="w-5 h-5" />
                    <span className="flex-1 text-left">Google Calendar</span>
                    <ExternalLink className="w-4 h-4 text-slate-400" />
                </button>

                {/* Outlook */}
                <button
                    onClick={onOutlookClick}
                    className="w-full flex items-center gap-3 px-4 py-3 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                >
                    <OutlookIcon className="w-5 h-5" />
                    <span className="flex-1 text-left">Outlook Calendar</span>
                    <ExternalLink className="w-4 h-4 text-slate-400" />
                </button>

                <div className="border-t border-slate-100 my-1" />

                {/* Download ICS */}
                <button
                    onClick={onICSClick}
                    className="w-full flex items-center gap-3 px-4 py-3 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
                >
                    <AppleIcon className="w-5 h-5" />
                    <span className="flex-1 text-left">Apple / Autre (ICS)</span>
                    <Download className="w-4 h-4 text-slate-400" />
                </button>
            </div>

            {/* Footer note */}
            <div className="px-4 py-2 bg-slate-50 border-t border-slate-100">
                <p className="text-xs text-slate-500">
                    📅 Un rappel sera ajouté 30min avant
                </p>
            </div>
        </motion.div>
    );
}

export default AddToCalendar;
