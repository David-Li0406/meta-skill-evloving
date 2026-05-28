import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/mock_supplement_repository.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  late MockSupplementRepository repository;

  setUp(() {
    repository = const MockSupplementRepository();
  });

  group('MockSupplementRepository', () {
    test('getAllSupplements returns a list of supplements', () async {
      final supplements = await repository.getAllSupplements();
      expect(supplements, isNotEmpty);
      expect(supplements.first, isA<Supplement>());
    });

    test('getSupplement returns correct supplement', () async {
      final supplements = await repository.getAllSupplements();
      final expected = supplements.first;
      final result = await repository.getSupplement(expected.id);
      expect(result, isNotNull);
      expect(result!.id, expected.id);
    });

    test('getSupplement returns null for invalid id', () async {
      final result = await repository.getSupplement('invalid_id');
      expect(result, isNull);
    });

    test('getSupplementsByCategory filters correctly', () async {
      final supplements = await repository.getAllSupplements();
      final category = supplements.first.category;
      final result = await repository.getSupplementsByCategory(category);
      expect(result, isNotEmpty);
      expect(result.every((s) => s.category == category), isTrue);
    });

    test('searchSupplements matches by name', () async {
      // "Omega-3" is in the mock data
      final result = await repository.searchSupplements('Omega');
      expect(result, isNotEmpty);
      expect(result.any((s) => s.name.contains('Omega')), isTrue);
    });

    test('searchSupplements matches by benefit', () async {
      // "focus" matches "Improves focus" benefit of Omega-3
      final result = await repository.searchSupplements('focus');
      expect(result, isNotEmpty);
    });

    test('watchSupplements emits data', () async {
      final stream = repository.watchSupplements();
      expect(stream, emits(isNotEmpty));
    });
  });
}
