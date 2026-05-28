import 'package:flutter/material.dart';
import '../../domain/entities/supplement.dart';
import '../../domain/entities/supplement_stack.dart';
import '../../domain/repositories/supplement_repository.dart';
import '../../domain/repositories/stack_repository.dart';
import '../../application/view_models/safety_view_model.dart';
import '../../utils/logger.dart';

class StackBuilderViewModel extends ChangeNotifier {
  final StackRepository _stackRepository;
  final SupplementRepository _supplementRepository;
  final SafetyViewModel _safetyViewModel;
  final String _userId;

  StackBuilderViewModel({
    required StackRepository stackRepository,
    required SupplementRepository supplementRepository,
    required SafetyViewModel safetyViewModel,
    required String userId,
  })  : _stackRepository = stackRepository,
        _supplementRepository = supplementRepository,
        _safetyViewModel = safetyViewModel,
        _userId = userId;

  // State
  List<Supplement> _availableSupplements = [];
  SupplementStack? _currentStack;
  bool _isLoading = false;
  String? _error;
  String _selectedSlot = 'morning';
  String _searchQuery = '';

  // Getters
  List<Supplement> get availableSupplements => _searchQuery.isEmpty
      ? _availableSupplements
      : _availableSupplements
          .where(
              (s) => s.name.toLowerCase().contains(_searchQuery.toLowerCase()))
          .toList();
  SupplementStack? get currentStack => _currentStack;
  bool get isLoading => _isLoading;
  String? get error => _error;
  String get selectedSlot => _selectedSlot;
  String get searchQuery => _searchQuery;

  Future<void> initialize() async {
    _setLoading(true);
    _error = null;

    try {
      // Load all available supplements
      _availableSupplements =
          await _supplementRepository.getAllSupplements(userId: _userId);

      // Load existing stacks for this user
      final stacks = await _stackRepository.getUserStacks(_userId);

      // For now, let's work with the stack matching the selected slot
      _updateCurrentStackFromList(stacks);
    } catch (e) {
      _error = 'Failed to initialize stack builder: $e';
      AppLogger.e(_error!);
    } finally {
      _setLoading(false);
    }
  }

  void updateSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void _updateCurrentStackFromList(List<SupplementStack> stacks) {
    _currentStack = stacks.firstWhere(
      (s) => s.timeOfDay?.toLowerCase() == _selectedSlot.toLowerCase(),
      orElse: () => SupplementStack(
        id: '${_selectedSlot.toLowerCase()}_routine',
        userId: _userId,
        name: '${_selectedSlot.capitalize()} Stack',
        items: [],
        timeOfDay: _selectedSlot,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      ),
    );
    _checkInteractions();
  }

  Future<void> selectSlot(String slot) async {
    if (_selectedSlot == slot) return;
    _selectedSlot = slot;

    _setLoading(true);
    try {
      final stacks = await _stackRepository.getUserStacks(_userId);
      _updateCurrentStackFromList(stacks);
    } catch (e) {
      _error = 'Failed to load stack for $slot: $e';
    } finally {
      _setLoading(false);
    }
  }

  void addItem(Supplement supplement) {
    if (_currentStack == null) return;

    // Check if item already exists in stack
    if (_currentStack!.items
        .any((item) => item.supplementId == supplement.id)) {
      return;
    }

    final newItem = StackItem(
      supplementId: supplement.id,
      customDosage: supplement.defaultDosage,
      order: _currentStack!.items.length,
    );

    final updatedItems = List<StackItem>.from(_currentStack!.items)
      ..add(newItem);
    _currentStack =
        _currentStack!.copyWith(items: updatedItems, updatedAt: DateTime.now());

    _checkInteractions();
    notifyListeners();
  }

  void updateItemDosage(String supplementId, String dosage) {
    if (_currentStack == null) return;

    final updatedItems = _currentStack!.items.map((item) {
      if (item.supplementId == supplementId) {
        return item.copyWith(customDosage: dosage);
      }
      return item;
    }).toList();

    _currentStack =
        _currentStack!.copyWith(items: updatedItems, updatedAt: DateTime.now());
    notifyListeners();
  }

  void updateStackMeta(String name, {String? timeOfDay}) {
    if (_currentStack == null) return;

    _currentStack = _currentStack!.copyWith(
      name: name,
      timeOfDay: timeOfDay ?? _currentStack!.timeOfDay,
      updatedAt: DateTime.now(),
    );
    notifyListeners();
  }

  void removeItem(int index) {
    if (_currentStack == null) return;

    final updatedItems = List<StackItem>.from(_currentStack!.items)
      ..removeAt(index);
    // Re-order remaining items
    for (int i = 0; i < updatedItems.length; i++) {
      updatedItems[i] = updatedItems[i].copyWith(order: i);
    }

    _currentStack =
        _currentStack!.copyWith(items: updatedItems, updatedAt: DateTime.now());

    _checkInteractions();
    notifyListeners();
  }

  void reorderItems(int oldIndex, int newIndex) {
    if (_currentStack == null) return;

    final updatedItems = List<StackItem>.from(_currentStack!.items);
    if (oldIndex < newIndex) {
      newIndex -= 1;
    }
    final item = updatedItems.removeAt(oldIndex);
    updatedItems.insert(newIndex, item);

    // Update order property
    for (int i = 0; i < updatedItems.length; i++) {
      updatedItems[i] = updatedItems[i].copyWith(order: i);
    }

    _currentStack =
        _currentStack!.copyWith(items: updatedItems, updatedAt: DateTime.now());
    notifyListeners();
  }

  Future<bool> saveStack() async {
    if (_currentStack == null) return false;

    _setLoading(true);
    try {
      await _stackRepository.saveStack(_userId, _currentStack!);
      return true;
    } catch (e) {
      _error = 'Failed to save stack: $e';
      notifyListeners();
      return false;
    } finally {
      _setLoading(false);
    }
  }

  /// Returns real-time expert insights based on the current stack items.
  String? get stackInsight {
    if (_currentStack == null || _currentStack!.items.isEmpty) return null;

    final ids = _currentStack!.items.map((i) => i.supplementId).toList();

    // Synergy: L-Theanine + Caffeine
    if (ids.contains('caffeine') && ids.contains('l-theanine')) {
      return 'Synergy Detected: L-Theanine significantly reduces potential "jitters" from Caffeine while maintaining focus. 🧠✨';
    }

    // Synergy: Magnesium + Vitamin D3
    if (ids.contains('magnesium') && ids.contains('vitamin-d')) {
      return 'Optimization: Magnesium is a cofactor for Vitamin D metabolism. This pair ensures maximum efficiency for bone and brain health. 🦴⚡';
    }

    // Synergy: Zinc + Copper (Preventing deficiency)
    if (ids.contains('zinc') && !ids.contains('copper')) {
      return 'Tip: High Zinc intake can deplete Copper levels. Consider adding a small amount of Copper if identifying long-term Zinc use.';
    }

    // Generic Tip based on count
    if (ids.length >= 4) {
      return 'Expert Tip: You have a robust stack. Remember to "cycle" certain nootropics to maintain receptor sensitivity.';
    }

    return 'Building a great routine! Each item here supports your ADHD cognitive profile.';
  }

  /// Applies a pre-configured stack archetype.
  void applyPreset(String archetype) {
    if (_currentStack == null) return;

    List<StackItem> presetItems = [];

    switch (archetype.toLowerCase()) {
      case 'student':
        presetItems = const [
          StackItem(
              supplementId: 'l-theanine', customDosage: '200mg', order: 0),
          StackItem(supplementId: 'caffeine', customDosage: '100mg', order: 1),
          StackItem(supplementId: 'omega-3', customDosage: '1000mg', order: 2),
        ];
        break;
      case 'creative':
        presetItems = const [
          StackItem(supplementId: 'magnesium', customDosage: '200mg', order: 0),
          StackItem(
              supplementId: 'vitamin-d', customDosage: '2000iu', order: 1),
          StackItem(
              supplementId: 'lions-mane', customDosage: '500mg', order: 2),
        ];
        break;
      case 'executive':
        presetItems = const [
          StackItem(
              supplementId: 'rhodiola-rosea', customDosage: '300mg', order: 0),
          StackItem(
              supplementId: 'bacopa-monnieri', customDosage: '300mg', order: 1),
          StackItem(supplementId: 'zinc', customDosage: '15mg', order: 2),
        ];
        break;
    }

    if (presetItems.isNotEmpty) {
      _currentStack = _currentStack!.copyWith(
        items: presetItems,
        updatedAt: DateTime.now(),
      );
      _checkInteractions();
      notifyListeners();
    }
  }

  void _checkInteractions() {
    if (_currentStack == null) return;
    final ids = _currentStack!.items.map((i) => i.supplementId).toList();
    _safetyViewModel.checkInteractions(ids);
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
}

extension StringExtension on String {
  String capitalize() {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }
}
