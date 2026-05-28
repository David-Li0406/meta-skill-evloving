import 'package:flutter/material.dart';
import '../../domain/entities/supplement_interaction.dart';
import '../../domain/entities/safety_override.dart';
import '../../domain/repositories/safety_repository.dart';
import 'package:uuid/uuid.dart';

class SafetyViewModel extends ChangeNotifier {
  final SafetyRepository _repository;
  final String userId;

  SafetyViewModel({
    required SafetyRepository repository,
    required this.userId,
  }) : _repository = repository;

  List<SupplementInteraction> _currentInteractions = [];
  bool _isLoading = false;
  String? _error;
  bool _isDisposed = false;

  List<SupplementInteraction> get currentInteractions => _currentInteractions;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Check for interactions between a list of supplements
  Future<void> checkInteractions(List<String> supplementIds) async {
    if (supplementIds.length < 2) {
      _currentInteractions = [];
      notifyListeners();
      return;
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _currentInteractions =
          await _repository.getInteractionsForSupplements(supplementIds);
    } catch (e) {
      _error = 'Failed to check interactions: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Log a safety override
  Future<void> overrideInteraction(String interactionId, String? reason) async {
    final override = SafetyOverride(
      id: const Uuid().v4(),
      userId: userId,
      interactionId: interactionId,
      timestamp: DateTime.now(),
      userReason: reason,
      isAcknowledged: true,
    );

    try {
      await _repository.logSafetyOverride(override);
    } catch (e) {
      _error = 'Failed to log override: $e';
      notifyListeners();
      rethrow;
    }
  }

  /// Check if there are any critical interactions
  bool get hasCriticalInteractions => _currentInteractions
      .any((i) => i.severity == InteractionSeverity.critical);

  /// Get recommendations for current interactions
  List<String> get recommendations =>
      _currentInteractions.map((i) => i.recommendation).toList();
  @override
  void dispose() {
    _isDisposed = true;
    super.dispose();
  }

  @override
  void notifyListeners() {
    if (!_isDisposed) {
      super.notifyListeners();
    }
  }
}
