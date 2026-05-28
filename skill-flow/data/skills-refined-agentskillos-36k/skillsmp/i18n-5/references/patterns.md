# Internationalization

## Patterns

### **Next Intl Setup**
  #### **Description**
next-intl for Next.js App Router
  #### **Example**
    // middleware.ts
    import createMiddleware from "next-intl/middleware";
    
    export default createMiddleware({
      locales: ["en", "es", "fr", "de"],
      defaultLocale: "en",
    });
    
    export const config = {
      matcher: ["/((?!api|_next|.*\..*).*)"],
    };
    
    
    // app/[locale]/layout.tsx
    import { NextIntlClientProvider } from "next-intl";
    import { getMessages } from "next-intl/server";
    
    export default async function LocaleLayout({
      children,
      params: { locale },
    }) {
      const messages = await getMessages();
    
      return (
        <html lang={locale}>
          <body>
            <NextIntlClientProvider messages={messages}>
              {children}
            </NextIntlClientProvider>
          </body>
        </html>
      );
    }
    
    
    // messages/en.json
    {
      "HomePage": {
        "title": "Welcome to our app",
        "greeting": "Hello, {name}!"
      }
    }
    
    // messages/es.json
    {
      "HomePage": {
        "title": "Bienvenido a nuestra app",
        "greeting": "Hola, {name}!"
      }
    }
    
    
    // app/[locale]/page.tsx
    import { useTranslations } from "next-intl";
    
    export default function HomePage() {
      const t = useTranslations("HomePage");
    
      return (
        <div>
          <h1>{t("title")}</h1>
          <p>{t("greeting", { name: "John" })}</p>
        </div>
      );
    }
    
### **Date Formatting**
  #### **Description**
Locale-aware date formatting
  #### **Example**
    import { useFormatter } from "next-intl";
    
    function DateDisplay({ date }) {
      const format = useFormatter();
    
      return (
        <div>
          <p>{format.dateTime(date, { dateStyle: "long" })}</p>
          <p>{format.relativeTime(date)}</p>
        </div>
      );
    }
    
    // Or with Intl API directly
    const formatted = new Intl.DateTimeFormat(locale, {
      dateStyle: "long",
      timeStyle: "short",
    }).format(date);
    
### **Number Formatting**
  #### **Description**
Locale-aware number and currency
  #### **Example**
    import { useFormatter } from "next-intl";
    
    function PriceDisplay({ amount, currency }) {
      const format = useFormatter();
    
      return (
        <span>
          {format.number(amount, {
            style: "currency",
            currency,
          })}
        </span>
      );
    }
    
    // Results by locale:
    // en-US: $1,234.56
    // de-DE: 1.234,56 $
    // ja-JP: $1,234
    

## Anti-Patterns

### **String Concatenation**
  #### **Description**
Building sentences from parts
  #### **Wrong**
t('hello') + ' ' + name + '!'
  #### **Right**
t('greeting', { name })
### **Date Manual Format**
  #### **Description**
Manual date formatting
  #### **Wrong**
date.getMonth() + '/' + date.getDate()
  #### **Right**
Use Intl.DateTimeFormat or library
### **Hardcoded Strings**
  #### **Description**
User-facing strings not in translations
  #### **Wrong**
<button>Submit</button>
  #### **Right**
<button>{t('submit')}</button>