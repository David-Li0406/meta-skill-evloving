# Full Code Review Checklist

프로젝트 전체 검수를 위한 통합 체크리스트입니다.
주요 기능 개발 후, 배포 전에 이 체크리스트를 사용하세요.

## Quick Reference

```bash
# 빠른 검수 (5분)
ruby .claude/skills/code-review/scripts/full_review.rb --quick

# 표준 검수 (15분)
ruby .claude/skills/code-review/scripts/full_review.rb

# 심층 검수 (30분)
ruby .claude/skills/code-review/scripts/full_review.rb --deep
```

---

## 1. Database Layer (데이터베이스)

### Migration Status
- [ ] `rails db:migrate:status` - 모든 마이그레이션 적용됨
- [ ] 롤백 가능한 마이그레이션 작성됨
- [ ] 대용량 테이블 변경 시 `disable_ddl_transaction!` 사용

### Schema Consistency
- [ ] `db/schema.rb`가 최신 상태
- [ ] 외래키 컬럼에 인덱스 있음
- [ ] unique 제약조건에 인덱스 있음

### Data Integrity
- [ ] 고아 레코드 없음
- [ ] Counter cache 정확함
- [ ] Enum 값 일관성

### Performance Indexes
- [ ] 자주 검색되는 컬럼에 인덱스
- [ ] 복합 쿼리용 복합 인덱스
- [ ] 불필요한 인덱스 없음

---

## 2. Model Layer (모델)

### Associations
- [ ] belongs_to 정의 완료
- [ ] has_many에 dependent 옵션 있음
- [ ] polymorphic 관계 올바르게 설정

### Validations
- [ ] 필수 필드에 presence 검증
- [ ] unique 필드에 uniqueness 검증 (+ DB 인덱스)
- [ ] format 검증 (이메일, 전화번호 등)
- [ ] length 검증 (최소/최대)

### Callbacks
- [ ] callback 복잡도 적절함 (5개 이하)
- [ ] 외부 API 호출은 background job으로 분리
- [ ] after_commit 적절히 활용

### Scopes & Enums
- [ ] 자주 사용하는 쿼리에 scope 정의
- [ ] enum 정의 및 i18n 연동

### Security
- [ ] 민감 정보 filter_attributes 설정
- [ ] attr_accessor 보안 확인

---

## 3. Controller Layer (컨트롤러)

### Strong Parameters
- [ ] 모든 create/update에 *_params 메서드 사용
- [ ] 민감 필드 (admin, role 등) 허용 안 함
- [ ] 중첩 속성 올바르게 허용

### Authentication
- [ ] before_action :require_login 적용
- [ ] skip_before_action 최소화
- [ ] 리소스 소유권 확인

### Authorization
- [ ] 수정/삭제 시 권한 확인
- [ ] 관리자 기능 접근 제어

### N+1 Prevention
- [ ] includes/preload/eager_load 사용
- [ ] 뷰에서 추가 쿼리 발생 안 함

### Response Handling
- [ ] 적절한 HTTP 상태 코드
- [ ] Turbo Stream 응답 지원
- [ ] 에러 메시지 사용자 친화적

### Error Handling
- [ ] rescue_from 전역 처리
- [ ] 예외 로깅 설정

---

## 4. View Layer (뷰)

### Security
- [ ] raw/html_safe 사용 시 sanitize 적용
- [ ] 사용자 입력 자동 이스케이핑 확인

### Performance
- [ ] 반복문에서 N+1 없음
- [ ] 복잡한 로직은 helper/presenter로 분리
- [ ] 이미지 최적화 (lazy loading)

### Accessibility
- [ ] alt 태그 설정
- [ ] label과 input 연결
- [ ] 키보드 네비게이션 가능

### Turbo/Stimulus
- [ ] Turbo Frame 적절히 사용
- [ ] Stimulus controller 연결 확인
- [ ] data-turbo-method 설정

---

## 5. Security (보안)

### OWASP Top 10

#### SQL Injection
- [ ] 파라미터화된 쿼리 사용
- [ ] where 절에 문자열 보간 없음

#### XSS
- [ ] 사용자 입력 이스케이핑
- [ ] CSP 헤더 설정

#### CSRF
- [ ] protect_from_forgery 활성화
- [ ] 폼에 authenticity_token 포함

#### Authentication
- [ ] 비밀번호 최소 길이 8자
- [ ] has_secure_password 사용
- [ ] 세션 타임아웃 설정

#### Authorization
- [ ] 모든 액션에 권한 확인
- [ ] IDOR 취약점 없음

### Dependency Security
- [ ] `bundle audit check` 통과
- [ ] 취약한 gem 업데이트

### Secrets Management
- [ ] .env 파일 .gitignore에 포함
- [ ] API 키/비밀번호 하드코딩 없음
- [ ] Rails credentials 활용

---

## 6. Performance (성능)

### Database
- [ ] N+1 쿼리 없음 (Bullet 확인)
- [ ] 느린 쿼리 없음 (100ms 이하)
- [ ] Counter cache 활용

### Caching
- [ ] Fragment caching 적용
- [ ] HTTP 캐시 헤더 설정
- [ ] Redis/Memcached 설정 (프로덕션)

### Assets
- [ ] 이미지 최적화
- [ ] CSS/JS 압축 (프로덕션)
- [ ] CDN 설정 (프로덕션)

### Background Jobs
- [ ] 긴 작업 background job으로 분리
- [ ] 이메일 전송 async
- [ ] 외부 API 호출 async

---

## 7. Testing (테스트)

### Coverage
- [ ] Model 테스트 90%+
- [ ] Controller 테스트 80%+
- [ ] Integration 테스트 주요 흐름

### Quality
- [ ] 테스트 독립적 (순서 무관)
- [ ] Fixture/Factory 적절히 사용
- [ ] Edge case 커버

### CI/CD
- [ ] 모든 테스트 통과
- [ ] Rubocop 통과
- [ ] Brakeman 통과

---

## 8. Code Quality (코드 품질)

### DRY
- [ ] 중복 코드 없음
- [ ] Concern/Module 활용
- [ ] Partial 재사용

### Complexity
- [ ] 메서드 20줄 이하
- [ ] 클래스 200줄 이하
- [ ] 조건문 3단계 이하

### Naming
- [ ] 명확한 변수명
- [ ] 일관된 메서드 네이밍
- [ ] 영어 사용 (코드)

### Documentation
- [ ] 복잡한 로직 주석
- [ ] API 문서화
- [ ] README 업데이트

---

## 9. Architecture (아키텍처)

### Routes
- [ ] RESTful 패턴 준수
- [ ] 불필요한 커스텀 라우트 없음
- [ ] namespace 적절히 사용

### File Structure
- [ ] Rails 컨벤션 준수
- [ ] Service/Query Object 분리 (필요 시)
- [ ] Concern 적절히 활용

### JavaScript
- [ ] Stimulus controller 연결
- [ ] Import maps 정리
- [ ] 불필요한 JS 없음

---

## 10. Production Readiness (배포 준비)

### Configuration
- [ ] 환경별 설정 분리
- [ ] 시크릿 관리
- [ ] 로깅 설정

### Monitoring
- [ ] 에러 트래킹 (Sentry 등)
- [ ] 성능 모니터링 (APM)
- [ ] 로그 수집

### Backup
- [ ] 데이터베이스 백업 설정
- [ ] 복구 테스트 완료

### Deployment
- [ ] 무중단 배포 설정
- [ ] 롤백 절차 문서화
- [ ] 헬스 체크 엔드포인트

---

## Review Summary Template

```markdown
# Code Review Report

**Date**: YYYY-MM-DD
**Reviewer**:
**Branch/PR**:

## Summary
- Total Issues: X
- Critical: X | High: X | Medium: X | Low: X

## Critical Issues
1. ...

## High Priority Issues
1. ...

## Recommendations
1. ...

## Tests
- [ ] All tests passing
- [ ] Coverage acceptable

## Approved: [ ] Yes [ ] No

## Notes
...
```

---

## Automation Commands

```bash
# 전체 검수 실행
ruby .claude/skills/code-review/scripts/full_review.rb

# 개별 검수
ruby .claude/skills/code-review/scripts/full_review.rb --database
ruby .claude/skills/code-review/scripts/full_review.rb --models
ruby .claude/skills/code-review/scripts/full_review.rb --controllers
ruby .claude/skills/code-review/scripts/full_review.rb --security
ruby .claude/skills/code-review/scripts/full_review.rb --performance

# 기존 스킬 활용
ruby .claude/skills/database-maintenance/scripts/health_check.rb
ruby .claude/skills/security-audit/scripts/security_audit.rb
ruby .claude/skills/performance-check/scripts/performance_check.rb

# 테스트 실행
SKIP_ASSET_BUILD=true rails test

# 보안 스캔
bundle exec brakeman
bundle exec bundler-audit check
```
