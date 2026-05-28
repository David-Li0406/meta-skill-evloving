# Output Format Reference

> load-context Skill 출력 형식 가이드

## 기본 출력 템플릿

```markdown
[SEMO] Skill: load-context 호출 - {domain}

## 📋 컨텍스트 요약: {Domain}

### 📄 Spec 상태
| 파일 | 상태 | 요약 |
|------|------|------|
| spec.md | ✅ | {one_line_summary} |
| plan.md | ✅ | {tech_stack_summary} |
| tasks.md | ⚠️ | 3/7 완료 |

### 📁 코드 구조
```text
domain/posts/
├── entity/Post.kt              # 8 fields (id, title, content, ...)
├── repository/PostRepository.kt # 3 custom methods
├── service/
│   ├── PostCommandService.kt   # create, update, delete
│   └── PostQueryService.kt     # findById, findAll, search
├── web/PostController.kt       # 5 endpoints
└── exception/PostException.kt  # NotFound, AlreadyExists
```

### 🔄 최근 변경
| 날짜 | 커밋 | 내용 |
|------|------|------|
| 12/03 | a1b2c3d | ✨ Add pagination to post list |
| 12/02 | e4f5g6h | 🐛 Fix null pointer in getPost |
| 12/01 | i7j8k9l | 📝 Update post spec |

### 🎫 관련 이슈
- #123: 게시글 페이지네이션 구현 (closed)
- #145: 게시글 검색 기능 추가 (open)
- #156: 게시글 캐싱 적용 (open)

### 📊 테스트 현황
- 테스트 파일: 4개
- 테스트 메서드: 23개
- 커버리지 추정: ~70%

### 🔗 연관 도메인
- `user` (작성자 참조)
- `comment` (댓글 연관)
- `category` (카테고리 분류)

---

**다음 작업 제안**:
1. #145 이슈 구현을 위해 `spec-master` 호출
2. 검색 기능 spec 보완 필요
```

---

## 상황별 출력 변형

### Spec이 없는 경우

```markdown
### 📄 Spec 상태
| 파일 | 상태 |
|------|------|
| spec.md | ❌ 없음 |
| plan.md | ❌ 없음 |
| tasks.md | ❌ 없음 |

⚠️ **SDD 미완료**: 명세 작성이 필요합니다.

**권장 조치**: `/speckit.specify {domain}` 실행
```

### 코드가 없는 경우

```markdown
### 📁 코드 구조
❌ `domain/{domain}/` 디렉토리가 존재하지 않습니다.

**현재 상태**: Spec만 존재, 구현 전

**권장 조치**: `skill:scaffold-domain {domain}` 실행
```

### Git 이력이 없는 경우

```markdown
### 🔄 최근 변경
ℹ️ 아직 커밋된 변경이 없습니다. (새 도메인)
```

---

## 옵션별 출력

### --deep 모드

```markdown
[SEMO] Skill: load-context 호출 - {domain} (상세 모드)

## 📋 상세 컨텍스트: {Domain}

### 📄 Spec 전문

#### spec.md
```markdown
# {Domain} Feature Specification
...전체 내용...
```

#### plan.md
```markdown
# {Domain} Implementation Plan
...전체 내용...
```

### 📁 주요 코드

#### Entity
```kotlin
@Table("posts")
data class Post(
    @Id val id: UUID? = null,
    val title: String,
    val content: String,
    val authorId: UUID,
    val status: String = PostStatus.DRAFT,
    val viewCount: Long = 0,
    val createdAt: Instant = Instant.now(),
    val updatedAt: Instant? = null
)
```

#### Service Methods
```kotlin
// PostCommandService.kt
suspend fun create(request: CreatePostRequest): Post
suspend fun update(id: UUID, request: UpdatePostRequest): Post
suspend fun delete(id: UUID)
suspend fun publish(id: UUID): Post

// PostQueryService.kt
suspend fun findById(id: UUID): Post?
fun findAll(): Flow<Post>
fun findByStatus(status: String): Flow<Post>
suspend fun search(query: String): List<Post>
```

### 🔄 변경 이력 상세
...더 많은 커밋 + diff...
```

### --spec-only 모드

```markdown
[SEMO] Skill: load-context 호출 - {domain} (Spec 전용)

## 📄 Spec Documents: {Domain}

### spec.md
{full_content}

### plan.md
{full_content}

### tasks.md
{full_content}
```

### --code-only 모드

```markdown
[SEMO] Skill: load-context 호출 - {domain} (코드 전용)

## 📁 코드 구조: {Domain}

### 파일 목록
{file_tree}

### Entity 구조
{entity_fields}

### Service 메서드
{service_methods}

### Controller 엔드포인트
{endpoints}
```

---

## 에러 출력

### 도메인을 찾을 수 없는 경우

```markdown
[SEMO] Skill: load-context 호출 - {domain}

❌ **도메인을 찾을 수 없습니다**: `{domain}`

**확인된 경로**:
- specs/{domain}/: ❌
- domain/{domain}/: ❌

**존재하는 도메인 목록**:
- posts
- users
- comments

**도움말**: 정확한 도메인명을 입력하거나, 새 도메인 생성 시 `skill:scaffold-domain {domain}` 사용
```

### 부분적으로만 존재하는 경우

```markdown
[SEMO] Skill: load-context 호출 - {domain}

⚠️ **부분 컨텍스트**: `{domain}`

| 소스 | 상태 |
|------|------|
| specs/ | ✅ 존재 |
| domain/ | ❌ 없음 |

**현재 상태**: Spec 완료, 구현 대기

**권장 조치**: `skill:implement {domain}` 실행
```
