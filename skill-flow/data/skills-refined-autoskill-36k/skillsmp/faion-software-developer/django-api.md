# API Endpoints Reference (DRF)

## Thin Views Principle

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from apps.users import services as user_services
from . import serializers


class ItemActivationView(APIView):
    @extend_schema(
        summary="Activate item",
        description="Activates item for authenticated user",
        request=serializers.ItemActivationRequest,
        responses={200: serializers.ItemActivationResponse},
        tags=['Items'],
    )
    def post(self, request):
        # 1. Validate input
        serializer = serializers.ItemActivationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Call service (business logic)
        item = user_services.activate_user_item(
            user=request.user,
            item_code=serializer.validated_data['item_code'],
        )

        # 3. Return response
        response = serializers.ItemActivationResponse(item)
        return Response(response.data, status=status.HTTP_200_OK)
```

## OpenAPI Documentation (drf-spectacular)

```python
@extend_schema(
    summary="Short description (max 10 words)",     # Required
    description="Detailed description with rules",  # Required
    request=RequestSerializer,                      # Required for POST/PUT
    responses={200: ResponseSerializer},            # Required
    tags=['Category'],                              # Required
)
```

## ViewSet Pattern

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order_services.cancel_order(order)
        return Response({'status': 'cancelled'})
```

## Serializers

```python
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'uid', 'amount', 'status', 'created_at']
        read_only_fields = ['id', 'uid', 'created_at']


class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    item_id = serializers.IntegerField()

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value
```

## Error Responses

```python
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


class OrderLimitExceeded(APIException):
    status_code = 400
    default_detail = 'Daily order limit exceeded'
    default_code = 'order_limit_exceeded'
```
