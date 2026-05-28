# Testing Guide for Rails

This guide defines testing strategies and what makes a meaningful test.

## Table of Contents

- [Testing Principles](#testing-principles)
- [What NOT to Test](#what-not-to-test)
- [What TO Test](#what-to-test)
- [RSpec Examples](#rspec-examples)
- [Minitest Examples](#minitest-examples)

## Testing Principles

### Core Principles

1. **Test behavior, not implementation**
   - Focus on what the code does, not how it does it
   - Tests should describe the expected outcomes

2. **Test meaningful logic only**
   - Avoid testing framework features (Rails validations, associations)
   - Test custom business logic and edge cases

3. **Keep tests simple and readable**
   - One assertion concept per test
   - Clear test names that describe the scenario

4. **Avoid brittle tests**
   - Don't test private methods directly
   - Don't test constants or simple attribute accessors

## What NOT to Test

### ❌ Avoid These Tests

**1. Constant Value Checks**
```ruby
# ❌ BAD - Meaningless test
it 'has correct constant value' do
  expect(Article::MAX_TITLE_LENGTH).to eq 255
end
```

**2. Simple Attribute Accessors**
```ruby
# ❌ BAD - Rails already tests this
it 'has a title attribute' do
  article = Article.new(title: 'Test')
  expect(article.title).to eq 'Test'
end
```

**3. Framework Features**
```ruby
# ❌ BAD - Testing Rails validations without custom logic
it { should validate_presence_of(:title) }
it { should belong_to(:user) }
```

**4. Private Methods Directly**
```ruby
# ❌ BAD - Test public interface instead
it 'calls private method' do
  expect(article.send(:format_title)).to eq 'Title'
end
```

**5. Database Schema**
```ruby
# ❌ BAD - Schema is tested by migrations
it 'has a title column' do
  expect(Article.column_names).to include('title')
end
```

## What TO Test

### ✅ Write These Tests

**1. Custom Business Logic**
```ruby
# ✅ GOOD - Tests custom method behavior
describe '#published?' do
  it 'returns true when published_at is in the past' do
    article = Article.new(published_at: 1.day.ago)
    expect(article.published?).to be true
  end

  it 'returns false when published_at is in the future' do
    article = Article.new(published_at: 1.day.from_now)
    expect(article.published?).to be false
  end

  it 'returns false when published_at is nil' do
    article = Article.new(published_at: nil)
    expect(article.published?).to be false
  end
end
```

**2. Complex Validations with Custom Logic**
```ruby
# ✅ GOOD - Tests custom validation logic
describe 'custom validations' do
  it 'allows title to be blank if article is draft' do
    article = Article.new(title: '', status: 'draft')
    expect(article).to be_valid
  end

  it 'requires title when article is published' do
    article = Article.new(title: '', status: 'published')
    expect(article).not_to be_valid
    expect(article.errors[:title]).to include("can't be blank")
  end
end
```

**3. Scopes with Complex Logic**
```ruby
# ✅ GOOD - Tests scope behavior
describe '.recent' do
  it 'returns articles from the last 7 days' do
    old_article = create(:article, created_at: 10.days.ago)
    recent_article = create(:article, created_at: 3.days.ago)

    expect(Article.recent).to include(recent_article)
    expect(Article.recent).not_to include(old_article)
  end
end
```

**4. Callbacks with Side Effects**
```ruby
# ✅ GOOD - Tests callback behavior
describe 'callbacks' do
  it 'sends notification email after publishing' do
    article = create(:article, status: 'draft')

    expect {
      article.update(status: 'published')
    }.to have_enqueued_job(SendNotificationJob).with(article)
  end
end
```

**5. Controller Actions**
```ruby
# ✅ GOOD - Tests controller behavior
describe 'POST #create' do
  context 'with valid parameters' do
    it 'creates a new article' do
      expect {
        post :create, params: { article: valid_attributes }
      }.to change(Article, :count).by(1)
    end

    it 'redirects to the created article' do
      post :create, params: { article: valid_attributes }
      expect(response).to redirect_to(Article.last)
    end
  end

  context 'with invalid parameters' do
    it 'does not create a new article' do
      expect {
        post :create, params: { article: invalid_attributes }
      }.not_to change(Article, :count)
    end

    it 'renders new template with unprocessable entity status' do
      post :create, params: { article: invalid_attributes }
      expect(response).to have_http_status(:unprocessable_entity)
      expect(response).to render_template(:new)
    end
  end
end
```

**6. Service Objects / POROs**
```ruby
# ✅ GOOD - Tests service object logic
describe ArticlePublisher do
  describe '#publish' do
    it 'sets published_at to current time' do
      article = create(:article, published_at: nil)
      publisher = ArticlePublisher.new(article)

      publisher.publish

      expect(article.published_at).to be_within(1.second).of(Time.current)
    end

    it 'notifies subscribers' do
      article = create(:article)
      publisher = ArticlePublisher.new(article)

      expect {
        publisher.publish
      }.to have_enqueued_job(NotifySubscribersJob)
    end
  end
end
```

## RSpec Examples

### Model Tests

```ruby
# spec/models/article_spec.rb
require 'rails_helper'

RSpec.describe Article, type: :model do
  describe '#to_param' do
    it 'returns slug when present' do
      article = Article.new(id: 1, slug: 'my-article')
      expect(article.to_param).to eq 'my-article'
    end

    it 'returns id when slug is nil' do
      article = Article.new(id: 1, slug: nil)
      expect(article.to_param).to eq '1'
    end
  end

  describe '#excerpt' do
    it 'returns first 100 characters when body is longer' do
      article = Article.new(body: 'a' * 150)
      expect(article.excerpt).to eq('a' * 100 + '...')
    end

    it 'returns full body when shorter than 100 characters' do
      article = Article.new(body: 'Short body')
      expect(article.excerpt).to eq 'Short body'
    end
  end
end
```

### Controller Tests

```ruby
# spec/controllers/articles_controller_spec.rb
require 'rails_helper'

RSpec.describe ArticlesController, type: :controller do
  let(:user) { create(:user) }
  let(:article) { create(:article, user: user) }

  before { sign_in user }

  describe 'GET #index' do
    it 'assigns all articles to @articles' do
      article1 = create(:article)
      article2 = create(:article)

      get :index

      expect(assigns(:articles)).to match_array([article1, article2])
    end
  end

  describe 'DELETE #destroy' do
    it 'destroys the article' do
      article_to_delete = create(:article, user: user)

      expect {
        delete :destroy, params: { id: article_to_delete.id }
      }.to change(Article, :count).by(-1)
    end

    context 'when user does not own the article' do
      it 'does not destroy the article' do
        other_article = create(:article, user: create(:user))

        expect {
          delete :destroy, params: { id: other_article.id }
        }.not_to change(Article, :count)
      end
    end
  end
end
```

### Request Tests (Preferred over Controller Tests)

```ruby
# spec/requests/articles_spec.rb
require 'rails_helper'

RSpec.describe 'Articles', type: :request do
  let(:user) { create(:user) }

  before { sign_in user }

  describe 'POST /articles' do
    context 'with valid parameters' do
      let(:valid_params) { { article: { title: 'Test', body: 'Content' } } }

      it 'creates a new article' do
        expect {
          post articles_path, params: valid_params
        }.to change(Article, :count).by(1)
      end

      it 'returns success response' do
        post articles_path, params: valid_params
        expect(response).to have_http_status(:redirect)
      end
    end

    context 'with invalid parameters' do
      let(:invalid_params) { { article: { title: '' } } }

      it 'does not create an article' do
        expect {
          post articles_path, params: invalid_params
        }.not_to change(Article, :count)
      end

      it 'returns unprocessable entity status' do
        post articles_path, params: invalid_params
        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end
end
```

## Minitest Examples

### Model Tests

```ruby
# test/models/article_test.rb
require 'test_helper'

class ArticleTest < ActiveSupport::TestCase
  test "excerpt returns first 100 characters when body is longer" do
    article = Article.new(body: 'a' * 150)
    assert_equal 'a' * 100 + '...', article.excerpt
  end

  test "excerpt returns full body when shorter than 100 characters" do
    article = Article.new(body: 'Short body')
    assert_equal 'Short body', article.excerpt
  end

  test "published? returns true when published_at is in the past" do
    article = Article.new(published_at: 1.day.ago)
    assert article.published?
  end

  test "published? returns false when published_at is in the future" do
    article = Article.new(published_at: 1.day.from_now)
    assert_not article.published?
  end
end
```

### Controller Tests

```ruby
# test/controllers/articles_controller_test.rb
require 'test_helper'

class ArticlesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @user = users(:one)
    @article = articles(:one)
    sign_in @user
  end

  test "should get index" do
    get articles_url
    assert_response :success
  end

  test "should create article with valid params" do
    assert_difference('Article.count', 1) do
      post articles_url, params: { article: { title: 'Test', body: 'Content' } }
    end

    assert_redirected_to article_url(Article.last)
  end

  test "should not create article with invalid params" do
    assert_no_difference('Article.count') do
      post articles_url, params: { article: { title: '' } }
    end

    assert_response :unprocessable_entity
  end

  test "should destroy own article" do
    assert_difference('Article.count', -1) do
      delete article_url(@article)
    end

    assert_redirected_to articles_url
  end
end
```

### System Tests

```ruby
# test/system/articles_test.rb
require 'application_system_test_case'

class ArticlesTest < ApplicationSystemTestCase
  setup do
    @user = users(:one)
    sign_in @user
  end

  test "creating an article" do
    visit articles_url
    click_on 'New Article'

    fill_in 'Title', with: 'My New Article'
    fill_in 'Body', with: 'This is the article content'
    click_on 'Create Article'

    assert_text 'Article was successfully created'
    assert_text 'My New Article'
  end

  test "updating an article" do
    article = articles(:one)
    visit article_url(article)
    click_on 'Edit'

    fill_in 'Title', with: 'Updated Title'
    click_on 'Update Article'

    assert_text 'Article was successfully updated'
    assert_text 'Updated Title'
  end
end
```
