'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { toast } from 'sonner';
import { awardPoints, getMyGrowthSummary, type GrowthSummary } from '@/app/(platform)/services/growth.service';
import { GamificationWidget } from './GamificationWidget';
import { ReferralCard } from './ReferralCard';

async function fireConfettiOnce(storageKey: string) {
    if (typeof window === 'undefined') return;
    if (window.localStorage.getItem(storageKey)) return;

    window.localStorage.setItem(storageKey, '1');

    try {
        const confetti = (await import('canvas-confetti')).default;
        confetti({
            particleCount: 140,
            spread: 70,
            startVelocity: 35,
            origin: { y: 0.65 },
        });
    } catch {
        // ignore if dependency not available
    }
}

export function GrowthDashboardWidgets() {
    const [summary, setSummary] = useState<GrowthSummary | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const hasCheckedPhotoQuest = useRef(false);

    const refresh = useCallback(async () => {
        setIsLoading(true);
        try {
            const data = await getMyGrowthSummary();
            setSummary(data);
        } catch (error) {
            console.error('getMyGrowthSummary failed', error);
            toast.error("Impossible de charger l'espace Growth.");
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        refresh();
    }, [refresh]);

    useEffect(() => {
        if (!summary?.profile?.avatarUrl) return;
        if (hasCheckedPhotoQuest.current) return;
        hasCheckedPhotoQuest.current = true;

        awardPoints('PROFILE_PHOTO')
            .then(async (result) => {
                if (!result.awarded) return;
                toast.success(`🏆 +${result.amount} points !`);
                await fireConfettiOnce('sociopulse_confetti_first_quest_v1');
                await refresh();
            })
            .catch((error) => {
                const message = error instanceof Error ? error.message : null;
                toast.error(message || "Impossible de valider la quête 'Photo'.");
            });
    }, [refresh, summary?.profile?.avatarUrl]);

    return (
        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
                <GamificationWidget summary={summary} isLoading={isLoading} />
            </div>
            <div className="lg:col-span-1">
                <ReferralCard
                    referralCode={summary?.referralCode ?? null}
                    pendingCount={summary?.referrals.pendingCount ?? 0}
                    confirmedCount={summary?.referrals.confirmedCount ?? 0}
                    pendingPoints={summary?.pendingPoints ?? 0}
                />
            </div>
        </section>
    );
}

