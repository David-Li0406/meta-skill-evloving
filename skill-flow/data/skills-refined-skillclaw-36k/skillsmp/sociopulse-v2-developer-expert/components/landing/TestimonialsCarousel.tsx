'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Star, Quote } from 'lucide-react';
import { isMedical } from '@/lib/brand';

// ===========================================
// TESTIMONIALS CAROUSEL
// Auto-sliding testimonials with photos
// ===========================================

const TESTIMONIALS = [
    {
        name: 'Sophie M.',
        role: 'Directrice EHPAD',
        location: 'Lyon',
        avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
        quote: 'En 2h, nous avions trouvé une IDE pour le week-end. La réactivité est incroyable !',
        rating: 5,
    },
    {
        name: 'Thomas D.',
        role: 'Éducateur Spécialisé',
        location: 'Paris',
        avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
        quote: 'J\'ai décroché 3 missions en une semaine. La plateforme est intuitive et les établissements sérieux.',
        rating: 5,
    },
    {
        name: 'Marie L.',
        role: 'Responsable RH - IME',
        location: 'Bordeaux',
        avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop',
        quote: 'Fini les galères de recrutement. On publie, on reçoit des candidatures qualifiées, c\'est simple.',
        rating: 5,
    },
    {
        name: 'Pierre B.',
        role: 'Aide-Soignant',
        location: 'Marseille',
        avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop',
        quote: 'Les missions correspondent vraiment à mes compétences. Et les paiements sont rapides.',
        rating: 5,
    },
];

export function TestimonialsCarousel() {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, amount: 0.3 });
    const carouselRef = useRef<HTMLDivElement>(null);

    return (
        <section ref={ref} className="py-20 px-4 sm:px-6 overflow-hidden bg-gradient-to-b from-white to-slate-50">
            <div className="max-w-6xl mx-auto">
                {/* Section Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={isInView ? { opacity: 1, y: 0 } : {}}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-12"
                >
                    <span className={`inline-block px-4 py-1.5 rounded-full text-sm font-semibold mb-4 ${isMedical()
                            ? 'bg-rose-100 text-rose-700'
                            : 'bg-teal-100 text-teal-700'
                        }`}>
                        Témoignages
                    </span>
                    <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-slate-900">
                        Ils nous font{' '}
                        <span className={`bg-clip-text text-transparent bg-gradient-to-r ${isMedical() ? 'from-rose-600 to-violet-600' : 'from-teal-600 to-indigo-600'
                            }`}>
                            confiance
                        </span>
                    </h2>
                </motion.div>

                {/* Testimonials Grid/Carousel */}
                <div
                    ref={carouselRef}
                    className="flex gap-6 overflow-x-auto carousel-container pb-4 px-2 -mx-2"
                    style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                >
                    {TESTIMONIALS.map((testimonial, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 30 }}
                            animate={isInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 0.6, delay: index * 0.1 }}
                            className="carousel-item w-80 sm:w-96 flex-shrink-0"
                        >
                            <div className="h-full p-6 rounded-3xl bg-white border border-slate-200 shadow-lg hover:shadow-xl transition-shadow duration-300 card-shine">
                                {/* Quote Icon */}
                                <div className={`inline-flex p-2 rounded-xl mb-4 ${isMedical() ? 'bg-rose-100 text-rose-500' : 'bg-teal-100 text-teal-500'
                                    }`}>
                                    <Quote className="h-5 w-5" />
                                </div>

                                {/* Quote */}
                                <p className="text-slate-700 leading-relaxed mb-6 text-lg">
                                    "{testimonial.quote}"
                                </p>

                                {/* Rating */}
                                <div className="flex gap-1 mb-4">
                                    {[...Array(testimonial.rating)].map((_, i) => (
                                        <Star key={i} className="h-5 w-5 fill-amber-400 text-amber-400" />
                                    ))}
                                </div>

                                {/* Author */}
                                <div className="flex items-center gap-3">
                                    <img
                                        src={testimonial.avatar}
                                        alt={testimonial.name}
                                        className="h-12 w-12 rounded-full object-cover border-2 border-white shadow"
                                    />
                                    <div>
                                        <p className="font-bold text-slate-900">{testimonial.name}</p>
                                        <p className="text-sm text-slate-500">{testimonial.role} • {testimonial.location}</p>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
