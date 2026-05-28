---
name: logging-setup
description: Setup structured logging, performance monitoring, and error tracking. Use when user needs logging system, error tracking, performance monitoring, or says "setup logging", "add error tracking", "monitor performance", "log requests", "structured logs".
---

# Logging & Monitoring Setup

프로덕션급 로깅 시스템, 성능 모니터링, 에러 추적을 설정합니다.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Install Lograge (structured logging)
- [ ] 2. Configure log formats (dev/prod)
- [ ] 3. Setup custom loggers
- [ ] 4. Add performance tracking
- [ ] 5. Configure error tracking (optional)
- [ ] 6. Test logging output
```

## Core Components

### 1. Lograge (구조화된 로깅)

**설치**:
```ruby
# Gemfile
gem 'lograge'
```

**설정** (config/environments/production.rb):
```ruby
# Lograge 활성화
config.lograge.enabled = true

# JSON 포맷
config.lograge.formatter = Lograge::Formatters::Json.new

# 커스텀 필드 추가
config.lograge.custom_options = lambda do |event|
  {
    user_id: event.payload[:user_id],
    ip: event.payload[:ip],
    host: event.payload[:host],
    params: event.payload[:params].except('controller', 'action')
  }
end

# 무시할 경로
config.lograge.ignore_actions = ['HealthController#check']
```

**결과 예시**:
```json
{
  "method": "GET",
  "path": "/posts/123",
  "format": "html",
  "controller": "PostsController",
  "action": "show",
  "status": 200,
  "duration": 45.23,
  "view": 32.12,
  "db": 8.45,
  "user_id": 456,
  "ip": "192.168.1.1"
}
```

### 2. Custom Loggers

**비즈니스 이벤트 로거**:
```ruby
# app/services/loggers/business_logger.rb
module Loggers
  class BusinessLogger
    def self.log_event(event_type, details = {})
      Rails.logger.info({
        event: event_type,
        timestamp: Time.current.iso8601,
        environment: Rails.env,
        **details
      }.to_json)
    end

    def self.log_user_action(user, action, resource = nil)
      log_event('user_action', {
        user_id: user.id,
        action: action,
        resource_type: resource&.class&.name,
        resource_id: resource&.id
      })
    end

    def self.log_error(error, context = {})
      log_event('error', {
        error_class: error.class.name,
        error_message: error.message,
        backtrace: error.backtrace&.first(5),
        **context
      })
    end
  end
end
```

**사용 예시**:
```ruby
# In controller
Loggers::BusinessLogger.log_user_action(
  current_user,
  'created_post',
  @post
)

# In service
Loggers::BusinessLogger.log_event('payment_processed', {
  order_id: order.id,
  amount: order.amount,
  payment_method: payment.method
})
```

### 3. Performance Tracking

**요청 성능 모니터링**:
```ruby
# app/controllers/concerns/request_logger.rb
module RequestLogger
  extend ActiveSupport::Concern

  included do
    around_action :log_request_performance
  end

  private

  def log_request_performance
    start_time = Time.current

    yield

    duration = Time.current - start_time

    Rails.logger.info({
      type: 'request_performance',
      controller: controller_name,
      action: action_name,
      duration_ms: (duration * 1000).round(2),
      user_id: current_user&.id,
      status: response.status,
      path: request.fullpath,
      method: request.method
    }.to_json)

    # 느린 요청 경고
    if duration > 1.0
      Rails.logger.warn "Slow request detected: #{duration}s for #{request.fullpath}"
    end
  end
end

# In ApplicationController
class ApplicationController < ActionController::Base
  include RequestLogger
end
```

**데이터베이스 쿼리 추적**:
```ruby
# config/initializers/query_logger.rb
if Rails.env.development?
  ActiveSupport::Notifications.subscribe('sql.active_record') do |name, start, finish, id, payload|
    duration = (finish - start) * 1000

    if duration > 100 # 100ms 이상
      Rails.logger.warn({
        type: 'slow_query',
        duration_ms: duration.round(2),
        sql: payload[:sql],
        name: payload[:name]
      }.to_json)
    end
  end
end
```

### 4. 환경별 로그 설정

**Development (개발 환경)**:
```ruby
# config/environments/development.rb
config.log_level = :debug
config.log_formatter = Logger::Formatter.new

# 콘솔에 색상 출력
config.colorize_logging = true

# SQL 쿼리 로깅
config.active_record.verbose_query_logs = true
```

**Production (프로덕션)**:
```ruby
# config/environments/production.rb
config.log_level = :info
config.log_formatter = Logger::Formatter.new

# JSON 포맷으로 로그 출력
config.lograge.enabled = true
config.lograge.formatter = Lograge::Formatters::Json.new

# 로그 파일 로테이션
config.logger = ActiveSupport::Logger.new(
  Rails.root.join('log', "#{Rails.env}.log"),
  10,           # 10개 파일 유지
  10.megabytes  # 각 파일 최대 10MB
)
```

### 5. 에러 추적 (Sentry/Rollbar)

**Sentry 설정** (optional):
```ruby
# Gemfile
gem 'sentry-ruby'
gem 'sentry-rails'

# config/initializers/sentry.rb
Sentry.init do |config|
  config.dsn = ENV['SENTRY_DSN']
  config.breadcrumbs_logger = [:active_support_logger, :http_logger]

  # 환경 설정
  config.environment = Rails.env
  config.enabled_environments = %w[production staging]

  # 샘플링 레이트 (프로덕션 트래픽의 10%만 전송)
  config.traces_sample_rate = 0.1

  # 필터링
  config.excluded_exceptions += ['ActiveRecord::RecordNotFound']
end
```

**수동 에러 캡처**:
```ruby
begin
  risky_operation
rescue => e
  Sentry.capture_exception(e, {
    extra: {
      user_id: current_user&.id,
      context: 'payment_processing'
    }
  })
  raise
end
```

### 6. API 요청 로깅

```ruby
# app/controllers/api/v1/base_controller.rb
module Api
  module V1
    class BaseController < ApplicationController
      after_action :log_api_request

      private

      def log_api_request
        Rails.logger.info({
          type: 'api_request',
          method: request.method,
          path: request.fullpath,
          controller: controller_name,
          action: action_name,
          status: response.status,
          user_id: current_api_user&.id,
          ip: request.remote_ip,
          user_agent: request.user_agent,
          duration_ms: (Time.current - @request_start_time) * 1000
        }.to_json)
      end
    end
  end
end
```

### 7. Background Job 로깅

```ruby
# app/jobs/application_job.rb
class ApplicationJob < ActiveJob::Base
  around_perform :log_job_performance

  private

  def log_job_performance
    start_time = Time.current
    job_id = job_id

    Rails.logger.info({
      type: 'job_started',
      job: self.class.name,
      job_id: job_id,
      queue: queue_name
    }.to_json)

    yield

    duration = Time.current - start_time
    Rails.logger.info({
      type: 'job_completed',
      job: self.class.name,
      job_id: job_id,
      duration_ms: (duration * 1000).round(2),
      status: 'success'
    }.to_json)
  rescue => e
    Rails.logger.error({
      type: 'job_failed',
      job: self.class.name,
      job_id: job_id,
      error: e.class.name,
      message: e.message
    }.to_json)

    raise
  end
end
```

## 로그 분석 도구

### 로그 검색 (로컬)

**JSON 로그 파싱**:
```bash
# 특정 사용자의 요청
cat log/production.log | grep '"user_id":123'

# 느린 요청 찾기
cat log/production.log | grep '"duration"' | awk -F'"duration":' '{print $2}' | awk -F',' '{if($1>1000) print}'

# 에러 필터링
cat log/production.log | grep '"status":[45]'

# 최근 100줄
tail -n 100 log/production.log

# 실시간 모니터링
tail -f log/production.log | grep ERROR
```

### 로그 대시보드 (프로덕션)

**권장 도구**:
1. **ELK Stack** (Elasticsearch, Logstash, Kibana)
2. **Splunk**
3. **Datadog**
4. **CloudWatch** (AWS)
5. **Google Cloud Logging** (GCP)

## Best Practices

### 1. 로그 레벨 사용
```ruby
Rails.logger.debug "상세한 디버그 정보"      # 개발 전용
Rails.logger.info "일반 정보 (요청, 이벤트)"  # 주요 로그
Rails.logger.warn "경고 (느린 쿼리, 잠재적 문제)"
Rails.logger.error "에러 (예외, 실패)"
Rails.logger.fatal "치명적 에러 (앱 종료)"
```

### 2. 민감 정보 필터링
```ruby
# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :password,
  :password_confirmation,
  :token,
  :api_key,
  :secret,
  :credit_card
]
```

### 3. 구조화된 로그
```ruby
# ❌ 나쁜 예
Rails.logger.info "User #{user.id} created post #{post.id}"

# ✅ 좋은 예
Rails.logger.info({
  event: 'post_created',
  user_id: user.id,
  post_id: post.id,
  timestamp: Time.current.iso8601
}.to_json)
```

### 4. 컨텍스트 추가
```ruby
# config/application.rb
config.log_tags = [
  :request_id,
  -> request { request.remote_ip }
]
```

## Integration Examples

### Controller에서
```ruby
class PostsController < ApplicationController
  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      Loggers::BusinessLogger.log_user_action(
        current_user,
        'created_post',
        @post
      )
      redirect_to @post
    else
      Rails.logger.warn({
        event: 'post_creation_failed',
        user_id: current_user.id,
        errors: @post.errors.full_messages
      }.to_json)
      render :new
    end
  end
end
```

### Service에서
```ruby
class ProcessPaymentService
  def call
    Rails.logger.info({
      event: 'payment_processing_started',
      order_id: @order.id,
      amount: @order.amount
    }.to_json)

    result = charge_gateway

    if result.success?
      Rails.logger.info({
        event: 'payment_successful',
        order_id: @order.id,
        transaction_id: result.transaction_id
      }.to_json)
    else
      Rails.logger.error({
        event: 'payment_failed',
        order_id: @order.id,
        error: result.error_message
      }.to_json)
    end

    result
  end
end
```

### Query에서
```ruby
class PostsQuery
  def call
    start_time = Time.current
    result = @relation.to_a
    duration = Time.current - start_time

    Rails.logger.debug({
      query: 'posts_query',
      filters: @filters,
      count: result.size,
      duration_ms: (duration * 1000).round(2)
    }.to_json)

    result
  end
end
```

## Monitoring Checklist

- [ ] Lograge 설치 및 설정
- [ ] JSON 포맷 로그 활성화
- [ ] 환경별 로그 레벨 설정
- [ ] 민감 정보 필터링
- [ ] Custom loggers 생성
- [ ] 성능 추적 추가
- [ ] 에러 추적 설정 (optional)
- [ ] 로그 로테이션 설정
- [ ] 로그 분석 도구 선택
- [ ] 프로덕션 테스트

## Troubleshooting

**로그가 JSON으로 출력되지 않음**:
- Lograge 설정 확인
- `config.lograge.enabled = true` 확인

**로그 파일이 너무 큼**:
- 로그 로테이션 설정
- `ActiveSupport::Logger.new` with rotation

**느린 요청 찾기 어려움**:
- `log_request_performance` concern 추가
- 임계값 설정 (e.g., 1초)

**프로덕션 에러 추적 안됨**:
- Sentry DSN 환경변수 확인
- `enabled_environments` 설정 확인
