import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/global_search_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/stack_repository.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_stack.dart';

@GenerateMocks([SupplementRepository, StackRepository])
import 'global_search_view_model_test.mocks.dart';

void main() {
  late GlobalSearchViewModel viewModel;
  late MockSupplementRepository mockSupplementRepository;
  late MockStackRepository mockStackRepository;
  const testUserId = 'test_user_123';

  setUp(() {
    mockSupplementRepository = MockSupplementRepository();
    mockStackRepository = MockStackRepository();
    viewModel = GlobalSearchViewModel(
      supplementRepository: mockSupplementRepository,
      stackRepository: mockStackRepository,
      userId: testUserId,
    );
  });

  tearDown(() {
    viewModel.dispose();
  });

  group('GlobalSearchViewModel', () {
    group('Initialization', () {
      test('should initialize with empty state', () {
        expect(viewModel.query, isEmpty);
        expect(viewModel.supplementResults, isEmpty);
        expect(viewModel.stackResults, isEmpty);
        expect(viewModel.isLoading, isFalse);
        expect(viewModel.error, isNull);
        expect(viewModel.hasResults, isFalse);
        expect(viewModel.isEmpty, isFalse);
      });
    });

    group('updateQuery', () {
      test('should update query and trigger search after debounce', () async {
        // Arrange
        const supplements = [
          Supplement(
            id: '1',
            name: 'Omega-3',
            category: 'Cognitive',
            benefits: ['Focus'],
            dosage: '1000mg',
            form: 'Capsule',
            defaultDosage: '1000mg',
            shapeIcon: 'capsule',
            colorHex: '#FFB74D',
          ),
        ];

        when(mockSupplementRepository.searchSupplements('omega'))
            .thenAnswer((_) async => List<Supplement>.from(supplements));
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        // Act
        viewModel.updateQuery('omega');

        // Assert - should be loading immediately
        expect(viewModel.query, 'omega');
        expect(viewModel.isLoading, isTrue);

        // Wait for debounce (300ms + buffer)
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert - should have results after debounce
        expect(viewModel.isLoading, isFalse);
        expect(viewModel.supplementResults, supplements);
        expect(viewModel.stackResults, isEmpty);
        expect(viewModel.hasResults, isTrue);
      });

      test('should clear results when query is empty', () {
        // Act
        viewModel.updateQuery('');

        // Assert
        expect(viewModel.query, isEmpty);
        expect(viewModel.supplementResults, isEmpty);
        expect(viewModel.stackResults, isEmpty);
        expect(viewModel.isLoading, isFalse);
      });

      test('should cancel previous search when new query is entered', () async {
        // Arrange
        when(mockSupplementRepository.searchSupplements(any))
            .thenAnswer((_) async => <Supplement>[]);
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        // Act - rapid typing
        viewModel.updateQuery('om');
        await Future<void>.delayed(const Duration(milliseconds: 100));
        viewModel.updateQuery('ome');
        await Future<void>.delayed(const Duration(milliseconds: 100));
        viewModel.updateQuery('omega');

        // Wait for final debounce
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert - should only search once for final query
        verify(mockSupplementRepository.searchSupplements('omega')).called(1);
        verifyNever(mockSupplementRepository.searchSupplements('om'));
        verifyNever(mockSupplementRepository.searchSupplements('ome'));
      });

      test('should trim whitespace from query', () async {
        // Arrange
        when(mockSupplementRepository.searchSupplements('omega'))
            .thenAnswer((_) async => <Supplement>[]);
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        // Act
        viewModel.updateQuery('  omega  ');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert
        expect(viewModel.query, 'omega');
        verify(mockSupplementRepository.searchSupplements('omega')).called(1);
      });
    });

    group('Search Results', () {
      test('should filter stacks by name case-insensitively', () async {
        // Arrange
        final stacks = [
          SupplementStack(
            id: '1',
            userId: testUserId,
            name: 'Morning Focus Stack',
            items: const [],
            timeOfDay: 'morning',
            createdAt: DateTime.now(),
            updatedAt: DateTime.now(),
          ),
          SupplementStack(
            id: '2',
            userId: testUserId,
            name: 'Evening Calm',
            items: const [],
            timeOfDay: 'evening',
            createdAt: DateTime.now(),
            updatedAt: DateTime.now(),
          ),
        ];

        when(mockSupplementRepository.searchSupplements('focus'))
            .thenAnswer((_) async => <Supplement>[]);
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => List<SupplementStack>.from(stacks));

        // Act
        viewModel.updateQuery('focus');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert - should only return matching stack
        expect(viewModel.stackResults.length, 1);
        expect(viewModel.stackResults.first.name, 'Morning Focus Stack');
      });

      test('should handle search errors gracefully', () async {
        // Arrange
        when(mockSupplementRepository.searchSupplements(any))
            .thenThrow(Exception('Network error'));
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        // Act
        viewModel.updateQuery('omega');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert
        expect(viewModel.isLoading, isFalse);
        expect(viewModel.error, isNotNull);
        expect(viewModel.error, contains('Search failed'));
      });

      test('should execute supplement and stack searches in parallel',
          () async {
        // Arrange
        const supplements = [
          Supplement(
            id: '1',
            name: 'Magnesium',
            category: 'Sleep',
            benefits: ['Sleep'],
            dosage: '400mg',
            form: 'Tablet',
            defaultDosage: '400mg',
            shapeIcon: 'tablet',
            colorHex: '#FFB74D',
          ),
        ];
        final stacks = [
          SupplementStack(
            id: '1',
            userId: testUserId,
            name: 'Sleep Stack',
            items: const [],
            timeOfDay: 'evening',
            createdAt: DateTime.now(),
            updatedAt: DateTime.now(),
          ),
        ];

        when(mockSupplementRepository.searchSupplements('mag'))
            .thenAnswer((_) async => List<Supplement>.from(supplements));
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => List<SupplementStack>.from(stacks));

        // Act
        viewModel.updateQuery('mag');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert - both should be called
        verify(mockSupplementRepository.searchSupplements('mag')).called(1);
        verify(mockStackRepository.getUserStacks(testUserId)).called(1);
        expect(viewModel.supplementResults, supplements);
        expect(viewModel.stackResults.length,
            0); // 'mag' doesn't match 'Sleep Stack'
      });
    });

    group('Computed Properties', () {
      test('hasResults should be true when supplements exist', () async {
        // Arrange
        const supplements = [
          Supplement(
            id: '1',
            name: 'Test',
            category: 'Test',
            benefits: [],
            dosage: '100mg',
            form: 'Pill',
            defaultDosage: '100mg',
            shapeIcon: 'pill',
            colorHex: '#FFB74D',
          ),
        ];

        when(mockSupplementRepository.searchSupplements(any))
            .thenAnswer((_) async => List<Supplement>.from(supplements));
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        // Act
        viewModel.updateQuery('test');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert
        expect(viewModel.hasResults, isTrue);
      });

      test('hasResults should be true when stacks exist', () async {
        // Arrange
        final stacks = [
          SupplementStack(
            id: '1',
            userId: testUserId,
            name: 'Test Stack',
            items: const [],
            timeOfDay: 'morning',
            createdAt: DateTime.now(),
            updatedAt: DateTime.now(),
          ),
        ];

        when(mockSupplementRepository.searchSupplements(any))
            .thenAnswer((_) async => <Supplement>[]);
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => List<SupplementStack>.from(stacks));

        // Act
        viewModel.updateQuery('test');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert
        expect(viewModel.hasResults, isTrue);
      });

      test('isEmpty should be true when query exists but no results', () async {
        // Arrange
        when(mockSupplementRepository.searchSupplements(any))
            .thenAnswer((_) async => <Supplement>[]);
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        // Act
        viewModel.updateQuery('nonexistent');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert
        expect(viewModel.isEmpty, isTrue);
        expect(viewModel.query, 'nonexistent');
        expect(viewModel.hasResults, isFalse);
        expect(viewModel.isLoading, isFalse);
        expect(viewModel.error, isNull);
      });
    });

    group('clear', () {
      test('should reset all state', () async {
        // Arrange - set up some state
        when(mockSupplementRepository.searchSupplements(any))
            .thenAnswer((_) async => <Supplement>[]);
        when(mockStackRepository.getUserStacks(testUserId))
            .thenAnswer((_) async => <SupplementStack>[]);

        viewModel.updateQuery('test');
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Act
        viewModel.clear();

        // Assert
        expect(viewModel.query, isEmpty);
        expect(viewModel.supplementResults, isEmpty);
        expect(viewModel.stackResults, isEmpty);
        expect(viewModel.isLoading, isFalse);
        expect(viewModel.error, isNull);
      });

      test('should cancel pending debounce timer', () async {
        // Arrange
        viewModel.updateQuery('test');

        // Act - clear before debounce completes
        await Future<void>.delayed(const Duration(milliseconds: 100));
        viewModel.clear();
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert - search should not have been called
        verifyNever(mockSupplementRepository.searchSupplements(any));
      });
    });

    group('Dispose', () {
      test('should cancel debounce timer on dispose', () async {
        // Arrange - use a separate instance to avoid double-dispose in tearDown
        final localViewModel = GlobalSearchViewModel(
          supplementRepository: mockSupplementRepository,
          stackRepository: mockStackRepository,
          userId: testUserId,
        );
        localViewModel.updateQuery('test');

        // Act
        await Future<void>.delayed(const Duration(milliseconds: 100));
        localViewModel.dispose();
        await Future<void>.delayed(const Duration(milliseconds: 400));

        // Assert - search should not have been called
        verifyNever(mockSupplementRepository.searchSupplements(any));
      });
    });
  });
}
