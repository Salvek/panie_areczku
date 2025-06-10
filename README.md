# Panie Areczku

---

## 📝 Opis projektu

Symulacja systemu logistycznego w Pythonie. Aplikacja generuje losową planszę z punktami (klientami i magazynami), tworzy flotę ciężarówek i wyznacza dla nich trasy. Każda ciężarówka obsługuje punkty na swojej trasie, dostarczając lub odbierając towary.

---

## 📂 Struktura repozytorium


---
````
panie_areczku/
├── README.md
├── requirements.txt
└── src
    ├── board.py          # logika planszy i jej wizualizacja
    ├── config.py         # parametry aplikacji
    ├── fleet.py          # tworzenie i obsługa floty
    ├── main.py           # punkt wejścia programu
    ├── point.py          # definicja punktu na planszy
    ├── truck.py          # model ciężarówki i obsługa trasy
    ├── util
    │   ├── __init__.py
    │   └── move_truck.py # funkcje planowania i przemieszczania ciężarówki
    └── PM
        └── pm.jpg        # zdjęcie prject managera
````
---

## Specyfikacja wymagań projektu

- **Magazyny:** 5 punktów (nieograniczona pojemność)
- **Pojazdy:**
  - Zielone – 1000 kg
  - Niebieskie – 1500 kg
  - Czerwone – 2000 kg
- **Towary:** Pomarańcze, Uran, Tuńczyk (zapotrzebowanie losowe)
- **Easter egg:** Kot konsumujący tuńczyka (1 kg/km trasy)

---

## 🛠 Technologie i metody

**Technologia:** Python 3.11  
**Biblioteki:**
- NumPy
- Matplotlib

**Metody optymalizacji:**
- Algorytmy zachłanne
- Heurystyki optymalizacyjne
- Algorytm symulowanego wyżarzania (Simulated Annealing)
- 2-OPT (optymalizacja lokalna)

---

## 🚀 Uruchomienie projektu

1. **Klonowanie repozytorium**
```bash
git clone https://github.com/Salvek/panie_areczku.git
cd panie_areczku
```

## Ogólny algorytm

Poniższy pseudokod opisuje główne kroki aplikacji:

```
1. Utwórz Board i wypełnij go losowymi punktami.
2. Wybrane punkty oznacz jako magazyny.
3. Wygeneruj losową flotę ciężarówek (niektóre posiadają kota zjadającego tuńczyka).
4. Podziel klientów pomiędzy dostępne magazyny.
5. Dla każdego magazynu wyznacz trasę do obsługi swoich klientów
   (algorytm najbliższego sąsiada – `plan_route`).
6. Przypisz wygenerowane trasy ciężarówkom z floty.
7. Dla każdej ciężarówki:
   a. Załaduj towary potrzebne na całej trasie.
   b. Jedź po punktach w zaplanowanej kolejności,
      dostarczaj i odbieraj ładunek,
      a w razie potrzeby wracaj do magazynu lub szukaj innego źródła.
   c. Zapisuj przebytą drogę i wykonane kroki.
   d. Jeśli pozostały nieobsłużone punkty – spróbuj ponownie.
8. Po zakończeniu kursów wypisz raport stanu punktów
   i wyświetl wizualizację z przebytymi trasami.
```


