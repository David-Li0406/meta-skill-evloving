import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/shared_prefs_settings_repository.dart';

void main() {
  late SharedPrefsSettingsRepository repository;
  late SharedPreferences prefs;

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    prefs = await SharedPreferences.getInstance();
    repository = SharedPrefsSettingsRepository(prefs);
  });

  group('SharedPrefsSettingsRepository Compliance', () {
    test('hasAcceptedDisclaimer defaults to false', () {
      expect(repository.hasAcceptedDisclaimer(), false);
    });

    test('setAcceptedDisclaimer persists value', () async {
      await repository.setAcceptedDisclaimer(true);
      expect(repository.hasAcceptedDisclaimer(), true);

      // Verify in raw prefs
      expect(prefs.getBool('accepted_medical_disclaimer'), true);
    });
  });
}
