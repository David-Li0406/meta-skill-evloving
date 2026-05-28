require_relative "test_helper"

class CouponCodeTest < ActiveSupport::TestCase
  test "should not save without code" do
    coupon = CouponCode.new(usage: "unused")
    assert_not coupon.save, "Saved coupon without code"
    assert_includes coupon.errors[:code], "can't be blank"
  end

  test "should not save duplicate code" do
    CouponCode.create!(code: "SK1000AAA", usage: "unused")
    coupon = CouponCode.new(code: "SK1000AAA", usage: "unused")
    assert_not coupon.save, "Saved coupon with duplicate code"
    assert_includes coupon.errors[:code], "has already been taken"
  end

  test "should validate case-insensitive uniqueness" do
    CouponCode.create!(code: "SK1000AAA", usage: "unused")
    coupon = CouponCode.new(code: "sk1000aaa", usage: "unused")
    assert_not coupon.save, "Saved coupon with duplicate code (different case)"
    assert_includes coupon.errors[:code], "has already been taken"
  end

  test "should normalize code to uppercase" do
    coupon = CouponCode.create!(code: "sk1000abc", usage: "unused")
    assert_equal "SK1000ABC", coupon.code
  end

  test "should default usage to unused" do
    coupon = CouponCode.new(code: "SK1000AAA")
    assert_equal "unused", coupon.usage
  end

  test "should validate usage inclusion" do
    coupon = CouponCode.new(code: "SK1000AAA", usage: "invalid")
    assert_not coupon.save, "Saved coupon with invalid usage"
    assert_includes coupon.errors[:usage], "is not included in the list"
  end

  test "unused? returns true for unused coupons" do
    coupon = CouponCode.new(code: "SK1000AAA", usage: "unused")
    assert coupon.unused?, "unused? should return true for unused coupons"
  end

  test "used? returns true for used coupons" do
    coupon = CouponCode.new(code: "SK1000AAA", usage: "used")
    assert coupon.used?, "used? should return true for used coupons"
  end

  test "mark_as_used! changes usage to used" do
    coupon = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    coupon.mark_as_used!
    assert_equal "used", coupon.usage
    assert coupon.used?
  end

  test "unused scope returns only unused coupons" do
    CouponCode.create!(code: "SK1000AAA", usage: "unused")
    CouponCode.create!(code: "SK1001BBB", usage: "used")
    CouponCode.create!(code: "SK1002CCC", usage: "unused")

    unused_coupons = CouponCode.unused
    assert_equal 2, unused_coupons.count
    assert unused_coupons.all?(&:unused?)
  end

  test "used scope returns only used coupons" do
    CouponCode.create!(code: "SK1000AAA", usage: "unused")
    CouponCode.create!(code: "SK1001BBB", usage: "used")
    CouponCode.create!(code: "SK1002CCC", usage: "used")

    used_coupons = CouponCode.used
    assert_equal 2, used_coupons.count
    assert used_coupons.all?(&:used?)
  end

  test "should have many orders" do
    coupon = CouponCode.reflect_on_association(:orders)
    assert_equal :has_many, coupon.macro
  end

  test "should not delete coupon with associated orders" do
    kit = PromiseFitnessKit.create!(name: "Test Kit", description: "Description", slug: "test-kit")
    coupon = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    Order.create!(
      promise_fitness_kit: kit,
      coupon_code: coupon,
      first_name: "John",
      last_name: "Doe",
      address1: "123 Main St",
      city: "San Francisco",
      state: "CA",
      zip: "94102",
      phone: "4155551234",
      email: "john@example.com"
    )

    assert_not coupon.destroy, "Coupon was destroyed even though it has associated orders"
    assert_includes coupon.errors.full_messages.join, "Cannot delete record because dependent orders exist"
  end

  # New format validation tests
  test "should accept valid SK format codes" do
    valid_codes = ["SK1000AAA", "SK1001BBB", "SK9999ZZZ", "SK0ABC"]
    valid_codes.each do |code|
      coupon = CouponCode.new(code: code, usage: "unused")
      assert coupon.valid?, "#{code} should be valid but got errors: #{coupon.errors.full_messages}"
    end
  end

  test "should reject invalid format codes" do
    invalid_codes = ["TEST123", "SK1000", "SK1000AA", "SK1000AAAA", "1000AAA", "SKABC", "SK-1000AAA"]
    invalid_codes.each do |code|
      coupon = CouponCode.new(code: code, usage: "unused")
      assert_not coupon.valid?, "#{code} should be invalid"
      assert_includes coupon.errors[:code], "must be in format SK[number][3 letters]"
    end
  end

  # generate_next_code tests
  test "generate_next_code returns SK1000AAA when no coupons exist" do
    CouponCode.delete_all
    code = CouponCode.generate_next_code
    assert_match /\ASK1000[A-Z]{3}\z/, code
    assert code.starts_with?("SK1000")
  end

  test "generate_next_code increments the number correctly" do
    CouponCode.create!(code: "SK1000AAA", usage: "unused")
    CouponCode.create!(code: "SK1001BBB", usage: "unused")

    code = CouponCode.generate_next_code
    assert code.starts_with?("SK1002"), "Expected code to start with SK1002, got #{code}"
    assert_match /\ASK1002[A-Z]{3}\z/, code
  end

  test "generate_next_code finds max number across all codes" do
    CouponCode.create!(code: "SK1005CCC", usage: "unused")
    CouponCode.create!(code: "SK1002AAA", usage: "unused")
    CouponCode.create!(code: "SK1010BBB", usage: "unused")

    code = CouponCode.generate_next_code
    assert code.starts_with?("SK1011"), "Expected code to start with SK1011, got #{code}"
  end

  test "generate_next_code returns code in correct format" do
    code = CouponCode.generate_next_code
    assert_match /\ASK\d+[A-Z]{3}\z/, code, "Generated code should match SK format"
  end

  # Deletion protection tests
  test "cannot delete used coupon" do
    coupon = CouponCode.create!(code: "SK1000AAA", usage: "used")

    result = coupon.destroy
    assert_not result, "Should not be able to delete used coupon"
    assert CouponCode.exists?(coupon.id), "Used coupon should still exist in database"
    assert_includes coupon.errors.full_messages.join, "cannot be deleted"
  end

  test "can delete unused coupon" do
    coupon = CouponCode.create!(code: "SK1000AAA", usage: "unused")

    result = coupon.destroy
    assert result, "Should be able to delete unused coupon"
    assert_not CouponCode.exists?(coupon.id), "Unused coupon should be deleted from database"
  end

  # Cursor pagination scope test
  test "by_cursor scope with next direction" do
    c1 = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    c2 = CouponCode.create!(code: "SK1001BBB", usage: "unused")
    c3 = CouponCode.create!(code: "SK1002CCC", usage: "unused")

    results = CouponCode.by_cursor(c1.id, 'next').limit(2)
    assert_equal 2, results.count
    assert_equal c2.id, results.first.id
    assert_equal c3.id, results.last.id
  end

  test "by_cursor scope with prev direction" do
    c1 = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    c2 = CouponCode.create!(code: "SK1001BBB", usage: "unused")
    c3 = CouponCode.create!(code: "SK1002CCC", usage: "unused")

    results = CouponCode.by_cursor(c3.id, 'prev').limit(2).order(id: :desc)
    assert_equal 2, results.count
    assert_includes results.pluck(:id), c1.id
    assert_includes results.pluck(:id), c2.id
  end

  test "by_cursor returns all records when cursor is nil" do
    CouponCode.create!(code: "SK1000AAA", usage: "unused")
    CouponCode.create!(code: "SK1001BBB", usage: "unused")

    results = CouponCode.by_cursor(nil, 'next')
    assert_equal 2, results.count
  end
end
