import React from 'react';
import { Icon } from '@components/icons';
import { cn } from './index';

interface SpinnerProps extends React.SVGProps<SVGSVGElement> {
  size?: number;
}

export function Spinner({ size = 24, className, ...props }: SpinnerProps) {
  return <Icon.Loader2 className={cn('animate-spin', className)} size={size} {...props} />;
}

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  className?: string;
}

const sizeMap = {
  sm: 16,
  md: 24,
  lg: 32,
};

export function LoadingSpinner({ size = 'md', text, className }: LoadingSpinnerProps) {
  const spinnerSize = sizeMap[size];

  return (
    <div className={cn('flex flex-col items-center justify-center gap-3', className)}>
      <Spinner size={spinnerSize} />
      {text && <p className="text-sm text-muted-foreground">{text}</p>}
    </div>
  );
}

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'text' | 'circular' | 'rectangular';
}

export function Skeleton({ className, variant = 'rectangular', ...props }: SkeletonProps) {
  const variantStyles = {
    text: 'h-4 w-3/4 rounded max-w-sm',
    circular: 'h-12 w-12 rounded-full',
    rectangular: 'h-20 w-full rounded-md',
  };

  return (
    <div className={cn('animate-pulse bg-muted', variantStyles[variant], className)} {...props} />
  );
}

interface ProgressBarProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

const progressBarSizeMap = {
  sm: 'h-1',
  md: 'h-2',
  lg: 'h-3',
};

export function ProgressBar({
  value,
  max = 100,
  size = 'md',
  showLabel = false,
  className,
  ...props
}: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div className={cn('w-full space-y-1', className)} {...props}>
      {showLabel && (
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>Progress</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div
        className={cn('w-full bg-muted rounded-full overflow-hidden', progressBarSizeMap[size])}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
      >
        <div
          className="h-full bg-primary transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
