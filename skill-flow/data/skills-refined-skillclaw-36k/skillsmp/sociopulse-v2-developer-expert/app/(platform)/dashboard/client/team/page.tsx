import { Plus, Search, Star, MessageCircle } from 'lucide-react';

export default function ClientTeamPage() {
    return (
        <div className="p-6 space-y-6">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900">
                        Mon Équipe
                    </h1>
                    <p className="text-slate-600">
                        Votre vivier de talents favoris et historique de collaborations.
                    </p>
                </div>
                <button className="inline-flex items-center gap-2 rounded-lg bg-purple-600 px-4 py-2 text-sm font-medium text-white hover:bg-purple-700">
                    <Plus className="h-4 w-4" />
                    Ajouter un Talent
                </button>
            </div>

            {/* Search */}
            <div className="relative">
                <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                <input
                    type="text"
                    placeholder="Rechercher un talent par nom, spécialité..."
                    className="w-full rounded-lg border border-slate-200 bg-white py-2.5 pl-10 pr-4 text-sm placeholder:text-slate-400 focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500"
                />
            </div>

            {/* Talent Pool Grid */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <TalentCard
                    name="Marie Lambert"
                    specialty="Aide-soignante"
                    rating={4.9}
                    missions={12}
                    tags={['Nuit', 'Weekend']}
                />
                <TalentCard
                    name="Thomas Durand"
                    specialty="Éducateur spécialisé"
                    rating={4.7}
                    missions={8}
                    tags={['Autisme', 'Adolescents']}
                />
                <TalentCard
                    name="Sophie Martin"
                    specialty="Art-thérapeute"
                    rating={5.0}
                    missions={5}
                    tags={['Séniors', 'Ateliers']}
                />
                <TalentCard
                    name="Pierre Dubois"
                    specialty="AMP"
                    rating={4.6}
                    missions={15}
                    tags={['EHPAD', 'Jour']}
                />
            </div>

            {/* Recent Conversations */}
            <div className="rounded-lg border border-slate-200 bg-white">
                <div className="border-b border-slate-200 px-6 py-4">
                    <h2 className="font-semibold text-slate-900">Conversations récentes</h2>
                </div>
                <div className="divide-y divide-slate-200">
                    <ConversationRow
                        name="Marie Lambert"
                        lastMessage="Parfait, je serai là demain à 20h."
                        time="Il y a 2h"
                        unread
                    />
                    <ConversationRow
                        name="Thomas Durand"
                        lastMessage="Merci pour la mission, c'était super !"
                        time="Hier"
                    />
                </div>
            </div>
        </div>
    );
}

interface TalentCardProps {
    name: string;
    specialty: string;
    rating: number;
    missions: number;
    tags: string[];
}

function TalentCard({ name, specialty, rating, missions, tags }: TalentCardProps) {
    return (
        <div className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="flex items-start gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-lg font-medium text-purple-600">
                    {name.charAt(0)}
                </div>
                <div className="flex-1">
                    <h3 className="font-semibold text-slate-900">{name}</h3>
                    <p className="text-sm text-slate-500">{specialty}</p>
                </div>
                <button
                    className="rounded-md p-1.5 text-slate-400 hover:bg-slate-100 hover:text-purple-600"
                    aria-label={`Envoyer un message à ${name}`}
                >
                    <MessageCircle className="h-5 w-5" />
                </button>
            </div>
            <div className="mt-3 flex items-center gap-4 text-sm">
                <span className="flex items-center gap-1 text-amber-500">
                    <Star className="h-4 w-4 fill-current" />
                    {rating}
                </span>
                <span className="text-slate-500">{missions} missions</span>
            </div>
            <div className="mt-3 flex flex-wrap gap-1">
                {tags.map((tag) => (
                    <span
                        key={tag}
                        className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-600"
                    >
                        {tag}
                    </span>
                ))}
            </div>
        </div>
    );
}

interface ConversationRowProps {
    name: string;
    lastMessage: string;
    time: string;
    unread?: boolean;
}

function ConversationRow({ name, lastMessage, time, unread }: ConversationRowProps) {
    return (
        <div className="flex items-center gap-3 px-6 py-4 hover:bg-slate-50">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-purple-100 text-sm font-medium text-purple-600">
                {name.charAt(0)}
            </div>
            <div className="flex-1 truncate">
                <div className="flex items-center justify-between">
                    <p className={`text-sm ${unread ? 'font-semibold text-slate-900' : 'text-slate-700'}`}>
                        {name}
                    </p>
                    <span className="text-xs text-slate-400">{time}</span>
                </div>
                <p className="truncate text-sm text-slate-500">{lastMessage}</p>
            </div>
            {unread && <span className="h-2 w-2 rounded-full bg-purple-500" />}
        </div>
    );
}
