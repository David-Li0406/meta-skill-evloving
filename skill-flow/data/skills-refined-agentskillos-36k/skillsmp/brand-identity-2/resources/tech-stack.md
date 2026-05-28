# Al-Huda Technical Stack

**Platform:** Mobile (iOS & Android)  
**Framework:** React Native 0.73+ (Bare Workflow)

---

## Frontend Stack

### Core
| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.2.0 | Core framework |
| react-native | ^0.73.0 | Native platform layer |
| typescript | ^5.3.0 | Type safety |

### Navigation
| Package | Purpose |
|---------|---------|
| @react-navigation/native | Core navigation |
| @react-navigation/stack | Stack navigation |
| @react-navigation/bottom-tabs | Tab navigation |

### State Management
| Package | Purpose |
|---------|---------|
| zustand | Global state (auth, session) |
| @tanstack/react-query | Server state, caching |

### Storage
| Package | Purpose |
|---------|---------|
| react-native-mmkv | Fast key-value storage |
| react-native-keychain | Secure token storage |

### Networking
| Package | Purpose |
|---------|---------|
| axios | HTTP requests |
| socket.io-client | Real-time WebSocket |

### UI & Animation
| Package | Purpose |
|---------|---------|
| react-native-reanimated | Smooth animations |
| react-native-gesture-handler | Touch gestures |
| react-native-fast-image | Optimized images |
| react-native-skia | Advanced graphics |

### Firebase
| Package | Purpose |
|---------|---------|
| @react-native-firebase/app | Firebase core |
| @react-native-firebase/messaging | Push notifications |
| @react-native-firebase/analytics | Usage analytics |

### Utilities
| Package | Purpose |
|---------|---------|
| date-fns | Date formatting |
| uuid | ID generation |
| react-native-geolocation-service | Location services |

---

## Backend Stack

### Framework
- **FastAPI** (Python 3.11+)
- **SQLAlchemy 2.0** (Async ORM)
- **Pydantic v2** (Validation)

### Database
- **PostgreSQL 15+** (Primary database)
- **Redis 7+** (Caching, sessions)

### Authentication
- **JWT tokens** via python-jose
- **OAuth2** for social login

---

## Native Modules (Android)

### App Blocking Module
The app blocking feature requires a custom Kotlin native module:

```kotlin
// android/app/src/main/java/com/quranapp/appblocking/
AppBlockingModule.kt      // React Native bridge
AppBlockingService.kt     // AccessibilityService implementation
```

This module uses Android's AccessibilityService to:
- Monitor app launches
- Block specified package names
- Return user to Quran app

---

## Development Tools

### IDE & Extensions
- **VS Code** with:
  - ESLint
  - Prettier
  - React Native Tools
  - TypeScript Hero

### Debugging
- Flipper (network, performance, logs)
- React Native Debugger
- Reactotron

### Testing
| Tool | Purpose |
|------|---------|
| Jest | Unit tests |
| @testing-library/react-native | Component tests |
| Detox | E2E tests |

---

## Project Structure

```
src/
├── app/
│   ├── App.tsx
│   ├── navigation/
│   └── providers/
├── core/
│   ├── api/
│   ├── constants/
│   ├── theme/
│   └── utils/
├── features/
│   ├── auth/
│   ├── quran/
│   ├── goals/
│   ├── focus-mode/
│   ├── social/
│   ├── prayers/
│   └── duas/
├── shared/
│   ├── components/
│   ├── hooks/
│   └── services/
└── types/
```

---

## Build Commands

### Development
```bash
# Install dependencies
npm install

# iOS (requires macOS)
cd ios && pod install && cd ..
npm run ios

# Android
npm run android
```

### Production
```bash
# Android
cd android && ./gradlew bundleRelease

# iOS
cd ios && xcodebuild -workspace QuranApp.xcworkspace -scheme QuranApp archive
```

---

## Performance Guidelines

1. **Use MMKV** instead of AsyncStorage for faster reads
2. **Memoize components** with React.memo for lists
3. **Optimize images** with react-native-fast-image
4. **Lazy load** feature screens
5. **Cache API responses** with React Query

---

## Memory Considerations

This project is optimized for development on low-RAM machines (4GB):
- React Native builds use ~2-3GB RAM (vs Flutter's 4-6GB)
- Use `npm run android -- --no-daemon` to reduce memory
- Close other applications during builds
