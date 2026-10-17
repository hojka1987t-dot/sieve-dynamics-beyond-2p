# Exact populations of driving terms for constellations of consecutive gaps

Pairs, triples and quadruples of consecutive gaps with span at most 104, in the cycles G(p#) for p = 5, 7, ..., 47.
T. Hojka, October 2026. Code: `code/constellations/`.

## Files

| file | content |
|---|---|
| `pairs_triples/nK<p>_constellations.csv` | 514 pairs and 6101 triples at p# |
| `quadruples/nQ<p>_quadruples.csv.gz` | 45 857 quadruples at p# (gzip-compressed CSV, same format) |
| `gaps/nG<p>_gaps.csv` | gaps of span at most 104 at p# (p = 5, ..., 43), used in the checks; for 47# see `data/nG47.csv` |
| `model_coefficients_p0_47.csv` | exact coefficients of Holt's models for all pairs and triples from p0 = 47 |
| `missing_constellations.txt` | missing pairs, triples and quadruples at every stage, with their causes |
| `survival_104.txt` | survival test for pairs and triples of span at most 104 among the primes up to 10^9 (output in Polish: rozpietosc = span, pary = pairs, trojki = triples; median relative deviation and chi^2 per degree of freedom) |

Rows have the format of the nG files: `Constellation = a,b,c`, total, then n_{s,J}(p#) for J = 1, 2, ..., where J is the
number of gaps of the driving term. Only one of s and its reversal is listed; the reversal has the same populations.
Stages up to 13# were computed by full enumeration of the cycle, from 17# on by the engine of version 3 of the paper
(doi:10.5281/zenodo.23007182) extended to constellations, i.e. Theorem 3.7 with all points of the
constellation forced.

## Models

For a constellation with m gaps: L_j = sum_{i>=j} C(i-m, j-m) n_{s,i}(47#), D_m = prod_{m+1 < p <= 47} (p-m-1),
l_k = L_{m+k-1} / D_m, and w_s(p#) = sum_k (-1)^(k-1) l_k prod_{47 < q <= p} (q-m-k)/(q-m-1).
This is the normalisation of Holt (arXiv:2502.20470); every step from 53 on is uniform for span at most 104.
l_1 is the asymptotic relative population.

## Checks

- for every constellation and stage the total equals the CRT count prod_p (p - nu_p);
- the sums over all pairs, triples and quadruples of span g equal (J-1) n_{g,J}, C(J-1,2) n_{g,J} and C(J-1,3) n_{g,J}
  for the gaps at the same stage;
- consecutive, independently computed stages satisfy the uniform recursion exactly wherever span < 2p
  (97 732 checks for pairs, triples and quadruples together);
- the gap rows at 37# equal Holt's nG37.csv; the gap rows from two independent runs are identical;
- l_1 equals prod_{p<=m+1}(p-nu_p) * prod_{p>m+1}(p-nu_p)/(p-m-1) exactly for all pairs and triples, and for m = 1 the
  coefficient code reproduces the published gap coefficients.

All checks are repeated by `code/constellations/check_all.py` and `models_p0_47.py`.

## Results in brief

- Missing pairs are all delays, as missing gaps are. Triples show blocked births at 7#, ..., 23# and 31#, all of the form
  (q-1, 2, q'-1): with N the product of the primes below q, the points N - q and N + q lie in the same class mod q.
  Quadruples show 49 blocked births up to 41#: some at distinguished points of the cycle (N, N/2, N/3, N/6), the others
  where the only driving term with one extra point has that point 2q away from an end point.
- Survival test: pairs and triples up to span 104 agree with the cycle at Polya's cutoff z(x) of the Banks-Ford-Tao model
  within sampling noise, and not at the level sqrt(x).
