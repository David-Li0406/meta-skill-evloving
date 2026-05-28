'use client';

import { Lock, CreditCard } from 'lucide-react';
import { motion } from 'framer-motion';

export function PaymentForm() {
    return (
        <div className="space-y-6">
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center border border-slate-200 shadow-sm">
                        <CreditCard className="w-5 h-5 text-slate-700" />
                    </div>
                    <div>
                        <p className="font-medium text-slate-900">Carte Bancaire</p>
                        <p className="text-xs text-slate-500">Visa, Mastercard, Amex</p>
                    </div>
                </div>
                <div className="w-4 h-4 rounded-full border-[5px] border-brand-600 bg-white" />
            </div>

            <div className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                        Numéro de carte
                    </label>
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="0000 0000 0000 0000"
                            className="input-premium w-full pl-10"
                        />
                        <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            Expiration
                        </label>
                        <input
                            type="text"
                            placeholder="MM/AA"
                            className="input-premium w-full"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-1">
                            CVC
                        </label>
                        <input
                            type="text"
                            placeholder="123"
                            className="input-premium w-full"
                        />
                    </div>
                </div>
            </div>

            <div className="pt-4">
                <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className="w-full bg-brand-600 text-white font-bold py-4 rounded-xl shadow-lg shadow-brand-600/20 hover:bg-brand-700 transition-all flex items-center justify-center gap-2"
                >
                    <Lock className="w-4 h-4" />
                    Payer 237,60 €
                </motion.button>
                <div className="mt-4 flex items-center justify-center gap-2 text-xs text-slate-400">
                    <Lock className="w-3 h-3" />
                    Paiement sécurisé via Stripe
                </div>
            </div>
        </div>
    );
}
