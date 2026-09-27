# Data

All files in this folder were computed in this project. Third-party data are not redistributed (see the main README).

## Population matrices `nG*.csv`

Format of Holt's tables: one row per span, `Gap Sum = g`; column `Totals` is the sum over lengths; columns `Length = j` give
n_{g,j}(p#), the number of driving terms of span g consisting of j consecutive gaps in one period of the cycle G(p#). Empty cells are zero.

| File | Stage | Spans |
|---|---|---|
| `nG41.csv`, `nG41_92.csv`, `nG41_110.csv` | G(41#) | g <= 82, 92, 110 |
| `nG43.csv`, `nG43_104.csv` | G(43#) | g <= 92, 104 |
| `nG47.csv` | G(47#) | g <= 104 |

Checks: agreement with Holt's G(37#) data propagated by his recursion; column sums equal the number of admissible pairs; the populations of gaps in G(53#) predicted from `nG47.csv` agree with an independently computed profile (52/52); the leading coefficient of Holt's model equals the Hardy-Littlewood constant for g = 84..104 (11/11).

## Pair structures `pary_G37.json`, `pary_G41.json`, `pary_G43.json`

For the transition p -> q (q = next prime): `{ "g": { "j,a,b": count } }`, where j is the length of the driving term,
a the number of interior points at distance 2q from an endpoint, b the number of pairs of interior points at distance 2q.
Used to verify the transition law in the band 2q <= g < 4q.

## `klasyfikacja.json` — classification of Ziller's missing differences, k+1 = 19..30

Keys (Polish): `k+1` stage, `g` missing difference, `etap_k` stage searched, `baza` wheel size, `a` = 2q,
`werdykt` = `OPOZNIENIE` (lag: no constellation (2q, g-2q) exists) or `ZABOJSTWO` (blocked birth), `okien` windows searched,
`budzet` budget exceeded (false everywhere). All 15 entries are lags.

## `verification_logs/`

Logs of the exhaustive verifier of Ziller's table for k = 27..30 (`k_*.txt`) and of the validation against Holt's G(37#) data (`waliacja.txt`).
