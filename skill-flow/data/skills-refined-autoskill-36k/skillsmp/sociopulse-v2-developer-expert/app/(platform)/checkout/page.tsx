'use client';

import { useEffect, useState, useMemo } from 'react';
import { useSearchParams } from 'next/navigation';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { createPaymentIntent } from '@/app/(platform)/services/payment.service';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || '');

function CheckoutForm() {
    const stripe = useStripe();
    const elements = useElements();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError(null);

        if (!stripe || !elements) {
            return;
        }

        setIsSubmitting(true);

        const { error: stripeError } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: `${window.location.origin}/checkout/success`,
            },
        });

        if (stripeError) {
            setError(stripeError.message || 'Une erreur est survenue lors du paiement.');
            setIsSubmitting(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <PaymentElement />
            {error && (
                <p className="text-sm text-red-600">
                    {error}
                </p>
            )}
            <button
                type="submit"
                disabled={!stripe || isSubmitting}
                className={`w-full h-11 rounded-xl font-semibold text-white text-sm transition-colors ${
                    !stripe || isSubmitting
                        ? 'bg-slate-400 cursor-not-allowed'
                        : 'bg-brand-600 hover:bg-brand-700'
                }`}
            >
                {isSubmitting ? 'Paiement en cours...' : 'Payer'}
            </button>
        </form>
    );
}

export default function CheckoutPage() {
    const searchParams = useSearchParams();
    const [clientSecret, setClientSecret] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const { amount, plan } = useMemo(() => {
        const amountParam = searchParams.get('amount');
        const planParam = searchParams.get('plan') || 'PRO';

        const parsedAmount = amountParam ? parseInt(amountParam, 10) : NaN;
        const normalizedAmount = Number.isFinite(parsedAmount) && parsedAmount > 0 ? parsedAmount : 2900;

        return {
            amount: normalizedAmount,
            plan: planParam,
        };
    }, [searchParams]);

    useEffect(() => {
        const createIntent = async () => {
            try {
                const result = await createPaymentIntent(amount, 'eur', {
                    product: 'subscription',
                    plan,
                });
                setClientSecret(result.clientSecret);
            } catch (err) {
                console.error('createPaymentIntent error', err);
                setError('Impossible d initialiser le paiement.');
            } finally {
                setIsLoading(false);
            }
        };

        createIntent();
    }, [amount, plan]);

    const options = useMemo(
        () =>
            clientSecret
                ? {
                      clientSecret,
                      appearance: {
                          theme: 'flat',
                      } as any,
                  }
                : undefined,
        [clientSecret]
    );

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
            <div className="w-full max-w-md">
                <div className="mb-6 text-center">
                    <h1 className="text-xl font-semibold text-slate-900">Abonnement Pro</h1>
                    <p className="text-sm text-slate-500 mt-1">
                        Reglez votre abonnement de {(amount / 100).toFixed(2)} EUR pour acceder aux fonctionnalites avancees.
                    </p>
                </div>

                <div className="bg-white rounded-2xl shadow-soft border border-slate-100 p-6">
                    {isLoading && (
                        <div className="flex justify-center py-10">
                            <div className="w-6 h-6 border-2 border-slate-300 border-t-brand-600 rounded-full animate-spin" />
                        </div>
                    )}

                    {error && !isLoading && (
                        <p className="text-sm text-red-600 text-center">
                            {error}
                        </p>
                    )}

                    {!isLoading && !error && clientSecret && options && stripePromise && (
                        <Elements stripe={stripePromise} options={options}>
                            <CheckoutForm />
                        </Elements>
                    )}
                </div>
            </div>
        </div>
    );
}
