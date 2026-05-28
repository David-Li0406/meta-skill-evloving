---
name: Server Deploy
description: Sunucuyu GitHub ile senkronize etmek ve deploy yapmak için kullanılır
---

# Server Deploy Skill

## Ne Zaman Kullanılır
- Kodu sunucuya deploy etmek istediğinde
- GitHub değişikliklerini sunucuya yansıtmak istediğinde
- Sunucu build/restart işlemleri gerektiğinde

## Server Gemini'ye Verilecek Komutlar

### Hızlı Deploy (Script ile)
```bash
cd /var/www/prosektorweb && ./server-sync.sh
```

### Manuel Deploy
```bash
cd /var/www/prosektorweb/prosektorweb
git fetch origin
git reset --hard origin/main
rm -rf .next node_modules/.cache
npm install
npx prisma generate
npm run build
pm2 restart all
```

### Sadece Restart
```bash
pm2 restart all
```

### Log Kontrolü
```bash
pm2 logs --lines 50
```

## Doğrulama
- `git log --oneline -1` → En son commit'i göster
- `curl -I https://prosektorweb.com` → 200 OK dönmeli
