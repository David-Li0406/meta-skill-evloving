---
name: api-pattern
description: ForkLore API 규칙을 검증하고 적용하는 스킬
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# API Pattern Skill

이 스킬은 ForkLore 프로젝트의 API 개발 규칙을 검증하고 적용합니다.

## 핵심 규칙

### 1. 응답 형식 - StandardJSONRenderer

**절대 규칙**: 뷰는 RAW 데이터만 반환합니다. `StandardJSONRenderer`가 자동으로 래핑합니다.

```python
# ✅ 올바른 방법
def retrieve(self, request, pk=None):
    novel = Novel.objects.filter(pk=pk).first()
    if not novel:
        raise NotFound("소설을 찾을 수 없습니다.")
    return Response(NovelSerializer(novel).data)

# ❌ 잘못된 방법 - 이중 래핑 발생
def retrieve(self, request, pk=None):
    novel = Novel.objects.filter(pk=pk).first()
    return Response({
        "success": True,
        "data": NovelSerializer(novel).data
    })
```

**출력 형식**:
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-01-16T12:00:00Z"
}
```

### 2. 예외 처리 - DRF 예외 사용

```python
from rest_framework.exceptions import (
    NotFound,           # 404
    PermissionDenied,   # 403
    ValidationError,    # 400
)

# 사용 예시
if not novel:
    raise NotFound("소설을 찾을 수 없습니다.")  # 한국어 메시지

if not request.user.can_edit(novel):
    raise PermissionDenied("수정 권한이 없습니다.")

if not data.get("title"):
    raise ValidationError({"title": "제목은 필수입니다."})
```

### 3. 서비스 패턴 - 비즈니스 로직 분리

```python
# apps/novels/services.py
class NovelService:
    @transaction.atomic
    def create(self, author: User, data: dict) -> Novel:
        """새 소설 생성.
        
        Args:
            author: 작성자
            data: 소설 데이터
        Returns:
            생성된 Novel 인스턴스
        Raises:
            ValidationError: 유효하지 않은 데이터
        """
        novel = Novel.objects.create(author=author, **data)
        Branch.objects.create(novel=novel, name="main", is_main=True)
        return novel

# apps/novels/views.py
class NovelViewSet(ModelViewSet):
    def create(self, request):
        serializer = NovelCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = NovelService()
        novel = service.create(request.user, serializer.validated_data)
        
        return Response(NovelSerializer(novel).data, status=201)
```

### 4. 시리얼라이저 규칙

```python
# Input 시리얼라이저 (생성/수정용)
class NovelCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    genre = serializers.ChoiceField(choices=Novel.GENRE_CHOICES)

# Output 시리얼라이저 (응답용)
class NovelSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.nickname')
    
    class Meta:
        model = Novel
        fields = ['id', 'title', 'genre', 'author_name', 'created_at']
```

### 5. URL 패턴

```python
# RESTful 규칙
/api/v1/novels/           # GET(목록), POST(생성)
/api/v1/novels/{id}/      # GET(상세), PUT(수정), DELETE(삭제)
/api/v1/novels/{id}/chapters/  # 중첩 리소스
```

## 검증 체크리스트

- [ ] 뷰가 RAW 데이터만 반환하는가?
- [ ] DRF 예외를 사용하는가?
- [ ] 비즈니스 로직이 서비스 레이어에 있는가?
- [ ] 에러 메시지가 한국어인가?
- [ ] 타입 힌트가 있는가?
- [ ] Docstring이 있는가?
