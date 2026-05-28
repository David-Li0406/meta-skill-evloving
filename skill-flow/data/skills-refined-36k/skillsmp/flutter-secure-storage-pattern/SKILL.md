---
name: flutter-secure-storage-pattern
description: Pattern sicuro per salvare dati sensibili (Token, Seed) su device.
---

# Secure Storage & Cryptography

Usa questa skill quando devi salvare dati sensibili come token API, seed crypto o PIN.
Il progetto usa `flutter_secure_storage` e `cryptography`.

## Regole di Sicurezza

1. **Mai SharedPreferences**: Non usare `shared_preferences` per dati sensibili. Sono salvati in chiaro.
2. **Usa Secure Storage**: Usa sempre `FlutterSecureStorage` per piccole stringhe segrete.
3. **Biometria**: Se richiesto, proteggi l'accesso con `local_auth` prima di leggere dallo storage.

## Pattern di Utilizzo

### Inizializzazione
Definisci le opzioni per garantire la crittografia massima su ogni piattaforma.

```dart
final _storage = const FlutterSecureStorage(
  aOptions: AndroidOptions(
    encryptedSharedPreferences: true,
  ),
  iOptions: IOSOptions(
    accessibility: KeychainAccessibility.first_unlock,
  ),
);
```

### Lettura/Scrittura Asincrona
Ricorda che l'accesso al keychain è lento e asincrono.

```dart
// Scrittura
await _storage.write(key: 'auth_token', value: token);

// Lettura
String? token = await _storage.read(key: 'auth_token');

// Cancellazione (es. Logout)
await _storage.delete(key: 'auth_token');
```

## Gestione Errori
L'accesso al Secure Storage può fallire (device bloccato, corruzione dati). Gestisci sempre le eccezioni `PlatformException`.

```dart
try {
  await _storage.read(key: 'secret');
} catch (e) {
  // Logga l'errore e gestisci il caso (es. richiedi login)
  print('Errore SecureStorage: $e');
}
```
