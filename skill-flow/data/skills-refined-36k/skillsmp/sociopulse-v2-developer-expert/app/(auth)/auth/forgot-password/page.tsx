'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Mail, ChevronLeft, ChevronRight, Loader2, CheckCircle } from 'lucide-react';
import Link from 'next/link';

const forgotSchema = z.object({
    email: z.string().email('Email invalide'),
});

type ForgotSchema = z.infer<typeof forgotSchema>;

export default function ForgotPasswordPage() {
    const [isLoading, setIsLoading] = useState(false);
    const [isSuccess, setIsSuccess] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<ForgotSchema>({
        resolver: zodResolver(forgotSchema),
    });

    const onSubmit = async (data: ForgotSchema) => {
        setIsLoading(true);
        // TODO: Implement password reset API call
        // await fetch('/api/v1/auth/forgot-password', { ... })
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        setIsSuccess(true);
        setIsLoading(false);
    };

    if (isSuccess) {
        return (
            <div className="min-h-screen bg-slate-50 flex flex-col justify-center items-center p-4">
                <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 text-center space-y-6">
                    <div className="w-16 h-16 mx-auto bg-green-100 rounded-full flex items-center justify-center">
                        <CheckCircle className="w-8 h-8 text-green-600" />
                    </div>
                    <div className="space-y-2">
                        <h1 className="text-2xl font-bold text-slate-900">Email envoyé !</h1>
                        <p className="text-slate-500">
                            Si un compte existe avec cet email, vous recevrez un lien de réinitialisation.
                        </p>
                    </div>
                    <Link 
                        href="/auth/login"
                        className="inline-flex items-center gap-2 text-brand-600 font-semibold hover:text-brand-700"
                    >
                        <ChevronLeft className="w-4 h-4" />
                        Retour à la connexion
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col justify-center items-center p-4">
            <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8 space-y-6">
                <div className="text-center space-y-2">
                    <h1 className="text-3xl font-bold text-slate-900">Mot de passe oublié</h1>
                    <p className="text-slate-500">
                        Entrez votre email pour recevoir un lien de réinitialisation
                    </p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    <div className="space-y-1">
                        <label className="text-sm font-medium text-slate-700">Email</label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
                            <input
                                {...register('email')}
                                type="email"
                                placeholder="vous@exemple.com"
                                className={`w-full pl-10 pr-4 py-3 rounded-xl border bg-slate-50 focus:bg-white transition-all outline-none focus:ring-2 focus:ring-brand-500/20 ${
                                    errors.email ? 'border-red-500 focus:border-red-500' : 'border-slate-200 focus:border-brand-500'
                                }`}
                            />
                        </div>
                        {errors.email && (
                            <p className="text-sm text-red-500 px-1">{errors.email.message}</p>
                        )}
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-3 rounded-xl transition-all active:scale-[0.98] flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <>
                                Envoyer le lien
                                <ChevronRight className="w-5 h-5" />
                            </>
                        )}
                    </button>
                </form>

                <div className="text-center pt-4 border-t border-slate-100">
                    <Link 
                        href="/auth/login" 
                        className="inline-flex items-center gap-2 text-sm text-slate-600 hover:text-slate-900"
                    >
                        <ChevronLeft className="w-4 h-4" />
                        Retour à la connexion
                    </Link>
                </div>
            </div>
        </div>
    );
}
