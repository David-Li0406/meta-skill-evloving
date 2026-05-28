# Anti-Pattern Catalog

> 피해야 할 일반적인 디자인 패턴과 대안

## 개요

"AI가 만든 것 같은" 느낌을 주는 패턴들입니다. 이 패턴들을 사용하면 차별화되지 않은 결과물이 나옵니다.

## Typography Anti-Patterns

### 제네릭 폰트 사용

| ❌ 피해야 할 폰트 | ✅ 대안 |
|------------------|---------|
| Inter | Plus Jakarta Sans, Satoshi |
| Roboto | Manrope, DM Sans |
| Arial | Pretendard (한글) |
| system-ui | 명시적 폰트 스택 |
| Open Sans | Source Sans 3, Nunito |

```css
/* ❌ BAD */
font-family: 'Inter', 'Roboto', system-ui, sans-serif;

/* ✅ GOOD - 의도적 선택 */
font-family: 'Plus Jakarta Sans', 'Pretendard', sans-serif;
```

### 단조로운 타입 스케일

```css
/* ❌ BAD - 기본 Tailwind 스케일만 사용 */
.heading { @apply text-2xl; }
.subheading { @apply text-xl; }
.body { @apply text-base; }

/* ✅ GOOD - 의도적인 대비 */
.heading {
  @apply text-5xl md:text-7xl font-bold tracking-tight;
}
.subheading {
  @apply text-lg font-medium text-muted-foreground;
}
```

### 안전한 폰트 무게만 사용

```css
/* ❌ BAD - 400, 700만 사용 */
font-weight: 400;
font-weight: 700;

/* ✅ GOOD - 다양한 무게 활용 */
font-weight: 300; /* Light for large display */
font-weight: 500; /* Medium for emphasis */
font-weight: 800; /* Extra bold for impact */
```

## Color Anti-Patterns

### 보라색-핑크 그래디언트

```css
/* ❌ BAD - AI 생성물의 클리셰 */
background: linear-gradient(to right, #8B5CF6, #EC4899);
background: linear-gradient(135deg, #667eea, #764ba2);

/* ✅ GOOD - 의도적 팔레트 */
background: linear-gradient(to right, #1A1A2E, #16213E);
background: #E94560; /* 단색 포인트 */
```

### 과도한 색상 사용

```css
/* ❌ BAD - 5개 이상의 랜덤 색상 */
--primary: #3B82F6;
--secondary: #10B981;
--accent: #F59E0B;
--highlight: #EF4444;
--special: #8B5CF6;

/* ✅ GOOD - 제한된 팔레트 */
--primary: #1A1A2E;
--accent: #E94560;
--surface: #F8F9FA;
/* 나머지는 위 색상의 변형 */
```

### 의미 없는 색상 선택

```css
/* ❌ BAD - 왜 이 색상인지 설명 불가 */
--button-color: #4F46E5; /* "그냥 예뻐서" */

/* ✅ GOOD - 의도가 있는 선택 */
--button-color: #E94560; /* 브랜드 시그니처 레드, CTA 강조 */
```

## Layout Anti-Patterns

### 동일한 카드 그리드

```jsx
/* ❌ BAD - 반복적인 동일 크기 그리드 */
<div className="grid grid-cols-3 gap-4">
  <Card />
  <Card />
  <Card />
  <Card />
  <Card />
  <Card />
</div>

/* ✅ GOOD - 시각적 계층 */
<div className="space-y-8">
  {/* Featured - 큰 카드 */}
  <Card className="md:col-span-2 h-64" featured />

  {/* Secondary - 중간 크기 */}
  <div className="grid grid-cols-2 gap-4">
    <Card className="h-48" />
    <Card className="h-48" />
  </div>

  {/* Compact - 작은 리스트 */}
  <div className="space-y-2">
    <CompactCard />
    <CompactCard />
  </div>
</div>
```

### 완벽한 대칭

```jsx
/* ❌ BAD - 모든 것이 중앙 정렬, 균등 배치 */
<div className="flex justify-center items-center">
  <div className="text-center">
    <h1>Title</h1>
    <p>Description</p>
    <Button>Action</Button>
  </div>
</div>

/* ✅ GOOD - 의도적 비대칭 */
<div className="grid grid-cols-12 gap-4">
  <div className="col-span-7">
    <h1 className="text-left">Title</h1>
    <p>Description</p>
  </div>
  <div className="col-span-5 flex items-end justify-end">
    <Button>Action</Button>
  </div>
</div>
```

### 예측 가능한 섹션 패턴

```jsx
/* ❌ BAD - 모든 페이지가 동일한 구조 */
<Hero />
<Features /> {/* 3열 아이콘 그리드 */}
<Testimonials /> {/* 3열 카드 */}
<CTA />

/* ✅ GOOD - 섹션마다 다른 레이아웃 */
<Hero variant="asymmetric" />
<Features layout="bento" /> {/* 벤토 그리드 */}
<Testimonials layout="marquee" /> {/* 스크롤 마퀴 */}
<CTA variant="sticky-bottom" />
```

## Component Anti-Patterns

### 기본 shadcn/ui 그대로 사용

```jsx
/* ❌ BAD - 커스터마이징 없음 */
<Button>Click me</Button>

/* ✅ GOOD - 프로젝트 스타일 적용 */
<Button
  className="rounded-full px-8 py-6 text-lg
             bg-brand hover:bg-brand/90
             transition-all hover:scale-105"
>
  Click me
</Button>
```

### 모든 곳에 둥근 모서리

```jsx
/* ❌ BAD - rounded-lg 남용 */
<Card className="rounded-lg" />
<Button className="rounded-lg" />
<Input className="rounded-lg" />

/* ✅ GOOD - 의도적 믹스 */
<Card className="rounded-2xl" /> {/* 큰 요소는 더 둥글게 */}
<Button className="rounded-full" /> {/* 버튼은 완전히 둥글게 */}
<Input className="rounded-none border-b" /> {/* 인풋은 언더라인 */}
```

### 호버 효과 없음

```jsx
/* ❌ BAD - 인터랙션 피드백 없음 */
<Card>Content</Card>

/* ✅ GOOD - 명확한 인터랙션 */
<Card className="
  transition-all duration-300
  hover:shadow-xl hover:-translate-y-1
  hover:border-brand/50
  cursor-pointer
">
  Content
</Card>
```

## Motion Anti-Patterns

### 애니메이션 없음

```jsx
/* ❌ BAD - 정적인 상태 변화 */
{isOpen && <Modal />}

/* ✅ GOOD - 부드러운 전환 */
<AnimatePresence>
  {isOpen && (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
    >
      <Modal />
    </motion.div>
  )}
</AnimatePresence>
```

### 과도한 애니메이션

```jsx
/* ❌ BAD - 모든 것이 움직임 */
<motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity }}>
  <motion.div animate={{ scale: [1, 1.1, 1] }}>
    <motion.div animate={{ x: [0, 10, 0] }}>
      Content
    </motion.div>
  </motion.div>
</motion.div>

/* ✅ GOOD - 절제된 모션 */
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>
```

## Spacing Anti-Patterns

### 기본 간격만 사용

```jsx
/* ❌ BAD - 모든 곳에 gap-4 */
<div className="space-y-4">
  <Section />
  <Section />
  <Section />
</div>

/* ✅ GOOD - 리듬감 있는 간격 */
<div>
  <Section className="mb-24" /> {/* 큰 섹션 사이 */}
  <Section className="mb-16" /> {/* 중간 섹션 사이 */}
  <Section className="mb-8" />  {/* 관련 섹션 사이 */}
</div>
```

## 검증 체크리스트

작업 완료 전 다음을 확인하세요:

```markdown
## Anti-Pattern 검증

### Typography
- [ ] Inter, Roboto, Arial 사용하지 않음
- [ ] 타입 스케일에 명확한 대비 있음
- [ ] 다양한 폰트 무게 활용

### Color
- [ ] 보라-핑크 그래디언트 없음
- [ ] 색상 팔레트 3-4개로 제한
- [ ] 각 색상에 명확한 용도 정의

### Layout
- [ ] 동일 크기 카드 그리드 회피
- [ ] 의도적인 비대칭 요소 존재
- [ ] 섹션마다 다른 레이아웃

### Component
- [ ] shadcn/ui 기본 스타일 커스터마이징
- [ ] 호버/포커스 상태 정의
- [ ] 인터랙션 피드백 존재

### Motion
- [ ] 상태 변화에 애니메이션 적용
- [ ] 과도하지 않은 절제된 모션
- [ ] 성능 영향 고려
```
