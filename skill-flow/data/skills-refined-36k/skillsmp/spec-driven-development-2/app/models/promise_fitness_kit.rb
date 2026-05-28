class PromiseFitnessKit < ApplicationRecord
  # Associations
  has_many :orders, dependent: :restrict_with_error

  # Validations
  validates :name, presence: true, uniqueness: true
  validates :description, presence: true
  validates :slug, presence: true,
                   uniqueness: true,
                   format: {
                     with: /\A[a-z0-9-]+\z/,
                     message: "must contain only lowercase letters, numbers, and hyphens"
                   }

  # Scopes
  scope :ordered_by_name, -> { order(:name) }

  # Instance Methods
  def to_s
    name
  end
end
