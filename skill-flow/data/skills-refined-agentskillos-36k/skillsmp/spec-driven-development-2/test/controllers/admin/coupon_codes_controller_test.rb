require_relative "../test_helper"

class Admin::CouponCodesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @admin = admins(:one)
    login_as_admin(@admin)
  end

  def login_as_admin(admin)
    post admin_login_url, params: { username: admin.username, password: 'password123' }
  end

  # Index action tests
  test "should get index" do
    get admin_coupon_codes_url
    assert_response :success
  end

  test "should require authentication for index" do
    delete admin_logout_url
    get admin_coupon_codes_url
    assert_redirected_to admin_login_url
  end

  test "index should load coupon codes" do
    coupon = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    get admin_coupon_codes_url
    assert_response :success
    assert_select 'td', text: coupon.code
  end

  test "index should filter by status unused" do
    unused = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    used = CouponCode.create!(code: 'SK1001BBB', usage: 'used')

    get admin_coupon_codes_url, params: { status: 'unused' }
    assert_response :success

    assert_select 'td', text: unused.code
    assert_select 'td', text: used.code, count: 0
  end

  test "index should filter by status used" do
    unused = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    used = CouponCode.create!(code: 'SK1001BBB', usage: 'used')

    get admin_coupon_codes_url, params: { status: 'used' }
    assert_response :success

    assert_select 'td', text: unused.code, count: 0
    assert_select 'td', text: used.code
  end

  test "index should search by code" do
    matching = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    non_matching = CouponCode.create!(code: 'SK1001BBB', usage: 'unused')

    get admin_coupon_codes_url, params: { search: '1000' }
    assert_response :success

    assert_select 'td', text: matching.code
    assert_select 'td', text: non_matching.code, count: 0
  end

  test "index should handle cursor pagination next" do
    c1 = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    c2 = CouponCode.create!(code: 'SK1001BBB', usage: 'unused')
    c3 = CouponCode.create!(code: 'SK1002CCC', usage: 'unused')

    get admin_coupon_codes_url, params: { cursor: c1.id, direction: 'next' }
    assert_response :success

    assert_select 'td', text: c1.code, count: 0
  end

  test "index should handle cursor pagination prev" do
    c1 = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    c2 = CouponCode.create!(code: 'SK1001BBB', usage: 'unused')
    c3 = CouponCode.create!(code: 'SK1002CCC', usage: 'unused')

    get admin_coupon_codes_url, params: { cursor: c3.id, direction: 'prev' }
    assert_response :success

    assert_select 'td', text: c3.code, count: 0
  end

  # Create action tests
  test "should create new coupon code" do
    assert_difference('CouponCode.count', 1) do
      post admin_coupon_codes_url
    end

    assert_redirected_to admin_coupon_codes_url
    assert_match /Coupon code .* created successfully/, flash[:notice]
  end

  test "created coupon should follow SK format" do
    post admin_coupon_codes_url

    new_coupon = CouponCode.last
    assert_match /\ASK\d+[A-Z]{3}\z/, new_coupon.code
  end

  test "created coupon should be unused" do
    post admin_coupon_codes_url

    new_coupon = CouponCode.last
    assert_equal 'unused', new_coupon.usage
  end

  test "should require authentication for create" do
    delete admin_logout_url
    post admin_coupon_codes_url
    assert_redirected_to admin_login_url
  end



  # Destroy action tests
  test "should destroy unused coupon" do
    coupon = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')

    assert_difference('CouponCode.count', -1) do
      delete admin_coupon_code_url(coupon)
    end

    assert_redirected_to admin_coupon_codes_url
    assert_match /deleted successfully/, flash[:notice]
  end

  test "should not destroy used coupon" do
    coupon = CouponCode.create!(code: 'SK1000AAA', usage: 'used')

    assert_no_difference('CouponCode.count') do
      delete admin_coupon_code_url(coupon)
    end

    assert_redirected_to admin_coupon_codes_url
    assert_match /cannot be deleted/i, flash[:alert]
  end

  test "should not destroy coupon with orders" do
    kit = PromiseFitnessKit.create!(name: "Test Kit", description: "Description", slug: "test-kit")
    coupon = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
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

    assert_no_difference('CouponCode.count') do
      delete admin_coupon_code_url(coupon)
    end

    assert_redirected_to admin_coupon_codes_url
    assert_match /Cannot delete/i, flash[:alert]
  end

  test "should require authentication for destroy" do
    coupon = CouponCode.create!(code: 'SK1000AAA', usage: 'unused')
    delete admin_logout_url

    delete admin_coupon_code_url(coupon)
    assert_redirected_to admin_login_url
  end


end
