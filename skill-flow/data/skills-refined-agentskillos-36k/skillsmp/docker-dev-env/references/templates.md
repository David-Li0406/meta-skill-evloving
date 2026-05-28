# 开发环境模板

## Python 开发环境

### Dockerfile

```dockerfile
FROM python:3.11-slim

LABEL maintainer="dev@example.com"

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=dev

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 配置国内镜像源
RUN sed -i 's@deb.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖和常用工具
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        htop \
        net-tools \
        tree \
        unzip \
        vim \
        zip \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js (用于 npm 包管理)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm config set registry https://registry.npmmirror.com

# 创建用户
RUN groupadd -g ${HOST_GID} ${HOST_USER} \
    && useradd -m -u ${HOST_UID} -g ${HOST_GID} -s /bin/bash ${HOST_USER}

# 配置 pip 镜像
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /workspace
USER ${HOST_USER}

CMD ["/bin/bash"]
```

### docker-compose.yml

```yaml
services:
  python-dev:
    build:
      context: .
      args:
        HOST_UID: ${HOST_UID}
        HOST_GID: ${HOST_GID}
        HOST_USER: ${HOST_USER}
    container_name: python-dev
    volumes:
      - .:/workspace
    stdin_open: true
    tty: true
```

---

## Node.js 开发环境

### Dockerfile

```dockerfile
FROM node:20-slim

LABEL maintainer="dev@example.com"

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=dev

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai

# 配置国内镜像源
RUN sed -i 's@deb.debian.org@mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/debian.sources

# 安装系统依赖和常用工具
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        htop \
        net-tools \
        tree \
        unzip \
        vim \
        zip \
    && rm -rf /var/lib/apt/lists/*

# 修改 node 用户 UID/GID 以匹配宿主机
RUN groupmod -g ${HOST_GID} node \
    && usermod -u ${HOST_UID} -g ${HOST_GID} node

# 配置 npm 镜像
RUN npm config set registry https://registry.npmmirror.com

WORKDIR /workspace
USER node

CMD ["/bin/bash"]
```

### docker-compose.yml

```yaml
services:
  node-dev:
    build:
      context: .
      args:
        HOST_UID: ${HOST_UID}
        HOST_GID: ${HOST_GID}
        HOST_USER: ${HOST_USER}
    container_name: node-dev
    volumes:
      - .:/workspace
      - node_modules:/workspace/node_modules
    ports:
      - "3000:3000"
      - "5173:5173"
    stdin_open: true
    tty: true

volumes:
  node_modules:
```

---

## 通用开发环境

### Dockerfile

```dockerfile
FROM ubuntu:22.04

LABEL maintainer="dev@example.com"

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USER=dev

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai
ENV LANG=C.UTF-8

# 配置国内镜像源
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list \
    && sed -i 's@//.*security.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list

# 安装基础工具
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        htop \
        jq \
        less \
        net-tools \
        openssh-client \
        sudo \
        tree \
        unzip \
        vim \
        wget \
        zip \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js (用于 npm 包管理)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm config set registry https://registry.npmmirror.com

# 创建用户并添加 sudo 权限
RUN groupadd -g ${HOST_GID} ${HOST_USER} \
    && useradd -m -u ${HOST_UID} -g ${HOST_GID} -s /bin/bash ${HOST_USER} \
    && echo "${HOST_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /workspace
USER ${HOST_USER}

CMD ["/bin/bash"]
```

### docker-compose.yml

```yaml
services:
  dev:
    build:
      context: .
      args:
        HOST_UID: ${HOST_UID}
        HOST_GID: ${HOST_GID}
        HOST_USER: ${HOST_USER}
    container_name: dev
    volumes:
      - .:/workspace
    stdin_open: true
    tty: true
```

---

## 文件清单

创建开发环境时需要生成以下文件：

```
project/
├── .env              # 由 init-env.sh 生成
├── Dockerfile
├── docker-compose.yml
├── init-env.sh       # 复制自 skill
├── enter.sh          # 复制自 skill
└── .dockerignore     # 可选
```

### .dockerignore 模板

```
.git
.gitignore
.env
*.md
node_modules
__pycache__
*.pyc
.venv
venv
```
