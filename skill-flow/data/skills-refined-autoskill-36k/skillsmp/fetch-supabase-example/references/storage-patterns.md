# Storage Patterns

세미콜론 커뮤니티 솔루션은 두 개의 Storage 버킷을 운용합니다.

## Bucket Configuration

| 버킷 | 용도 | 기본값 |
|------|------|--------|
| `public-bucket` | 공개 파일 (사용자 업로드) | ✅ 기본값 |
| `private-bucket` | 비공개 파일 (민감/관리자용) | - |

## Upload Patterns

### 프로필 이미지 업로드 (공개)

```typescript
async uploadAvatar(userId: string, file: File): Promise<string> {
  const filename = `${Date.now()}-${file.name}`;
  const path = `avatars/${userId}/${filename}`;

  const { data, error } = await supabase.storage
    .from('public-bucket')
    .upload(path, file, {
      cacheControl: '3600',
      upsert: true
    });

  if (error) throw new Error(`Avatar upload failed: ${error.message}`);
  return data.path;
}
```

### 게시물 첨부파일 업로드 (공개)

```typescript
async uploadPostAttachment(postId: string, file: File): Promise<string> {
  const filename = `${Date.now()}-${file.name}`;
  const path = `posts/${postId}/${filename}`;

  const { data, error } = await supabase.storage
    .from('public-bucket')
    .upload(path, file);

  if (error) throw new Error(`Attachment upload failed: ${error.message}`);
  return data.path;
}
```

### 비공개 문서 업로드 (관리자용)

```typescript
async uploadPrivateDocument(userId: string, file: File): Promise<string> {
  const filename = `${Date.now()}-${file.name}`;
  const path = `documents/${userId}/${filename}`;

  const { data, error } = await supabase.storage
    .from('private-bucket')
    .upload(path, file);

  if (error) throw new Error(`Document upload failed: ${error.message}`);
  return data.path;
}
```

## Download/URL Patterns

### 공개 파일 URL 가져오기

```typescript
function getPublicUrl(path: string): string {
  const { data } = supabase.storage.from("public-bucket").getPublicUrl(path);
  return data.publicUrl;
}
```

### 비공개 파일 서명된 URL 가져오기

```typescript
async function getSignedUrl(path: string, expiresIn = 3600): Promise<string> {
  const { data, error } = await supabase.storage
    .from("private-bucket")
    .createSignedUrl(path, expiresIn);

  if (error) throw new Error(`Signed URL creation failed: ${error.message}`);
  return data.signedUrl;
}
```

## Path Convention

| 파일 유형 | 버킷 | 경로 패턴 |
|-----------|------|-----------|
| 프로필 이미지 | `public-bucket` | `avatars/{userId}/{filename}` |
| 게시물 첨부 | `public-bucket` | `posts/{postId}/{filename}` |
| 썸네일 | `public-bucket` | `thumbnails/{resourceId}/{filename}` |
| 민감한 문서 | `private-bucket` | `documents/{userId}/{filename}` |
| 관리자 자료 | `private-bucket` | `admin/{category}/{filename}` |

## Storage Rules

1. **버킷 명시 필수**: 모든 업로드에 버킷 이름 명시
2. **기본값 public-bucket**: 특별한 이유 없으면 `public-bucket` 사용
3. **경로 규칙 준수**: `{type}/{ownerId}/{filename}` 패턴
4. **파일명 유니크**: timestamp 또는 UUID 포함 권장
