# Request Specs Reference

## Basic Request Spec

```ruby
# spec/requests/api/v1/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Api::V1::Tasks", type: :request do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }
  let(:headers) { auth_headers(user) }

  describe "GET /api/v1/tasks" do
    let!(:tasks) { create_list(:task, 3, account: account) }
    let!(:other_task) { create(:task) }

    before { get api_v1_tasks_path, headers: headers }

    it "returns success" do
      expect(response).to have_http_status(:ok)
    end

    it "returns tasks for current account only" do
      expect(json_response['data'].size).to eq(3)
    end

    it "does not include other account tasks" do
      ids = json_response['data'].pluck('id')
      expect(ids).not_to include(other_task.id)
    end
  end

  describe "POST /api/v1/tasks" do
    let(:merchant) { create(:merchant, account: account) }
    let(:valid_params) do
      { task: { merchant_id: merchant.id, description: "New task" } }
    end

    context "with valid params" do
      it "creates a task" do
        expect {
          post api_v1_tasks_path, params: valid_params, headers: headers
        }.to change(Task, :count).by(1)
      end

      it "returns created status" do
        post api_v1_tasks_path, params: valid_params, headers: headers
        expect(response).to have_http_status(:created)
      end
    end

    context "with invalid params" do
      let(:invalid_params) { { task: { description: "" } } }

      it "returns unprocessable entity" do
        post api_v1_tasks_path, params: invalid_params, headers: headers
        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end

  def json_response
    JSON.parse(response.body)
  end
end
```

---

## Testing Pagination

```ruby
describe 'GET /api/v1/posts' do
  before { create_list(:post, 30) }

  it 'includes pagination metadata' do
    get '/api/v1/posts', params: { page: 2, per_page: 10 }, headers: auth_headers

    expect(json_response['meta']).to include(
      'current_page' => 2,
      'total_pages' => 3,
      'total_count' => 30,
      'per_page' => 10
    )
  end
end
```

---

## Testing Rate Limiting

```ruby
# spec/requests/api/rate_limiting_spec.rb
RSpec.describe 'API Rate Limiting', type: :request do
  let(:user) { create(:user) }
  let(:auth_headers) { { 'Authorization' => "Bearer #{user.jwt_token}" } }

  before do
    Rack::Attack.cache.store = ActiveSupport::Cache::MemoryStore.new
    Rack::Attack.enabled = true
  end

  after do
    Rack::Attack.cache.store.clear
  end

  it 'throttles requests exceeding limit' do
    11.times { get '/api/v1/posts', headers: auth_headers }

    expect(response).to have_http_status(:too_many_requests)
    expect(response.headers['Retry-After']).to be_present
  end
end
```

---

## Testing API Versioning

```ruby
describe 'v1 endpoint' do
  it 'returns v1 response format' do
    get '/api/v1/posts', headers: auth_headers

    expect(json_response).to have_key('posts')
    expect(json_response).to have_key('meta')
  end
end

describe 'v2 endpoint' do
  it 'returns v2 response format' do
    get '/api/v2/posts', headers: auth_headers

    expect(json_response).to have_key('data')
    expect(json_response).to have_key('pagination')
  end
end
```

---

## Testing Authentication

```ruby
context 'without authentication' do
  it 'returns 401 unauthorized' do
    get '/api/v1/posts'
    expect(response).to have_http_status(:unauthorized)
  end
end

context 'with invalid token' do
  it 'returns 401 unauthorized' do
    get '/api/v1/posts', headers: { 'Authorization' => 'Bearer invalid' }
    expect(response).to have_http_status(:unauthorized)
  end
end
```

---

## Testing Authorization

```ruby
context 'when user is not post author' do
  let(:other_post) { create(:post) }

  it 'returns 403 forbidden' do
    patch "/api/v1/posts/#{other_post.id}",
          params: { post: { title: 'Updated' } }.to_json,
          headers: auth_headers

    expect(response).to have_http_status(:forbidden)
  end
end
```
