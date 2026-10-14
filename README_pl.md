# Porządkowanie Plików
## Autor: Kornelia Błaszczuk

## Opis projektu

**Porządkowanie Plików** to aplikacja napisana w języku Python, zaprojektowana do organizowania plików w wybranych katalogach. Wykrywa typowe problemy związane z zarządzaniem plikami, takie jak duplikaty, pliki tymczasowe, puste pliki, problematyczne nazwy plików oraz nieprawidłowe uprawnienia.

Aplikacja umożliwia analizowanie katalogu głównego i dodatkowych katalogów, identyfikowanie plików wymagających uwagi oraz wykonywanie operacji pomagających utrzymać porządek w plikach.

## Funkcje

Aplikacja obsługuje następujące funkcje:

- **Wykrywanie identycznej zawartości** – identyfikuje pliki o identycznej zawartości i ustala, który z nich jest najstarszy.
- **Wykrywanie identycznych nazw plików** – wyszukuje pliki o takich samych nazwach.
- **Wykrywanie problematycznych nazw plików** – identyfikuje nazwy zawierające znaki uznane za problematyczne.
- **Wykrywanie plików tymczasowych** – wykrywa pliki na podstawie rozszerzeń określonych w konfiguracji.
- **Wykrywanie pustych plików** – identyfikuje pliki o rozmiarze zero bajtów.
- **Sprawdzanie uprawnień do plików** – wykrywa pliki, których uprawnienia różnią się od skonfigurowanej wartości.
- **Organizowanie plików** – umożliwia przenoszenie plików do wybranego katalogu i wykonywanie dostępnych operacji zarządzania plikami.
- **Konfiguracja** – pozwala określić domyślne uprawnienia do plików, problematyczne znaki, znak zastępczy oraz rozszerzenia plików tymczasowych.

## Wymagania

- Python w wersji 3.10 lub nowszej.
- Moduły standardowej biblioteki Pythona wykorzystywane przez projekt.
- `pytest` – jeśli chcesz uruchamiać testy automatyczne.

## Konfiguracja

Ustawienia aplikacji są zdefiniowane w pliku `config.py`. Można skonfigurować następujące parametry:

- `permission_set` – domyślne uprawnienia do plików.
- `problematic_symbols` – lista znaków uznawanych za problematyczne w nazwach plików.
- `substitute_symbol` – znak używany do zastępowania problematycznych znaków.
- `temporary` – lista rozszerzeń używanych do identyfikowania plików tymczasowych.

## Uruchamianie aplikacji

Katalogi przeznaczone do analizy należy przekazać za pomocą argumentów wiersza poleceń obsługiwanych przez aplikację. Aby wyświetlić dostępne argumenty, uruchom:

```bash
python3 cli.py --help
```

## Testowanie ręczne

Aplikację można testować ręcznie, wykorzystując przykładowe katalogi zawierające pliki o różnych właściwościach. Pozwala to sprawdzić, czy każdy tryb działania wykrywa odpowiednie problemy i proponuje właściwe działania.

### Struktura katalogów testowych

Do testowania ręcznego wykorzystaj trzy katalogi:

- `tests/X` – katalog główny.
- `tests/Y1` – pierwszy katalog dodatkowy.
- `tests/Y2` – drugi katalog dodatkowy.

Aplikacja analizuje wskazane katalogi, traktując pierwszy katalog (`X`) jako katalog główny.

### Dostępne tryby działania

Uruchom aplikację, używając jednego z poniższych trybów:

| Tryb | Opis |
|---|---|
| `duplicate-content` | Wykrywa pliki o identycznej zawartości i wskazuje najstarszy plik. |
| `duplicate-name` | Wykrywa pliki o takich samych nazwach. |
| `problematic-name` | Wykrywa nazwy zawierające skonfigurowane problematyczne znaki i sugeruje ich normalizację. |
| `temporary` | Wykrywa pliki tymczasowe na podstawie rozszerzeń określonych w konfiguracji. |
| `empty` | Wykrywa pliki o rozmiarze zero bajtów. |
| `permissions` | Wykrywa pliki, których uprawnienia różnią się od wartości domyślnej określonej w konfiguracji. |
| `move` | Przenosi pliki z dodatkowych katalogów do katalogu głównego, zgodnie z zaimplementowanymi zasadami. |

### Polecenia do testowania ręcznego

Poniższe polecenia należy uruchamiać z głównego katalogu projektu.

**1. Wykrywanie plików o identycznej zawartości**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode duplicate-content
```

**2. Wykrywanie plików o identycznych nazwach**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode duplicate-name
```

**3. Normalizacja problematycznych nazw plików**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode problematic-name
```

**4. Wykrywanie plików tymczasowych**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode temporary
```

**5. Wykrywanie pustych plików**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode empty
```

**6. Normalizacja uprawnień do plików**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode permissions
```
**7. Przenoszenie plików do katalogu głównego**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode move
```
### Tryb interaktywny i symulacja działania

Opcja `-i` lub `--interactive` włącza pytania o potwierdzenie przed wykonaniem poszczególnych operacji.

Aby wyświetlić planowane operacje bez modyfikowania plików, użyj opcji `--dry-run`. Na przykład:

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 --dry-run --mode problematic-name
```

Tryb symulacji powinien wyświetlać planowane działania bez faktycznej zmiany nazw, usuwania ani przenoszenia plików.

### Sprawdzanie konfiguracji

Przed rozpoczęciem testowania sprawdź, czy konfiguracja zawiera oczekiwane wartości:

- `permission_set` – domyślne uprawnienia do plików, na przykład `0o644`.
- `problematic_symbols` – znaki, które mają być zastępowane w nazwach plików.
- `substitute_symbol` – znak zastępczy, na przykład `_`.
- `temporary` – rozszerzenia plików tymczasowych, na przykład `.tmp` i `.temp`.

## Uruchamianie testów

Aby uruchomić testy automatyczne, wykonaj polecenie:

```bash
python3 -m pytest -v
```

## Bezpieczeństwo

Przed wykonaniem operacji takich jak usuwanie, zastępowanie lub przenoszenie plików upewnij się, że wybrane zostały właściwe katalogi. Podczas tworzenia i testowania aplikacji zaleca się korzystanie z katalogów testowych zawierających przykładowe pliki, aby uniknąć przypadkowej utraty danych.