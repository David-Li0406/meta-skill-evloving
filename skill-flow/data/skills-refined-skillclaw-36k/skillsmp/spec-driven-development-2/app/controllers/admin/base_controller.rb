class Admin::BaseController < ApplicationController
  before_action :require_admin
  layout 'admin'

  private

  def require_admin
    unless current_admin
      redirect_to admin_login_path, alert: "Please log in to access admin area"
    end
  end

  def current_admin
    @current_admin ||= Admin.find_by(id: session[:admin_id]) if session[:admin_id]
  end
  helper_method :current_admin
end
