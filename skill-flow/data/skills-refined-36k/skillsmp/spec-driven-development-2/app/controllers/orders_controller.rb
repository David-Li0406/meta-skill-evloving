class OrdersController < ApplicationController
  before_action :set_promise_fitness_kit, only: [:new, :create]

  def new
    @order = Order.new(promise_fitness_kit: @promise_fitness_kit)
    @coupon_code = CouponCode.new
  end

  def create
    @order = Order.new(order_params)
    @order.promise_fitness_kit = @promise_fitness_kit

    # Find and validate coupon code
    coupon = CouponCode.find_by(code: params[:order][:coupon_code_input]&.upcase&.strip)

    if coupon.nil?
      flash.now[:error] = 'Invalid coupon code'
      render :new, status: :unprocessable_entity
      return
    end

    if coupon.used?
      flash.now[:error] = 'This code has been used before and can no longer be used to place an order'
      render :new, status: :unprocessable_entity
      return
    end

    @order.coupon_code = coupon

    if @order.save
      redirect_to order_path(@order), notice: 'Order placed successfully!'
    else
      flash.now[:error] = 'Please correct the errors below'
      render :new, status: :unprocessable_entity
    end
  end

  def show
    @order = Order.find(params[:id])
  end

  private

  def set_promise_fitness_kit
    @promise_fitness_kit = PromiseFitnessKit.find_by(slug: params[:slug])

    if @promise_fitness_kit.nil?
      redirect_to root_path, alert: 'Fitness kit not found'
    end
  end

  def order_params
    params.require(:order).permit(
      :first_name,
      :last_name,
      :address1,
      :address2,
      :city,
      :state,
      :zip,
      :phone,
      :email,
      :description
    )
  end
end
