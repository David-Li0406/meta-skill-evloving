# 語言生態系與版本處理

本文件說明各程式語言生態系的相依性檔案、版本檢測方式與套件 Registry。

---

## JavaScript / TypeScript / Node.js

### 相依性檔案
- **主要**：`package.json`
- **鎖定檔**：`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`

### 版本格式範例
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "next": "14.2.0",
    "express": "~4.21.2"
  }
}
```

### 套件 Registry
- **npm**：`https://registry.npmjs.org/{package}/latest`

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| React | hooks, context, suspense, error-boundaries |
| Next.js | routing, middleware, api-routes, server-components |
| Express | middleware, routing, error-handling |
| Tailwind CSS | utilities, dark-mode, customization |

---

## Python

### 相依性檔案
- `requirements.txt`
- `pyproject.toml`
- `Pipfile`

### 版本格式範例
```txt
# requirements.txt
django==4.2.0
flask>=2.0.0
fastapi~=0.100.0
```

```toml
# pyproject.toml
[tool.poetry.dependencies]
django = "^4.2.0"
```

### 套件 Registry
- **PyPI**：`https://pypi.org/pypi/{package}/json`

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| Django | models, views, ORM, middleware |
| Flask | routing, blueprints, templates |
| FastAPI | async, type-hints, dependency-injection |

---

## Ruby

### 相依性檔案
- **主要**：`Gemfile`
- **鎖定檔**：`Gemfile.lock`

### 版本格式範例
```ruby
# Gemfile
gem 'rails', '~> 7.0.8'
gem 'sinatra', '>= 3.0.0'
```

### 套件 Registry
- **RubyGems**：`https://rubygems.org/api/v1/gems/{gem}.json`

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| Rails | ActiveRecord, routing, controllers |
| Sinatra | routing, middleware, helpers |

---

## Go

### 相依性檔案
- **主要**：`go.mod`
- **鎖定檔**：`go.sum`

### 版本格式範例
```go
// go.mod
require (
    github.com/gin-gonic/gin v1.9.1
    github.com/labstack/echo/v4 v4.11.0
)
```

### 套件 Registry
- **pkg.go.dev**：官方文件
- **GitHub Releases**：版本資訊

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| Gin | routing, middleware, JSON-binding |
| Echo | routing, middleware, context |

---

## Rust

### 相依性檔案
- **主要**：`Cargo.toml`
- **鎖定檔**：`Cargo.lock`

### 版本格式範例
```toml
# Cargo.toml
[dependencies]
tokio = "1.35.0"
axum = "0.7.0"
serde = { version = "1.0", features = ["derive"] }
```

### 套件 Registry
- **crates.io**：`https://crates.io/api/v1/crates/{crate}`

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| Tokio | async-runtime, futures, I/O |
| Axum | routing, extractors, handlers |

---

## PHP

### 相依性檔案
- **主要**：`composer.json`
- **鎖定檔**：`composer.lock`

### 版本格式範例
```json
{
  "require": {
    "laravel/framework": "^10.0",
    "symfony/console": "^6.0"
  }
}
```

### 套件 Registry
- **Packagist**：`https://repo.packagist.org/p2/{vendor}/{package}.json`

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| Laravel | Eloquent, routing, middleware |
| Symfony | bundles, services, Doctrine |

---

## Java / Kotlin

### 相依性檔案
- **Maven**：`pom.xml`
- **Gradle**：`build.gradle`, `build.gradle.kts`

### 版本格式範例
```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.1.0</version>
</dependency>
```

```kotlin
// build.gradle.kts
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:3.1.0")
}
```

### 套件 Registry
- **Maven Central**：官方搜尋 API

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| Spring Boot | annotations, beans, REST, JPA |

---

## .NET / C#

### 相依性檔案
- `*.csproj`
- `packages.config`
- `Directory.Build.props`

### 版本格式範例
```xml
<!-- *.csproj -->
<ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc" Version="2.2.0" />
</ItemGroup>
```

### 套件 Registry
- **NuGet**：`https://api.nuget.org/v3-flatcontainer/{package}/index.json`

### 常見框架
| 框架 | 常用查詢主題 |
|------|--------------|
| ASP.NET Core | MVC, Razor, Entity Framework, DI |

---

## 升級指南模板

當發現有較新版本時，使用以下模板提供升級建議：

```markdown
## {Library} {CurrentVersion} → {LatestVersion} 升級指南

### Breaking Changes
- [列出 API 移除/變更]
- [行為變更]
- [相依性需求變更]

### 遷移步驟
1. 更新相依性檔案
2. 安裝/更新：{對應的安裝指令}
3. 必要的程式碼變更
4. 執行測試

### 是否建議升級？
✅ **建議**：[效益大於成本的情況]
⚠️ **暫緩**：[建議等待的原因]

**預估工時**：{Low|Medium|High}（{時間估計}）
```
