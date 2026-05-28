# Dockerfile 编写规范

## 基本原则

1. **使用官方基础镜像**，指定明确版本标签
2. **减少层数**，合并相关 RUN 指令
3. **利用构建缓存**，将变化频繁的指令放在后面
4. **清理缓存**，减小镜像体积

## 标准结构

```dockerfile
# ============================================================
# 基础镜像
# ============================================================
FROM ubuntu:22.04

# ============================================================
# 元信息
# ============================================================
LABEL maintainer="your@email.com"
LABEL description="Development environment"

# ============================================================
# 构建参数
# ============================================================
ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=dev

# ============================================================
# 环境变量
# ============================================================
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
ENV LANG=C.UTF-8

# ============================================================
# 系统配置（镜像源、时区等）
# ============================================================
# 配置镜像源（见 mirrors.md）
RUN ...

# ============================================================
# 安装系统依赖
# ============================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
        package1 \
        package2 \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# 创建用户（与宿主机权限一致）
# ============================================================
RUN groupadd -g ${HOST_GID} ${HOST_USER} \
    && useradd -m -u ${HOST_UID} -g ${HOST_GID} -s /bin/bash ${HOST_USER}

# ============================================================
# 安装开发工具和语言运行时
# ============================================================
# 根据需求安装

# ============================================================
# 配置工作目录
# ============================================================
WORKDIR /workspace

# ============================================================
# 切换用户
# ============================================================
USER ${HOST_USER}

# ============================================================
# 入口点
# ============================================================
CMD ["/bin/bash"]
```

## 关键规范

### 1. 包安装规范

```dockerfile
# ✅ 正确：合并命令，清理缓存，按字母排序
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        vim \
        wget \
    && rm -rf /var/lib/apt/lists/*

# ❌ 错误：多个 RUN，不清理缓存
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
```

### 2. 用户权限规范

```dockerfile
# 使用 ARG 接收宿主机用户信息
ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=dev

# 创建与宿主机一致的用户
RUN groupadd -g ${HOST_GID} ${HOST_USER} \
    && useradd -m -u ${HOST_UID} -g ${HOST_GID} -s /bin/bash ${HOST_USER}
```

### 3. 多阶段构建（生产环境）

```dockerfile
# 构建阶段
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 运行阶段
FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/main.js"]
```

### 4. COPY vs ADD

```dockerfile
# ✅ 优先使用 COPY（更明确）
COPY package.json ./

# 只在需要解压或远程 URL 时使用 ADD
ADD https://example.com/file.tar.gz /tmp/
```

## 常见问题

### 权限问题

如果容器内创建的文件在宿主机无法访问：
- 确保 Dockerfile 中用户 UID/GID 与宿主机一致
- 检查 .env 文件是否正确生成

### 缓存失效

如果修改代码后构建很慢：
- 将 `COPY . .` 放在安装依赖之后
- 先复制依赖声明文件，安装依赖，再复制源码
