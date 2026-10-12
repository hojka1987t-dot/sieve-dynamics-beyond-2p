# Eratosthenes sieve dynamics beyond 2p

**Author:** Tomasz Hojka (independent researcher)  
**Preprint:** <https://doi.org/10.5281/zenodo.23007182> (all versions; this release accompanies version 3)  
**Code and data:** <https://doi.org/10.5281/zenodo.23009304> (all versions; this is release v2.0.0)

This repository contains the code, data and verification scripts that accompany the preprint.

## What this is about

At each stage of Eratosthenes sieve the numbers coprime to a modulus N (for example a primorial p#) form a periodic *cycle of gaps* G(N). Adding the next prime q produces G(qN). F. B. Holt has shown that the populations of gaps and of their *driving terms* evolve by an exact linear system, but only for spans smaller than 2q; beyond that threshold several points of one driving term can be removed in the same copy, and the length of the resulting term was not determined.

Part I gives the exact transition law for **all spans**, resolved by residue classes modulo q, and draws consequences for Holt's population models, for M. Ziller's table of missing differences and for the birth of maximal gaps (Jacobsthal's function of primorials, OEIS A048670). Part II studies windows with the least number of survivors (the function φ_min of Costello and Watts) and the depth, above this minimum, of the windows from which the minimum at the next stage arises.

## Main results

**Proven**

- **Transition law (all spans).** Each residue class of the points of a driving term modulo q is removed in exactly one of the q lifts; classes are sets of points pairwise 2q, 4q, … apart. This determines the length of every lift. The criterion that two points fall into the same lift exactly when q divides their distance is Holt's (arXiv:2502.20470, Lemma 3.1); what is new is that it determines the lengths of all lifts.
- **Ladder of thresholds.** If 3 | N and q ≠ 3, classes of 2, 3, 4 and 5 points span at least 2q, 6q, 8q and 12q; all four thresholds are attained in the tests.
- **Moment form.** In binomial moments S_k the dynamics is diagonal with a nonnegative source: `S_k(qN) = (q − m − 1 − k)·S_k(N) + Π_k(N)`, with `Π_k ≥ 0`.
- **Birth law.** A gap is born at stage qN exactly from a qualifying constellation: one whose interior points removed by q form one residue class disjoint from the endpoints. For primorials with k ≤ 18 this gives `D(k+1) = D(k) ∪ {sums of two adjacent gaps of G(p_k#)}`.
- **Constellations.** The same laws for arbitrary constellations, a persistence lemma and a criterion for first appearance.
- **Holt's chain on lengths** is exact at a transition **if and only if** no populated shape has two points congruent modulo q (Theorem 5.2, with an explicit formula for the excess).
- **Part II.** The minimum number of survivors at the next stage is attained by windows at depth 0 for spans below 6q and at depth at most 1 below 8q; a certified recursion computes φ_min from the previous stage.

**Computed**

- **Exhaustive verification** for every constellation of span at most 40 on all cycles up to 19# and on sieves with an omitted small prime: 63 731 shape identities and 254 835 constellations without error; the excess formula of Theorem 5.2 in all 243 117 cases where it applies.
- **Ziller's missing differences up to k = 30:** all 20 are *delays*. 17 are *holes* below the reach of pairs and 3 lie in the *shadow* of a maximal gap born coincidently (186, 188 at k = 21; 328 at k = 30). Witnesses for every value of the reach of pairs M₂ in Table 2 and for all 54 new differences at 20 ≤ k ≤ 27 (50 arise from pairs, 4 only coincidently, all maxima) are in `data/`, each checkable by gcd. The table was verified again for k = 22–25 (logs in `data/verification_logs/`).
- **Birth of maximal gaps** (n ≤ 54 from Ziller's and Morack's complete lists, n ≤ 64 from the OEIS A048670 table): every maximum is born either from a pair of adjacent gaps or from a triple with middle gap exactly 2pₙ.
- **Holt's models** for all even gaps g ≤ 150: initial conditions at p₀ = 47 for g ≤ 104 and at p₀ = 53, 59, 61, 67, 71, 73 for larger gaps; the leading coefficient equals the normalised singular series 𝔖(g)/𝔖(2) for every gap. The matrices for 106 ≤ g ≤ 112 were computed by two independent exact methods with identical results.
- **Survival test.** All primes between 47² and 10⁹: the gaps g ≤ 104, and the pairs and triples of consecutive gaps of span at most 40, follow the cycle at the level x^(1/e^γ) of the Banks–Ford–Tao model within sampling noise, and not at the level √x of Holt's survival hypothesis.
- **Part II.** Depth at most 1 in all 3943 computed cases up to about 20q, and at most 2 in all computed windows up to about 230q; depth 2 occurs in clusters, associated with a small number of optimal windows.

**Not claimed:** anything proved about the actual gaps between primes (the survival test is empirical); a proof of Ziller's Conjecture 4.1 (only a reformulation); that the depth of Part II is bounded (an open question).

## Repository layout

| Folder | Contents |
|---|---|
| `paper/` | the paper: LaTeX source and PDF of version 3 |
| `data/` | population matrices n(g, j) for 41#, 43#, 47# and, for g ≥ 106, for 53#–73#; exact coefficients of Holt's models (`wspolczynniki_l.csv`); witnesses for Table 2 and for the births in the bands; classifier results; verifier logs (see `data/README.md`) |
| `data/windows/` | profiles W_N(y) for 29#–73# and the recursion for 79#, the depth map, full enumerations, depth statistics |
| `code/engine/` | first exact method for n(g, j): dynamic programming over uncovered nodes (PyPy) |
| `code/engine_45/` | second exact method: inclusion–exclusion over node subsets with exact integer arithmetic (CPython + numpy); stage checks `kontrola_etapu.py` |
| `code/exhaustive/` | exhaustive verification of Part I and of Theorem 5.2 |
| `code/survival/` | sieve up to 10⁹ and the survival tests of Section 6.4 |
| `code/windows/` | Part II: branch and bound for W_N(y), depth tests, certified recursion, full enumerations, depth statistics |
| `code/ziller_verifier/` | exhaustive verifier of Ziller's table of missing differences; targeted search for pair witnesses |
| `code/classifier/` | classifier delay / blocked birth, closure of the table, rescue check |
| `code/sat_check/` | independent check with a SAT model solved by Google OR-Tools CP-SAT |
| `code/brute_force/` | full-cycle brute-force verification of the theorems, the "sieve laboratory", the audit |
| `code/analysis/` | birth of maximal gaps, Holt's models and their coefficients (`generuj_150.py` produces Table 1 and Appendix A), Holt's Figure 6 |
| `docs/` | working notes for version 2 of the paper (Polish); where they differ, the paper is authoritative |

## Running

Python 3.10+ and `numpy`; `ortools` for `code/sat_check`. Quick checks (minutes):

```
cd code/brute_force && python bf.py && python kon.py && python nar.py && python pakiet.py && python audyt.py
cd code/analysis   && python holt_models.py ../../data/nG47.csv && python holt_fig6.py
cd code/exhaustive && python weryfikacja_wyczerpujaca.py "2,3,5,7" 11 40 40 && python test_koniecznosci.py
```

`weryfikacja_wyczerpujaca.py` takes the primes of N, the prime q and the two spans; the ten calls behind Table 6 are listed in `wyniki_weryfikacji.txt`. `test_koniecznosci.py` and `test_koniecznosci_reszta.py` check the excess formula of Theorem 5.2 on the same transitions.

Survival test: `python sito.py` (sieve up to 10⁹, writes `sito_1e9.npz`) and `python sito_konst.py`, then `test_przetrwania.py`, `test_przetrwania_konstelacje.py` and `rozrzut.py` in the same folder.

The engines, the verifier, the classifier and the computations of Part II were run in JupyterLab on Windows with multiprocessing. Each component consists of a cell **A**, which writes a worker module to disk, and further cells that load it and run the computation; paste them as separate notebook cells. The first engine was run under PyPy, the second requires CPython with numpy. Long runs took from minutes to about a day on 16 cores.

## Third-party data (not included)

- Holt's population data for G(37#): <https://github.com/fbholt/Primegaps-v2>
- Complete lists of maximal configurations for n ≤ 54: ancillary file `remainders.txt` of M. Ziller and J. F. Morack, arXiv:1611.03310
- OEIS A048670 table with start positions (R. Gerbicz; values n = 62–64 computed by A. Bożek): <https://oeis.org/A048670>

## References

- F. B. Holt, H. Rudd, *Combinatorics of the gaps between primes*, arXiv:1510.00743 (2015)
- F. B. Holt, *Models for gaps g = 2p₁*, arXiv:2309.16833 (2023)
- F. B. Holt, *Eratosthenes sieve supports the k-tuple conjecture*, arXiv:2502.20470 (2025)
- F. B. Holt, *Discrete dynamics of Eratosthenes sieve*, arXiv:2608.26384 (2026)
- F. B. Holt, *Surviving Eratosthenes sieve I: quadratic density and Legendre's conjecture* arXiv:2603.25915 (2026)
- W. Banks, K. Ford, T. Tao, *Large prime gaps and probabilistic models*, Invent. Math. (2023)
- F. Costello, P. Watts, *A computational upper bound on Jacobsthal's function*, Math. Comp. (2015)
- M. Ziller, *On differences between consecutive numbers coprime to primorials*, arXiv:2007.01808 (2020)
- M. Ziller, J. F. Morack, *Algorithmic concepts for the computation of Jacobsthal's function*, arXiv:1611.03310 (2016)
- T. Hagedorn, *Computation of Jacobsthal's function h(n) for n < 50*, Math. Comp. 78 (2009), 1073–1087

## How to cite

The paper: T. Hojka, *Exact dynamics of Eratosthenes sieve beyond 2p: coincident fusions, births of gaps and missing differences*, preprint, version 3 (2026), doi:10.5281/zenodo.23007182.

The code and data: T. Hojka, *Eratosthenes sieve dynamics beyond 2p: code, data and verification*, version v2.0.0 (2026), doi:10.5281/zenodo.23009304.

## AI assistance

Claude (Anthropic) assisted with parts of the code, the computations and the drafting. The author takes full responsibility for the content.

## Language

Code comments and working notes are in Polish; the paper is in English.

## License

Code: MIT (`LICENSE`). Data and documents: CC BY 4.0 (`LICENSE-DATA`).
