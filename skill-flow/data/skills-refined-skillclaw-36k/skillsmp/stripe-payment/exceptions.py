"""Stripe Payment 异常定义."""


class StripeError(Exception):
    """Stripe 基础异常."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """初始化异常."""
        super().__init__(message)
        self.message = message
        self.code = code


class PaymentError(StripeError):
    """支付错误."""

    pass


class WebhookError(StripeError):
    """Webhook 错误."""

    pass


class SubscriptionError(StripeError):
    """订阅错误."""

    pass


class RefundError(StripeError):
    """退款错误."""

    pass


class CustomerError(StripeError):
    """客户错误."""

    pass


class SignatureVerificationError(StripeError):
    """签名验证错误."""

    pass

