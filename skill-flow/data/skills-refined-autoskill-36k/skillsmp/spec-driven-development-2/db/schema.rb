# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.1].define(version: 2026_01_22_032105) do
  create_table "admins", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.string "password_digest", null: false
    t.datetime "updated_at", null: false
    t.string "username", null: false
    t.index ["username"], name: "index_admins_on_username", unique: true
  end

  create_table "coupon_codes", force: :cascade do |t|
    t.string "code", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "usage", default: "unused", null: false
    t.index ["code"], name: "index_coupon_codes_on_code", unique: true
    t.index ["usage"], name: "index_coupon_codes_on_usage"
    t.check_constraint "usage IN ('unused', 'used')", name: "usage_check"
  end

  create_table "orders", force: :cascade do |t|
    t.string "address1", null: false
    t.string "address2"
    t.string "city", null: false
    t.integer "coupon_code_id", null: false
    t.datetime "created_at", null: false
    t.text "description"
    t.string "email", null: false
    t.string "first_name", null: false
    t.string "last_name", null: false
    t.integer "order_confirmation", null: false
    t.string "phone", limit: 10, null: false
    t.integer "promise_fitness_kit_id", null: false
    t.string "state", limit: 2, null: false
    t.datetime "updated_at", null: false
    t.string "zip", null: false
    t.index ["coupon_code_id"], name: "index_orders_on_coupon_code_id"
    t.index ["created_at"], name: "index_orders_on_created_at"
    t.index ["email"], name: "index_orders_on_email"
    t.index ["order_confirmation"], name: "index_orders_on_order_confirmation", unique: true
    t.index ["promise_fitness_kit_id"], name: "index_orders_on_promise_fitness_kit_id"
  end

  create_table "promise_fitness_kits", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.text "description", null: false
    t.string "name", null: false
    t.string "slug", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_promise_fitness_kits_on_name", unique: true
    t.index ["slug"], name: "index_promise_fitness_kits_on_slug", unique: true
  end

  add_foreign_key "orders", "coupon_codes"
  add_foreign_key "orders", "promise_fitness_kits"
end
