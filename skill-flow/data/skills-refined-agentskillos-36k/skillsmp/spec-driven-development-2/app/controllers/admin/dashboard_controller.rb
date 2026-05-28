class Admin::DashboardController < Admin::BaseController
  def index
    # Placeholder - will be fully implemented in Phase 4
    @total_orders = Order.count
    @total_coupons = CouponCode.count
    @unused_coupons = CouponCode.unused.count
  end
end
