'use client';

import { motion } from 'framer-motion';
import {
    Star,
    BadgeCheck,
    ThumbsUp,
    MessageCircle,
    MoreHorizontal,
    Quote
} from 'lucide-react';
import { EmptyState } from './EmptyState';

export interface ReviewItem {
    id: string;
    /** Reviewer name */
    reviewerName: string;
    /** Reviewer avatar URL */
    reviewerAvatar?: string | null;
    /** Reviewer role/title */
    reviewerRole?: string;
    /** Rating 1-5 */
    rating: number;
    /** Review comment */
    comment: string;
    /** Review date */
    date: Date | string;
    /** Whether this review is from a verified mission */
    isVerifiedMission?: boolean;
    /** Mission title (if verified) */
    missionTitle?: string;
    /** Provider response to the review */
    response?: string;
    /** Response date */
    responseDate?: Date | string;
    /** Number of helpful votes */
    helpfulCount?: number;
}

export interface ReviewsListProps {
    /** List of reviews */
    reviews: ReviewItem[];
    /** Average rating */
    averageRating?: number;
    /** Total reviews count */
    totalReviews?: number;
    /** Show summary header */
    showSummary?: boolean;
    /** User's first name for personalization */
    userName?: string;
    /** Whether viewing own profile */
    isOwnProfile?: boolean;
    /** Empty state message */
    emptyMessage?: string;
    /** Callback for empty state action */
    onEmptyAction?: () => void;
}

const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1,
        },
    },
};

const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            type: 'spring' as const,
            stiffness: 100,
            damping: 15,
        },
    },
};

function StarRating({ rating, size = 'sm' }: { rating: number; size?: 'sm' | 'md' | 'lg' }) {
    const sizeClasses = {
        sm: 'w-3.5 h-3.5',
        md: 'w-4 h-4',
        lg: 'w-5 h-5',
    };

    return (
        <div className="flex items-center gap-0.5">
            {[1, 2, 3, 4, 5].map((star) => (
                <Star
                    key={star}
                    className={`
                        ${sizeClasses[size]}
                        ${star <= rating
                            ? 'text-amber-400 fill-amber-400'
                            : 'text-slate-200 fill-slate-200'
                        }
                    `}
                />
            ))}
        </div>
    );
}

function formatReviewDate(date: Date | string): string {
    const d = new Date(date);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Aujourd'hui";
    if (diffDays === 1) return 'Hier';
    if (diffDays < 7) return `Il y a ${diffDays} jours`;
    if (diffDays < 30) return `Il y a ${Math.floor(diffDays / 7)} semaines`;

    return d.toLocaleDateString('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: d.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
    });
}

function ReviewCard({ review }: { review: ReviewItem }) {
    const initials = review.reviewerName
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);

    return (
        <motion.article
            variants={itemVariants}
            className="card-surface p-6 hover:shadow-soft-lg transition-shadow"
        >
            {/* Header: Reviewer + Date + Rating */}
            <div className="flex items-start justify-between gap-3 mb-4">
                <div className="flex items-center gap-3">
                    {/* Avatar */}
                    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-brand-100 to-indigo-100 flex items-center justify-center overflow-hidden">
                        {review.reviewerAvatar ? (
                            <img
                                src={review.reviewerAvatar}
                                alt={review.reviewerName}
                                className="w-full h-full object-cover"
                            />
                        ) : (
                            <span className="text-sm font-semibold text-brand-600">
                                {initials}
                            </span>
                        )}
                    </div>

                    {/* Name & Role */}
                    <div>
                        <div className="flex items-center gap-1.5">
                            <h4 className="text-sm font-semibold text-slate-900">
                                {review.reviewerName}
                            </h4>
                            {review.isVerifiedMission && (
                                <span className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded-lg bg-brand-50 text-brand-600">
                                    <BadgeCheck className="w-3 h-3" />
                                    <span className="text-[10px] font-medium">Vérifié</span>
                                </span>
                            )}
                        </div>
                        <p className="text-xs text-slate-500">
                            {review.reviewerRole || 'Membre'}
                            {' • '}
                            {formatReviewDate(review.date)}
                        </p>
                    </div>
                </div>

                {/* Rating */}
                <div className="flex flex-col items-end gap-1">
                    <StarRating rating={review.rating} size="sm" />
                    <span className="text-xs font-medium text-slate-500">
                        {review.rating}/5
                    </span>
                </div>
            </div>

            {/* Verified Mission Badge */}
            {review.isVerifiedMission && review.missionTitle && (
                <div className="flex items-center gap-2 px-3 py-2 mb-3 rounded-lg bg-green-50 border border-green-100">
                    <BadgeCheck className="w-4 h-4 text-green-600 flex-shrink-0" />
                    <span className="text-xs text-green-700">
                        <span className="font-medium">Mission vérifiée :</span> {review.missionTitle}
                    </span>
                </div>
            )}

            {/* Comment */}
            <div className="relative">
                <Quote className="absolute -top-1 -left-1 w-6 h-6 text-slate-100" />
                <p className="text-sm text-slate-600 leading-relaxed italic pl-4">
                    "{review.comment}"
                </p>
            </div>

            {/* Provider Response */}
            {review.response && (
                <div className="mt-4 pl-4 border-l-2 border-brand-200 bg-brand-50/50 rounded-r-lg p-3">
                    <div className="flex items-center gap-2 mb-1">
                        <MessageCircle className="w-3.5 h-3.5 text-brand-500" />
                        <span className="text-xs font-semibold text-brand-700">
                            Réponse du professionnel
                        </span>
                        {review.responseDate && (
                            <span className="text-xs text-brand-400">
                                • {formatReviewDate(review.responseDate)}
                            </span>
                        )}
                    </div>
                    <p className="text-sm text-brand-900/80 leading-relaxed">
                        {review.response}
                    </p>
                </div>
            )}

            {/* Actions */}
            <div className="flex items-center justify-between mt-4 pt-3 border-t border-slate-100">
                <button className="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-700 transition-colors">
                    <ThumbsUp className="w-3.5 h-3.5" />
                    Utile {review.helpfulCount ? `(${review.helpfulCount})` : ''}
                </button>
                <button
                    className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
                    aria-label="Plus d'options"
                >
                    <MoreHorizontal className="w-4 h-4" />
                </button>
            </div>
        </motion.article>
    );
}

export function ReviewsList({
    reviews,
    averageRating,
    totalReviews,
    showSummary = true,
    userName,
    isOwnProfile = false,
    emptyMessage,
    onEmptyAction
}: ReviewsListProps) {
    if (reviews.length === 0) {
        return (
            <EmptyState
                type="reviews"
                userName={userName}
                isOwnProfile={isOwnProfile}
                customMessage={emptyMessage}
                onAction={onEmptyAction}
                actionLabel={isOwnProfile
                    ? 'Compléter mon profil'
                    : 'Laisser un avis'
                }
            />
        );
    }

    // Calculate rating distribution
    const ratingDistribution = [5, 4, 3, 2, 1].map(rating => ({
        rating,
        count: reviews.filter(r => Math.round(r.rating) === rating).length,
        percentage: (reviews.filter(r => Math.round(r.rating) === rating).length / reviews.length) * 100,
    }));

    return (
        <div className="py-4">
            {/* Rating Summary */}
            {showSummary && (
                <div className="flex flex-col sm:flex-row gap-6 px-4 sm:px-6 pb-6 mb-6 border-b border-slate-100">
                    {/* Average Rating */}
                    <div className="flex items-center gap-4">
                        <div className="text-center">
                            <div className="text-4xl font-bold text-slate-900">
                                {(averageRating ?? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)}
                            </div>
                            <StarRating
                                rating={Math.round(averageRating ?? reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length)}
                                size="md"
                            />
                            <p className="text-xs text-slate-500 mt-1">
                                {totalReviews ?? reviews.length} avis
                            </p>
                        </div>
                    </div>

                    {/* Rating Distribution */}
                    <div className="flex-1 space-y-1.5">
                        {ratingDistribution.map(({ rating, count, percentage }) => (
                            <div key={rating} className="flex items-center gap-2 text-xs">
                                <span className="w-3 text-slate-500 font-medium">{rating}</span>
                                <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                                <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                                    <motion.div
                                        initial={{ width: 0 }}
                                        animate={{ width: `${percentage}%` }}
                                        transition={{ duration: 0.5, delay: 0.1 * (5 - rating) }}
                                        className="h-full bg-amber-400 rounded-full"
                                    />
                                </div>
                                <span className="w-8 text-slate-400 text-right">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Reviews List */}
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="space-y-4 px-4 sm:px-6"
            >
                {reviews.map((review) => (
                    <ReviewCard key={review.id} review={review} />
                ))}
            </motion.div>

            {/* Load More */}
            {reviews.length >= 5 && (
                <div className="mt-6 text-center">
                    <button className="btn-secondary">
                        Voir plus d'avis
                    </button>
                </div>
            )}
        </div>
    );
}
