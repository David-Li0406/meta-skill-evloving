# 国内镜像源配置

## Ubuntu/Debian APT 镜像

### 清华大学 (tuna)

```dockerfile
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list \
    && sed -i 's@//.*security.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list
```

### 阿里云

```dockerfile
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.aliyun.com@g' /etc/apt/sources.list \
    && sed -i 's@//.*security.ubuntu.com@//mirrors.aliyun.com@g' /etc/apt/sources.list
```

### 中科大 (ustc)

```dockerfile
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list \
    && sed -i 's@//.*security.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
```

## Python pip 镜像

### 清华大学

```dockerfile
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

或创建配置文件：

```dockerfile
RUN mkdir -p ~/.pip && echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\ntrusted-host = pypi.tuna.tsinghua.edu.cn" > ~/.pip/pip.conf
```

## Node.js npm 镜像

### 淘宝镜像

```dockerfile
RUN npm config set registry https://registry.npmmirror.com
```

### pnpm

```dockerfile
RUN pnpm config set registry https://registry.npmmirror.com
```

### yarn

```dockerfile
RUN yarn config set registry https://registry.npmmirror.com
```

## Alpine APK 镜像

### 清华大学

```dockerfile
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
```

## Go Proxy

```dockerfile
ENV GOPROXY=https://goproxy.cn,direct
```

## Rust Cargo 镜像

创建 `~/.cargo/config`：

```toml
[source.crates-io]
replace-with = 'tuna'

[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

## 完整示例

```dockerfile
FROM ubuntu:22.04

# 配置 APT 镜像源
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list \
    && sed -i 's@//.*security.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list

# 安装 Python
RUN apt-get update && apt-get install -y python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 配置 pip 镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
