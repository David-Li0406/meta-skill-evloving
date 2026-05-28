---
name: flutter-clean-architecture
description: Struttura del progetto Flutter e separazione delle responsabilità.
---

# Flutter Clean Architecture

Usa questa skill per decidere dove mettere i file e come strutturare nuove feature.

## Struttura delle Cartelle

Il progetto è diviso in layer. Non mischiare logica di business con UI.

```text
lib/
├── models/       # Definizioni dei dati (Classi pure Dart, JSON serialization)
├── providers/    # State management (Riverpod Controllers & Repositories)
├── services/     # Servizi esterni (API client, Database, Local Auth)
├── screens/      # Pagine intere (Scaffold)
├── widgets/      # Componenti UI riutilizzabili (Bottoni, Card, Grafici)
└── main.dart     # Entry point
```

## Regole per Layer

### 1. Models
- Classi semplici.
- Usa `json_serializable` o `freezed` se necessario, ma mantienile snelle.
- Devono essere indipendenti da Flutter (niente import `package:flutter/...`).

### 2. Services
- Contengono la logica "sporca" (chiamate HTTP, accesso al disco).
- Devono essere esposti tramite Provider per essere mockabili nei test.
- Esempio: `AuthService`, `DatabaseService`.

### 3. Providers (Logic)
- Fanno da ponte tra UI e Services.
- Gestiscono lo stato dell'applicazione.
- Non devono contenere riferimenti a Widget o `BuildContext`.

### 4. UI (Screens & Widgets)
- Devono essere stupidi.
- Si limitano a mostrare i dati forniti dai Provider e a chiamare metodi dei Controller sugli eventi utente.
- Usa `ConsumerWidget` per ascoltare i cambiamenti.

## Esempio Flusso Feature "Login"

1.  **Model**: `User` (in `models/user.dart`)
2.  **Service**: `AuthService` (in `services/auth_service.dart`) -> Fa la chiamata API.
3.  **Provider**: `AuthController` (in `providers/auth_controller.dart`) -> Chiama `AuthService` e gestisce lo stato (loading/success/error).
4.  **Screen**: `LoginScreen` (in `screens/login_screen.dart`) -> Mostra form e osserva `AuthController`.
