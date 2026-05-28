import 'package:flutter_test/flutter_test.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';

void main() {
  late UrlService urlService;
  late List<Map<String, dynamic>> launchCalls;

  setUp(() {
    launchCalls = [];
  });

  Future<bool> mockLauncher(Uri url,
      {LaunchMode mode = LaunchMode.platformDefault}) async {
    launchCalls.add({'url': url.toString(), 'mode': mode});
    // Simulate success unless we specify otherwise
    return true;
  }

  group('UrlService Tests', () {
    test('launchReferral should use externalApplication mode', () async {
      urlService = UrlService(launcher: mockLauncher);
      const testUrl = 'https://example.com/buy';

      await urlService.launchReferral(testUrl);

      expect(launchCalls.length, 1);
      expect(launchCalls.first['url'], testUrl);
      expect(launchCalls.first['mode'], LaunchMode.externalApplication);
    });

    test('launchInAppBrowser should attempt inAppBrowserView first', () async {
      urlService = UrlService(launcher: mockLauncher);
      const testUrl = 'https://pubmed.ncbi.nlm.nih.gov/123/';

      await urlService.launchInAppBrowser(testUrl);

      expect(launchCalls.length, 1);
      expect(launchCalls.first['url'], testUrl);
      expect(launchCalls.first['mode'], LaunchMode.inAppBrowserView);
    });

    test('launchInAppBrowser should fallback to external if in-app fails',
        () async {
      // Setup launcher that fails on first attempt (in-app) but succeeds on second (external)
      int callCount = 0;
      Future<bool> failingMockLauncher(Uri url,
          {LaunchMode mode = LaunchMode.platformDefault}) async {
        callCount++;
        launchCalls.add({'url': url.toString(), 'mode': mode});
        if (mode == LaunchMode.inAppBrowserView) return false;
        return true;
      }

      urlService = UrlService(launcher: failingMockLauncher);
      const testUrl = 'https://pubmed.ncbi.nlm.nih.gov/123/';

      await urlService.launchInAppBrowser(testUrl);

      expect(callCount, 2);
      expect(launchCalls[0]['mode'], LaunchMode.inAppBrowserView);
      expect(launchCalls[1]['mode'], LaunchMode.externalApplication);
    });

    test(
        'launchInAppBrowser should fallback if an exception occurs during in-app launch',
        () async {
      int callCount = 0;
      Future<bool> crashingMockLauncher(Uri url,
          {LaunchMode mode = LaunchMode.platformDefault}) async {
        callCount++;
        launchCalls.add({'url': url.toString(), 'mode': mode});
        if (mode == LaunchMode.inAppBrowserView) {
          throw Exception('System crash');
        }
        return true;
      }

      urlService = UrlService(launcher: crashingMockLauncher);
      const testUrl = 'https://pubmed.ncbi.nlm.nih.gov/123/';

      await urlService.launchInAppBrowser(testUrl);

      expect(callCount, 2);
      expect(launchCalls[0]['mode'], LaunchMode.inAppBrowserView);
      expect(launchCalls[1]['mode'], LaunchMode.externalApplication);
    });

    test('launchUri should use platformDefault mode', () async {
      urlService = UrlService(launcher: mockLauncher);
      const testUrl = 'https://google.com';

      await urlService.launchUri(testUrl);

      expect(launchCalls.length, 1);
      expect(launchCalls.first['url'], testUrl);
      expect(launchCalls.first['mode'], LaunchMode.platformDefault);
    });

    test('highly resilient: should throw only if all fallbacks fail', () async {
      Future<bool> absoluteFailureLauncher(Uri url,
          {LaunchMode mode = LaunchMode.platformDefault}) async {
        throw Exception('No browser found');
      }

      urlService = UrlService(launcher: absoluteFailureLauncher);

      expect(
        () => urlService.launchInAppBrowser('https://example.com'),
        throwsA(isA<Exception>()),
      );
    });

    group('Error Cases', () {
      test('should throw for invalid URLs', () async {
        urlService = UrlService(launcher: mockLauncher);
        // Invalid URL that Uri.parse might handle but launchUrl won't
        expect(() => urlService.launchUri('::invalid::'),
            throwsA(isA<FormatException>()));
      });
    });
  });
}
