# Code Review Checklist

## Security

### Injection Attacks
- SQL Injection: Raw query에 사용자 입력 직접 삽입
- Command Injection: Runtime.exec(), ProcessBuilder에 사용자 입력
- NoSQL Injection: MongoDB 쿼리에 `$where`, `$regex` 사용자 입력

### Authentication & Authorization
- 인증 없는 엔드포인트 노출
- 권한 검증 누락 (owner 체크, admin 체크)
- 하드코딩된 credentials
- JWT/Session 검증 우회 가능성

### Data Exposure
- 로그에 민감정보 출력 (password, token)
- 에러 메시지에 내부 정보 노출
- API 응답에 불필요한 필드 포함

## Performance

### Database
- N+1 쿼리: 루프 내 개별 조회
- 인덱스 미사용 쿼리
- 불필요한 전체 컬럼 조회 (SELECT *)
- 트랜잭션 범위 과도하게 넓음

### Memory
- 대용량 데이터 메모리 로드 (페이징 미적용)
- Stream 미사용으로 전체 컬렉션 메모리 유지
- 캐시 만료 정책 미설정

### Concurrency
- Race condition 가능성
- 데드락 위험
- Thread-safe하지 않은 공유 자원

## Code Quality

### Kotlin Specific
- `!!` (non-null assertion) 남용
- `lateinit` 초기화 보장 안됨
- data class의 copy() 오용
- sealed class exhaustive when 누락

### Spring Boot Specific
- `@Transactional` 누락 또는 잘못된 propagation
- `@Async` 반환값 미처리
- `@Cacheable` key 충돌 가능성
- Bean lifecycle 오해 (prototype in singleton)

### General
- 매직 넘버/스트링
- 중복 코드
- 과도한 중첩 (3단계 이상)
- 함수 길이 50줄 초과
- 파라미터 5개 초과

## Testing

- 새 기능에 대한 테스트 누락
- Edge case 테스트 부재
- Mock 설정 불완전
- 테스트 격리 안됨 (상태 공유)

## Project Conventions (reg-meta)

- `ApiResponse<T>` wrapper 사용
- `BusinessException(ErrorCode)` 패턴
- Service: Interface + Impl 분리
- Controller: `/internal/*` vs `/meta/*` 경로 구분
- DTO: request/response 패키지 분리
