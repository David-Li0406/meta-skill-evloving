# DTO Patterns Reference

## Naming Convention

| Operation | Request | Response |
|-----------|---------|----------|
| create{Entity} | Create{Entity}Request | Create{Entity}Response |
| get{Entity} | - | Get{Entity}Response |
| update{Entity} | Update{Entity}Request | Update{Entity}Response |
| delete{Entity} | - | - |
| list{Entity}s | - | Paged{Entity}sResponse |

## Request DTO

```kotlin
data class CreatePostRequest(
    @field:NotBlank
    val title: String,

    @field:NotBlank
    @field:Size(min = 10)
    val content: String
)

data class UpdatePostRequest(
    val title: String? = null,
    val content: String? = null
)
```

## Response DTO

```kotlin
data class PostResponse(
    val id: UUID,
    val title: String,
    val content: String,
    val status: String,
    val authorId: UUID,
    val createdAt: Instant,
    val updatedAt: Instant?
)

// Paged response
data class PagedPostsResponse(
    val posts: List<PostResponse>,
    val pagination: Pagination
)

data class Pagination(
    val page: Int,
    val size: Int,
    val totalElements: Long,
    val totalPages: Int
)
```

## Entity → Response 변환

```kotlin
fun Post.toResponse() = PostResponse(
    id = id!!,
    title = title,
    content = content,
    status = status,
    authorId = authorId,
    createdAt = createdAt,
    updatedAt = updatedAt
)
```
