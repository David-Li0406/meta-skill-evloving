import 'package:adhd_supplement_app/infrastructure/services/perplexity_service.dart';

abstract class PerplexityRepository {
  Future<String> search(String query, {String? systemPrompt});
}

class PerplexityRepositoryImpl implements PerplexityRepository {
  final PerplexityService _service;

  PerplexityRepositoryImpl(this._service);

  @override
  Future<String> search(String query, {String? systemPrompt}) async {
    return _service.search(query, systemPrompt: systemPrompt);
  }
}
