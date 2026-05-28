import '../entities/supplement_stack.dart';

abstract class StackRepository {
  Future<void> saveStack(String userId, SupplementStack stack);
  Future<SupplementStack?> getStack(String userId);
  Future<List<SupplementStack>> getUserStacks(String userId);
  Stream<List<SupplementStack>> watchUserStacks(String userId);
}
