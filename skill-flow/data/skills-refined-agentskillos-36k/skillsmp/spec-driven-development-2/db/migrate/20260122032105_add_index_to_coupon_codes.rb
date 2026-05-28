class AddIndexToCouponCodes < ActiveRecord::Migration[8.1]
  def change
    add_index :coupon_codes, :usage unless index_exists?(:coupon_codes, :usage)
  end
end
