---
name: docker-deploy
description: Docker部署技能。生成Docker配置、docker-compose编排、部署脚本，支持开发和生产环境。
---

# Skill: Docker Deploy（Docker部署）

## 技能描述

本技能用于生成Docker部署配置，包括Dockerfile、docker-compose.yml、部署脚本，支持开发环境和生产环境部署。

## 适用场景

- 项目容器化部署
- 开发环境搭建
- 生产环境部署

## 核心能力

### 1. Dockerfile生成
- 前端项目Dockerfile
- 后端项目Dockerfile
- 多阶段构建优化

### 2. Docker Compose编排
- 多服务编排
- 网络配置
- 数据卷管理

### 3. 部署脚本
- 一键部署脚本
- 环境变量管理
- 健康检查配置

## 执行流程

```
1. 分析项目结构和技术栈
   ↓
2. 生成前端Dockerfile
   ↓
3. 生成后端Dockerfile
   ↓
4. 生成docker-compose.yml
   ↓
5. 生成.env配置文件
   ↓
6. 生成部署脚本
   ↓
7. 生成部署文档
```

## 输出文件

```
deploy/
├── docker/
│   ├── frontend/
│   │   └── Dockerfile
│   ├── backend/
│   │   └── Dockerfile
│   └── nginx/
│       └── nginx.conf
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── deploy.sh
└── README.md
```

## Dockerfile模板

### 前端Dockerfile（Vue3）
```dockerfile
# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci --registry=https://registry.npmmirror.com

# 构建
COPY . .
RUN npm run build

# 运行阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### 后端Dockerfile（Spring Boot）
```dockerfile
# 构建阶段
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# 复制pom.xml并下载依赖
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 复制源码并构建
COPY src ./src
RUN mvn package -DskipTests

# 运行阶段
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# 复制jar包
COPY --from=builder /app/target/*.jar app.jar

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -q --spider http://localhost:8080/actuator/health || exit 1

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 后端Dockerfile（FastAPI）
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制源码
COPY . .

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose模板

### 开发环境（docker-compose.yml）
```yaml
version: '3.8'

services:
  # 前端服务
  frontend:
    build:
      context: ./frontend
      dockerfile: ../deploy/docker/frontend/Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - app-network

  # 后端服务
  backend:
    build:
      context: ./backend
      dockerfile: ../deploy/docker/backend/Dockerfile
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=dev
      - DATABASE_URL=jdbc:postgresql://postgres:5432/${DB_NAME}
      - DATABASE_USERNAME=${DB_USER}
      - DATABASE_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
      - ./sql/init-data.sql:/docker-entrypoint-initdb.d/02-init-data.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### 生产环境（docker-compose.prod.yml）
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deploy/docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend
    networks:
      - app-network
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: ../deploy/docker/backend/Dockerfile
    environment:
      - SPRING_PROFILES_ACTIVE=prod
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G
    networks:
      - app-network
    restart: always

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: always

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: always

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

## 环境变量模板（.env.example）
```bash
# 数据库配置
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=your_secure_password

# Redis配置
REDIS_HOST=redis
REDIS_PORT=6379

# JWT配置
JWT_SECRET=your_jwt_secret_key
JWT_EXPIRATION=7200

# 应用配置
APP_ENV=development
APP_DEBUG=true
```

## 部署脚本模板（deploy.sh）
```bash
#!/bin/bash

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}开始部署...${NC}"

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${RED}错误: .env文件不存在${NC}"
    echo "请复制.env.example为.env并配置环境变量"
    exit 1
fi

# 加载环境变量
export $(cat .env | xargs)

# 构建并启动
if [ "$1" == "prod" ]; then
    echo "生产环境部署..."
    docker-compose -f docker-compose.prod.yml up -d --build
else
    echo "开发环境部署..."
    docker-compose up -d --build
fi

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 健康检查
echo "执行健康检查..."
if curl -s http://localhost:8080/actuator/health | grep -q "UP"; then
    echo -e "${GREEN}后端服务启动成功${NC}"
else
    echo -e "${RED}后端服务启动失败${NC}"
    docker-compose logs backend
    exit 1
fi

echo -e "${GREEN}部署完成！${NC}"
echo "前端地址: http://localhost:3000"
echo "后端地址: http://localhost:8080"
```

## Nginx配置模板
```nginx
server {
    listen 80;
    server_name localhost;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 健康检查
    location /health {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
```

## 常用命令

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f [service_name]

# 重启服务
docker-compose restart [service_name]

# 停止所有服务
docker-compose down

# 清理数据卷
docker-compose down -v

# 重新构建
docker-compose up -d --build

# 进入容器
docker-compose exec [service_name] sh
```

## 质量检查清单

- [ ] Dockerfile使用多阶段构建
- [ ] 服务有健康检查配置
- [ ] 敏感信息通过环境变量传递
- [ ] 数据卷持久化配置
- [ ] 网络隔离配置
- [ ] 资源限制配置（生产环境）
- [ ] 部署脚本可执行

## 注意事项

1. **安全第一**：不要在Dockerfile或docker-compose.yml中硬编码敏感信息
2. **镜像优化**：使用Alpine镜像减小体积
3. **健康检查**：所有服务配置健康检查
4. **日志管理**：配置日志轮转，避免磁盘占满
5. **资源限制**：生产环境配置CPU和内存限制
