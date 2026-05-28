'use client';

import { Calendar, MapPin, Clock } from 'lucide-react';

export function ReceiptCard() {
    return (
        <div className="card-surface p-6 sticky top-24">
            <h2 className="text-lg font-bold text-slate-900 mb-4">Récapitulatif</h2>

            {/* Mission Details */}
            <div className="flex gap-4 mb-6 pb-6 border-b border-slate-100">
                <div className="w-16 h-16 rounded-xl bg-slate-100 flex-shrink-0" />
                <div>
                    <h3 className="font-semibold text-slate-900">Garde de nuit</h3>
                    <p className="text-sm text-slate-500 mb-2">avec Marie Dupont</p>
                    <div className="space-y-1">
                        <div className="flex items-center gap-2 text-xs text-slate-600">
                            <Calendar className="w-3.5 h-3.5" />
                            12 Déc - 13 Déc
                        </div>
                        <div className="flex items-center gap-2 text-xs text-slate-600">
                            <Clock className="w-3.5 h-3.5" />
                            20:00 - 08:00 (12h)
                        </div>
                        <div className="flex items-center gap-2 text-xs text-slate-600">
                            <MapPin className="w-3.5 h-3.5" />
                            Lyon 3ème
                        </div>
                    </div>
                </div>
            </div>

            {/* Pricing Breakdown */}
            <div className="space-y-3 text-sm">
                <div className="flex justify-between text-slate-600">
                    <span>Prestation (12h x 18€)</span>
                    <span>216,00 €</span>
                </div>
                <div className="flex justify-between text-slate-600">
                    <span>Frais de service (10%)</span>
                    <span>21,60 €</span>
                </div>
                <div className="pt-3 border-t border-slate-100 mt-3">
                    <div className="flex justify-between font-bold text-slate-900 text-lg">
                        <span>Total</span>
                        <span>237,60 €</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
