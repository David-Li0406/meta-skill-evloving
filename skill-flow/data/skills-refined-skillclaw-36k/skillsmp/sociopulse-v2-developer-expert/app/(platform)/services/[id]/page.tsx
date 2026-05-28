import BookingWidget from "@/components/ui/BookingWidget";
import MobileBookingDrawer from "@/components/MobileBookingDrawer";

export default function ServicePage({ params }: { params: { id: string } }) {
    // Mock Data (In real app, fetch based on params.id)
    const service = {
        title: "Atelier Créatif : Céramique & Poterie",
        category: "Art & Artisanat",
        description:
            "Découvrez l'art de la céramique lors de cet atelier immersif. Apprenez les techniques de base du modelage, du tournage et de l'émaillage dans une ambiance détendue et créative. Nos artisans experts vous guideront pas à pas pour créer vos propres pièces uniques.",
        highlights: [
            "Matériel professionnel inclus",
            "Cuisson de vos pièces comprise",
            "Gouter gourmand offert",
            "Accessible aux débutants",
        ],
        images: [
            "https://images.unsplash.com/photo-1565193566173-0923d195c16b?auto=format&fit=crop&q=80&w=1000",
            "https://images.unsplash.com/photo-1493106641515-6b5631de4bb9?auto=format&fit=crop&q=80&w=1000",
            "https://images.unsplash.com/photo-1526404209869-655639695655?auto=format&fit=crop&q=80&w=1000",
        ],
    };

    return (
        <main className="min-h-screen bg-gray-50/50 pb-24 lg:pb-0">
            {/* === HERO SECTION (Mobile Only) === */}
            <div className="lg:hidden w-full h-64 relative">
                <img
                    src={service.images[0]}
                    alt={service.title}
                    className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute bottom-4 left-4 text-white">
                    <span className="px-2 py-1 bg-brand-600 text-xs font-bold uppercase tracking-wider rounded-md mb-2 inline-block">
                        {service.category}
                    </span>
                    <h1 className="text-2xl font-bold leading-tight">{service.title}</h1>
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
                <div className="flex flex-col lg:flex-row gap-12">

                    {/* ==============================================
              LEFT COLUMN (66%) - Content
          ============================================== */}
                    <div className="w-full lg:w-2/3 space-y-10">

                        {/* Desktop Header */}
                        <div className="hidden lg:block space-y-4">
                            <span className="px-3 py-1 bg-brand-50 text-brand-600 text-xs font-bold uppercase tracking-wider rounded-full">
                                {service.category}
                            </span>
                            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight leading-tight">
                                {service.title}
                            </h1>
                            <div className="flex items-center gap-4 text-sm text-gray-500">
                                <span className="flex items-center gap-1">
                                    <svg className="w-4 h-4 text-brand-600" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                                    4.9 (128 avis)
                                </span>
                                <span>•</span>
                                <span>Paris 11ème</span>
                                <span>•</span>
                                <span>2h - 3h30</span>
                            </div>
                        </div>

                        {/* Gallery Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 rounded-3xl overflow-hidden">
                            <div className="md:col-span-2 h-64 md:h-96 relative group">
                                <img
                                    src={service.images[0]}
                                    alt="Main view"
                                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                                />
                            </div>
                            {service.images.slice(1).map((img, idx) => (
                                <div key={idx} className="h-48 relative group overflow-hidden">
                                    <img
                                        src={img}
                                        alt={`Detail ${idx}`}
                                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                                    />
                                </div>
                            ))}
                        </div>

                        {/* Description */}
                        <div className="prose prose-lg prose-gray max-w-none">
                            <h3 className="text-xl font-bold text-gray-900 mb-4">À propos de l'atelier</h3>
                            <p className="text-gray-600 leading-relaxed">
                                {service.description}
                            </p>

                            <h4 className="text-lg font-bold text-gray-900 mt-8 mb-4">Ce qui est inclus</h4>
                            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3 list-none pl-0">
                                {service.highlights.map((item, i) => (
                                    <li key={i} className="flex items-center gap-3 text-gray-600 bg-white p-3 rounded-xl border border-gray-100">
                                        <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                                        </svg>
                                        <span className="text-sm font-medium">{item}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* Reviews Preview (Placeholder) */}
                        <div className="bg-white p-8 rounded-3xl border border-gray-100">
                            <h3 className="text-xl font-bold text-gray-900 mb-6">Avis participants</h3>
                            <div className="space-y-6">
                                {[1, 2].map((_, i) => (
                                    <div key={i} className="flex gap-4 items-start">
                                        <div className="w-10 h-10 rounded-full bg-gray-200 flex-shrink-0" />
                                        <div>
                                            <div className="flex items-center gap-2 mb-1">
                                                <span className="font-bold text-gray-900">Sophie M.</span>
                                                <div className="flex text-brand-600 text-xs">★★★★★</div>
                                            </div>
                                            <p className="text-gray-600 text-sm">
                                                "Superbe expérience ! L'animateur était très pédagogue et l'ambiance géniale. Je recommande vivement pour un team building."
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                    </div>

                    {/* ==============================================
              RIGHT COLUMN (33%) - Sticky Widget
          ============================================== */}
                    <div className="hidden lg:block w-full lg:w-1/3 relative">
                        <BookingWidget />
                    </div>

                </div>
            </div>

            {/* Mobile Drawer */}
            <MobileBookingDrawer />
        </main>
    );
}
