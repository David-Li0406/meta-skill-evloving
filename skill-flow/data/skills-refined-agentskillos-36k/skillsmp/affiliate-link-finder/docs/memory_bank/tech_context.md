# Tech Context - Technologies & Frameworks

## Core Framework
| Technology | Version | Purpose |
|------------|---------|---------|
| **Flutter** | 3.38.7+ | Cross-platform UI framework |
| **Dart** | 3.x | Programming language |

## State Management
| Package | Version | Usage |
|---------|---------|-------|
| `provider` | ^6.1.1 | ChangeNotifier-based state |
| `get_it` | ^7.6.4 | Service locator / DI |

## Backend Services
| Package | Version | Purpose |
|---------|---------|---------|
| `firebase_core` | ^3.0.0 | Firebase initialization |
| `firebase_auth` | ^5.0.0 | User authentication |
| `cloud_firestore` | ^5.0.0 | NoSQL database |

## UI & UX
| Package | Version | Purpose |
|---------|---------|---------|
| `google_fonts` | ^6.1.0 | Typography |
| `fl_chart` | ^0.68.0 | Charts and visualizations |
| `cupertino_icons` | ^1.0.6 | iOS-style icons |
| **`pdf`** | ^3.11.0 | PDF generation (Report Export) |
| **`printing`** | ^5.13.0 | Print and Share PDFs |

## Notifications
| Package | Version | Purpose |
|---------|---------|---------|
| `flutter_local_notifications` | ^17.0.0 | Local push notifications |

## Utilities
| Package | Version | Purpose |
|---------|---------|---------|
| `url_launcher` | ^6.2.0 | Open external URLs |
| `share_plus` | ^9.0.0 | Native share sheet |
| `uuid` | ^4.0.0 | Unique ID generation |
| **`intl`** | ^0.19.0 | Date formatting/localization |

## Development Tools
| Tool | Purpose |
|------|---------|
| `flutter_lints` | Static analysis rules |
| `mockito` | Unit test mocking |
| `flutter_test` | Widget testing |

## Platform Requirements
- **Android**: SDK 21+ (Android 5.0 Lollipop)
- **iOS**: iOS 15.0+
- **Web**: Chromium-based browsers

## 2026 Compliance
- **16KB Page Alignment**: Required for May 2026 Google Play
- **Gradle**: 8.5.1+ with NDK r28+
- **Build Verification**: `flutter build appbundle --analyze-size`

## File Structure
```
lib/
├── application/       # ViewModels & Use Cases
├── config/            # DI setup (locator.dart)
├── domain/            # Entities, Services, Ports
├── infrastructure/    # Firebase Repos, Services
└── presentation/      # Screens, Widgets, Themes
```

## External Integrations
| Service | Purpose | Status |
|---------|---------|--------|
| Firebase Auth | User accounts | ✅ Configured |
| Firebase Firestore | Data persistence | ✅ Configured |
| Amazon Associates | Affiliate revenue | 🔧 Placeholder tags |

## Documentation Roadmap
- **[Developer Handoff Summary](file:///Users/lycanbeats/Desktop/adhd_supplement_app/docs/developer_summary.md)**: Technical "Source of Truth" for backend and logic implementation.
