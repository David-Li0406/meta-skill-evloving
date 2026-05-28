'use client';

import Link from 'next/link';

// ===========================================
// SAAS MINIMALIST FOOTER
// Compact, SEO-Optimized, Light Theme
// ===========================================

const productLinks = [
    { label: 'SOS Renfort', href: '/feed?type=manual' },
    { label: 'Fil Pro', href: '/feed' },
    { label: 'Agenda', href: '/agenda' },
    { label: 'Tarifs', href: '/pricing' },
];

const resourceLinks = [
    { label: 'Blog', href: '/blog' },
    { label: 'Guides Métiers', href: '/guides' },
    { label: 'Simulateur de Coût', href: '/simulator' },
    { label: 'Annuaire des structures', href: '/directory' },
];

const legalLinks = [
    { label: "Centre d'aide", href: '/help' },
    { label: 'CGU / CGV', href: '/cgu' },
    { label: 'Confidentialité', href: '/confidentialite' },
    { label: 'Mentions Légales', href: '/mentions-legales' },
];

export function SeoFooter() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-slate-50 border-t border-slate-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-10">
                {/* Centered 3-Column Grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-6 lg:gap-12 max-w-3xl mx-auto">
                    {/* Col 1: Product */}
                    <div className="text-center">
                        <h4 className="uppercase text-xs font-bold tracking-wider text-slate-500 mb-3">
                            Produit
                        </h4>
                        <ul className="space-y-1.5">
                            {productLinks.map((link) => (
                                <li key={link.href}>
                                    <Link
                                        href={link.href}
                                        className="text-xs text-slate-600 hover:text-brand-600 transition-colors"
                                    >
                                        {link.label}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Col 2: Resources */}
                    <div className="text-center">
                        <h4 className="uppercase text-xs font-bold tracking-wider text-slate-500 mb-3">
                            Ressources
                        </h4>
                        <ul className="space-y-1.5">
                            {resourceLinks.map((link) => (
                                <li key={link.href}>
                                    <Link
                                        href={link.href}
                                        className="text-xs text-slate-600 hover:text-brand-600 transition-colors"
                                    >
                                        {link.label}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* Col 3: Legal */}
                    <div className="col-span-2 md:col-span-1 text-center">
                        <h4 className="uppercase text-xs font-bold tracking-wider text-slate-500 mb-3">
                            Support & Légal
                        </h4>
                        <ul className="space-y-1.5">
                            {legalLinks.map((link) => (
                                <li key={link.href}>
                                    <Link
                                        href={link.href}
                                        className="text-xs text-slate-600 hover:text-brand-600 transition-colors"
                                    >
                                        {link.label}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                {/* Copyright */}
                <div className="mt-8 pt-6 border-t border-slate-200 flex justify-center">
                    <p className="text-[10px] uppercase tracking-widest text-slate-400 font-medium">
                        © {currentYear} Curapulse Group. Tous droits réservés.
                    </p>
                </div>
            </div>
        </footer>
    );
}
