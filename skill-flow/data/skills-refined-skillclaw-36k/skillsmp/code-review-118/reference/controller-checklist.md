# Controller Layer Checklist

컨트롤러 계층 검수를 위한 상세 체크리스트입니다.

## 1. Strong Parameters

### 필수 확인 항목

- [ ] **모든 create/update 액션에 적용**
  ```ruby
  # ✅ Good
  def create
    @post = current_user.posts.build(post_params)
    # ...
  end

  private

  def post_params
    params.require(:post).permit(:title, :content, :category)
  end
  ```

- [ ] **민감 필드 제외 확인**
  ```ruby
  # ❌ Bad - admin 필드 허용
  def user_params
    params.require(:user).permit(:email, :name, :admin)
  end

  # ✅ Good
  def user_params
    params.require(:user).permit(:email, :name)
  end
  ```

- [ ] **중첩 속성 허용**
  ```ruby
  def post_params
    params.require(:post).permit(
      :title,
      :content,
      images_attributes: [:id, :url, :_destroy]
    )
  end
  ```

- [ ] **배열 파라미터**
  ```ruby
  def user_params
    params.require(:user).permit(
      :name,
      tag_ids: [],                    # 배열
      settings: {}                    # 해시
    )
  end
  ```

## 2. 인증/인가 (Authentication/Authorization)

### 필수 확인 항목

- [ ] **before_action 인증 필터**
  ```ruby
  class PostsController < ApplicationController
    before_action :require_login, except: [:index, :show]
    before_action :authorize_user, only: [:edit, :update, :destroy]
  end
  ```

- [ ] **skip_before_action 사용 시 주의**
  ```ruby
  # ✅ Good - 명시적 액션 지정
  skip_before_action :require_login, only: [:index, :show]

  # ❌ Bad - 전체 스킵
  skip_before_action :require_login
  ```

- [ ] **리소스 소유권 확인**
  ```ruby
  # ✅ Good
  def set_post
    @post = current_user.posts.find(params[:id])
  end

  # ❌ Bad - 모든 사용자가 접근 가능
  def set_post
    @post = Post.find(params[:id])
  end
  ```

- [ ] **인가 헬퍼 구현**
  ```ruby
  private

  def authorize_user
    unless @post.user == current_user
      redirect_to posts_path, alert: '권한이 없습니다.'
    end
  end
  ```

## 3. N+1 쿼리 방지

### 필수 확인 항목

- [ ] **includes 사용**
  ```ruby
  # ✅ Good
  def index
    @posts = Post.includes(:user, :comments)
                 .published
                 .recent
                 .page(params[:page])
  end

  # ❌ Bad
  def index
    @posts = Post.all
  end
  ```

- [ ] **관련 데이터 미리 로드**
  ```ruby
  # ✅ Good
  def show
    @post = Post.includes(:user, comments: :user).find(params[:id])
  end
  ```

- [ ] **카운트 최적화**
  ```ruby
  # ❌ Bad
  @posts.each { |p| p.comments.count }

  # ✅ Good - counter_cache 사용
  @posts.each { |p| p.comments_count }
  ```

## 4. 응답 처리

### 필수 확인 항목

- [ ] **respond_to 활용**
  ```ruby
  def create
    @post = current_user.posts.build(post_params)

    respond_to do |format|
      if @post.save
        format.html { redirect_to @post, notice: '게시글이 작성되었습니다.' }
        format.turbo_stream
        format.json { render json: @post, status: :created }
      else
        format.html { render :new, status: :unprocessable_entity }
        format.json { render json: @post.errors, status: :unprocessable_entity }
      end
    end
  end
  ```

- [ ] **Turbo Stream 응답**
  ```ruby
  # app/views/posts/create.turbo_stream.erb
  <%= turbo_stream.prepend "posts", @post %>
  <%= turbo_stream.update "flash", partial: "shared/flash" %>
  ```

- [ ] **적절한 HTTP 상태 코드**
  ```ruby
  # 성공
  render :show, status: :ok           # 200
  render :new, status: :created       # 201

  # 클라이언트 에러
  render :edit, status: :unprocessable_entity  # 422
  render json: { error: 'Not found' }, status: :not_found  # 404

  # 리다이렉트
  redirect_to posts_path, status: :see_other  # 303 (Turbo)
  ```

## 5. 에러 처리

### 필수 확인 항목

- [ ] **전역 에러 핸들링**
  ```ruby
  # app/controllers/application_controller.rb
  class ApplicationController < ActionController::Base
    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActionController::ParameterMissing, with: :bad_request

    private

    def not_found
      respond_to do |format|
        format.html { render 'errors/not_found', status: :not_found }
        format.json { render json: { error: 'Not found' }, status: :not_found }
      end
    end

    def bad_request(exception)
      render json: { error: exception.message }, status: :bad_request
    end
  end
  ```

- [ ] **개별 에러 처리**
  ```ruby
  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      redirect_to @post
    else
      flash.now[:alert] = @post.errors.full_messages.first
      render :new, status: :unprocessable_entity
    end
  rescue StandardError => e
    Rails.logger.error "Post creation failed: #{e.message}"
    redirect_to posts_path, alert: '오류가 발생했습니다.'
  end
  ```

## 6. RESTful 패턴

### 필수 확인 항목

- [ ] **표준 액션 사용**
  ```ruby
  # RESTful 액션
  # index, show, new, create, edit, update, destroy

  class PostsController < ApplicationController
    def index; end
    def show; end
    def new; end
    def create; end
    def edit; end
    def update; end
    def destroy; end
  end
  ```

- [ ] **커스텀 액션 최소화**
  ```ruby
  # ❌ Bad - 과도한 커스텀 액션
  def publish; end
  def unpublish; end
  def archive; end

  # ✅ Good - update로 통합
  def update
    @post.update(post_params)  # status 변경 포함
  end
  ```

- [ ] **중첩 리소스 제한**
  ```ruby
  # ✅ Good - 1단계 중첩
  resources :posts do
    resources :comments, only: [:create, :destroy]
  end

  # ❌ Bad - 과도한 중첩
  resources :users do
    resources :posts do
      resources :comments do
        resources :likes
      end
    end
  end
  ```

## 7. 캐싱

### 체크 항목

- [ ] **Action 캐싱**
  ```ruby
  # 정적 페이지
  caches_page :index

  # 동적 페이지 (조건부)
  caches_action :show, expires_in: 1.hour
  ```

- [ ] **Fragment 캐싱 (뷰에서)**
  ```erb
  <% cache @post do %>
    <%= render @post %>
  <% end %>
  ```

- [ ] **ETag/Last-Modified**
  ```ruby
  def show
    @post = Post.find(params[:id])
    fresh_when(@post)
  end
  ```

## 8. 보안

### 필수 확인 항목

- [ ] **CSRF 보호**
  ```ruby
  # ApplicationController
  protect_from_forgery with: :exception

  # API 컨트롤러
  protect_from_forgery with: :null_session
  ```

- [ ] **XSS 방지**
  ```ruby
  # 뷰에서 자동 이스케이핑 확인
  # raw, html_safe 사용 시 sanitize 필수
  ```

- [ ] **SQL Injection 방지**
  ```ruby
  # ❌ Bad
  Post.where("title = '#{params[:title]}'")

  # ✅ Good
  Post.where(title: params[:title])
  Post.where("title = ?", params[:title])
  ```

- [ ] **파라미터 검증**
  ```ruby
  def set_page
    @page = params[:page].to_i
    @page = 1 if @page < 1
    @page = 100 if @page > 100  # 최대 제한
  end
  ```

## 9. 성능

### 체크 항목

- [ ] **페이지네이션**
  ```ruby
  def index
    @posts = Post.published
                 .includes(:user)
                 .page(params[:page])
                 .per(20)
  end
  ```

- [ ] **불필요한 쿼리 제거**
  ```ruby
  # ❌ Bad
  @posts = Post.all
  @posts_count = Post.count  # 추가 쿼리

  # ✅ Good
  @posts = Post.all
  @posts_count = @posts.size  # 메모리에서 계산
  ```

- [ ] **select 활용**
  ```ruby
  # 필요한 컬럼만 로드
  @posts = Post.select(:id, :title, :created_at).limit(10)
  ```

## 10. 코드 구조

### 체크 항목

- [ ] **Fat Controller 방지**
  ```ruby
  # ❌ Bad - 컨트롤러에 비즈니스 로직
  def create
    @post = Post.new(post_params)
    @post.calculate_score
    @post.assign_tags
    @post.notify_subscribers
    # ...
  end

  # ✅ Good - Service Object 활용
  def create
    result = Posts::CreateService.call(post_params, current_user)

    if result.success?
      redirect_to result.post
    else
      render :new
    end
  end
  ```

- [ ] **before_action 활용**
  ```ruby
  before_action :set_post, only: [:show, :edit, :update, :destroy]

  private

  def set_post
    @post = Post.find(params[:id])
  end
  ```

- [ ] **Private 메서드 분리**
  ```ruby
  class PostsController < ApplicationController
    # 공개 액션
    def index; end
    def show; end

    private

    # 헬퍼 메서드
    def set_post; end
    def post_params; end
    def authorize_user; end
  end
  ```

## 검수 결과 템플릿

```
## Controller Layer Review - [날짜]

### 검토 컨트롤러
- [ ] ApplicationController
- [ ] PostsController
- [ ] CommentsController
- [ ] UsersController
- [ ] SessionsController

### 발견된 이슈
| 컨트롤러 | 이슈 | 심각도 | 해결방안 |
|----------|------|--------|---------|
| | | | |

### 보안 체크
- [ ] Strong Parameters 적용
- [ ] 인증 필터 적용
- [ ] 인가 로직 구현
- [ ] CSRF 보호 활성화

### 성능 체크
- [ ] N+1 쿼리 없음
- [ ] 페이지네이션 적용
- [ ] 캐싱 설정
```
