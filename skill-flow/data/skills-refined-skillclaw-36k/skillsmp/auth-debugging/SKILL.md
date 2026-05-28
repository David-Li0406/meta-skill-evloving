---
name: Auth Debugging
description: NextAuth kimlik doğrulama sorunlarını çözmek için
---

# Auth Debugging Skill

## Yaygın Hatalar ve Çözümleri

### ERR_TOO_MANY_REDIRECTS
**Neden:** Middleware'de sonsuz redirect döngüsü
**Çözüm:**
1. `middleware.ts` → matcher'a `/login` ekle
2. `auth.config.ts` → duplicate redirect kontrollerini kaldır

### 500 Server Error (credentials)
**Neden:** AUTH_SECRET eksik veya bcryptjs yüklü değil
**Çözüm:**
```bash
# .env dosyasına ekle
AUTH_SECRET=random-32-karakter-string

# bcryptjs yükle
npm install bcryptjs
```

### "Hatalı e-posta veya şifre"
**Neden:** Kullanıcı veritabanında yok veya şifre hash'i yanlış
**Çözüm:** Yeni kullanıcı oluştur (database-ops skill'e bak)

## Fallback Admin Bilgileri
auth.ts dosyasında hardcoded:
- Email: `admin@prosektorweb.com` (veya ADMIN_EMAIL env)
- Şifre: `6509d6d5a0e97a0c8d79c76e` (veya ADMIN_PASSWORD env)

## Giriş URL'leri
- `/login` → Müşteri girişi → /portal'a yönlendirir
- `/yonetim-girisi` → Admin girişi → /admin'e yönlendirir

## Debug Logları
```bash
pm2 logs --lines 30 | grep -i "auth\|credential\|error"
```
