class CreateCouponCodes < ActiveRecord::Migration[8.1]
  def change
    create_table :coupon_codes do |t|
      t.string :code, null: false
      t.string :usage, null: false, default: 'unused'

      t.timestamps
    end

    add_index :coupon_codes, :code, unique: true
    add_check_constraint :coupon_codes, "usage IN ('unused', 'used')", name: 'usage_check'
  end
end
