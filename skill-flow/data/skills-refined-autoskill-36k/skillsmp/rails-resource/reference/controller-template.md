# Controller Patterns

Complete controller template from existing code (PostsController, JobPostsController).

## Full Controller Template

```ruby
class ResourceNamesController < ApplicationController
  before_action :require_login, except: [:index, :show]
  before_action :set_resource_name, only: [:show, :edit, :update, :destroy]
  before_action :authorize_user, only: [:edit, :update, :destroy]

  def index
    @resource_names = ResourceName.includes(:user)
                                   .published
                                   .recent
                                   .limit(50)
  end

  def show
    @resource_name.increment_views!
  end

  def new
    @resource_name = ResourceName.new
  end

  def create
    @resource_name = current_user.resource_names.build(resource_name_params)

    if @resource_name.save
      redirect_to @resource_name, notice: '성공적으로 생성되었습니다.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit
  end

  def update
    if @resource_name.update(resource_name_params)
      redirect_to @resource_name, notice: '성공적으로 수정되었습니다.'
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @resource_name.destroy
    redirect_to resource_names_path, notice: '성공적으로 삭제되었습니다.'
  end

  private

  def set_resource_name
    @resource_name = ResourceName.find(params[:id])
  end

  def authorize_user
    redirect_to root_path, alert: '권한이 없습니다.' unless @resource_name.user == current_user
  end

  def resource_name_params
    params.require(:resource_name).permit(:title, :content, :status, :category)
  end
end
```

## Key Patterns

**N+1 Prevention**: Always use `includes(:user)` in index
**Authorization**: Check `@resource.user == current_user`
**Flash Messages**: Korean text
**Status Codes**: `:unprocessable_entity` for validation errors
**Redirects**: Use `notice` for success, `alert` for errors
