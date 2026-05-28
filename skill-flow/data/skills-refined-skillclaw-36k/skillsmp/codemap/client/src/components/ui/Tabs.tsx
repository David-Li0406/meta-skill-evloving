import React, { useState } from 'react';
import { cn } from './index';

export function Tabs({
  className,
  children,
  defaultValue,
  onValueChange,
  ...props
}: {
  className?: string;
  children: React.ReactNode;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
} & React.HTMLAttributes<HTMLDivElement>) {
  const [activeTab, setActiveTab] = useState(defaultValue || '');

  return (
    <div ref={(ref) => ref} className={cn('', className)} {...props}>
      {React.Children.map(children, (child) => {
        if (React.isValidElement(child)) {
          // Only pass isActive to TabsTrigger components
          if (child.type === TabsTrigger) {
            return React.cloneElement(child as React.ReactElement<any>, {
              isActive: child.props.value === activeTab,
              onClick: () => {
                setActiveTab(child.props.value);
                onValueChange?.(child.props.value);
              },
            });
          }
          // Pass activeTab to TabsContent components
          if (child.type === TabsContent) {
            return React.cloneElement(child as React.ReactElement<any>, {
              activeTab: activeTab,
            });
          }
        }
        return child;
      })}
    </div>
  );
}
Tabs.displayName = 'Tabs';

export function TabsList({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md bg-muted p-1',
        'text-muted-foreground',
        className
      )}
      {...props}
    />
  );
}

export function TabsTrigger({
  value,
  isActive,
  onClick,
  className,
  ...props
}: {
  value: string;
  isActive?: boolean;
  onClick?: () => void;
  className?: string;
} & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5',
        'text-sm font-medium ring-offset-background transition-all',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        isActive && 'bg-background text-foreground',
        !isActive && 'hover:bg-muted hover:text-accent-foreground',
        'transition-colors',
        className
      )}
      {...props}
    />
  );
}
TabsTrigger.displayName = 'TabsTrigger';

export function TabsContent({
  value,
  activeTab,
  className,
  ...props
}: {
  value: string;
  activeTab?: string;
  className?: string;
} & React.HTMLAttributes<HTMLDivElement>) {
  if (activeTab !== value) return null;

  return (
    <div
      className={cn(
        'mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-ring focus-visible:ring-offset-2',
        className
      )}
      {...props}
    />
  );
}
TabsContent.displayName = 'TabsContent';
