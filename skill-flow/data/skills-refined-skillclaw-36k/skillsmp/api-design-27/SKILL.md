---
name: api-design
description: RESTful API 설계 시 따라야 할 원칙과 베스트 프랙티스를 정의합니다
license: MIT
compatibility: opencode
metadata:
  category: architecture
  type: rest-api
---

# API 설계 가이드라인

RESTful API를 설계할 때 다음 원칙과 패턴을 따릅니다.

## 1. URL 설계 원칙

### 리소스 중심
```
# Good - 명사 사용
GET /users
GET /users/123
GET /users/123/orders

# Bad - 동사 사용
GET /getUsers
GET /getUserById/123
POST /createUser
```

### 복수형 사용
```
# Good
GET /users
GET /products
GET /orders

# Bad
GET /user
GET /product
```

### 계층 구조
```
# 리소스 간 관계 표현
GET /users/123/orders          # 특정 사용자의 주문 목록
GET /users/123/orders/456      # 특정 사용자의 특정 주문
POST /users/123/orders         # 특정 사용자에게 주문 생성
```

## 2. HTTP 메서드

| 메서드 | 용도 | 멱등성 | 안전성 |
|-------|------|-------|-------|
| GET | 리소스 조회 | ✅ | ✅ |
| POST | 리소스 생성 | ❌ | ❌ |
| PUT | 리소스 전체 수정 | ✅ | ❌ |
| PATCH | 리소스 부분 수정 | ❌ | ❌ |
| DELETE | 리소스 삭제 | ✅ | ❌ |

### 사용 예시
```
GET    /users          # 목록 조회
GET    /users/123      # 단일 조회
POST   /users          # 생성
PUT    /users/123      # 전체 수정
PATCH  /users/123      # 부분 수정
DELETE /users/123      # 삭제
```

## 3. HTTP 상태 코드

### 성공 (2xx)
| 코드 | 의미 | 사용 상황 |
|-----|------|---------|
| 200 | OK | 일반적인 성공 |
| 201 | Created | 리소스 생성 성공 |
| 204 | No Content | 성공, 반환 데이터 없음 (DELETE) |

### 클라이언트 에러 (4xx)
| 코드 | 의미 | 사용 상황 |
|-----|------|---------|
| 400 | Bad Request | 잘못된 요청 형식 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 권한 없음 |
| 404 | Not Found | 리소스 없음 |
| 409 | Conflict | 충돌 (중복 등) |
| 422 | Unprocessable Entity | 유효성 검증 실패 |

### 서버 에러 (5xx)
| 코드 | 의미 | 사용 상황 |
|-----|------|---------|
| 500 | Internal Server Error | 서버 내부 에러 |
| 503 | Service Unavailable | 서비스 일시 중단 |

## 4. 요청/응답 형식

### 요청 본문
```json
POST /users
Content-Type: application/json

{
  "name": "홍길동",
  "email": "hong@example.com"
}
```

### 성공 응답
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "123",
  "name": "홍길동",
  "email": "hong@example.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### 에러 응답
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "유효성 검증에 실패했습니다",
    "details": [
      {
        "field": "email",
        "message": "올바른 이메일 형식이 아닙니다"
      }
    ]
  }
}
```

## 5. 페이지네이션

### 쿼리 파라미터
```
GET /users?page=1&limit=20
GET /users?offset=0&limit=20
GET /users?cursor=abc123&limit=20
```

### 응답 형식
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

## 6. 필터링 및 정렬

### 필터링
```
GET /users?status=active
GET /users?role=admin&status=active
GET /products?minPrice=1000&maxPrice=5000
```

### 정렬
```
GET /users?sort=createdAt:desc
GET /users?sort=name:asc,createdAt:desc
```

### 필드 선택
```
GET /users?fields=id,name,email
```

## 7. 버전 관리

### URL 버전
```
GET /v1/users
GET /v2/users
```

### 헤더 버전
```
GET /users
Accept: application/vnd.api+json;version=1
```

## 8. 보안 체크리스트

- [ ] HTTPS 사용
- [ ] 인증 (JWT, OAuth)
- [ ] 입력값 검증
- [ ] Rate Limiting
- [ ] CORS 설정
- [ ] 민감 정보 로깅 금지
