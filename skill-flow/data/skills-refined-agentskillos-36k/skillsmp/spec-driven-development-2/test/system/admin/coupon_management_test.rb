require_relative "../test_helper"

class Admin::CouponManagementTest < ApplicationSystemTestCase
  setup do
    Admin.destroy_all
    @admin = Admin.create!(username: "admin", password: "password123", password_confirmation: "password123")
    # Clear existing coupons to have a clean state
    CouponCode.destroy_all
  end

  test "admin can create, filter, search, and delete coupon codes" do
    # Login as admin
    visit admin_login_path
    fill_in "Username", with: @admin.username
    fill_in "Password", with: "password123"
    click_button "Log In"

    # Should be on dashboard now
    assert_text "Admin Dashboard"

    # Navigate to coupon codes
    visit admin_coupon_codes_path
    assert_text "Coupon Codes"

    # Create a new coupon code
    click_button "Create New Coupon"
    assert_text "created successfully"

    # Verify the code follows SK format
    first_coupon = CouponCode.first
    assert_match /\ASK\d+[A-Z]{3}\z/, first_coupon.code
    assert_text first_coupon.code

    # Create a few more coupons
    click_button "Create New Coupon"
    assert_text "created successfully"

    click_button "Create New Coupon"
    assert_text "created successfully"

    # Verify we have 3 coupons
    assert_equal 3, CouponCode.count

    # All should be unused initially
    assert_equal 3, CouponCode.unused.count

    # Mark one as used for testing
    second_coupon = CouponCode.second
    second_coupon.mark_as_used!

    # Refresh page
    visit admin_coupon_codes_path

    # Filter by unused status
    click_link "Unused"
    assert_text first_coupon.code
    assert_no_text second_coupon.code

    # Filter by used status
    click_link "Used"
    assert_text second_coupon.code
    assert_no_text first_coupon.code

    # Go back to all
    click_link "All"
    assert_text first_coupon.code
    assert_text second_coupon.code

    # Search for specific code
    fill_in "search", with: first_coupon.code[0..5]
    click_button "Search"
    assert_text first_coupon.code

    # Clear search
    click_link "Clear"
    assert_text first_coupon.code
    assert_text second_coupon.code

    # Try to delete a used coupon (should fail)
    within("tr", text: second_coupon.code) do
      # Should not have a delete button for used coupons
      assert_no_button "Delete"
    end

    # Delete an unused coupon (should succeed)
    third_coupon = CouponCode.third
    within("tr", text: third_coupon.code) do
      # Handle the confirmation dialog
      accept_confirm do
        click_button "Delete"
      end
    end

    assert_text "deleted successfully"
    assert_no_text third_coupon.code
    assert_equal 2, CouponCode.count
  end

  test "admin cannot delete coupon with associated order" do
    # Create a coupon and associate it with an order
    kit = PromiseFitnessKit.create!(name: "Test Kit", description: "Description", slug: "test-kit")
    coupon = CouponCode.create!(code: "SK1000AAA", usage: "unused")
    order = Order.create!(
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

    # Login
    visit admin_login_path
    fill_in "Username", with: @admin.username
    fill_in "Password", with: "password123"
    click_button "Log In"

    # Should be on dashboard
    assert_text "Admin Dashboard"

    # Go to coupon codes page
    visit admin_coupon_codes_path

    # Coupon should be marked as used now (because it has an order)
    # and should not have a delete button
    within("tr", text: coupon.code) do
      assert_no_button "Delete"
    end

    # Verify the coupon still exists
    assert CouponCode.exists?(coupon.id)
  end

  test "pagination works correctly" do
    # Login
    visit admin_login_path
    fill_in "Username", with: @admin.username
    fill_in "Password", with: "password123"
    click_button "Log In"

    # Should be on dashboard
    assert_text "Admin Dashboard"

    # Create more than PER_PAGE (25) coupons
    30.times do
      CouponCode.create!(code: CouponCode.generate_next_code, usage: "unused")
    end

    visit admin_coupon_codes_path

    # Should show "Coupon Codes" heading
    assert_text "Coupon Codes"

    # Should show 25 coupons on first page
    assert_text "Showing 25 coupons"

    # Next button should be enabled
    assert_link "Next →"

    # Previous button should be disabled
    assert_text "← Previous"
    # Check that it's a span, not a link (disabled)
    assert_selector "span", text: "← Previous"

    # Click next
    click_link "Next →"

    # Should show remaining coupons
    assert_text "Showing 5 coupons"

    # Previous button should now be enabled
    assert_link "← Previous"

    # Click previous
    click_link "← Previous"

    # Should be back to first page
    assert_text "Showing 25 coupons"
  end

  test "sequential code generation increments correctly" do
    # Login
    visit admin_login_path
    fill_in "Username", with: @admin.username
    fill_in "Password", with: "password123"
    click_button "Log In"

    # Should be on dashboard
    assert_text "Admin Dashboard"

    visit admin_coupon_codes_path

    # Create first coupon
    click_button "Create New Coupon"

    # Wait for the page to reload
    assert_text "created successfully"

    first_code = CouponCode.last.code

    # Extract the number from first code
    first_number = first_code.match(/SK(\d+)/)[1].to_i

    # Create second coupon
    click_button "Create New Coupon"

    # Wait for the page to reload
    assert_text "created successfully"

    second_code = CouponCode.last.code
    second_number = second_code.match(/SK(\d+)/)[1].to_i

    # Second number should be first + 1
    assert_equal first_number + 1, second_number

    # Create third coupon
    click_button "Create New Coupon"

    # Wait for the page to reload
    assert_text "created successfully"

    third_code = CouponCode.last.code
    third_number = third_code.match(/SK(\d+)/)[1].to_i

    # Third number should be second + 1
    assert_equal second_number + 1, third_number
  end
end
