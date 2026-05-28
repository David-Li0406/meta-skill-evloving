---
name: nodejs-best-practices
description: Node.js best practices e patterns
triggers: [nodejs, node, express, nestjs, typescript, npm, yarn]
sources:
  - https://github.com/goldbergyoni/nodebestpractices
  - https://github.com/expressjs/express
  - https://github.com/nestjs/nest
---

# Node.js Best Practices

**Convenções baseadas em nodebestpractices e frameworks populares.**

---

## Framework Recomendado

### Express (Leve e Flexível)

**Para APIs simples e microserviços:**

```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/users', async (req, res) => {
  const users = await getUsers();
  res.json(users);
});
```

### NestJS (Estruturado e TypeScript)

**Para projetos maiores com arquitetura em módulos:**

```typescript
import { Module, Controller, Get } from '@nestjs/common';

@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    return this.usersService.findAll();
  }
}
```

---

## Estrutura de Projeto

### Express

```
project/
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── middleware/
│   └── app.js
├── tests/
└── package.json
```

### NestJS

```
project/
├── src/
│   ├── users/
│   │   ├── users.module.ts
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   └── users.entity.ts
│   └── app.module.ts
└── package.json
```

---

## Error Handling

```javascript
// Express
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

// NestJS
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    // Handle error
  }
}
```

---

## Environment Variables

**SEMPRE usar variáveis de ambiente:**

```javascript
require('dotenv').config();

const config = {
  port: process.env.PORT || 3000,
  dbUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
};
```

---

## Checklist

- [ ] Error handling implementado
- [ ] Variáveis de ambiente configuradas
- [ ] Estrutura de projeto organizada
- [ ] TypeScript (quando usar NestJS)
- [ ] Testes configurados

