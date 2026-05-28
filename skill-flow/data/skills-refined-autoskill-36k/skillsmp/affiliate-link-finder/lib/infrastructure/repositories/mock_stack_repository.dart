import '../../domain/repositories/stack_repository.dart';
import '../../domain/entities/supplement_stack.dart';

class MockStackRepository implements StackRepository {
  @override
  Future<void> saveStack(String userId, SupplementStack stack) async {
    // Mock implementation - do nothing
  }

  @override
  Future<SupplementStack?> getStack(String userId) async {
    return null; // Return null to indicate no stack exists
  }

  @override
  Future<List<SupplementStack>> getUserStacks(String userId) async {
    return []; // Return empty list
  }

  @override
  Stream<List<SupplementStack>> watchUserStacks(String userId) async* {
    yield [];
  }
}
