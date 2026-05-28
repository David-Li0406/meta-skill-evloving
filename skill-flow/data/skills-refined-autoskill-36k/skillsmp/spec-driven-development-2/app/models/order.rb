class Order < ApplicationRecord
  # Associations
  belongs_to :promise_fitness_kit
  belongs_to :coupon_code

  # Constants
  US_STATES = %w[
    AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD
    MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC
    SD TN TX UT VT VA WA WV WI WY DC
  ].freeze

  # Validations
  validates :first_name, presence: true
  validates :last_name, presence: true
  validates :address1, presence: true
  validates :city, presence: true
  validates :state, presence: true,
                    inclusion: { in: US_STATES, message: 'must be a valid US state' }
  validates :zip, presence: true,
                  format: { with: /\A\d{5}(-\d{4})?\z/, message: 'must be 5 digits or ZIP+4' }
  validates :phone, presence: true,
                    length: { is: 10, message: 'must be exactly 10 digits' },
                    format: { with: /\A\d{10}\z/, message: 'must contain only digits' }
  validates :email, presence: true,
                    format: { with: URI::MailTo::EMAIL_REGEXP, message: 'must be a valid email' }
  validates :order_confirmation, uniqueness: true, allow_nil: true

  # Custom validations
  validate :coupon_code_must_be_unused, on: :create

  # Callbacks
  before_validation :normalize_attributes
  before_create :generate_order_confirmation
  after_create :mark_coupon_as_used

  # Scopes
  scope :recent, -> { order(created_at: :desc) }

  # Class Methods
  def self.next_confirmation_number
    maximum(:order_confirmation).to_i + 1
  end

  # Instance Methods
  def formatted_order_confirmation
    sprintf("%06d", order_confirmation)
  end

  def full_name
    "#{first_name} #{last_name}"
  end

  def formatted_phone
    "(#{phone[0..2]}) #{phone[3..5]}-#{phone[6..9]}"
  end

  def full_address
    [address1, address2, "#{city}, #{state} #{zip}"].compact.join("\n")
  end

  private

  def normalize_attributes
    self.state = state.to_s.upcase.strip if state.present?
    self.email = email.to_s.downcase.strip if email.present?
    self.phone = phone.to_s.gsub(/\D/, '') if phone.present? # Remove non-digits
    self.zip = zip.to_s.strip if zip.present?
  end

  def generate_order_confirmation
    self.order_confirmation = self.class.next_confirmation_number
  end

  def coupon_code_must_be_unused
    return unless coupon_code

    if coupon_code.used?
      errors.add(:coupon_code, 'has already been used')
    end
  end

  def mark_coupon_as_used
    coupon_code.mark_as_used!
  end
end
