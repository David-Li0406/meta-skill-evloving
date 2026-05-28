---
name: Build Systems
description: This skill should be used when the user asks to "configure webpack", "set up vite", "configure build", "optimize bundle", "tree shaking", "code splitting", "gradle build", "xcode build", "foundry build", "turbopack", "esbuild", "rollup", or needs help with frontend bundlers, mobile builds, or Web3 build tooling.
version: 1.0.0
---

# Build Systems

Comprehensive guidance for configuring and optimizing build systems across web, mobile, and Web3 platforms.

## Frontend Bundlers

### Vite (Recommended for Modern Projects)

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    target: 'esnext',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash', 'date-fns']
        }
      }
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8080'
    }
  }
})
```

**Key Features:**
- Native ESM development server
- Instant HMR (Hot Module Replacement)
- Rollup-based production builds
- Built-in TypeScript support

### Webpack 5

```javascript
// webpack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  mode: process.env.NODE_ENV || 'development',
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    clean: true
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        }
      }
    }
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: 'babel-loader'
      },
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader']
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({ template: './src/index.html' }),
    new MiniCssExtractPlugin({ filename: '[name].[contenthash].css' })
  ]
};
```

### esbuild (Ultra-Fast)

```javascript
// esbuild.config.js
require('esbuild').build({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  minify: true,
  sourcemap: true,
  target: ['chrome90', 'firefox88', 'safari14'],
  outdir: 'dist',
  splitting: true,
  format: 'esm',
  loader: {
    '.png': 'file',
    '.svg': 'dataurl'
  }
}).catch(() => process.exit(1));
```

### Build Tool Comparison

| Tool | Dev Speed | Prod Build | Config | Use Case |
|------|-----------|------------|--------|----------|
| Vite | ⚡⚡⚡ | ⚡⚡ | Simple | Modern SPA |
| Webpack | ⚡ | ⚡⚡ | Complex | Legacy, complex |
| esbuild | ⚡⚡⚡ | ⚡⚡⚡ | Simple | Libraries, fast builds |
| Turbopack | ⚡⚡⚡ | ⚡⚡ | Simple | Next.js |
| Rollup | ⚡⚡ | ⚡⚡⚡ | Medium | Libraries |

## Bundle Optimization

### Code Splitting

```javascript
// Dynamic imports for route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

// Named chunks
const Chart = lazy(() => import(/* webpackChunkName: "charts" */ './components/Chart'));
```

### Tree Shaking

Ensure tree shaking works:

```json
// package.json
{
  "sideEffects": false,
  // or specify files with side effects
  "sideEffects": ["*.css", "*.scss"]
}
```

```javascript
// Use named exports (better tree shaking)
export { Button, Input, Modal };

// Avoid default exports of objects
// Bad: export default { Button, Input, Modal }
```

### Bundle Analysis

```bash
# Webpack
npx webpack-bundle-analyzer dist/stats.json

# Vite
npx vite-bundle-visualizer

# General
npx source-map-explorer dist/*.js
```

## Mobile Builds

### iOS (Xcode)

```bash
# Build from command line
xcodebuild -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath build/MyApp.xcarchive \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath build/MyApp.xcarchive \
  -exportPath build/ipa \
  -exportOptionsPlist ExportOptions.plist
```

**ExportOptions.plist:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
</dict>
</plist>
```

### Android (Gradle)

```groovy
// app/build.gradle
android {
    compileSdk 34

    defaultConfig {
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }

    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'),
                          'proguard-rules.pro'
            signingConfig signingConfigs.release
        }
    }

    signingConfigs {
        release {
            storeFile file(RELEASE_STORE_FILE)
            storePassword RELEASE_STORE_PASSWORD
            keyAlias RELEASE_KEY_ALIAS
            keyPassword RELEASE_KEY_PASSWORD
        }
    }
}
```

```bash
# Build APK
./gradlew assembleRelease

# Build AAB (App Bundle)
./gradlew bundleRelease

# Run tests
./gradlew test

# Lint
./gradlew lint
```

### React Native

```bash
# iOS build
npx react-native build-ios --mode Release

# Android build
cd android && ./gradlew assembleRelease

# Using EAS Build (Expo)
eas build --platform ios --profile production
eas build --platform android --profile production
```

### Flutter

```bash
# iOS
flutter build ios --release

# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# Build with flavor
flutter build apk --flavor production --release
```

## Web3 Build Tools

### Foundry (Solidity)

```toml
# foundry.toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
optimizer = true
optimizer_runs = 200

[profile.ci]
verbosity = 4
fuzz_runs = 10000
```

```bash
# Install dependencies
forge install OpenZeppelin/openzeppelin-contracts

# Build
forge build

# Test
forge test -vvv

# Deploy
forge create --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  src/MyContract.sol:MyContract

# Verify on Etherscan
forge verify-contract $CONTRACT_ADDRESS \
  src/MyContract.sol:MyContract \
  --chain mainnet \
  --etherscan-api-key $ETHERSCAN_KEY
```

### Hardhat

```javascript
// hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {},
    mainnet: {
      url: process.env.MAINNET_RPC,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};
```

```bash
# Compile
npx hardhat compile

# Test
npx hardhat test

# Deploy
npx hardhat run scripts/deploy.js --network mainnet

# Verify
npx hardhat verify --network mainnet $CONTRACT_ADDRESS
```

## Monorepo Build Tools

### Turborepo

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "test/**"]
    },
    "lint": {},
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

```bash
# Build all packages
turbo build

# Build specific package
turbo build --filter=@myorg/web

# Run with cache
turbo build --cache-dir=".turbo"
```

### Nx

```bash
# Generate app
nx generate @nx/react:app myapp

# Build
nx build myapp

# Affected builds only
nx affected --target=build

# Dependency graph
nx graph
```

## Performance Optimization

### Caching Strategies

```javascript
// Webpack cache
module.exports = {
  cache: {
    type: 'filesystem',
    buildDependencies: {
      config: [__filename]
    }
  }
};
```

### Parallel Builds

```bash
# Use multiple CPU cores
# Gradle
./gradlew build --parallel

# npm scripts
npm-run-all --parallel build:*
```

### Build Time Analysis

```bash
# Webpack
SPEED_MEASURE_PLUGIN=true webpack

# General timing
time npm run build
```

## CI/CD Build Configuration

### GitHub Actions

```yaml
# .github/workflows/build.yml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: dist/
```

## Additional Resources

### Reference Files

- **`references/bundler-configs.md`** - Complete config examples for all bundlers
- **`references/optimization-checklist.md`** - Build optimization checklist

### Example Files

- **`examples/vite-react-config.js`** - Production Vite config
- **`examples/webpack-advanced.js`** - Advanced Webpack setup
