class CreatePromiseFitnessKits < ActiveRecord::Migration[8.1]
  def change
    create_table :promise_fitness_kits do |t|
      t.string :name, null: false
      t.text :description, null: false

      t.timestamps
    end

    add_index :promise_fitness_kits, :name, unique: true
  end
end
