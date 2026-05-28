/**
 * BOG Payment Gateway TypeScript Type Definitions
 *
 * These types can be copied into your project for type-safe
 * integration with the Bank of Georgia Payment Gateway API.
 */

// ============================================
// Authentication
// ============================================

export interface AuthTokenResponse {
  access_token: string;
  token_type: 'Bearer';
  expires_in: number;
}

export interface AuthCredentials {
  clientId: string;
  clientSecret: string;
}

// ============================================
// Order Creation
// ============================================

export interface BasketItem {
  /** Product SKU or identifier (required) */
  product_id: string;
  /** Item quantity (required) */
  quantity: number;
  /** Price per unit in minor units or decimal (required) */
  unit_price: number;
  /** Product description */
  description?: string;
  /** Discount amount per unit */
  unit_discount_price?: number;
  /** Total price for this line item */
  total_price?: number;
  /** VAT amount */
  vat?: number;
  /** VAT percentage (e.g., 18 for 18%) */
  vat_percent?: number;
  /** Product image URL */
  image?: string;
  /** Package code for customs */
  package_code?: string;
  /** Tax identification number */
  tin?: string;
  /** Personal identification number (Uzbekistan) */
  pinfl?: string;
  /** Discount campaign ID */
  product_discount_id?: string;
}

export interface Delivery {
  /** Delivery fee amount */
  amount?: number;
}

export interface PurchaseUnits {
  /** Array of items in the basket (required) */
  basket: BasketItem[];
  /** Total order amount (required) */
  total_amount: number;
  /** Currency code (default: GEL) */
  currency?: 'GEL' | 'USD' | 'EUR';
  /** Total discount amount */
  total_discount_amount?: number;
  /** Delivery details */
  delivery?: Delivery;
}

export interface RedirectUrls {
  /** URL to redirect on successful payment */
  success?: string;
  /** URL to redirect on failed payment */
  fail?: string;
}

export interface Buyer {
  /** Customer full name */
  full_name?: string;
  /** Masked email (e.g., j***@example.com) */
  masked_email?: string;
  /** Masked phone (e.g., +995*****1234) */
  masked_phone?: string;
}

export interface LoanConfig {
  /** Loan type */
  type?: string;
  /** Number of installment months */
  month?: number;
}

export interface CampaignConfig {
  /** Campaign card type */
  card?: string;
  /** Campaign type */
  type?: string;
}

export interface AccountConfig {
  /** Account tag for routing */
  tag?: string;
}

export interface OrderConfig {
  /** Loan/installment configuration */
  loan?: LoanConfig;
  /** Campaign configuration */
  campaign?: CampaignConfig;
  /** Account routing configuration */
  account?: AccountConfig;
}

export type PaymentMethod = 'card' | 'google_pay' | 'apple_pay' | 'bog_auth';
export type CaptureMode = 'automatic' | 'manual';
export type ApplicationType = 'web' | 'mobile';

export interface CreateOrderRequest {
  /** Callback URL for payment notifications (required) */
  callback_url: string;
  /** Order details including basket items (required) */
  purchase_units: PurchaseUnits;
  /** Merchant's external order ID */
  external_order_id?: string;
  /** Capture mode: automatic (default) or manual for pre-auth */
  capture?: CaptureMode;
  /** Success/fail redirect URLs */
  redirect_urls?: RedirectUrls;
  /** Customer information */
  buyer?: Buyer;
  /** Allowed payment methods */
  payment_method?: PaymentMethod[];
  /** Time-to-live in seconds (default: 600) */
  ttl?: number;
  /** Application type */
  application_type?: ApplicationType;
  /** Additional configuration */
  config?: OrderConfig;
}

export interface OrderLinks {
  /** Link to get order details */
  details: {
    href: string;
  };
  /** Link to redirect customer for payment */
  redirect: {
    href: string;
  };
}

export interface CreateOrderResponse {
  /** BOG order ID */
  id: string;
  /** Merchant's external order ID */
  external_order_id?: string;
  /** Order status */
  status: OrderStatus;
  /** Currency code */
  currency: string;
  /** Total amount */
  total_amount: number;
  /** HATEOAS links */
  _links: OrderLinks;
}

// ============================================
// Payment Details
// ============================================

export type OrderStatus =
  | 'created'
  | 'processing'
  | 'completed'
  | 'rejected'
  | 'expired'
  | 'refunded'
  | 'partially_refunded';

export interface OrderStatusDetail {
  key: OrderStatus;
  value: string;
}

export interface PaymentDetail {
  /** Payment response code */
  code: PaymentResponseCode;
  /** Human-readable message */
  message: string;
  /** Masked card number (if card payment) */
  card_mask?: string;
  /** Transaction ID */
  transaction_id?: string;
}

export interface PaymentDetailsResponse {
  /** BOG order ID */
  id: string;
  /** Merchant's external order ID */
  external_order_id?: string;
  /** Current order status */
  status: OrderStatus;
  /** Detailed status information */
  order_status: OrderStatusDetail;
  /** Payment result details */
  payment_detail?: PaymentDetail;
  /** Order amounts and items */
  purchase_units: PurchaseUnits;
  /** Order creation timestamp */
  create_date: string;
  /** Payment completion timestamp */
  payment_date?: string;
}

// ============================================
// Refund
// ============================================

export interface RefundRequest {
  /** Amount to refund (omit for full refund) */
  amount?: number;
}

export interface RefundResponse {
  /** Response key */
  key: string;
  /** Human-readable message */
  message: string;
  /** Refund action ID for tracking */
  action_id: string;
}

// ============================================
// Callback
// ============================================

export interface PaymentCallback {
  /** BOG order ID */
  order_id: string;
  /** Merchant's external order ID */
  external_order_id?: string;
  /** Payment status */
  status: OrderStatus;
  /** Payment result details */
  payment_detail: PaymentDetail;
  /** Callback timestamp */
  timestamp: string;
}

// ============================================
// Response Codes
// ============================================

export type PaymentResponseCode =
  | 100  // Successful payment
  | 200  // Successful preauthorization
  | 101  // Card usage limited
  | 102  // Saved card not found
  | 103  // Invalid card
  | 104  // Transaction limit exceeded
  | 105  // Card expired
  | 106  // Amount limit exceeded
  | 107  // Insufficient funds
  | 108  // Authentication declined
  | 109  // Technical issue
  | 110  // Transaction expired
  | 111  // Authentication timeout
  | 112  // General error
  | 199; // Unknown response

export const PAYMENT_RESPONSE_CODES = {
  SUCCESSFUL_PAYMENT: 100,
  SUCCESSFUL_PREAUTH: 200,
  CARD_LIMITED: 101,
  SAVED_CARD_NOT_FOUND: 102,
  INVALID_CARD: 103,
  TRANSACTION_LIMIT: 104,
  CARD_EXPIRED: 105,
  AMOUNT_LIMIT: 106,
  INSUFFICIENT_FUNDS: 107,
  AUTH_DECLINED: 108,
  TECHNICAL_ISSUE: 109,
  TRANSACTION_EXPIRED: 110,
  AUTH_TIMEOUT: 111,
  GENERAL_ERROR: 112,
  UNKNOWN: 199,
} as const;

// ============================================
// API Client Configuration
// ============================================

export interface BogPaymentConfig {
  /** OAuth client ID */
  clientId: string;
  /** OAuth client secret */
  clientSecret: string;
  /** Environment: production or sandbox */
  environment?: 'production' | 'sandbox';
  /** Request timeout in milliseconds */
  timeout?: number;
}

// ============================================
// Request Headers
// ============================================

export interface RequestHeaders {
  Authorization: string;
  'Content-Type': 'application/json';
  'Accept-Language'?: 'ka' | 'en';
  'Idempotency-Key'?: string;
  Theme?: string;
}

// ============================================
// Error Response
// ============================================

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface ApiErrorResponse {
  error: ApiError;
  timestamp: string;
}
