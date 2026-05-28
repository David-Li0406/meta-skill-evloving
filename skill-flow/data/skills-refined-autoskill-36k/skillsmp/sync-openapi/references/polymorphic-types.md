# Polymorphic Types Reference

## Discriminator Pattern

OpenAPI에서 polymorphic 타입 정의 시:

```yaml
components:
  schemas:
    ContentResponse:
      oneOf:
        - $ref: '#/components/schemas/PostResponse'
        - $ref: '#/components/schemas/CommentResponse'
      discriminator:
        propertyName: type
        mapping:
          post: '#/components/schemas/PostResponse'
          comment: '#/components/schemas/CommentResponse'
```

## Kotlin Implementation

```kotlin
@JsonTypeInfo(
    use = JsonTypeInfo.Id.NAME,
    include = JsonTypeInfo.As.PROPERTY,
    property = "type"
)
@JsonSubTypes(
    JsonSubTypes.Type(value = PostResponse::class, name = "post"),
    JsonSubTypes.Type(value = CommentResponse::class, name = "comment")
)
sealed class ContentResponse

data class PostResponse(
    val id: UUID,
    val title: String,
    val content: String
) : ContentResponse()

data class CommentResponse(
    val id: UUID,
    val postId: UUID,
    val content: String
) : ContentResponse()
```

## Usage in Controller

```kotlin
@GetMapping("/contents/{id}")
suspend fun getContent(
    @PathVariable id: UUID
): ApiResponse.Success<ContentResponse> {
    val content = contentService.findById(id)
    return ApiResponse.Success(data = content)
}
```
