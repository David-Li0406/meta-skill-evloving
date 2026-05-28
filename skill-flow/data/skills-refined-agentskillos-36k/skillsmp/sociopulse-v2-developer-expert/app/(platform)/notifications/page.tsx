'use client';

import { useEffect, useMemo, useState } from 'react';
import Cookies from 'js-cookie';
import Link from 'next/link';
import { Bell, CheckCircle2, Clock, Inbox, Loader2 } from 'lucide-react';
import { getApiBaseWithVersion } from '@/lib/config';

type Notification = {
    id: string;
    type: string;
    title: string;
    message: string;
    link?: string | null;
    isRead: boolean;
    createdAt: string;
    readAt?: string | null;
};

const buildApiBase = getApiBaseWithVersion;

export default function NotificationsPage() {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [filter, setFilter] = useState<'all' | 'unread'>('all');
    const [loading, setLoading] = useState(true);
    const [markingRead, setMarkingRead] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const filteredNotifications = useMemo(() => {
        return filter === 'unread'
            ? notifications.filter((n) => !n.isRead)
            : notifications;
    }, [notifications, filter]);

    const fetchNotifications = async (unreadOnly = false) => {
        const token = Cookies.get('accessToken');
        if (!token) {
            setError('Session expiree, merci de vous reconnecter.');
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            const baseUrl = buildApiBase();
            const response = await fetch(`${baseUrl}/notifications?unreadOnly=${unreadOnly}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                cache: 'no-store',
            });

            if (!response.ok) {
                throw new Error('Impossible de recuperer les notifications');
            }

            const data = await response.json();
            setNotifications(data);
            setError(null);
        } catch (err: any) {
            setError(err.message || 'Erreur lors du chargement');
        } finally {
            setLoading(false);
        }
    };

    const markAllAsRead = async () => {
        const token = Cookies.get('accessToken');
        if (!token) return;
        try {
            setMarkingRead(true);
            const baseUrl = buildApiBase();
            const response = await fetch(`${baseUrl}/notifications/mark-all-read`, {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (!response.ok) {
                throw new Error('Impossible de marquer comme lu');
            }
            setNotifications((prev) =>
                prev.map((n) => ({ ...n, isRead: true, readAt: new Date().toISOString() })),
            );
        } catch (err) {
            setError('Echec du marquage des notifications');
        } finally {
            setMarkingRead(false);
        }
    };

    useEffect(() => {
        fetchNotifications(filter === 'unread');
    }, [filter]);

    const renderNotificationCard = (notification: Notification) => {
        const createdAt = new Date(notification.createdAt);
        const dateLabel = createdAt.toLocaleString('fr-FR');

        return (
            <div
                key={notification.id}
                className={`p-4 rounded-2xl border transition-all bg-white ${notification.isRead ? 'border-slate-200' : 'border-indigo-200 shadow-sm'
                    }`}
            >
                <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-teal-500 flex items-center justify-center text-white shadow-sm">
                            <Bell className="w-5 h-5" />
                        </div>
                        <div>
                            <p className="text-xs uppercase tracking-wide text-slate-400">{notification.type}</p>
                            <h3 className="text-base font-semibold text-slate-900">{notification.title}</h3>
                            <p className="text-sm text-slate-600 mt-1">{notification.message}</p>
                            <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                                <Clock className="w-3.5 h-3.5" />
                                <span>{dateLabel}</span>
                            </div>
                        </div>
                    </div>
                    {!notification.isRead && (
                        <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
                            <CheckCircle2 className="w-3 h-3" />
                            Non lue
                        </span>
                    )}
                </div>
                {notification.link && (
                    <Link
                        href={notification.link}
                        className="inline-flex items-center text-sm font-medium text-indigo-600 mt-3 hover:text-indigo-700"
                    >
                        Ouvrir
                    </Link>
                )}
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
            <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                        <p className="text-sm text-slate-500">Centre de notifications</p>
                        <h1 className="text-2xl font-bold text-slate-900">Vos alertes & mises a jour</h1>
                    </div>
                    <div className="flex items-center gap-3">
                        <div className="inline-flex rounded-full bg-white border border-slate-200 p-1">
                            <button
                                onClick={() => setFilter('all')}
                                className={`px-3 py-1.5 rounded-full text-sm font-medium ${filter === 'all' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-600'
                                    }`}
                            >
                                Toutes
                            </button>
                            <button
                                onClick={() => setFilter('unread')}
                                className={`px-3 py-1.5 rounded-full text-sm font-medium ${filter === 'unread' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-600'
                                    }`}
                            >
                                Non lues
                            </button>
                        </div>
                        <button
                            onClick={markAllAsRead}
                            disabled={markingRead || notifications.length === 0}
                            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white border border-slate-200 text-sm font-medium text-slate-700 hover:border-slate-300 disabled:opacity-50"
                        >
                            {markingRead ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
                            Tout marquer comme lu
                        </button>
                    </div>
                </div>

                {error && (
                    <div className="p-4 rounded-xl border border-red-200 bg-red-50 text-sm text-red-700">
                        {error}
                    </div>
                )}

                {loading ? (
                    <div className="flex items-center justify-center py-16">
                        <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" />
                    </div>
                ) : filteredNotifications.length === 0 ? (
                    <div className="text-center py-16 bg-white border border-slate-200 rounded-2xl">
                        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-slate-100 flex items-center justify-center">
                            <Inbox className="w-8 h-8 text-slate-400" />
                        </div>
                        <h2 className="text-lg font-semibold text-slate-900">Aucune notification</h2>
                        <p className="text-sm text-slate-500 mt-2">Vous serez alerte ici des prochaines mises a jour.</p>
                    </div>
                ) : (
                    <div className="grid gap-4">
                        {filteredNotifications.map((notification) => renderNotificationCard(notification))}
                    </div>
                )}
            </div>
        </div>
    );
}
