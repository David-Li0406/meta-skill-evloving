---
name: swagger-annotation
description: Swagger/OpenAPI 어노테이션 작성 가이드. Java/Kotlin DTO 및 Controller에 @Schema, @Operation, @ApiResponses 어노테이션을 일관되게 작성할 때 사용. SpringDoc OpenAPI 기반 프로젝트에서 API 문서화 시 활용.
---

# Swagger Annotation Guide

## Core Principles

- All DTO fields require `@Schema`
- Descriptions in Korean, clear and concise
- Examples should match real usage
- Use together with Validation annotations

## Request DTO Pattern

```java
public record ProductUpdateRequest(
        @Schema(description = "상품 설명", example = "고품질 유기농 제품 (수정할 값만 보내주세요)")
        @Size(max = 100)
        String description,

        @Schema(description = "이미지 목록")
        @Valid
        @Size(min = 1, max = 5)
        List<ProductImageRequest> images,

        @Schema(description = "카테고리 ID 목록 (수정할 값만 보내주세요)")
        List<Long> categoryIds
) { }
```

## Response DTO Pattern

```java
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public record CommentResponse(
        @Schema(description = "댓글 ID", example = "1")
        long commentId,

        @JsonUnwrapped
        @Schema(implementation = UserProfileResponse.class)
        UserProfileResponse user,

        @Schema(description = "댓글 내용", example = "좋은 상품이네요!")
        String content,

        @Schema(description = "댓글 작성 시간", example = "2025-06-30T00:00:00")
        LocalDateTime createdAt
) { }
```

## @Schema Attributes

**Required:**
| Attribute | Condition | Description |
|-----------|-----------|-------------|
| description | Always | Field description (Korean) |
| example | Always | Example value similar to real usage |
| implementation | With @JsonUnwrapped | Class type to be unwrapped |

**Optional:** hidden, deprecated, nullable, defaultValue

## Examples by Type

```java
// String
@Schema(description = "상품 설명", example = "고품질 상품입니다")
String description;

// Long, Integer
@Schema(description = "상품 ID", example = "1")
long productId;

// Boolean
@Schema(description = "재고 있음 여부", example = "true")
boolean inStock;

// LocalDateTime
@Schema(description = "생성 시간", example = "2025-06-30T14:30:00")
LocalDateTime createdAt;

// LocalDate
@Schema(description = "생성 날짜", example = "2025-06-30")
LocalDate createdDate;

// Enum
@Schema(description = "상품 상태", example = "ACTIVE")
ProductStatus status;

// List<Long>
@Schema(description = "카테고리 ID 목록", example = "[1, 2, 3]")
List<Long> categoryIds;

// List<String>
@Schema(description = "태그 목록", example = "[\"신상품\", \"할인\"]")
List<String> tags;
```

## Controller Annotations

```java
@Operation(
    summary = "상품 수정",
    description = "상품의 설명, 이미지, 카테고리를 수정합니다. 수정할 필드만 전송하면 됩니다."
)
@ApiResponses({
    @ApiResponse(responseCode = "200", description = "수정 성공"),
    @ApiResponse(responseCode = "400", description = "잘못된 요청"),
    @ApiResponse(responseCode = "401", description = "인증 필요"),
    @ApiResponse(responseCode = "403", description = "수정 권한 없음"),
    @ApiResponse(responseCode = "404", description = "상품을 찾을 수 없음")
})
@PatchMapping("/{productId}")
public ApiResponse<ProductResponse> update(
        @Parameter(description = "상품 ID", example = "1")
        @PathVariable Long productId,

        @RequestBody @Valid ProductUpdateRequest request
) { ... }
```

## Paging Response Pattern

```java
public record PageResponse<T>(
        @Schema(description = "데이터 목록")
        List<T> content,
        
        @Schema(description = "현재 페이지 번호", example = "0")
        int pageNumber,
        
        @Schema(description = "페이지 크기", example = "20")
        int pageSize,
        
        @Schema(description = "전체 요소 수", example = "100")
        long totalElements,
        
        @Schema(description = "전체 페이지 수", example = "5")
        int totalPages,
        
        @Schema(description = "마지막 페이지 여부", example = "false")
        boolean last
) { }
```

## Common Mistakes

```java
// ❌ Missing description or example
@Schema(example = "1")
long productId;

// ❌ Meaningless example
@Schema(description = "사용자 이름", example = "test")
String userName;

// ❌ Missing implementation for @JsonUnwrapped
@JsonUnwrapped
@Schema
UserProfileResponse user;

// ✅ Correct usage
@Schema(description = "상품 ID", example = "1")
long productId;

@Schema(description = "사용자 이름", example = "홍길동")
String userName;

@JsonUnwrapped
@Schema(implementation = UserProfileResponse.class)
UserProfileResponse user;
```

## Checklist

**DTO:**
- [ ] All fields have @Schema(description, example)?
- [ ] implementation specified when using @JsonUnwrapped?

**Controller:**
- [ ] @Operation(summary, description) present?
- [ ] All response codes documented with @ApiResponses?
- [ ] PathVariable and RequestParam described with @Parameter?
