# Model Layer Checklist

모델 계층 검수를 위한 상세 체크리스트입니다.

## 1. 관계 (Associations)

### 필수 확인 항목

- [ ] **belongs_to 정의 확인**
  ```ruby
  # ✅ Good
  class Comment < ApplicationRecord
    belongs_to :post
    belongs_to :user
  end

  # ❌ Bad - belongs_to 누락
  class Comment < ApplicationRecord
    # post_id 컬럼은 있지만 belongs_to 없음
  end
  ```

- [ ] **has_many dependent 옵션**
  ```ruby
  # ✅ Good
  class User < ApplicationRecord
    has_many :posts, dependent: :destroy
    has_many :comments, dependent: :destroy
  end

  # ❌ Bad - 고아 레코드 발생 가능
  class User < ApplicationRecord
    has_many :posts  # dependent 없음
  end
  ```

- [ ] **has_many through 관계**
  ```ruby
  # ✅ Good - 중간 테이블 활용
  class User < ApplicationRecord
    has_many :likes
    has_many :liked_posts, through: :likes, source: :likeable, source_type: 'Post'
  end
  ```

- [ ] **Polymorphic 관계**
  ```ruby
  # ✅ Good
  class Like < ApplicationRecord
    belongs_to :likeable, polymorphic: true
    belongs_to :user
  end

  class Post < ApplicationRecord
    has_many :likes, as: :likeable
  end
  ```

### 주의 사항

1. **순환 참조 방지**: A → B → A 형태의 관계 주의
2. **불필요한 관계 제거**: 사용하지 않는 association 정리
3. **inverse_of 설정**: 양방향 관계에서 메모리 최적화

## 2. 검증 (Validations)

### 필수 확인 항목

- [ ] **presence 검증**
  ```ruby
  # ✅ Good
  class User < ApplicationRecord
    validates :email, presence: true
    validates :name, presence: true
  end
  ```

- [ ] **uniqueness 검증 (DB 인덱스 필요)**
  ```ruby
  # ✅ Good - DB 인덱스와 함께
  validates :email, uniqueness: { case_sensitive: false }

  # Migration
  add_index :users, :email, unique: true
  ```

- [ ] **format 검증**
  ```ruby
  # ✅ Good
  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :phone, format: { with: /\A\d{10,11}\z/ }
  ```

- [ ] **length 검증**
  ```ruby
  # ✅ Good
  validates :title, length: { minimum: 1, maximum: 255 }
  validates :content, length: { minimum: 10 }
  validates :password, length: { minimum: 8 }
  ```

- [ ] **numericality 검증**
  ```ruby
  # ✅ Good
  validates :price, numericality: { greater_than: 0 }
  validates :quantity, numericality: { only_integer: true }
  ```

- [ ] **inclusion/exclusion 검증**
  ```ruby
  # ✅ Good
  validates :status, inclusion: { in: %w[draft published archived] }
  validates :role, exclusion: { in: %w[super_admin] }
  ```

### 커스텀 검증

```ruby
class Post < ApplicationRecord
  validate :content_not_spam

  private

  def content_not_spam
    if content&.include?('spam_keyword')
      errors.add(:content, 'contains spam')
    end
  end
end
```

## 3. Callbacks

### 체크 항목

- [ ] **callback 순서 확인**
  ```ruby
  # 실행 순서
  # before_validation → after_validation
  # before_save → around_save → after_save
  # before_create → around_create → after_create
  ```

- [ ] **부작용 최소화**
  ```ruby
  # ❌ Bad - callback에서 외부 API 호출
  after_create :send_to_external_api

  # ✅ Good - 백그라운드 잡으로 분리
  after_create_commit :schedule_external_sync

  def schedule_external_sync
    ExternalSyncJob.perform_later(id)
  end
  ```

- [ ] **조건부 실행**
  ```ruby
  # ✅ Good
  after_save :notify_followers, if: :published?
  before_destroy :check_can_destroy, unless: :admin_user?
  ```

- [ ] **트랜잭션 고려**
  ```ruby
  # after_commit은 트랜잭션 완료 후 실행
  after_commit :send_notification, on: :create
  ```

### Callback 복잡도 지표

| 레벨 | Callback 수 | 권장 조치 |
|------|------------|----------|
| 낮음 | 0-3 | 유지 |
| 중간 | 4-6 | 검토 필요 |
| 높음 | 7+ | Service Object로 분리 |

## 4. Scopes

### 체크 항목

- [ ] **기본 scope 정의**
  ```ruby
  class Post < ApplicationRecord
    scope :published, -> { where(status: :published) }
    scope :recent, -> { order(created_at: :desc) }
    scope :popular, -> { order(likes_count: :desc) }
  end
  ```

- [ ] **체이닝 가능 scope**
  ```ruby
  # ✅ Good - 체이닝 가능
  Post.published.recent.limit(10)
  ```

- [ ] **파라미터 scope**
  ```ruby
  scope :by_category, ->(category) { where(category: category) }
  scope :created_after, ->(date) { where('created_at > ?', date) }
  ```

## 5. Enums

### 체크 항목

- [ ] **enum 정의 확인**
  ```ruby
  class Post < ApplicationRecord
    enum :status, { draft: 0, published: 1, archived: 2 }
    enum :category, { free: 0, question: 1, promotion: 2, hiring: 3, seeking: 4 }
  end
  ```

- [ ] **enum 메서드 활용**
  ```ruby
  post.published?      # 상태 확인
  post.published!      # 상태 변경
  Post.published       # scope
  Post.statuses        # 전체 목록
  ```

- [ ] **i18n 연동**
  ```yaml
  # config/locales/ko.yml
  ko:
    activerecord:
      attributes:
        post:
          statuses:
            draft: 임시저장
            published: 게시됨
            archived: 보관됨
  ```

## 6. Concerns

### 체크 항목

- [ ] **공통 로직 추출**
  ```ruby
  # app/models/concerns/likeable.rb
  module Likeable
    extend ActiveSupport::Concern

    included do
      has_many :likes, as: :likeable, dependent: :destroy
    end

    def liked_by?(user)
      likes.exists?(user: user)
    end
  end
  ```

- [ ] **Concern 적용 확인**
  ```ruby
  class Post < ApplicationRecord
    include Likeable
    include Bookmarkable
  end
  ```

## 7. Counter Cache

### 체크 항목

- [ ] **자주 카운트하는 관계에 적용**
  ```ruby
  class Comment < ApplicationRecord
    belongs_to :post, counter_cache: true
  end

  # Migration
  add_column :posts, :comments_count, :integer, default: 0, null: false
  ```

- [ ] **정확도 확인**
  ```ruby
  # 카운터 리셋
  Post.reset_counters(post.id, :comments)
  ```

## 8. Security

### 체크 항목

- [ ] **민감 정보 마스킹**
  ```ruby
  class User < ApplicationRecord
    # 로그에서 제외
    self.filter_attributes += [:password, :ssn]
  end
  ```

- [ ] **attr_accessor 보안**
  ```ruby
  # 대량 할당에서 제외
  attr_accessor :admin_flag  # Strong Parameters에서 허용하지 않음
  ```

## 검수 결과 템플릿

```
## Model Layer Review - [날짜]

### 검토 모델
- [ ] User
- [ ] Post
- [ ] Comment
- [ ] Like
- [ ] Bookmark
- [ ] Notification

### 발견된 이슈
| 모델 | 이슈 | 심각도 | 해결방안 |
|------|------|--------|---------|
| | | | |

### 권장 개선사항
1.
2.
3.
```
