import { Siren, Clock, MapPin } from 'lucide-react';

export default function ReliefPage() {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto space-y-8">
                {/* Header */}
                <div className="text-center">
                    <div className="mx-auto w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
                        <Siren className="w-8 h-8 text-red-600 animate-pulse" />
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900">SOS Renfort</h1>
                    <p className="mt-2 text-gray-600">Publiez une mission urgente pour trouver un professionnel en moins de 30 min.</p>
                </div>

                {/* Form Placeholder */}
                <div className="bg-white shadow-xl rounded-3xl overflow-hidden border border-gray-100">
                    <div className="p-8 space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">Type d'urgence</label>
                                <select className="w-full rounded-xl border-gray-200 focus:ring-2 focus:ring-red-100 focus:border-red-400 h-12">
                                    <option>Remplacement inopiné</option>
                                    <option>Surcroît d'activité</option>
                                    <option>Crise sanitaire</option>
                                </select>
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">Profession recherchée</label>
                                <select className="w-full rounded-xl border-gray-200 focus:ring-2 focus:ring-red-100 focus:border-red-400 h-12">
                                    <option>Infirmier(e) DE</option>
                                    <option>Aide-Soignant(e)</option>
                                    <option>Masseur-Kinésithérapeute</option>
                                </select>
                            </div>
                        </div>

                        <div className="bg-red-50 p-4 rounded-xl flex items-start gap-3">
                            <Clock className="w-5 h-5 text-red-600 mt-0.5" />
                            <div>
                                <h4 className="font-semibold text-red-900">Délai d'intervention</h4>
                                <p className="text-sm text-red-700">Les professionnels disponibles recevront une notification push immédiate.</p>
                            </div>
                        </div>

                        <button className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-red-200 transform hover:-translate-y-0.5">
                            Lancer l'alerte SOS
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
