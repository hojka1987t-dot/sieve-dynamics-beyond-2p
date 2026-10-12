# Silnik 4.5: dokładne n_{g,j}(p#) dalej niż 53# (11.10.2026)

## Pliki

- **`holt_A_45.py`**: komórka A, zapisuje `holt_worker.py` w wersji 4.5. Interfejs `rozklad_csp` i `zadanie` jest ten sam co w 4.1.
- **`holt_C_etap.py`**: komórka C dla dowolnego etapu (`K`, `BAZA`, `LUKI`). Zapis po każdej luce, z możliwością wznowienia. Uruchomienie: `licz()`.
- **`holt_T_test.py`**: porównuje 4.1 i 4.5 okno po oknie, także tam, gdzie int64 nie wystarcza (73#, 79#).
- **`holt_A_41.py`**: Twoja komórka A, potrzebna do testu.
- **`sufit_45.py`**: szacunek czasu, np. `python sufit_45.py 16 10` (16 rdzeni, 10 ns na operację).
- **`nG59_118_120.csv`**: n_{g,j}(59#) dla g = 118 i 120, policzone tutaj i sprawdzone momentami CRT dla k = 0..4.

Uruchamiaj w CPythonie z numpy (najlepiej numpy ≥ 2.0).

## Co nowego względem 4.3 (wynik ten sam co w 4.1)

1. **Bloki.** Podzbiory węzłów są przetwarzane w blokach po 2^21. Proces zajmuje ok. 0,4 GB niezależnie od liczby węzłów, więc 16 procesów to ok. 6–7 GB. Gdyby pamięci było mało: `BLOK = 20`.
2. **Duże p.** Reszty węzłów modulo p są numerowane w obrębie okna, więc działa dowolnie duże p.
3. **Bez limitu int64.** Gdy iloczyn liczb klas przekracza 2^63, fale są dzielone na grupy z iloczynem poniżej 2^63. Sumy S_k liczone są modulo kilku liczb pierwszych mniejszych od 2^31 i składane chińskim twierdzeniem o resztach. To jest dokładne, bo 0 ≤ S_k < iloczyn modułów. Narzut jest niewielki.

## Sprawdzenia

- **Okno po oknie, 4.5 kontra 4.1** (liczby całkowite Pythona): zgodne przy 53#, 73# i 79#, w tym na ścieżce wielomodułowej.
- **Ścieżka wielomodułowa wymuszona przy 53#**: wynik równy ścieżce int64.
- **Całe luki 40, 60, 80 przy 71#**: równe nG47.csv po pięciu krokach jednorodnych.
- **59#, g = 118 i 120**: momenty CRT dla k ≤ 4 się zgadzają. Na 2 rdzeniach liczyło się 0,7 min i 2,2 min.

## Szacunek czasu

Założenia: 16 rdzeni i 10 ns na (podzbiór × fala), tyle co jeden rdzeń tutaj.

| Etap p0 | Nowe luki (modele Holta z p0) | Czas |
|---|---|---|
| 59# | 118–120 | minuty |
| 61# | 122–132 | ok. 6 min |
| 67# | 134–140 | ok. 15 min |
| 71# | 142–144 | ok. 20 min |
| 73# | 146–156 | ok. 3–4 h |
| 79# | 158–164 | ok. 8 h |
| 83# | 166–176 | ok. 65 h |

Każdy kolejny etap jest mniej więcej 8 razy droższy.

Na 16 rdzeni zalecane jest koło 11# (`BAZA = 5`). Koło 7# daje tylko kilkadziesiąt okien, więc rdzenie nie byłyby równo obciążone.

Przy 83# pojedyncze największe okno to ok. 14 h na jednym rdzeniu. To ono wyznacza minimalny czas, chyba że podzielić bloki jednego okna między procesy.
