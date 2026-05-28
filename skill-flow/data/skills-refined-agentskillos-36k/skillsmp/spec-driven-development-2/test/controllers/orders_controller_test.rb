require_relative "test_helper"

class OrdersControllerTest < ActionDispatch::IntegrationTest
  def setup
    @kit = PromiseFitnessKit.create!(name: "Test Kit", description: "Test Description", slug: "test-kit")
    @coupon = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    @used_coupon = CouponCode.create!(code: "SK1001BBB", usage: "used")
    @valid_params = {
      order: {
        first_name: "John",
        last_name: "Doe",
        address1: "123 Main St",
        city: "San Francisco",
        state: "CA",
        zip: "94102",
        phone: "415-555-1234",
        email: "john@example.com",
        coupon_code_input: "SK1000AAA"
      }
    }
  end

  # New Action Tests
  test "should get new" do
    get fitness_kit_order_url(slug: @kit.slug)
    assert_response :success
  end

  test "should assign order and fitness kit" do
    get fitness_kit_order_url(slug: @kit.slug)
    assert_not_nil assigns(:order)
    assert_not_nil assigns(:promise_fitness_kit)
    assert_equal @kit.id, assigns(:promise_fitness_kit).id
  end

  test "should redirect to root for invalid kit" do
    get fitness_kit_order_url(slug: "invalid-kit-slug")
    assert_redirected_to root_path
    assert_equal "Fitness kit not found", flash[:alert]
  end

  # Create Action - Success Tests
  test "should create order with valid params" do
    assert_difference('Order.count', 1) do
      post create_fitness_kit_order_url(slug: @kit.slug), params: @valid_params
    end
  end

  test "should redirect to order show on success" do
    post create_fitness_kit_order_url(slug: @kit.slug), params: @valid_params
    assert_redirected_to order_path(Order.last)
  end

  test "should mark coupon as used after order creation" do
    assert_equal "unused", @coupon.usage
    post create_fitness_kit_order_url(slug: @kit.slug), params: @valid_params
    @coupon.reload
    assert_equal "used", @coupon.usage
  end

  test "should increment order confirmation number" do
    existing_order_count = Order.count
    post create_fitness_kit_order_url(slug: @kit.slug), params: @valid_params
    order = Order.last
    assert_equal existing_order_count + 1, order.order_confirmation
  end

  test "should set success flash message" do
    post create_fitness_kit_order_url(slug: @kit.slug), params: @valid_params
    assert_equal "Order placed successfully!", flash[:notice]
  end

  # Create Action - Error Tests
  test "should not create order with invalid coupon" do
    params = @valid_params.deep_dup
    params[:order][:coupon_code_input] = "INVALID999"

    assert_no_difference('Order.count') do
      post create_fitness_kit_order_url(slug: @kit.slug), params: params
    end
  end

  test "should render new with error for invalid coupon" do
    params = @valid_params.deep_dup
    params[:order][:coupon_code_input] = "INVALID999"

    post create_fitness_kit_order_url(slug: @kit.slug), params: params
    assert_response :unprocessable_entity
    assert_template :new
    assert_equal "Invalid coupon code", flash[:error]
  end

  test "should not create order with used coupon" do
    params = @valid_params.deep_dup
    params[:order][:coupon_code_input] = "USED123"

    assert_no_difference('Order.count') do
      post create_fitness_kit_order_url(slug: @kit.slug), params: params
    end
  end

  test "should show specific error for used coupon" do
    params = @valid_params.deep_dup
    params[:order][:coupon_code_input] = "USED123"

    post create_fitness_kit_order_url(slug: @kit.slug), params: params
    assert_response :unprocessable_entity
    assert_equal "This code has been used before and can no longer be used to place an order", flash[:error]
  end

  test "should not create order with missing fields" do
    params = @valid_params.deep_dup
    params[:order].delete(:first_name)
    params[:order].delete(:email)

    assert_no_difference('Order.count') do
      post create_fitness_kit_order_url(slug: @kit.slug), params: params
    end
  end

  test "should render new with validation errors" do
    params = @valid_params.deep_dup
    params[:order].delete(:first_name)

    post create_fitness_kit_order_url(slug: @kit.slug), params: params
    assert_response :unprocessable_entity
    assert_template :new
    assert_not_nil assigns(:order).errors[:first_name]
  end

  test "should return 422 for validation errors" do
    params = @valid_params.deep_dup
    params[:order].delete(:email)

    post create_fitness_kit_order_url(slug: @kit.slug), params: params
    assert_response :unprocessable_entity
  end

  test "should preserve form data on errors" do
    params = @valid_params.deep_dup
    params[:order].delete(:first_name)

    post create_fitness_kit_order_url(slug: @kit.slug), params: params
    order = assigns(:order)
    assert_equal "Doe", order.last_name
    assert_equal "john@example.com", order.email
  end

  # Show Action Tests
  test "should get show" do
    order = Order.create!(
      promise_fitness_kit: @kit,
      coupon_code: @coupon,
      first_name: "John",
      last_name: "Doe",
      address1: "123 Main St",
      city: "San Francisco",
      state: "CA",
      zip: "94102",
      phone: "4155551234",
      email: "john@example.com"
    )

    get order_url(order)
    assert_response :success
  end

  test "should assign order" do
    order = Order.create!(
      promise_fitness_kit: @kit,
      coupon_code: @coupon,
      first_name: "John",
      last_name: "Doe",
      address1: "123 Main St",
      city: "San Francisco",
      state: "CA",
      zip: "94102",
      phone: "4155551234",
      email: "john@example.com"
    )

    get order_url(order)
    assert_not_nil assigns(:order)
    assert_equal order.id, assigns(:order).id
  end

  test "should return 404 for invalid order" do
    assert_raises(ActiveRecord::RecordNotFound) do
      get order_url(id: 99999)
    end
  end
end
