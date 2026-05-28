import React from 'react';
import { cn } from './index';
import { Icon } from '@components/icons';

export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string;
  alt?: string;
  fallback?: string;
  size?: 'sm' | 'md' | 'lg';
}

const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, src, alt, fallback, size = 'md', ...props }, ref) => {
    const sizeClasses = {
      sm: 'h-8 w-8 text-xs',
      md: 'h-10 w-10 text-sm',
      lg: 'h-12 w-12 text-base',
    };

    const getInitials = (name: string) => {
      return name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
    };

    if (!src) {
      return (
        <div
          ref={ref}
          className={cn(
            'relative flex shrink-0 overflow-hidden rounded-full bg-muted items-center justify-center font-medium',
            sizeClasses[size],
            className
          )}
          {...props}
        >
          {fallback && <span>{getInitials(fallback)}</span>}
          {!fallback && <Icon.User size={size === 'sm' ? 16 : size === 'lg' ? 24 : 20} />}
        </div>
      );
    }

    return (
      <div
        ref={ref}
        className={cn(
          'relative shrink-0 overflow-hidden rounded-full',
          sizeClasses[size],
          className
        )}
        {...props}
      >
        <img src={src} alt={alt || fallback} className="aspect-square h-full w-full object-cover" />
      </div>
    );
  }
);
Avatar.displayName = 'Avatar';

export { Avatar };
