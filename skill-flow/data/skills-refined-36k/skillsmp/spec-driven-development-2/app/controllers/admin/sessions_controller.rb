class Admin::SessionsController < ApplicationController
  layout 'admin'

  def new
    # Redirect to dashboard if already logged in
    redirect_to admin_dashboard_path if current_admin
  end

  def create
    admin = Admin.find_by(username: params[:username])

    if admin&.authenticate(params[:password])
      session[:admin_id] = admin.id
      session[:admin_expires_at] = 12.hours.from_now
      redirect_to admin_dashboard_path, notice: "Welcome back, #{admin.username}!"
    else
      flash.now[:alert] = "Invalid username or password"
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    session[:admin_id] = nil
    session[:admin_expires_at] = nil
    redirect_to root_path, notice: "Logged out successfully"
  end

  private

  def current_admin
    @current_admin ||= Admin.find_by(id: session[:admin_id]) if session[:admin_id]
  end
  helper_method :current_admin
end
