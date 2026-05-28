import { Search, Filter, MapPin } from 'lucide-react';

export default function SearchPage() {
    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-5xl mx-auto space-y-8">
                {/* Search Header */}
                <div className="text-center mb-12">
                    <h1 className="text-3xl font-bold text-gray-900 mb-4">Rechercher un talent</h1>
                    <div className="max-w-2xl mx-auto relative">
                        <input
                            type="text"
                            placeholder="Ex: Infirmier de nuit, Kinésithérapeute..."
                            className="w-full h-14 pl-12 pr-4 rounded-2xl border-gray-200 shadow-sm focus:ring-4 focus:ring-brand-100 focus:border-brand-400 text-lg transition-shadow"
                        />
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-6 h-6" />
                    </div>
                </div>

                {/* Filters */}
                <div className="flex flex-wrap gap-2 justify-center mb-8">
                    {['Tous', 'Infirmier', 'Aide-Soignant', 'Educateur', 'Cuisinier', 'ASH'].map((filter) => (
                        <button key={filter} className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm font-medium hover:border-brand-200 hover:text-brand-600 transition-colors">
                            {filter}
                        </button>
                    ))}
                    <button className="px-4 py-2 border border-gray-200 rounded-full text-sm font-medium flex items-center gap-2 hover:bg-gray-50">
                        <Filter className="w-4 h-4" />
                        Plus de filtres
                    </button>
                </div>

                {/* Results Grid (Mock) */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="bg-white p-6 rounded-2xl border border-gray-100 hover:shadow-lg transition-shadow cursor-pointer">
                            <div className="flex items-start justify-between mb-4">
                                <div className="w-12 h-12 bg-gray-100 rounded-full"></div>
                                <span className="text-green-600 text-xs font-bold bg-green-50 px-2 py-1 rounded-full">DISPONIBLE</span>
                            </div>
                            <h3 className="font-bold text-gray-900">Thomas Martin</h3>
                            <p className="text-gray-500 text-sm mb-4">Infirmier DE - 8 ans d'exp.</p>
                            <div className="flex items-center gap-2 text-gray-400 text-xs mb-4">
                                <MapPin className="w-4 h-4" />
                                <span>Paris et petite couronne</span>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                <span className="bg-gray-50 px-2 py-1 rounded text-xs text-gray-500">Ursi</span>
                                <span className="bg-gray-50 px-2 py-1 rounded text-xs text-gray-500">Gériatrie</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
