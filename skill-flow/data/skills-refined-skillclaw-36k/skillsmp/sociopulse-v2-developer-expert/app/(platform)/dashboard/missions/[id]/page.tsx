'use client';

import { useEffect, useMemo, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Users, MapPin, Send, Award, AlertCircle, CheckCircle2, Shield } from 'lucide-react';
import { ToastContainer, useToasts } from '@/components/ui/Toast';
import { getMissionCandidates, getMissionById } from '@/app/(platform)/services/matching.service';

type Candidate = {
    id: string;
    name: string;
    score?: number;
    skills?: string[];
    distanceKm?: number;
};

interface PageProps {
    params: { id: string };
}

type ContractStatus = 'PENDING' | 'SIGNED';

type MissionInfo = {
    id: string;
    title: string;
    jobTitle?: string;
    hourlyRate?: number;
    city?: string;
    address?: string;
    startDate?: string;
    assignedTalentId?: string;
    contract?: {
        status?: ContractStatus;
        signatureUrl?: string;
        signedAt?: string;
    };
};

const decodeUserId = () => {
    if (typeof window === 'undefined') return null;
    const token =
        window.localStorage.getItem('accessToken') ||
        window.localStorage.getItem('token') ||
        window.localStorage.getItem('jwt');
    if (!token) return null;
    try {
        const cleaned = token.replace(/^Bearer\\s+/i, '').trim();
        const parts = cleaned.split('.');
        if (parts.length < 2) return null;
        const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')));
        return payload.sub || payload.id || null;
    } catch {
        return null;
    }
};

const SkeletonCard = () => (
    <div className="rounded-2xl border border-slate-100 bg-white shadow-soft p-5 animate-pulse space-y-3">
        <div className="h-4 w-32 bg-slate-200 rounded" />
        <div className="h-3 w-20 bg-slate-100 rounded" />
        <div className="flex gap-2 flex-wrap">
            <div className="h-6 w-16 bg-slate-100 rounded-full" />
            <div className="h-6 w-20 bg-slate-100 rounded-full" />
        </div>
        <div className="h-8 w-28 bg-slate-200 rounded-lg" />
    </div>
);

export default function MissionDetailPage({ params }: PageProps) {
    const missionId = useMemo(() => params.id, [params.id]);
    const [candidates, setCandidates] = useState<Candidate[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [mission, setMission] = useState<MissionInfo | null>(null);
    const [isMissionLoading, setIsMissionLoading] = useState(true);
    const currentUserId = useMemo(() => decodeUserId(), []);
    const router = useRouter();
    const { toasts, addToast, removeToast } = useToasts();

    const fetchMission = useCallback(async () => {
        setIsMissionLoading(true);
        try {
            const response = await getMissionById(missionId);
            const mapped: MissionInfo = {
                id: response?.id || missionId,
                title: response?.title || response?.jobTitle || 'Mission',
                jobTitle: response?.jobTitle,
                hourlyRate: response?.hourlyRate,
                city: response?.city,
                address: response?.address,
                startDate: response?.startDate,
                assignedTalentId: response?.assignedTalentId,
                contract: response?.contract
                    ? {
                          status: response.contract.status,
                          signatureUrl: response.contract.signatureUrl,
                          signedAt: response.contract.signedAt,
                      }
                    : undefined,
            };
            setMission(mapped);
        } catch (err) {
            console.error('getMissionById error', err);
            setError('Erreur lors du chargement de la mission');
            addToast({ message: 'Erreur lors du chargement de la mission', type: 'error' });
        } finally {
            setIsMissionLoading(false);
        }
    }, [addToast, missionId]);

    const fetchCandidates = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await getMissionCandidates(missionId);
            const list =
                (Array.isArray(response) && response) ||
                (Array.isArray(response?.items) && response.items) ||
                (Array.isArray(response?.candidates) && response.candidates) ||
                [];

            const mapped = list.map((c: any): Candidate => ({
                id: c?.id || c?.userId || '',
                name: c?.name || c?.fullName || c?.displayName || 'Candidat',
                score: c?.matchScore ?? c?.score ?? undefined,
                skills: Array.isArray(c?.skills) ? c.skills : Array.isArray(c?.specialties) ? c.specialties : [],
                distanceKm: c?.distanceKm ?? c?.distance ?? undefined,
            }));

            setCandidates(mapped);
        } catch (err) {
            console.error('getMissionCandidates error', err);
            setError('Erreur lors du chargement des candidats');
            addToast({ message: 'Erreur lors du chargement des candidats', type: 'error' });
        } finally {
            setIsLoading(false);
        }
    }, [addToast, missionId]);

    useEffect(() => {
        fetchCandidates();
        fetchMission();
    }, [fetchCandidates, fetchMission]);

    const handleContact = (candidateId: string) => {
        router.push(`/messages?recipientId=${encodeURIComponent(candidateId)}`);
    };

    const renderContent = () => {
        if (isLoading) {
            return (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Array.from({ length: 6 }).map((_, idx) => (
                        <SkeletonCard key={idx} />
                    ))}
                </div>
            );
        }

        if (error) {
            return (
                <div className="flex items-center gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                    <AlertCircle className="w-4 h-4" />
                    <span>{error}</span>
                </div>
            );
        }

        if (candidates.length === 0) {
            return (
                <div className="flex flex-col items-center gap-3 rounded-2xl border border-slate-100 bg-white px-6 py-10 shadow-soft text-center">
                    <Users className="w-8 h-8 text-slate-400" />
                    <p className="text-sm text-slate-500">Aucun candidat trouve pour le moment.</p>
                </div>
            );
        }

        return (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {candidates.map((candidate) => (
                    <div key={candidate.id} className="rounded-2xl border border-slate-100 bg-white shadow-soft p-5 space-y-3">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-semibold text-slate-900">{candidate.name}</p>
                                <p className="text-xs text-slate-400">Profil trouve</p>
                            </div>
                            {candidate.score !== undefined && (
                                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-semibold">
                                    <Award className="w-3.5 h-3.5" />
                                    {candidate.score}%
                                </span>
                            )}
                        </div>

                        {candidate.skills && candidate.skills.length > 0 && (
                            <div className="flex flex-wrap gap-1.5">
                                {candidate.skills.slice(0, 5).map((skill, idx) => (
                                    <span key={`${candidate.id}-skill-${idx}`} className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 text-xs">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        )}

                        <div className="flex items-center justify-between">
                            {candidate.distanceKm !== undefined ? (
                                <div className="inline-flex items-center gap-1 text-xs text-slate-500">
                                    <MapPin className="w-3 h-3" />
                                    <span>{candidate.distanceKm} km</span>
                                </div>
                            ) : (
                                <span className="text-xs text-slate-400">Distance inconnue</span>
                            )}

                            <button
                                type="button"
                                onClick={() => handleContact(candidate.id)}
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand-600 text-white text-xs font-semibold hover:bg-brand-700 transition-colors"
                            >
                                <Send className="w-3.5 h-3.5" />
                                Contacter
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-slate-50">
            <ToastContainer toasts={toasts} onRemove={removeToast} />
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
                <div className="flex items-center justify-between flex-wrap gap-3">
                    <div>
                        <p className="text-sm text-slate-500">Mission</p>
                        <h1 className="text-2xl font-semibold text-slate-900">
                            {mission?.title || 'Candidats trouves'}
                        </h1>
                        {mission?.city && (
                            <p className="text-sm text-slate-500">
                                {mission.city}
                            </p>
                        )}
                    </div>
                    <div className="flex items-center gap-2">
                        {mission && mission.contract?.status === 'SIGNED' ? (
                            <span className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-semibold">
                                <CheckCircle2 className="w-4 h-4" />
                                Contrat signe
                            </span>
                        ) : (
                            <Link
                                href={`/dashboard/missions/${missionId}/contract`}
                                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-semibold hover:bg-brand-700 transition-colors"
                            >
                                <Shield className="w-4 h-4" />
                                Signer le contrat
                            </Link>
                        )}
                        <button
                            type="button"
                            onClick={fetchCandidates}
                            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors"
                        >
                            <Users className="w-4 h-4" />
                            Rafraichir
                        </button>
                    </div>
                </div>

                {renderContent()}
            </div>
        </div>
    );
}

