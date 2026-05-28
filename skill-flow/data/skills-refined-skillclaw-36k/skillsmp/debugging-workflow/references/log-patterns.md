# 로그 패턴 사전

디버깅에 사용되는 표준 로그 패턴입니다.

---

## 태그 규칙

| 태그 | 용도 | 예시 |
|------|------|------|
| `[ENTRY]` | 함수 진입점 | 입력 파라미터 |
| `[STATE]` | 중간 상태 | 현재 상태, 변수값 |
| `[RESULT]` | 함수 출력 | 반환값, 결과 |
| `[ERROR]` | 에러 발생 | 예외, 실패 |
| `[WARN]` | 경고 상황 | 비정상 but 계속 |
| `[DEBUG]` | 상세 정보 | 디버깅용 |

---

## Python 패턴

### 기본 설정

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    filename='D:/AI/claude01/logs/debug_output.log'
)

logger = logging.getLogger(__name__)
```

### 함수 로깅

```python
def process_data(data: dict) -> dict:
    logger.debug(f"[ENTRY] process_data: data={data}")

    try:
        logger.debug(f"[STATE] processing step 1")
        result = transform(data)

        logger.debug(f"[STATE] processing step 2")
        validated = validate(result)

        logger.debug(f"[RESULT] process_data: result={validated}")
        return validated

    except Exception as e:
        logger.error(f"[ERROR] process_data failed: {e}", exc_info=True)
        raise
```

### 조건 분기

```python
if condition:
    logger.debug(f"[STATE] branch: condition=True, taking path A")
else:
    logger.debug(f"[STATE] branch: condition=False, taking path B")
```

---

## TypeScript 패턴

### 기본 설정

```typescript
const DEBUG = true;
const LOG_FILE = 'D:/AI/claude01/logs/debug_output.log';

const debugLog = (tag: string, msg: string, data?: any) => {
    if (!DEBUG) return;

    const timestamp = new Date().toISOString();
    const logLine = `${timestamp} [${tag}] ${msg} ${data ? JSON.stringify(data) : ''}`;

    console.log(logLine);

    // 파일 로깅 (Node.js)
    if (typeof require !== 'undefined') {
        const fs = require('fs');
        fs.appendFileSync(LOG_FILE, logLine + '\n');
    }
};
```

### 함수 로깅

```typescript
async function fetchUserData(userId: string): Promise<User> {
    debugLog('ENTRY', 'fetchUserData', { userId });

    try {
        debugLog('STATE', 'calling API');
        const response = await api.get(`/users/${userId}`);

        debugLog('STATE', 'parsing response', { status: response.status });
        const user = response.data;

        debugLog('RESULT', 'fetchUserData', { user });
        return user;

    } catch (error) {
        debugLog('ERROR', 'fetchUserData failed', { error: error.message });
        throw error;
    }
}
```

---

## 분석 명령어

```powershell
# 에러만 필터링
Get-Content debug_output.log | Select-String "ERROR"

# 특정 함수 추적
Get-Content debug_output.log | Select-String "process_data"

# ENTRY/RESULT 페어 확인
Get-Content debug_output.log | Select-String "ENTRY|RESULT"

# 타임라인 분석 (최근 100줄)
Get-Content debug_output.log -Tail 100

# 시간대별 에러 빈도
Get-Content debug_output.log | Select-String "ERROR" |
    ForEach-Object { $_.Line.Substring(0, 19) } |
    Group-Object | Sort-Object Count -Descending
```

---

## 로그 저장 위치

```
D:\AI\claude01\logs\
├── debug_<issue-number>_<timestamp>.log  # 이슈별 로그
├── debug_output.log                       # 현재 세션 로그
└── archive\                               # 보관 로그
```

---

## Anti-Patterns

| 금지 | 이유 | 개선 |
|------|------|------|
| `print(data)` | 구조화 안 됨 | `logger.debug(f"[TAG] {data}")` |
| `console.log(x)` | 태그 없음 | `debugLog('TAG', 'msg', x)` |
| 민감정보 로깅 | 보안 위험 | 마스킹 처리 |
| 반복문 내 로깅 | 로그 폭발 | 샘플링 또는 요약 |
