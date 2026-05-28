'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';

type ServiceSummary = {
    id: string;
    name: string;
    basePrice?: number | null;
    description?: string | null;
    profile?: {
        firstName?: string | null;
        lastName?: string | null;
        avatarUrl?: string | null;
        city?: string | null;
        averageRating?: number | null;
        totalReviews?: number | null;
    } | null;
};

const API_BASE = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/v1').replace(/\/$/, '');

export default function NewBookingPage() {
    const searchParams = useSearchParams();
    const serviceId = searchParams.get('serviceId') || '';
    const router = useRouter();

    const [service, setService] = useState<ServiceSummary | null>(null);
    const [isLoadingService, setIsLoadingService] = useState(false);
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');
    const [duration, setDuration] = useState(1);
    const [message, setMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!serviceId) return;
        setIsLoadingService(true);
        fetch(`${API_BASE}/wall/services/${serviceId}`, { cache: 'no-store' })
            .then(async (res) => {
                if (res.status === 404) return null;
                if (!res.ok) throw new Error('Erreur lors du chargement du service');
                return res.json();
            })
            .then((data) => setService(data))
            .catch(() => setService(null))
            .finally(() => setIsLoadingService(false));
    }, [serviceId]);

    const pricePerHour = useMemo(() => {
        if (!service) return 0;
        const value = service.basePrice ?? 0;
        return Number.isFinite(value) ? Number(value) : 0;
    }, [service]);

    const total = useMemo(() => {
        const subtotal = pricePerHour * duration;
        return Number.isFinite(subtotal) ? subtotal : 0;
    }, [pricePerHour, duration]);

    const handleSubmit = async () => {
        setError(null);
        if (!serviceId) {
            setError('Aucun service sélectionné.');
            return;
        }
        if (!date || !time) {
            setError('Merci de renseigner la date et l’heure.');
            return;
        }
        setIsSubmitting(true);
        try {
            const res = await fetch(`${API_BASE}/bookings`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    serviceId,
                    date,
                    startTime: time,
                    duration,
                    message: message.trim() || undefined,
                }),
            });

            if (!res.ok) {
                throw new Error('La réservation a échoué');
            }

            const booking = await res.json();
            const bookingId = booking?.id;
            if (bookingId) {
                router.push(`/checkout/${bookingId}`);
            } else {
                router.push('/bookings');
            }
        } catch (err: any) {
            setError(err?.message || 'Erreur lors de la réservation');
        } finally {
            setIsSubmitting(false);
        }
    };

    const initials = (value?: string | null) => {
        if (!value) return 'LX';
        return value
            .split(' ')
            .filter(Boolean)
            .map((p) => p[0]?.toUpperCase())
            .join('')
            .slice(0, 2);
    };

    return (
        <div className="min-h-screen bg-slate-50">
            <div className="max-w-5xl mx-auto px-4 py-10">
                <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
                    <div className="bg-white rounded-2xl shadow-soft p-6 space-y-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-slate-500">Réservation</p>
                                <h1 className="text-2xl font-semibold text-slate-900">Planifier votre session</h1>
                            </div>
                            <Link href="/fil-pro" className="text-sm text-brand-600 font-semibold hover:underline">
                                Retour au Fil Pro
                            </Link>
                        </div>

                        {error && (
                            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                                {error}
                            </div>
                        )}

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <label className="space-y-2">
                                <span className="text-sm font-medium text-slate-700">Date</span>
                                <input
                                    type="date"
                                    className="input-premium"
                                    value={date}
                                    onChange={(e) => setDate(e.target.value)}
                                />
                            </label>
                            <label className="space-y-2">
                                <span className="text-sm font-medium text-slate-700">Heure</span>
                                <input
                                    type="time"
                                    className="input-premium"
                                    value={time}
                                    onChange={(e) => setTime(e.target.value)}
                                />
                            </label>
                            <label className="space-y-2">
                                <span className="text-sm font-medium text-slate-700">Durée</span>
                                <select
                                    className="input-premium"
                                    value={duration}
                                    onChange={(e) => setDuration(Number(e.target.value))}
                                >
                                    {[1, 2, 3, 4].map((h) => (
                                        <option key={h} value={h}>
                                            {h}h
                                        </option>
                                    ))}
                                </select>
                            </label>
                        </div>

                        <label className="space-y-2 block">
                            <span className="text-sm font-medium text-slate-700">Détails pour l'intervenant</span>
                            <textarea
                                className="input-premium min-h-[120px]"
                                placeholder="Partagez vos besoins, vos contraintes horaires, le contexte..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                            />
                        </label>

                        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-end">
                            <button
                                type="button"
                                onClick={handleSubmit}
                                disabled={isSubmitting}
                                className={`inline-flex items-center justify-center px-4 py-3 rounded-xl font-semibold text-white bg-brand-600 hover:bg-brand-700 transition-colors ${
                                    isSubmitting ? 'opacity-60 cursor-not-allowed' : ''
                                }`}
                            >
                                {isSubmitting ? 'Envoi...' : 'Confirmer la demande'}
                            </button>
                        </div>
                    </div>

                    <aside className="bg-white rounded-2xl shadow-soft p-6 space-y-4">
                        <h2 className="text-lg font-semibold text-slate-900">Résumé</h2>
                        <div className="flex items-center gap-3">
                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center overflow-hidden ring-2 ring-white shadow">
                                {service?.profile?.avatarUrl ? (
                                    <img
                                        src={service.profile.avatarUrl}
                                        alt={service.name}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <span className="text-sm font-semibold text-orange-600">
                                        {initials(service?.profile ? `${service.profile.firstName || ''} ${service.profile.lastName || ''}` : service?.name)}
                                    </span>
                                )}
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm text-slate-500">
                                    {service?.profile?.city || (isLoadingService ? 'Chargement...' : 'Ville inconnue')}
                                </p>
                                <p className="text-base font-semibold text-slate-900 line-clamp-1">
                                    {isLoadingService ? 'Chargement...' : service?.name || 'Service'}
                                </p>
                                <p className="text-xs text-slate-500">
                                    {service ? `${pricePerHour} € / h` : '--'}
                                </p>
                            </div>
                        </div>

                        <div className="border-t border-slate-100 pt-4 space-y-2 text-sm text-slate-700">
                            <div className="flex justify-between">
                                <span>Tarif horaire</span>
                                <span>{pricePerHour.toFixed(2)} €</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Durée</span>
                                <span>{duration} h</span>
                            </div>
                            <div className="flex justify-between font-semibold text-slate-900 text-base">
                                <span>Total à payer</span>
                                <span>{total.toFixed(2)} €</span>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>
        </div>
    );
}
