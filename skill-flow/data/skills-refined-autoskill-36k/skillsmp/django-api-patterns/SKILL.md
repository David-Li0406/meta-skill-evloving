---
name: django-api-patterns
description: Django REST Framework API 开发模式，包含视图、序列化器、路由和最佳实践。在创建或修改 Django API 时使用。
---

# Django REST Framework API 开发模式

## When to Use

- 创建新的 API 端点
- 修改现有 API
- 添加序列化器
- 配置 URL 路由
- 实现 API 认证和权限

## 核心模式

### 序列化器 (Serializers)

#### 基础序列化器
```python
from rest_framework import serializers
from .models import WorkOrder

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
```

#### 嵌套序列化器
```python
class WorkOrderDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    processes = WorkOrderProcessSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOrder
        fields = ['id', 'order_number', 'customer_name', 'processes', ...]
```

#### 自定义验证
```python
class WorkOrderSerializer(serializers.ModelSerializer):
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("数量必须大于0")
        return value

    def validate(self, attrs):
        if attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError("结束日期不能早于开始日期")
        return attrs
```

### 视图 (Views)

#### ModelViewSet
```python
from rest_framework import viewsets
from .models import WorkOrder
from .serializers import WorkOrderSerializer

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]
```

#### 自定义筛选
```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = WorkOrderFilter
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']
```

#### 自定义操作
```python
from rest_framework.decorators import action
from rest_framework.response import Response

class WorkOrderViewSet(viewsets.ModelViewSet):
    # ... 基础配置

    @action(detail=True, methods=['post'])
    def submit_approval(self, request, pk=None):
        workorder = self.get_object()
        workorder.status = 'pending_approval'
        workorder.save()
        return Response({'message': '已提交审核'})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        stats = {
            'total': WorkOrder.objects.count(),
            'pending': WorkOrder.objects.filter(status='pending').count()
        }
        return Response(stats)
```

### 权限 (Permissions)

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 读取权限允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限只给所有者
        return obj.created_by == request.user

class WorkOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

### 路由 (URLs)

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet

router = DefaultRouter()
router.register(r'workorders', WorkOrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## 最佳实践

### 1. 查询优化
```python
from rest_framework.decorators import action

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.select_related('customer').prefetch_related('processes')
```

### 2. 分页
```python
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class WorkOrderViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
```

### 3. 异常处理
```python
from rest_framework.exceptions import APIException
from rest_framework import status

class WorkOrderViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
```

### 4. API 响应格式
```python
from rest_framework.response import Response

class WorkOrderViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })
```

## 常见模式

### 软删除
```python
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
```

### 审计日志
```python
class WorkApprovalLog(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    comment = models.TextField(blank=True)
```

### 批量操作
```python
@action(detail=False, methods=['post'])
def batch_delete(self, request):
    ids = request.data.get('ids', [])
    count = WorkOrder.objects.filter(id__in=ids).delete()
    return Response({'deleted_count': count})
```

## 认证

### JWT 认证
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# views.py
from rest_framework.permissions import IsAuthenticated

class ProtectedView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

### 自定义认证
```python
from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken
```

## 测试

```python
from rest_framework.test import APITestCase
from django.urls import reverse

class WorkOrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_list_workorders(self):
        url = reverse('workorder-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

## 相关技能

- `vue-component-patterns` - 前端组件开发
- `systematic-debugging` - 调试 API 问题
- `testing-patterns` - 编写 API 测试
