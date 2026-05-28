'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { CheckCircle2, Circle, Gift, Loader2, Sparkles } from 'lucide-react';
import type { GrowthSummary } from '@/app/(platform)/services/growth.service';

export interface GamificationWidgetProps {
    summary: GrowthSummary | null;
    isLoading?: boolean;
}

function computeCompletion(summary: GrowthSummary | null) {
    if (!summary) return 0;

    const tagsDone = summary.tags.length > 0;
    const avatarDone = Boolean(summary.profile?.avatarUrl);
    const invited = summary.referrals.pendingCount + summary.referrals.confirmedCount > 0;

    const completion =
        (tagsDone ? 20 : 0) +
        (avatarDone ? 50 : 0) +
        (invited ? 30 : 0);

    return Math.max(0, Math.min(100, completion));
}

export function GamificationWidget({ summary, isLoading }: GamificationWidgetProps) {
    const completion = computeCompletion(summary);
    const tagsDone = Boolean(summary && summary.tags.length > 0);
    const avatarDone = Boolean(summary?.profile?.avatarUrl);
    const invited = Boolean(summary && summary.referrals.pendingCount + summary.referrals.confirmedCount > 0);

    return (
        <div className="bg-white rounded-2xl shadow-soft border border-slate-100 p-6 space-y-6">
            <div className="flex items-start justify-between gap-4">
                <div className="space-y-1">
                    <p className="label-sm">Growth</p>
                    <h3 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-brand-600" />
                        Profil complété à {completion}%
                    </h3>
                    <p className="text-sm text-slate-600">
                        {isLoading ? 'Chargement…' : `${summary?.points ?? 0} points · ${summary?.pendingPoints ?? 0} en attente`}
                    </p>
                </div>
                <div className="shrink-0 w-12 h-12 rounded-2xl bg-slate-900 text-white flex items-center justify-center">
                    {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Gift className="w-5 h-5" />}
                </div>
            </div>

            <div className="space-y-2">
                <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-gradient-to-r from-brand-600 to-teal-500 rounded-full"
                        initial={{ width: 0 }}
                        animate={{ width: `${completion}%` }}
                        transition={{ type: 'spring', stiffness: 120, damping: 20 }}
                    />
                </div>
                <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Début</span>
                    <span>100%</span>
                </div>
            </div>

            <div className="space-y-3">
                <p className="text-sm font-semibold text-slate-900">Quêtes</p>

                <div className="space-y-2">
                    <div className="flex items-start gap-3 rounded-2xl border border-slate-200 p-4">
                        {tagsDone ? (
                            <CheckCircle2 className="w-5 h-5 text-green-600 shrink-0 mt-0.5" />
                        ) : (
                            <Circle className="w-5 h-5 text-slate-300 shrink-0 mt-0.5" />
                        )}
                        <div className="flex-1">
                            <p className="text-sm font-semibold text-slate-900">Sélectionner vos tags</p>
                            <p className="text-sm text-slate-600">Personnalisez votre expérience.</p>
                        </div>
                        {!tagsDone ? (
                            <Link href="/onboarding" className="btn-secondary !px-3 !py-2">
                                Continuer
                            </Link>
                        ) : null}
                    </div>

                    <div className="flex items-start gap-3 rounded-2xl border border-slate-200 p-4">
                        {avatarDone ? (
                            <CheckCircle2 className="w-5 h-5 text-green-600 shrink-0 mt-0.5" />
                        ) : (
                            <Circle className="w-5 h-5 text-slate-300 shrink-0 mt-0.5" />
                        )}
                        <div className="flex-1">
                            <p className="text-sm font-semibold text-slate-900">Ajouter une photo (+50 pts)</p>
                            <p className="text-sm text-slate-600">Améliore la confiance et votre visibilité.</p>
                        </div>
                        {!avatarDone ? (
                            <Link href="/settings" className="btn-secondary !px-3 !py-2">
                                Ajouter
                            </Link>
                        ) : null}
                    </div>

                    <div className="flex items-start gap-3 rounded-2xl border border-slate-200 p-4">
                        {invited ? (
                            <CheckCircle2 className="w-5 h-5 text-green-600 shrink-0 mt-0.5" />
                        ) : (
                            <Circle className="w-5 h-5 text-slate-300 shrink-0 mt-0.5" />
                        )}
                        <div className="flex-1">
                            <p className="text-sm font-semibold text-slate-900">Inviter un collègue (+200 pts)</p>
                            <p className="text-sm text-slate-600">
                                Les points sont validés après vérification d’identité.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

