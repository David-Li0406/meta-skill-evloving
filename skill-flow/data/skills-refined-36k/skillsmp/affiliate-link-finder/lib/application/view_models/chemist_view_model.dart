import 'package:flutter/foundation.dart';
import '../../infrastructure/repositories/perplexity_repository.dart';
import '../../infrastructure/services/perplexity_service.dart';

class ChemistViewModel extends ChangeNotifier {
  final PerplexityRepository _repository;

  ChemistViewModel(this._repository);

  String _response = '';
  bool _isLoading = false;
  final List<Map<String, String>> _messages = [];

  String get response => _response;
  bool get isLoading => _isLoading;
  List<Map<String, String>> get messages => _messages;

  Future<void> askChemist(String question) async {
    if (question.isEmpty) return;

    _messages.add({'role': 'user', 'content': question});
    _isLoading = true;
    _response = '';
    notifyListeners();

    try {
      final result = await _repository.search(
        question,
        systemPrompt: PerplexityService.chemistSystemPrompt,
      );
      _response = result;
      _messages.add({'role': 'assistant', 'content': result});
    } catch (e) {
      _response = 'Error: $e';
      _messages.add(
          {'role': 'assistant', 'content': 'Scientific error occurred: $e'});
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearChat() {
    _messages.clear();
    _response = '';
    notifyListeners();
  }
}
