# Deep Linking in Flutter

Deep linking enables your Flutter application to open specific screens in response to external URLs from web browsers, push notifications, QR codes, or other applications. This guide covers Android App Links, iOS Universal Links, and custom URL schemes.

## Deep Linking Overview

Deep linking refers to using URLs to navigate directly to specific content within a mobile application. There are three types of deep links:

**Custom URL Schemes:** App-specific URLs (e.g., `myapp://product/123`) that work without domain verification but may show disambiguation dialogs if multiple apps use the same scheme.

**Android App Links:** Verified HTTPS URLs that open directly in your Android app without disambiguation, requiring domain ownership verification.

**iOS Universal Links:** Verified HTTPS URLs that open directly in your iOS app, requiring domain ownership verification through an apple-app-site-association file.

### Benefits of Deep Linking

**Direct navigation** to specific content from external sources like marketing emails, push notifications, and social media.

**Improved user experience** by eliminating manual navigation through multiple screens to reach desired content.

**Attribution tracking** for marketing campaigns and user acquisition channels.

**Platform integration** with features like Spotlight Search on iOS and Google Search on Android.

**Web-to-app continuity** allowing users to seamlessly transition from web content to native app experiences.

## Flutter Version Considerations

Flutter 3.27 and later versions automatically enable deep linking. For earlier versions, manual configuration is required:

### Flutter 3.27+

Deep linking is enabled by default. No additional configuration needed in the Flutter framework itself.

### Flutter Earlier Than 3.27

Add to `ios/Runner/Info.plist`:

```xml
<key>FlutterDeepLinkingEnabled</key>
<true/>
```

### Third-Party Plugin Compatibility

If using third-party plugins for deep linking (like `app_links`), Flutter's default deep link handler may conflict. Disable it:

```xml
<key>FlutterDeepLinkingEnabled</key>
<false/>
```

## Android Deep Linking Configuration

Android supports both custom URL schemes and verified App Links. App Links are recommended for production applications.

### Android Custom URL Schemes

Custom URL schemes use app-specific protocols like `myapp://`.

#### Step 1: Configure AndroidManifest.xml

Edit `android/app/src/main/AndroidManifest.xml` to add intent filters:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
  <application>
    <activity
      android:name=".MainActivity"
      android:exported="true">

      <!-- Existing launch intent filter -->
      <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
      </intent-filter>

      <!-- Deep link intent filter -->
      <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />

        <!-- Custom scheme -->
        <data android:scheme="myapp" />
      </intent-filter>

    </activity>
  </application>
</manifest>
```

This configuration enables URLs like `myapp://product/123` to open your app.

#### Step 2: Add Metadata

Add Flutter deep linking metadata:

```xml
<activity android:name=".MainActivity">
  <!-- ... existing intent filters ... -->

  <meta-data
    android:name="flutter_deeplinking_enabled"
    android:value="true" />
</activity>
```

### Android App Links (HTTPS)

App Links use verified HTTPS URLs and open directly without disambiguation dialogs.

#### Step 1: Host Digital Asset Links File

Create `assetlinks.json` and host it at `https://yourdomain.com/.well-known/assetlinks.json`:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.myapp",
    "sha256_cert_fingerprints":
    ["14:6D:E9:83:C5:73:06:50:D8:EE:B9:95:2F:34:FC:64:16:A0:83:42:E6:1D:BE:A8:8A:04:96:B2:3F:CF:44:E5"]
  }
}]
```

**package_name:** Your app's package name from `build.gradle`.

**sha256_cert_fingerprints:** SHA256 fingerprint of your signing certificate.

#### Step 2: Get SHA256 Fingerprint

For debug builds:

```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```

For release builds:

```bash
keytool -list -v -keystore /path/to/your/keystore.jks -alias your-key-alias
```

Copy the SHA256 fingerprint from the output (remove colons).

#### Step 3: Configure AndroidManifest.xml

Add intent filter with `android:autoVerify="true"`:

```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />

  <data android:scheme="https" />
  <data android:host="yourdomain.com" />
</intent-filter>
```

The `android:autoVerify="true"` attribute triggers Android to verify the association with your domain.

#### Step 4: Add Path Patterns (Optional)

Restrict which paths your app handles:

```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />

  <data android:scheme="https" />
  <data android:host="yourdomain.com" />
  <data android:pathPrefix="/products" />
</intent-filter>
```

This limits app links to URLs starting with `https://yourdomain.com/products`.

### Multiple Domains and Schemes

Support multiple domains or schemes by adding multiple `<data>` tags:

```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />

  <!-- Multiple schemes -->
  <data android:scheme="https" />
  <data android:scheme="http" />

  <!-- Multiple hosts -->
  <data android:host="yourdomain.com" />
  <data android:host="www.yourdomain.com" />

  <!-- Path patterns -->
  <data android:pathPrefix="/products" />
</intent-filter>
```

### Testing Android Deep Links

#### Test Custom URL Schemes

```bash
adb shell am start -W -a android.intent.action.VIEW -d "myapp://product/123" com.example.myapp
```

#### Test App Links

```bash
adb shell am start -W -a android.intent.action.VIEW -d "https://yourdomain.com/product/123" com.example.myapp
```

#### Verify App Links Association

```bash
adb shell dumpsys package domain-preferred-apps
```

Look for your package name and verify the domain association status.

## iOS Deep Linking Configuration

iOS supports both custom URL schemes and Universal Links. Universal Links are recommended for production.

### iOS Custom URL Schemes

Custom URL schemes use app-specific protocols like `myapp://`.

#### Step 1: Configure URL Types in Xcode

1. Open `ios/Runner.xcworkspace` in Xcode
2. Select the Runner target
3. Go to the "Info" tab
4. Expand "URL Types" section
5. Click "+" to add a new URL type
6. Set "URL Schemes" to your custom scheme (e.g., `myapp`)
7. Set "Identifier" to your bundle identifier

Alternatively, edit `ios/Runner/Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleTypeRole</key>
    <string>Editor</string>
    <key>CFBundleURLName</key>
    <string>com.example.myapp</string>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>myapp</string>
    </array>
  </dict>
</array>
```

This enables URLs like `myapp://product/123` to open your app.

### iOS Universal Links

Universal Links use verified HTTPS URLs and provide seamless web-to-app transitions.

#### Step 1: Enable Associated Domains

1. Open `ios/Runner.xcworkspace` in Xcode
2. Select the Runner target
3. Go to "Signing & Capabilities" tab
4. Click "+ Capability" button
5. Add "Associated Domains"
6. Click "+" under Associated Domains
7. Add `applinks:yourdomain.com`

For multiple domains or subdomains:

```
applinks:yourdomain.com
applinks:www.yourdomain.com
applinks:*.yourdomain.com
```

The wildcard `*.yourdomain.com` matches all subdomains.

#### Step 2: Host Apple App Site Association File

Create `apple-app-site-association` (no file extension) and host it at:

- `https://yourdomain.com/.well-known/apple-app-site-association`
- `https://yourdomain.com/apple-app-site-association` (fallback)

File content:

```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAMID.com.example.myapp",
        "paths": [
          "/products/*",
          "/categories/*",
          "NOT /admin/*"
        ]
      }
    ]
  }
}
```

**appID:** Your Team ID (from Apple Developer account) + bundle identifier.

**paths:** Array of path patterns your app handles. Use `*` for wildcards and `NOT` to exclude paths.

#### Step 3: Find Your Team ID

1. Go to https://developer.apple.com/account
2. Navigate to "Membership" section
3. Copy your Team ID

Alternatively, find it in Xcode:
1. Select Runner target
2. Go to "Signing & Capabilities"
3. Team ID is shown under "Signing" section

#### Step 4: Configure Content Type

Serve `apple-app-site-association` with the correct content type:

```
Content-Type: application/json
```

No caching should be enforced to ensure iOS retrieves updates:

```
Cache-Control: no-cache
```

#### Step 5: Validate Association File

Use Apple's validator:

```
https://search.validator.apple.com/
```

Enter your domain URL to verify the association file is properly configured.

### Path Matching Patterns

Universal Links support flexible path matching:

**Exact match:**
```json
"/products/featured"
```

**Wildcard match:**
```json
"/products/*"
```

**Query parameters (ignored):**
```json
"/search"  // Matches /search?q=flutter
```

**Exclusions:**
```json
"NOT /admin/*"
```

**Multiple patterns:**
```json
{
  "paths": [
    "/products/*",
    "/categories/*",
    "/search",
    "NOT /api/*"
  ]
}
```

### Testing iOS Deep Links

#### Test Custom URL Schemes

```bash
xcrun simctl openurl booted "myapp://product/123"
```

#### Test Universal Links

```bash
xcrun simctl openurl booted "https://yourdomain.com/product/123"
```

Note: Universal Links don't work when tapped directly in Safari's address bar. Test by:
- Tapping links in Notes app
- Tapping links in Messages app
- Opening from another app
- Using `xcrun simctl openurl` command

### iOS 14+ Privacy Changes

iOS 14 introduced privacy changes affecting deep linking:

- Users can disable Universal Links per app in Settings
- First launch may show a banner asking to open the app
- Long-press on links shows "Open in App" option

Handle these scenarios gracefully by providing web fallbacks.

## Handling Deep Links in Flutter

Once platform configuration is complete, handle incoming deep links in your Flutter app.

### Using GoRouter

GoRouter automatically handles deep links based on route configuration:

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/products/:id',
      builder: (context, state) {
        final productId = state.pathParameters['id']!;
        return ProductScreen(productId: productId);
      },
    ),
    GoRoute(
      path: '/categories/:category',
      builder: (context, state) {
        final category = state.pathParameters['category']!;
        final sort = state.uri.queryParameters['sort'];
        return CategoryScreen(category: category, sort: sort);
      },
    ),
  ],
);
```

Deep links are automatically routed to matching screens:
- `myapp://products/123` → ProductScreen(productId: '123')
- `https://yourdomain.com/categories/electronics?sort=price` → CategoryScreen

### Using app_links Package

For more control, use the `app_links` package:

```yaml
dependencies:
  app_links: ^6.0.0
```

#### Initial Link Handling

Handle the link that opened the app:

```dart
import 'package:app_links/app_links.dart';

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final _appLinks = AppLinks();
  String? _initialLink;

  @override
  void initState() {
    super.initState();
    _handleInitialLink();
    _handleIncomingLinks();
  }

  Future<void> _handleInitialLink() async {
    try {
      final uri = await _appLinks.getInitialLink();
      if (uri != null) {
        setState(() {
          _initialLink = uri.toString();
        });
        _handleDeepLink(uri);
      }
    } catch (e) {
      print('Error getting initial link: $e');
    }
  }

  void _handleIncomingLinks() {
    _appLinks.uriLinkStream.listen((uri) {
      _handleDeepLink(uri);
    }, onError: (err) {
      print('Error listening to links: $err');
    });
  }

  void _handleDeepLink(Uri uri) {
    print('Received deep link: $uri');

    // Parse and navigate based on URI
    if (uri.pathSegments.isNotEmpty) {
      if (uri.pathSegments[0] == 'products' && uri.pathSegments.length > 1) {
        final productId = uri.pathSegments[1];
        // Navigate to product screen
        context.go('/products/$productId');
      } else if (uri.pathSegments[0] == 'categories') {
        final category = uri.pathSegments.length > 1
            ? uri.pathSegments[1]
            : 'all';
        final sort = uri.queryParameters['sort'];
        context.go('/categories/$category${sort != null ? '?sort=$sort' : ''}');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
    );
  }
}
```

#### Link Stream Handling

Listen to incoming links while the app is running:

```dart
late StreamSubscription<Uri> _linkSubscription;

@override
void initState() {
  super.initState();
  _linkSubscription = _appLinks.uriLinkStream.listen(
    _handleDeepLink,
    onError: (err) {
      print('Error: $err');
    },
  );
}

@override
void dispose() {
  _linkSubscription.cancel();
  super.dispose();
}
```

### Parsing Query Parameters

Extract query parameters from deep link URIs:

```dart
void _handleDeepLink(Uri uri) {
  final queryParams = uri.queryParameters;

  final searchQuery = queryParams['q'];
  final filter = queryParams['filter'];
  final page = int.tryParse(queryParams['page'] ?? '1') ?? 1;

  context.go('/search?q=$searchQuery&filter=$filter&page=$page');
}
```

## Advanced Deep Linking Patterns

### Deferred Deep Links

Deferred deep links work even when the app isn't installed, directing users to the app store first, then to the intended content after installation.

This typically requires third-party services like:
- Firebase Dynamic Links (deprecated)
- Branch.io
- AppsFlyer
- Adjust

Example with Branch:

```yaml
dependencies:
  flutter_branch_sdk: ^7.0.0
```

```dart
import 'package:flutter_branch_sdk/flutter_branch_sdk.dart';

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    super.initState();
    _listenToBranchLinks();
  }

  void _listenToBranchLinks() {
    FlutterBranchSdk.listSession().listen((data) {
      if (data.containsKey('+clicked_branch_link') &&
          data['+clicked_branch_link'] == true) {
        // Handle deferred deep link
        final productId = data['product_id'];
        if (productId != null) {
          context.go('/products/$productId');
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: router,
    );
  }
}
```

### Deep Link Analytics

Track deep link usage for analytics:

```dart
void _handleDeepLink(Uri uri) {
  // Log to analytics
  FirebaseAnalytics.instance.logEvent(
    name: 'deep_link_opened',
    parameters: {
      'link_url': uri.toString(),
      'link_path': uri.path,
      'link_source': uri.queryParameters['utm_source'] ?? 'unknown',
    },
  );

  // Navigate
  _navigateBasedOnUri(uri);
}
```

### Deep Link Error Handling

Handle invalid or expired deep links gracefully:

```dart
void _handleDeepLink(Uri uri) {
  try {
    if (uri.pathSegments.isEmpty) {
      context.go('/');
      return;
    }

    if (uri.pathSegments[0] == 'products' && uri.pathSegments.length > 1) {
      final productId = uri.pathSegments[1];

      // Validate product exists
      if (_isValidProductId(productId)) {
        context.go('/products/$productId');
      } else {
        _showErrorAndNavigateHome('Product not found');
      }
    } else {
      _showErrorAndNavigateHome('Invalid link');
    }
  } catch (e) {
    print('Error handling deep link: $e');
    _showErrorAndNavigateHome('Error opening link');
  }
}

void _showErrorAndNavigateHome(String message) {
  // Show error to user
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text(message)),
  );

  // Navigate to home
  context.go('/');
}
```

## Common Issues and Solutions

### iOS Universal Links Not Working

**Issue:** Tapping links in Safari opens the website instead of the app.

**Solutions:**
- Verify `apple-app-site-association` file is properly hosted and accessible
- Ensure no redirects occur when accessing the file
- Check that file is served with `application/json` content type
- Verify Team ID and bundle identifier are correct
- Test in Notes or Messages apps, not Safari address bar directly
- Reinstall the app to refresh the association

### Android App Links Not Verifying

**Issue:** Links show disambiguation dialog instead of opening directly.

**Solutions:**
- Verify `assetlinks.json` is hosted at the correct location
- Ensure SHA256 fingerprint matches your signing certificate
- Check that `android:autoVerify="true"` is set in the intent filter
- Verify package name matches exactly
- Wait a few minutes after installing for verification to complete
- Check verification status with `adb shell dumpsys package domain-preferred-apps`

### Deep Links Not Working in Debug Mode

**Issue:** Deep links work in release but not debug builds.

**Solutions:**
- Ensure debug and release signing keys have separate SHA256 fingerprints in `assetlinks.json`
- Add both debug and release fingerprints to the configuration
- Verify intent filters are present in debug manifest

### Cold Start vs. Warm Start

**Issue:** Deep links behave differently when app is closed vs. running.

**Solutions:**
- Handle both `getInitialLink()` and `uriLinkStream` for complete coverage
- Test both cold starts (app closed) and warm starts (app in background)
- Ensure navigation logic works in both scenarios

## Testing Deep Links

### Manual Testing Checklist

- [ ] Test custom URL scheme (if implemented)
- [ ] Test HTTPS deep links
- [ ] Test with app closed (cold start)
- [ ] Test with app in background (warm start)
- [ ] Test with app in foreground
- [ ] Test invalid URLs (error handling)
- [ ] Test links with query parameters
- [ ] Test links with fragments
- [ ] Test on both iOS and Android
- [ ] Test in release builds
- [ ] Verify domain association files are accessible

### Automated Testing

Test deep link handling in integration tests:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Handle product deep link', (tester) async {
    await tester.pumpWidget(MyApp());

    // Simulate deep link
    final uri = Uri.parse('myapp://products/123');
    // Trigger deep link handling

    await tester.pumpAndSettle();

    // Verify navigation
    expect(find.text('Product 123'), findsOneWidget);
  });
}
```

## Best Practices

**Use HTTPS deep links** (App Links/Universal Links) for production rather than custom URL schemes for better security and user experience.

**Implement fallback URLs** for users who don't have the app installed, directing them to the web version or app store.

**Validate deep link data** before navigating to prevent crashes from malformed or malicious links.

**Handle errors gracefully** by showing friendly messages and navigating to a safe screen when links are invalid.

**Test extensively** across platforms, build types, and scenarios (cold start, warm start, foreground).

**Keep paths simple** to make links easier to share and remember.

**Document your deep link structure** for marketing and development teams.

**Monitor deep link performance** through analytics to understand user engagement.

**Version your deep links** if the app structure changes significantly to maintain backward compatibility.

**Provide clear CTAs** in web content to encourage app installation when appropriate.

Deep linking is essential for modern mobile applications, providing seamless navigation from external sources and improving user experience. Proper implementation requires platform-specific configuration and careful testing, but the benefits of direct content access and improved user engagement make it worthwhile for most applications.
