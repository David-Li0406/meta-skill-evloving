# Model Specs Reference

## Complete Model Spec Structure

```ruby
# spec/models/task_spec.rb
require 'rails_helper'

RSpec.describe Task, type: :model do
  describe 'associations' do
    it { is_expected.to belong_to(:account) }
    it { is_expected.to belong_to(:merchant) }
    it { is_expected.to have_many(:timelines) }
  end

  describe 'validations' do
    it { is_expected.to validate_presence_of(:status) }
    it { is_expected.to validate_inclusion_of(:status).in_array(Task::STATUSES) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:pending_task) { create(:task, status: 'pending') }
      let!(:completed_task) { create(:task, status: 'completed') }

      it 'returns only non-completed tasks' do
        expect(Task.active).to include(pending_task)
        expect(Task.active).not_to include(completed_task)
      end
    end
  end

  describe '#completable?' do
    context 'when task is pending' do
      let(:task) { build(:task, status: 'pending') }

      it 'returns true' do
        expect(task.completable?).to be true
      end
    end

    context 'when task is completed' do
      let(:task) { build(:task, status: 'completed') }

      it 'returns false' do
        expect(task.completable?).to be false
      end
    end
  end
end
```

---

## Shoulda Matchers

### Association Matchers

```ruby
# belongs_to
it { is_expected.to belong_to(:account) }
it { is_expected.to belong_to(:merchant).optional }
it { is_expected.to belong_to(:carrier).class_name('User') }

# has_many
it { is_expected.to have_many(:timelines).dependent(:destroy) }
it { is_expected.to have_many(:tasks).through(:assignments) }

# has_one
it { is_expected.to have_one(:profile) }
it { is_expected.to have_one(:address).dependent(:destroy) }
```

### Validation Matchers

```ruby
# Presence
it { is_expected.to validate_presence_of(:email) }

# Uniqueness
it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
it { is_expected.to validate_uniqueness_of(:code).scoped_to(:account_id) }

# Length
it { is_expected.to validate_length_of(:password).is_at_least(8) }
it { is_expected.to validate_length_of(:bio).is_at_most(500) }

# Numericality
it { is_expected.to validate_numericality_of(:amount).is_greater_than(0) }
it { is_expected.to validate_numericality_of(:quantity).only_integer }

# Inclusion
it { is_expected.to validate_inclusion_of(:status).in_array(%w[draft published]) }

# Format
it { is_expected.to allow_value('test@example.com').for(:email) }
it { is_expected.not_to allow_value('invalid').for(:email) }
```

### Enum Matchers

```ruby
it { is_expected.to define_enum_for(:status).with_values([:pending, :active, :completed]) }
it { is_expected.to define_enum_for(:role).with_prefix(true) }
```

---

## Testing Callbacks

```ruby
describe 'callbacks' do
  describe 'before_save' do
    it 'normalizes phone number' do
      task = build(:task, phone: '(555) 123-4567')
      task.save
      expect(task.phone).to eq('+15551234567')
    end
  end

  describe 'after_create' do
    it 'creates initial timeline' do
      expect { create(:task) }
        .to change(Timeline, :count).by(1)
    end
  end
end
```

---

## Testing Class Methods

```ruby
describe '.by_status' do
  let!(:pending) { create(:task, status: 'pending') }
  let!(:completed) { create(:task, status: 'completed') }

  it 'filters by status' do
    expect(Task.by_status('pending')).to eq([pending])
  end
end

describe '.search' do
  let!(:task) { create(:task, description: 'Important delivery') }

  it 'searches description' do
    expect(Task.search('important')).to include(task)
  end
end
```
