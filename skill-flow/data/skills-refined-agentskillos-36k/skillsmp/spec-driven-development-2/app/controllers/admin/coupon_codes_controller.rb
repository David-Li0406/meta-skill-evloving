class Admin::CouponCodesController < Admin::BaseController
  PER_PAGE = 25

  def index
    @coupons = CouponCode.all

    # Filter by status
    if params[:status].present?
      @coupons = @coupons.where(usage: params[:status])
    end

    # Search by code
    if params[:search].present?
      @coupons = @coupons.where("code LIKE ?", "%#{params[:search]}%")
    end

    # Apply cursor pagination
    @coupons = @coupons.by_cursor(params[:cursor], params[:direction] || 'next')

    # Order by id
    if params[:direction] == 'prev'
      @coupons = @coupons.order(id: :desc)
    else
      @coupons = @coupons.order(id: :asc)
    end

    # Fetch one extra to check if there are more records
    @coupons = @coupons.limit(PER_PAGE + 1).to_a
    @has_more = @coupons.size > PER_PAGE
    @coupons = @coupons.first(PER_PAGE) if @has_more
  end

  def create
    begin
      code = CouponCode.generate_next_code
      coupon = CouponCode.create!(code: code, usage: 'unused')
      redirect_to admin_coupon_codes_path, notice: "Coupon code #{coupon.code} created successfully"
    rescue StandardError => e
      redirect_to admin_coupon_codes_path, alert: "Error creating coupon code: #{e.message}"
    end
  end

  def destroy
    @coupon = CouponCode.find(params[:id])

    if @coupon.destroy
      redirect_to admin_coupon_codes_path, notice: "Coupon code deleted successfully"
    else
      redirect_to admin_coupon_codes_path, alert: @coupon.errors.full_messages.join(", ")
    end
  rescue ActiveRecord::InvalidForeignKey => e
    redirect_to admin_coupon_codes_path, alert: "Cannot delete coupon code because it has associated orders"
  end
end
