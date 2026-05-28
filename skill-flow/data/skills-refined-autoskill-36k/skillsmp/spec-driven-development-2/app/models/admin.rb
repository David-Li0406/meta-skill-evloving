class Admin < ApplicationRecord
  has_secure_password

  validates :username, presence: true,
                       uniqueness: true,
                       length: { minimum: 3, maximum: 50 }
  validates :password, length: { minimum: 8 }, allow_nil: true
end
