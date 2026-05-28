---
name: KeePassXC Integration
description: Integracja KeePassXC z Cursorem do bezpiecznego zarządzania sekretami (hasła, tokeny API, klucze SSH)
compatibility:
  - wsl
  - windows
---

# Skill: KeePassXC Integration

## Activation Gate

Użyj tego skill gdy:
- Użytkownik potrzebuje pobrać sekret z bazy KeePassXC (hasło, token API, klucz SSH)
- Użytkownik chce użyć `keepassxc-cli` do zarządzania sekretami
- Użytkownik pyta o konfigurację KeePassXC z Cursorem

**Before implementing KeePassXC features, verify architecture:**
- Keyring (SecretManagement/secret-tool) = database password **ONLY**
- KeePassXC database = **ALL** secrets (passwords, tokens, keys)
- No file-based fallbacks

## Przegląd

Ten skill umożliwia bezpieczne zarządzanie sekretami przez KeePassXC z poziomu Cursora. Używa osobnej bazy `cursor.kdbx` z hasłem przechowywanym w PowerShell SecretManagement, SSH Agent dla kluczy SSH, oraz `keepassxc-cli` dla innych sekretów.

## Konfiguracja

### Zmienne środowiskowe

- `KEEPASS_DB_PATH` - ścieżka do bazy Cursor (ustawiona w `~/.profile` i `~/.bashrc`)
  - WSL: `/mnt/c/Users/janja/OneDrive/Dokumenty/Inne/cursor.kdbx`
  - Windows: `C:\Users\janja\OneDrive\Dokumenty\Inne\cursor.kdbx`

### Hasło bazy

Hasło bazy jest przechowywane w:
- **PowerShell SecretManagement** (główna metoda, pozwala na odczyt, dostępne z Windows i WSL)
- **secret-tool** (opcjonalny fallback dla WSL, jeśli D-Bus dostępny)
- **Windows Credential Manager** (backup, tylko zapis, nie można odczytać programatycznie)

**WAŻNE:** 
- SecretManagement/secret-tool przechowują **TYLKO** hasło bazy KeePassXC, nie hasła z bazy
- Wszystkie sekrety (hasła, tokeny API, klucze SSH) są przechowywane **wyłącznie** w bazie KeePassXC
- Nie ma fallbacku do pliku - wszystkie metody używają bezpiecznych mechanizmów keyring

Hasło jest automatycznie zapisywane przez skrypt `save-keepass-password-to-keyring.sh` gdy baza jest otwarta w GUI.

## Użycie

### Podstawowe komendy

#### Pobieranie sekretu przez skrypt pomocniczy

```bash
# Pobierz hasło z wpisu
~/.cursor/scripts/get-keepass-secret.sh "Entry Title" "Password"

# Pobierz token API
~/.cursor/scripts/get-keepass-secret.sh "GitHub Token" "Token"

# Pobierz dowolny atrybut
~/.cursor/scripts/get-keepass-secret.sh "Entry Title" "Attribute Name"
```

#### Bezpośrednie użycie keepassxc-cli

```bash
# Lista wszystkich wpisów
keepassxc-cli ls "$KEEPASS_DB_PATH"

# Wyświetl szczegóły wpisu
keepassxc-cli show "$KEEPASS_DB_PATH" "Entry Title"

# Pobierz konkretny atrybut
keepassxc-cli show -a "Password" "$KEEPASS_DB_PATH" "Entry Title"

# Pobierz hasło (interaktywnie, jeśli nie jest w SecretManagement)
echo "hasło" | keepassxc-cli show -a "Password" "$KEEPASS_DB_PATH" "Entry Title"
```

### Zapisywanie hasła do keyring

```bash
# Uruchom skrypt (wymaga otwartej bazy w GUI)
~/.cursor/scripts/save-keepass-password-to-keyring.sh
```

## SSH Agent

KeePassXC SSH Agent automatycznie ładuje klucze SSH z bazy do systemowego SSH agenta gdy baza jest otwarta w GUI.

### Weryfikacja

```bash
# W PowerShell (Windows)
ssh-add -l

# Powinien być widoczny klucz SSH z bazy
```

### Użycie kluczy SSH

Klucze SSH są automatycznie dostępne dla wszystkich połączeń SSH (nie trzeba podawać `-i`).

## Przykłady użycia

### Pobieranie tokenu GitHub

```bash
GITHUB_TOKEN=$(~/.cursor/scripts/get-keepass-secret.sh "GitHub Token" "Token")
export GITHUB_TOKEN
```

### Pobieranie hasła do bazy danych

```bash
DB_PASSWORD=$(~/.cursor/scripts/get-keepass-secret.sh "Database Credentials" "Password")
```

### Pobieranie klucza API

```bash
API_KEY=$(~/.cursor/scripts/get-keepass-secret.sh "Service API" "API Key")
```

## Bezpieczeństwo

### Best Practices

1. **Nie commituj haseł do Git** - wszystkie sekrety są w bazie KeePassXC
2. **Używaj SSH Agent** - klucze SSH są automatycznie ładowane, nie przechowywane na dysku
3. **Hasło w SecretManagement** - bezpieczniejsze niż w zmiennych systemowych lub plikach
4. **Osobna baza Cursor** - izolacja sekretów Cursora od głównej bazy
5. **Regularna synchronizacja** - używaj KeeShare lub Merge do synchronizacji z główną bazą
6. **Tylko hasło bazy w keyring** - wszystkie inne sekrety są wyłącznie w bazie KeePassXC

### Ostrzeżenia

- Hasło bazy jest przechowywane w PowerShell SecretManagement - dostępne tylko dla użytkownika
- Skrypt `get-keepass-secret.sh` próbuje w kolejności:
  1. PowerShell SecretManagement (główna metoda)
  2. secret-tool (jeśli dostępny w WSL)
  3. Wpis w bazie "Cursor Database Password" (jeśli baza otwarta w GUI)
  4. Interaktywnie (ostatni fallback)
- Baza musi być otwarta w GUI, aby odczytać hasło z wpisu "Cursor Database Password"
- **Nie ma fallbacku do pliku** - wszystkie metody używają bezpiecznych mechanizmów keyring

## Rozwiązywanie problemów

### Problem: "Nie można odczytać hasła z bazy"

**Rozwiązanie:**
1. Upewnij się, że baza `cursor.kdbx` jest otwarta w KeePassXC GUI
2. Sprawdź czy wpis "Cursor Database Password" istnieje w bazie
3. Uruchom `save-keepass-password-to-keyring.sh` aby zapisać hasło do SecretManagement

### Problem: "keepassxc-cli: command not found"

**Rozwiązanie:**
```bash
sudo apt update
sudo apt install -y keepassxc
```

### Problem: "Cannot retrieve secret from SecretManagement"

**Rozwiązanie:**
1. Sprawdź czy moduły są zainstalowane:
   ```powershell
   Get-Module -ListAvailable -Name Microsoft.PowerShell.SecretManagement
   ```
2. Jeśli nie, zainstaluj:
   ```powershell
   Install-Module -Name Microsoft.PowerShell.SecretManagement -Scope CurrentUser
   Install-Module -Name Microsoft.PowerShell.SecretStore -Scope CurrentUser
   ```
3. Zarejestruj vault:
   ```powershell
   Register-SecretVault -Name LocalStore -ModuleName Microsoft.PowerShell.SecretStore -DefaultVault
   ```

### Problem: Klucze SSH nie są widoczne w ssh-add

**Rozwiązanie:**
1. Upewnij się, że SSH Agent jest włączony w KeePassXC (Tools → Settings → SSH Agent)
2. Upewnij się, że Windows OpenSSH Agent jest uruchomiony:
   ```powershell
   Set-Service ssh-agent -StartupType Automatic
   Start-Service ssh-agent
   ```
3. Sprawdź czy klucz SSH jest dodany do bazy z konfiguracją SSH Agent

## Synchronizacja baz

Baza `cursor.kdbx` może być synchronizowana z główną bazą `jjaszczak.kdbx` używając:
- **KeeShare** (rekomendowane) - GUI-based synchronizacja
- **Merge** - jednorazowe scalenie baz

Szczegółowe instrukcje w planie integracji.

## Dokumentacja

- Plan integracji: `~/.cursor/plans/keepassxc_integration_setup_6191af80.plan.md`
- Konfiguracja: `~/.cursor/doc/configuration.md`
- Skrypty: `~/.cursor/scripts/`
