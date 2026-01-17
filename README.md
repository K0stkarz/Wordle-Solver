# Wordle Solver - Premium

Profesjonalne narzędzie wspomagające rozwiązywanie zagadek typu Wordle, napisane w języku Python z wykorzystaniem frameworka Kivy. Aplikacja oferuje nowoczesny interfejs graficzny, wysoką wydajność oraz możliwość dostosowania wyglądu do preferencji użytkownika.


## Główne Funkcje

* **Zaawansowany algorytm filtrowania:** Błyskawiczne wyszukiwanie pasujących słów na podstawie wprowadzonych kryteriów.
* **Obsługa wszystkich reguł Wordle:**
    * **Litery wykluczone:** Litery, które nie występują w haśle (szare).
    * **Litery na pozycjach:** Litery trafione idealnie (zielone).
    * **Litery nie na pozycjach:** Litery obecne w haśle, ale w innym miejscu (żółte).
* **Skalowanie interfejsu (DPI):** Możliwość zmiany wielkości GUI (od 1.0x do 2.0x) dla komfortowej pracy na monitorach o wysokiej rozdzielczości (2K/4K).
* **Elastyczna długość słowa:** Obsługa haseł o długości od 2 do 11 znaków.
* **Pamięć ustawień:** Aplikacja zapamiętuje wybraną skalę oraz długość słowa po ponownym uruchomieniu.
* **Tryb Ciemny:** Nowoczesny design oparty na palecie kolorów `#1B1B1E` i `#25F7BF`.

## Instalacja

### Wymagania wstępne
* Python 3.10 lub nowszy
* System operacyjny: Windows, macOS lub Linux (testowano na Fedorze)

### Krok po kroku

1.  **Sklonuj repozytorium (lub pobierz pliki):**
    ```bash
    git clone [https://github.com/twoj-login/wordle-solver.git](https://github.com/twoj-login/wordle-solver.git)
    cd wordle-solver
    ```

2.  **Przygotuj strukturę katalogów:**
    Upewnij się, że posiadasz plik słownika. Aplikacja szuka go w ścieżce: `../Data/slowa.txt` względem pliku `app.py`.
    ```text
    Projekt/
    ├── Data/
    │   └── slowa.txt       # Twój plik ze słownikiem
    └── src/
        ├── app.py          # Główny plik aplikacji
        ├── requirements.txt
        ├── utils/
        │   └── wordFinder.py
        └── ui/
            ├── eventHandlers.py
            └── ... (elementy UI)
    ```

3.  **Utwórz wirtualne środowisko (zalecane):**
    ```bash
    python -m venv venv
    
    # Linux / macOS:
    source venv/bin/activate
    
    # Windows:
    .\venv\Scripts\activate
    ```

4.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

## Uruchomienie

Będąc w katalogu `src`, uruchom polecenie:

```bash
python app.py