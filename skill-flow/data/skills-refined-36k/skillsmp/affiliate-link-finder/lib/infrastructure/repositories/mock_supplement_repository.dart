import '../../domain/entities/supplement.dart';
import '../../domain/repositories/supplement_repository.dart';
import '../../utils/logger.dart';

class MockSupplementRepository implements SupplementRepository {
  const MockSupplementRepository(); // Added const constructor

  @override
  Future<List<Supplement>> getAllSupplements({String? userId}) async {
    await Future<void>.delayed(
        const Duration(milliseconds: 500)); // Simulate net lag
    return const [
      Supplement(
        id: '1',
        name: 'Omega-3 (EPA/DHA)',
        description:
            'Essential fatty acids that may improve attention and reduce hyperactivity symptoms.',
        referralUrl: 'https://example.com/omega3',
        benefits: [
          'Improves focus',
          'Supports brain health',
          'Reduces inflammation'
        ],
        category: 'Essentials',
        dosage: '1000mg daily with food',
        sideEffects: ['Fishy aftertaste', 'Mild stomach upset'],
        focusLevel: 4,
      ),
      Supplement(
        id: '2',
        name: 'Magnesium Glycinate',
        description:
            'Helps with relaxation, sleep quality, and calming restlessness.',
        referralUrl: 'https://example.com/magnesium',
        benefits: ['Reduces hyperactivity', 'Improves sleep', 'Calms anxiety'],
        category: 'Sleep',
        dosage: '200mg before bed',
        sideEffects: ['Drowsiness'],
        focusLevel: 3,
      ),
      Supplement(
        id: '3',
        name: 'L-Theanine',
        description:
            'An amino acid found in tea that promotes calm focus without drowsiness.',
        referralUrl: 'https://example.com/ltheanine',
        benefits: [
          'Calm alertness',
          'Reduces stress',
          'Pairs well with caffeine'
        ],
        category: 'Calm',
        dosage: '100-200mg as needed',
        sideEffects: [],
        focusLevel: 5,
      ),
      Supplement(
        id: '4',
        name: 'Zinc',
        description: 'Essential mineral that supports dopamine regulation.',
        referralUrl: 'https://example.com/zinc',
        benefits: ['Supports attention', 'Dopamine regulation'],
        dosage: '15-30mg daily with food',
        sideEffects: ['Nausea if taken on empty stomach'],
        focusLevel: 3,
        category: 'Essentials',
      ),
    ];
  }

  @override
  Future<Supplement?> getSupplement(String id, {String? userId}) async {
    final supplements = await getAllSupplements(userId: userId);
    try {
      return supplements.firstWhere((s) => s.id == id);
    } catch (_) {
      return null;
    }
  }

  @override
  Future<List<Supplement>> getSupplementsByCategory(String category,
      {String? userId}) async {
    final supplements = await getAllSupplements(userId: userId);
    return supplements.where((s) => s.category == category).toList();
  }

  @override
  Future<List<Supplement>> searchSupplements(String query,
      {String? userId}) async {
    final supplements = await getAllSupplements(userId: userId);
    final lowerQuery = query.toLowerCase();
    return supplements.where((s) {
      return s.name.toLowerCase().contains(lowerQuery) ||
          s.description.toLowerCase().contains(lowerQuery) ||
          s.benefits.any((b) => b.toLowerCase().contains(lowerQuery));
    }).toList();
  }

  @override
  Stream<List<Supplement>> watchSupplements({String? userId}) async* {
    final supplements = await getAllSupplements(userId: userId);
    yield supplements;
  }

  @override
  Future<void> saveCustomSupplement(Supplement supplement) async {
    AppLogger.d('Mock: Saved custom supplement ${supplement.name}');
  }

  @override
  Future<void> deleteCustomSupplement(String id, String userId) async {
    AppLogger.d('Mock: Deleted custom supplement $id for user $userId');
  }

  @override
  Future<void> trackReferralClick(String supplementId) async {
    // In production, this would write to Firestore
    // In a real app, this would log to analytics
    AppLogger.d('Tracked referral click for: $supplementId');
  }
}
