import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/view_models/stack_builder_view_model.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_stack.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/stack_repository.dart';
import 'package:adhd_supplement_app/application/view_models/safety_view_model.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_interaction.dart';

class FakeSupplementRepository implements SupplementRepository {
  List<Supplement> supplements = [];
  @override
  Future<List<Supplement>> getAllSupplements({String? userId}) async =>
      supplements;
  @override
  Future<Supplement?> getSupplement(String id, {String? userId}) async =>
      supplements.firstWhere((s) => s.id == id);
  @override
  Future<List<Supplement>> searchSupplements(String query,
          {String? userId}) async =>
      [];
  @override
  Future<List<Supplement>> getSupplementsByCategory(String category,
          {String? userId}) async =>
      [];
  @override
  Stream<List<Supplement>> watchSupplements({String? userId}) =>
      Stream.value([]);
  @override
  Future<void> saveCustomSupplement(Supplement supplement) async {}
  @override
  Future<void> deleteCustomSupplement(String id, String userId) async {}
  @override
  Future<void> trackReferralClick(String supplementId) async {}
}

class FakeStackRepository implements StackRepository {
  @override
  Future<List<SupplementStack>> getUserStacks(String userId) async => [];
  @override
  Future<void> saveStack(String userId, SupplementStack stack) async {}
  @override
  Future<SupplementStack?> getStack(String userId) async => null;

  @override
  Stream<List<SupplementStack>> watchUserStacks(String userId) =>
      Stream.value([]);
}

class FakeSafetyViewModel extends Fake implements SafetyViewModel {
  @override
  List<SupplementInteraction> get currentInteractions => [];
  @override
  Future<void> checkInteractions(List<String> ids) async {}
}

void main() {
  late StackBuilderViewModel viewModel;
  late FakeSupplementRepository fakeSupplementRepo;
  late FakeStackRepository fakeStackRepo;

  setUp(() {
    fakeSupplementRepo = FakeSupplementRepository();
    fakeStackRepo = FakeStackRepository();
    viewModel = StackBuilderViewModel(
      supplementRepository: fakeSupplementRepo,
      stackRepository: fakeStackRepo,
      safetyViewModel: FakeSafetyViewModel(),
      userId: 'test-user',
    );
  });

  group('StackBuilderViewModel Improvements', () {
    test('updateSearchQuery filters available supplements', () async {
      fakeSupplementRepo.supplements = [
        const Supplement(id: '1', name: 'Omega-3', category: 'Fats'),
        const Supplement(id: '2', name: 'Zinc', category: 'Minerals'),
      ];

      await viewModel.initialize();
      expect(viewModel.availableSupplements.length, 2);

      viewModel.updateSearchQuery('Zinc');
      expect(viewModel.availableSupplements.length, 1);
      expect(viewModel.availableSupplements.first.name, 'Zinc');

      viewModel.updateSearchQuery('');
      expect(viewModel.availableSupplements.length, 2);
    });

    test('updateItemDosage changes dosage for specific supplement', () async {
      const supplement = Supplement(
          id: '1', name: 'Omega-3', category: 'Fats', defaultDosage: '1000mg');
      fakeSupplementRepo.supplements = [supplement];

      await viewModel.initialize();
      viewModel.addItem(supplement);

      expect(viewModel.currentStack?.items.first.customDosage, '1000mg');

      viewModel.updateItemDosage('1', '2000mg');
      expect(viewModel.currentStack?.items.first.customDosage, '2000mg');
    });

    test('updateStackMeta changes name and time', () async {
      await viewModel.initialize();
      expect(viewModel.currentStack?.name, 'Morning Stack');

      viewModel.updateStackMeta('Early Bird Focus', timeOfDay: '07:00');
      expect(viewModel.currentStack?.name, 'Early Bird Focus');
      expect(viewModel.currentStack?.timeOfDay, '07:00');
    });
  });
}
