---
name: Database Operations
description: Prisma veritabanı işlemleri için komutlar ve rehber
---

# Database Operations Skill

## Ne Zaman Kullanılır
- Veritabanı şemasını güncellemek istediğinde
- Seed data eklemek istediğinde
- Kullanıcı oluşturmak/silmek istediğinde
- Veritabanı sorgularında

## Prisma Komutları

### Schema Değişikliği Sonrası
```bash
npx prisma generate      # Client'ı güncelle
npx prisma db push       # Schema'yı DB'ye uygula (dev)
npx prisma migrate dev   # Migration oluştur (prod)
```

### Prisma Studio (GUI)
```bash
npx prisma studio        # Tarayıcıda veritabanı yönetimi
```

## Kullanıcı Oluşturma

### Admin Kullanıcı
```javascript
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

(async () => {
  const prisma = new PrismaClient();
  const hash = await bcrypt.hash('sifre123', 10);
  
  await prisma.user.create({
    data: { 
      name: 'Admin', 
      email: 'admin@email.com', 
      password: hash, 
      role: 'ADMIN' 
    }
  });
  
  console.log('Admin oluşturuldu');
  process.exit(0);
})();
```

### Client Kullanıcı
```javascript
// Role: 'CLIENT' olarak değiştir, companyId ekle
```

## Kullanıcıları Listele
```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

prisma.user.findMany({ select: { email: true, role: true } })
  .then(users => console.log(JSON.stringify(users, null, 2)))
  .then(() => process.exit(0));
```

## Rol Tipleri
- `ADMIN` → /admin paneline erişim
- `CLIENT` → /portal paneline erişim
