# UX実装パターン集

React + Tailwind CSS での具体的な実装パターン。

---

## ローディング・フィードバック

### スケルトンスクリーン

**原則**: Doherty Threshold, Labor Illusion

```tsx
// スケルトンコンポーネント
function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "animate-pulse rounded-md bg-gray-200",
        className
      )}
    />
  );
}

// カードのスケルトン
function CardSkeleton() {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4">
      <Skeleton className="h-6 w-3/4 mb-2" />
      <Skeleton className="h-4 w-full mb-1" />
      <Skeleton className="h-4 w-2/3" />
    </div>
  );
}

// 使用例
function ItemList() {
  const { data, isLoading } = useQuery(itemsQueryOptions);

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <CardSkeleton key={i} />
        ))}
      </div>
    );
  }

  return <>{/* 実際のコンテンツ */}</>;
}
```

### ストリーミングレスポンス

**原則**: Doherty Threshold

```tsx
function StreamingMessage({ content }: { content: string }) {
  return (
    <div className="prose">
      {content}
      <span className="inline-block w-2 h-4 ml-1 bg-gray-400 animate-pulse" />
    </div>
  );
}

// AIチャットでの使用
function ChatMessage({ message, isStreaming }: Props) {
  return (
    <div className="rounded-lg bg-gray-100 p-4">
      {isStreaming ? (
        <StreamingMessage content={message.content} />
      ) : (
        <div className="prose">{message.content}</div>
      )}
    </div>
  );
}
```

### 処理中インジケーター

**原則**: Labor Illusion

```tsx
function ProcessingIndicator({ step }: { step: string }) {
  return (
    <div className="flex items-center gap-3 text-gray-600">
      <Loader2 className="h-5 w-5 animate-spin" />
      <span>{step}</span>
    </div>
  );
}

// 複数ステップの処理
function MultiStepProcessing({ steps }: { steps: string[] }) {
  const [currentStep, setCurrentStep] = useState(0);

  return (
    <div className="space-y-2">
      {steps.map((step, i) => (
        <div
          key={step}
          className={cn(
            "flex items-center gap-2",
            i < currentStep && "text-green-600",
            i === currentStep && "text-blue-600",
            i > currentStep && "text-gray-400"
          )}
        >
          {i < currentStep ? (
            <Check className="h-4 w-4" />
          ) : i === currentStep ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Circle className="h-4 w-4" />
          )}
          <span>{step}</span>
        </div>
      ))}
    </div>
  );
}
```

### Optimistic Update

**原則**: Doherty Threshold

```tsx
function useOptimisticTodo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createTodo,
    onMutate: async (newTodo) => {
      // キャンセル中のクエリをキャンセル
      await queryClient.cancelQueries({ queryKey: ["todos"] });

      // 以前の値を保存
      const previousTodos = queryClient.getQueryData(["todos"]);

      // 楽観的に更新
      queryClient.setQueryData(["todos"], (old: Todo[]) => [
        ...old,
        { ...newTodo, id: "temp-id", status: "pending" },
      ]);

      return { previousTodos };
    },
    onError: (err, newTodo, context) => {
      // エラー時にロールバック
      queryClient.setQueryData(["todos"], context?.previousTodos);
    },
    onSettled: () => {
      // 最新データで再取得
      queryClient.invalidateQueries({ queryKey: ["todos"] });
    },
  });
}
```

---

## フォーム・入力

### インラインバリデーション

**原則**: Cognitive Load, Doherty Threshold

```tsx
function FormField({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      {children}
      {error && (
        <p className="text-sm text-red-600 flex items-center gap-1">
          <AlertCircle className="h-4 w-4" />
          {error}
        </p>
      )}
    </div>
  );
}

// 使用例（react-hook-form）
function EmailField() {
  const { register, formState: { errors } } = useForm();

  return (
    <FormField label="メールアドレス" error={errors.email?.message}>
      <input
        {...register("email", {
          required: "メールアドレスは必須です",
          pattern: {
            value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: "有効なメールアドレスを入力してください",
          },
        })}
        className={cn(
          "w-full rounded-md border px-3 py-2",
          errors.email
            ? "border-red-500 focus:ring-red-500"
            : "border-gray-300 focus:ring-blue-500"
        )}
      />
    </FormField>
  );
}
```

### ステップフォーム

**原則**: Progressive Disclosure, Goal Gradient Effect

```tsx
function StepForm({ steps, currentStep, onStepChange }: Props) {
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="space-y-6">
      {/* プログレスバー */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-gray-600">
          <span>ステップ {currentStep + 1} / {steps.length}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="h-2 rounded-full bg-gray-200">
          <div
            className="h-2 rounded-full bg-blue-600 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* ステップインジケーター */}
      <div className="flex justify-between">
        {steps.map((step, i) => (
          <div
            key={step.title}
            className={cn(
              "flex flex-col items-center",
              i <= currentStep ? "text-blue-600" : "text-gray-400"
            )}
          >
            <div
              className={cn(
                "flex h-8 w-8 items-center justify-center rounded-full border-2",
                i < currentStep && "bg-blue-600 border-blue-600 text-white",
                i === currentStep && "border-blue-600",
                i > currentStep && "border-gray-300"
              )}
            >
              {i < currentStep ? <Check className="h-4 w-4" /> : i + 1}
            </div>
            <span className="mt-1 text-xs">{step.title}</span>
          </div>
        ))}
      </div>

      {/* コンテンツ */}
      <div>{steps[currentStep].content}</div>
    </div>
  );
}
```

### デフォルト値の設定

**原則**: Default Bias

```tsx
// フォームのデフォルト値
const defaultValues = {
  notifications: true,  // 推奨設定をデフォルトに
  language: "ja",
  theme: "system",
};

function SettingsForm() {
  const form = useForm({ defaultValues });

  return (
    <form>
      <label className="flex items-center gap-2">
        <input type="checkbox" {...form.register("notifications")} />
        <span>通知を受け取る</span>
        <span className="text-xs text-gray-500">（推奨）</span>
      </label>
    </form>
  );
}
```

---

## ナビゲーション・構造

### 視覚的階層

**原則**: Visual Hierarchy, Serial Position Effect

```tsx
function PricingCards() {
  return (
    <div className="grid grid-cols-3 gap-6">
      {/* Basic */}
      <div className="rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium">Basic</h3>
        <p className="mt-2 text-3xl font-bold">¥980</p>
      </div>

      {/* Pro - 強調 */}
      <div className="rounded-lg border-2 border-blue-600 p-6 relative shadow-lg">
        <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-3 py-1 rounded-full text-sm">
          おすすめ
        </div>
        <h3 className="text-lg font-medium">Pro</h3>
        <p className="mt-2 text-3xl font-bold text-blue-600">¥2,980</p>
      </div>

      {/* Enterprise */}
      <div className="rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-medium">Enterprise</h3>
        <p className="mt-2 text-3xl font-bold">お問い合わせ</p>
      </div>
    </div>
  );
}
```

### 折りたたみセクション

**原則**: Progressive Disclosure

```tsx
function Accordion({ items }: { items: AccordionItem[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <div className="divide-y divide-gray-200 border rounded-lg">
      {items.map((item, index) => (
        <div key={item.title}>
          <button
            onClick={() => setOpenIndex(openIndex === index ? null : index)}
            className="flex w-full items-center justify-between p-4 text-left"
          >
            <span className="font-medium">{item.title}</span>
            <ChevronDown
              className={cn(
                "h-5 w-5 transition-transform",
                openIndex === index && "rotate-180"
              )}
            />
          </button>
          {openIndex === index && (
            <div className="px-4 pb-4 text-gray-600">{item.content}</div>
          )}
        </div>
      ))}
    </div>
  );
}
```

---

## 社会的証明・信頼

### レビュー表示

**原則**: Social Proof

```tsx
function ReviewSection({ reviews, averageRating, totalCount }: Props) {
  return (
    <div className="space-y-4">
      {/* サマリー */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={cn(
                "h-5 w-5",
                i < Math.round(averageRating)
                  ? "fill-yellow-400 text-yellow-400"
                  : "text-gray-300"
              )}
            />
          ))}
        </div>
        <span className="text-lg font-medium">{averageRating.toFixed(1)}</span>
        <span className="text-gray-500">({totalCount.toLocaleString()}件のレビュー)</span>
      </div>

      {/* レビュー一覧 */}
      <div className="space-y-4">
        {reviews.map((review) => (
          <div key={review.id} className="border-b pb-4">
            <div className="flex items-center gap-2">
              <Avatar src={review.user.avatar} />
              <span className="font-medium">{review.user.name}</span>
              <span className="text-gray-500 text-sm">{review.date}</span>
            </div>
            <p className="mt-2">{review.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 利用者数表示

**原則**: Social Proof

```tsx
function TrustIndicators() {
  return (
    <div className="flex items-center gap-8 text-gray-600">
      <div className="flex items-center gap-2">
        <Users className="h-5 w-5" />
        <span><strong>10,000+</strong> ユーザーが利用中</span>
      </div>
      <div className="flex items-center gap-2">
        <Star className="h-5 w-5 text-yellow-400" />
        <span>評価 <strong>4.8</strong> / 5.0</span>
      </div>
      <div className="flex items-center gap-2">
        <Shield className="h-5 w-5" />
        <span>SSL暗号化通信</span>
      </div>
    </div>
  );
}
```

---

## エラー・確認

### 確認ダイアログ

**原則**: Intentional Friction, Loss Aversion

```tsx
function DeleteConfirmDialog({ isOpen, onClose, onConfirm, itemName }: Props) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-red-600">
            <AlertTriangle className="h-5 w-5" />
            削除の確認
          </DialogTitle>
        </DialogHeader>

        <div className="py-4">
          <p className="text-gray-600">
            「{itemName}」を削除しますか？
          </p>
          <p className="mt-2 text-sm text-red-600">
            この操作は取り消せません。
          </p>
        </div>

        <DialogFooter className="gap-2">
          <Button variant="outline" onClick={onClose}>
            キャンセル
          </Button>
          <Button variant="destructive" onClick={onConfirm}>
            削除する
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

### 成功フィードバック

**原則**: Peak-End Rule, User Delight

```tsx
function SuccessAnimation({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <div className="absolute inset-0 animate-ping rounded-full bg-green-400 opacity-25" />
        <div className="relative flex h-16 w-16 items-center justify-center rounded-full bg-green-500">
          <Check className="h-8 w-8 text-white" />
        </div>
      </div>
      <h2 className="mt-6 text-xl font-semibold text-gray-900">{message}</h2>
    </div>
  );
}
```

---

## 希少性・緊急性

### 残り在庫表示

**原則**: Scarcity Effect

```tsx
function StockIndicator({ stock }: { stock: number }) {
  if (stock === 0) {
    return <span className="text-red-600 font-medium">在庫切れ</span>;
  }

  if (stock <= 5) {
    return (
      <span className="text-orange-600 font-medium flex items-center gap-1">
        <AlertCircle className="h-4 w-4" />
        残り{stock}点
      </span>
    );
  }

  return <span className="text-green-600">在庫あり</span>;
}
```

### カウントダウン

**原則**: Scarcity Effect（適度に使用）

```tsx
function CountdownTimer({ endTime }: { endTime: Date }) {
  const [remaining, setRemaining] = useState(getRemainingTime(endTime));

  useEffect(() => {
    const timer = setInterval(() => {
      setRemaining(getRemainingTime(endTime));
    }, 1000);
    return () => clearInterval(timer);
  }, [endTime]);

  return (
    <div className="flex items-center gap-2 bg-red-50 text-red-700 px-4 py-2 rounded-lg">
      <Clock className="h-5 w-5" />
      <span className="font-medium">
        残り {remaining.hours}:{remaining.minutes}:{remaining.seconds}
      </span>
    </div>
  );
}
```

---

## ゲーミフィケーション

### 進捗表示

**原則**: Goal Gradient Effect, Zeigarnik Effect

```tsx
function ProgressCard({ current, total, title }: Props) {
  const percentage = (current / total) * 100;

  return (
    <div className="rounded-lg border bg-white p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium">{title}</span>
        <span className="text-sm text-gray-500">{current} / {total}</span>
      </div>
      <div className="h-3 rounded-full bg-gray-200">
        <div
          className="h-3 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
      {percentage >= 80 && (
        <p className="mt-2 text-sm text-blue-600 font-medium">
          あと少しで完了です！
        </p>
      )}
    </div>
  );
}
```

### バッジ・実績

**原則**: Gamification, Variable Reward

```tsx
function AchievementBadge({ achievement, isUnlocked }: Props) {
  return (
    <div
      className={cn(
        "relative flex flex-col items-center p-4 rounded-lg border",
        isUnlocked ? "bg-white" : "bg-gray-100 opacity-50"
      )}
    >
      {isUnlocked && (
        <div className="absolute -top-2 -right-2">
          <div className="flex h-6 w-6 items-center justify-center rounded-full bg-green-500">
            <Check className="h-4 w-4 text-white" />
          </div>
        </div>
      )}
      <div className="text-3xl">{achievement.icon}</div>
      <span className="mt-2 font-medium text-sm">{achievement.name}</span>
      <span className="text-xs text-gray-500">{achievement.description}</span>
    </div>
  );
}
```
