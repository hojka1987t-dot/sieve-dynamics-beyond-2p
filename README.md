# Eratosthenes sieve dynamics beyond 2p

**Author:** Tomasz Hojka (independent researcher)  
**Preprint:** <https://doi.org/10.5281/zenodo.23007183>  
**Code and data, release v1.0.0:** <https://doi.org/10.5281/zenodo.23009305>

This repository contains the code, data and verification scripts that accompany it.

## What this is about

At each stage of Eratosthenes sieve the numbers coprime to a modulus N (for example a primorial p#) form a periodic *cycle of gaps* G(N). Adding the next prime q produces G(qN). F. B. Holt has shown that the populations of gaps and of their *driving terms* evolve by an exact linear system, but only for spans smaller than 2q; beyond that threshold several points of one driving term can be removed in the same copy, and the length of the resulting term was not determined.

This work gives the exact transition law for **all spans**, resolved by residue classes modulo q, and draws consequences for Holt's population models, for M. Ziller's table of missing differences and for the birth of maximal gaps (Jacobsthal's function of primorials, OEIS A048670).

## Main results

**Proven, with independent computational verification**

- **Transition law (all spans).** Each residue class of the points of a driving term modulo q is removed in exactly one of the q lifts; classes are sets of points pairwise 2q, 4q, … apart. This determines the length of every lift. Verified on full cycles by brute force (1585 cells, including sieves in which a small prime is omitted, so that multi-point removals are frequent), with the counting engine on the prime sieve (805 cells: 23#→29#, 37#→41#, 41#→43#, 43#→47#), and in an audit that includes spans ≥ N. The criterion that two points fall into the same lift exactly when q divides their distance is Holt's (arXiv:2502.20470, Lemma 3.1); what is new is that it determines the lengths of all lifts.
- **Ladder of thresholds.** Classes of 2, 3, 4, 5 points first appear at spans 2q, 6q, 8q, 12q (the bound for 3 points is proved via residues mod 3; higher ones follow Hagedorn 2009). All four thresholds are attained in the tests.
- **Moment form.** In binomial moments S_k the dynamics is diagonal with a nonnegative source: `S_k(qN) = (q − k − 2)·S_k(N) + Π_k(N)`, with `Π_k ≥ 0`.
- **Birth law.** A gap is born at stage qN exactly from a driving term whose interior points form one residue class mod q disjoint from the endpoints; equivalently from constellations whose end gaps are not multiples of 2q and whose middle gaps are. For primorials with k ≤ 18 this gives `D(k+1) = D(k) ∪ {sums of two adjacent gaps of G(p_k#)}`.
- **Constellations.** The same laws for arbitrary constellations, a persistence lemma, a criterion for the first appearance of a constellation, and a sufficient condition for the exactness of Holt's Markov chain on lengths.

**Computed**

- **Ziller's missing differences up to k = 30:** all 20 are *delays* — none is caused by a blocked birth. 17 are *holes* in the set of sums of adjacent pairs and 3 lie in the *shadow* of a maximal gap born from a triple (186, 188 at k = 21; 328 at k = 30). Independent confirmation with the CP-SAT solver for 10 of the 14 computed cases.
- **Birth of maximal gaps** (n ≤ 54 from Ziller's complete lists of maximal configurations, n ≤ 64 from the OEIS A048670 table): every maximum is born either from a pair of adjacent gaps or from a triple with middle gap exactly 2pₙ; the second route appears first at n = 21 and is the more frequent one afterwards. An earlier extrapolation ("only triples from n = 47 on") was **refuted** by the data for n = 55–64.
- **Holt's models:** exact models for gaps 84 ≤ g ≤ 104 from initial conditions at 47#; the leading coefficient equals the Hardy–Littlewood constant for all 11 gaps, as required by Holt's Theorem 1.1 (arXiv:2608.26384; Corollary 1.2 of arXiv:2502.20470) — a check of the totals; Holt's Figure 6 (constellation 2,10,2,10,2) is reproduced for the three transitions that lie outside his linear model.

**Not claimed:** anything about the actual gaps between primes; a proof of Ziller's Conjecture 4.1 (only a reformulation); necessity of the condition for Holt's chain.

## Repository layout

| Folder | Contents |
|---|---|
| `data/` | our population matrices n(g, j) for 41#, 43#, 47#; pair structures; classifier results; verifier logs (see `data/README.md`) |
| `code/engine/` | counting engine for n(g, j) at p#, pair structures, gap profiles |
| `code/ziller_verifier/` | exhaustive verifier of Ziller's table of missing differences, k = 18–30 |
| `code/classifier/` | classifier delay/blocked-birth, closure of the table (pairs/triples), rescue check |
| `code/sat_check/` | independent check with a SAT model solved by Google OR-Tools CP-SAT |
| `code/brute_force/` | full-cycle brute-force verification of all theorems, the "sieve laboratory", the audit |
| `code/analysis/` | birth of maximal gaps, Holt's models for gaps 84–104, reproduction of Holt's Figure 6 |
| `paper/` | the paper: LaTeX source and PDF (preprint, doi:10.5281/zenodo.23007183) |
| `docs/` | working notes with all statements and proofs (Polish, v5) |

## Running

Python 3.10+ and `numpy`; `ortools` for `code/sat_check` (CPython, not PyPy). Quick checks (minutes):

```
cd code/brute_force && python bf.py && python kon.py && python nar.py && python pakiet.py && python audyt.py
cd code/analysis   && python holt_models.py ../../data/nG47.csv && python holt_fig6.py
```

The engine, the verifier and the classifier were run in JupyterLab on Windows with multiprocessing. Each component consists of a cell **A**, which writes a worker module to disk, and a cell **B**, which loads it and runs the computation; paste them as two separate notebook cells. Long runs took from minutes to about a day on 16 cores.

## Third-party data (not included)

- Holt's population data for G(37#): <https://github.com/fbholt/Primegaps-v2>
- Complete lists of maximal configurations for n ≤ 54: ancillary file `remainders.txt` of M. Ziller and J. F. Morack, arXiv:1611.03310
- OEIS A048670 table with start positions (R. Gerbicz; values n = 62–64 computed by A. Bożek): <https://oeis.org/A048670>

## References

- F. B. Holt, H. Rudd, *Combinatorics of the gaps between primes*, arXiv:1510.00743 (2015)
- F. B. Holt, *Models for gaps g = 2p₁*, arXiv:2309.16833 (2023)
- F. B. Holt, *Eratosthenes sieve supports the k-tuple conjecture*, arXiv:2502.20470 (2025)
- F. B. Holt, *Discrete dynamics of Eratosthenes sieve*, arXiv:2608.26384 (2026)
- M. Ziller, *On differences between consecutive numbers coprime to primorials*, arXiv:2007.01808 (2020)
- M. Ziller, J. F. Morack, *Algorithmic concepts for the computation of Jacobsthal's function*, arXiv:1611.03310 (2016)
- T. Hagedorn, *Computation of Jacobsthal's function h(n) for n < 50*, Math. Comp. 78 (2009), 1073–1087
- L. Hajdu, N. Saradha, *Disproof of a conjecture of Jacobsthal*, Math. Comp. 81 (2012), 2461–2471

## How to cite

The paper: T. Hojka, *Exact dynamics of Eratosthenes sieve beyond 2p: coincident fusions, births of gaps and missing differences*, preprint (2026), doi:10.5281/zenodo.23007183.

The code and data: T. Hojka, *Eratosthenes sieve dynamics beyond 2p: code, data and verification*, version v1.0.0 (2026), doi:10.5281/zenodo.23009305.

## AI assistance

Parts of the code, the computations and the drafting were carried out with the assistance of Claude, an AI model by Anthropic. The author takes full responsibility for the content.

## Language

Code comments and working notes are in Polish; the paper is in English.

## License

Code: MIT (`LICENSE`). Data and documents: CC BY 4.0 (`LICENSE-DATA`).
