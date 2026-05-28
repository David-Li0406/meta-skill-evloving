---
name: flutter-riverpod-architecture
description: Gestione dello stato e dependency injection con Riverpod 2.0 (Code Generation).
---

# Flutter Riverpod Architecture

Usa questa skill quando devi gestire lo stato, creare provider o iniettare dipendenze.
Il progetto usa **Riverpod 2.x** con **Code Generation** (`riverpod_annotation`).

## Regole Fondamentali

1. **Usa Code Generation**:
   Non usare `StateNotifierProvider` o `Provider` manuali.
   Usa l'annotazione `@riverpod`.

2. **Sintassi**:
   Definisci classi o funzioni annotate con `@riverpod`.
   Ricordati di aggiungere `part 'nome_file.g.dart';` all'inizio del file.

3. **Consumare i Provider**:
   - Nei widget: Estendi `ConsumerWidget` (o `ConsumerStatefulWidget`) e usa `ref.watch(provider)`.
   - Nella logica: Usa `ref.read` solo nei callback o metodi di lifecycle, mai nel build.

## Template Provider Semplice (Read-Only)

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'my_provider.g.dart';

@riverpod
String myLabel(MyLabelRef ref) {
  return 'Hello World';
}
```

## Template Provider di Stato (Notifier)

Usa questo per gestire stati mutabili (es. form, liste dinamiche, stati di caricamento).

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'todo_controller.g.dart';

@riverpod
class TodoController extends _$TodoController {
  @override
  List<String> build() {
    // Stato iniziale
    return [];
  }

  void addItem(String item) {
    // In Riverpod i Notifier sono immutabili, crea sempre una nuova istanza
    state = [...state, item];
  }
  
  void removeItem(int index) {
    var newState = [...state];
    newState.removeAt(index);
    state = newState;
  }
}
```

## Gestione Asincrona (AsyncValue)

Per chiamate API o database, ritorna `Future<T>`.

```dart
@riverpod
Future<User> fetchUser(FetchUserRef ref, int userId) async {
  final api = ref.watch(apiProvider);
  return api.getUser(userId);
}
```

Nei widget gestisci i 3 stati:
```dart
final userAsync = ref.watch(fetchUserProvider(1));

return userAsync.when(
  data: (user) => Text(user.name),
  loading: () => CircularProgressIndicator(),
  error: (err, stack) => Text('Errore: $err'),
);
```
