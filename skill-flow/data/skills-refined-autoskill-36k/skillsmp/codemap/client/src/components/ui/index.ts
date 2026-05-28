import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export * from './Button';
export * from './Input';
export * from './Dialog';
export * from './Tabs';
export * from './Select';
export * from './Badge';
export * from './Avatar';
export * from './Separator';
export * from './ScrollArea';
export * from './Card';
export * from './Alert';
export * from './Tooltip';
export * from './Toast';
export * from './Loading';
export * from './EmptyState';
export * from './Label';
export * from './Checkbox';
export * from './Switch';
export * from './Table';
// export * from './motion'; // 暂时禁用，等 JSX 编译问题解决
