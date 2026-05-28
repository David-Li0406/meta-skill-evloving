# 테스트 작성 가이드

house-hold-account 프로젝트의 테스트 작성 가이드입니다.

## 테스트 구조

프로젝트는 다음 3가지 테스트 레벨을 지원합니다:

### 1. 단위 테스트 (Unit Tests)

**위치**: `test/` 디렉토리

**대상**:
- Utility 함수
- 비즈니스 로직
- Model 직렬화 (fromJson, toJson)
- Provider 로직

**예시**: `test/features/payment_method/models/payment_method_model_test.dart`

```dart
void main() {
  group('PaymentMethodModel', () {
    test('fromJson을 사용하여 JSON에서 모델을 생성할 수 있어야 한다', () {
      // Arrange: 테스트 데이터 준비
      final json = {
        'id': 'pm_123',
        'name': '신용카드',
        'can_auto_save': true,
      };

      // Act: 실제 동작 수행
      final model = PaymentMethodModel.fromJson(json);

      // Assert: 결과 검증
      expect(model.id, equals('pm_123'));
      expect(model.name, equals('신용카드'));
      expect(model.canAutoSave, isTrue);
    });

    test('toJson을 사용하여 모델을 JSON으로 변환할 수 있어야 한다', () {
      final model = PaymentMethodModel(
        id: 'pm_123',
        name: '신용카드',
        canAutoSave: true,
      );

      final json = model.toJson();

      expect(json['id'], equals('pm_123'));
      expect(json['name'], equals('신용카드'));
      expect(json['can_auto_save'], isTrue);
    });

    test('null 값이 있는 필드도 올바르게 처리해야 한다', () {
      final json = {
        'id': 'pm_123',
        'name': '현금',
        'icon': null,
        'can_auto_save': false,
      };

      final model = PaymentMethodModel.fromJson(json);

      expect(model.icon, isNull);
      expect(model.canAutoSave, isFalse);
    });
  });
}
```

### 2. 위젯 테스트 (Widget Tests)

**위치**: `test/` 디렉토리

**대상**:
- StatelessWidget
- StatefulWidget
- 복잡한 UI 컴포넌트

**예시**: `test/features/payment_method/widgets/payment_method_card_test.dart`

```dart
void main() {
  group('PaymentMethodCard', () {
    testWidgets(
      '결제수단 정보를 표시해야 한다',
      (WidgetTester tester) async {
        // Arrange
        final method = PaymentMethod(
          id: 'pm_123',
          name: '우리 신용카드',
          color: '#FF0000',
        );

        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: PaymentMethodCard(method: method),
            ),
          ),
        );

        // Assert
        expect(find.text('우리 신용카드'), findsOneWidget);
        expect(find.byType(Container), findsWidgets);
      },
    );

    testWidgets(
      '탭 시 콜백이 호출되어야 한다',
      (WidgetTester tester) async {
        bool tapped = false;

        final method = PaymentMethod(id: 'pm_123', name: '카드');

        await tester.pumpWidget(
          MaterialApp(
            home: Scaffold(
              body: PaymentMethodCard(
                method: method,
                onTap: () => tapped = true,
              ),
            ),
          ),
        );

        await tester.tap(find.byType(PaymentMethodCard));
        await tester.pumpAndSettle();

        expect(tapped, isTrue);
      },
    );
  });
}
```

### 3. E2E 테스트 (Maestro)

**위치**: `maestro-tests/` 디렉토리

**대상**:
- 전체 사용자 흐름
- 복잡한 상호작용
- 멀티 사용자 시나리오

**예시**: `maestro-tests/01_payment_method_flow.yaml`

```yaml
appId: com.your.app
name: Payment Method Flow
commands:
  # 결제수단 추가 화면으로 이동
  - tapOn:
      text: 결제수단 추가

  # 이름 입력
  - tapOn:
      hint: 결제수단 이름
  - typeText: 새 카드

  # 자동저장 활성화
  - tapOn:
      text: 자동저장

  # 저장 버튼 클릭
  - tapOn:
      text: 저장

  # 성공 메시지 확인
  - assertVisible:
      text: 결제수단이 추가되었습니다
```

---

## 테스트 작성 원칙

### 1. 한글로 명확하게 설명

**테스트 이름은 "어떤 상황에서 어떤 결과가 나와야 하는가"를 명확히 표현**

```dart
// ❌ 불명확
test('test_payment_method', () { ... });

// ✅ 명확
test('결제수단 생성 시 중복된 이름이 있으면 DuplicateItemException 발생', () { ... });
```

### 2. AAA 패턴: Arrange - Act - Assert

```dart
test('금액이 음수인 거래는 생성할 수 없어야 한다', () {
  // Arrange: 테스트 조건 준비
  final transaction = Transaction(
    amount: -1000,
    date: DateTime.now(),
  );

  // Act: 실제 동작
  final validator = TransactionValidator();
  final result = validator.validate(transaction);

  // Assert: 결과 확인
  expect(result.isValid, isFalse);
  expect(result.errors, contains('금액은 0 이상이어야 합니다'));
});
```

### 3. 단일 책임 원칙

**하나의 테스트는 하나의 시나리오만 테스트**

```dart
// ❌ 틀림 - 너무 많은 시나리오
test('거래 추가 및 삭제 테스트', () {
  // 추가 테스트
  // 삭제 테스트
  // 조회 테스트
});

// ✅ 올바름 - 각각 분리
test('거래를 추가할 수 있어야 한다', () { ... });
test('거래를 삭제할 수 있어야 한다', () { ... });
test('거래를 조회할 수 있어야 한다', () { ... });
```

### 4. Edge Case 테스트

**정상 케이스뿐만 아니라 경계값, 예외 상황도 테스트**

```dart
test('금액 0은 유효해야 한다', () { ... });
test('매우 큰 금액(9,999,999,999)도 처리할 수 있어야 한다', () { ... });
test('null 금액은 에러가 발생해야 한다', () { ... });
```

---

## 실제 예시: Payment Method 테스트

### Model 테스트

```dart
// test/features/payment_method/models/payment_method_model_test.dart

void main() {
  group('PaymentMethodModel', () {
    test('소유자 ID가 null인 경우 공유 결제수단으로 간주되어야 한다', () {
      final model = PaymentMethodModel(
        id: 'pm_123',
        ledgerId: 'ledger_1',
        ownerUserId: null,
        name: '공용 자금',
        canAutoSave: false,
      );

      expect(model.isShared, isTrue);
    });

    test('소유자 ID가 있는 경우 멤버별 결제수단으로 간주되어야 한다', () {
      final model = PaymentMethodModel(
        id: 'pm_123',
        ledgerId: 'ledger_1',
        ownerUserId: 'user_456',
        name: '내 카드',
        canAutoSave: true,
      );

      expect(model.isShared, isFalse);
    });

    test('자동저장 불가능한 결제수단은 canAutoSave가 false여야 한다', () {
      final model = PaymentMethodModel(
        id: 'pm_123',
        ledgerId: 'ledger_1',
        ownerUserId: null,
        name: '공용',
        canAutoSave: false,
      );

      expect(model.canAutoSave, isFalse);
    });
  });
}
```

### Repository 테스트 (Mock 사용)

```dart
// test/features/payment_method/data/repositories/payment_method_repository_test.dart

import 'package:mockito/mockito.dart';

void main() {
  group('PaymentMethodRepository', () {
    late MockSupabaseClient mockClient;
    late PaymentMethodRepository repository;

    setUp(() {
      mockClient = MockSupabaseClient();
      repository = PaymentMethodRepository(client: mockClient);
    });

    test('가계부 ID로 결제수단을 조회할 수 있어야 한다', () async {
      // Arrange
      final mockResponse = [
        {'id': 'pm_1', 'name': '카드1'},
        {'id': 'pm_2', 'name': '카드2'},
      ];

      when(mockClient.from('payment_methods').select())
          .thenReturn(MockQueryBuilder());

      // Act
      final result = await repository.getPaymentMethods('ledger_123');

      // Assert
      expect(result, hasLength(2));
      expect(result[0].name, equals('카드1'));
    });

    test('중복된 이름의 결제수단 생성 시 예외가 발생해야 한다', () async {
      // Arrange
      when(mockClient.from('payment_methods').insert(any))
          .thenThrow(DuplicateException());

      // Act & Assert
      expect(
        () => repository.createPaymentMethod(
          ledgerId: 'ledger_123',
          name: '기존 카드',
        ),
        throwsA(isA<DuplicateItemException>()),
      );
    });
  });
}
```

### Provider 테스트 (Riverpod ProviderContainer)

```dart
// test/features/payment_method/presentation/providers/payment_method_provider_test.dart

void main() {
  group('paymentMethodNotifierProvider', () {
    test('결제수단 목록을 로드할 수 있어야 한다', () async {
      // Arrange
      final container = ProviderContainer(
        overrides: [
          paymentMethodRepositoryProvider.overrideWithValue(
            MockPaymentMethodRepository(),
          ),
          selectedLedgerIdProvider.overrideWithValue('ledger_123'),
        ],
      );

      // Act
      final state = await container.read(paymentMethodNotifierProvider.future);

      // Assert
      expect(state, isNotEmpty);
      expect(state.first.name, equals('신용카드'));
    });

    test('결제수단 추가 후 목록이 업데이트되어야 한다', () async {
      // Arrange
      final container = ProviderContainer(
        overrides: [
          paymentMethodRepositoryProvider.overrideWithValue(
            MockPaymentMethodRepository(),
          ),
          selectedLedgerIdProvider.overrideWithValue('ledger_123'),
        ],
      );

      final notifier = container.read(
        paymentMethodNotifierProvider.notifier,
      );

      // Act
      await notifier.addPaymentMethod(name: '새 카드');

      // Assert
      final updated = container.read(paymentMethodNotifierProvider);
      expect(updated, isA<AsyncValue<List<PaymentMethod>>>());
    });
  });
}
```

---

## 테스트 실행

### 단위 테스트 + 위젯 테스트

```bash
# 전체 테스트 실행
flutter test

# 특정 파일만 실행
flutter test test/features/payment_method/models/payment_method_model_test.dart

# 특정 그룹만 실행
flutter test -k "PaymentMethodModel"

# 특정 테스트만 실행
flutter test -k "중복된 이름"

# 커버리지 생성
flutter test --coverage
```

### Maestro E2E 테스트

```bash
# 전체 E2E 테스트 실행
bash maestro-tests/run_share_test.sh

# 특정 플로우만 실행
maestro test maestro-tests/01_payment_method_flow.yaml

# 빠른 테스트
bash maestro-tests/quick_test.sh
```

---

## 테스트 시 주의사항

### 1. 모의 객체(Mock) 사용

```dart
// ✅ Repository 테스트 시 Mock Supabase 사용
class MockSupabaseClient extends Mock implements SupabaseClient {}

// 또는 mockito 패키지 사용
import 'package:mockito/mockito.dart';

void main() {
  late MockPaymentMethodRepository mockRepository;

  setUp(() {
    mockRepository = MockPaymentMethodRepository();
  });
}
```

### 2. 비동기 테스트

```dart
// ❌ 잘못된 방법
test('비동기 작업을 처리해야 한다', () {
  repository.getPaymentMethods('ledger_123');
  // 작업이 완료되지 않은 상태에서 assert!
});

// ✅ 올바른 방법
test('비동기 작업을 처리해야 한다', () async {
  final result = await repository.getPaymentMethods('ledger_123');
  expect(result, isNotEmpty);
});
```

### 3. 에러 처리 테스트

```dart
test('DB 연결 실패 시 에러가 발생해야 한다', () async {
  when(mockClient.from('payment_methods').select())
      .thenThrow(SocketException('연결 실패'));

  expect(
    () => repository.getPaymentMethods('ledger_123'),
    throwsA(isA<SocketException>()),
  );
});
```

---

## 테스트 커버리지 목표

| 구분 | 목표 |
|------|------|
| Model (Entity, Model 클래스) | 100% |
| Repository (CRUD 로직) | 90% 이상 |
| Provider (상태 관리) | 80% 이상 |
| Widget (UI 컴포넌트) | 70% 이상 |
| Page (페이지) | 50% 이상 (E2E로 커버) |

---

## 테스트 작성 체크리스트

새 기능을 작성할 때:

- [ ] Model 단위 테스트 작성 (100% 커버)
- [ ] Repository 단위 테스트 작성 (정상/에러 케이스)
- [ ] Provider 단위 테스트 작성 (상태 변경 테스트)
- [ ] Widget 위젯 테스트 작성 (UI 렌더링)
- [ ] E2E 테스트 (Maestro) 작성 (사용자 흐름)
- [ ] 에러 케이스 테스트 추가
- [ ] 경계값 테스트 추가
- [ ] 한글로 명확한 테스트 이름 사용
- [ ] 테스트 커버리지 확인

