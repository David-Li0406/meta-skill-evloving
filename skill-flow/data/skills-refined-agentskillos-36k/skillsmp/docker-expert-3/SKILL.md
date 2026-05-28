---
name: docker-expert
description: Criação e otimização de ambientes Docker para desenvolvimento e produção PHP/Laravel. Usar para criar Dockerfiles, configurar docker-compose para dev e prod, otimizar imagens, configurar multi-stage builds, networking entre containers, volumes, e troubleshooting de containers.
---

# Docker Expert

Skill para containerização de aplicações PHP/Laravel.

## Estrutura de Arquivos Docker

```
project/
├── docker/
│   ├── php/
│   │   ├── Dockerfile          # Imagem PHP
│   │   └── php.ini             # Configurações PHP
│   ├── nginx/
│   │   ├── Dockerfile          # Imagem Nginx (prod)
│   │   └── default.conf        # Config Nginx
│   └── mysql/
│       └── my.cnf              # Config MySQL
├── docker-compose.yml          # Desenvolvimento
├── docker-compose.prod.yml     # Produção
└── .dockerignore
```

## Dockerfile PHP - Desenvolvimento

```dockerfile
FROM php:8.3-fpm

# Argumentos
ARG USER_ID=1000
ARG GROUP_ID=1000

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Extensões PHP
RUN docker-php-ext-install \
    pdo_mysql \
    mbstring \
    exif \
    pcntl \
    bcmath \
    gd \
    zip \
    opcache

# Redis
RUN pecl install redis && docker-php-ext-enable redis

# Xdebug (dev only)
RUN pecl install xdebug && docker-php-ext-enable xdebug

# Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Criar usuário não-root
RUN groupadd -g ${GROUP_ID} developer \
    && useradd -u ${USER_ID} -g developer -m developer

# Diretório de trabalho
WORKDIR /var/www/html

# Permissões
RUN chown -R developer:developer /var/www/html

USER developer

EXPOSE 9000
CMD ["php-fpm"]
```

## Dockerfile PHP - Produção (Multi-stage)

```dockerfile
# Stage 1: Composer dependencies
FROM composer:2 as composer

WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader --prefer-dist

COPY . .
RUN composer dump-autoload --optimize --classmap-authoritative

# Stage 2: Frontend assets
FROM node:20-alpine as frontend

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 3: Production image
FROM php:8.3-fpm-alpine

# Dependências mínimas
RUN apk add --no-cache \
    libpng \
    libzip \
    icu-libs

# Extensões PHP
RUN docker-php-ext-install \
    pdo_mysql \
    bcmath \
    opcache \
    zip

# Redis
RUN apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apk del .build-deps

# Configurações PHP para produção
COPY docker/php/php.ini /usr/local/etc/php/conf.d/99-production.ini

WORKDIR /var/www/html

# Copiar aplicação
COPY --from=composer /app/vendor ./vendor
COPY --from=frontend /app/public/build ./public/build
COPY . .

# Permissões
RUN chown -R www-data:www-data storage bootstrap/cache \
    && chmod -R 775 storage bootstrap/cache

# Otimizações Laravel
RUN php artisan config:cache \
    && php artisan route:cache \
    && php artisan view:cache

USER www-data

EXPOSE 9000
CMD ["php-fpm"]
```

## docker-compose.yml - Desenvolvimento

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
      args:
        USER_ID: ${USER_ID:-1000}
        GROUP_ID: ${GROUP_ID:-1000}
    container_name: ${APP_NAME:-laravel}_app
    restart: unless-stopped
    volumes:
      - .:/var/www/html
      - ./docker/php/php.ini:/usr/local/etc/php/conf.d/99-custom.ini
    networks:
      - app-network
    depends_on:
      - mysql
      - redis

  nginx:
    image: nginx:alpine
    container_name: ${APP_NAME:-laravel}_nginx
    restart: unless-stopped
    ports:
      - "${APP_PORT:-80}:80"
    volumes:
      - .:/var/www/html
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
    networks:
      - app-network
    depends_on:
      - app

  mysql:
    image: mysql:8.0
    container_name: ${APP_NAME:-laravel}_mysql
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${DB_DATABASE:-laravel}
      MYSQL_USER: ${DB_USERNAME:-laravel}
      MYSQL_PASSWORD: ${DB_PASSWORD:-secret}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD:-root}
    ports:
      - "${DB_PORT:-3306}:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./docker/mysql/my.cnf:/etc/mysql/conf.d/custom.cnf
    networks:
      - app-network

  redis:
    image: redis:alpine
    container_name: ${APP_NAME:-laravel}_redis
    restart: unless-stopped
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network

  mailhog:
    image: mailhog/mailhog
    container_name: ${APP_NAME:-laravel}_mail
    ports:
      - "${MAIL_PORT:-1025}:1025"
      - "${MAILHOG_PORT:-8025}:8025"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mysql-data:
  redis-data:
```

## docker-compose.prod.yml - Produção

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: docker/php/Dockerfile.prod
    restart: always
    environment:
      - APP_ENV=production
      - APP_DEBUG=false
    networks:
      - app-network
    depends_on:
      - mysql
      - redis
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/prod.conf:/etc/nginx/conf.d/default.conf
      - ./docker/nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - app-network
    depends_on:
      - app

  mysql:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: ${DB_DATABASE}
      MYSQL_USER: ${DB_USERNAME}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    volumes:
      - mysql-data:/var/lib/mysql
    networks:
      - app-network

  redis:
    image: redis:alpine
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mysql-data:
  redis-data:
```

## Nginx Config

```nginx
server {
    listen 80;
    server_name localhost;
    root /var/www/html/public;
    index index.php;

    charset utf-8;
    client_max_body_size 100M;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_pass app:9000;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_hide_header X-Powered-By;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

## Comandos Úteis

```bash
# Build e iniciar
docker-compose up -d --build

# Logs
docker-compose logs -f app

# Executar Artisan
docker-compose exec app php artisan migrate

# Bash no container
docker-compose exec app bash

# Rebuild sem cache
docker-compose build --no-cache app

# Limpar tudo
docker-compose down -v --rmi all

# Produção
docker-compose -f docker-compose.prod.yml up -d
```

## .dockerignore

```
.git
.gitignore
.env
.env.*
!.env.example
node_modules
vendor
storage/logs/*
storage/framework/cache/*
storage/framework/sessions/*
storage/framework/views/*
bootstrap/cache/*
docker-compose*.yml
Dockerfile*
*.md
.phpunit.result.cache
.php-cs-fixer.cache
```
