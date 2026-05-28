# 에러 처리 패턴

house-hold-account 프로젝트의 **에러 처리 원칙**과 **구현 패턴**.

## 핵심 원칙

> **모든 에러는 절대 무시하지 않는다**
>
> DB 에러, 네트워크 에러, 예상치 못한 에러 등 모든 예외 상황은:
> 1. 반드시 catch하여 처리
> 2. 에러를 상위 계층으로 전파 (rethrow)
> 3. UI 계층에서 사용자에게 명확하게 표시
>
> 에러를 삼키거나 무시하면 앱이 불안정해지고 사용자 경험이 나빠집니다.

---

## 에러 처리 계층

### Layer 1: Repository (데이터 접근 계층)

**책임**: DB 에러를 프로세싱하고 상위로 전파

```dart
// ❌ 틀림 - 에러를 삼킴
Future<List<Transaction>> getTransactions(String ledgerId) async {
  try {
    return await _client.from('transactions').select().eq('ledger_id', ledgerId);
  } catch (e) {
    debugPrint('Error: $e');
    return []; // 에러를 숨김!
  }
}

// ✅ 올바름 - 에러를 전파
Future<List<Transaction>> getTransactions(String ledgerId) async {
  try {
    final response = await _client
        .from('transactions')
        .select()
        .eq('ledger_id', ledgerId);
    return response.map((json) => TransactionModel.fromJson(json)).toList();
  } catch (e) {
    // 필요한 경우 에러 변환 (예: 중복 에러 처리)
    if (SupabaseErrorHandler.isDuplicateError(e)) {
      throw DuplicateItemException(itemType: '거래', itemName: name);
    }
    rethrow; // 원본 에러를 그대로 전파
  }
}
```

### Layer 2: Provider (상태관리 계층)

**책임**: 에러를 AsyncValue.error로 변환하고 전파

```dart
// ❌ 틀림 - 에러를 UI까지 전파하지 않음
class TransactionNotifier extends SafeNotifier<List<Transaction>> {
  Future<void> loadTransactions() async {
    try {
      final txs = await repository.getTransactions(ledgerId);
      if (mounted) {
        state = AsyncValue.data(txs);
      }
    } catch (e, st) {
      // 여기서 끝나면 호출자가 에러를 알 수 없음!
      debugPrint('Load fail: $e');
      state = AsyncValue.error(e, st);
    }
  }
}

// ✅ 올바름 - 에러를 UI까지 전파
class TransactionNotifier extends SafeNotifier<List<Transaction>> {
  Future<void> loadTransactions() async {
    state = const AsyncValue.loading();
    try {
      final txs = await repository.getTransactions(ledgerId);
      if (mounted) {
        state = AsyncValue.data(txs);
      }
    } catch (e, st) {
      if (mounted) {
        state = AsyncValue.error(e, st);
      }
      rethrow; // UI에서 catch할 수 있도록!
    }
  }
}
```

### Layer 3: UI (사용자 인터페이스 계층)

**책임**: 에러를 사용자에게 표시

```dart
// 페이지/위젯에서
final transactionsAsync = ref.watch(transactionNotifierProvider);

transactionsAsync.when(
  loading: () => LoadingWidget(),
  data: (txs) => TransactionsList(txs),
  error: (error, st) {
    // 사용자에게 피드백
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('거래 조회 실패: $error')),
      );
    });
    return ErrorWidget(error: error);
  },
);
```

---

## SafeNotifier 안전 패턴

### 패턴 1: safeAsync

dispose 후에도 안전하게 비동기 작업 수행

```dart
Future<PaymentMethod> createPaymentMethod(String name) async {
  try {
    // safeAsync로 감싼 비동기 작업
    final method = await safeAsync(() =>
      repository.createPaymentMethod(ledgerId: ledgerId, name: name)
    );

    if (method == null) {
      // disposed된 경우
      return;
    }

    // method 사용 가능
    safeUpdateState(AsyncValue.data(/* ... */));
  } catch (e, st) {
    safeUpdateState(AsyncValue.error(e, st));
    rethrow;
  }
}
```

**safeAsync 내부 동작**:
```dart
Future<R?> safeAsync<R>(Future<R> Function() action) async {
  final result = await action();
  if (!mounted) return null; // dispose된 경우 null 반환
  return result;
}
```

### 패턴 2: safeInvalidate

Provider 무효화 시 mounted 체크

```dart
Future<void> updatePaymentMethod({required String id, required String name}) async {
  try {
    await safeAsync(() =>
      repository.updatePaymentMethod(id: id, name: name)
    );

    // Realtime 구독이 있으면 자동 갱신되지만,
    // 명시적으로 Provider 무효화
    safeInvalidate(paymentMethodsProvider);
  } catch (e, st) {
    safeUpdateState(AsyncValue.error(e, st));
    rethrow;
  }
}
```

### 패턴 3: safeUpdateState

상태 업데이트 전 mounted 체크

```dart
Future<void> loadItems() async {
  state = const AsyncValue.loading();
  try {
    final items = await repository.getItems(ledgerId);

    // 안전하게 상태 업데이트
    safeUpdateState(AsyncValue.data(items));
  } catch (e, st) {
    safeUpdateState(AsyncValue.error(e, st));
    rethrow;
  }
}
```

### 패턴 4: safeGuard

AsyncValue.guard 래핑 + mounted 체크

```dart
Future<void> complexOperation() async {
  await safeGuard(() async {
    // 복잡한 비동기 작업
    await repository.step1();
    await repository.step2();
    await repository.step3();

    // 결과는 자동으로 state에 저장됨
    return newData;
  });
}
```

---

## Supabase 커스텀 에러 처리

### 중복 에러 처리

```dart
// data/repositories/payment_method_repository.dart

import '../../../../core/utils/supabase_error_handler.dart';

Future<PaymentMethod> createPaymentMethod({
  required String ledgerId,
  required String name,
}) async {
  try {
    final response = await _client
        .from('payment_methods')
        .insert({'ledger_id': ledgerId, 'name': name})
        .select()
        .single();

    return PaymentMethodModel.fromJson(response);
  } catch (e) {
    // 중복 에러를 커스텀 예외로 변환
    if (SupabaseErrorHandler.isDuplicateError(e)) {
      throw DuplicateItemException(itemType: '결제수단', itemName: name);
    }
    rethrow;
  }
}
```

### 권한 에러 처리

```dart
Future<List<Ledger>> getLedgers() async {
  try {
    final response = await _client
        .from('ledgers')
        .select()
        .eq('user_id', userId);

    return response.map((json) => LedgerModel.fromJson(json)).toList();
  } catch (e) {
    // RLS 위반 에러 (403)
    if (SupabaseErrorHandler.isPermissionError(e)) {
      throw PermissionException('가계부 접근 권한이 없습니다');
    }
    rethrow;
  }
}
```

---

## 실제 예시: Payment Method

### Repository에서 에러 처리

```dart
// data/repositories/payment_method_repository.dart

class PaymentMethodRepository {
  Future<List<PaymentMethodModel>> getPaymentMethods(String ledgerId) async {
    try {
      final response = await _client
          .from('payment_methods')
          .select()
          .eq('ledger_id', ledgerId)
          .order('sort_order');

      return (response as List)
          .map((json) => PaymentMethodModel.fromJson(json))
          .toList();
    } catch (e) {
      // 더 구체적인 에러 처리 필요하면 여기 추가
      rethrow;
    }
  }

  Future<PaymentMethodModel> createPaymentMethod({
    required String ledgerId,
    required String name,
    // ...
  }) async {
    try {
      final currentUserId = _client.auth.currentUser?.id;
      if (currentUserId == null) {
        throw Exception('로그인이 필요합니다');
      }

      final data = {
        'ledger_id': ledgerId,
        'owner_user_id': currentUserId,
        'name': name,
        // ...
      };

      final response = await _client
          .from('payment_methods')
          .insert(data)
          .select()
          .single();

      return PaymentMethodModel.fromJson(response);
    } catch (e) {
      // 중복된 이름
      if (SupabaseErrorHandler.isDuplicateError(e)) {
        throw DuplicateItemException(itemType: '결제수단', itemName: name);
      }
      rethrow;
    }
  }
}
```

### Provider에서 에러 처리

```dart
// presentation/providers/payment_method_provider.dart

class PaymentMethodNotifier extends SafeNotifier<List<PaymentMethod>> {
  Future<void> loadPaymentMethods() async {
    if (_ledgerId == null) {
      state = const AsyncValue.data([]);
      return;
    }

    state = const AsyncValue.loading();
    try {
      final methods = await _repository.getPaymentMethods(_ledgerId);
      if (mounted) {
        state = AsyncValue.data(methods);
      }
    } catch (e, st) {
      if (mounted) {
        state = AsyncValue.error(e, st);
      }
      rethrow; // UI에서 처리 가능
    }
  }

  Future<void> createPaymentMethod({required String name}) async {
    if (_ledgerId == null) throw Exception('가계부를 선택해주세요');

    try {
      final method = await safeAsync(() =>
        _repository.createPaymentMethod(ledgerId: _ledgerId!, name: name)
      );

      if (method == null) return;

      safeInvalidate(paymentMethodsProvider);
      await loadPaymentMethods();
    } catch (e, st) {
      safeUpdateState(AsyncValue.error(e, st));
      rethrow; // 호출자가 처리 가능
    }
  }
}
```

### UI에서 에러 표시

```dart
// presentation/pages/payment_methods_page.dart

class PaymentMethodsPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final methodsAsync = ref.watch(paymentMethodNotifierProvider);

    return methodsAsync.when(
      loading: () => Center(child: CircularProgressIndicator()),
      data: (methods) => PaymentMethodsList(methods: methods),
      error: (error, st) {
        // 사용자에게 에러 표시
        WidgetsBinding.instance.addPostFrameCallback((_) {
          String message = '오류가 발생했습니다';

          if (error is DuplicateItemException) {
            message = '이미 존재하는 ${error.itemType}입니다: ${error.itemName}';
          } else if (error is PermissionException) {
            message = error.message;
          } else {
            message = error.toString();
          }

          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(message)),
          );
        });

        return Center(child: ErrorWidget(error: error));
      },
    );
  }
}
```

---

## 에러 처리 체크리스트

코드 리뷰 시 다음을 확인하세요:

- [ ] Repository 메서드에서 try-catch 모든 에러를 catch하고 필요시 `rethrow` 사용
- [ ] Provider (StateNotifier)에서 catch 후 `AsyncValue.error()` 설정 후 반드시 `rethrow`
- [ ] UI에서 `error` 상태 처리 (when/whenData 사용)
- [ ] 사용자에게 에러 메시지 명확하게 표시 (SnackBar, Dialog 등)
- [ ] 모든 try-catch 블록에서 에러를 처리 (에러를 삼키지 않음)
- [ ] 비동기 StateNotifier는 SafeNotifier 상속 필수
- [ ] safeAsync, safeInvalidate, safeUpdateState 사용
- [ ] **DB 에러, 네트워크 에러, 예상치 못한 모든 에러는 절대 무시하지 않음**
- [ ] 에러 발생 경로가 명확한지 확인 (어디서 발생했는지 추적 가능해야 함)

