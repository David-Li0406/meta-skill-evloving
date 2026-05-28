'use client';

import { useEffect, useMemo, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { SignaturePad } from '@/components/ui/SignaturePad';
import { ToastContainer, useToasts } from '@/components/ui/Toast';
import { getMissionById } from '@/app/(platform)/services/matching.service';
import { signContract } from '@/app/(platform)/services/contract.service';
import { CheckCircle2, ShieldAlert, MapPin, Calendar, Coins } from 'lucide-react';

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

interface PageProps {
    params: { id: string };
}

export default function MissionContractPage({ params }: PageProps) {
    const missionId = useMemo(() => params.id, [params.id]);
    const router = useRouter();
    const { toasts, addToast, removeToast } = useToasts();
    const [mission, setMission] = useState<MissionInfo | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isSigning, setIsSigning] = useState(false);
    const currentUserId = useMemo(() => decodeUserId(), []);

    const fetchMission = useCallback(async () => {
        setIsLoading(true);
        setError(null);
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
            setError('Erreur lors du chargement de la mission ou du contrat.');
        } finally {
            setIsLoading(false);
        }
    }, [missionId]);

    useEffect(() => {
        fetchMission();
    }, [fetchMission]);

    const handleSignatureSave = async (dataUrl: string) => {
        if (!mission) return;
        setIsSigning(true);
        try {
            await signContract(mission.id, dataUrl);
            setMission({
                ...mission,
                contract: {
                    status: 'SIGNED',
                    signatureUrl: dataUrl,
                    signedAt: new Date().toISOString(),
                },
            });
            addToast({ message: 'Contrat signe avec succes', type: 'success' });
            router.push(`/dashboard/missions/${mission.id}`);
        } catch (err) {
            console.error('signContract error', err);
            addToast({ message: 'Erreur lors de la signature du contrat', type: 'error' });
        } finally {
            setIsSigning(false);
        }
    };

    const isSigned = mission?.contract?.status === 'SIGNED';
    const isAuthorized =
        !!mission?.assignedTalentId && !!currentUserId && mission.assignedTalentId === currentUserId;

    return (
        <div className="min-h-screen bg-slate-100 py-10 px-4">
            <ToastContainer toasts={toasts} onRemove={removeToast} />
            <div className="max-w-4xl mx-auto">
                <div className="mb-6">
                    <h1 className="text-2xl font-semibold text-slate-900">Contrat de mission</h1>
                    <p className="text-sm text-slate-500">
                        Mission #{missionId}
                    </p>
                </div>

                {isLoading && (
                    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 animate-pulse space-y-4">
                        <div className="h-4 w-40 bg-slate-200 rounded" />
                        <div className="h-3 w-64 bg-slate-100 rounded" />
                        <div className="h-3 w-52 bg-slate-100 rounded" />
                        <div className="h-48 w-full bg-slate-100 rounded" />
                    </div>
                )}

                {!isLoading && error && (
                    <div className="bg-white rounded-2xl border border-red-200 shadow-sm p-6 text-red-700">
                        {error}
                    </div>
                )}

                {!isLoading && mission && !error && (
                    <div className="bg-white rounded-2xl border border-slate-200 shadow-md p-8 space-y-6">
                        <div className="flex items-center justify-between">
                            <div className="space-y-1">
                                <h2 className="text-xl font-semibold text-slate-900">{mission.title}</h2>
                                <p className="text-sm text-slate-500">{mission.jobTitle}</p>
                            </div>
                            {isSigned ? (
                                <span className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-50 text-emerald-700 text-xs font-semibold">
                                    <CheckCircle2 className="w-4 h-4" />
                                    Contrat signe
                                </span>
                            ) : (
                                <span className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-50 text-amber-700 text-xs font-semibold">
                                    <ShieldAlert className="w-4 h-4" />
                                    Signature requise
                                </span>
                            )}
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm text-slate-600">
                            <div className="flex items-center gap-2">
                                <Calendar className="w-4 h-4 text-slate-400" />
                                <span>
                                    Debut:{' '}
                                    {mission.startDate
                                        ? new Date(mission.startDate).toLocaleDateString('fr-FR')
                                        : 'Non renseigne'}
                                </span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Coins className="w-4 h-4 text-slate-400" />
                                <span>
                                    Tarif horaire: {mission.hourlyRate ? `${mission.hourlyRate} EUR/h` : 'Non renseigne'}
                                </span>
                            </div>
                            <div className="flex items-center gap-2">
                                <MapPin className="w-4 h-4 text-slate-400" />
                                <span>{mission.city || mission.address || 'Lieu non renseigne'}</span>
                            </div>
                        </div>

                        <div className="border border-slate-200 rounded-xl p-6 bg-white font-serif text-slate-800 leading-relaxed">
                            <h3 className="text-lg font-semibold mb-4">Contrat de mise a disposition</h3>
                            <p className="mb-3">
                                Entre l etablissement (client) et l Extra (prestataire), il est convenu que l Extra
                                realise la mission ci-dessus de maniere professionnelle, en respectant la deontologie
                                et les consignes de l etablissement. La remuneration horaire convenue est de{' '}
                                {mission.hourlyRate ? `${mission.hourlyRate} EUR/h` : '____ EUR/h'}, pour une
                                intervention a {mission.city || '____'} a compter du{' '}
                                {mission.startDate ? new Date(mission.startDate).toLocaleDateString('fr-FR') : '____'}.
                            </p>
                            <p className="mb-3">
                                L Extra s engage a respecter les horaires, consignes de securite, confidentialite et
                                protocoles internes. Toute modification ou annulation devra etre notifiee a
                                l etablissement dans les meilleurs delais.
                            </p>
                            <p className="mb-3">
                                La signature ci-dessous atteste de l acceptation des conditions de mise a disposition et
                                de la prise de connaissance des informations relatives a la mission.
                            </p>
                        </div>

                        {isSigned && mission.contract?.signatureUrl ? (
                            <div className="space-y-3">
                                <p className="text-sm text-slate-600">Signature apposee le {mission.contract.signedAt ? new Date(mission.contract.signedAt).toLocaleString('fr-FR') : ''}</p>
                                <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                                    <img src={mission.contract.signatureUrl} alt="Signature" className="h-32 object-contain" />
                                </div>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                <p className="text-sm text-slate-600">
                                    Merci de signer ci-dessous pour valider le contrat.
                                </p>

                                {!isAuthorized && (
                                    <div className="rounded-lg border border-amber-200 bg-amber-50 text-amber-700 text-sm px-4 py-3">
                                        Cette mission n est pas assignee a votre compte. Signature impossible.
                                    </div>
                                )}

                                {isAuthorized && (
                                    <div className="border border-slate-200 rounded-xl p-4 bg-slate-50">
                                        <SignaturePad onSave={handleSignatureSave} />
                                        {isSigning && (
                                            <p className="text-xs text-slate-500 mt-2">Enregistrement de la signature...</p>
                                        )}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

