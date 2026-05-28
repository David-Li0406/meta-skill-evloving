import React from 'react';
import { Icon } from '@components/icons';
import { Button } from './Button';
import { cn } from './index';

export interface EmptyStateProps extends React.HTMLAttributes<HTMLDivElement> {
  icon?: keyof typeof Icon;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  variant?: 'default' | 'compact' | 'minimal';
}

const EmptyState = React.forwardRef<HTMLDivElement, EmptyStateProps>(
  (
    {
      className,
      icon = 'FolderOpen',
      title,
      description,
      actionLabel,
      onAction,
      variant = 'default',
      ...props
    },
    ref
  ) => {
    const IconComponent = Icon[icon];

    const variantStyles = {
      default: 'py-12',
      compact: 'py-8',
      minimal: 'py-4',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'flex flex-col items-center justify-center text-center',
          variantStyles[variant],
          className
        )}
        {...props}
      >
        {IconComponent && (
          <div className="mb-4 flex items-center justify-center">
            {variant === 'minimal' ? (
              <IconComponent size={32} className="text-muted-foreground" />
            ) : (
              <div className="rounded-full bg-muted p-4">
                <IconComponent size={48} className="text-muted-foreground" />
              </div>
            )}
          </div>
        )}

        <div className="max-w-sm space-y-2">
          <h3 className={cn('font-semibold', variant === 'minimal' ? 'text-sm' : 'text-lg')}>
            {title}
          </h3>

          {description && (
            <p className={cn('text-sm text-muted-foreground', variant === 'minimal' && 'text-xs')}>
              {description}
            </p>
          )}
        </div>

        {actionLabel && onAction && (
          <div className="mt-6">
            <Button onClick={onAction}>
              <Icon.Plus size={16} className="mr-2" />
              {actionLabel}
            </Button>
          </div>
        )}
      </div>
    );
  }
);
EmptyState.displayName = 'EmptyState';

export { EmptyState };
