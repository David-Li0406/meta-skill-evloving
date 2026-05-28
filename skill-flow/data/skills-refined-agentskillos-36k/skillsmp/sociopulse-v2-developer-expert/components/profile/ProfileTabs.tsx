'use client';

import { useState, ReactNode } from 'react';
import { motion } from 'framer-motion';

export interface Tab {
    id: string;
    label: string;
    icon?: ReactNode;
}

export interface ProfileTabsProps {
    tabs: Tab[];
    activeTab: string;
    onTabChange: (tabId: string) => void;
}

export function ProfileTabs({ tabs, activeTab, onTabChange }: ProfileTabsProps) {
    return (
        <div className="border-b border-slate-200 overflow-x-auto scrollbar-none">
            <nav className="flex gap-1 px-4 sm:px-6 min-w-max" aria-label="Tabs">
                {tabs.map((tab) => {
                    const isActive = activeTab === tab.id;

                    return (
                        <button
                            key={tab.id}
                            onClick={() => onTabChange(tab.id)}
                            className={`
                                relative flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors touch-target
                                ${isActive
                                    ? 'text-brand-600'
                                    : 'text-slate-500 hover:text-slate-700'
                                }
                            `}
                            aria-selected={isActive}
                            role="tab"
                        >
                            {tab.icon && (
                                <span className={isActive ? 'text-brand-500' : 'text-slate-400'}>
                                    {tab.icon}
                                </span>
                            )}
                            {tab.label}

                            {/* Active Indicator */}
                            {isActive && (
                                <motion.div
                                    layoutId="activeTab"
                                    className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-600 rounded-t-full"
                                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                                />
                            )}
                        </button>
                    );
                })}
            </nav>
        </div>
    );
}

export interface TabPanelProps {
    children: ReactNode;
    isActive: boolean;
}

export function TabPanel({ children, isActive }: TabPanelProps) {
    if (!isActive) return null;

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            role="tabpanel"
        >
            {children}
        </motion.div>
    );
}
