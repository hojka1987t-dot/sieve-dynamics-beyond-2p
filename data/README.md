# Data

All files in this folder were computed in this project. Third-party data are not redistributed (see the main README).

## Population matrices `nG*.csv`

Format of Holt's tables: one row per span, `Gap Sum = g`; column `Totals` is the sum over lengths; columns `Length = j` give
n_{g,j}(p#), the number of driving terms of span g consisting of j consecutive gaps in one period of the cycle G(p#). Empty cells are zero.

| File | Stage | Spans | Method |
|---|---|---|---|
| `nG41.csv`, `nG41_92.csv`, `nG41_110.csv` | G(41#) | g <= 82, 92, 110 | first |
| `nG43.csv`, `nG43_104.csv` | G(43#) | g <= 92, 104 | first |
| `nG47.csv` | G(47#) | g <= 104 (initial conditions p0 = 47) | first |
| `nG53_106_112.csv` | G(53#) | controls 20, 30, 40; 106-112 (written by `code/engine/holt_C_53.py` as `nG53_nowe.csv`) | first |
| `nG53_45.csv` | G(53#) | controls 20, 40, 60; 114, 116 | second |
| `nG59_45.csv` | G(59#) | controls; 118, 120 | second |
| `nG61_45.csv` | G(61#) | controls; 122-132 | second |
| `nG67_45.csv` | G(67#) | controls; 134-140 | second |
| `nG71_45.csv` | G(71#) | controls; 142, 144 | second |
| `nG73_45.csv` | G(73#) | controls; 146-150 | second |

First method: dynamic programming over uncovered nodes (`code/engine/`). Second method: inclusion-exclusion over node subsets
(`code/engine_45/`). Checks: for 47#, agreement with Holt's G(37#) data propagated by his recursion and with an independent
profile of G(53#) (52/52). For g >= 106: the two methods give identical matrices for 106-112; for every gap the sum over all
lengths equals the number of pairs at distance g in G(p0#), and the moments for k <= 4 agree with Theorem 3.7 evaluated
independently; at every stage the control gaps agree with `nG47.csv` carried forward by uniform steps
(`code/engine_45/kontrola_etapu.py`). The leading coefficient of Holt's model equals the normalised singular series
S(g)/S(2) for every gap.

## Coefficients `wspolczynniki_l.csv`

All nonzero coefficients l_j of Holt's models for even g <= 150: columns `g`, `p0`, `j`, the exact value as a fraction and
its decimal value. Produced by `code/analysis/generuj_150.py`, which also writes Table 1 and Appendix A of the paper.

## Pair structures `pary_G37.json`, `pary_G41.json`, `pary_G43.json`

For the transition p -> q (q = next prime): `{ "g": { "j,a,b": count } }`, where j is the length of the driving term,
a the number of interior points at distance 2q from an endpoint, b the number of pairs of interior points at distance 2q.
Used to verify the transition law in the band 2q <= g < 4q.

## Ziller's table of missing differences

- `klasyfikacja.json` - classification of the missing differences, k+1 = 19..30. Keys (Polish): `k+1` stage, `g` missing
  difference, `etap_k` stage searched, `baza` wheel size, `a` = 2q, `werdykt` = `OPOZNIENIE` (delay: no constellation
  (2q, g-2q) exists) or `ZABOJSTWO` (blocked birth), `okien` windows searched, `budzet` budget exceeded (false everywhere).
  All 15 entries are delays.
- `swiadkowie_M2.json` - for every row of Table 2, a qualifying pair of adjacent gaps whose sum is the reach of pairs M2.
- `narodziny_maksimow.json` - the birth of the maximum of G(p_k#) for k = 20..30 (pair or coincident triple).
- `klasyfikacja_pasm_k20_27.json` - all 54 new differences h(k-1) < g <= h(k) for 20 <= k <= 27: a pair witness (`para`),
  a coincident witness (`koincydentne`) where one is known, and the route (`droga`).
- `closure_k30_326.json` - the pair sum 326 at k = 30 (also contained in `swiadkowie_M2.json`).

**Witness convention.** A witness is an integer X. The gap g occurs in G(p_k#) at X if X and X + g are coprime to p_k#
and every integer strictly between them has a common factor with p_k#. The constellation lists the gaps that the same
interval spans at the previous stage, that is, with respect to p_{k-1}#: one interior point for a pair, two points at
distance 2p_k for a coincident birth. Every witness can be checked with `gcd` alone.

## `verification_logs/`

Certificates of the exhaustive verifier of Ziller's table: `k_27`, `k_28` (base 9) and `k_29`, `k_30` (base 10);
`k_22` to `k_25` (base 7), with the witness for every present difference in `swiadkowie_k*__baza_7.json`;
validation against Holt's G(37#) data (`waliacja.txt`).

## `windows/` (Part II)

- `profiles/profil_z{p}.txt` - for N = p#, one line per even y: y, W_N(y), and residue classes a_2, a_3, ..., a_p of an
  optimal window: position t in [0, y] is removed by the prime l exactly when t = a_l (mod l). Computed by branch and bound
  (`code/windows/`). `profil_rek_z79.txt` was computed by the certified recursion; columns as in its header
  (y, W_79#(y), last level J, certificate, C_0..C_J, time in seconds).
- `mapa_glebokosci.txt` - the recursion chain 13# -> 37# for long windows (Table 8); columns as in its header
  (q, y, W, depth, certificate, C_0..C_J, time).
- `full_enumeration/szt_wyniki_r{7,8,9}.txt` - complete enumeration for N = 17#, 19#, 23#: y, W_N(y), W_qN(y), depths of the
  ancestors of the optimal windows, the largest class C_j at each level (as `j:C_j`), completeness flag, windows checked.
- `depth_analysis/` - `dane_q{13,17,19}.json`: one record per length, [y, n, S(n), capacity increase (0/1), W, C_0, C_1,
  C_2, depth]; `krotnosci.json`: the number of optimal windows for each length. Used for the depth statistics of Section 9.
