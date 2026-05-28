# Background Jobs, Mailers & Action Cable

## ActionMailer

### Mailer Structure

```ruby
# app/mailers/user_mailer.rb
class UserMailer < ApplicationMailer
  default from: 'notifications@example.com'

  def welcome_email(user)
    @user = user
    @url = root_url

    mail(
      to: email_address_with_name(@user.email, @user.name),
      subject: 'Welcome to My App'
    )
  end

  def password_reset(user, token)
    @user = user
    @token = token
    @reset_url = edit_password_reset_url(token: @token)

    mail(to: @user.email, subject: 'Password Reset Instructions')
  end

  private

  def email_address_with_name(email, name)
    Mail::Address.new(email).tap { |a| a.display_name = name }.format
  end
end
```

### Mailer Previews

```ruby
# test/mailers/previews/user_mailer_preview.rb
class UserMailerPreview < ActionMailer::Preview
  def welcome_email
    UserMailer.welcome_email(User.first)
  end

  def password_reset
    user = User.first
    token = SecureRandom.urlsafe_base64
    UserMailer.password_reset(user, token)
  end
end

# Visit: http://localhost:3000/rails/mailers/user_mailer/welcome_email
```

### Delivery Methods

```ruby
# Asynchronous (recommended)
UserMailer.welcome_email(@user).deliver_later

# With delay
UserMailer.welcome_email(@user).deliver_later(wait: 1.hour)

# At specific time
UserMailer.welcome_email(@user).deliver_later(wait_until: Date.tomorrow.noon)

# Synchronous (avoid in production)
UserMailer.welcome_email(@user).deliver_now
```

---

## ActiveJob

### Job Structure

```ruby
# app/jobs/application_job.rb
class ApplicationJob < ActiveJob::Base
  retry_on StandardError, wait: :exponentially_longer, attempts: 5
  retry_on ActiveRecord::Deadlocked, wait: 5.seconds, attempts: 3
  discard_on ActiveJob::DeserializationError

  rescue_from(Exception) do |exception|
    ErrorTracker.notify(exception)
    raise exception
  end
end

# app/jobs/send_welcome_email_job.rb
class SendWelcomeEmailJob < ApplicationJob
  queue_as :mailers

  def perform(user)
    UserMailer.welcome_email(user).deliver_now
  end
end

# Usage
SendWelcomeEmailJob.perform_later(user)
```

### Sidekiq-Specific Options

```ruby
class ProcessOrderJob < ApplicationJob
  queue_as :orders

  sidekiq_options retry: 3,
                  backtrace: true,
                  dead: true

  def perform(order_id)
    order = Order.find(order_id)
    OrderProcessor.new(order).process!
  end
end
```

### Sidekiq Configuration

```yaml
# config/sidekiq.yml
:queues:
  - critical
  - default
  - mailers
  - low_priority

:schedule:
  daily_cleanup:
    cron: '0 0 * * *'  # Daily at midnight
    class: DailyCleanupJob
```

---

## Action Cable

### Connection Setup

```ruby
# app/channels/application_cable/connection.rb
module ApplicationCable
  class Connection < ActionCable::Connection::Base
    identified_by :current_user

    def connect
      self.current_user = find_verified_user
    end

    private

    def find_verified_user
      if verified_user = User.find_by(id: cookies.encrypted[:user_id])
        verified_user
      else
        reject_unauthorized_connection
      end
    end
  end
end
```

### Channel Structure

```ruby
# app/channels/chat_channel.rb
class ChatChannel < ApplicationCable::Channel
  def subscribed
    stream_from "chat_#{params[:room_id]}"
  end

  def unsubscribed
    stop_all_streams
  end

  def speak(data)
    message = current_user.messages.create!(
      content: data['message'],
      room_id: params[:room_id]
    )

    ActionCable.server.broadcast(
      "chat_#{params[:room_id]}",
      message: render_message(message)
    )
  end

  private

  def render_message(message)
    ApplicationController.render(
      partial: 'messages/message',
      locals: { message: message }
    )
  end
end
```

### Client-Side JavaScript

```javascript
// app/javascript/channels/chat_channel.js
import consumer from "./consumer"

consumer.subscriptions.create(
  { channel: "ChatChannel", room_id: roomId },
  {
    connected() {
      console.log("Connected to chat")
    },

    disconnected() {
      console.log("Disconnected from chat")
    },

    received(data) {
      const messages = document.getElementById('messages')
      messages.insertAdjacentHTML('beforeend', data.message)
    },

    speak(message) {
      this.perform('speak', { message: message })
    }
  }
)
```

### Broadcasting from Models

```ruby
class Message < ApplicationRecord
  belongs_to :user
  belongs_to :room

  after_create_commit :broadcast_message

  private

  def broadcast_message
    broadcast_append_to(
      [room, :messages],
      target: "messages",
      partial: "messages/message",
      locals: { message: self }
    )
  end
end
```

---

## Testing Jobs and Mailers

### Job Testing

```ruby
RSpec.describe SendWelcomeEmailJob, type: :job do
  include ActiveJob::TestHelper

  let(:user) { create(:user) }

  it 'enqueues the job' do
    expect {
      SendWelcomeEmailJob.perform_later(user)
    }.to have_enqueued_job(SendWelcomeEmailJob).with(user)
  end

  it 'sends welcome email' do
    expect {
      perform_enqueued_jobs do
        SendWelcomeEmailJob.perform_later(user)
      end
    }.to change { ActionMailer::Base.deliveries.count }.by(1)
  end
end
```

### Mailer Testing

```ruby
RSpec.describe UserMailer, type: :mailer do
  describe '#welcome_email' do
    let(:user) { create(:user, email: 'user@example.com') }
    let(:mail) { UserMailer.welcome_email(user) }

    it 'renders the subject' do
      expect(mail.subject).to eq('Welcome to My App')
    end

    it 'renders the receiver email' do
      expect(mail.to).to eq([user.email])
    end

    it 'contains user name' do
      expect(mail.body.encoded).to match(user.name)
    end
  end
end
```

### Channel Testing

```ruby
RSpec.describe ChatChannel, type: :channel do
  let(:user) { create(:user) }
  let(:room) { create(:room) }

  before do
    stub_connection(current_user: user)
  end

  it 'successfully subscribes' do
    subscribe(room_id: room.id)
    expect(subscription).to be_confirmed
    expect(subscription).to have_stream_from("chat_#{room.id}")
  end

  it 'broadcasts messages' do
    subscribe(room_id: room.id)

    expect {
      perform :speak, message: 'Hello'
    }.to have_broadcasted_to("chat_#{room.id}")
  end
end
```
