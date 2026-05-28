# System Specs Reference

## Basic System Spec

```ruby
# spec/system/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Tasks", type: :system do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }

  before do
    driven_by(:selenium_chrome_headless)
    sign_in(user)
  end

  describe "viewing tasks" do
    let!(:tasks) { create_list(:task, 5, account: account) }

    it "displays all tasks" do
      visit tasks_path

      tasks.each do |task|
        expect(page).to have_content(task.tracking_number)
      end
    end
  end

  describe "creating a task" do
    let!(:merchant) { create(:merchant, account: account) }

    it "creates a new task" do
      visit new_task_path

      select merchant.name, from: "Merchant"
      fill_in "Description", with: "Test delivery"
      fill_in "Amount", with: "100.00"

      click_button "Create Task"

      expect(page).to have_content("Task created successfully")
      expect(page).to have_content("Test delivery")
    end
  end
end
```

---

## Testing with Turbo

```ruby
describe 'Turbo Streams' do
  it 'creates post without full page reload' do
    visit posts_path

    within '#new_post' do
      fill_in 'Title', with: 'My Turbo Post'
      click_button 'Create Post'
    end

    # Post appears without page reload
    expect(page).to have_content('My Turbo Post')
    expect(page).to have_current_path(posts_path) # No redirect
    expect(find_field('Title').value).to be_blank # Form reset
  end

  it 'updates post inline with Turbo Frame' do
    post = create(:post, title: 'Original')
    visit posts_path

    within "##{dom_id(post)}" do
      click_link 'Edit'
      fill_in 'Title', with: 'Updated'
      click_button 'Update'

      expect(page).to have_content('Updated')
      expect(page).not_to have_field('Title')
    end

    expect(page).to have_current_path(posts_path)
  end

  it 'removes post via Turbo Stream' do
    post = create(:post)
    visit posts_path

    within "##{dom_id(post)}" do
      accept_confirm { click_button 'Delete' }
    end

    expect(page).not_to have_selector("##{dom_id(post)}")
  end
end
```

---

## Turbo Helpers

```ruby
# spec/support/turbo_helpers.rb
module TurboHelpers
  def expect_turbo_stream(action:, target:)
    expect(page).to have_selector(
      "turbo-stream[action='#{action}'][target='#{target}']",
      visible: false
    )
  end

  def wait_for_turbo_frame(id, timeout: 5)
    expect(page).to have_selector("turbo-frame##{id}[complete]", wait: timeout)
  end

  def within_turbo_frame(id, &block)
    within("turbo-frame##{id}", &block)
  end
end

RSpec.configure do |config|
  config.include TurboHelpers, type: :system
end
```

---

## Testing Lazy-Loaded Frames

```ruby
describe 'lazy loading frames' do
  let!(:post) { create(:post) }

  it 'loads frame content when visible' do
    visit post_path(post)

    within 'turbo-frame#comments' do
      expect(page).to have_content('Loading comments...')
    end

    wait_for_turbo_frame('comments')

    within 'turbo-frame#comments' do
      expect(page).not_to have_content('Loading comments...')
      expect(page).to have_selector('.comment', count: post.comments.count)
    end
  end
end
```

---

## JavaScript Testing

```ruby
describe 'JavaScript interactions', js: true do
  it 'opens modal on click' do
    visit tasks_path

    click_button 'New Task'

    expect(page).to have_selector('.modal.open')
    within('.modal') do
      expect(page).to have_content('Create New Task')
    end
  end

  it 'autocompletes search' do
    create(:merchant, name: 'Acme Corp')
    visit tasks_path

    fill_in 'Search', with: 'Acm'

    expect(page).to have_selector('.autocomplete-item', text: 'Acme Corp')
  end
end
```

---

## File Uploads

```ruby
describe 'file upload' do
  it 'uploads an image' do
    visit new_task_path

    attach_file 'Photo', Rails.root.join('spec/fixtures/files/photo.jpg')
    click_button 'Create'

    expect(page).to have_selector('img[src*="photo.jpg"]')
  end
end
```
