import React from 'react';
import { cn } from './index';

export interface SeparatorProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'horizontal' | 'vertical';
  decorative?: boolean;
}

const Separator = React.forwardRef<HTMLDivElement, SeparatorProps>(
  ({ className, orientation = 'horizontal', decorative = true, ...props }, ref) => {
    const ariaOrientation = orientation === 'vertical' ? 'vertical' : undefined;
    return (
      <div
        ref={ref}
        role={decorative ? 'none' : 'separator'}
        aria-orientation={ariaOrientation}
        className={cn(
          'shrink-0 bg-border',
          {
            'h-[1px] w-full': orientation === 'horizontal',
            'h-full w-[1px]': orientation === 'vertical',
          },
          className
        )}
        {...props}
      />
    );
  }
);
Separator.displayName = 'Separator';

export { Separator };
