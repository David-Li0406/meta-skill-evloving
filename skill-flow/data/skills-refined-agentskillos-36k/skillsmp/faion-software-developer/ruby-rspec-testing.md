---
id: ruby-rspec-testing
name: "RSpec Testing"
domain: RUBY
skill: faion-software-developer
category: "backend"
---

## RSpec Testing

### Problem
Write comprehensive, maintainable tests.

### Framework: Model Specs

```ruby
# spec/models/user_spec.rb
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
    it { is_expected.to validate_length_of(:name).is_at_least(2).is_at_most(100) }
  end

  describe 'associations' do
    it { is_expected.to have_one(:profile).dependent(:destroy) }
    it { is_expected.to have_many(:orders).dependent(:nullify) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:active_user) { create(:user, active: true) }
      let!(:inactive_user) { create(:user, active: false) }

      it 'returns only active users' do
        expect(User.active).to eq([active_user])
      end
    end
  end

  describe '#full_name' do
    let(:user) { build(:user, first_name: 'John', last_name: 'Doe') }

    it 'returns combined first and last name' do
      expect(user.full_name).to eq('John Doe')
    end
  end
end
```

### Service Specs

```ruby
# spec/services/users/create_service_spec.rb
require 'rails_helper'

RSpec.describe Users::CreateService do
  describe '#call' do
    subject(:service) { described_class.new(params: params) }

    context 'with valid params' do
      let(:params) { { name: 'John', email: 'john@example.com', password: 'secret123' } }

      it 'creates a user' do
        expect { service.call }.to change(User, :count).by(1)
      end

      it 'returns success result' do
        result = service.call
        expect(result).to be_success
        expect(result.data).to be_a(User)
      end

      it 'sends welcome email' do
        expect { service.call }
          .to have_enqueued_mail(UserMailer, :welcome)
      end
    end

    context 'with invalid params' do
      let(:params) { { name: '', email: 'invalid' } }

      it 'does not create a user' do
        expect { service.call }.not_to change(User, :count)
      end

      it 'returns failure result with errors' do
        result = service.call
        expect(result).to be_failure
        expect(result.errors).to include(/Email/)
      end
    end
  end
end
```

### Agent

faion-backend-agent
