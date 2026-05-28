# Clean Architecture Guide

house-hold-account 프로젝트는 **Clean Architecture** + **Feature-first 구조**를 사용합니다.

## 디렉토리 구조

```
lib/features/{feature}/
├── domain/
│   └── entities/               # 비즈니스 엔티티 (불변 객체, 최소한의 로직)
│       ├── {entity_name}.dart
│       └── ...
├── data/
│   ├── models/                 # Entity 확장 + DB/API 직렬화
│   │   └── {entity_name}_model.dart
│   ├── repositories/           # 데이터 접근 계층 (Repository 패턴)
│   │   ├── {entity_name}_repository.dart
│   │   └── ...
│   └── services/               # 외부 서비스 (SMS, FCM 등)
│       ├── {service_name}_service.dart
│       └── ...
└── presentation/
    ├── pages/                  # 화면 단위 위젯 (라우트 대상)
    │   └── {feature}_page.dart
    ├── widgets/                # 재사용 위젯 (UI 컴포넌트)
    │   ├── {widget_name}.dart
    │   └── ...
    └── providers/              # Riverpod Provider (상태관리)
        └── {entity_name}_provider.dart
```

## 레이어별 책임

### Domain Layer (도메인 레이어)

**Entity 정의**: 비즈니스 규칙을 표현하는 불변 객체

```dart
// domain/entities/transaction.dart
class Transaction extends Equatable {
  final String id;
  final String ledgerId;
  final int amount;
  final DateTime date;
  // ... 필드들

  const Transaction({
    required this.id,
    required this.ledgerId,
    required this.amount,
    required this.date,
    // ...
  });

  // copyWith 메서드 제공 (불변성)
  Transaction copyWith({
    String? id,
    String? ledgerId,
    int? amount,
    DateTime? date,
    // ...
  }) {
    return Transaction(
      id: id ?? this.id,
      ledgerId: ledgerId ?? this.ledgerId,
      amount: amount ?? this.amount,
      date: date ?? this.date,
      // ...
    );
  }

  @override
  List<Object?> get props => [id, ledgerId, amount, date, /* ... */];
}
```

**특징**:
- 어떤 외부 라이브러리도 의존하지 않음 (순수 Dart)
- 비즈니스 로직만 포함
- 불변 객체 (copyWith 패턴)
- Equatable 상속 (동등성 비교 자동화)

---

### Data Layer (데이터 레이어)

#### Model: Entity 확장 + 직렬화

```dart
// data/models/transaction_model.dart
class TransactionModel extends Transaction {
  const TransactionModel({
    required super.id,
    required super.ledgerId,
    required super.amount,
    required super.date,
    // ...
  });

  // JSON → Dart 변환
  factory TransactionModel.fromJson(Map<String, dynamic> json) {
    return TransactionModel(
      id: json['id'] as String,
      ledgerId: json['ledger_id'] as String,
      amount: json['amount'] as int,
      date: DateTime.parse(json['date'] as String),
      // ...
    );
  }

  // Dart → JSON 변환
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'ledger_id': ledgerId,
      'amount': amount,
      'date': date.toIso8601String(),
      // ...
    };
  }
}
```

**특징**:
- Entity의 자식 클래스 (상속)
- fromJson, toJson 메서드 포함
- Repository에서 생성/반환

#### Repository: 데이터 접근 계층

```dart
// data/repositories/transaction_repository.dart
class TransactionRepository {
  final _client = SupabaseConfig.client;

  // 조회
  Future<List<TransactionModel>> getTransactions(String ledgerId) async {
    final response = await _client
        .from('transactions')
        .select('*, categories(...), profiles(...)')
        .eq('ledger_id', ledgerId)
        .order('date', ascending: false);

    return (response as List)
        .map((json) => TransactionModel.fromJson(json))
        .toList();
  }

  // 생성
  Future<TransactionModel> createTransaction({
    required String ledgerId,
    required int amount,
    // ...
  }) async {
    try {
      final response = await _client
          .from('transactions')
          .insert({
            'ledger_id': ledgerId,
            'amount': amount,
            // ...
          })
          .select()
          .single();

      return TransactionModel.fromJson(response);
    } catch (e) {
      // 에러 처리: rethrow 필수
      rethrow;
    }
  }

  // 수정
  Future<TransactionModel> updateTransaction({
    required String id,
    int? amount,
    // ...
  }) async {
    try {
      final updates = <String, dynamic>{};
      if (amount != null) updates['amount'] = amount;
      // ...

      final response = await _client
          .from('transactions')
          .update(updates)
          .eq('id', id)
          .select()
          .single();

      return TransactionModel.fromJson(response);
    } catch (e) {
      rethrow;
    }
  }

  // 삭제
  Future<void> deleteTransaction(String id) async {
    await _client.from('transactions').delete().eq('id', id);
  }
}
```

**특징**:
- Supabase 클라이언트 직접 사용
- 모든 DB 에러는 rethrow (UI까지 전파)
- 데이터 변환은 Model에서 처리
- CRUD 메서드 제공

#### Service: 외부 서비스 통합

```dart
// data/services/sms_scanner_service.dart
class SmsScannerService {
  final LearnedSmsFormatRepository _repository;

  SmsScannerService(this._repository);

  // SMS 메시지 분석
  Future<Map<String, dynamic>?> scanSms(String smsContent) async {
    // 한국 금융기관 패턴 매칭
    final patterns = KoreanFinancialPatterns.allPatterns;

    for (final pattern in patterns) {
      final match = RegExp(pattern).firstMatch(smsContent);
      if (match != null) {
        return {
          'amount': int.parse(match.group(1) ?? '0'),
          'bank': match.group(2),
          'balance': int.parse(match.group(3) ?? '0'),
        };
      }
    }

    return null;
  }
}
```

---

### Presentation Layer (표현 레이어)

#### Provider: 상태 관리

**FutureProvider**: 단순 데이터 조회

```dart
// presentation/providers/transaction_provider.dart

final transactionRepositoryProvider = Provider<TransactionRepository>(
  (ref) => TransactionRepository(),
);

// 현재 가계부의 거래 목록 조회
final transactionsProvider = FutureProvider<List<TransactionModel>>((ref) async {
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  if (ledgerId == null) return [];

  final repository = ref.watch(transactionRepositoryProvider);
  return repository.getTransactions(ledgerId);
});
```

**StateNotifierProvider**: 상태 변경 필요 시

```dart
// presentation/providers/transaction_provider.dart

// TransactionNotifier는 SafeNotifier를 상속
class TransactionNotifier extends SafeNotifier<List<TransactionModel>> {
  final TransactionRepository _repository;
  final String? _ledgerId;

  TransactionNotifier(this._repository, this._ledgerId, Ref ref)
    : super(ref, const AsyncValue.loading()) {
    if (_ledgerId != null) {
      Future.microtask(() => loadTransactions());
    } else {
      state = const AsyncValue.data([]);
    }
  }

  Future<void> loadTransactions() async {
    if (_ledgerId == null) return;

    state = const AsyncValue.loading();
    try {
      final transactions = await _repository.getTransactions(_ledgerId);
      if (mounted) {
        state = AsyncValue.data(transactions);
      }
    } catch (e, st) {
      if (mounted) {
        state = AsyncValue.error(e, st);
      }
      rethrow; // UI까지 에러 전파
    }
  }

  Future<void> addTransaction({required int amount, /* ... */}) async {
    try {
      await safeAsync(() => _repository.createTransaction(
        ledgerId: _ledgerId!,
        amount: amount,
        // ...
      ));

      // 데이터 새로고침
      safeInvalidate(transactionsProvider);
      await loadTransactions();
    } catch (e, st) {
      safeUpdateState(AsyncValue.error(e, st));
      rethrow;
    }
  }
}

final transactionNotifierProvider = StateNotifierProvider<
  TransactionNotifier,
  AsyncValue<List<TransactionModel>>
>((ref) {
  final repository = ref.watch(transactionRepositoryProvider);
  final ledgerId = ref.watch(selectedLedgerIdProvider);
  return TransactionNotifier(repository, ledgerId, ref);
});
```

#### Page: 화면 단위 위젯

```dart
// presentation/pages/transaction_list_page.dart

class TransactionListPage extends ConsumerWidget {
  const TransactionListPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final transactionsAsync = ref.watch(transactionNotifierProvider);

    return transactionsAsync.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      data: (transactions) => ListView.builder(
        itemCount: transactions.length,
        itemBuilder: (context, index) {
          final tx = transactions[index];
          return TransactionCard(transaction: tx);
        },
      ),
      error: (error, st) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('거래 목록 조회 실패: $error')),
        );
        return const Center(child: Text('오류가 발생했습니다.'));
      },
    );
  }
}
```

#### Widget: 재사용 컴포넌트

```dart
// presentation/widgets/transaction_card.dart

class TransactionCard extends StatelessWidget {
  final TransactionModel transaction;

  const TransactionCard({
    Key? key,
    required this.transaction,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(transaction.title ?? '거래'),
        subtitle: Text(transaction.date.toString()),
        trailing: Text('${transaction.amount}원'),
      ),
    );
  }
}
```

---

## 파일 생성 순서 (Best Practice)

새 기능을 구현할 때 다음 순서를 따르세요:

### 1️⃣ Entity 정의 (domain/entities/)

- 비즈니스 엔티티 클래스 작성
- 필드, copyWith, props 정의
- 아무 외부 라이브러리도 import 하지 않음

### 2️⃣ Model 정의 (data/models/)

- Entity 상속
- fromJson, toJson 메서드 구현
- 선택사항: toCreateJson, toUpdateJson 헬퍼

### 3️⃣ Repository 구현 (data/repositories/)

- Supabase CRUD 로직
- 모든 에러에 rethrow 적용
- Model 직렬화 처리

### 4️⃣ Service 구현 (data/services/) - 필요시

- SMS, FCM 같은 외부 서비스
- 선택사항 (모든 기능이 필요한 것은 아님)

### 5️⃣ Provider 구현 (presentation/providers/)

- Repository/Service Provider 정의
- 데이터 조회 Provider (Fut ureProvider)
- 상태 변경 Provider (StateNotifierProvider + SafeNotifier)

### 6️⃣ Page 구현 (presentation/pages/)

- 라우트 대상 위젯
- Provider를 watch하여 UI 구성
- 에러/로딩 상태 처리

### 7️⃣ Widget 구현 (presentation/widgets/)

- 재사용 컴포넌트
- 필요한 데이터만 Props로 받음
- 상태관리는 최소화

---

## 의존성 방향

```
Domain Layer (entities)
        ↑
        │ depends on
        │
Data Layer (models, repositories, services)
        ↑
        │ depends on
        │
Presentation Layer (providers, pages, widgets)
```

**중요**: 하위 계층은 상위 계층을 의존해서는 안 됨. 항상 위 방향으로만 의존합니다.

---

## 실제 예시: Payment Method Feature

```
features/payment_method/
├── domain/entities/
│   ├── payment_method.dart      # PaymentMethod 엔티티
│   ├── auto_save_mode.dart      # AutoSaveMode enum
│   └── pending_transaction.dart # PendingTransaction 엔티티
├── data/
│   ├── models/
│   │   ├── payment_method_model.dart
│   │   ├── pending_transaction_model.dart
│   │   └── learned_sms_format_model.dart
│   ├── repositories/
│   │   ├── payment_method_repository.dart
│   │   ├── pending_transaction_repository.dart
│   │   └── learned_sms_format_repository.dart
│   └── services/
│       ├── auto_save_service.dart          # 메인 오케스트레이터
│       ├── sms_scanner_service.dart        # SMS 분석
│       ├── sms_parsing_service.dart        # 한국 패턴 파싱
│       ├── category_mapping_service.dart   # 카테고리 자동 할당
│       └── duplicate_check_service.dart    # 중복 검사
└── presentation/
    ├── pages/
    │   ├── payment_methods_page.dart
    │   ├── pending_transactions_page.dart
    │   └── auto_save_settings_page.dart
    ├── widgets/
    │   ├── payment_method_card.dart
    │   ├── pending_transaction_card.dart
    │   └── auto_save_settings_form.dart
    └── providers/
        └── payment_method_provider.dart
```

