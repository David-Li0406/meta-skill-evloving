'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Loader2, Mail, Lock, ChevronRight, User, Sparkles, Clock, Shield, CheckCircle2 } from 'lucide-react';
import { auth } from '@/lib/auth';
import { useToasts, ToastContainer } from '@/components/ui/Toast';
import { Logo } from '@/components/ui/Logo';
import { motion } from 'framer-motion';

// ===========================================
// LOGIN PAGE - Two Column Layout
// Left: Register CTA | Right: Login Form
// ===========================================

const loginSchema = z.object({
    email: z.string().email('Email invalide'),
    password: z.string().min(1, 'Mot de passe requis'),
});

type LoginSchema = z.infer<typeof loginSchema>;

const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';
    const normalized = apiBase.replace(/\/+$/, '');
    return normalized.endsWith('/api/v1') ? normalized : `${normalized}/api/v1`;
};

const REGISTER_BENEFITS = [
    { icon: Clock, text: "Inscription en 2 minutes" },
    { icon: Shield, text: "Vérification sécurisée" },
    { icon: CheckCircle2, text: "Accès immédiat aux opportunités" },
];

export default function LoginPage() {
    const router = useRouter();
    const { toasts, addToast, removeToast } = useToasts();
    const [isLoading, setIsLoading] = useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginSchema>({
        resolver: zodResolver(loginSchema),
    });

    const onSubmit = async (data: LoginSchema) => {
        setIsLoading(true);
        try {
            const response = await auth.login(data.email, data.password);
            auth.setToken(response.accessToken);

            const hostname = typeof window !== 'undefined' ? window.location.hostname : '';
            const isDashHost = hostname.startsWith('dash.');

            // V2: Role-based redirect after login
            let redirectPath = '/';

            try {
                const meRes = await fetch(`${getApiBase()}/auth/me`, {
                    headers: { Authorization: `Bearer ${response.accessToken}` },
                });

                if (meRes.ok) {
                    const user = await meRes.json();
                    const role = String(user?.role).toUpperCase();

                    // V2 Role-based routing
                    if (role === 'ADMIN') {
                        redirectPath = '/admin';
                    } else if (role === 'CLIENT') {
                        redirectPath = '/dashboard/client';
                    } else if (role === 'TALENT') {
                        redirectPath = '/dashboard/talent';
                    } else {
                        // Fallback for unknown roles
                        redirectPath = '/';
                    }

                    // If on dash subdomain but not admin, logout
                    if (isDashHost && role !== 'ADMIN') {
                        auth.logout();
                        return;
                    }
                }
            } catch {
                // If /auth/me fails, redirect to landing
                redirectPath = '/';
            }

            addToast({
                message: 'Connexion réussie ! Redirection...',
                type: 'success',
            });

            setTimeout(() => {
                router.push(redirectPath);
                router.refresh();
            }, 800);
        } catch (error: any) {
            addToast({
                message: error.message || 'Erreur lors de la connexion',
                type: 'error',
            });
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12">
            <div className="w-full max-w-5xl grid lg:grid-cols-2 gap-8 lg:gap-12 items-stretch">

                {/* LEFT COLUMN - Register CTA */}
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5 }}
                    className="hidden lg:flex flex-col justify-center p-10 rounded-3xl bg-gradient-to-br from-indigo-600 via-indigo-500 to-teal-500 text-white shadow-2xl shadow-indigo-500/30"
                >
                    <div className="space-y-6">
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 backdrop-blur-sm text-sm font-medium">
                            <Sparkles className="w-4 h-4" />
                            Nouveau sur la plateforme ?
                        </div>

                        <h2 className="text-3xl font-bold leading-tight">
                            Créer un compte
                            <br />
                            <span className="text-white/90">en 2 minutes</span>
                        </h2>

                        <p className="text-white/80 text-lg leading-relaxed">
                            Rejoignez la communauté des professionnels du médico-social.
                            Trouvez des missions ou proposez vos services.
                        </p>

                        <ul className="space-y-4 pt-4">
                            {REGISTER_BENEFITS.map((benefit, index) => (
                                <li key={index} className="flex items-center gap-3">
                                    <div className="h-10 w-10 rounded-xl bg-white/20 flex items-center justify-center">
                                        <benefit.icon className="w-5 h-5" />
                                    </div>
                                    <span className="font-medium">{benefit.text}</span>
                                </li>
                            ))}
                        </ul>

                        <Link
                            href="/onboarding"
                            className="inline-flex items-center gap-2 mt-6 px-8 py-4 rounded-2xl bg-white text-indigo-600 font-bold text-lg shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-transform"
                        >
                            <User className="w-5 h-5" />
                            S'inscrire maintenant
                            <ChevronRight className="w-5 h-5" />
                        </Link>
                    </div>
                </motion.div>

                {/* RIGHT COLUMN - Login Form */}
                <motion.div
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                    className="bg-white/90 backdrop-blur-xl shadow-xl shadow-slate-200/50 border border-slate-100 rounded-3xl p-8 sm:p-10 w-full flex flex-col justify-center"
                >
                    <div className="flex flex-col items-center gap-6 mb-8">
                        <Logo size="lg" showBaseline={false} />
                        <div className="text-center space-y-2">
                            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Se connecter</h1>
                            <p className="text-slate-500">Accédez à votre espace professionnel</p>
                        </div>
                    </div>

                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
                        <div className="space-y-1 group">
                            <label className="text-sm font-medium text-slate-700 ml-1">Email</label>
                            <div className="relative transition-all duration-300">
                                <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors w-5 h-5" />
                                <input
                                    {...register('email')}
                                    type="email"
                                    placeholder="exemple@sociopulse.com"
                                    className={`w-full pl-12 pr-4 py-3.5 rounded-2xl border bg-slate-50/50 focus:bg-white transition-all outline-none focus:ring-4 focus:ring-indigo-500/10 placeholder:text-slate-400 ${errors.email
                                        ? 'border-red-300 focus:border-red-500'
                                        : 'border-slate-200 focus:border-indigo-500 hover:border-slate-300'
                                        }`}
                                />
                            </div>
                            {errors.email && <p className="text-sm text-red-500 px-2 font-medium">{errors.email.message}</p>}
                        </div>

                        <div className="space-y-1 group">
                            <div className="flex justify-between items-center px-1">
                                <label className="text-sm font-medium text-slate-700">Mot de passe</label>
                                <Link
                                    href="/auth/forgot-password"
                                    className="text-xs text-indigo-600 hover:text-indigo-700 font-semibold transition-colors"
                                >
                                    Mot de passe oublié ?
                                </Link>
                            </div>
                            <div className="relative transition-all duration-300">
                                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors w-5 h-5" />
                                <input
                                    {...register('password')}
                                    type="password"
                                    placeholder="••••••••"
                                    className={`w-full pl-12 pr-4 py-3.5 rounded-2xl border bg-slate-50/50 focus:bg-white transition-all outline-none focus:ring-4 focus:ring-indigo-500/10 placeholder:text-slate-400 ${errors.password
                                        ? 'border-red-300 focus:border-red-500'
                                        : 'border-slate-200 focus:border-indigo-500 hover:border-slate-300'
                                        }`}
                                />
                            </div>
                            {errors.password && <p className="text-sm text-red-500 px-2 font-medium">{errors.password.message}</p>}
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-gradient-to-r from-indigo-600 to-teal-500 hover:scale-[1.02] active:scale-[0.98] text-white font-bold py-3.5 rounded-2xl shadow-lg shadow-indigo-500/20 transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed disabled:hover:scale-100 mt-2"
                        >
                            {isLoading ? (
                                <Loader2 className="w-5 h-5 animate-spin" />
                            ) : (
                                <>
                                    Se connecter
                                    <ChevronRight className="w-5 h-5 stroke-[2.5]" />
                                </>
                            )}
                        </button>
                    </form>

                    {/* Mobile only - Register link */}
                    <div className="lg:hidden text-center pt-8 mt-2 border-t border-slate-100">
                        <p className="text-sm text-slate-500">
                            Pas encore de compte ?{' '}
                            <Link href="/onboarding" className="text-indigo-600 font-bold hover:text-indigo-700 transition-colors">
                                Créer un compte en 2 minutes
                            </Link>
                        </p>
                    </div>

                    <ToastContainer toasts={toasts} onRemove={removeToast} />
                </motion.div>
            </div>
        </div>
    );
}
