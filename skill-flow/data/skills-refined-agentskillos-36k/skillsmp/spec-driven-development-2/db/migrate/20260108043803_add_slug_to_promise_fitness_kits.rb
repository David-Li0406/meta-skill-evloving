class AddSlugToPromiseFitnessKits < ActiveRecord::Migration[8.1]
  def up
    # Step 1: Add column (nullable initially)
    add_column :promise_fitness_kits, :slug, :string

    # Step 2: Populate slugs for existing kits
    reversible do |dir|
      dir.up do
        mapping = {
          'SK-1' => 'strength-kit-1',
          'SK-2' => 'strength-kit-2',
          'SK-3' => 'strength-kit-3',
          'SK-4' => 'strength-kit-4',
          'PK-1' => 'pilates-kit-1',
          'YK-1' => 'yoga-kit-1',
          'WK-1' => 'walking-trekking-kit-1'
        }

        mapping.each do |name, slug|
          kit = PromiseFitnessKit.find_by(name: name)
          kit&.update_column(:slug, slug)
        end

        # Handle Test Kit if it exists (from test fixtures)
        test_kit = PromiseFitnessKit.find_by(name: 'Test Kit')
        test_kit&.update_column(:slug, 'test-kit')
      end
    end

    # Step 3: Add constraints
    change_column_null :promise_fitness_kits, :slug, false
    add_index :promise_fitness_kits, :slug, unique: true
  end

  def down
    remove_index :promise_fitness_kits, :slug
    remove_column :promise_fitness_kits, :slug
  end
end
