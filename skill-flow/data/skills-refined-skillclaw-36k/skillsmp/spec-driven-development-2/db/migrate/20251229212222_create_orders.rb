class CreateOrders < ActiveRecord::Migration[8.1]
  def change
    create_table :orders do |t|
      t.references :promise_fitness_kit, null: false, foreign_key: true
      t.references :coupon_code, null: false, foreign_key: true
      t.integer :order_confirmation, null: false
      t.string :first_name, null: false
      t.string :last_name, null: false
      t.string :address1, null: false
      t.string :address2
      t.string :city, null: false
      t.string :state, null: false, limit: 2
      t.string :zip, null: false
      t.string :phone, null: false, limit: 10
      t.string :email, null: false
      t.text :description

      t.timestamps
    end

    add_index :orders, :order_confirmation, unique: true
    add_index :orders, :email
    add_index :orders, :created_at
  end
end
