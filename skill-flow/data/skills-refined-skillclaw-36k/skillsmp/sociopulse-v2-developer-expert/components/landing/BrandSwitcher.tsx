'use client';

import { motion } from 'framer-motion';
import { isMedical } from '@/lib/brand';

// ===========================================
// BRAND SWITCHER - Modern SaaS 2026 Style
// Établissement / Talent toggle with trendy design
// ===========================================

export type ViewMode = 'establishment' | 'talent';

interface BrandSwitcherProps {
    value: ViewMode;
    onChange: (mode: ViewMode) => void;
}

export function BrandSwitcher({ value, onChange }: BrandSwitcherProps) {
    const isEstablishment = value === 'establishment';

    // Modern labels with trendy emojis
    const establishmentLabel = isMedical() ? 'Établissement' : 'Établissement';
    const talentLabel = isMedical() ? 'Soignant' : 'Talent';
    const establishmentEmoji = isMedical() ? '🏥' : '🏢';
    const talentEmoji = isMedical() ? '👩‍⚕️' : '✨';

    // Brand colors
    const activeColor = isMedical()
        ? 'bg-rose-500 text-white shadow-lg shadow-rose-500/25'
        : 'bg-teal-500 text-white shadow-lg shadow-teal-500/25';

    return (
        <div className="flex justify-center py-4">
            <div className="inline-flex items-center p-1 rounded-2xl bg-white border border-slate-200 shadow-sm">
                {/* Establishment Button */}
                <button
                    onClick={() => onChange('establishment')}
                    className={`
                        relative flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300
                        ${isEstablishment
                            ? activeColor
                            : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                        }
                    `}
                >
                    <span>{establishmentEmoji}</span>
                    <span>{establishmentLabel}</span>
                </button>

                {/* Talent Button */}
                <button
                    onClick={() => onChange('talent')}
                    className={`
                        relative flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300
                        ${!isEstablishment
                            ? activeColor
                            : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                        }
                    `}
                >
                    <span>{talentEmoji}</span>
                    <span>{talentLabel}</span>
                </button>
            </div>
        </div>
    );
}
