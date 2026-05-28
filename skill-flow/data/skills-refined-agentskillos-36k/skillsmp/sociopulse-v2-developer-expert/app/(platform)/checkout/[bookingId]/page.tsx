'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { ArrowLeft, CheckCircle, Loader2, CreditCard, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || '');

const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const normalized = apiBase.replace(/\/+$/, '');
    return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`;
};

const getToken = () => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('accessToken') || 
           document.cookie.split(';').find(c => c.trim().startsWith('accessToken='))?.split('=')[1];
};

interface BookingDetails {
    id: string;
    totalPrice: number;
    sessionDate: string | null;
    sessionTime: string | null;
    service: { name: string; imageUrl: string | null } | null;
    provider: {
        profile: { firstName: string; lastName: string; avatarUrl: string | null } | null;
    } | null;
}

function CheckoutForm({ bookingId, onSuccess }: { bookingId: string; onSuccess: () => void }) {
    const stripe = useStripe();
    const elements = useElements();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);

        if (!stripe || !elements) return;

        setIsSubmitting(true);

        const { error: stripeError, paymentIntent } = await stripe.confirmPayment({
            elements,
            redirect: 'if_required',
        });

        if (stripeError) {
            setError(stripeError.message || 'Une erreur est survenue lors du paiement.');
            setIsSubmitting(false);
            return;
        }

        if (paymentIntent?.status === 'succeeded') {
            try {
                const token = getToken();
                const confirmHeaders: Record<string, string> = {
                    'Content-Type': 'application/json',
                };
                if (token) {
                    confirmHeaders['Authorization'] = `Bearer ${token}`;
                }
                await fetch(`${getApiBase()}/payments/confirm-mock/${bookingId}`, {
                    method: 'POST',
                    headers: confirmHeaders,
                });
                onSuccess();
            } catch (err) {
                console.error('Confirm error:', err);
                onSuccess();
            }
        }

        setIsSubmitting(false);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6">
                <div className="flex items-center gap-2 mb-4">
                    <CreditCard className="h-5 w-5 text-slate-600" />
                    <span className="font-medium text-slate-900">Informations de paiement</span>
                </div>
                <PaymentElement 
                    options={{
                        layout: 'tabs',
                    }}
                />
            </div>

            {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                    <p className="text-sm text-red-700">{error}</p>
                </div>
            )}

            <button
                type="submit"
                disabled={!stripe || isSubmitting}
                className={`w-full h-12 rounded-xl font-semibold text-white text-sm transition-all flex items-center justify-center gap-2 ${
                    !stripe || isSubmitting
                        ? 'bg-slate-400 cursor-not-allowed'
                        : 'bg-brand-600 hover:bg-brand-700 shadow-lg hover:shadow-xl'
                }`}
            >
                {isSubmitting ? (
                    <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Paiement en cours...
                    </>
                ) : (
                    <>
                        <ShieldCheck className="h-4 w-4" />
                        Payer maintenant
                    </>
                )}
            </button>

            <p className="text-xs text-slate-500 text-center flex items-center justify-center gap-1">
                <ShieldCheck className="h-3 w-3" />
                Paiement securise par Stripe
            </p>
        </form>
    );
}

function SuccessView() {
    const router = useRouter();

    useEffect(() => {
        const timer = setTimeout(() => {
            router.push('/bookings');
        }, 3000);
        return () => clearTimeout(timer);
    }, [router]);

    return (
        <div className="text-center py-12">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
            <h2 className="text-xl font-semibold text-slate-900 mb-2">Paiement reussi !</h2>
            <p className="text-slate-600 mb-6">
                Votre reservation est confirmee. Vous allez etre redirige...
            </p>
            <Link
                href="/bookings"
                className="inline-flex items-center gap-2 text-brand-600 font-medium hover:underline"
            >
                Voir mes reservations
            </Link>
        </div>
    );
}

export default function BookingCheckoutPage() {
    const params = useParams();
    const bookingId = params.bookingId as string;
    
    const [clientSecret, setClientSecret] = useState<string | null>(null);
    const [booking, setBooking] = useState<BookingDetails | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [paymentSuccess, setPaymentSuccess] = useState(false);

    useEffect(() => {
        const initCheckout = async () => {
            try {
                const token = getToken();
                const headers: Record<string, string> = {
                    'Content-Type': 'application/json',
                };
                if (token) headers['Authorization'] = `Bearer ${token}`;

                const [bookingRes, intentRes] = await Promise.all([
                    fetch(`${getApiBase()}/payments/booking/${bookingId}`, { headers }),
                    fetch(`${getApiBase()}/payments/create-intent/${bookingId}`, {
                        method: 'POST',
                        headers,
                    }),
                ]);

                if (!bookingRes.ok || !intentRes.ok) {
                    throw new Error('Impossible de charger le checkout');
                }

                const bookingData = await bookingRes.json();
                const intentData = await intentRes.json();

                setBooking(bookingData);
                setClientSecret(intentData.clientSecret);
            } catch (err) {
                console.error('Checkout init error:', err);
                setError('Impossible de charger le paiement. Verifiez que la reservation existe.');
            } finally {
                setIsLoading(false);
            }
        };

        if (bookingId) {
            initCheckout();
        }
    }, [bookingId]);

    const handleSuccess = useCallback(() => {
        setPaymentSuccess(true);
    }, []);

    if (isLoading) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <Loader2 className="h-8 w-8 text-brand-600 animate-spin" />
                    <p className="text-slate-600">Chargement du paiement...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
                <div className="w-full max-w-md text-center">
                    <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
                        <p className="text-red-700 mb-4">{error}</p>
                        <Link
                            href="/bookings"
                            className="inline-flex items-center gap-2 text-brand-600 font-medium hover:underline"
                        >
                            <ArrowLeft className="h-4 w-4" />
                            Retour aux reservations
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 py-8 px-4">
            <div className="max-w-lg mx-auto">
                <Link
                    href="/bookings"
                    className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900 mb-6 transition-colors"
                >
                    <ArrowLeft className="h-4 w-4" />
                    Retour
                </Link>

                <div className="bg-white rounded-3xl shadow-soft border border-slate-100 overflow-hidden">
                    <div className="p-6 border-b border-slate-100">
                        <h1 className="text-xl font-semibold text-slate-900">Finaliser le paiement</h1>
                        {booking && (
                            <div className="mt-4 flex items-center gap-4">
                                {booking.service?.imageUrl ? (
                                    <img
                                        src={booking.service.imageUrl}
                                        alt={booking.service.name}
                                        className="w-16 h-16 rounded-xl object-cover"
                                    />
                                ) : (
                                    <div className="w-16 h-16 rounded-xl bg-slate-100 flex items-center justify-center">
                                        <CreditCard className="h-6 w-6 text-slate-400" />
                                    </div>
                                )}
                                <div>
                                    <p className="font-medium text-slate-900">
                                        {booking.service?.name || 'Reservation'}
                                    </p>
                                    {booking.provider?.profile && (
                                        <p className="text-sm text-slate-500">
                                            avec {booking.provider.profile.firstName} {booking.provider.profile.lastName}
                                        </p>
                                    )}
                                    {booking.sessionDate && (
                                        <p className="text-sm text-slate-500">
                                            {new Date(booking.sessionDate).toLocaleDateString('fr-FR')}
                                            {booking.sessionTime && ` a ${booking.sessionTime}`}
                                        </p>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="p-6 bg-slate-50 border-b border-slate-100">
                        <div className="flex items-center justify-between">
                            <span className="text-slate-600">Total a payer</span>
                            <span className="text-2xl font-bold text-slate-900">
                                {booking ? `${booking.totalPrice.toFixed(2)} EUR` : '--'}
                            </span>
                        </div>
                    </div>

                    <div className="p-6">
                        {paymentSuccess ? (
                            <SuccessView />
                        ) : clientSecret && stripePromise ? (
                            <Elements
                                stripe={stripePromise}
                                options={{
                                    clientSecret,
                                    appearance: {
                                        theme: 'stripe',
                                        variables: {
                                            colorPrimary: '#4F46E5',
                                            borderRadius: '12px',
                                        },
                                    },
                                }}
                            >
                                <CheckoutForm bookingId={bookingId} onSuccess={handleSuccess} />
                            </Elements>
                        ) : (
                            <p className="text-center text-slate-500">
                                Impossible de charger le formulaire de paiement
                            </p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
