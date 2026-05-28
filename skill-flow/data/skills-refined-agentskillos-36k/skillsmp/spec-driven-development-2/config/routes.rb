Rails.application.routes.draw do
  # Fitness kit order pages - only matches if slug exists in database
  # This allows me to create routes like promisekits.com/strength-kit-1
  get '/:slug', to: 'orders#new', as: :fitness_kit_order,
    constraints: lambda { |request|
      slug = request.path_parameters[:slug]
      slug.present? && PromiseFitnessKit.exists?(slug: slug)
    }
  post '/:slug', to: 'orders#create', as: :create_fitness_kit_order,
    constraints: lambda { |request|
      slug = request.path_parameters[:slug]
      slug.present? && PromiseFitnessKit.exists?(slug: slug)
    }

  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  # Render dynamic PWA files from app/views/pwa/* (remember to link manifest in application.html.erb)
  # get "manifest" => "rails/pwa#manifest", as: :pwa_manifest
  # get "service-worker" => "rails/pwa#service_worker", as: :pwa_service_worker

  # Admin namespace
  namespace :admin do
    # Login/logout
    get 'login', to: 'sessions#new'
    post 'login', to: 'sessions#create'
    delete 'logout', to: 'sessions#destroy'

    # Dashboard
    root to: 'dashboard#index', as: :dashboard

    # Coupon Codes
    resources :coupon_codes, only: [:index, :create, :destroy]
  end

  # Redirect /admin to /admin/dashboard or login
  get 'admin', to: redirect('/admin')

  # Defines the root path route ("/")
  root "home#index"

  # Order confirmation page
  resources :orders, only: [:show]
end
