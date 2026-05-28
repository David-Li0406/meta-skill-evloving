'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
    X,
    Siren,
    Calendar,
    Palette,
    Megaphone,
    ChevronRight,
    ShieldAlert
} from 'lucide-react';
import { useAuth } from '@/lib/useAuth';

interface PublishModalProps {
    isOpen: boolean;
    onClose: () => void;
}

const tiles = [
    {
        id: 'sos',
        title: 'SOS URGENCE',
        subtitle: 'Remplacement imprévu (<48h)',
        icon: Siren,
        href: '/sos',
        colorClasses: {
            bg: 'bg-rose-50 hover:bg-rose-100',
            border: 'border-rose-200 hover:border-rose-300',
            iconBg: 'bg-rose-100',
            icon: 'text-rose-600',
            title: 'text-rose-900',
            subtitle: 'text-rose-600',
        },
    },
    {
        id: 'mission',
        title: 'OFFRE DE MISSION',
        subtitle: 'Renfort planifié ou CDD',
        icon: Calendar,
        href: '/offer/new',
        colorClasses: {
            bg: 'bg-blue-50 hover:bg-blue-100',
            border: 'border-blue-200 hover:border-blue-300',
            iconBg: 'bg-blue-100',
            icon: 'text-blue-600',
            title: 'text-blue-900',
            subtitle: 'text-blue-600',
        },
    },
    {
        id: 'atelier',
        title: 'ATELIER / PROJET',
        subtitle: 'SocioLive ou Intervenant',
        icon: Palette,
        href: '/bookings/new',
        colorClasses: {
            bg: 'bg-teal-50 hover:bg-teal-100',
            border: 'border-teal-200 hover:border-teal-300',
            iconBg: 'bg-teal-100',
            icon: 'text-teal-600',
            title: 'text-teal-900',
            subtitle: 'text-teal-600',
        },
    },
    {
        id: 'news',
        title: 'PARTAGER UNE ACTU',
        subtitle: 'Info équipe ou veille',
        icon: Megaphone,
        href: '/fil-pro',
        colorClasses: {
            bg: 'bg-slate-50 hover:bg-slate-100',
            border: 'border-slate-200 hover:border-slate-300',
            iconBg: 'bg-slate-100',
            icon: 'text-slate-600',
            title: 'text-slate-900',
            subtitle: 'text-slate-500',
        },
    },
];

const overlayVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
};

const modalVariants = {
    hidden: { opacity: 0, scale: 0.95, y: 20 },
    visible: {
        opacity: 1,
        scale: 1,
        y: 0,
        transition: { type: 'spring' as const, damping: 25, stiffness: 300 }
    },
    exit: {
        opacity: 0,
        scale: 0.95,
        y: 20,
        transition: { duration: 0.15 }
    },
};

const tileVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: (i: number) => ({
        opacity: 1,
        y: 0,
        transition: { delay: i * 0.05 },
    }),
};

export function PublishModal({ isOpen, onClose }: PublishModalProps) {
    const { user } = useAuth();
    const [showComplianceModal, setShowComplianceModal] = useState(false);
    
    // Check if establishment has KBIS/SIRET (compliance)
    const isEstablishmentCompliant = user?.role === 'CLIENT' && user?.establishment?.siret;
    
    const handleTileClick = (tileId: string) => {
        // For SOS and mission tiles, check compliance for clients
        if ((tileId === 'sos' || tileId === 'mission') && user?.role === 'CLIENT' && !isEstablishmentCompliant) {
            setShowComplianceModal(true);
            return false; // Prevent navigation
        }
        return true; // Allow navigation
    };
    
    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Overlay */}
                    <motion.div
                        variants={overlayVariants}
                        initial="hidden"
                        animate="visible"
                        exit="hidden"
                        onClick={onClose}
                        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
                    />

                    {/* Modal */}
                    <motion.div
                        variants={modalVariants}
                        initial="hidden"
                        animate="visible"
                        exit="exit"
                        className="fixed left-1/2 top-1/2 z-50 w-full max-w-2xl -translate-x-1/2 -translate-y-1/2 px-4"
                    >
                        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">
                            {/* Header */}
                            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-4">
                                <div>
                                    <h2 className="text-xl font-bold text-slate-900">Que souhaitez-vous publier ?</h2>
                                    <p className="text-sm text-slate-500">Choisissez le type de publication</p>
                                </div>
                                <button
                                    onClick={onClose}
                                    className="rounded-full p-2 text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-600"
                                    aria-label="Fermer"
                                >
                                    <X className="h-5 w-5" />
                                </button>
                            </div>

                            {/* Grid of Tiles */}
                            <div className="grid grid-cols-1 gap-4 p-6 sm:grid-cols-2">
                                {tiles.map((tile, index) => (
                                    <motion.div
                                        key={tile.id}
                                        custom={index}
                                        variants={tileVariants}
                                        initial="hidden"
                                        animate="visible"
                                    >
                                        {(tile.id === 'sos' || tile.id === 'mission') && user?.role === 'CLIENT' && !isEstablishmentCompliant ? (
                                            <button
                                                type="button"
                                                onClick={() => setShowComplianceModal(true)}
                                                className={`group flex flex-col rounded-xl border p-5 transition-all w-full text-left ${tile.colorClasses.bg} ${tile.colorClasses.border}`}
                                            >
                                                <div className="flex items-start justify-between">
                                                    <div className={`rounded-xl p-3 ${tile.colorClasses.iconBg}`}>
                                                        <tile.icon className={`h-6 w-6 ${tile.colorClasses.icon}`} />
                                                    </div>
                                                    <ShieldAlert className="h-5 w-5 text-amber-500" />
                                                </div>
                                                <h3 className={`mt-4 text-lg font-bold ${tile.colorClasses.title}`}>
                                                    {tile.title}
                                                </h3>
                                                <p className={`mt-1 text-sm ${tile.colorClasses.subtitle}`}>
                                                    {tile.subtitle}
                                                </p>
                                            </button>
                                        ) : (
                                            <Link
                                                href={tile.href}
                                                onClick={onClose}
                                                className={`group flex flex-col rounded-xl border p-5 transition-all ${tile.colorClasses.bg} ${tile.colorClasses.border}`}
                                            >
                                                <div className="flex items-start justify-between">
                                                    <div className={`rounded-xl p-3 ${tile.colorClasses.iconBg}`}>
                                                        <tile.icon className={`h-6 w-6 ${tile.colorClasses.icon}`} />
                                                    </div>
                                                    <ChevronRight className={`h-5 w-5 ${tile.colorClasses.icon} opacity-0 transition-all group-hover:translate-x-0.5 group-hover:opacity-100`} />
                                                </div>
                                                <h3 className={`mt-4 text-lg font-bold ${tile.colorClasses.title}`}>
                                                    {tile.title}
                                                </h3>
                                                <p className={`mt-1 text-sm ${tile.colorClasses.subtitle}`}>
                                                    {tile.subtitle}
                                                </p>
                                            </Link>
                                        )}
                                    </motion.div>
                                ))}
                            </div>

                            {/* Compliance Modal for Clients */}
                            <AnimatePresence>
                                {showComplianceModal && (
                                    <>
                                        <motion.div
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                            onClick={() => setShowComplianceModal(false)}
                                            className="fixed inset-0 z-[60] bg-black/50 backdrop-blur-sm"
                                        />
                                        <motion.div
                                            initial={{ opacity: 0, scale: 0.95 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            exit={{ opacity: 0, scale: 0.95 }}
                                            className="fixed left-1/2 top-1/2 z-[60] w-full max-w-md -translate-x-1/2 -translate-y-1/2 px-4"
                                        >
                                            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
                                                <div className="flex items-center justify-between mb-4">
                                                    <div className="flex items-center gap-3">
                                                        <div className="w-12 h-12 rounded-full bg-amber-100 flex items-center justify-center">
                                                            <ShieldAlert className="w-6 h-6 text-amber-600" />
                                                        </div>
                                                        <h3 className="text-lg font-bold text-slate-900">🔒 Conformité</h3>
                                                    </div>
                                                    <button
                                                        onClick={() => setShowComplianceModal(false)}
                                                        className="rounded-full p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors"
                                                        aria-label="Fermer"
                                                    >
                                                        <X className="w-5 h-5" />
                                                    </button>
                                                </div>
                                                <p className="text-slate-600 mb-6">
                                                    Veuillez fournir votre KBIS pour publier des missions et offres d'emploi.
                                                </p>
                                                <div className="flex gap-3">
                                                    <button
                                                        onClick={() => setShowComplianceModal(false)}
                                                        className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 text-slate-600 font-medium hover:bg-slate-50 transition-colors"
                                                    >
                                                        Plus tard
                                                    </button>
                                                    <Link
                                                        href="/dashboard/client/settings"
                                                        onClick={() => { setShowComplianceModal(false); onClose(); }}
                                                        className="flex-1 px-4 py-2.5 rounded-xl bg-amber-500 text-white font-semibold hover:bg-amber-600 text-center transition-colors"
                                                    >
                                                        Ajouter mon KBIS
                                                    </Link>
                                                </div>
                                            </div>
                                        </motion.div>
                                    </>
                                )}
                            </AnimatePresence>
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}

// Hook for modal state management
export function usePublishModal() {
    const [isOpen, setIsOpen] = useState(false);
    return {
        isOpen,
        open: () => setIsOpen(true),
        close: () => setIsOpen(false),
        toggle: () => setIsOpen(prev => !prev),
    };
}
