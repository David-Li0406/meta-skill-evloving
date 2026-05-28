# Localization Testing Reference

## Test Helpers

```ruby
# spec/support/i18n_helpers.rb
module I18nHelpers
  def with_locale(locale, &block)
    original_locale = I18n.locale
    I18n.locale = locale
    yield
  ensure
    I18n.locale = original_locale
  end

  def t(key, **options)
    I18n.t(key, **options)
  end

  def l(object, **options)
    I18n.l(object, **options)
  end
end

RSpec.configure do |config|
  config.include I18nHelpers
end
```

---

## LocalizationHelper Specs

```ruby
# spec/helpers/localization_helper_spec.rb
require 'rails_helper'

RSpec.describe LocalizationHelper, type: :helper do
  describe '#text_direction' do
    it 'returns ltr for English' do
      with_locale(:en) do
        expect(helper.text_direction).to eq('ltr')
      end
    end

    it 'returns rtl for Arabic' do
      with_locale(:ar) do
        expect(helper.text_direction).to eq('rtl')
      end
    end
  end

  describe '#to_eastern_arabic' do
    it 'converts Western to Eastern Arabic numerals' do
      expect(helper.to_eastern_arabic('123')).to eq('١٢٣')
      expect(helper.to_eastern_arabic('0')).to eq('٠')
      expect(helper.to_eastern_arabic('9876543210')).to eq('٩٨٧٦٥٤٣٢١٠')
    end
  end

  describe '#localized_currency' do
    it 'formats currency for English locale' do
      with_locale(:en) do
        expect(helper.localized_currency(1000, currency: 'SAR')).to include('SAR')
      end
    end

    it 'formats currency for Arabic locale' do
      with_locale(:ar) do
        expect(helper.localized_currency(1000, currency: 'SAR')).to include('ر.س')
      end
    end
  end

  describe '#rtl?' do
    it 'returns false for English' do
      with_locale(:en) { expect(helper.rtl?).to be false }
    end

    it 'returns true for Arabic' do
      with_locale(:ar) { expect(helper.rtl?).to be true }
    end
  end

  describe '#greeting' do
    it 'returns time-appropriate greeting' do
      travel_to Time.zone.local(2024, 1, 1, 9, 0, 0) do
        with_locale(:en) do
          expect(helper.greeting).to eq('Good morning')
        end
      end
    end
  end
end
```

---

## I18n Configuration Specs

```ruby
# spec/i18n_spec.rb
require 'rails_helper'

RSpec.describe 'I18n' do
  describe 'locale files' do
    it 'has all required locales' do
      expect(I18n.available_locales).to contain_exactly(:en, :ar)
    end

    it 'has no missing translations for English' do
      I18n.with_locale(:en) do
        expect { I18n.t('common.actions.save', raise: true) }.not_to raise_error
        expect { I18n.t('activerecord.models.user.one', raise: true) }.not_to raise_error
      end
    end

    it 'has no missing translations for Arabic' do
      I18n.with_locale(:ar) do
        expect { I18n.t('common.actions.save', raise: true) }.not_to raise_error
        expect { I18n.t('activerecord.models.user.one', raise: true) }.not_to raise_error
      end
    end
  end

  describe 'Arabic pluralization' do
    it 'handles all plural forms' do
      I18n.with_locale(:ar) do
        expect(I18n.t('datetime.distance_in_words.x_days', count: 0)).to include('صفر')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 1)).to include('يوم واحد')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 2)).to include('يومان')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 5)).to include('أيام')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 20)).to include('يومًا')
        expect(I18n.t('datetime.distance_in_words.x_days', count: 100)).to include('يوم')
      end
    end
  end

  describe 'date formatting' do
    let(:date) { Date.new(2024, 1, 15) }

    it 'formats dates in English' do
      I18n.with_locale(:en) do
        expect(I18n.l(date, format: :long)).to eq('January 15, 2024')
      end
    end

    it 'formats dates in Arabic' do
      I18n.with_locale(:ar) do
        expect(I18n.l(date, format: :long)).to include('يناير')
      end
    end
  end
end
```

---

## System Specs for Localization

```ruby
# spec/system/localization_spec.rb
require 'rails_helper'

RSpec.describe 'Localization', type: :system do
  describe 'language switching' do
    it 'switches to Arabic' do
      visit root_path

      click_link 'العربية'

      expect(page).to have_css('html[dir="rtl"]')
      expect(page).to have_css('html[lang="ar"]')
    end

    it 'persists locale preference' do
      visit root_path(locale: :ar)

      visit users_path

      expect(page).to have_css('html[lang="ar"]')
    end
  end

  describe 'RTL layout' do
    before { visit root_path(locale: :ar) }

    it 'applies RTL direction to body' do
      expect(page).to have_css('body.rtl')
    end

    it 'displays Arabic content' do
      expect(page).to have_content('أهلاً وسهلاً')
    end
  end

  describe 'form localization' do
    it 'displays localized labels and errors' do
      visit new_user_path(locale: :ar)

      click_button 'إرسال'

      expect(page).to have_content('لا يمكن أن يكون فارغًا')
    end
  end

  describe 'bidirectional forms' do
    it 'keeps email input LTR in Arabic locale' do
      visit new_user_path(locale: :ar)

      email_input = find('input[type="email"]')
      expect(email_input['dir']).to eq('ltr')
    end

    it 'uses auto direction for name fields' do
      visit new_user_path(locale: :ar)

      name_input = find('input[name*="first_name"]')
      expect(name_input['dir']).to eq('auto')
    end
  end
end
```

---

## Translation Completeness Test

```ruby
# spec/i18n/completeness_spec.rb
require 'rails_helper'

RSpec.describe 'Translation completeness' do
  let(:english_keys) { collect_keys(:en) }
  let(:arabic_keys) { collect_keys(:ar) }

  it 'has all English keys in Arabic' do
    missing = english_keys - arabic_keys
    expect(missing).to be_empty, "Missing Arabic translations: #{missing.join(', ')}"
  end

  it 'has no extra Arabic keys not in English' do
    extra = arabic_keys - english_keys
    # Some extra keys may be intentional (pluralization forms)
    non_plural_extra = extra.reject { |k| k.match?(/\.(zero|two|few|many)$/) }
    expect(non_plural_extra).to be_empty, "Extra Arabic keys: #{non_plural_extra.join(', ')}"
  end

  private

  def collect_keys(locale, hash = I18n.backend.translations[locale], prefix = '')
    keys = []
    hash.each do |key, value|
      full_key = prefix.empty? ? key.to_s : "#{prefix}.#{key}"
      if value.is_a?(Hash)
        keys += collect_keys(locale, value, full_key)
      else
        keys << full_key
      end
    end
    keys
  end
end
```

---

## Request Specs for Locale Switching

```ruby
# spec/requests/locales_spec.rb
require 'rails_helper'

RSpec.describe 'Locale switching', type: :request do
  describe 'GET /locale/:locale' do
    it 'sets locale cookie' do
      get switch_locale_path(locale: 'ar')

      expect(response.cookies['locale']).to eq('ar')
    end

    it 'redirects back to previous page' do
      get users_path
      get switch_locale_path(locale: 'ar'), headers: { 'HTTP_REFERER' => users_path }

      expect(response).to redirect_to(users_path(locale: 'ar'))
    end

    it 'ignores invalid locales' do
      get switch_locale_path(locale: 'xx')

      expect(response.cookies['locale']).to be_nil
    end
  end

  describe 'locale detection' do
    it 'uses URL parameter first' do
      get root_path(locale: 'ar')

      expect(response.body).to include('أهلاً')
    end

    it 'falls back to cookie' do
      cookies[:locale] = 'ar'
      get root_path

      expect(response.body).to include('العربية')
    end

    it 'falls back to Accept-Language header' do
      get root_path, headers: { 'HTTP_ACCEPT_LANGUAGE' => 'ar' }

      expect(response.body).to include('أهلاً')
    end
  end
end
```
