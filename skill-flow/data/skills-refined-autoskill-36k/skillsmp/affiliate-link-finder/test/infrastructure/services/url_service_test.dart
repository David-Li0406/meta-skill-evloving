import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';

void main() {
  group('UrlService', () {
    late UrlService urlService;

    setUp(() {
      urlService = UrlService();
    });

    test('should create instance successfully', () {
      expect(urlService, isA<UrlService>());
    });
  });
}
