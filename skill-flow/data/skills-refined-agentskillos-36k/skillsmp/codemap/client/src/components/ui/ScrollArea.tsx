import React from 'react';
import { cn } from './index';

export interface ScrollAreaProps extends React.HTMLAttributes<HTMLDivElement> {
  orientation?: 'both' | 'horizontal' | 'vertical';
}

const ScrollArea = React.forwardRef<HTMLDivElement, ScrollAreaProps>(
  ({ className, orientation = 'both', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'relative overflow-auto',
          {
            'scrollbar-thin': orientation === 'both',
            'overflow-x-auto overflow-y-hidden scrollbar-thin': orientation === 'horizontal',
            'overflow-y-auto overflow-x-hidden scrollbar-thin': orientation === 'vertical',
          },
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
ScrollArea.displayName = 'ScrollArea';

export { ScrollArea };
