# 다각도 코드 리뷰 상세 체크리스트

## 목차

1. [UI/UX 체크리스트](#1-uiux-체크리스트)
2. [성능 체크리스트](#2-성능-체크리스트)
3. [디자인 체크리스트](#3-디자인-체크리스트)
4. [코드 품질 체크리스트](#4-코드-품질-체크리스트)
5. [엣지케이스 체크리스트](#5-엣지케이스-체크리스트)
6. [보안 체크리스트](#6-보안-체크리스트)

---

## 1. UI/UX 체크리스트

### 1.1 로딩 상태

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 로딩 인디케이터 | API 호출 시 로딩 상태 표시 | High |
| 스켈레톤 UI | 리스트/카드 로딩 시 스켈레톤 사용 | Medium |
| 버튼 비활성화 | 제출 중 버튼 비활성화 | High |
| 프로그레스 표시 | 긴 작업 시 진행률 표시 | Medium |

```dart
// 좋은 예: AsyncValue.when 사용
state.when(
  loading: () => const CircularProgressIndicator(),
  error: (e, st) => ErrorWidget(message: e.toString()),
  data: (data) => DataListWidget(data: data),
);
```

### 1.2 에러 처리

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 에러 메시지 | 사용자 친화적 에러 메시지 | High |
| 재시도 옵션 | 에러 시 재시도 버튼 제공 | Medium |
| 스낵바/토스트 | 에러 알림 방식 일관성 | Medium |
| 에러 로깅 | 디버그용 에러 로깅 | Low |

```dart
// 좋은 예: 사용자 친화적 에러 메시지
catch (e) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(l10n.errorSaveFailed),  // i18n 사용
      action: SnackBarAction(
        label: l10n.retry,
        onPressed: _retry,
      ),
    ),
  );
}
```

### 1.3 빈 상태

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| Empty State | 데이터 없을 때 안내 메시지 | Medium |
| 액션 유도 | '첫 거래 추가하기' 같은 CTA | Low |
| 일러스트 | 빈 상태 시각적 표현 | Low |

### 1.4 접근성

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| Semantics | 스크린 리더 지원 | Medium |
| 터치 영역 | 최소 48x48 dp | Medium |
| 색상 대비 | WCAG 2.0 기준 충족 | Low |
| 키보드 접근 | 키보드로 모든 기능 접근 | Low |

### 1.5 반응형/적응형

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 화면 크기 대응 | MediaQuery 활용 | Medium |
| 가로/세로 모드 | OrientationBuilder 활용 | Low |
| 텍스트 크기 | textScaleFactor 대응 | Medium |
| 다크모드 | Theme.of(context) 활용 | Medium |

---

## 2. 성능 체크리스트

### 2.1 위젯 최적화

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| const 사용 | 불변 위젯에 const 적용 | Medium |
| 리빌드 범위 | Consumer 위치 최적화 | High |
| Key 사용 | 리스트 아이템에 Key 적용 | Medium |
| 위젯 분리 | 큰 위젯 작은 단위로 분리 | Low |

```dart
// 나쁜 예: 전체 위젯이 리빌드됨
Consumer(
  builder: (context, ref, child) {
    final data = ref.watch(provider);
    return Scaffold(
      body: ExpensiveWidget(),  // 매번 리빌드
    );
  },
);

// 좋은 예: 필요한 부분만 리빌드
Scaffold(
  body: Column(
    children: [
      Consumer(
        builder: (context, ref, child) {
          final data = ref.watch(provider);
          return SmallWidget(data: data);
        },
      ),
      const ExpensiveWidget(),  // const로 리빌드 방지
    ],
  ),
);
```

### 2.2 리스트 최적화

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| ListView.builder | 대량 리스트에 builder 사용 | High |
| itemExtent | 고정 높이 아이템 최적화 | Low |
| 페이지네이션 | 대량 데이터 페이징 처리 | High |
| 캐싱 | 이미지/데이터 캐싱 | Medium |

### 2.3 메모리 관리

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| dispose | Controller/Subscription 정리 | Critical |
| 이미지 메모리 | 대용량 이미지 처리 | High |
| 캐시 크기 | 캐시 메모리 제한 | Medium |
| 전역 상태 | 불필요한 전역 데이터 제거 | Medium |

```dart
class _MyPageState extends State<MyPage> {
  late final TextEditingController _controller;
  StreamSubscription? _subscription;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
    _subscription = stream.listen(_onData);
  }

  @override
  void dispose() {
    _controller.dispose();
    _subscription?.cancel();
    super.dispose();
  }
}
```

### 2.4 네트워크 최적화

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| API 호출 횟수 | 불필요한 중복 호출 제거 | High |
| N+1 문제 | 쿼리 최적화 | High |
| 배치 요청 | 여러 요청 하나로 묶기 | Medium |
| 캐싱 전략 | 응답 캐싱 적용 | Medium |

---

## 3. 디자인 체크리스트

### 3.1 Clean Architecture

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 레이어 분리 | Domain/Data/Presentation 분리 | High |
| 의존성 방향 | 외부에서 내부로만 의존 | High |
| Entity 순수성 | Entity에 프레임워크 의존 없음 | Medium |
| Repository 추상화 | 인터페이스 정의 | Medium |

```
정상적인 의존성 방향:
Presentation --> Domain <-- Data

잘못된 의존성 방향:
Presentation --> Data (Domain 우회)
Domain --> Data (내부가 외부 의존)
```

### 3.2 Feature-first 구조

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 폴더 구조 | feature별 도메인 그룹핑 | Medium |
| 파일 위치 | 올바른 레이어에 배치 | Medium |
| 공유 코드 | shared/ 또는 core/ 활용 | Low |

```
lib/features/transaction/
  domain/
    entities/
      transaction.dart         # Entity
  data/
    models/
      transaction_model.dart   # Model (JSON 변환)
    repositories/
      transaction_repository.dart
  presentation/
    providers/
      transaction_provider.dart
    pages/
      transaction_list_page.dart
    widgets/
      transaction_card.dart
```

### 3.3 SOLID 원칙

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| SRP | 클래스는 하나의 책임만 | High |
| OCP | 확장에 열림, 수정에 닫힘 | Medium |
| LSP | 하위 클래스 대체 가능 | Medium |
| ISP | 인터페이스 분리 | Low |
| DIP | 추상화에 의존 | Medium |

### 3.4 Riverpod 패턴

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| Provider 종류 | 적절한 Provider 타입 선택 | Medium |
| StateNotifier | 복잡한 상태는 StateNotifier | Medium |
| Family | 파라미터 필요 시 family 사용 | Low |
| AutoDispose | 불필요한 상태 자동 정리 | Medium |

---

## 4. 코드 품질 체크리스트

### 4.1 네이밍

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 클래스명 | PascalCase, 명사형 | Low |
| 함수명 | camelCase, 동사형 | Low |
| 변수명 | 의미 있는 이름 | Medium |
| 상수명 | 명확한 의도 표현 | Low |

```dart
// 나쁜 예
final d = DateTime.now();
final t = transactions.where((x) => x.date == d);

// 좋은 예
final today = DateTime.now();
final todayTransactions = transactions.where(
  (transaction) => transaction.date == today,
);
```

### 4.2 문자열 규칙

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 따옴표 | 작은따옴표('') 사용 | Low |
| i18n | 하드코딩 텍스트 금지 | High |
| 문자열 보간 | $variable 또는 ${expr} | Low |

```dart
// 프로젝트 규칙: 작은따옴표 사용
final message = '저장되었습니다';  // 올바름
// final message = "저장되었습니다";  // 틀림

// i18n 필수
Text(l10n.saveSuccess),  // 올바름
// Text('저장되었습니다'),  // 틀림 (하드코딩)
```

### 4.3 주석

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 언어 | 한글 주석 사용 | Low |
| 이모티콘 | 이모티콘 사용 금지 | Low |
| 필요성 | 자명한 코드는 주석 없이 | Low |
| 문서화 | public API는 dartdoc | Medium |

```dart
// 올바른 주석
// 사용자가 dispose된 경우 작업을 중단한다
if (result == null) return;

// 틀린 주석 (이모티콘)
// 사용자 체크 완료!
```

### 4.4 코드 구조

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 함수 길이 | 50줄 이하 권장 | Medium |
| 클래스 길이 | 300줄 이하 권장 | Medium |
| 중첩 깊이 | 3단계 이하 권장 | Medium |
| 중복 코드 | DRY 원칙 준수 | High |

---

## 5. 엣지케이스 체크리스트

### 5.1 Null 안전

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| Null 체크 | 외부 데이터 null 처리 | Critical |
| 기본값 | ?? 연산자로 기본값 제공 | High |
| Optional | ?. 연산자 활용 | Medium |

```dart
// 외부 데이터는 항상 null 가능성 고려
final amount = json['amount'] as double? ?? 0.0;
final merchant = json['merchant'] as String? ?? '알 수 없음';

// 체이닝에서 null 안전
final categoryName = transaction?.category?.name ?? '미분류';
```

### 5.2 경계값

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 빈 컬렉션 | isEmpty 체크 | High |
| 0/음수 | 숫자 범위 검증 | High |
| 최대값 | int/double 오버플로우 | Medium |
| 날짜 범위 | 미래/과거 날짜 처리 | Medium |

```dart
// 빈 리스트 처리
if (transactions.isEmpty) {
  return EmptyStateWidget(message: l10n.noTransactions);
}

// 금액 검증
if (amount <= 0) {
  throw ValidationException('금액은 0보다 커야 합니다');
}
if (amount > 999999999) {
  throw ValidationException('금액이 너무 큽니다');
}
```

### 5.3 동시성

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| Race Condition | SafeNotifier 사용 | Critical |
| 중복 요청 | 로딩 플래그로 방지 | High |
| 순서 보장 | 비동기 작업 순서 | High |

```dart
// SafeNotifier로 Race Condition 방지
class TransactionNotifier extends SafeNotifier<List<Transaction>> {
  Future<void> loadTransactions() async {
    state = const AsyncValue.loading();
    try {
      final result = await safeAsync(
        () => repository.getTransactions(),
      );
      if (result == null) return;  // disposed 체크
      safeUpdateState(AsyncValue.data(result));
    } catch (e, st) {
      safeUpdateState(AsyncValue.error(e, st));
      rethrow;
    }
  }
}
```

### 5.4 네트워크

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 타임아웃 | 요청 타임아웃 설정 | High |
| 재시도 | 실패 시 재시도 로직 | Medium |
| 오프라인 | 네트워크 없을 때 처리 | Medium |

---

## 6. 보안 체크리스트

### 6.1 인증/인가

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 세션 검증 | 모든 요청에서 인증 확인 | Critical |
| 권한 검증 | RLS 정책 적용 | Critical |
| 토큰 관리 | 안전한 토큰 저장 | High |

```dart
// RLS 정책 예시 (Supabase)
// pending_transactions 테이블
CREATE POLICY "Users can view own pending transactions"
ON pending_transactions FOR SELECT
USING (
  payment_method_id IN (
    SELECT id FROM payment_methods
    WHERE owner_user_id = auth.uid()
  )
);
```

### 6.2 데이터 보호

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| 민감 정보 로깅 | 토큰/비밀번호 로깅 금지 | Critical |
| 입력 검증 | 사용자 입력 검증 | High |
| SQL Injection | 파라미터화된 쿼리 사용 | Critical |

```dart
// 민감 정보 로깅 금지
debugPrint('User logged in: ${user.id}');  // OK
// debugPrint('Token: $accessToken');  // 절대 금지!

// 입력 검증
String sanitizeInput(String input) {
  return input.trim().replaceAll(RegExp(r'[<>]'), '');
}
```

### 6.3 OWASP Top 10

| 항목 | 확인 내용 | 심각도 |
|------|----------|--------|
| Injection | SQL/NoSQL/Command Injection | Critical |
| XSS | 사용자 입력 표시 시 이스케이프 | High |
| CSRF | 상태 변경 요청 보호 | Medium |
| 암호화 | 민감 데이터 암호화 | High |

---

## 심각도별 조치 가이드

### Critical (즉시 수정)

- 배포 차단 사유
- 보안 취약점, 데이터 손실, 크래시 유발
- 코드 리뷰 통과 불가

### High (수정 권장)

- 배포 전 수정 권장
- 기능 오동작, 심각한 성능 문제
- 1일 이내 수정

### Medium (개선 권장)

- 다음 스프린트에서 개선
- 코드 품질, 유지보수성 문제
- 1주 이내 수정

### Low (선택적 수정)

- 팀 논의 후 결정
- 스타일, 문서화 등
- 시간 여유 있을 때 수정
