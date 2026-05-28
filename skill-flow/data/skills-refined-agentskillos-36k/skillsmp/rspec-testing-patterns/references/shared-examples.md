# Shared Examples & Contexts Reference

## Shared Examples

### Tenant Scoping

```ruby
# spec/support/shared_examples/tenant_scoped.rb
RSpec.shared_examples "tenant scoped" do
  describe "tenant scoping" do
    let(:account) { create(:account) }
    let(:other_account) { create(:account) }

    let!(:scoped_record) { create(described_class.model_name.singular, account: account) }
    let!(:other_record) { create(described_class.model_name.singular, account: other_account) }

    it "scopes to current account" do
      Current.account = account
      expect(described_class.all).to include(scoped_record)
      expect(described_class.all).not_to include(other_record)
    end
  end
end

# Usage
RSpec.describe Task do
  it_behaves_like "tenant scoped"
end
```

### API Authentication

```ruby
# spec/support/shared_examples/api_authentication.rb
RSpec.shared_examples "requires authentication" do
  context "without authentication" do
    let(:headers) { {} }

    it "returns unauthorized" do
      make_request
      expect(response).to have_http_status(:unauthorized)
    end
  end
end

# Usage
RSpec.describe "Api::V1::Tasks" do
  describe "GET /api/v1/tasks" do
    it_behaves_like "requires authentication" do
      let(:make_request) { get api_v1_tasks_path, headers: headers }
    end
  end
end
```

### Pagination

```ruby
RSpec.shared_examples 'paginates results' do
  it 'includes pagination metadata' do
    make_request

    expect(json_response['meta']).to include(
      'current_page',
      'total_pages',
      'total_count',
      'per_page'
    )
  end

  it 'respects per_page parameter' do
    make_request(per_page: 5)

    expect(json_response['meta']['per_page']).to eq(5)
    expect(json_response[collection_key].size).to be <= 5
  end
end
```

### Service Results

```ruby
RSpec.shared_examples 'a successful service' do
  it 'returns success result' do
    expect(result).to be_success
  end

  it 'has no error' do
    expect(result.error).to be_nil
  end
end

RSpec.shared_examples 'a failed service' do |expected_error|
  it 'returns failure result' do
    expect(result).to be_failure
  end

  if expected_error
    it "returns error: #{expected_error}" do
      expect(result.error).to eq(expected_error)
    end
  end
end
```

---

## Shared Contexts

### Authenticated User

```ruby
# spec/support/shared_contexts/authenticated_user.rb
RSpec.shared_context "authenticated user" do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }

  before do
    sign_in(user)
    Current.account = account
  end
end

# Usage
RSpec.describe TasksController do
  include_context "authenticated user"

  # tests with authenticated user...
end
```

### Frozen Time

```ruby
RSpec.shared_context "frozen time" do
  let(:frozen_time) { Time.zone.parse('2024-01-15 10:00:00') }

  around do |example|
    travel_to(frozen_time) { example.run }
  end
end

# Usage
RSpec.describe Task do
  include_context "frozen time"

  it 'sets created_at to current time' do
    task = create(:task)
    expect(task.created_at).to eq(frozen_time)
  end
end
```

### API Headers

```ruby
RSpec.shared_context "api headers" do
  let(:user) { create(:user) }
  let(:auth_headers) do
    {
      'Authorization' => "Bearer #{user.jwt_token}",
      'Content-Type' => 'application/json',
      'Accept' => 'application/json'
    }
  end
end
```

---

## Metadata-Based Inclusion

```ruby
# spec/rails_helper.rb
RSpec.configure do |config|
  config.include_context "authenticated user", type: :controller
  config.include_context "api headers", type: :request
end
```
