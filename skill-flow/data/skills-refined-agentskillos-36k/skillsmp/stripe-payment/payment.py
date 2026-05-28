"""Stripe Payment - Stripe 支付集成.

提供 Checkout Session、订阅管理、Webhook 处理等功能。
"""

import logging
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from pydantic import BaseModel, Field

from agentflow.skills.builtin.stripe_payment.exceptions import (
    CustomerError,
    PaymentError,
    RefundError,
    SignatureVerificationError,
    SubscriptionError,
    WebhookError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 配置模型
# ============================================================================


class StripeConfig(BaseModel):
    """Stripe 配置."""

    secret_key: str = Field(..., description="Stripe 密钥 (sk_test_... 或 sk_live_...)")
    webhook_secret: str | None = Field(default=None, description="Webhook 签名密钥")
    success_url: str = Field(
        default="https://example.com/success", description="支付成功后的跳转 URL"
    )
    cancel_url: str = Field(
        default="https://example.com/cancel", description="支付取消后的跳转 URL"
    )
    test_mode: bool = Field(default=False, description="测试模式")


# ============================================================================
# 主类
# ============================================================================


class StripePayment:
    """Stripe 支付集成.

    提供完整的 Stripe 支付功能：
    - Checkout Session（托管结账）
    - 订阅管理
    - Webhook 处理（带幂等性）
    - Customer Portal
    - 退款处理

    使用示例:
        ```python
        config = StripeConfig(
            secret_key="sk_test_...",
            webhook_secret="whsec_...",
        )
        stripe = StripePayment(config)

        # 创建结账会话
        session = await stripe.create_checkout_session(
            customer_email="test@example.com",
            line_items=[{"price": "price_xxx", "quantity": 1}],
            mode="subscription",
        )
        print(session.url)
        ```
    """

    def __init__(self, config: StripeConfig) -> None:
        """初始化 Stripe Payment.

        Args:
            config: Stripe 配置
        """
        self._config = config
        self._stripe: Any = None
        self._processed_events: set[str] = set()  # 内存幂等性存储

        self._initialize()

    def _initialize(self) -> None:
        """初始化 Stripe 客户端."""
        try:
            import stripe
        except ImportError:
            raise ImportError("stripe 库未安装，请运行: pip install stripe")

        stripe.api_key = self._config.secret_key
        self._stripe = stripe
        logger.info(
            f"Stripe 已初始化 ({'测试模式' if self._config.test_mode else '生产模式'})"
        )

    # ========================================================================
    # Checkout Session
    # ========================================================================

    async def create_checkout_session(
        self,
        line_items: list[dict[str, Any]],
        mode: str = "payment",
        customer_email: str | None = None,
        customer_id: str | None = None,
        metadata: dict[str, str] | None = None,
        success_url: str | None = None,
        cancel_url: str | None = None,
        trial_period_days: int | None = None,
        allow_promotion_codes: bool = False,
    ) -> Any:
        """创建 Checkout Session.

        Args:
            line_items: 购买项目列表
            mode: 模式（payment/subscription/setup）
            customer_email: 客户邮箱
            customer_id: 已有客户 ID
            metadata: 自定义元数据
            success_url: 成功跳转 URL
            cancel_url: 取消跳转 URL
            trial_period_days: 试用期天数（仅订阅）
            allow_promotion_codes: 允许促销码

        Returns:
            Checkout Session 对象
        """
        try:
            params: dict[str, Any] = {
                "line_items": line_items,
                "mode": mode,
                "success_url": success_url or self._config.success_url,
                "cancel_url": cancel_url or self._config.cancel_url,
            }

            if customer_email:
                params["customer_email"] = customer_email
            if customer_id:
                params["customer"] = customer_id
            if metadata:
                params["metadata"] = metadata
            if allow_promotion_codes:
                params["allow_promotion_codes"] = True

            # 订阅模式特有参数
            if mode == "subscription":
                subscription_data: dict[str, Any] = {}
                if trial_period_days:
                    subscription_data["trial_period_days"] = trial_period_days
                if metadata:
                    subscription_data["metadata"] = metadata
                if subscription_data:
                    params["subscription_data"] = subscription_data

            session = self._stripe.checkout.Session.create(**params)
            logger.info(f"已创建 Checkout Session: {session.id}")
            return session

        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    # ========================================================================
    # Customer Portal
    # ========================================================================

    async def create_portal_session(
        self,
        customer_id: str,
        return_url: str,
    ) -> str:
        """创建 Customer Portal 会话.

        Args:
            customer_id: 客户 ID
            return_url: 返回 URL

        Returns:
            Portal URL
        """
        try:
            session = self._stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            return session.url
        except self._stripe.error.StripeError as e:
            raise CustomerError(str(e), getattr(e, "code", None))

    # ========================================================================
    # Webhook 处理
    # ========================================================================

    def verify_webhook(
        self,
        payload: bytes,
        signature: str,
    ) -> Any:
        """验证 Webhook 签名.

        Args:
            payload: 请求体
            signature: Stripe-Signature 头

        Returns:
            验证后的事件对象
        """
        if not self._config.webhook_secret:
            raise WebhookError("未配置 webhook_secret")

        try:
            event = self._stripe.Webhook.construct_event(
                payload,
                signature,
                self._config.webhook_secret,
            )
            return event
        except self._stripe.error.SignatureVerificationError as e:
            raise SignatureVerificationError(str(e))
        except ValueError as e:
            raise WebhookError(f"无效的 payload: {e}")

    async def handle_webhook_event(
        self,
        event: Any,
        handlers: dict[str, Callable],
        idempotency_store: Any | None = None,
    ) -> bool:
        """处理 Webhook 事件（带幂等性）.

        Args:
            event: Stripe 事件对象
            handlers: 事件处理器映射 {"event_type": handler_func}
            idempotency_store: 幂等性存储（数据库管理器）

        Returns:
            是否处理成功
        """
        event_id = event.id
        event_type = event.type

        # 幂等性检查
        if idempotency_store:
            # 使用数据库存储
            existing = await idempotency_store.select(
                "_stripe_events",
                filters={"event_id": event_id},
            )
            if existing:
                logger.info(f"事件已处理过: {event_id}")
                return True
        else:
            # 使用内存存储
            if event_id in self._processed_events:
                logger.info(f"事件已处理过: {event_id}")
                return True

        # 查找处理器
        handler = handlers.get(event_type)
        if not handler:
            logger.warning(f"未找到事件处理器: {event_type}")
            return True  # 返回 True 避免 Stripe 重试

        try:
            # 执行处理器
            await handler(event)

            # 记录已处理
            if idempotency_store:
                await idempotency_store.insert(
                    "_stripe_events",
                    {
                        "event_id": event_id,
                        "event_type": event_type,
                        "processed_at": datetime.now().isoformat(),
                    },
                )
            else:
                self._processed_events.add(event_id)

            logger.info(f"事件处理成功: {event_type} ({event_id})")
            return True

        except Exception as e:
            logger.error(f"事件处理失败: {event_type} ({event_id}): {e}")
            raise WebhookError(f"事件处理失败: {e}")

    def idempotent(self, key_prefix: str) -> Callable:
        """幂等性装饰器.

        Args:
            key_prefix: 幂等性键前缀

        Returns:
            装饰器
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(event: Any, *args: Any, **kwargs: Any) -> Any:
                key = f"{key_prefix}:{event.id}"
                if key in self._processed_events:
                    logger.info(f"跳过重复事件: {key}")
                    return None
                result = await func(event, *args, **kwargs)
                self._processed_events.add(key)
                return result

            return wrapper

        return decorator

    # ========================================================================
    # 订阅管理
    # ========================================================================

    async def list_subscriptions(
        self,
        customer_id: str,
        status: str | None = None,
    ) -> list[Any]:
        """获取客户的订阅列表.

        Args:
            customer_id: 客户 ID
            status: 过滤状态（active/past_due/canceled/all）

        Returns:
            订阅列表
        """
        try:
            params: dict[str, Any] = {"customer": customer_id}
            if status and status != "all":
                params["status"] = status

            subscriptions = self._stripe.Subscription.list(**params)
            return list(subscriptions.data)
        except self._stripe.error.StripeError as e:
            raise SubscriptionError(str(e), getattr(e, "code", None))

    async def get_subscription(self, subscription_id: str) -> Any:
        """获取订阅详情.

        Args:
            subscription_id: 订阅 ID

        Returns:
            订阅对象
        """
        try:
            return self._stripe.Subscription.retrieve(subscription_id)
        except self._stripe.error.StripeError as e:
            raise SubscriptionError(str(e), getattr(e, "code", None))

    async def update_subscription(
        self,
        subscription_id: str,
        price_id: str | None = None,
        proration_behavior: str = "create_prorations",
        metadata: dict[str, str] | None = None,
    ) -> Any:
        """更新订阅.

        Args:
            subscription_id: 订阅 ID
            price_id: 新价格 ID（升级/降级）
            proration_behavior: 按比例计费行为
            metadata: 元数据

        Returns:
            更新后的订阅
        """
        try:
            params: dict[str, Any] = {
                "proration_behavior": proration_behavior,
            }

            if price_id:
                # 获取当前订阅项
                subscription = await self.get_subscription(subscription_id)
                item_id = subscription.items.data[0].id

                params["items"] = [{"id": item_id, "price": price_id}]

            if metadata:
                params["metadata"] = metadata

            updated = self._stripe.Subscription.modify(subscription_id, **params)
            logger.info(f"已更新订阅: {subscription_id}")
            return updated

        except self._stripe.error.StripeError as e:
            raise SubscriptionError(str(e), getattr(e, "code", None))

    async def cancel_subscription(
        self,
        subscription_id: str,
        cancel_at_period_end: bool = True,
    ) -> Any:
        """取消订阅.

        Args:
            subscription_id: 订阅 ID
            cancel_at_period_end: 是否在周期结束时取消

        Returns:
            取消后的订阅
        """
        try:
            if cancel_at_period_end:
                cancelled = self._stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True,
                )
            else:
                cancelled = self._stripe.Subscription.cancel(subscription_id)

            logger.info(
                f"已取消订阅: {subscription_id} "
                f"({'周期结束' if cancel_at_period_end else '立即'})"
            )
            return cancelled

        except self._stripe.error.StripeError as e:
            raise SubscriptionError(str(e), getattr(e, "code", None))

    async def pause_subscription(self, subscription_id: str) -> Any:
        """暂停订阅.

        Args:
            subscription_id: 订阅 ID

        Returns:
            暂停后的订阅
        """
        try:
            paused = self._stripe.Subscription.modify(
                subscription_id,
                pause_collection={"behavior": "mark_uncollectible"},
            )
            logger.info(f"已暂停订阅: {subscription_id}")
            return paused
        except self._stripe.error.StripeError as e:
            raise SubscriptionError(str(e), getattr(e, "code", None))

    async def resume_subscription(self, subscription_id: str) -> Any:
        """恢复订阅.

        Args:
            subscription_id: 订阅 ID

        Returns:
            恢复后的订阅
        """
        try:
            resumed = self._stripe.Subscription.modify(
                subscription_id,
                pause_collection="",
            )
            logger.info(f"已恢复订阅: {subscription_id}")
            return resumed
        except self._stripe.error.StripeError as e:
            raise SubscriptionError(str(e), getattr(e, "code", None))

    # ========================================================================
    # 退款
    # ========================================================================

    async def create_refund(
        self,
        payment_intent_id: str,
        amount: int | None = None,
        reason: str | None = None,
    ) -> Any:
        """创建退款.

        Args:
            payment_intent_id: PaymentIntent ID
            amount: 退款金额（None 表示全额）
            reason: 退款原因

        Returns:
            退款对象
        """
        try:
            params: dict[str, Any] = {"payment_intent": payment_intent_id}

            if amount:
                params["amount"] = amount
            if reason:
                params["reason"] = reason

            refund = self._stripe.Refund.create(**params)
            logger.info(
                f"已创建退款: {refund.id} "
                f"(金额: {refund.amount}, PaymentIntent: {payment_intent_id})"
            )
            return refund

        except self._stripe.error.StripeError as e:
            raise RefundError(str(e), getattr(e, "code", None))

    # ========================================================================
    # 发票
    # ========================================================================

    async def list_invoices(
        self,
        customer_id: str,
        status: str | None = None,
        limit: int = 10,
    ) -> list[Any]:
        """获取发票列表.

        Args:
            customer_id: 客户 ID
            status: 状态过滤
            limit: 返回数量

        Returns:
            发票列表
        """
        try:
            params: dict[str, Any] = {
                "customer": customer_id,
                "limit": limit,
            }
            if status:
                params["status"] = status

            invoices = self._stripe.Invoice.list(**params)
            return list(invoices.data)
        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    async def create_invoice(
        self,
        customer_id: str,
        items: list[dict[str, Any]] | None = None,
        auto_advance: bool = True,
    ) -> Any:
        """创建发票.

        Args:
            customer_id: 客户 ID
            items: 发票项目
            auto_advance: 自动发送

        Returns:
            发票对象
        """
        try:
            # 创建发票
            invoice = self._stripe.Invoice.create(
                customer=customer_id,
                auto_advance=auto_advance,
            )

            # 添加发票项目
            if items:
                for item in items:
                    self._stripe.InvoiceItem.create(
                        customer=customer_id,
                        invoice=invoice.id,
                        **item,
                    )

            # 最终化发票
            if auto_advance:
                invoice = self._stripe.Invoice.finalize_invoice(invoice.id)

            logger.info(f"已创建发票: {invoice.id}")
            return invoice

        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    # ========================================================================
    # 产品/价格管理
    # ========================================================================

    async def create_product(
        self,
        name: str,
        description: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> Any:
        """创建产品.

        Args:
            name: 产品名称
            description: 描述
            metadata: 元数据

        Returns:
            产品对象
        """
        try:
            params: dict[str, Any] = {"name": name}
            if description:
                params["description"] = description
            if metadata:
                params["metadata"] = metadata

            product = self._stripe.Product.create(**params)
            logger.info(f"已创建产品: {product.id}")
            return product
        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    async def create_price(
        self,
        product_id: str,
        unit_amount: int,
        currency: str = "jpy",
        recurring: dict[str, Any] | None = None,
    ) -> Any:
        """创建价格.

        Args:
            product_id: 产品 ID
            unit_amount: 单价（最小单位）
            currency: 货币
            recurring: 周期性设置

        Returns:
            价格对象
        """
        try:
            params: dict[str, Any] = {
                "product": product_id,
                "unit_amount": unit_amount,
                "currency": currency,
            }
            if recurring:
                params["recurring"] = recurring

            price = self._stripe.Price.create(**params)
            logger.info(f"已创建价格: {price.id}")
            return price
        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    async def list_prices(
        self,
        product_id: str | None = None,
        active: bool | None = None,
    ) -> list[Any]:
        """列出价格.

        Args:
            product_id: 产品 ID
            active: 是否活跃

        Returns:
            价格列表
        """
        try:
            params: dict[str, Any] = {}
            if product_id:
                params["product"] = product_id
            if active is not None:
                params["active"] = active

            prices = self._stripe.Price.list(**params)
            return list(prices.data)
        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    # ========================================================================
    # 客户管理
    # ========================================================================

    async def create_customer(
        self,
        email: str,
        name: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> Any:
        """创建客户.

        Args:
            email: 邮箱
            name: 名称
            metadata: 元数据

        Returns:
            客户对象
        """
        try:
            params: dict[str, Any] = {"email": email}
            if name:
                params["name"] = name
            if metadata:
                params["metadata"] = metadata

            customer = self._stripe.Customer.create(**params)
            logger.info(f"已创建客户: {customer.id}")
            return customer
        except self._stripe.error.StripeError as e:
            raise CustomerError(str(e), getattr(e, "code", None))

    async def get_customer(self, customer_id: str) -> Any:
        """获取客户.

        Args:
            customer_id: 客户 ID

        Returns:
            客户对象
        """
        try:
            return self._stripe.Customer.retrieve(customer_id)
        except self._stripe.error.StripeError as e:
            raise CustomerError(str(e), getattr(e, "code", None))

    async def get_or_create_customer(
        self,
        email: str,
        name: str | None = None,
        metadata: dict[str, str] | None = None,
    ) -> Any:
        """获取或创建客户.

        Args:
            email: 邮箱
            name: 名称
            metadata: 元数据

        Returns:
            客户对象
        """
        try:
            # 搜索现有客户
            customers = self._stripe.Customer.list(email=email, limit=1)
            if customers.data:
                return customers.data[0]

            # 创建新客户
            return await self.create_customer(email, name, metadata)
        except self._stripe.error.StripeError as e:
            raise CustomerError(str(e), getattr(e, "code", None))

    # ========================================================================
    # 测试工具
    # ========================================================================

    async def create_test_clock(self, frozen_time: datetime) -> Any:
        """创建测试时钟（仅测试模式）.

        Args:
            frozen_time: 冻结时间

        Returns:
            测试时钟对象
        """
        if not self._config.test_mode:
            raise PaymentError("测试时钟仅在测试模式下可用")

        try:
            clock = self._stripe.test_helpers.TestClock.create(
                frozen_time=int(frozen_time.timestamp())
            )
            logger.info(f"已创建测试时钟: {clock.id}")
            return clock
        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

    async def advance_test_clock(
        self,
        test_clock_id: str,
        frozen_time: datetime,
    ) -> Any:
        """推进测试时钟.

        Args:
            test_clock_id: 测试时钟 ID
            frozen_time: 新的时间

        Returns:
            更新后的测试时钟
        """
        if not self._config.test_mode:
            raise PaymentError("测试时钟仅在测试模式下可用")

        try:
            clock = self._stripe.test_helpers.TestClock.advance(
                test_clock_id,
                frozen_time=int(frozen_time.timestamp()),
            )
            logger.info(f"已推进测试时钟: {test_clock_id} -> {frozen_time}")
            return clock
        except self._stripe.error.StripeError as e:
            raise PaymentError(str(e), getattr(e, "code", None))

