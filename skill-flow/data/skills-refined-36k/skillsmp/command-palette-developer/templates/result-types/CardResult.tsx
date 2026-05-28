import * as React from 'react';
import { cn } from '@/lib/utils';
import { Star } from 'lucide-react';

export interface CardResultProps {
  card: {
    image: string;
    title: string;
    description: string;
    tags: string[];
    starred?: boolean;
    author?: {
      name: string;
      avatar?: string;
    };
  };
  selected: boolean;
  onClick: () => void;
}

// Truncate description to specific line count
const truncateDescription = (text: string, maxLines: number = 2): string => {
  const lines = text.split('\n');
  if (lines.length <= maxLines) return text;
  return lines.slice(0, maxLines).join('\n') + '...';
};

export function CardResult({ card, selected, onClick }: CardResultProps) {
  const { image, title, description, tags, starred, author } = card;
  const [imageLoaded, setImageLoaded] = React.useState(false);
  const [imageError, setImageError] = React.useState(false);

  return (
    <button
      type="button"
      role="option"
      aria-selected={selected}
      onClick={onClick}
      className={cn(
        'w-full flex flex-col text-left overflow-hidden rounded-lg',
        'transition-all duration-150 ease-out',
        'focus:outline-none border',
        selected
          ? 'bg-primary/5 border-primary shadow-md'
          : 'hover:bg-muted/30 border-border shadow-sm hover:shadow'
      )}
    >
      {/* Image with lazy loading */}
      <div className="relative w-full h-40 bg-muted overflow-hidden">
        {!imageError ? (
          <>
            {!imageLoaded && (
              <div className="absolute inset-0 animate-pulse bg-muted" />
            )}
            <img
              src={image}
              alt={title}
              loading="lazy"
              onLoad={() => setImageLoaded(true)}
              onError={() => setImageError(true)}
              className={cn(
                'w-full h-full object-cover transition-opacity duration-300',
                imageLoaded ? 'opacity-100' : 'opacity-0'
              )}
            />
          </>
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-muted text-muted-foreground text-sm">
            No preview
          </div>
        )}

        {/* Star/favorite icon */}
        {starred && (
          <div className="absolute top-2 right-2 p-1.5 rounded-full bg-background/80 backdrop-blur-sm">
            <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-col gap-2 p-3">
        {/* Title */}
        <div className="font-semibold text-sm line-clamp-1" title={title}>
          {title}
        </div>

        {/* Description (2-3 lines, truncated) */}
        <div className="text-xs text-muted-foreground line-clamp-2">
          {truncateDescription(description, 2)}
        </div>

        {/* Tags */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-1">
            {tags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className={cn(
                  'inline-flex items-center px-2 py-0.5 rounded-full',
                  'text-xs font-medium',
                  'bg-primary/10 text-primary'
                )}
              >
                {tag}
              </span>
            ))}
            {tags.length > 3 && (
              <span className="inline-flex items-center px-2 py-0.5 text-xs text-muted-foreground">
                +{tags.length - 3}
              </span>
            )}
          </div>
        )}

        {/* Author metadata */}
        {author && (
          <div className="flex items-center gap-2 mt-1 pt-2 border-t border-border/50">
            {author.avatar ? (
              <img
                src={author.avatar}
                alt={author.name}
                className="w-5 h-5 rounded-full object-cover"
              />
            ) : (
              <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center text-xs">
                {author.name[0]?.toUpperCase()}
              </div>
            )}
            <span className="text-xs text-muted-foreground truncate">
              {author.name}
            </span>
          </div>
        )}
      </div>
    </button>
  );
}

// Skeleton loading state
export function CardResultSkeleton() {
  return (
    <div className="w-full flex flex-col rounded-lg border border-border shadow-sm overflow-hidden animate-pulse">
      <div className="w-full h-40 bg-muted" />
      <div className="p-3 space-y-2">
        <div className="h-4 w-3/4 bg-muted rounded" />
        <div className="space-y-1">
          <div className="h-3 w-full bg-muted rounded" />
          <div className="h-3 w-2/3 bg-muted rounded" />
        </div>
        <div className="flex gap-1.5 mt-2">
          <div className="h-5 w-16 bg-muted rounded-full" />
          <div className="h-5 w-20 bg-muted rounded-full" />
        </div>
      </div>
    </div>
  );
}
