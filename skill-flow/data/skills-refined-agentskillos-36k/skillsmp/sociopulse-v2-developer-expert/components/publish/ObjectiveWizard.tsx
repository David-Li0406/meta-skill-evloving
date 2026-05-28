'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import {
    Siren,
    Calendar,
    Users,
    ChevronRight
} from 'lucide-react';

const options = [
    {
        id: 'absence',
        label: 'Combler une absence',
        href: '/sos',
        icon: Siren,
        color: 'rose',
    },
    {
        id: 'activite',
        label: 'Organiser une activité',
        href: '/bookings/new',
        icon: Calendar,
        color: 'teal',
    },
    {
        id: 'equipe',
        label: 'Compléter mon équipe',
        href: '/offer/new',
        icon: Users,
        color: 'blue',
    },
];

const colorClasses = {
    rose: {
        bg: 'bg-rose-50 hover:bg-rose-100',
        border: 'border-rose-200 hover:border-rose-300',
        text: 'text-rose-700',
        icon: 'text-rose-500',
    },
    teal: {
        bg: 'bg-teal-50 hover:bg-teal-100',
        border: 'border-teal-200 hover:border-teal-300',
        text: 'text-teal-700',
        icon: 'text-teal-500',
    },
    blue: {
        bg: 'bg-blue-50 hover:bg-blue-100',
        border: 'border-blue-200 hover:border-blue-300',
        text: 'text-blue-700',
        icon: 'text-blue-500',
    },
};

interface ObjectiveWizardProps {
    userName?: string;
}

export function ObjectiveWizard({ userName = 'Jean' }: ObjectiveWizardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
            <h2 className="text-lg font-semibold text-slate-900">
                Bonjour{userName ? ` ${userName}` : ''}, quel est votre objectif ?
            </h2>
            <p className="mt-1 text-sm text-slate-500">
                Choisissez une action rapide pour commencer
            </p>

            {/* Pill Buttons */}
            <div className="mt-5 flex flex-wrap gap-3">
                {options.map((option, index) => {
                    const colors = colorClasses[option.color as keyof typeof colorClasses];
                    return (
                        <motion.div
                            key={option.id}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                        >
                            <Link
                                href={option.href}
                                className={`group inline-flex items-center gap-2 rounded-full border px-4 py-2.5 text-sm font-medium transition-all ${colors.bg} ${colors.border} ${colors.text}`}
                            >
                                <option.icon className={`h-4 w-4 ${colors.icon}`} />
                                {option.label}
                                <ChevronRight className="h-4 w-4 opacity-0 transition-all group-hover:translate-x-0.5 group-hover:opacity-100" />
                            </Link>
                        </motion.div>
                    );
                })}
            </div>
        </motion.div>
    );
}
