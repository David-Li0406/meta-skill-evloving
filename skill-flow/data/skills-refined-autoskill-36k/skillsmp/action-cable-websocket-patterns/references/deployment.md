# Action Cable Production Deployment

## Nginx Configuration

```nginx
# /etc/nginx/sites-enabled/myapp
upstream cable {
  server localhost:28080;
}

map $http_upgrade $connection_upgrade {
  default upgrade;
  '' close;
}

server {
  listen 443 ssl;
  server_name example.com;

  location /cable {
    proxy_pass http://cable;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;

    # WebSocket specific timeouts
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
  }
}
```

## Rails Production Configuration

```ruby
# config/environments/production.rb
Rails.application.configure do
  # WebSocket URL (must be wss:// for HTTPS)
  config.action_cable.url = ENV.fetch('ACTION_CABLE_URL') { 'wss://example.com/cable' }

  # Allowed origins (security!)
  config.action_cable.allowed_request_origins = [
    'https://example.com',
    'https://www.example.com',
    /https:\/\/.*\.example\.com/  # Regex for subdomains
  ]

  # Disable request forgery protection for Action Cable
  config.action_cable.disable_request_forgery_protection = true

  # Mount Action Cable separately (recommended for scaling)
  config.action_cable.mount_path = nil
end
```

## Cable.yml Configuration

```yaml
# config/cable.yml
development:
  adapter: redis
  url: redis://localhost:6379/1

test:
  adapter: test

production:
  adapter: redis
  url: <%= ENV.fetch("REDIS_URL") { "redis://localhost:6379/1" } %>
  channel_prefix: myapp_production
```

## Standalone Action Cable Server

```ruby
# cable/config.ru
require_relative '../config/environment'

Rails.application.eager_load!

run ActionCable.server
```

```bash
# Run standalone cable server
bundle exec puma -p 28080 cable/config.ru
```

## Docker Configuration

```dockerfile
# Dockerfile.cable
FROM ruby:3.2-slim

WORKDIR /app
COPY Gemfile* ./
RUN bundle install --without development test

COPY . .

EXPOSE 28080
CMD ["bundle", "exec", "puma", "-p", "28080", "cable/config.ru"]
```

```yaml
# docker-compose.yml
services:
  cable:
    build:
      context: .
      dockerfile: Dockerfile.cable
    ports:
      - "28080:28080"
    environment:
      - REDIS_URL=redis://redis:6379/1
      - RAILS_ENV=production
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## Scaling Considerations

### Horizontal Scaling

Action Cable requires Redis adapter for multi-server deployments:

```ruby
# All servers broadcast to Redis, all servers receive from Redis
ActionCable.server.broadcast("posts", data)
# ↓
# Redis pub/sub
# ↓
# All connected servers receive and forward to their clients
```

### Connection Limits

```ruby
# Monitor connections
ActionCable.server.connections.count

# Limit connections per server (optional)
# config/initializers/action_cable.rb
ActionCable.server.config.connection_class = -> {
  ApplicationCable::Connection
}
```

### Memory Considerations

Each WebSocket connection uses ~50KB of memory. Plan capacity accordingly:

- 1000 connections ≈ 50MB
- 10000 connections ≈ 500MB
- 100000 connections ≈ 5GB

## Monitoring

```ruby
# config/initializers/action_cable_monitoring.rb
ActiveSupport::Notifications.subscribe 'perform_action.action_cable' do |*args|
  event = ActiveSupport::Notifications::Event.new(*args)
  Rails.logger.info "Action Cable: #{event.payload[:channel_class]}##{event.payload[:action]} (#{event.duration.round(1)}ms)"
end

ActiveSupport::Notifications.subscribe 'transmit.action_cable' do |*args|
  event = ActiveSupport::Notifications::Event.new(*args)
  StatsD.increment 'action_cable.transmit'
end
```

## Health Check

```ruby
# app/controllers/health_controller.rb
class HealthController < ApplicationController
  def cable
    # Check Redis connection
    Redis.current.ping

    # Check ActionCable is running
    render json: {
      status: 'ok',
      connections: ActionCable.server.connections.count
    }
  rescue Redis::CannotConnectError => e
    render json: { status: 'error', message: e.message }, status: 503
  end
end
```
