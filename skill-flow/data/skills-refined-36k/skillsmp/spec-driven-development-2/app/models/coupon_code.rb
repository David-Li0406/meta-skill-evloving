class CouponCode < ApplicationRecord
  # Associations
  has_many :orders, dependent: :restrict_with_error

  # Validations
  validates :code, presence: true, uniqueness: { case_sensitive: false },
                   format: { with: /\ASK\d+[A-Z]{3}\z/, message: "must be in format SK[number][3 letters]" }
  validates :usage, presence: true, inclusion: { in: %w[unused used] }

  # Callbacks
  before_validation :normalize_code
  before_destroy :check_not_used

  # Scopes
  scope :unused, -> { where(usage: 'unused') }
  scope :used, -> { where(usage: 'used') }
  scope :by_cursor, ->(cursor, direction) {
    return all if cursor.nil?

    if direction == 'next'
      where('id > ?', cursor)
    else
      where('id < ?', cursor)
    end
  }

  # Class Methods
  def self.generate_next_code
    # Extract all numbers from existing codes
    numbers = all.pluck(:code).map { |code| code[/\d+/].to_i }

    # Find max number, default to 999 if no codes exist
    max_number = numbers.max || 999

    # Increment by 1
    next_number = max_number + 1

    # Generate 3 random uppercase letters
    letters = 3.times.map { ('A'..'Z').to_a.sample }.join

    # Return formatted code
    "SK#{next_number}#{letters}"
  end

  # Instance Methods
  def unused?
    usage == 'unused'
  end

  def used?
    usage == 'used'
  end

  def mark_as_used!
    update!(usage: 'used')
  end

  private

  def normalize_code
    self.code = code.to_s.upcase.strip if code.present?
  end

  def check_not_used
    if used?
      errors.add(:base, "Used coupon codes cannot be deleted")
      throw :abort
    end
  end
end
