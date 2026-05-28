import 'package:flutter/foundation.dart';
import '../../domain/entities/supplement.dart';
import '../../domain/entities/supplement_stack.dart';
import '../../domain/repositories/supplement_repository.dart';
import '../../domain/repositories/stack_repository.dart';
import '../../utils/logger.dart';
import 'dart:async';

/// ViewModel for global search functionality across supplements and stacks.
///
/// This ViewModel implements an ADHD-friendly search experience with:
/// - **Debounced search**: 300ms delay prevents excessive API calls during typing
/// - **Parallel execution**: Searches supplements and stacks simultaneously
/// - **Instant feedback**: Loading state updates immediately on query change
/// - **Clear error handling**: User-friendly error messages
///
/// ## Usage
/// ```dart
/// final viewModel = GlobalSearchViewModel(
///   supplementRepository: locator<SupplementRepository>(),
///   stackRepository: locator<StackRepository>(),
///   userId: currentUserId,
/// );
///
/// // Update search query (debounced automatically)
/// viewModel.updateQuery('omega');
///
/// // Clear search
/// viewModel.clear();
/// ```
///
/// ## State Management
/// The ViewModel provides computed properties for UI state:
/// - `hasResults`: True if any supplements or stacks match
/// - `isEmpty`: True if query exists but no results found
/// - `isLoading`: True during search execution
/// - `error`: Contains error message if search fails
class GlobalSearchViewModel extends ChangeNotifier {
  final SupplementRepository _supplementRepository;
  final StackRepository _stackRepository;
  final String _userId;

  // State
  String _query = '';
  List<Supplement> _supplementResults = [];
  List<SupplementStack> _stackResults = [];
  bool _isLoading = false;
  String? _error;
  Timer? _debounceTimer;

  // Getters

  /// Current search query (trimmed)
  String get query => _query;

  /// Supplements matching the search query
  List<Supplement> get supplementResults => _supplementResults;

  /// User's stacks matching the search query (filtered by name)
  List<SupplementStack> get stackResults => _stackResults;

  /// True while search is in progress
  bool get isLoading => _isLoading;

  /// Error message if search failed, null otherwise
  String? get error => _error;

  /// True if any results exist (supplements or stacks)
  bool get hasResults =>
      _supplementResults.isNotEmpty || _stackResults.isNotEmpty;

  /// True if query exists but no results found (empty state)
  bool get isEmpty =>
      _query.isNotEmpty && !_isLoading && !hasResults && _error == null;

  GlobalSearchViewModel({
    required SupplementRepository supplementRepository,
    required StackRepository stackRepository,
    required String userId,
  })  : _supplementRepository = supplementRepository,
        _stackRepository = stackRepository,
        _userId = userId;

  /// Updates the search query with automatic debouncing.
  ///
  /// This method:
  /// 1. Trims whitespace from the query
  /// 2. Cancels any pending search timer
  /// 3. Clears results if query is empty
  /// 4. Sets loading state immediately for instant feedback
  /// 5. Schedules search execution after 300ms debounce
  ///
  /// The debounce prevents excessive API calls during rapid typing,
  /// which is especially important for ADHD users who may type quickly.
  ///
  /// Example:
  /// ```dart
  /// viewModel.updateQuery('omega'); // Triggers search after 300ms
  /// viewModel.updateQuery('omega-3'); // Cancels previous, searches after 300ms
  /// ```
  void updateQuery(String newQuery) {
    _query = newQuery.trim();
    _error = null;

    // Cancel previous timer
    _debounceTimer?.cancel();

    if (_query.isEmpty) {
      _supplementResults = [];
      _stackResults = [];
      _isLoading = false;
      notifyListeners();
      return;
    }

    // Set loading state immediately for visual feedback
    _isLoading = true;
    notifyListeners();

    // Debounce search by 300ms
    _debounceTimer = Timer(const Duration(milliseconds: 300), () {
      _performSearch();
    });
  }

  /// Executes the search across supplements and stacks in parallel.
  ///
  /// This private method:
  /// 1. Searches supplements via repository (server-side search)
  /// 2. Fetches user's stacks and filters by name (client-side filter)
  /// 3. Executes both operations in parallel for optimal performance
  /// 4. Updates results and loading state
  /// 5. Handles errors gracefully with user-friendly messages
  ///
  /// The parallel execution ensures fast results even when searching
  /// multiple data sources.
  Future<void> _performSearch() async {
    if (_query.isEmpty) return;

    AppLogger.d('Performing search for: $_query');

    try {
      // Search supplements and stacks in parallel
      final results = await Future.wait([
        _supplementRepository.searchSupplements(_query, userId: _userId),
        _stackRepository.getUserStacks(_userId),
      ]);

      _supplementResults = results[0] as List<Supplement>;

      // Filter stacks by name
      final allStacks = results[1] as List<SupplementStack>;
      _stackResults = allStacks
          .where((stack) =>
              stack.name.toLowerCase().contains(_query.toLowerCase()))
          .toList();

      AppLogger.d(
          'Search results: ${_supplementResults.length} supplements, ${_stackResults.length} stacks');
    } catch (e) {
      _error = 'Search failed: $e';
      AppLogger.e('Search error', e);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Clears the search query, results, and any pending search operations.
  ///
  /// This method:
  /// 1. Resets query to empty string
  /// 2. Clears all results
  /// 3. Cancels pending debounce timer
  /// 4. Resets error and loading states
  /// 5. Notifies listeners of state change
  ///
  /// Use this when the user taps the clear button or navigates away.
  void clear() {
    _query = '';
    _supplementResults = [];
    _stackResults = [];
    _error = null;
    _isLoading = false;
    _debounceTimer?.cancel();
    notifyListeners();
  }

  /// Cancels any pending search operations before disposal.
  ///
  /// This ensures the debounce timer doesn't fire after the ViewModel
  /// has been disposed, preventing memory leaks and errors.
  @override
  void dispose() {
    _debounceTimer?.cancel();
    super.dispose();
  }
}
