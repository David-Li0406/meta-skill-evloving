# Complete Locale Files Reference

## File Structure

```
config/
└── locales/
    ├── en/
    │   ├── activerecord.en.yml
    │   ├── controllers.en.yml
    │   ├── mailers.en.yml
    │   ├── models.en.yml
    │   └── views.en.yml
    ├── ar/
    │   ├── activerecord.ar.yml
    │   ├── controllers.ar.yml
    │   ├── mailers.ar.yml
    │   ├── models.ar.yml
    │   └── views.ar.yml
    ├── defaults/
    │   ├── en.yml      # Rails defaults, pagination, etc.
    │   └── ar.yml
    └── shared/
        ├── errors.en.yml
        ├── errors.ar.yml
        ├── flash.en.yml
        └── flash.ar.yml
```

---

## Base English Locale

```yaml
# config/locales/defaults/en.yml
en:
  # Direction and language metadata
  direction: ltr
  language_name: "English"
  language_name_native: "English"

  # Date and time formats
  date:
    formats:
      default: "%Y-%m-%d"
      short: "%b %d"
      long: "%B %d, %Y"
      month_year: "%B %Y"
      day_month: "%d %B"
    day_names:
      - Sunday
      - Monday
      - Tuesday
      - Wednesday
      - Thursday
      - Friday
      - Saturday
    abbr_day_names:
      - Sun
      - Mon
      - Tue
      - Wed
      - Thu
      - Fri
      - Sat
    month_names:
      - ~
      - January
      - February
      - March
      - April
      - May
      - June
      - July
      - August
      - September
      - October
      - November
      - December
    abbr_month_names:
      - ~
      - Jan
      - Feb
      - Mar
      - Apr
      - May
      - Jun
      - Jul
      - Aug
      - Sep
      - Oct
      - Nov
      - Dec
    order:
      - :year
      - :month
      - :day

  time:
    formats:
      default: "%a, %d %b %Y %H:%M:%S %z"
      short: "%d %b %H:%M"
      long: "%B %d, %Y %H:%M"
      time_only: "%H:%M"
      time_with_zone: "%H:%M %Z"
    am: "AM"
    pm: "PM"

  # Number formats
  number:
    format:
      separator: "."
      delimiter: ","
      precision: 2
      significant: false
      strip_insignificant_zeros: false
    currency:
      format:
        format: "%u%n"
        unit: "$"
        separator: "."
        delimiter: ","
        precision: 2
        significant: false
        strip_insignificant_zeros: false
    percentage:
      format:
        delimiter: ""
        format: "%n%"
    precision:
      format:
        delimiter: ""
    human:
      format:
        delimiter: ""
        precision: 3
        significant: true
        strip_insignificant_zeros: true
      storage_units:
        format: "%n %u"
        units:
          byte:
            one: "Byte"
            other: "Bytes"
          kb: "KB"
          mb: "MB"
          gb: "GB"
          tb: "TB"
          pb: "PB"
      decimal_units:
        format: "%n %u"
        units:
          unit: ""
          thousand: "Thousand"
          million: "Million"
          billion: "Billion"
          trillion: "Trillion"
          quadrillion: "Quadrillion"

  # Distance of time in words
  datetime:
    distance_in_words:
      half_a_minute: "half a minute"
      less_than_x_seconds:
        one: "less than 1 second"
        other: "less than %{count} seconds"
      x_seconds:
        one: "1 second"
        other: "%{count} seconds"
      less_than_x_minutes:
        one: "less than a minute"
        other: "less than %{count} minutes"
      x_minutes:
        one: "1 minute"
        other: "%{count} minutes"
      about_x_hours:
        one: "about 1 hour"
        other: "about %{count} hours"
      x_days:
        one: "1 day"
        other: "%{count} days"
      about_x_months:
        one: "about 1 month"
        other: "about %{count} months"
      x_months:
        one: "1 month"
        other: "%{count} months"
      about_x_years:
        one: "about 1 year"
        other: "about %{count} years"
      over_x_years:
        one: "over 1 year"
        other: "over %{count} years"
      almost_x_years:
        one: "almost 1 year"
        other: "almost %{count} years"
    prompts:
      year: "Year"
      month: "Month"
      day: "Day"
      hour: "Hour"
      minute: "Minute"
      second: "Second"

  # Support
  support:
    array:
      words_connector: ", "
      two_words_connector: " and "
      last_word_connector: ", and "

  # Common UI elements
  common:
    actions:
      save: "Save"
      cancel: "Cancel"
      delete: "Delete"
      edit: "Edit"
      create: "Create"
      update: "Update"
      back: "Back"
      next: "Next"
      previous: "Previous"
      submit: "Submit"
      confirm: "Confirm"
      close: "Close"
      search: "Search"
      filter: "Filter"
      clear: "Clear"
      reset: "Reset"
      download: "Download"
      upload: "Upload"
      export: "Export"
      import: "Import"
      print: "Print"
      refresh: "Refresh"
      view: "View"
      view_all: "View All"
      show_more: "Show More"
      show_less: "Show Less"
      loading: "Loading..."
      processing: "Processing..."

    confirmations:
      delete: "Are you sure you want to delete this?"
      unsaved_changes: "You have unsaved changes. Are you sure you want to leave?"
      action_irreversible: "This action cannot be undone."

    status:
      active: "Active"
      inactive: "Inactive"
      pending: "Pending"
      approved: "Approved"
      rejected: "Rejected"
      completed: "Completed"
      cancelled: "Cancelled"
      draft: "Draft"
      published: "Published"
      archived: "Archived"

    labels:
      yes: "Yes"
      no: "No"
      all: "All"
      none: "None"
      select: "Select"
      select_option: "Select an option"
      optional: "Optional"
      required: "Required"
      not_available: "N/A"
      unknown: "Unknown"
      other: "Other"

    messages:
      no_results: "No results found"
      no_data: "No data available"
      error_occurred: "An error occurred"
      try_again: "Please try again"
      success: "Success"
      saved_successfully: "Saved successfully"
      deleted_successfully: "Deleted successfully"
      updated_successfully: "Updated successfully"
      created_successfully: "Created successfully"

    pagination:
      first: "First"
      last: "Last"
      previous: "Previous"
      next: "Next"
      showing: "Showing %{from} to %{to} of %{total} entries"
      per_page: "per page"

  # Greetings (time-based)
  greetings:
    morning: "Good morning"
    afternoon: "Good afternoon"
    evening: "Good evening"
    welcome: "Welcome"
    welcome_back: "Welcome back"
    hello: "Hello"
    goodbye: "Goodbye"
    thank_you: "Thank you"
```

---

## Base Arabic Locale

```yaml
# config/locales/defaults/ar.yml
ar:
  # Direction and language metadata
  direction: rtl
  language_name: "Arabic"
  language_name_native: "العربية"

  # Date and time formats
  date:
    formats:
      default: "%Y-%m-%d"
      short: "%d %b"
      long: "%d %B، %Y"
      month_year: "%B %Y"
      day_month: "%d %B"
    day_names:
      - الأحد
      - الاثنين
      - الثلاثاء
      - الأربعاء
      - الخميس
      - الجمعة
      - السبت
    abbr_day_names:
      - أحد
      - اثنين
      - ثلاثاء
      - أربعاء
      - خميس
      - جمعة
      - سبت
    month_names:
      - ~
      - يناير
      - فبراير
      - مارس
      - أبريل
      - مايو
      - يونيو
      - يوليو
      - أغسطس
      - سبتمبر
      - أكتوبر
      - نوفمبر
      - ديسمبر
    abbr_month_names:
      - ~
      - يناير
      - فبراير
      - مارس
      - أبريل
      - مايو
      - يونيو
      - يوليو
      - أغسطس
      - سبتمبر
      - أكتوبر
      - نوفمبر
      - ديسمبر
    order:
      - :day
      - :month
      - :year

  time:
    formats:
      default: "%a، %d %b %Y %H:%M:%S %z"
      short: "%d %b %H:%M"
      long: "%d %B، %Y %H:%M"
      time_only: "%H:%M"
      time_with_zone: "%H:%M %Z"
    am: "ص"
    pm: "م"

  # Number formats (using Arabic-Indic separators)
  number:
    format:
      separator: "٫"
      delimiter: "٬"
      precision: 2
      significant: false
      strip_insignificant_zeros: false
    currency:
      format:
        format: "%n %u"
        unit: "ر.س"
        separator: "٫"
        delimiter: "٬"
        precision: 2
        significant: false
        strip_insignificant_zeros: false
    percentage:
      format:
        delimiter: ""
        format: "%%n"
    precision:
      format:
        delimiter: ""
    human:
      format:
        delimiter: ""
        precision: 3
        significant: true
        strip_insignificant_zeros: true
      storage_units:
        format: "%n %u"
        units:
          byte:
            zero: "بايت"
            one: "بايت"
            two: "بايت"
            few: "بايت"
            many: "بايت"
            other: "بايت"
          kb: "ك.ب"
          mb: "م.ب"
          gb: "ج.ب"
          tb: "ت.ب"
          pb: "ب.ب"
      decimal_units:
        format: "%n %u"
        units:
          unit: ""
          thousand: "ألف"
          million: "مليون"
          billion: "مليار"
          trillion: "تريليون"
          quadrillion: "كوادريليون"

  # Distance of time in words (with Arabic pluralization - 6 forms)
  datetime:
    distance_in_words:
      half_a_minute: "نصف دقيقة"
      less_than_x_seconds:
        zero: "أقل من ثانية"
        one: "أقل من ثانية واحدة"
        two: "أقل من ثانيتين"
        few: "أقل من %{count} ثوانٍ"
        many: "أقل من %{count} ثانية"
        other: "أقل من %{count} ثانية"
      x_seconds:
        zero: "صفر ثوانٍ"
        one: "ثانية واحدة"
        two: "ثانيتان"
        few: "%{count} ثوانٍ"
        many: "%{count} ثانية"
        other: "%{count} ثانية"
      less_than_x_minutes:
        zero: "أقل من دقيقة"
        one: "أقل من دقيقة واحدة"
        two: "أقل من دقيقتين"
        few: "أقل من %{count} دقائق"
        many: "أقل من %{count} دقيقة"
        other: "أقل من %{count} دقيقة"
      x_minutes:
        zero: "صفر دقائق"
        one: "دقيقة واحدة"
        two: "دقيقتان"
        few: "%{count} دقائق"
        many: "%{count} دقيقة"
        other: "%{count} دقيقة"
      about_x_hours:
        zero: "أقل من ساعة"
        one: "حوالي ساعة واحدة"
        two: "حوالي ساعتين"
        few: "حوالي %{count} ساعات"
        many: "حوالي %{count} ساعة"
        other: "حوالي %{count} ساعة"
      x_days:
        zero: "صفر أيام"
        one: "يوم واحد"
        two: "يومان"
        few: "%{count} أيام"
        many: "%{count} يومًا"
        other: "%{count} يوم"
      about_x_months:
        zero: "أقل من شهر"
        one: "حوالي شهر واحد"
        two: "حوالي شهرين"
        few: "حوالي %{count} أشهر"
        many: "حوالي %{count} شهرًا"
        other: "حوالي %{count} شهر"
      x_months:
        zero: "صفر أشهر"
        one: "شهر واحد"
        two: "شهران"
        few: "%{count} أشهر"
        many: "%{count} شهرًا"
        other: "%{count} شهر"
      about_x_years:
        zero: "أقل من سنة"
        one: "حوالي سنة واحدة"
        two: "حوالي سنتين"
        few: "حوالي %{count} سنوات"
        many: "حوالي %{count} سنة"
        other: "حوالي %{count} سنة"
      over_x_years:
        zero: "أقل من سنة"
        one: "أكثر من سنة واحدة"
        two: "أكثر من سنتين"
        few: "أكثر من %{count} سنوات"
        many: "أكثر من %{count} سنة"
        other: "أكثر من %{count} سنة"
      almost_x_years:
        zero: "أقل من سنة"
        one: "ما يقارب سنة واحدة"
        two: "ما يقارب سنتين"
        few: "ما يقارب %{count} سنوات"
        many: "ما يقارب %{count} سنة"
        other: "ما يقارب %{count} سنة"
    prompts:
      year: "السنة"
      month: "الشهر"
      day: "اليوم"
      hour: "الساعة"
      minute: "الدقيقة"
      second: "الثانية"

  # Support
  support:
    array:
      words_connector: "، "
      two_words_connector: " و"
      last_word_connector: "، و"

  # Common UI elements
  common:
    actions:
      save: "حفظ"
      cancel: "إلغاء"
      delete: "حذف"
      edit: "تعديل"
      create: "إنشاء"
      update: "تحديث"
      back: "رجوع"
      next: "التالي"
      previous: "السابق"
      submit: "إرسال"
      confirm: "تأكيد"
      close: "إغلاق"
      search: "بحث"
      filter: "تصفية"
      clear: "مسح"
      reset: "إعادة تعيين"
      download: "تحميل"
      upload: "رفع"
      export: "تصدير"
      import: "استيراد"
      print: "طباعة"
      refresh: "تحديث"
      view: "عرض"
      view_all: "عرض الكل"
      show_more: "عرض المزيد"
      show_less: "عرض أقل"
      loading: "جارٍ التحميل..."
      processing: "جارٍ المعالجة..."

    confirmations:
      delete: "هل أنت متأكد من الحذف؟"
      unsaved_changes: "لديك تغييرات غير محفوظة. هل تريد المغادرة؟"
      action_irreversible: "لا يمكن التراجع عن هذا الإجراء."

    status:
      active: "نشط"
      inactive: "غير نشط"
      pending: "قيد الانتظار"
      approved: "معتمد"
      rejected: "مرفوض"
      completed: "مكتمل"
      cancelled: "ملغي"
      draft: "مسودة"
      published: "منشور"
      archived: "مؤرشف"

    labels:
      yes: "نعم"
      no: "لا"
      all: "الكل"
      none: "لا شيء"
      select: "اختر"
      select_option: "اختر خيارًا"
      optional: "اختياري"
      required: "مطلوب"
      not_available: "غير متوفر"
      unknown: "غير معروف"
      other: "أخرى"

    messages:
      no_results: "لا توجد نتائج"
      no_data: "لا توجد بيانات"
      error_occurred: "حدث خطأ"
      try_again: "يرجى المحاولة مرة أخرى"
      success: "نجاح"
      saved_successfully: "تم الحفظ بنجاح"
      deleted_successfully: "تم الحذف بنجاح"
      updated_successfully: "تم التحديث بنجاح"
      created_successfully: "تم الإنشاء بنجاح"

    pagination:
      first: "الأولى"
      last: "الأخيرة"
      previous: "السابق"
      next: "التالي"
      showing: "عرض %{from} إلى %{to} من %{total} سجل"
      per_page: "لكل صفحة"

  # Greetings (time-based) - Culturally appropriate Arabic
  greetings:
    morning: "صباح الخير"
    afternoon: "مساء الخير"
    evening: "مساء الخير"
    welcome: "أهلاً وسهلاً"
    welcome_back: "أهلاً بعودتك"
    hello: "مرحبًا"
    goodbye: "مع السلامة"
    thank_you: "شكرًا لك"
```

---

## ActiveRecord Translations

### English ActiveRecord

```yaml
# config/locales/en/activerecord.en.yml
en:
  activerecord:
    models:
      user:
        one: "User"
        other: "Users"
      transaction:
        one: "Transaction"
        other: "Transactions"
      account:
        one: "Account"
        other: "Accounts"

    attributes:
      user:
        email: "Email"
        password: "Password"
        password_confirmation: "Password confirmation"
        first_name: "First name"
        last_name: "Last name"
        full_name: "Full name"
        phone_number: "Phone number"
        created_at: "Created at"
        updated_at: "Updated at"
      transaction:
        amount: "Amount"
        description: "Description"
        category: "Category"
        date: "Date"
        status: "Status"
      account:
        name: "Name"
        balance: "Balance"
        currency: "Currency"
        account_number: "Account number"

    errors:
      models:
        user:
          attributes:
            email:
              taken: "is already registered"
              invalid: "is not a valid email address"
            password:
              too_short: "must be at least %{count} characters"
      messages:
        record_invalid: "Validation failed: %{errors}"
        restrict_dependent_destroy:
          has_one: "Cannot delete record because dependent %{record} exists"
          has_many: "Cannot delete record because dependent %{record} exist"
        required: "must exist"
        taken: "has already been taken"
        blank: "can't be blank"
        present: "must be blank"
        too_long:
          one: "is too long (maximum is 1 character)"
          other: "is too long (maximum is %{count} characters)"
        too_short:
          one: "is too short (minimum is 1 character)"
          other: "is too short (minimum is %{count} characters)"
        wrong_length:
          one: "is the wrong length (should be 1 character)"
          other: "is the wrong length (should be %{count} characters)"
        not_a_number: "is not a number"
        not_an_integer: "must be an integer"
        greater_than: "must be greater than %{count}"
        greater_than_or_equal_to: "must be greater than or equal to %{count}"
        equal_to: "must be equal to %{count}"
        less_than: "must be less than %{count}"
        less_than_or_equal_to: "must be less than or equal to %{count}"
        other_than: "must be other than %{count}"
        odd: "must be odd"
        even: "must be even"
        invalid: "is invalid"
        confirmation: "doesn't match %{attribute}"
        accepted: "must be accepted"
        empty: "can't be empty"
        inclusion: "is not included in the list"
        exclusion: "is reserved"
        not_saved:
          one: "1 error prohibited this %{resource} from being saved:"
          other: "%{count} errors prohibited this %{resource} from being saved:"
```

### Arabic ActiveRecord (with 6 plural forms)

```yaml
# config/locales/ar/activerecord.ar.yml
ar:
  activerecord:
    models:
      user:
        zero: "مستخدمين"
        one: "مستخدم"
        two: "مستخدمان"
        few: "مستخدمين"
        many: "مستخدمًا"
        other: "مستخدم"
      transaction:
        zero: "معاملات"
        one: "معاملة"
        two: "معاملتان"
        few: "معاملات"
        many: "معاملة"
        other: "معاملة"
      account:
        zero: "حسابات"
        one: "حساب"
        two: "حسابان"
        few: "حسابات"
        many: "حسابًا"
        other: "حساب"

    attributes:
      user:
        email: "البريد الإلكتروني"
        password: "كلمة المرور"
        password_confirmation: "تأكيد كلمة المرور"
        first_name: "الاسم الأول"
        last_name: "اسم العائلة"
        full_name: "الاسم الكامل"
        phone_number: "رقم الهاتف"
        created_at: "تاريخ الإنشاء"
        updated_at: "تاريخ التحديث"
      transaction:
        amount: "المبلغ"
        description: "الوصف"
        category: "الفئة"
        date: "التاريخ"
        status: "الحالة"
      account:
        name: "الاسم"
        balance: "الرصيد"
        currency: "العملة"
        account_number: "رقم الحساب"

    errors:
      models:
        user:
          attributes:
            email:
              taken: "مسجّل مسبقًا"
              invalid: "غير صالح"
            password:
              too_short: "يجب أن تكون %{count} أحرف على الأقل"
      messages:
        record_invalid: "فشل التحقق: %{errors}"
        restrict_dependent_destroy:
          has_one: "لا يمكن حذف السجل لوجود %{record} مرتبط"
          has_many: "لا يمكن حذف السجل لوجود %{record} مرتبطة"
        required: "مطلوب"
        taken: "محجوز مسبقًا"
        blank: "لا يمكن أن يكون فارغًا"
        present: "يجب أن يكون فارغًا"
        too_long:
          zero: "طويل جدًا (الحد الأقصى صفر أحرف)"
          one: "طويل جدًا (الحد الأقصى حرف واحد)"
          two: "طويل جدًا (الحد الأقصى حرفان)"
          few: "طويل جدًا (الحد الأقصى %{count} أحرف)"
          many: "طويل جدًا (الحد الأقصى %{count} حرفًا)"
          other: "طويل جدًا (الحد الأقصى %{count} حرف)"
        too_short:
          zero: "قصير جدًا (الحد الأدنى صفر أحرف)"
          one: "قصير جدًا (الحد الأدنى حرف واحد)"
          two: "قصير جدًا (الحد الأدنى حرفان)"
          few: "قصير جدًا (الحد الأدنى %{count} أحرف)"
          many: "قصير جدًا (الحد الأدنى %{count} حرفًا)"
          other: "قصير جدًا (الحد الأدنى %{count} حرف)"
        wrong_length:
          zero: "الطول غير صحيح (يجب أن يكون صفر أحرف)"
          one: "الطول غير صحيح (يجب أن يكون حرفًا واحدًا)"
          two: "الطول غير صحيح (يجب أن يكون حرفين)"
          few: "الطول غير صحيح (يجب أن يكون %{count} أحرف)"
          many: "الطول غير صحيح (يجب أن يكون %{count} حرفًا)"
          other: "الطول غير صحيح (يجب أن يكون %{count} حرف)"
        not_a_number: "ليس رقمًا"
        not_an_integer: "يجب أن يكون عددًا صحيحًا"
        greater_than: "يجب أن يكون أكبر من %{count}"
        greater_than_or_equal_to: "يجب أن يكون أكبر من أو يساوي %{count}"
        equal_to: "يجب أن يساوي %{count}"
        less_than: "يجب أن يكون أقل من %{count}"
        less_than_or_equal_to: "يجب أن يكون أقل من أو يساوي %{count}"
        other_than: "يجب أن يكون مختلفًا عن %{count}"
        odd: "يجب أن يكون فرديًا"
        even: "يجب أن يكون زوجيًا"
        invalid: "غير صالح"
        confirmation: "غير مطابق لـ %{attribute}"
        accepted: "يجب قبوله"
        empty: "لا يمكن أن يكون فارغًا"
        inclusion: "غير مدرج في القائمة"
        exclusion: "محجوز"
        not_saved:
          zero: "لم يتم الحفظ:"
          one: "خطأ واحد منع حفظ %{resource}:"
          two: "خطآن منعا حفظ %{resource}:"
          few: "%{count} أخطاء منعت حفظ %{resource}:"
          many: "%{count} خطأً منع حفظ %{resource}:"
          other: "%{count} خطأ منع حفظ %{resource}:"
```
