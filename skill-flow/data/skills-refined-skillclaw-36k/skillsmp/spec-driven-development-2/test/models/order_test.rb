require_relative "test_helper"

class OrderTest < ActiveSupport::TestCase
  def setup
    @kit = PromiseFitnessKit.create!(name: "Test Kit", description: "Description", slug: "test-kit")
    @coupon = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    @valid_attributes = {
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
    }
  end

  # Validation Tests - Required Fields
  test "should not save without first_name" do
    order = Order.new(@valid_attributes.except(:first_name))
    assert_not order.save, "Saved order without first_name"
    assert_includes order.errors[:first_name], "can't be blank"
  end

  test "should not save without last_name" do
    order = Order.new(@valid_attributes.except(:last_name))
    assert_not order.save, "Saved order without last_name"
    assert_includes order.errors[:last_name], "can't be blank"
  end

  test "should not save without address1" do
    order = Order.new(@valid_attributes.except(:address1))
    assert_not order.save, "Saved order without address1"
    assert_includes order.errors[:address1], "can't be blank"
  end

  test "should not save without city" do
    order = Order.new(@valid_attributes.except(:city))
    assert_not order.save, "Saved order without city"
    assert_includes order.errors[:city], "can't be blank"
  end

  test "should not save without state" do
    order = Order.new(@valid_attributes.except(:state))
    assert_not order.save, "Saved order without state"
    assert_includes order.errors[:state], "can't be blank"
  end

  test "should not save without zip" do
    order = Order.new(@valid_attributes.except(:zip))
    assert_not order.save, "Saved order without zip"
    assert_includes order.errors[:zip], "can't be blank"
  end

  test "should not save without phone" do
    order = Order.new(@valid_attributes.except(:phone))
    assert_not order.save, "Saved order without phone"
    assert_includes order.errors[:phone], "can't be blank"
  end

  test "should not save without email" do
    order = Order.new(@valid_attributes.except(:email))
    assert_not order.save, "Saved order without email"
    assert_includes order.errors[:email], "can't be blank"
  end

  test "should save without address2 (optional)" do
    order = Order.new(@valid_attributes)
    assert order.save, "Failed to save order without address2"
  end

  test "should save without description (optional)" do
    order = Order.new(@valid_attributes)
    assert order.save, "Failed to save order without description"
  end

  # Email Validation
  test "should validate email format" do
    order = Order.new(@valid_attributes.merge(email: "valid@example.com"))
    assert order.valid?, "Valid email was rejected"
  end

  test "should reject invalid email" do
    invalid_emails = ["invalid", "@example.com", "user@", "user @example.com"]
    invalid_emails.each do |invalid_email|
      order = Order.new(@valid_attributes.merge(email: invalid_email))
      assert_not order.valid?, "#{invalid_email} was accepted as valid"
      assert_includes order.errors[:email], "must be a valid email"
    end
  end

  # State Validation
  test "should validate state is 2 letters" do
    order = Order.new(@valid_attributes.merge(state: "CA"))
    assert order.valid?, "Valid state code was rejected"
  end

  test "should validate state is valid US state" do
    order = Order.new(@valid_attributes.merge(state: "CA"))
    assert order.valid?, "Valid US state was rejected"
  end

  test "should reject invalid state code" do
    order = Order.new(@valid_attributes.merge(state: "XX"))
    assert_not order.valid?, "Invalid state code was accepted"
    assert_includes order.errors[:state], "must be a valid US state"
  end

  # ZIP Validation
  test "should validate zip format 5 digits" do
    order = Order.new(@valid_attributes.merge(zip: "94102"))
    assert order.valid?, "Valid 5-digit ZIP was rejected"
  end

  test "should validate zip format ZIP+4" do
    order = Order.new(@valid_attributes.merge(zip: "94102-1234"))
    assert order.valid?, "Valid ZIP+4 was rejected"
  end

  test "should reject invalid zip" do
    invalid_zips = ["1234", "123456", "ABCDE", "9410"]
    invalid_zips.each do |invalid_zip|
      order = Order.new(@valid_attributes.merge(zip: invalid_zip))
      assert_not order.valid?, "#{invalid_zip} was accepted as valid"
      assert_includes order.errors[:zip], "must be 5 digits or ZIP+4"
    end
  end

  # Phone Validation
  test "should validate phone is exactly 10 digits" do
    order = Order.new(@valid_attributes.merge(phone: "4155551234"))
    assert order.valid?, "Valid 10-digit phone was rejected"
  end

  test "should reject phone with letters" do
    order = Order.new(@valid_attributes.merge(phone: "415555abcd"))
    assert_not order.valid?, "Phone with letters was accepted"
    assert_includes order.errors[:phone], "must contain only digits"
  end

  test "should reject phone with wrong length" do
    order = Order.new(@valid_attributes.merge(phone: "123456789"))
    assert_not order.valid?, "9-digit phone was accepted"
    assert_includes order.errors[:phone], "must be exactly 10 digits"
  end

  # Normalization Tests
  test "should normalize phone to digits only" do
    order = Order.create!(@valid_attributes.merge(phone: "415-555-1234"))
    assert_equal "4155551234", order.phone
  end

  test "should normalize email to lowercase" do
    order = Order.create!(@valid_attributes.merge(email: "Test@EXAMPLE.COM"))
    assert_equal "test@example.com", order.email
  end

  test "should normalize state to uppercase" do
    order = Order.create!(@valid_attributes.merge(state: "ca"))
    assert_equal "CA", order.state
  end

  # Order Confirmation Tests
  test "should auto-generate order_confirmation" do
    order = Order.create!(@valid_attributes)
    assert_not_nil order.order_confirmation
    assert order.order_confirmation > 0
  end

  test "should increment order_confirmation sequentially" do
    order1 = Order.create!(@valid_attributes)

    coupon2 = CouponCode.create!(code: "TEST456", usage: "unused")
    order2 = Order.create!(@valid_attributes.merge(coupon_code: coupon2))

    assert_equal order1.order_confirmation + 1, order2.order_confirmation
  end

  # Coupon Validation Tests
  test "should validate coupon_code must be unused" do
    order = Order.new(@valid_attributes)
    assert order.valid?, "Valid order with unused coupon was rejected"
  end

  test "should reject order with used coupon" do
    used_coupon = CouponCode.create!(code: "USED123", usage: "used")
    order = Order.new(@valid_attributes.merge(coupon_code: used_coupon))
    assert_not order.valid?, "Order with used coupon was accepted"
    assert_includes order.errors[:coupon_code], "has already been used"
  end

  test "should mark coupon as used after order creation" do
    assert_equal "unused", @coupon.usage
    order = Order.create!(@valid_attributes)
    @coupon.reload
    assert_equal "used", @coupon.usage
  end

  test "should rollback coupon if order fails" do
    # Create an invalid order (missing required field)
    invalid_order = Order.new(@valid_attributes.except(:first_name))
    assert_not invalid_order.save

    @coupon.reload
    assert_equal "unused", @coupon.usage, "Coupon was marked as used even though order failed"
  end

  # Helper Methods Tests
  test "formatted_order_confirmation returns 6-digit string" do
    order = Order.create!(@valid_attributes)
    formatted = order.formatted_order_confirmation
    assert_match(/\A\d{6}\z/, formatted)
    assert_equal 6, formatted.length
  end

  test "full_name returns first and last name" do
    order = Order.new(@valid_attributes)
    assert_equal "John Doe", order.full_name
  end

  test "formatted_phone returns formatted phone" do
    order = Order.create!(@valid_attributes.merge(phone: "4155551234"))
    assert_equal "(415) 555-1234", order.formatted_phone
  end

  test "full_address returns complete address" do
    order = Order.new(@valid_attributes.merge(address2: "Apt 5"))
    expected = "123 Main St\nApt 5\nSan Francisco, CA 94102"
    assert_equal expected, order.full_address
  end

  test "full_address without address2" do
    order = Order.new(@valid_attributes)
    expected = "123 Main St\nSan Francisco, CA 94102"
    assert_equal expected, order.full_address
  end

  test "next_confirmation_number returns next number" do
    next_num = Order.next_confirmation_number
    order = Order.create!(@valid_attributes)
    assert_equal next_num, order.order_confirmation
  end

  # Association Tests
  test "should belong to promise_fitness_kit" do
    order = Order.reflect_on_association(:promise_fitness_kit)
    assert_equal :belongs_to, order.macro
  end

  test "should belong to coupon_code" do
    order = Order.reflect_on_association(:coupon_code)
    assert_equal :belongs_to, order.macro
  end

  # Scope Tests
  test "recent scope returns orders in reverse chronological order" do
    order1 = Order.create!(@valid_attributes)

    coupon2 = CouponCode.create!(code: "TEST789", usage: "unused")
    order2 = Order.create!(@valid_attributes.merge(coupon_code: coupon2))

    recent_orders = Order.recent
    assert_equal order2.id, recent_orders.first.id
    assert_equal order1.id, recent_orders.last.id
  end
end
