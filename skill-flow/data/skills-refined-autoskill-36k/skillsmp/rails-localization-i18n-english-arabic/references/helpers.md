# Localization Helpers Reference

## LocalizationHelper

```ruby
# app/helpers/localization_helper.rb
module LocalizationHelper
  # Direction helper for RTL/LTR
  def text_direction
    I18n.t('direction', default: 'ltr')
  end

  def rtl?
    text_direction == 'rtl'
  end

  def ltr?
    text_direction == 'ltr'
  end

  # CSS class for direction
  def direction_class
    rtl? ? 'rtl' : 'ltr'
  end

  # Opposite direction (for certain UI elements)
  def opposite_direction
    rtl? ? 'ltr' : 'rtl'
  end

  # Locale-aware text alignment
  def start_align
    rtl? ? 'right' : 'left'
  end

  def end_align
    rtl? ? 'left' : 'right'
  end

  # Eastern Arabic numerals conversion
  EASTERN_ARABIC_NUMERALS = {
    '0' => '٠', '1' => '١', '2' => '٢', '3' => '٣', '4' => '٤',
    '5' => '٥', '6' => '٦', '7' => '٧', '8' => '٨', '9' => '٩'
  }.freeze

  def to_eastern_arabic(number)
    number.to_s.gsub(/[0-9]/, EASTERN_ARABIC_NUMERALS)
  end

  def to_western_arabic(number)
    number.to_s.gsub(/[٠-٩]/, EASTERN_ARABIC_NUMERALS.invert)
  end

  # Locale-aware number display
  def localized_number(number, eastern_arabic: false)
    formatted = number_with_delimiter(number)
    eastern_arabic && I18n.locale == :ar ? to_eastern_arabic(formatted) : formatted
  end

  # Time-based greeting
  def greeting
    hour = Time.current.hour
    key = case hour
          when 5..11 then 'greetings.morning'
          when 12..16 then 'greetings.afternoon'
          else 'greetings.evening'
          end
    I18n.t(key)
  end

  # Personalized greeting with name
  def greeting_with_name(name)
    "#{greeting}، #{name}" if I18n.locale == :ar
    "#{greeting}, #{name}"
  end

  # Language switcher links
  def locale_switch_links
    I18n.available_locales.map do |locale|
      next if locale == I18n.locale

      link_to(
        I18n.t('language_name_native', locale: locale),
        switch_locale_path(locale: locale),
        class: 'locale-switch',
        data: { locale: locale }
      )
    end.compact.join(' | ').html_safe
  end

  # Format currency with locale awareness
  def localized_currency(amount, currency: nil)
    currency ||= current_currency

    options = {
      unit: currency_unit(currency),
      format: I18n.t('number.currency.format.format'),
      separator: I18n.t('number.currency.format.separator'),
      delimiter: I18n.t('number.currency.format.delimiter')
    }

    number_to_currency(amount, options)
  end

  # Saudi Riyal specific formatting
  def format_sar(amount, show_halalas: true)
    precision = show_halalas ? 2 : 0
    formatted = number_with_precision(amount, precision: precision)

    if I18n.locale == :ar
      "#{formatted} ر.س"
    else
      "SAR #{formatted}"
    end
  end

  # Currency units mapping
  def currency_unit(currency)
    {
      'SAR' => I18n.locale == :ar ? 'ر.س' : 'SAR',
      'USD' => I18n.locale == :ar ? '$' : '$',
      'EUR' => I18n.locale == :ar ? '€' : '€',
      'GBP' => I18n.locale == :ar ? '£' : '£',
      'AED' => I18n.locale == :ar ? 'د.إ' : 'AED'
    }[currency.to_s.upcase] || currency
  end

  private

  def current_currency
    # Override this based on your app's logic
    'SAR'
  end
end
```

---

## ArabicHelper

```ruby
# app/helpers/arabic_helper.rb
module ArabicHelper
  # Arabic pluralization helper for custom cases
  # Arabic has: zero, one, two, few (3-10), many (11-99), other (100+)
  def arabic_pluralize(count, singular, dual, plural_few, plural_many, plural_other = nil)
    return I18n.locale == :ar ? singular : singular unless count

    plural_other ||= plural_many

    case count
    when 0
      singular
    when 1
      singular
    when 2
      dual
    when 3..10
      "#{count} #{plural_few}"
    when 11..99
      "#{count} #{plural_many}"
    else
      "#{count} #{plural_other}"
    end
  end

  # Common Arabic plural forms
  def items_count(count)
    arabic_pluralize(
      count,
      I18n.t('common.items.zero'),
      I18n.t('common.items.one'),
      I18n.t('common.items.two'),
      I18n.t('common.items.few'),
      I18n.t('common.items.many')
    )
  end

  # Gender-aware translation
  # Usage: gender_t('welcome_message', gender: user.gender)
  def gender_t(key, gender:, **options)
    gendered_key = "#{key}.#{gender == 'female' ? 'female' : 'male'}"

    if I18n.exists?(gendered_key)
      I18n.t(gendered_key, **options)
    else
      I18n.t(key, **options)
    end
  end

  # Hijri date display (requires hijri gem or custom implementation)
  def hijri_date(date, format: :default)
    return unless date

    # Using the hijri gem if available
    if defined?(Hijri)
      hijri = Hijri::Date.new(date.year, date.month, date.day)
      format_hijri_date(hijri, format)
    else
      # Fallback: just show Gregorian
      I18n.l(date, format: format)
    end
  end

  # Format phone number for Saudi Arabia
  def format_saudi_phone(phone)
    return phone unless phone.present?

    # Remove non-digits
    digits = phone.gsub(/\D/, '')

    # Format: +966 XX XXX XXXX
    if digits.start_with?('966')
      "+966 #{digits[3..4]} #{digits[5..7]} #{digits[8..11]}"
    elsif digits.start_with?('0')
      "+966 #{digits[1..2]} #{digits[3..5]} #{digits[6..9]}"
    else
      phone
    end
  end

  # Arabic-aware truncation (doesn't break in middle of word)
  def arabic_truncate(text, length: 100, separator: ' ', omission: '...')
    return '' unless text

    if I18n.locale == :ar
      # Arabic omission
      omission = '...'
    end

    truncate(text, length: length, separator: separator, omission: omission)
  end

  # Wrap Arabic text in proper direction span
  def bidi_text(text, direction: nil)
    direction ||= detect_direction(text)
    content_tag(:span, text, dir: direction)
  end

  private

  def detect_direction(text)
    return 'ltr' unless text

    # Check if first letter is Arabic
    text.match?(/[\u0600-\u06FF]/) ? 'rtl' : 'ltr'
  end

  def format_hijri_date(hijri, format)
    # Custom Hijri date formatting
    case format
    when :short
      "#{hijri.day}/#{hijri.month}/#{hijri.year}"
    when :long
      month_names = %w[محرم صفر ربيع\ الأول ربيع\ الثاني جمادى\ الأولى جمادى\ الآخرة رجب شعبان رمضان شوال ذو\ القعدة ذو\ الحجة]
      "#{hijri.day} #{month_names[hijri.month - 1]} #{hijri.year} هـ"
    else
      "#{hijri.day}/#{hijri.month}/#{hijri.year} هـ"
    end
  end
end
```

---

## Application Controller Setup

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  around_action :switch_locale

  private

  def switch_locale(&action)
    locale = extract_locale || I18n.default_locale
    I18n.with_locale(locale, &action)
  end

  def extract_locale
    # Priority: URL param > User preference > Cookie > Accept-Language header
    extract_locale_from_param ||
      extract_locale_from_user ||
      extract_locale_from_cookie ||
      extract_locale_from_header
  end

  def extract_locale_from_param
    parsed_locale = params[:locale]
    I18n.available_locales.map(&:to_s).include?(parsed_locale) ? parsed_locale : nil
  end

  def extract_locale_from_user
    current_user&.preferred_locale if user_signed_in?
  end

  def extract_locale_from_cookie
    cookies[:locale] if I18n.available_locales.map(&:to_s).include?(cookies[:locale])
  end

  def extract_locale_from_header
    request.env['HTTP_ACCEPT_LANGUAGE']&.scan(/^[a-z]{2}/)&.first&.then do |locale|
      I18n.available_locales.map(&:to_s).include?(locale) ? locale : nil
    end
  end

  def default_url_options
    { locale: I18n.locale }
  end
end
```

---

## Locale Switcher Controller

```ruby
# app/controllers/locales_controller.rb
class LocalesController < ApplicationController
  def switch
    locale = params[:locale]

    if I18n.available_locales.map(&:to_s).include?(locale)
      cookies[:locale] = { value: locale, expires: 1.year.from_now }
      current_user&.update(preferred_locale: locale) if user_signed_in?
    end

    redirect_back(fallback_location: root_path(locale: locale))
  end
end
```
