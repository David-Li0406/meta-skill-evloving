'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Calendar,
    ChevronLeft,
    CreditCard,
    Video,
    Loader2,
} from 'lucide-react';
import { BookingList, type Booking } from '@/components/bookings';
import { ToastContainer, useToasts } from '@/components/ui/Toast';

const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const normalized = apiBase.replace(/\/+$/, '');
    return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`;
};

// ===========================================
// TYPES
// ===========================================

type TabType = 'UPCOMING' | 'PENDING' | 'HISTORY';

// ===========================================
// COMPONENT
// ===========================================

interface ApiBooking {
    id: string;
    title: string;
    partnerName: string;
    partnerAvatar?: string;
    date: string;
    time: string;
    duration: string;
    location: string;
    price: number;
    status: string;
    isVideoSession?: boolean;
    videoRoomId?: string;
}

export default function BookingsPage() {
    const [activeTab, setActiveTab] = useState<TabType>('UPCOMING');
    const [bookings, setBookings] = useState<Booking[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const { toasts, addToast, removeToast } = useToasts();

    useEffect(() => {
        const fetchBookings = async () => {
            setIsLoading(true);
            try {
                const token = localStorage.getItem('token');
                const headers: Record<string, string> = { 'Content-Type': 'application/json' };
                if (token) {
                    headers['Authorization'] = `Bearer ${token}`;
                }
                const res = await fetch(`${getApiBase()}/wall/bookings`, {
                    headers,
                    cache: 'no-store',
                });

                if (!res.ok) {
                    throw new Error('Erreur lors du chargement');
                }

                const data: ApiBooking[] = await res.json();
                const mapped: Booking[] = data.map((b) => ({
                    ...b,
                    date: new Date(b.date),
                    status: b.status as Booking['status'],
                }));
                setBookings(mapped);
            } catch (error) {
                console.error('Erreur chargement bookings:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchBookings();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const handleCancel = (id: string) => {
        if (confirm('Êtes-vous sûr de vouloir annuler cette réservation ?')) {
            setBookings(prev => prev.map(booking =>
                booking.id === id ? { ...booking, status: 'CANCELLED' } : booking
            ));
            addToast({ message: 'Réservation annulée', type: 'info' });
        }
    };

    const filteredBookings = bookings.filter(booking => {
        if (activeTab === 'UPCOMING') return (booking.status === 'CONFIRMED' || booking.status === 'PAID') && booking.date > new Date();
        if (activeTab === 'PENDING') return booking.status === 'PENDING';
        if (activeTab === 'HISTORY') return booking.status === 'COMPLETED' || booking.status === 'CANCELLED' || booking.date < new Date();
        return false;
    });

    const TABS: { id: TabType; label: string; count?: number }[] = [
        { id: 'UPCOMING', label: 'À venir', count: bookings.filter(b => (b.status === 'CONFIRMED' || b.status === 'PAID') && b.date > new Date()).length },
        { id: 'PENDING', label: 'À payer', count: bookings.filter(b => b.status === 'PENDING').length },
        { id: 'HISTORY', label: 'Historique' },
    ];

    return (
        <div className="min-h-screen bg-slate-50">
            <ToastContainer toasts={toasts} onRemove={removeToast} />

            {/* Header */}
            <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-slate-100">
                <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-3">
                            <Link
                                href="/"
                                className="p-2 -ml-2 rounded-xl hover:bg-slate-100 transition-colors"
                                aria-label="Retour"
                            >
                                <ChevronLeft className="w-5 h-5 text-slate-600" />
                            </Link>
                            <h1 className="text-xl font-bold text-slate-900">
                                Mon Agenda
                            </h1>
                        </div>
                        <button className="p-2 rounded-xl hover:bg-slate-100 transition-colors">
                            <Calendar className="w-5 h-5 text-slate-600" />
                        </button>
                    </div>

                    {/* Tabs */}
                    <div className="flex gap-1 -mb-[1px] overflow-x-auto scrollbar-none">
                        {TABS.map((tab) => {
                            const isActive = activeTab === tab.id;
                            return (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`
                                        relative px-4 py-3 text-sm font-medium transition-colors whitespace-nowrap
                                        ${isActive ? 'text-brand-600' : 'text-slate-500 hover:text-slate-700'}
                                    `}
                                >
                                    <div className="flex items-center gap-2">
                                        {tab.label}
                                        {tab.count !== undefined && tab.count > 0 && (
                                            <span className={`
                                                px-1.5 py-0.5 text-[10px] rounded-full
                                                ${isActive ? 'bg-brand-100 text-brand-600' : 'bg-slate-100 text-slate-500'}
                                            `}>
                                                {tab.count}
                                            </span>
                                        )}
                                    </div>
                                    {isActive && (
                                        <motion.div
                                            layoutId="activeTabBorder"
                                            className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-500"
                                        />
                                    )}
                                </button>
                            );
                        })}
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                {isLoading ? (
                    <div className="flex items-center justify-center py-20">
                        <Loader2 className="w-8 h-8 animate-spin text-brand-600" />
                    </div>
                ) : (
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            transition={{ duration: 0.2 }}
                        >
                            <BookingList
                                bookings={filteredBookings}
                                onCancel={handleCancel}
                            />

                            {/* Action Buttons for each booking */}
                            <div className="mt-6 space-y-4">
                                {filteredBookings.map((booking) => (
                                    <div key={`action-${booking.id}`} className="bg-white rounded-xl p-4 border border-slate-100 shadow-sm">
                                        <div className="flex items-center justify-between">
                                            <div>
                                                <p className="font-medium text-slate-900">{booking.title}</p>
                                                <p className="text-sm text-slate-500">{booking.price}€</p>
                                            </div>
                                            {booking.status === 'PENDING' && (
                                                <Link
                                                    href={`/checkout/${booking.id}`}
                                                    className="flex items-center gap-2 px-4 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors font-medium text-sm"
                                                >
                                                    <CreditCard className="w-4 h-4" />
                                                    Payer
                                                </Link>
                                            )}
                                            {(booking.status === 'PAID' || booking.status === 'CONFIRMED') && (booking as any).isVideoSession && (
                                                <Link
                                                    href={`/visio/${(booking as any).videoRoomId || booking.id}`}
                                                    className="flex items-center gap-2 px-4 py-2 bg-brand-500 text-white rounded-xl hover:bg-brand-600 shadow-sm hover:shadow-md active:scale-95 transition-all font-medium text-sm"
                                                >
                                                    <Video className="w-4 h-4" />
                                                    Rejoindre Visio
                                                </Link>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    </AnimatePresence>
                )}
            </main>
        </div>
    );
}
