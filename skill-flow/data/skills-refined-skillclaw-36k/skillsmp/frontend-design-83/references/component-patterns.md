# Component Patterns

> 재사용 가능한 프로덕션 수준 컴포넌트 패턴

## 기본 원칙

1. **shadcn/ui 기반 확장**: 기본 컴포넌트를 래핑하여 프로젝트 스타일 적용
2. **변형(Variant) 시스템**: cva/CVA를 사용한 체계적인 변형 관리
3. **접근성 내장**: ARIA 속성, 키보드 네비게이션 기본 포함
4. **타입 안전성**: TypeScript로 prop 타입 명확히 정의

## Button Patterns

### 기본 확장 버튼

```tsx
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  // 기본 스타일
  "inline-flex items-center justify-center font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary:
          "bg-brand text-white hover:bg-brand/90 active:scale-[0.98]",
        secondary:
          "bg-surface border border-border hover:bg-surface-hover",
        ghost:
          "hover:bg-surface-hover",
        destructive:
          "bg-destructive text-white hover:bg-destructive/90",
      },
      size: {
        sm: "h-9 px-4 text-sm rounded-lg",
        md: "h-11 px-6 text-base rounded-xl",
        lg: "h-14 px-8 text-lg rounded-2xl",
        icon: "h-10 w-10 rounded-full",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export function Button({
  className,
  variant,
  size,
  isLoading,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading ? (
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      ) : null}
      {children}
    </button>
  );
}
```

### 인터랙티브 버튼 (모션 포함)

```tsx
import { motion } from "framer-motion";

export function InteractiveButton({ children, ...props }: ButtonProps) {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      className={cn(buttonVariants(props))}
      {...props}
    >
      {children}
    </motion.button>
  );
}
```

## Card Patterns

### 기본 카드

```tsx
const cardVariants = cva(
  "rounded-2xl border bg-card transition-all duration-300",
  {
    variants: {
      variant: {
        default: "border-border",
        elevated: "border-transparent shadow-lg",
        outline: "border-2 border-brand/20",
      },
      interactive: {
        true: "cursor-pointer hover:shadow-xl hover:-translate-y-1 hover:border-brand/30",
        false: "",
      },
    },
    defaultVariants: {
      variant: "default",
      interactive: false,
    },
  }
);

interface CardProps extends VariantProps<typeof cardVariants> {
  children: React.ReactNode;
  className?: string;
}

export function Card({
  variant,
  interactive,
  className,
  children,
}: CardProps) {
  return (
    <div className={cn(cardVariants({ variant, interactive }), className)}>
      {children}
    </div>
  );
}

// 서브 컴포넌트
export function CardHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn("p-6 pb-0", className)}>{children}</div>;
}

export function CardContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn("p-6", className)}>{children}</div>;
}

export function CardFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn("p-6 pt-0 flex items-center gap-4", className)}>{children}</div>;
}
```

### 벤토 그리드 카드

```tsx
export function BentoCard({
  title,
  description,
  icon: Icon,
  className,
  ...props
}: BentoCardProps) {
  return (
    <Card
      interactive
      className={cn(
        "group relative overflow-hidden",
        className
      )}
      {...props}
    >
      {/* 배경 그래디언트 효과 */}
      <div className="absolute inset-0 bg-gradient-to-br from-brand/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

      <CardContent className="relative z-10">
        <div className="mb-4 inline-flex p-3 rounded-xl bg-brand/10">
          <Icon className="h-6 w-6 text-brand" />
        </div>

        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        <p className="text-muted-foreground">{description}</p>
      </CardContent>

      {/* 호버 시 화살표 */}
      <div className="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
        <ArrowRight className="h-5 w-5 text-brand" />
      </div>
    </Card>
  );
}
```

## Input Patterns

### 플로팅 라벨 인풋

```tsx
import { useState } from "react";

export function FloatingInput({
  label,
  error,
  ...props
}: FloatingInputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [hasValue, setHasValue] = useState(false);

  const isFloating = isFocused || hasValue;

  return (
    <div className="relative">
      <input
        className={cn(
          "peer w-full h-14 px-4 pt-4 pb-2 rounded-xl border bg-background",
          "focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent",
          "transition-all duration-200",
          error && "border-destructive focus:ring-destructive"
        )}
        onFocus={() => setIsFocused(true)}
        onBlur={(e) => {
          setIsFocused(false);
          setHasValue(!!e.target.value);
        }}
        {...props}
      />

      <label
        className={cn(
          "absolute left-4 transition-all duration-200 pointer-events-none",
          "text-muted-foreground",
          isFloating
            ? "top-2 text-xs text-brand"
            : "top-1/2 -translate-y-1/2 text-base"
        )}
      >
        {label}
      </label>

      {error && (
        <p className="mt-1 text-sm text-destructive">{error}</p>
      )}
    </div>
  );
}
```

### 언더라인 인풋

```tsx
export function UnderlineInput({ label, ...props }: UnderlineInputProps) {
  return (
    <div className="relative">
      <input
        className={cn(
          "w-full py-3 bg-transparent border-b-2 border-border",
          "focus:outline-none focus:border-brand",
          "transition-colors duration-300",
          "placeholder-transparent peer"
        )}
        placeholder={label}
        {...props}
      />

      <label
        className={cn(
          "absolute left-0 -top-2.5 text-sm text-brand",
          "transition-all duration-300",
          "peer-placeholder-shown:top-3 peer-placeholder-shown:text-base peer-placeholder-shown:text-muted-foreground",
          "peer-focus:-top-2.5 peer-focus:text-sm peer-focus:text-brand"
        )}
      >
        {label}
      </label>

      {/* 애니메이션 언더라인 */}
      <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-brand transition-all duration-300 peer-focus:w-full" />
    </div>
  );
}
```

## Navigation Patterns

### 스티키 네비게이션

```tsx
export function StickyNav() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300",
        isScrolled
          ? "bg-background/80 backdrop-blur-lg border-b shadow-sm"
          : "bg-transparent"
      )}
    >
      <nav className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Logo />
        <NavLinks />
        <NavActions />
      </nav>
    </header>
  );
}
```

### 탭 네비게이션

```tsx
export function AnimatedTabs({ tabs, activeTab, onChange }: TabsProps) {
  return (
    <div className="relative flex bg-surface rounded-full p-1">
      {/* 애니메이션 배경 */}
      <motion.div
        className="absolute inset-y-1 bg-white rounded-full shadow-sm"
        layoutId="activeTab"
        style={{
          width: `${100 / tabs.length}%`,
          left: `${(tabs.findIndex((t) => t.id === activeTab) * 100) / tabs.length}%`,
        }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
      />

      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={cn(
            "relative z-10 flex-1 py-2 px-4 text-sm font-medium rounded-full transition-colors",
            activeTab === tab.id
              ? "text-foreground"
              : "text-muted-foreground hover:text-foreground"
          )}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

## Modal Patterns

### 애니메이션 모달

```tsx
import { AnimatePresence, motion } from "framer-motion";

export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* 배경 오버레이 */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
          />

          {/* 모달 컨텐츠 */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", duration: 0.3 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-lg"
          >
            <div className="bg-background rounded-2xl shadow-xl border">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

## Layout Patterns

### 벤토 그리드

```tsx
export function BentoGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {children}
    </div>
  );
}

// 사용 예시
<BentoGrid>
  <BentoCard className="md:col-span-2 md:row-span-2" featured />
  <BentoCard />
  <BentoCard />
  <BentoCard className="md:col-span-2" />
</BentoGrid>
```

### 마퀴 스크롤

```tsx
export function Marquee({
  children,
  speed = 30,
  pauseOnHover = true,
}: MarqueeProps) {
  return (
    <div className="overflow-hidden relative">
      <motion.div
        className={cn(
          "flex gap-4",
          pauseOnHover && "hover:[animation-play-state:paused]"
        )}
        animate={{ x: ["0%", "-50%"] }}
        transition={{
          x: {
            repeat: Infinity,
            repeatType: "loop",
            duration: speed,
            ease: "linear",
          },
        }}
      >
        {children}
        {/* 무한 루프를 위한 복제 */}
        {children}
      </motion.div>
    </div>
  );
}
```

## Utility Patterns

### cn 유틸리티

```tsx
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

### 반응형 훅

```tsx
import { useState, useEffect } from "react";

export function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
}

// 사용
const isMobile = useMediaQuery("(max-width: 768px)");
```

## 체크리스트

컴포넌트 작성 시 확인사항:

```markdown
## 컴포넌트 품질 체크

### 기능
- [ ] TypeScript 타입 정의 완료
- [ ] Props에 적절한 기본값 설정
- [ ] 에러 상태 처리

### 스타일
- [ ] cva/CVA로 변형 시스템 구축
- [ ] 호버/포커스/액티브 상태 정의
- [ ] 반응형 고려

### 접근성
- [ ] 키보드 네비게이션 지원
- [ ] ARIA 속성 적용
- [ ] 포커스 표시 명확

### 성능
- [ ] 불필요한 리렌더링 방지
- [ ] 애니메이션 GPU 가속 활용
- [ ] 큰 컴포넌트 코드 스플리팅
```
