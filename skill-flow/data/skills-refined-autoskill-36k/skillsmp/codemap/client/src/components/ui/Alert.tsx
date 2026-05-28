import React from 'react';
import { cn } from './index';
import { Icon } from '@components/icons';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive' | 'success' | 'warning';
  title?: string;
}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant = 'default', title, children, ...props }, ref) => {
    const getIcon = () => {
      switch (variant) {
        case 'destructive':
          return Icon.AlertCircle;
        case 'success':
          return Icon.CheckCircle;
        case 'warning':
          return Icon.AlertTriangle;
        default:
          return Icon.Info;
      }
    };

    const IconComponent = getIcon();

    const variantStyles = {
      default: 'bg-muted border-muted-foreground/20 text-foreground',
      destructive: 'bg-destructive/10 border-destructive/20 text-destructive',
      success: 'bg-success/10 border-success/20 text-success',
      warning: 'bg-warning/10 border-warning/20 text-warning',
    };

    return (
      <div
        ref={ref}
        role="alert"
        className={cn('relative w-full rounded-lg border p-4', variantStyles[variant], className)}
        {...props}
      >
        <div className="flex items-start gap-3">
          {IconComponent && <IconComponent className="mt-0.5 flex-shrink-0" size={18} />}
          <div className="flex-1 space-y-1">
            {title && (
              <h5 className="font-semibold text-sm leading-none tracking-tight">{title}</h5>
            )}
            <div className="text-sm leading-relaxed">{children}</div>
          </div>
        </div>
      </div>
    );
  }
);
Alert.displayName = 'Alert';

export { Alert };
