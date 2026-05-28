# Riverpod 패턴 모음

house-hold-account 프로젝트에서 사용하는 Riverpod 상태관리 패턴들입니다.

## 핵심 개념

### SafeNotifier: 필수 패턴

**문제**: StateNotifier에서 비동기 작업 중 위젯이 dispose되면 `"_dependents.isEmpty" 에러` 발생

**해결책**: SafeNotifier를 상속하여 `mounted` 체크

```dart
// lib/core/providers/safe_notifier.dart
abstract class SafeNotifier<T> extends StateNotifier<AsyncValue<T>> {
  final Ref ref;

  SafeNotifier(this.ref, AsyncValue<T> initialState) : super(initialState);

  // 비동기 작업 후 mounted 체크
  Future<R?> safeAsync<R>(Future<R> Function() action) async {
    final result = await action();
    if (!mounted) return null;
    return result;
  }

  // Provider 무효화 전 mounted 체크
  void safeInvalidate(ProviderBase provider) {
    if (mounted) {
      ref.invalidate(provider);
    }
  }

  // 상태 업데이트 전 mounted 체크
  void safeUpdateState(AsyncValue<T> newState) {
    if (mounted) {
      state = newState;
    }
  }

  // AsyncValue.guard 안전 구현
  Future<void> safeGuard(Future<T> Function() action) async {
    if (!mounted) return;
    state = const AsyncValue.loading();

    final result = await AsyncValue.guard(action);
    if (!mounted) return;
    state = result;
  }
}
```

**사용 필수**: 모든 비동기 StateNotifier는 SafeNotifier를 상속해야 함

---

## Provider 패턴

### 1. FutureProvider: 단순 데이터 조회

**언제 사용**: 매개변수가 없거나 상태 변경이 필요 없을 때

```dart
// 매개변수 없음
final currentUserProvider = FutureProvider<User>((ref) async {
  return ref.watch(authServiceProvider).getCurrentUser();
});

// 매개변수 있음 (family)
final userColorProvider = FutureProvider.family<String, String>((
  ref,
  userId,
) async {
  return ref.watch(profileRepositoryProvider).getUserColor(userId);
});
```

**특징**:
- 자동으로 캐싱됨
- AsyncValue<T> 상태 제공 (loading/data/error)
- 의존성 변경 시 자동 갱신

---

### 2. StateNotifierProvider + SafeNotifier: 상태 변경 필요

**언제 사용**: 데이터 CRUD, 상태 변경이 필요할 때

```dart
// State 타입: AsyncValue<List<PaymentMethod>>
class PaymentMethodNotifier extends SafeNotifier<List<PaymentMethod>> {
  final PaymentMethodRepository _repository;
  final String? _ledgerId;

  PaymentMethodNotifier(this._repository, this._ledgerId, Ref ref)
    : super(ref, const AsyncValue.loading()) {
    if (_ledgerId != null) {
      Future.microtask(() => loadPaymentMethods());
    }
  }

  Future<void> loadPaymentMethods() async {
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
      rethrow; // 필수!
    }
  }

  Future<void> addPaymentMethod(String name) async {
    try {
      final newMethod = await safeAsync(() =>
        _repository.createPaymentMethod(ledgerId: _ledgerId!, name: name)
      );
      if (newMethod == null) return; // disposed

      safeInvalidate(paymentMethodsProvider);
      await loadPaymentMethods();
    } catch (e, st) {
      safeUpdateState(AsyncValue.error(e, st));
      rethrow;
    }
  }
}

final paymentMethodNotifierProvider = StateNotifierProvider<
  PaymentMethodNotifier,
  AsyncValue<List<PaymentMethod>>
>((ref) {
  final repository = ref.watch(paymentMethodRepositoryProvider);
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  return PaymentMethodNotifier(repository, ledgerId, ref);
});
```

**특징**:
- 초기화: Future.microtask로 생성자 후 비동기 작업 수행
- safeAsync/safeInvalidate/safeUpdateState로 안전한 처리
- rethrow로 에러 전파
- 메서드를 통해 상태 변경

---

### 3. StreamProvider: 실시간 데이터

**언제 사용**: Realtime 구독, FCM 토큰 스트림 등

```dart
// Supabase Realtime 구독
final ledgerStreamProvider = StreamProvider<List<Ledger>>((ref) {
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  if (ledgerId == null) return const Stream.empty();

  return ref.watch(ledgerRepositoryProvider)
    .streamLedgerChanges(ledgerId);
});

// FCM 토큰 스트림
final fcmTokenStreamProvider = StreamProvider<String>((ref) {
  return ref.watch(firebaseMessagingServiceProvider)
    .onTokenRefresh;
});
```

---

### 4. StateProvider: 간단한 상태 (ui state)

**언제 사용**: 선택된 항목, 탭 인덱스, 토글 등 간단한 UI 상태

```dart
// 선택된 가계부 ID
final selectedLedgerIdProvider = StateProvider<String?>((ref) {
  // SharedPreferences에서 복원
  return ref.watch(sharedPreferencesProvider).getString('selectedLedgerId');
});

// 선택된 탭
final selectedPaymentMethodTabProvider = StateProvider<int>((ref) {
  return 0; // 초기값
});

// 사용 예
ref.read(selectedLedgerIdProvider.notifier).state = newLedgerId;
final current = ref.watch(selectedLedgerIdProvider);
```

---

## 의존성 패턴

### 1. Provider를 다른 Provider에서 참조

```dart
// paymentMethodsProvider는 selectedLedgerIdProvider에 의존
final paymentMethodsProvider = FutureProvider<List<PaymentMethod>>((ref) async {
  final ledgerId = ref.watch(selectedLedgerIdProvider); // 의존성!
  if (ledgerId == null) return [];

  return ref.watch(paymentMethodRepositoryProvider)
    .getPaymentMethods(ledgerId);
});

// selectedLedgerIdProvider가 변경되면 자동으로 paymentMethodsProvider 갱신됨!
```

### 2. 상태 변경 감지

```dart
// selectedLedgerIdProvider 변경 시 SharedPreferences에 저장
final ledgerIdPersistenceProvider = StateNotifierProvider.autoDispose<
  LedgerIdPersistence,
  void
>((ref) {
  return LedgerIdPersistence(ref);
});

class LedgerIdPersistence extends StateNotifier<void> {
  final Ref ref;

  LedgerIdPersistence(this.ref) : super(null) {
    ref.listen(selectedLedgerIdProvider, (previous, next) {
      if (next != null) {
        ref.watch(sharedPreferencesProvider)
          .setString('selectedLedgerId', next);
      }
    });
  }
}
```

---

## 실제 예시: Payment Method Feature

### Provider 구성

```dart
// 1. Repository Provider
final paymentMethodRepositoryProvider = Provider<PaymentMethodRepository>(
  (ref) => PaymentMethodRepository(),
);

// 2. 데이터 조회 Providers
final paymentMethodsProvider = FutureProvider<List<PaymentMethod>>((ref) async {
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  if (ledgerId == null) return [];

  return ref.watch(paymentMethodRepositoryProvider)
    .getPaymentMethods(ledgerId);
});

final paymentMethodsByOwnerProvider = FutureProvider.family<
  List<PaymentMethod>,
  String
>((ref, ownerUserId) async {
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  if (ledgerId == null) return [];

  return ref.watch(paymentMethodRepositoryProvider)
    .getPaymentMethodsByOwner(
      ledgerId: ledgerId,
      ownerUserId: ownerUserId,
    );
});

final sharedPaymentMethodsProvider = FutureProvider<List<PaymentMethod>>((ref) async {
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  if (ledgerId == null) return [];

  return ref.watch(paymentMethodRepositoryProvider)
    .getSharedPaymentMethods(ledgerId);
});

// 3. 상태 변경 Notifier
class PaymentMethodNotifier extends SafeNotifier<List<PaymentMethod>> {
  final PaymentMethodRepository _repository;
  final String? _ledgerId;
  RealtimeChannel? _channel;

  PaymentMethodNotifier(this._repository, this._ledgerId, Ref ref)
    : super(ref, const AsyncValue.loading()) {
    if (_ledgerId != null) {
      Future.microtask(() {
        _subscribeToChanges();
        loadPaymentMethods();
      });
    } else {
      state = const AsyncValue.data([]);
    }
  }

  void _subscribeToChanges() {
    if (_ledgerId == null) return;

    try {
      _channel = _repository.subscribePaymentMethods(
        ledgerId: _ledgerId,
        onPaymentMethodChanged: () {
          _refreshQuietly();
        },
      );
    } catch (e) {
      debugPrint('Subscribe fail: $e');
    }
  }

  Future<void> _refreshQuietly() async {
    if (_ledgerId == null) return;

    try {
      final methods = await safeAsync(
        () => _repository.getPaymentMethods(_ledgerId),
      );
      if (methods == null) return;

      safeUpdateState(AsyncValue.data(methods));
      safeInvalidate(paymentMethodsProvider);
    } catch (e) {
      debugPrint('Refresh fail: $e');
    }
  }

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
      rethrow;
    }
  }

  @override
  void dispose() {
    _channel?.unsubscribe();
    super.dispose();
  }
}

// 4. Provider 정의
final paymentMethodNotifierProvider = StateNotifierProvider<
  PaymentMethodNotifier,
  AsyncValue<List<PaymentMethod>>
>((ref) {
  final repository = ref.watch(paymentMethodRepositoryProvider);
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  return PaymentMethodNotifier(repository, ledgerId, ref);
});
```

### UI에서 사용

```dart
// 읽기 (watch)
final methods = ref.watch(paymentMethodNotifierProvider);

// 상태 처리
methods.when(
  loading: () => LoadingWidget(),
  data: (data) => MethodsList(data),
  error: (e, st) => ErrorWidget(e),
);

// 쓰기 (read + 메서드 호출)
final notifier = ref.read(paymentMethodNotifierProvider.notifier);
await notifier.addPaymentMethod('새 카드');

// 또는
ref.refresh(paymentMethodNotifierProvider); // 전체 새로고침
```

---

## 주의사항

### 1. 에러 처리: rethrow는 필수

```dart
// ❌ 틀림 - UI에서 에러를 알 수 없음
try {
  state = AsyncValue.data(await doSomething());
} catch (e, st) {
  state = AsyncValue.error(e, st);
  // 여기서 끝나면 호출자가 catch할 수 없음
}

// ✅ 올바름 - UI까지 에러 전파
try {
  state = AsyncValue.data(await doSomething());
} catch (e, st) {
  state = AsyncValue.error(e, st);
  rethrow; // 필수!
}
```

### 2. SafeNotifier 필수 사용

모든 비동기 StateNotifier는 SafeNotifier를 상속해야 합니다.

```dart
// ❌ 틀림
class MyNotifier extends StateNotifier<AsyncValue<Data>> {
  Future<void> load() async {
    final data = await repository.getData();
    state = AsyncValue.data(data); // disposed 후 에러!
  }
}

// ✅ 올바름
class MyNotifier extends SafeNotifier<Data> {
  Future<void> load() async {
    final data = await safeAsync(() => repository.getData());
    if (data == null) return; // disposed
    safeUpdateState(AsyncValue.data(data));
  }
}
```

### 3. Realtime 구독 정리

```dart
// dispose에서 구독 취소
@override
void dispose() {
  _channel?.unsubscribe(); // 메모리 누수 방지
  super.dispose();
}
```

